"""Host-side LLM proxy: Anthropic Messages API over a Unix socket -> Vertex AI.

Sandboxed harnesses talk to this proxy only. It maps every request to the backend model
registered for the caller's token, strips sampling params, enforces per-token and global USD
budgets, and appends one usage line per call to a JSONL ledger.
"""
import json, os, sys, time, threading, random, socketserver, http.server, argparse, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anthropic, hmac, hashlib, base64
from anthropic import AnthropicVertex

SECRET_PATH = os.path.expanduser('~/shi_eval/ledger/proxy_secret')

def make_token(payload, secret):
    b = base64.urlsafe_b64encode(json.dumps(payload, sort_keys=True).encode()).decode().rstrip('=')
    sig = base64.urlsafe_b64encode(hmac.new(secret, b.encode(), hashlib.sha256).digest()).decode().rstrip('=')
    return f'v1.{b}.{sig}'

def verify_token(token, secret):
    try:
        v, b, sig = token.split('.')
        if v != 'v1': return None
        want = base64.urlsafe_b64encode(hmac.new(secret, b.encode(), hashlib.sha256).digest()).decode().rstrip('=')
        if not hmac.compare_digest(want, sig): return None
        return json.loads(base64.urlsafe_b64decode(b + '=' * (-len(b) % 4)))
    except Exception:
        return None

PRICES = {  # USD per MTok: input, output, cache_write_5m, cache_read ; long-context tier for haiku-5-5
    'claude-haiku-5-5': (0.10, 0.50, 0.125, 0.01),
    'claude-haiku-5-5@long': (0.50, 2.50, 0.625, 0.05),
    'claude-sonnet-5-5': (2.00, 10.00, 2.50, 0.20),
    'claude-opus-5-5': (4.00, 20.00, 5.00, 0.20),
    'claude-haiku-4-5': (1.00, 5.00, 1.25, 0.10),
    'claude-sonnet-4-6': (3.00, 15.00, 3.75, 0.30),
}
ALLOWED = {'messages', 'system', 'max_tokens', 'tools', 'tool_choice', 'stop_sequences', 'metadata',
           'output_config', 'thinking', 'cache_control'}

def cost_usd(model, u):
    inp = u.get('input_tokens', 0) or 0; out = u.get('output_tokens', 0) or 0
    cw = u.get('cache_creation_input_tokens', 0) or 0; cr = u.get('cache_read_input_tokens', 0) or 0
    key = model
    if model == 'claude-haiku-5-5' and inp + cw + cr > 100_000: key = 'claude-haiku-5-5@long'
    p = PRICES.get(key, (5, 25, 6.25, 0.5))
    return (inp * p[0] + out * p[1] + cw * p[2] + cr * p[3]) / 1e6

class State:
    def __init__(self, registry, ledger, global_cap, stopfile):
        self.registry_path = registry; self.ledger_path = ledger; self.global_cap = global_cap
        self.stopfile = stopfile; self.cap_file = os.path.join(os.path.dirname(ledger), 'global_cap.txt'); self.lock = threading.Lock(); self.reg = {}; self.reg_mtime = 0
        self.spent = {}; self.total = 0.0; self.clients = {}; self.by_run = {}
        if os.path.exists(ledger):  # resume totals
            for line in open(ledger):
                try: r = json.loads(line)
                except Exception: continue
                self.spent[r['token']] = self.spent.get(r['token'], 0) + r['usd']; self.total += r['usd']
                self._acc_run(r)
    def _acc_run(self, r):
        a = self.by_run.setdefault(r.get('run', ''), {'usd': 0.0, 'calls': 0, 'inp': 0, 'out': 0, 'cr': 0, 'cw': 0, 'errors': 0})
        a['usd'] += r.get('usd', 0) or 0; a['calls'] += 1
        for k in ('inp', 'out', 'cr', 'cw'): a[k] += r.get(k) or 0
        if r.get('status') != 200: a['errors'] += 1
    def lookup(self, token):
        if token and token.startswith('v1.'):
            if not hasattr(self, 'secret'): self.secret = open(SECRET_PATH, 'rb').read()
            return verify_token(token, self.secret)
        try:
            m = os.path.getmtime(self.registry_path)
            if m != self.reg_mtime:
                with open(self.registry_path) as f: self.reg = json.load(f)
                self.reg_mtime = m
        except FileNotFoundError: self.reg = {}
        return self.reg.get(token)
    def client(self, region='global'):
        with self.lock:
            if region not in self.clients:
                self.clients[region] = AnthropicVertex(project_id='__CLOUD_PROJECT__', region=region, max_retries=0, timeout=600)
            return self.clients[region]
    def record(self, rec):
        with self.lock:
            self.spent[rec['token']] = self.spent.get(rec['token'], 0) + rec['usd']; self.total += rec['usd']
            self._acc_run(rec)
            with open(self.ledger_path, 'a') as f: f.write(json.dumps(rec) + '\n')

def synthetic_stop(model, text):
    return {'id': 'msg_budget', 'type': 'message', 'role': 'assistant', 'model': model,
            'content': [{'type': 'text', 'text': text}], 'stop_reason': 'end_turn', 'stop_sequence': None,
            'usage': {'input_tokens': 0, 'output_tokens': 0}}

class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *a): pass
    def send_json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        st = self.server.state
        from urllib.parse import urlparse, parse_qs
        u = urlparse(self.path); q = parse_qs(u.query)
        if u.path == '/spent':
            runs = q.get('run', [])
            if runs:
                return self.send_json(200, {r: st.by_run.get(r, {'usd': 0.0, 'calls': 0}) for r in runs})
            return self.send_json(200, {'total': st.total, 'cap': st.global_cap, 'runs': len(st.by_run)})
        if u.path == '/prefix':
            pre = q.get('p', [''])[0]
            agg = {'usd': 0.0, 'calls': 0, 'runs': 0}
            for r, a in st.by_run.items():
                if r.startswith(pre): agg['usd'] += a['usd']; agg['calls'] += a['calls']; agg['runs'] += 1
            return self.send_json(200, agg)
        return self.send_json(404, {'error': 'not found'})
    def do_POST(self):
        st = self.server.state
        n = int(self.headers.get('Content-Length', 0)); body = self.rfile.read(n)
        token = self.headers.get('x-api-key') or (self.headers.get('Authorization', '').replace('Bearer ', ''))
        if not self.path.rstrip('/').endswith('/v1/messages'):
            return self.send_json(404, {'type': 'error', 'error': {'type': 'not_found_error', 'message': 'only /v1/messages'}})
        ent = st.lookup(token)
        if ent is None:
            return self.send_json(401, {'type': 'error', 'error': {'type': 'authentication_error', 'message': 'unknown token'}})
        try: req = json.loads(body)
        except Exception:
            return self.send_json(400, {'type': 'error', 'error': {'type': 'invalid_request_error', 'message': 'bad json'}})
        model = ent['model']
        if os.path.exists(st.stopfile):
            return self.send_json(200, synthetic_stop(model, '[proxy stopped]'))
        try: st.global_cap = float(open(st.cap_file).read().strip())
        except Exception: pass
        if st.spent.get(token, 0) >= ent.get('budget_usd', 1.0) or st.total >= st.global_cap:
            return self.send_json(200, synthetic_stop(model, '[budget exhausted]'))
        params = {k: v for k, v in req.items() if k in ALLOWED}
        params['max_tokens'] = min(int(params.get('max_tokens', 4096)), ent.get('max_tokens_cap', 16000))
        if ent.get('force_thinking') is not None: params['thinking'] = ent['force_thinking']
        if ent.get('force_effort'): params['output_config'] = {'effort': ent['force_effort']}
        tc = params.get('tool_choice')
        if isinstance(tc, dict) and tc.get('type') in ('any', 'tool') and ent.get('no_forced_tools'):
            params['tool_choice'] = tc = {'type': 'auto'}
        if params.get('tools') and ent.get('single_tool_call', True):
            # compatibility shim: 2025-era harness loops handle one tool_use per response (as Claude 3.5 did)
            tc = dict(tc) if isinstance(tc, dict) else {'type': 'auto'}
            if tc.get('type') in ('auto', 'any', 'tool'): tc['disable_parallel_tool_use'] = True
            params['tool_choice'] = tc
        t0 = time.time(); err = None; resp = None
        if model.startswith('gemini') or model.startswith('openai/'):
            import translate
            d = None
            for attempt in range(6):
                try:
                    d = translate.call(model, params); break
                except Exception as e:
                    err = e; time.sleep(min(60, 2 ** attempt + random.random()))
            rec = {'ts': round(t0, 3), 'token': token, 'run': ent.get('run', ''), 'model': model,
                   'req_model': req.get('model'), 'lat': round(time.time() - t0, 2)}
            if d is None:
                rec.update(usd=0.0, status=502, err=str(err)[:300]); st.record(rec)
                return self.send_json(502, {'type': 'error', 'error': {'type': 'api_error', 'message': str(err)[:500]}})
            u = d['usage']
            rec.update(usd=round(translate.cost(model, u), 8), status=200, inp=u.get('input_tokens'), out=u.get('output_tokens'),
                       cw=0, cr=0, stop=d.get('stop_reason'))
            st.record(rec)
            return self.send_json(200, d)
        for attempt in range(8):
            try:
                resp = st.client(ent.get('region', 'global')).messages.create(model=model, **params)
                break
            except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
                err = e; time.sleep(min(60, 2 ** attempt + random.random()))
            except anthropic.APIStatusError as e:
                err = e; break
        rec = {'ts': round(t0, 3), 'token': token, 'run': ent.get('run', ''), 'model': model,
               'req_model': req.get('model'), 'lat': round(time.time() - t0, 2)}
        if resp is None:
            code = getattr(err, 'status_code', 502) or 502
            msg = str(getattr(err, 'message', err))
            if 'too long' in msg.lower() or 'context' in msg.lower() and 'exceed' in msg.lower():
                msg = 'Input is too long for requested model.'
            rec.update(usd=0.0, status=code, err=msg[:300]); st.record(rec)
            return self.send_json(code, {'type': 'error', 'error': {'type': 'api_error' if code >= 500 else 'invalid_request_error', 'message': msg}})
        d = resp.to_dict()
        if ent.get('strip_thinking', True):
            d['content'] = [b for b in d.get('content', []) if b.get('type') not in ('thinking', 'redacted_thinking')]
        u = d.get('usage', {}) or {}
        rec.update(usd=round(cost_usd(model, u), 8), status=200, inp=u.get('input_tokens'), out=u.get('output_tokens'),
                   cw=u.get('cache_creation_input_tokens'), cr=u.get('cache_read_input_tokens'), stop=d.get('stop_reason'))
        st.record(rec)
        return self.send_json(200, d)

class Server(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True
    def get_request(self):  # UnixStreamServer returns '' as address; BaseHTTPRequestHandler wants a tuple
        req, _ = super().get_request(); return req, ('uds', 0)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--sock', required=True); ap.add_argument('--registry', required=True)
    ap.add_argument('--ledger', required=True); ap.add_argument('--global-cap', type=float, required=True)
    ap.add_argument('--stopfile', default=os.path.expanduser('~/shi_eval/STOP'))
    a = ap.parse_args()
    if os.path.exists(a.sock): os.unlink(a.sock)
    srv = Server(a.sock, Handler); os.chmod(a.sock, 0o666)
    srv.state = State(a.registry, a.ledger, a.global_cap, a.stopfile)
    print(f'proxy up sock={a.sock} spent_so_far={srv.state.total:.4f} cap={a.global_cap}', flush=True)
    srv.serve_forever()

"""ADAS evaluation (Hu, Lu, Clune 2024; github.com/ShengranHu/ADAS @ 2702bee8) with only the model call changed.

ADAS's own modules are imported unmodified from ext/adas_repo/_<domain>/ (search.py, utils.py, <domain>_prompt.py):
LLMAgentBase, Info, the role/format instructions, the test-set sampling (evaluate_forward_fn with SEARCHING_MODE=False)
and the scoring run as written. What is replaced, all at the model-call boundary or in the driver:
  1. search.get_json_response_from_gpt -> get_json_response_from_claude: claude-haiku-5-5 through the study proxy
     (Anthropic Messages over the Unix socket; the token sets the model; the proxy strips temperature, so every agent
     samples at the default temperature; default adaptive thinking). max_tokens is 16000, not ADAS's 4096: the model
     thinks before it answers and those tokens count against max_tokens, so at 4096 replies were cut off (GPQA smoke
     test: 20 of 85 calls). Calls with more than 4096 output tokens are flagged ('over4096').
     JSON adapter, identical for every agent and logged per call: json.loads of the whole reply (what ADAS does with
     OpenAI JSON mode) -> a ```json fenced block -> the first JSON object embedded in the reply -> a Python dict literal
     -> values located by the requested field names. The last two exist because ADAS's format example is a Python dict
     repr ({'thinking': 'Your thinking.', ...}) that Claude sometimes copies, often with apostrophes inside the values;
     OpenAI JSON mode made gpt-3.5 emit valid JSON whatever the example looked like. Non-string field values are turned
     into strings and the fields are put in the requested order: the gpt-3.5 JSON-mode contract the archived agents
     were written against (e.g. MMLU's best agent calls .strip() on its 'confidence' field).
  2. search.ThreadPoolExecutor -> TaggedExecutor: tags each question's calls (run adas_p4|<domain>|<agent>|<qid>), runs
     only the first `limit` questions (pilot), and returns None for a question whose forward() raises, which ADAS's
     scorer counts as 0 (ADAS itself would abort the whole evaluation on the first exception).
  3. openai and backoff are stubbed (not installed here; nothing calls them after 1.); tqdm is silenced.
One domain per process: all four domains import a module named 'utils'.
"""
import ast, importlib.util, json, os, random, re, sys, threading, time, types
import concurrent.futures as cf
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import run_task, llm_proxy

ADAS = os.path.expanduser('~/shi_eval/ext/adas_repo')
ARCHIVES = os.path.expanduser('~/shi_eval/ext/adas')
MODEL = 'claude-haiku-5-5'
MAX_TOKENS = 16000  # ADAS: 4096 (no hidden reasoning in gpt-3.5); see the module docstring
BUDGET_USD = 0.20   # per (agent, question) token
DOMAINS = ('mgsm', 'drop', 'gpqa', 'mmlu')
_TL = threading.local()
STOP = threading.Event()   # no new questions: set on a proxy '[budget exhausted]' / '[proxy stopped]' answer or by a spend guard


class _NonRetryable(Exception):
    pass


def _post(body, tok):
    data = json.dumps(body); err = None
    for attempt in range(4):
        try:
            c = run_task._UDSConn(run_task.SOCK); c.timeout = 900
            c.request('POST', '/v1/messages', body=data, headers={'content-type': 'application/json', 'x-api-key': tok})
            r = json.loads(c.getresponse().read()); c.close()
            if r.get('type') == 'error':
                if (r.get('error') or {}).get('type') == 'invalid_request_error': raise _NonRetryable(str(r)[:300])
                raise RuntimeError(str(r)[:300])
            return r
        except _NonRetryable:
            raise
        except Exception as e:
            err = e; time.sleep(5 * (attempt + 1))
    raise err


_DEC = json.JSONDecoder(strict=False)
_FENCE = re.compile(r'```(?:json)?[ \t]*\n?(.*?)```', re.DOTALL | re.IGNORECASE)


def _blocks(text):
    """Candidate object texts: each fenced block's content, then the span from the first '{' to the last '}'."""
    out = [m.group(1).strip() for m in _FENCE.finditer(text)]
    i, j = text.find('{'), text.rfind('}')
    if 0 <= i < j: out.append(text[i:j + 1])
    return out


def keyed_parse(block, keys):
    """Values located by the requested field names ('key': or "key":), each running to the next key or the closing
    brace; surrounding quotes stripped. For dict-style replies whose values contain unescaped quotes."""
    if not keys or not block.startswith('{') or not block.endswith('}'): return None
    found = []
    for k in keys:
        m = re.search(r'["\']' + re.escape(k) + r'["\']\s*:\s*', block)
        if m is None: return None
        found.append((m.start(), m.end(), k))
    found.sort()
    vals = {}
    for n, (s, e, k) in enumerate(found):
        end = found[n + 1][0] if n + 1 < len(found) else len(block) - 1
        if end < e: return None
        v = block[e:end].rstrip()
        if v.endswith(','): v = v[:-1].rstrip()
        elif n + 1 < len(found): return None
        if len(v) >= 2 and v[0] == v[-1] and v[0] in '\'"': v = v[1:-1]
        vals[k] = v.replace("\\'", "'").replace('\\"', '"').replace('\\n', '\n')
    return {k: vals[k] for k in keys}


def extract_json(text, keys=None):
    """(object, how): json.loads of the whole reply as ADAS does, else a fenced block, else the first decodable JSON
    object, else a Python dict literal, else values located by the requested keys."""
    try:
        d = json.loads(text)
        if isinstance(d, dict): return d, 'direct'
    except Exception:
        pass
    for m in _FENCE.finditer(text):
        try:
            d = _DEC.decode(m.group(1).strip())
            if isinstance(d, dict): return d, 'fenced'
        except Exception:
            pass
    i = text.find('{')
    while i >= 0:
        try:
            d, _ = _DEC.raw_decode(text, i)
            if isinstance(d, dict): return d, 'embedded'
        except Exception:
            pass
        i = text.find('{', i + 1)
    for b in _blocks(text):
        try:
            d = ast.literal_eval(b)
            if isinstance(d, dict): return d, 'pyliteral'
        except Exception:
            pass
    for b in _blocks(text):
        d = keyed_parse(b, keys)
        if d is not None: return d, 'keyed'
    return None, 'fail'


_FMT_HEAD = 'Reply EXACTLY with the following JSON format.\n'


def requested_keys(system_message):
    """Field names in the order LLMAgentBase wrote them into FORMAT_INST (a dict repr on the line after the header)."""
    i = system_message.find(_FMT_HEAD)
    if i < 0: return None
    try:
        return list(ast.literal_eval(system_message[i + len(_FMT_HEAD):].split('\n', 1)[0]).keys())
    except Exception:
        return None


def _to_str(v):
    if isinstance(v, str): return v, None
    if v is None: return '', 'null'
    if isinstance(v, bool): return ('true' if v else 'false'), 'bool'
    if isinstance(v, (int, float)): return str(v), type(v).__name__
    return json.dumps(v, ensure_ascii=False), type(v).__name__


def get_json_response_from_claude(msg, model, system_message, temperature=0.5):
    """Drop-in for ADAS's get_json_response_from_gpt: returns the reply's JSON object; raises when there is none,
    which LLMAgentBase.query turns into empty fields exactly as in ADAS."""
    ctx = getattr(_TL, 'ctx', None)
    if ctx is None: raise RuntimeError('model call outside a tagged question')
    rec = {'n': len(ctx.calls), 'temp_req': temperature}
    ctx.calls.append(rec)
    body = {'model': MODEL, 'max_tokens': MAX_TOKENS, 'system': system_message,
            'messages': [{'role': 'user', 'content': msg}]}
    t0 = time.time()
    try:
        r = _post(body, ctx.tok)
    except Exception as e:
        rec.update(parse='api_error', err=str(e)[:200], lat=round(time.time() - t0, 1)); raise
    u = r.get('usage') or {}
    text = ''.join(b.get('text', '') for b in r.get('content', []) if b.get('type') == 'text')
    rec.update(lat=round(time.time() - t0, 1), stop=r.get('stop_reason'), inp=u.get('input_tokens') or 0,
               out=u.get('output_tokens') or 0, usd=round(llm_proxy.cost_usd(MODEL, u), 7))
    if rec['out'] > 4096: rec['over4096'] = 1
    if r.get('id') == 'msg_budget':
        STOP.set(); rec.update(parse='proxy_stop', err=text[:80]); raise RuntimeError(text)
    want = requested_keys(system_message)
    d, how = extract_json(text, want)
    rec['parse'] = how
    if how in ('pyliteral', 'keyed', 'fail'): rec['raw'] = text[:3000]
    if d is None: raise ValueError('no JSON object in the reply')
    if want is not None and set(d) == set(want) and list(d) != want:
        d = {k: d[k] for k in want}; rec['reordered'] = 1
    coerced = []
    for k in list(d):
        d[k], t = _to_str(d[k])
        if t: coerced.append(t)
    if coerced: rec['coerced'] = coerced
    if want is not None and set(d) != set(want): rec['keys'] = sorted(d)[:8]   # LLMAgentBase.query fills / drops
    return d


class Ctx:
    def __init__(self, domain, agent, qid):
        self.run = f'adas_p4|{domain}|{agent}|{qid}'
        self.tok = run_task.mint(self.run, MODEL, BUDGET_USD, single_tool_call=False)
        self.calls = []


_EVAL = None   # the Evaluation whose evaluate_forward_fn is running in this process


class TaggedExecutor(cf.ThreadPoolExecutor):
    """Stands in for ThreadPoolExecutor inside ADAS's evaluate_forward_fn (module docstring, change 2)."""
    def map(self, fn, *iterables, **kw):
        ev = _EVAL
        return super().map(lambda pair: ev.run_one(fn, *pair), enumerate(iterables[0]))


def _stub(name, **attrs):
    m = types.ModuleType(name); m.__dict__.update(attrs); return m


class _NoOpenAI:
    def __init__(self, *a, **k): pass


def load_domain(domain):
    """Import ADAS's search/utils/prompt modules for `domain` and apply changes 1-3. Returns (search, utils)."""
    assert domain in DOMAINS
    sys.modules['openai'] = _stub('openai', OpenAI=_NoOpenAI, RateLimitError=type('RateLimitError', (Exception,), {}))
    sys.modules['backoff'] = _stub('backoff', expo=None, on_exception=lambda *a, **k: (lambda f: f))
    os.chdir(ADAS)   # ADAS reads its datasets by relative path (dataset/...) from the repo root
    mods = []
    for name, fn in (('utils', 'utils.py'), (f'{domain}_prompt', f'{domain}_prompt.py'), (f'adas_search_{domain}', 'search.py')):
        spec = importlib.util.spec_from_file_location(name, os.path.join(ADAS, '_' + domain, fn))
        m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m); mods.append(m)
    U, S = mods[0], mods[2]
    S.get_json_response_from_gpt = get_json_response_from_claude
    S.ThreadPoolExecutor = TaggedExecutor
    S.tqdm = lambda it, **k: it
    S.SEARCHING_MODE = False
    return S, U


def adas_args(domain, **over):
    """argparse defaults of ADAS's search.py for `domain`, read from its source, plus overrides."""
    src = open(os.path.join(ADAS, '_' + domain, 'search.py')).read()
    a = {}
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Call) and getattr(node.func, 'attr', '') == 'add_argument':
            for kw in node.keywords:
                if kw.arg == 'default': a[node.args[0].value.lstrip('-')] = ast.literal_eval(kw.value)
    a.update(over)
    return types.SimpleNamespace(**a)


def test_items(U, domain, args):
    """(task text, gold) per test item, rebuilt as in ADAS's evaluate_forward_fn; used for diagnostics and checked
    against the task each forward() receives."""
    if domain == 'gpqa':
        qs = U.load_questions(args.data_filename, seed=0)[args.valid_size:] * args.n_repreat
        return [(f"What is the correct answer to this question: {q.question}"
                 + f"\n\nChoices:\n(A) {q.choice1}\n(B) {q.choice2}\n(C) {q.choice3}\n(D) {q.choice4}",
                 'ABCD'[q.correct_index]) for q in qs]
    if domain == 'mgsm':
        ex = U.get_all_examples(); random.seed(args.shuffle_seed)
    elif domain == 'drop':
        ex = U.load_drop(args.data_filename)[1:-1]; random.seed(args.shuffle_seed)
    else:
        import pandas
        df = pandas.read_csv(args.data_filename); random.seed(args.shuffle_seed)
        ex = [row.to_dict() for _, row in df.iterrows()]
    random.shuffle(ex)
    ex = ex[args.valid_size:args.valid_size + args.test_size] * args.n_repreat
    if domain == 'mmlu': return [(U.format_multichoice_question(e), e['Answer']) for e in ex]
    return [(e['inputs'], e['targets']) for e in ex]


class Evaluation:
    def __init__(self, S, domain, agent, items, limit, partial_path=None):
        self.S, self.domain, self.agent, self.items, self.limit = S, domain, agent, items, limit
        self.records = {}
        self.lock = threading.Lock()
        self.partial = open(partial_path, 'a') if partial_path else None   # one line per finished question (no score yet)

    def run_one(self, fn, idx, task):
        if (self.limit is not None and idx >= self.limit) or STOP.is_set(): return None
        ctx = Ctx(self.domain, self.agent, f'q{idx:04d}')
        _TL.ctx = ctx
        t0 = time.time(); res = None; err = None
        try:
            res = fn(task)
        except Exception as e:
            err = f'{type(e).__name__}: {e}'[:300]
        finally:
            _TL.ctx = None
        s = run_task.spent(runs=[ctx.run]).get(ctx.run, {})
        pred = res.content if isinstance(res, self.S.Info) else res
        self.records[idx] = {'domain': self.domain, 'agent': self.agent, 'idx': idx, 'run': ctx.run,
                             'task_ok': task.content == self.items[idx][0], 'gold': self.items[idx][1],
                             'pred': repr(pred)[:200], 'agent_error': err, 'calls': len(ctx.calls),
                             'usd_proxy': round(s.get('usd', 0.0), 7), 'calls_proxy': s.get('calls', 0),
                             'usd_local': round(sum(c.get('usd', 0) for c in ctx.calls), 7),
                             'wall': round(time.time() - t0, 1), 'call_log': ctx.calls}
        if self.partial:
            with self.lock:
                self.partial.write(json.dumps(self.records[idx]) + '\n'); self.partial.flush()
        return res

    def run(self, code, args):
        """ADAS's evaluate_forward_fn on `code`; returns the per-question records (first `limit`) with ADAS's score."""
        global _EVAL
        _EVAL = self
        acc = self.S.evaluate_forward_fn(args, code)
        out = []
        for idx in sorted(self.records):
            r = self.records[idx]; r['score'] = float(acc[idx]); out.append(r)
        return out


def archive(domain):
    return json.load(open(f'{ARCHIVES}/{domain}_gpt3.5_results.json'))


def median(s):
    m = re.search(r'Median: ([\-0-9.]+)%', s or '')
    return float(m.group(1)) if m else float('-inf')

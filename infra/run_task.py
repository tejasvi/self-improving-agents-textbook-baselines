"""Run a (possibly self-modified) DGM-style harness on one LCB task inside the sandbox, then grade it."""
import json, os, sys, time, shutil, http.client, socket
sys.path.insert(0, os.path.dirname(__file__))
import sandbox, lcb
from llm_proxy import make_token, SECRET_PATH
SHI = os.path.expanduser('~/shi_eval')
SOCK = os.environ.get('SHI_PROXY_SOCK', os.path.join(SHI, 'ledger', 'proxy.sock'))
_SECRET = None

def mint(run, model, budget, **kw):
    global _SECRET
    if _SECRET is None: _SECRET = open(SECRET_PATH, 'rb').read()
    return make_token(dict(run=run, model=model, budget_usd=budget, **kw), _SECRET)

class _UDSConn(http.client.HTTPConnection):
    def __init__(self, path): super().__init__('localhost', timeout=30); self._path = path
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); self.sock.connect(self._path)

def spent(runs=None, prefix=None):
    c = _UDSConn(SOCK)
    if prefix is not None: c.request('GET', '/prefix?p=' + prefix)
    elif runs: c.request('GET', '/spent?' + '&'.join('run=' + r for r in runs))
    else: c.request('GET', '/spent')
    return json.loads(c.getresponse().read())

def run_agent(agent_dir, task, run_id, outdir, model='claude-haiku-5-5', budget=0.25, timeout=900,
              keep_repo=False, extra_tok=None, entry='coding_agent.py'):
    """Returns result dict. outdir is created; logs kept there."""
    if os.path.exists(outdir): shutil.rmtree(outdir)
    os.makedirs(os.path.join(outdir, 'out'))
    repo = os.path.join(outdir, 'repo')
    base = lcb.make_repo(task, repo)
    tok = mint(run_id, model, budget, **(extra_tok or {}))
    ps = lcb.problem_statement(task)
    cmd = ['python3', f'/agent/{entry}', '--problem_statement', ps, '--git_dir', '/work/repo',
           '--base_commit', base, '--chat_history_file', '/work/out/chat.md', '--outdir', '/work/out',
           '--language', 'python']
    t0 = time.time()
    r = sandbox.run(cmd, rw=[(outdir, '/work')], ro=[(agent_dir, '/agent')], sock=SOCK, cwd='/agent',
                    env={'ANTHROPIC_BASE_URL': 'http://127.0.0.1:8080', 'ANTHROPIC_API_KEY': tok},
                    timeout=timeout, mem_gb=6)
    wall = time.time() - t0
    with open(os.path.join(outdir, 'out', 'agent_stderr.txt'), 'wb') as f: f.write(r['err'][-200000:])
    with open(os.path.join(outdir, 'out', 'agent_stdout.txt'), 'wb') as f: f.write(r['out'][-200000:])
    sol_path = os.path.join(repo, 'solution.py')
    code = open(sol_path).read() if os.path.exists(sol_path) else ''
    empty = code.strip() == lcb.stub(task).strip() or not code.strip()
    g = lcb.grade(task, code) if not empty else {'passed': False, 'first_fail': {'kind': 'empty_patch'}}
    chat = os.path.join(outdir, 'out', 'chat.md')
    conn_err = False
    if os.path.exists(chat):
        with open(chat, errors='replace') as f: conn_err = 'Connection error' in f.read()
    s = spent(runs=[run_id]).get(run_id, {})
    res = {'run': run_id, 'task': task['id'], 'passed': bool(g.get('passed')), 'empty': empty, 'grade': g,
           'agent_rc': r['rc'], 'agent_timed_out': r['timed_out'], 'wall': round(wall, 1), 'conn_err': conn_err,
           'usd': round(s.get('usd', 0.0), 6), 'calls': s.get('calls', 0), 'inp': s.get('inp', 0), 'out': s.get('out', 0)}
    with open(os.path.join(outdir, 'result.json'), 'w') as f: json.dump(res, f, indent=1)
    if not keep_repo:
        shutil.rmtree(os.path.join(repo, '.git'), ignore_errors=True)
    return res

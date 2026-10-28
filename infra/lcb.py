"""LiveCodeBench task access, task-repo construction and sandboxed grading."""
import json, os, subprocess, tempfile, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import sandbox
SHI = os.path.expanduser('~/shi_eval')
DATA = os.path.join(SHI, 'data', 'lcb')
DRIVER = os.path.join(SHI, 'infra', 'grade_driver_v2.py')
_INDEX = None

def index():
    global _INDEX
    if _INDEX is None:
        _INDEX = {t['id']: t for t in (json.loads(l) for l in open(os.path.join(DATA, 'index.jsonl')))}
    return _INDEX

def tests_path(tid):
    return os.path.join(DATA, 'tests', tid + '.json')

def problem_statement(t):
    s = t['statement'].replace('\r\n', '\n').strip()
    if t['testtype'] == 'stdin':
        how = ("Write a complete Python 3 program in `solution.py` that reads the input from standard input and "
               "prints the answer to standard output, exactly in the format described above. "
               "Your program will be run against hidden test cases (including larger inputs within the constraints), "
               "so it must be correct and efficient.")
    else:
        how = ("Implement the method in `solution.py`, completing the `Solution` class given by the starter code "
               f"(method `{t['func_name']}`). Your code will be imported and the method called on hidden test cases, "
               "so it must be correct and efficient. Do not read from standard input.")
    return f"# {t['title']}\n\n{s}\n\n## Task\n\n{how}\n"

def stub(t):
    if t['testtype'] == 'stdin':
        return "# Write your solution here. Read from stdin, write to stdout.\n"
    sc = t['starter_code'].rstrip()
    return sc + "\n        pass\n" if sc.endswith(':') else sc + "\n"

def make_repo(t, root):
    """Create a git repo for task t under root; returns base commit sha."""
    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, 'README.md'), 'w') as f: f.write(problem_statement(t))
    with open(os.path.join(root, 'solution.py'), 'w') as f: f.write(stub(t))
    env = dict(os.environ, GIT_AUTHOR_NAME='task', GIT_AUTHOR_EMAIL='t@l', GIT_COMMITTER_NAME='task', GIT_COMMITTER_EMAIL='t@l')
    subprocess.run(['git', 'init', '-q'], cwd=root, check=True)
    subprocess.run(['git', 'add', '-A'], cwd=root, check=True, env=env)
    subprocess.run(['git', 'commit', '-q', '-m', 'task'], cwd=root, check=True, env=env)
    return subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()

def grade(t, code, per_test=6.0, max_total=90.0, tmp_root=None):
    d = tempfile.mkdtemp(prefix='grade_', dir=tmp_root or os.path.join(SHI, 'tmp'))
    try:
        with open(os.path.join(d, 'solution.py'), 'w') as f: f.write(code)
        r = sandbox.run(['python3', '/opt/grade_driver.py', t['testtype'], '/work/solution.py', '/tests.json',
                         t.get('func_name') or '-', str(per_test), str(max_total)],
                        rw=[(d, '/work')], ro=[(DRIVER, '/opt/grade_driver.py'), (tests_path(t['id']), '/tests.json')],
                        timeout=max_total + 60, mem_gb=4)
        try:
            res = json.loads(r['out'].decode().strip().splitlines()[-1])
        except Exception:
            res = {'passed': False, 'first_fail': {'kind': 'grader_error', 'stderr': r['err'].decode()[-1000:]},
                   'timed_out': r['timed_out']}
        return res
    finally:
        shutil.rmtree(d, ignore_errors=True)

def grade_public(t, code, per_test=6.0, max_total=60.0, tmp_root=None):
    """Grade against the statement's public (sample) tests only (what an agent can check before submitting)."""
    d = tempfile.mkdtemp(prefix='gpub_', dir=tmp_root or os.path.join(SHI, 'tmp'))
    try:
        with open(os.path.join(d, 'solution.py'), 'w') as f: f.write(code)
        pub = json.load(open(tests_path(t['id'])))['public']
        with open(os.path.join(d, 'tests.json'), 'w') as f: json.dump({'public': pub, 'private': []}, f)
        r = sandbox.run(['python3', '/opt/grade_driver.py', t['testtype'], '/work/solution.py', '/work/tests.json',
                         t.get('func_name') or '-', str(per_test), str(max_total)],
                        rw=[(d, '/work')], ro=[(DRIVER, '/opt/grade_driver.py')], timeout=max_total + 60, mem_gb=4)
        try: return json.loads(r['out'].decode().strip().splitlines()[-1])
        except Exception: return {'passed': False, 'first_fail': {'kind': 'grader_error'}}
    finally:
        shutil.rmtree(d, ignore_errors=True)

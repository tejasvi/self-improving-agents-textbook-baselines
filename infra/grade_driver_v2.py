"""Runs INSIDE the sandbox. Grades one LCB solution against tests; prints one JSON line."""
import sys, json, subprocess, time, signal, os, resource
from decimal import Decimal, InvalidOperation
mode, sol, tests_path, func_name, per_test, max_total = sys.argv[1:7]
per_test = float(per_test); max_total = float(max_total)
T = json.load(open(tests_path)); tests = T['public'] + T['private']
# v2: stdin programs run exactly as written (what the agent tests is what is graded); class-method tasks get
# LCB-style imports, ending with `from builtins import *` so no builtin (e.g. 3-argument pow) is shadowed.
HEADER = ("from typing import *\nimport collections, heapq, bisect, itertools, functools, math, string, re, sys\n"
          "from collections import *\nfrom functools import *\nfrom itertools import *\nfrom heapq import *\n"
          "from bisect import *\nfrom math import *\nfrom builtins import *\nsys.setrecursionlimit(1000000)\n")
def tr(s, n=400):
    s = s if isinstance(s, str) else json.dumps(s)
    return s if len(s) <= n else s[:n] + f'...<{len(s)-n} more chars>'
def same_stdout(got, exp):
    g = [l.strip() for l in got.strip().split('\n')]; e = [l.strip() for l in exp.strip().split('\n')]
    if g == e: return True
    gt, et = got.split(), exp.split()
    if len(gt) != len(et): return False
    for a, b in zip(gt, et):
        if a == b: continue
        try:
            if Decimal(a) != Decimal(b):
                if not any(c in a + b for c in '.eE'): return False
                fa, fb = float(a), float(b)   # real-valued answers: absolute/relative error 1e-6
                if abs(fa - fb) > 1e-6 * max(1.0, abs(fb)): return False
        except (InvalidOperation, ValueError):
            return False
    return True
def norm(x):
    if isinstance(x, tuple): x = list(x)
    if isinstance(x, list): return [norm(y) for y in x]
    if isinstance(x, dict): return {k: norm(v) for k, v in x.items()}
    return x
def same_val(a, b):
    a, b = norm(a), norm(b)
    if isinstance(a, float) or isinstance(b, float):
        try: return abs(float(a) - float(b)) <= 1e-6 * max(1.0, abs(float(b)))
        except Exception: return False
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same_val(x, y) for x, y in zip(a, b))
    return a == b
res = {'passed': False, 'n_tests': len(tests), 'n_run': 0, 'first_fail': None}
t0 = time.time()
code = open(sol).read()
if mode == 'stdin':
    path = '/tmp/_sol.py'
    open(path, 'w').write(code)
    for i, t in enumerate(tests):
        if time.time() - t0 > max_total:
            res['first_fail'] = {'idx': i, 'kind': 'total_timeout'}; break
        try:
            p = subprocess.run([sys.executable, path], input=t['input'], capture_output=True, text=True, timeout=per_test)
        except subprocess.TimeoutExpired:
            res['first_fail'] = {'idx': i, 'kind': 'timeout', 'input': tr(t['input']), 'expected': tr(t['output'])}; break
        res['n_run'] = i + 1
        if p.returncode != 0:
            res['first_fail'] = {'idx': i, 'kind': 'runtime_error', 'input': tr(t['input']), 'expected': tr(t['output']),
                                 'got': tr(p.stdout), 'stderr': tr(p.stderr, 1200)}; break
        if not same_stdout(p.stdout, t['output']):
            res['first_fail'] = {'idx': i, 'kind': 'wrong_answer', 'input': tr(t['input']), 'expected': tr(t['output']),
                                 'got': tr(p.stdout)}; break
    else:
        res['passed'] = True
else:
    class TO(Exception): pass
    def on_alarm(*a): raise TO()
    signal.signal(signal.SIGALRM, on_alarm)
    g = {'__name__': '__solution__'}
    try:
        signal.setitimer(signal.ITIMER_REAL, per_test)
        exec(compile(HEADER + code, 'solution.py', 'exec'), g)
        signal.setitimer(signal.ITIMER_REAL, 0)
        cls = g['Solution']
        fn_ok = hasattr(cls(), func_name)
        if not fn_ok: raise AttributeError(f'Solution has no method {func_name}')
    except BaseException as e:
        signal.setitimer(signal.ITIMER_REAL, 0)
        res['first_fail'] = {'idx': -1, 'kind': 'compile_error', 'stderr': tr(f'{type(e).__name__}: {e}', 1200)}
        print(json.dumps(res)); sys.exit(0)
    for i, t in enumerate(tests):
        if time.time() - t0 > max_total:
            res['first_fail'] = {'idx': i, 'kind': 'total_timeout'}; break
        try:
            args = [json.loads(l) for l in t['input'].split('\n') if l.strip()]
            exp = json.loads(t['output'])
        except Exception as e:
            res['first_fail'] = {'idx': i, 'kind': 'bad_test', 'stderr': str(e)}; break
        try:
            signal.setitimer(signal.ITIMER_REAL, per_test)
            out = getattr(cls(), func_name)(*args)
            signal.setitimer(signal.ITIMER_REAL, 0)
        except TO:
            res['first_fail'] = {'idx': i, 'kind': 'timeout', 'input': tr(t['input']), 'expected': tr(t['output'])}; break
        except BaseException as e:
            signal.setitimer(signal.ITIMER_REAL, 0)
            res['first_fail'] = {'idx': i, 'kind': 'runtime_error', 'input': tr(t['input']), 'expected': tr(t['output']),
                                 'stderr': tr(f'{type(e).__name__}: {e}', 1200)}; break
        res['n_run'] = i + 1
        if not same_val(out, exp):
            res['first_fail'] = {'idx': i, 'kind': 'wrong_answer', 'input': tr(t['input']), 'expected': tr(t['output']),
                                 'got': tr(out)}; break
    else:
        res['passed'] = True
res['secs'] = round(time.time() - t0, 2)
print(json.dumps(res))

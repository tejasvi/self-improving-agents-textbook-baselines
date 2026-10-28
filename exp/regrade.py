"""Re-grade saved solutions with the current grader (v2) without re-running agents.

usage: regrade.py results <results.jsonl> <runs_root>      -> writes <results>.v2.jsonl
       regrade.py exp <EXP> [stage ...]                     -> writes agents/<aid>/evals/<stage>.v2.jsonl
Agent runs never see the grader, so a re-grade equals a fresh evaluation under the new grader.
"""
import json, os, sys, glob, concurrent.futures as cf, threading
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import lcb
SHI = os.path.expanduser('~/shi_eval')
I = lcb.index()
assert lcb.DRIVER.endswith('grade_driver_v2.py'), lcb.DRIVER

def regrade_record(r, sol_path):
    if r.get('empty') or not os.path.exists(sol_path):
        g = r.get('grade') or {'passed': False, 'first_fail': {'kind': 'empty_patch'}}
        return dict(r, grade_v1=r.get('grade'), passed_v1=r.get('passed'), passed=False if r.get('empty') else r.get('passed'), grade=g, regraded=False)
    code = open(sol_path, errors='replace').read()
    g = lcb.grade(I[r['task']], code)
    return dict(r, grade_v1=r.get('grade'), passed_v1=r.get('passed'), passed=bool(g.get('passed')), grade=g, regraded=True)

def run(pairs, out_path, workers=8):
    done = set()
    if os.path.exists(out_path):
        for l in open(out_path):
            x = json.loads(l); done.add((x.get('agent', ''), x['task'], x.get('rep', 0), x.get('stage', '')))
    todo = [(r, s) for r, s in pairs if (r.get('agent', ''), r['task'], r.get('rep', 0), r.get('stage', '')) not in done]
    lock = threading.Lock()
    def one(rs):
        nr = regrade_record(*rs)
        with lock:
            with open(out_path, 'a') as f: f.write(json.dumps(nr) + '\n')
    with cf.ThreadPoolExecutor(workers) as ex: list(ex.map(one, todo))
    return len(todo)

if __name__ == '__main__':
    if sys.argv[1] == 'results':
        res, root = sys.argv[2], sys.argv[3]
        pairs = []
        for l in open(res):
            r = json.loads(l)
            pairs.append((r, os.path.join(root, r['agent'].replace('/', '_'), f"{r['task']}_r{r['rep']}", 'repo', 'solution.py')))
        print('regraded', run(pairs, res.replace('.jsonl', '.v2.jsonl')))
    else:
        exp = sys.argv[2]; stages = sys.argv[3:] or ['small', 'medium', 'fresh1', 'fresh2']
        n = 0
        for ad in sorted(glob.glob(os.path.join(SHI, 'exps*', exp, 'agents', '*'))):
            for st in stages:
                p = os.path.join(ad, 'evals', f'{st}.jsonl')
                if not os.path.exists(p): continue
                pairs = []
                for l in open(p):
                    r = json.loads(l)
                    pairs.append((r, os.path.join(ad, 'runs', st, f"{r['task']}_r{r.get('rep', 0)}", 'repo', 'solution.py')))
                n += run(pairs, p.replace('.jsonl', '.v2.jsonl'))
        print(exp, 'regraded', n)

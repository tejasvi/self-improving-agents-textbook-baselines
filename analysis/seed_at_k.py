"""Compute-matched baseline: run the seed k times per task, submit the first solution that passes the statement's
sample (public) tests, else the last attempt. Cost = attempts actually used (stop at the first public pass).

Attempt pools on F1: F_seeds.v2 (3 reps) + F1_seeds_extra (3) + F1_seeds_extra2 (6, DGM seed) + F1_seeds_extra3
(2, strong seed). Accuracy and cost are averaged over random orderings of each task's attempts (200 orderings), so the
curve does not depend on run order. Also returns per-task expected pass at each k for paired comparisons.
Output: results/seed_at_k.json.
"""
import json, os, sys, collections, concurrent.futures as cf
import numpy as np
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import lcb
SHI = os.path.expanduser('~/shi_eval')
SP = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json'))); F1 = SP['fresh'][:116]
I = lcb.index() if os.path.exists(os.path.join(lcb.DATA, 'index.jsonl')) else {}  # supplement: problem texts are not shipped; grades come from the cache
POOLS = [('F_seeds.v2.jsonl', 'F_seeds'), ('F1_seeds_extra.jsonl', 'F1_seeds_extra'),
         ('F1_seeds_extra2.jsonl', 'F1_seeds_extra2'), ('F1_seeds_extra3.jsonl', 'F1_seeds_extra3')]

def attempts(agent):
    out = collections.defaultdict(list)   # task -> list of (passed, usd, solution_path, empty)
    for fn, root in POOLS:
        p = os.path.join(SHI, 'results', fn)
        if not os.path.exists(p): continue
        for l in open(p):
            r = json.loads(l)
            if r['agent'] != agent or r['task'] not in F1: continue
            sol = os.path.join(SHI, 'runs', root, agent, f"{r['task']}_r{r['rep']}", 'repo', 'solution.py')
            out[r['task']].append((bool(r['passed']), r.get('usd', 0.0), sol, bool(r.get('empty'))))
    return out

_cache_path = os.path.join(SHI, 'results', 'public_pass_cache.json')
_cache = json.load(open(_cache_path)) if os.path.exists(_cache_path) else {}

def public_pass(task, sol, empty):
    if empty or not os.path.exists(sol): return False
    key = os.path.relpath(sol, SHI)  # supplement: cache keys are paths relative to the project root
    if key in _cache: return _cache[key]
    v = bool(lcb.grade_public(I[task], open(sol, errors='replace').read()).get('passed'))
    _cache[key] = v; return v

if __name__ == '__main__':
    res = {}; rng = np.random.default_rng(0)
    for agent in ('seed_dgm', 'seed_strong'):
        A = attempts(agent)
        jobs = [(t, i) for t in F1 for i in range(len(A[t]))]
        with cf.ThreadPoolExecutor(12) as ex:
            pubs = dict(zip(jobs, ex.map(lambda ti: public_pass(ti[0], A[ti[0]][ti[1]][2], A[ti[0]][ti[1]][3]), jobs)))
        json.dump(_cache, open(_cache_path, 'w'))
        kmax = min(len(A[t]) for t in F1)
        res[agent] = {'kmax': kmax, 'n_attempts_per_task': {t: len(A[t]) for t in F1}}
        for k in range(1, kmax + 1):
            acc_t = np.zeros(len(F1)); cost_t = np.zeros(len(F1)); orc_t = np.zeros(len(F1))
            for j, t in enumerate(F1):
                n = len(A[t]); a_acc = a_cost = a_orc = 0.0
                for _ in range(200):
                    order = rng.permutation(n)[:k]; c = 0.0; chosen = None
                    for i in order:
                        c += A[t][i][1]
                        if pubs[(t, i)]: chosen = i; break
                    if chosen is None: chosen = order[-1]
                    a_acc += A[t][chosen][0]; a_cost += c; a_orc += any(A[t][i][0] for i in order)
                acc_t[j] = a_acc / 200; cost_t[j] = a_cost / 200; orc_t[j] = a_orc / 200
            res[agent][str(k)] = {'acc': float(acc_t.mean()), 'usd_per_task': float(cost_t.mean()),
                                  'oracle_any_pass': float(orc_t.mean()), 'per_task_acc': dict(zip(F1, acc_t.tolist()))}
            print(agent, k, {kk: round(v, 4) for kk, v in res[agent][str(k)].items() if kk != 'per_task_acc'})
    json.dump(res, open(os.path.join(SHI, 'results', 'seed_at_k.json'), 'w'), indent=1)

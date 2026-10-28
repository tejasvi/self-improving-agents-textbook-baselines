"""Exploratory compute-matched follow-up to H6 (DEVIATIONS entry 'compute-matched follow-up to H6').

L@2: grid_L's two runs per problem (results/F_grid.jsonl); submit the first run (in a given order) whose solution passes
the statement's sample tests, else the second; cost = runs used. Averaged over both orders. Compared with loop 3's best
agent (results/F_ablate.jsonl, 'full', mean over its runs) on all of F (232), paired bootstrap over problems.
Output: results/l_at_k.json.
"""
import collections, json, os, sys
import numpy as np
sys.path.insert(0, os.path.expanduser('~/shi_eval/analysis'))
import seed_at_k as SK
SHI = os.path.expanduser('~/shi_eval')
F = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))['fresh']

def runs(fn, root, agent):
    out = collections.defaultdict(list)
    for l in open(os.path.join(SHI, 'results', fn)):
        r = json.loads(l)
        if r['agent'] != agent: continue
        sol = os.path.join(SHI, 'runs', root, agent, f"{r['task']}_r{r['rep']}", 'repo', 'solution.py')
        out[r['task']].append((bool(r['passed']), r.get('usd') or 0.0, sol, bool(r.get('empty'))))
    return out

def boot(d, B=10000, seed=0):
    d = np.asarray(d); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(axis=1))
    return [round(100 * float(d.mean()), 6), round(100 * float(ms[int(.025 * B)]), 6), round(100 * float(ms[int(.975 * B) - 1]), 6)]

if __name__ == '__main__':
    L = runs('F_grid.jsonl', 'F_grid', 'grid_L'); A = runs('F_ablate.jsonl', 'F_ablate', 'abl_v2_A_dgm_s3__g024_0__full')
    S = runs('F_grid.jsonl', 'F_grid', 'grid_none')
    T = [t for t in F if len(L[t]) >= 2 and A[t] and S[t]]
    acc2, cost2, acc1, cost1, accA, costA, accS = [], [], [], [], [], [], []
    for t in T:
        pubs = [SK.public_pass(t, sol, e) for (_, _, sol, e) in L[t][:2]]
        a = c = 0.0
        for order in ((0, 1), (1, 0)):
            i, j = order
            if pubs[i]: a += L[t][i][0]; c += L[t][i][1]
            else: a += L[t][j][0]; c += L[t][i][1] + L[t][j][1]
        acc2.append(a / 2); cost2.append(c / 2)
        acc1.append(np.mean([x[0] for x in L[t][:2]])); cost1.append(np.mean([x[1] for x in L[t][:2]]))
        accA.append(np.mean([x[0] for x in A[t]])); costA.append(np.mean([x[1] for x in A[t]]))
        accS.append(np.mean([x[0] for x in S[t]]))
    json.dump(SK._cache, open(SK._cache_path, 'w'))
    acc2, acc1, accA, accS = map(np.array, (acc2, acc1, accA, accS))
    res = {'n_tasks': len(T),
           'L_at_1': {'acc': round(100 * acc1.mean(), 6), 'usd_per_task': round(float(np.mean(cost1)), 5)},
           'L_at_2': {'acc': round(100 * acc2.mean(), 6), 'usd_per_task': round(float(np.mean(cost2)), 5)},
           'loop3_best': {'acc': round(100 * accA.mean(), 6), 'usd_per_task': round(float(np.mean(costA)), 5)},
           'seed': {'acc': round(100 * accS.mean(), 6)},
           'L2_minus_loop3': boot(acc2 - accA), 'L1_minus_loop3': boot(acc1 - accA), 'L2_minus_seed': boot(acc2 - accS)}
    json.dump(res, open(os.path.join(SHI, 'results', 'l_at_k.json'), 'w'), indent=1)
    print(json.dumps(res, indent=1))

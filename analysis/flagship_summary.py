"""PREREG_v2 P1/H10: DGM SWE-bench flagship comparison from the full run (run on the SWE-bench machine, copied to
~/shi_eval/flagship/runs_full/<tag>/results.jsonl, tags flag_<agent>_s45).

Instances: fresh_gold.json (Verified minus DGM's 200, gold patch resolves) and dgm60_gold.json (DGM's 60 selection
tasks that resolve). A run counts as resolved only if the official evaluation resolved it; no prediction, an empty patch
or an early ending counts as unresolved (as in DGM's evaluation). Paired comparisons by instance: difference in resolve
rate with a 95% bootstrap CI and an exact McNemar test. Output: results/flagship_summary.json.
"""
import json, math, os
import numpy as np
SHI = os.path.expanduser('~/shi_eval'); FD = os.path.join(SHI, 'flagship')
AGENTS = ['dgm_init', 'dgm_best', 'moves', 'moves_retry']
PAIRS = [('moves', 'dgm_best'), ('moves_retry', 'dgm_best'), ('dgm_best', 'dgm_init'), ('moves', 'dgm_init'),
         ('moves_retry', 'moves'), ('moves_retry', 'dgm_init')]

INTERIM = []

def load_agent(a):
    p = os.path.join(FD, 'runs_full', f'flag_{a}_s45', 'results.jsonl')
    if not os.path.exists(p):   # before the final mirror: finished agents' results, dgm_best's interim grading
        p = os.path.join(FD, 'runs_full_partial', f'flag_{a}_s45.results.jsonl')
        if not os.path.exists(p):
            p = os.path.join(FD, 'runs_full_partial', f'flag_{a}_s45.interim.jsonl')
            if not os.path.exists(p): return None
        INTERIM.append(a)
    return {r['instance_id']: r for r in map(json.loads, open(p))}

def mcnemar(b, c):
    n = b + c
    if n == 0: return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)

def boot(d, B=10000, seed=0):
    d = np.asarray(d, float); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(axis=1))
    return round(100 * d.mean(), 6), round(100 * ms[int(.025 * B)], 6), round(100 * ms[int(.975 * B) - 1], 6)

def main():
    sets = {'fresh': json.load(open(os.path.join(FD, 'swe', 'fresh_gold.json'))),
            'dgm_selection': json.load(open(os.path.join(FD, 'swe', 'dgm60_gold.json')))}
    R = {a: load_agent(a) for a in AGENTS}
    out = {'n': {k: len(v) for k, v in sets.items()}, 'agents': {}, 'pairs': {}}
    res = lambda a, i: bool((R[a].get(i) or {}).get('resolved'))
    for a in AGENTS:
        if not R[a]: continue
        rows = list(R[a].values()); done = [r for r in rows if r.get('harness_ok') is not None or r.get('resolved') is not None]
        us = [r['usd'] for r in rows if 'usd' in r]
        rec = {'runs': len(rows), 'usd_mean': round(float(np.mean(us)), 3) if us else None,
               'usd_median': round(float(np.median(us)), 3) if us else None,
               'early_endings': sum(1 for r in rows if r.get('failed_step') == 'agent'),
               'no_prediction': sum(1 for r in rows if not r.get('prediction')),
               'empty_patch': sum(1 for r in rows if r.get('prediction') and r.get('patch_empty')),
               'budget_hits': sum(1 for r in rows if r.get('budget_hit'))}
        for s, ids in sets.items():
            got = [i for i in ids if i in R[a]]
            rec[f'{s}_n'] = len(got); rec[f'{s}_resolved'] = sum(res(a, i) for i in got)
            rec[f'{s}_rate'] = round(100 * rec[f'{s}_resolved'] / max(1, len(got)), 1)
        out['agents'][a] = rec
    for x, y in PAIRS:
        if not (R[x] and R[y]): continue
        for s, ids in sets.items():
            ids2 = [i for i in ids if i in R[x] and i in R[y]]
            if not ids2: continue
            d = [res(x, i) - res(y, i) for i in ids2]
            b = sum(1 for i in ids2 if res(x, i) and not res(y, i)); c = sum(1 for i in ids2 if res(y, i) and not res(x, i))
            diff, lo, hi = boot(d)
            out['pairs'][f'{x} - {y} | {s}'] = {'n': len(ids2), 'diff': diff, 'lo': lo, 'hi': hi, 'x_only': b, 'y_only': c,
                                                'mcnemar_p': float('%.3g' % mcnemar(b, c)),
                                                'H10_noninferior_3pt': bool(lo >= -3.0) if y == 'dgm_best' and x.startswith('moves') else None}
    out['interim_sources'] = INTERIM
    json.dump(out, open(os.path.join(SHI, 'results', 'flagship_summary.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1)[:4000])

if __name__ == '__main__':
    main()

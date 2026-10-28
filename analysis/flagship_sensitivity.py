"""SWE-bench sensitivity (exploratory): grade the patch present when a run ended early, as if DGM's harness had kept it
(flagship/runs_full/sensitivity/sens_results.jsonl), merged with the original results. Paired comparisons on fresh and
DGM-60 tasks. Writes results/flagship_sensitivity.json."""
import json, math, os
import numpy as np
SHI = os.path.expanduser('~/shi_eval'); FD = os.path.join(SHI, 'flagship')
fresh = json.load(open(os.path.join(FD, 'swe', 'fresh_gold.json'))); sel = json.load(open(os.path.join(FD, 'swe', 'dgm60_gold.json')))
AG = ['dgm_init', 'dgm_best', 'moves', 'moves_retry']
orig = {a: {r['instance_id']: r for r in map(json.loads, open(os.path.join(FD, 'runs_full', f'flag_{a}_s45', 'results.jsonl')))} for a in AG}
sens = {}
for r in map(json.loads, open(os.path.join(FD, 'runs_full', 'sensitivity', 'sens_results.jsonl'))):
    sens[(r['agent'], r['instance_id'])] = bool(r.get('resolved'))
def kept(a, i):
    r = orig[a][i]
    if r.get('failed_step') == 'agent': return sens.get((a, i), False)
    return bool(r.get('resolved'))
def mcnemar(b, c):
    n = b + c
    return 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n)
def boot(d, B=10000):
    d = np.asarray(d, float); rng = np.random.default_rng(0); ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(1))
    return {'diff': round(100 * float(d.mean()), 6), 'lo': round(100 * float(ms[250]), 6), 'hi': round(100 * float(ms[9749]), 6)}
out = {'agents': {}, 'pairs': {}}
for a in AG:
    out['agents'][a] = {s: {'kept_resolved': sum(kept(a, i) for i in ids), 'n': len(ids)} for s, ids in (('fresh', fresh), ('dgm60', sel))}
for x, y in (('moves', 'dgm_best'), ('dgm_best', 'dgm_init'), ('moves', 'dgm_init'), ('moves_retry', 'dgm_best')):
    for s, ids in (('fresh', fresh), ('dgm60', sel)):
        d = [kept(x, i) - kept(y, i) for i in ids]; b = sum(1 for i in ids if kept(x, i) and not kept(y, i)); c = sum(1 for i in ids if kept(y, i) and not kept(x, i))
        out['pairs'][f'{x} - {y} | {s}'] = dict(boot(d), x_only=b, y_only=c, mcnemar_p=float('%.3g' % mcnemar(b, c)))
json.dump(out, open(os.path.join(SHI, 'results', 'flagship_sensitivity.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))

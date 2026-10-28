"""Every loop's reported best vs the textbook model-loop move L and the cap-only seed, in the common final batch
(results/F_final.jsonl; F x 2). Writes results/loops_vs_L.json (points)."""
import collections, json, os
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
F = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))['fresh']
R = collections.defaultdict(lambda: collections.defaultdict(list))
for l in open(os.path.join(SHI, 'results', 'F_final.jsonl')):
    r = json.loads(l); R[r['agent']][r['task']].append(1.0 if r.get('passed') else 0.0)
rt = {a: {t: float(np.mean(v)) for t, v in d.items()} for a, d in R.items()}

def boot(x, y):
    ts = [t for t in F if t in x and t in y]; d = np.array([x[t] - y[t] for t in ts]); rng = np.random.default_rng(0)
    ms = np.sort(d[rng.integers(0, len(d), size=(10000, len(d)))].mean(1))
    return {'diff': round(100 * float(d.mean()), 6), 'lo': round(100 * float(ms[250]), 6), 'hi': round(100 * float(ms[9749]), 6)}

loops = sorted(a for a in rt if a.startswith('fin_v'))
vsL = {a: boot(rt[a], rt['fin_grid_L']) for a in loops}
best = max(loops, key=lambda a: vsL[a]['diff'])
out = {'per_loop': vsL, 'n_loops': len(loops), 'n_worse': sum(1 for v in vsL.values() if v['hi'] < 0),
       'n_better': sum(1 for v in vsL.values() if v['lo'] > 0), 'best': best, 'best_vs_L': vsL[best],
       'L_gain': boot(rt['fin_grid_L'], rt['fin_seed_dgm']), 'cap_gain': boot(rt['fin_seed_dgm_cap16k'], rt['fin_seed_dgm'])}
json.dump(out, open(os.path.join(SHI, 'results', 'loops_vs_L.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'per_loop'}))

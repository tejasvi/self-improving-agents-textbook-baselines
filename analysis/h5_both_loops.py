"""H5 for both first-round arm-A loop agents: change of the fresh gain on F1 under Claude Haiku 4.5 and Claude Sonnet 4.6
relative to the search model (transfer gain over the seed under that model minus the gain over the pooled seed reference
under Haiku 5.5), paired by problem, 95% bootstrap. Writes results/h5_both_loops.json."""
import collections, json, os
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
F1 = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))['fresh'][:116]
pool = collections.defaultdict(list)
for fn in ['F_seeds.v2.jsonl', 'F1_seeds_extra.jsonl', 'F1_seeds_extra2.jsonl', 'F1_seeds_extra3.jsonl']:
    p = os.path.join(SHI, 'results', fn)
    if not os.path.exists(p): continue
    for l in open(p):
        r = json.loads(l)
        if r['agent'] == 'seed_dgm': pool[r['task']].append(1.0 if r.get('passed') else 0.0)
ref = {t: float(np.mean(v)) for t, v in pool.items()}
def fresh1(e, aid):
    v = {}
    for l in open(os.path.join(SHI, 'exps', e, 'agents', aid, 'evals', 'fresh1.jsonl')):
        r = json.loads(l)
        if r.get('rep', 0) == 0: v[r['task']] = 1.0 if r.get('passed') else 0.0
    return v
bests = {'A1best': ('v2_A_dgm_s1', 'g002_1'), 'A3best': ('v2_A_dgm_s3', 'g024_0')}
out = {}
for model in ('claude-haiku-4-5', 'claude-sonnet-4-6'):
    X = collections.defaultdict(dict)
    for l in open(os.path.join(SHI, 'results', f'X_{model}.jsonl')):
        r = json.loads(l); X[r['agent']][r['task']] = 1.0 if r.get('passed') else 0.0
    for a, (e, aid) in bests.items():
        s = fresh1(e, aid); ts = [t for t in F1 if t in s and t in X[a] and t in X['seed_dgm'] and t in ref]
        d = np.array([(X[a][t] - X['seed_dgm'][t]) - (s[t] - ref[t]) for t in ts]); rng = np.random.default_rng(0)
        ms = np.sort(d[rng.integers(0, len(d), size=(10000, len(d)))].mean(1))
        out[f'{model}|{a}'] = {'diff': round(100 * float(d.mean()), 1), 'lo': round(100 * float(ms[250]), 1), 'hi': round(100 * float(ms[9749]), 1), 'n': len(ts)}
json.dump(out, open(os.path.join(SHI, 'results', 'h5_both_loops.json'), 'w'), indent=1); print(out)

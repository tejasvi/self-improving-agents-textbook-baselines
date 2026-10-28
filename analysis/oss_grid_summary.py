"""Textbook moves under gpt-oss-120b (results/F_grid_oss.jsonl; exploratory, DEVIATIONS 'textbook moves under
gpt-oss-120b') and the Haiku 4.5 paired comparison hand-written seed vs loop-2 best (results/F_final_k45.jsonl).
Writes results/oss_grid_summary.json (macro-ready keys, points) and results/k45_strong_minus_s2.json."""
import collections, json, os
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
F = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))['fresh']; F1, F2 = F[:116], F[116:]

def load(fn):
    R = collections.defaultdict(dict); U = collections.defaultdict(list)
    for l in open(os.path.join(SHI, 'results', fn)):
        r = json.loads(l); R[r['agent']][r['task']] = 1.0 if r.get('passed') else 0.0; U[r['agent']].append(r.get('usd') or 0.0)
    return R, U

def boot(R, a, b, ts):
    ts = [t for t in ts if t in R[a] and t in R[b]]; d = np.array([R[a][t] - R[b][t] for t in ts]); rng = np.random.default_rng(0)
    ms = np.sort(d[rng.integers(0, len(d), size=(10000, len(d)))].mean(1))
    return {'diff': round(100 * float(d.mean()), 6), 'lo': round(100 * float(ms[250]), 6), 'hi': round(100 * float(ms[9749]), 6), 'n': len(ts)}

R, U = load('F_grid_oss.jsonl'); out = {}
sc = lambda a, ts: 100 * float(np.mean([R[a][t] for t in ts if t in R[a]]))
names = {'none': 'None', 'E': 'E', 'B': 'B', 'L': 'L', 'P': 'P', 'EBLP': 'EBLP', 'loopbest': 'Loop'}
for k, w in names.items():
    a = f'ossgrid_{k}'; out[f'vog{w}F'] = round(sc(a, F), 1)
    if k != 'none': out[f'vog{w}gain'] = boot(R, a, 'ossgrid_none', F)
for k in ('L', 'EBLP', 'P'): out[f'vog{names[k]}vsLoop'] = boot(R, f'ossgrid_{k}', 'ossgrid_loopbest', F)
cands = [f'ossgrid_{k}' for k in ('E', 'B', 'L', 'P', 'EBLP')]
w = max(cands, key=lambda a: (sc(a, F1), a)); out['vogWinner'] = w.replace('ossgrid_', '')
out['vogWinnerFtwo'] = boot(R, w, 'ossgrid_loopbest', F2)
json.dump(out, open(os.path.join(SHI, 'results', 'oss_grid_summary.json'), 'w'), indent=1)
K, _ = load('F_final_k45.jsonl')
json.dump(boot(K, 'fk45_seed_strong', 'fk45_v3_K45_dgm_s2__g006_1', F), open(os.path.join(SHI, 'results', 'k45_strong_minus_s2.json'), 'w'))
print(json.dumps(out, indent=1))

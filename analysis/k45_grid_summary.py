"""Textbook single moves under Claude Haiku 4.5 (results/F_grid_k45.jsonl; exploratory, DEVIATIONS 2026-10-25 round-2
entry): pass rate, gain over the batch's seed and over/under the full hand-written seed (EBLP), signal-termination and
time-out shares. Writes results/k45_grid_summary.json (macro-ready keys, points)."""
import collections, json, os
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
F = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))['fresh']
R = collections.defaultdict(dict); sig = collections.Counter(); n = collections.Counter(); usd = collections.defaultdict(list)
for l in open(os.path.join(SHI, 'results', 'F_grid_k45.jsonl')):
    r = json.loads(l); a = r['agent'].replace('k45grid_', '')
    R[a][r['task']] = 1.0 if r.get('passed') else 0.0; n[a] += 1; usd[a].append(r.get('usd') or 0.0)
    sig[a] += r.get('agent_rc') in (137, 143) and not r.get('agent_timed_out')
def boot(x, y):
    ts = [t for t in F if t in x and t in y]; d = np.array([x[t] - y[t] for t in ts]); rng = np.random.default_rng(0)
    ms = np.sort(d[rng.integers(0, len(d), size=(10000, len(d)))].mean(1))
    return {'diff': round(100 * float(d.mean()), 6), 'lo': round(100 * float(ms[250]), 6), 'hi': round(100 * float(ms[9749]), 6)}
W = {'none': 'None', 'E': 'E', 'B': 'B', 'L': 'L', 'P': 'P', 'EBLP': 'EBLP'}
out = {}
for a, w in W.items():
    out[f'vkg{w}F'] = round(100 * float(np.mean(list(R[a].values()))), 1); out[f'vkg{w}Sig'] = round(100 * sig[a] / n[a])
    out[f'vkg{w}Usd'] = round(1000 * float(np.mean(usd[a])), 1)
    if a != 'none': out[f'vkg{w}gain'] = boot(R[a], R['none'])
out['vkgBMinusEBLP'] = boot(R['B'], R['EBLP'])
json.dump(out, open(os.path.join(SHI, 'results', 'k45_grid_summary.json'), 'w'), indent=1); print(out)

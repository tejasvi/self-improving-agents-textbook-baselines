"""One-shot redesigns under gpt-oss (results/F_redesign_oss.jsonl; exploratory, DEVIATIONS 'B3 under gpt-oss') and the
Haiku 4.5 seed's empty-run share (results/F_final_k45.jsonl). Writes results/oss_redesign_summary.json (macro-ready
keys, points) and results/k45_seed_empty.json."""
import collections, json, os
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
F = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))['fresh']; F1, F2 = F[:116], F[116:]
R = collections.defaultdict(dict)
for l in open(os.path.join(SHI, 'results', 'F_redesign_oss.jsonl')):
    r = json.loads(l); R[r['agent']][r['task']] = 1.0 if r.get('passed') else 0.0
sc = lambda a, ts: 100 * float(np.mean([R[a][t] for t in ts if t in R[a]]))

def boot(x, y, ts):
    ts = [t for t in ts if t in x and t in y]; d = np.array([x[t] - y[t] for t in ts]); rng = np.random.default_rng(0)
    ms = np.sort(d[rng.integers(0, len(d), size=(10000, len(d)))].mean(1))
    return {'diff': round(100 * float(d.mean()), 6), 'lo': round(100 * float(ms[250]), 6), 'hi': round(100 * float(ms[9749]), 6), 'n': len(ts)}

c = sorted(a for a in R if a.startswith('rdoss_opus'))
w = max(c, key=lambda a: (sc(a, F1), a))
mean = {t: float(np.mean([R[a][t] for a in c])) for t in F if all(t in R[a] for a in c)}
out = {'vorBestF': round(sc(w, F), 1), 'vorBestVsLoop': boot(R[w], R['rdoss_loopbest'], F2),
       'vorBestGain': boot(R[w], R['rdoss_seed'], F), 'vorMeanVsLoop': boot(mean, R['rdoss_loopbest'], F),
       'vorBroken': sum(1 for a in c if sc(a, F) == 0.0), 'vorLoopF': round(sc('rdoss_loopbest', F), 1),
       'vorSeedF': round(sc('rdoss_seed', F), 1),
       'vorAtLeastLoopMinusThree': sum(1 for a in c if sc(a, F) >= sc('rdoss_loopbest', F) - 3)}
json.dump(out, open(os.path.join(SHI, 'results', 'oss_redesign_summary.json'), 'w'), indent=1)
n = e = 0
for l in open(os.path.join(SHI, 'results', 'F_final_k45.jsonl')):
    r = json.loads(l)
    if r['agent'] == 'fk45_seed_dgm': n += 1; e += bool(r.get('empty'))
json.dump({'pct': 100 * e / n, 'n': n}, open(os.path.join(SHI, 'results', 'k45_seed_empty.json'), 'w'))
print(json.dumps(out), 'k45 seed empty %.1f%% of %d' % (100 * e / n, n))

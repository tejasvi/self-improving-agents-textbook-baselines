"""PREREG_v3 E2: clean random-diagnosis loops vs DGM loops, from the common batch results/F_final_r3.jsonl (all 232
fresh problems x 2 runs) and results/F_final_r3_manifest.json. Gains are per-problem pass-rate differences from the
batch's DGM seed. H14: mean fresh gain of the five clean random-diagnosis loops >= mean of all nine DGM loops - 3
points (problems resampled with the loops fixed, 10,000 resamples). Secondary: vs the three same-time DGM loops; Welch
test over loop means. Exploratory (not registered): v2 random-diagnosis loops vs the DGM loops, loop 3's agent vs L.
Writes results/r3_loops.json (unrounded)."""
import json, os, collections
import numpy as np
from scipy import stats
SHI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
man = json.load(open(os.path.join(SHI, 'results', 'F_final_r3_manifest.json')))['arms']
R = collections.defaultdict(lambda: collections.defaultdict(list)); usd = collections.defaultdict(list)
for l in open(os.path.join(SHI, 'results', 'F_final_r3.jsonl')):
    r = json.loads(l); R[r['agent']][r['task']].append(float(r['passed'])); usd[r['agent']].append(r.get('usd') or 0)
T = sorted(set.intersection(*[set(v) for v in R.values()]))
vec = lambda a: np.array([np.mean(R[a][t]) for t in T])
seed = vec('r3_seed_dgm')
def boot(d, B=10000, seed_=0):
    d = np.asarray(d, float); rng = np.random.default_rng(seed_)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(1))
    return {'diff': 100 * float(d.mean()), 'lo': 100 * float(ms[int(.025 * B)]), 'hi': 100 * float(ms[int(.975 * B) - 1]), 'n': len(d)}
groups = {'clean_random': [f'v4_RMC_s{s}' for s in range(11, 16)],
          'dgm_same_time': [f'v4_A_dgm_s{s}' for s in (7, 8, 9)],
          'dgm_earlier': ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3', 'v3_A_dgm_s4', 'v3_A_dgm_s5', 'v3_A_dgm_s6'],
          'random_v2': ['v3_RM_s1', 'v3_RM_s2', 'v3_RM_s3']}
groups['dgm_all'] = groups['dgm_same_time'] + groups['dgm_earlier']
groups['dgm_first_round'] = ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3']
out = {'n_tasks': len(T), 'seed_F': 100 * float(seed.mean()), 'L': boot(vec('r3_grid_L') - seed), 'loops': {}, 'groups': {}}
G = {}
for e, v in man.items():
    g = vec(v['agent_name']) - seed; G[e] = g
    out['loops'][e] = {'best': v['best'], 'best_S': v['best_S'], 'gain': boot(g), 'usd_per_run': float(np.mean(usd[v['agent_name']]))}
for name, es in groups.items():
    m = np.mean([G[e] for e in es], axis=0)
    out['groups'][name] = {'n_loops': len(es), 'mean_gain': boot(m), 'loop_gains': [100 * float(G[e].mean()) for e in es]}
def contrast(a, b):
    d = np.mean([G[e] for e in groups[a]], axis=0) - np.mean([G[e] for e in groups[b]], axis=0)
    w = stats.ttest_ind([G[e].mean() for e in groups[a]], [G[e].mean() for e in groups[b]], equal_var=False)
    return {**boot(d), 'welch_t': float(w.statistic), 'welch_p': float(w.pvalue)}
out['H14_clean_minus_dgm_all'] = contrast('clean_random', 'dgm_all')
out['clean_minus_dgm_same_time'] = contrast('clean_random', 'dgm_same_time')
out['clean_minus_random_v2'] = contrast('clean_random', 'random_v2')
out['dgm_same_time_minus_dgm_earlier'] = contrast('dgm_same_time', 'dgm_earlier')
out['H14_noninferior'] = out['H14_clean_minus_dgm_all']['lo'] > -3
out['exploratory_random_v2_minus_dgm_all'] = contrast('random_v2', 'dgm_all')
out['exploratory_random_v2_minus_dgm_first_round'] = contrast('random_v2', 'dgm_first_round')
out['exploratory_loop3_minus_L'] = boot(vec('r3_v2_A_dgm_s3__g024_0') - vec('r3_grid_L'))
json.dump(out, open(os.path.join(SHI, 'results', 'r3_loops.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'loops'}, indent=1)[:3000])

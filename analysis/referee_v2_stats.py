"""Statistics added in the first internal review round of the paper. Writes results/referee_v2_stats.json.

1. H2 in the registered form: per-loop selection-minus-fresh inflation with tasks resampled (S tasks of the reported best,
   fresh tasks paired with the seed, from the common final batch), plus a hierarchical bootstrap over the six DGM loops
   (resample loops, then tasks within loops).
2. Batch-adjusted contrasts (gain over each batch's own seed minus gain over the other batch's seed) for H6, H8 and L@2,
   and L@2 inside the common final batch.
3. Round-2 headline numbers without the 19 pilot problems that preceded the hand-written seed.
4. Loop-level (Welch) tests for arm comparisons, on per-loop mean fresh gains from the common final batch.
5. Time-out shares (600 s wall-clock cap) per agent in the gpt-oss batches and the Haiku 4.5 batch.
6. Haiku 4.5 seed: share of model responses that stopped at max_tokens (proxy ledger) in the final batch.
7. SWE-bench: completion-conditional resolve rates for all four agents.
"""
import collections, glob, json, math, os, sys
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
sys.path.insert(0, os.path.join(SHI, 'analysis'))
import seed_at_k as SK
from collect import collect
import ladder_report as LR
SP = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))
F = SP['fresh']; F1, F2 = F[:116], F[116:]
PILOT = set(json.load(open(os.path.join(SHI, 'data/lcb/splits_v1.json')))['pilot'])
FNP = [t for t in F if t not in PILOT]
B = 10000
out = {'n_pilot_in_F': len(F) - len(FNP)}

def rates(fn):
    R = collections.defaultdict(lambda: collections.defaultdict(list))
    for l in open(os.path.join(SHI, 'results', fn)):
        r = json.loads(l); R[r['agent']][r['task']].append(1.0 if r.get('passed') else 0.0)
    return {a: {t: float(np.mean(v)) for t, v in d.items()} for a, d in R.items()}

def boot_vec(d, seed=0):
    d = np.asarray(d, float); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(1))
    return {'diff': round(100 * float(d.mean()), 6), 'lo': round(100 * float(ms[int(.025 * B)]), 6), 'hi': round(100 * float(ms[int(.975 * B) - 1]), 6), 'n': len(d)}

def diff(x, y, ts): return boot_vec([x[t] - y[t] for t in ts if t in x and t in y])

def gdiff(xa, xs, ya, ys, ts):   # (xa - xs) - (ya - ys), each pair from its own batch
    ts = [t for t in ts if t in xa and t in xs and t in ya and t in ys]
    return boot_vec([(xa[t] - xs[t]) - (ya[t] - ys[t]) for t in ts])

G = rates('F_grid.jsonl'); A = rates('F_ablate.jsonl'); Rd = rates('F_redesign.jsonl'); FIN = rates('F_final.jsonl')
full3 = 'abl_v2_A_dgm_s3__g024_0__full'
# ---- 2. batch-adjusted contrasts
adj = {}
adj['H6_EBLP_vs_loop3_F2_raw'] = diff(G['grid_EBLP'], A[full3], F2)
adj['H6_EBLP_vs_loop3_F2_adj'] = gdiff(G['grid_EBLP'], G['grid_none'], A[full3], A['abl_seed_dgm'], F2)
adj['L_vs_loop3_F_adj'] = gdiff(G['grid_L'], G['grid_none'], A[full3], A['abl_seed_dgm'], F)
for m, w in (('opus', 'rd_opus_r3'), ('sonnet', 'rd_sonnet_r4')):
    adj[f'H8_{m}_best_vs_loop3_F2_adj'] = gdiff(Rd[w], Rd['rd_seed_dgm'], A[full3], A['abl_seed_dgm'], F2)
    c = [a for a in Rd if a.startswith(f'rd_{m}_r')]
    mr = {t: float(np.mean([Rd[a][t] for a in c])) for t in F if all(t in Rd[a] for a in c)}
    fulls = ['abl_v2_A_dgm_s1__g002_1__full', 'abl_v2_A_dgm_s2__g003_0__full', full3]
    ml = {t: float(np.mean([A[a][t] for a in fulls])) for t in F if all(t in A[a] for a in fulls)}
    adj[f'H8_{m}_mean_vs_mean_loops_F_adj'] = gdiff(mr, Rd['rd_seed_dgm'], ml, A['abl_seed_dgm'], F)
# L@2 inside the common final batch (both L and loop 3 have two runs per problem there)
runs = collections.defaultdict(list)
for l in open(os.path.join(SHI, 'results', 'F_final.jsonl')):
    r = json.loads(l)
    if r['agent'] in ('fin_grid_L', 'fin_v2_A_dgm_s3__g024_0'):
        root = os.path.join(SHI, 'results', 'box_runs_unavailable')
        runs[(r['agent'], r['task'])].append((bool(r.get('passed')), r.get('usd') or 0.0, r.get('rep', 0)))
out['L2_in_final_note'] = 'solutions of the second-machine batch are not on the first machine; L@2 inside F_final needs sample-test results'
cands = [a for a in G if a != 'grid_none']
lit = max(cands, key=lambda a: (float(np.mean([G[a][t] for t in F])), a))
adj['H6_literal_best_on_F'] = lit
adj['H6_literal_vs_loop3_F_raw'] = diff(G[lit], A[full3], F)
adj['H6_literal_vs_loop3_F_adj'] = gdiff(G[lit], G['grid_none'], A[full3], A['abl_seed_dgm'], F)
out['batch_adjusted'] = adj
# ---- 3. without the 19 pilot problems
np_ = {}
np_['L_gain_final_FNP'] = diff(FIN['fin_grid_L'], FIN['fin_seed_dgm'], FNP)
np_['L_gain_final_F'] = diff(FIN['fin_grid_L'], FIN['fin_seed_dgm'], F)
np_['L_gain_grid_FNP'] = diff(G['grid_L'], G['grid_none'], FNP)
np_['loop3_vs_L_final_FNP'] = diff(FIN['fin_v2_A_dgm_s3__g024_0'], FIN['fin_grid_L'], FNP)
loops = sorted(a for a in FIN if a.startswith('fin_v'))
vs = {a: diff(FIN[a], FIN['fin_grid_L'], FNP) for a in loops}
np_['loops_vs_L_FNP_n_worse'] = sum(1 for v in vs.values() if v['hi'] < 0)
np_['loops_vs_L_FNP_n_better'] = sum(1 for v in vs.values() if v['lo'] > 0)
np_['loops_vs_L_FNP_best'] = max(vs.values(), key=lambda v: v['diff'])
np_['H6_EBLP_vs_loop3_F2_raw_FNP'] = diff(G['grid_EBLP'], A[full3], [t for t in F2 if t not in PILOT])
np_['cap_vs_loop3_final_F'] = diff(FIN['fin_seed_dgm_cap16k'], FIN['fin_v2_A_dgm_s3__g024_0'], F)
np_['L_vs_cap_final_F'] = diff(FIN['fin_grid_L'], FIN['fin_seed_dgm_cap16k'], F)
out['without_pilot'] = np_
# ---- 4. loop-level Welch tests (per-loop mean fresh gains, final batch)
man = json.load(open(os.path.join(SHI, 'results', 'F_final_manifest.json')))['arms']
seed = FIN['fin_seed_dgm']
def lgain(e): a = man[e]['agent_name']; return 100 * float(np.mean([FIN[a][t] - seed[t] for t in F]))
grp = {'dgm6': ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3', 'v3_A_dgm_s4', 'v3_A_dgm_s5', 'v3_A_dgm_s6'],
       'dgm3': ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3'], 'random': ['v3_RM_s1', 'v3_RM_s2', 'v3_RM_s3'],
       'hgm': ['v3_H_hgm_s1', 'v3_H_hgm_s2', 'v3_H_hgm_s3']}
g = {k: [lgain(e) for e in v] for k, v in grp.items()}
def welch(x, y):
    x, y = np.array(x), np.array(y); vx, vy = x.var(ddof=1) / len(x), y.var(ddof=1) / len(y)
    t = (x.mean() - y.mean()) / math.sqrt(vx + vy); df = (vx + vy) ** 2 / (vx ** 2 / (len(x) - 1) + vy ** 2 / (len(y) - 1))
    from math import lgamma
    # two-sided p from Student t via the regularized incomplete beta (numerical integration)
    xx = df / (df + t * t); a, b = df / 2, 0.5
    def betainc(a, b, x, n=20000):
        s = np.linspace(0, x, n + 1)[1:]; f = s ** (a - 1) * (1 - s) ** (b - 1)
        return float(np.trapezoid(np.r_[0, f], np.linspace(0, x, n + 1)) / math.exp(lgamma(a) + lgamma(b) - lgamma(a + b)))
    p = betainc(a, b, xx)
    return {'mean_x': round(float(x.mean()), 6), 'mean_y': round(float(y.mean()), 6), 't': round(float(t), 6), 'df': round(float(df), 6), 'p': round(p, 6)}
out['loop_level'] = {'gains': {k: [round(v, 6) for v in vs_] for k, vs_ in g.items()},
                     'hgm_vs_dgm6': welch(g['hgm'], g['dgm6']), 'random_vs_dgm3': welch(g['random'], g['dgm3']),
                     'random_vs_dgm6': welch(g['random'], g['dgm6'])}
# ---- 1. H2: per-loop task-resampled inflation and hierarchical bootstrap over the six DGM loops
v1 = json.load(open(os.path.join(SHI, 'results', 'summary.json'))); smean = v1['seedDgm_S_runs']['mean']
S_TASKS = SP['small'] + SP['medium']
def s_vec(e, aid):
    d = os.path.join(SHI, 'exps', e, 'agents', aid, 'evals'); v = {}
    for st in ('small', 'medium'):
        p = os.path.join(d, f'{st}.jsonl')
        if os.path.exists(p):
            for l in open(p):
                r = json.loads(l)
                if r.get('rep', 0) == 0: v[r['task']] = 1.0 if r.get('passed') else 0.0
    return np.array([v[t] for t in S_TASKS if t in v])
per = {}; rng = np.random.default_rng(1); data = {}
for e in grp['dgm6']:
    a = man[e]['agent_name']; s = s_vec(e, man[e]['best'])
    fg = np.array([FIN[a][t] - seed[t] for t in F]); data[e] = (s, fg)
    sb = s[rng.integers(0, len(s), size=(B, len(s)))].mean(1) - smean
    fb = fg[rng.integers(0, len(fg), size=(B, len(fg)))].mean(1)
    infl = np.sort(100 * (sb - fb))
    per[e] = {'S_n': int(len(s)), 'inflation': round(100 * float(s.mean() - smean - fg.mean()), 6),
              'lo': round(float(infl[250]), 6), 'hi': round(float(infl[9749]), 6)}
hier = []
for b in range(4000):
    pick = rng.integers(0, 6, size=6); vals = []
    for i in pick:
        s, fg = data[grp['dgm6'][i]]
        vals.append(s[rng.integers(0, len(s), len(s))].mean() - smean - fg[rng.integers(0, len(fg), len(fg))].mean())
    hier.append(100 * float(np.mean(vals)))
hier = np.sort(hier)
out['H2'] = {'per_loop': per, 'hierarchical_mean': round(float(np.mean([v['inflation'] for v in per.values()])), 6),
             'hierarchical_lo': round(float(hier[100]), 6), 'hierarchical_hi': round(float(hier[3899]), 6)}
# ---- 5. time-out shares
to = {}
for fn in ('F_final_oss.jsonl', 'F_grid_oss.jsonl', 'F_redesign_oss.jsonl', 'F_final_k45.jsonl', 'F_final.jsonl'):
    c = collections.defaultdict(lambda: [0, 0])
    for l in open(os.path.join(SHI, 'results', fn)):
        r = json.loads(l); x = c[r['agent']]; x[0] += 1; x[1] += bool(r.get('agent_timed_out'))
    to[fn] = {a: round(100 * v[1] / v[0], 6) for a, v in c.items()}
out['timeouts_pct'] = to
# ---- 6. Haiku 4.5 seed: responses stopped at max_tokens
tot = mx = 0
for l in open(os.path.join(SHI, 'ledger', 'ledger.jsonl')):
    try: r = json.loads(l)
    except Exception: continue
    if r.get('run', '').startswith('F_final_k45|fk45_seed_dgm|') and r.get('status') == 200:
        tot += 1; mx += r.get('stop') == 'max_tokens'
out['k45_seed_max_tokens_share'] = {'responses': tot, 'max_tokens': mx, 'pct': round(100 * mx / max(1, tot), 6)}
# ---- 7. SWE completion-conditional rates
fresh = set(json.load(open(os.path.join(SHI, 'flagship', 'swe', 'fresh_gold.json'))))
cc = {}
for a in ('dgm_init', 'dgm_best', 'moves', 'moves_retry'):
    rows = [json.loads(l) for l in open(os.path.join(SHI, 'flagship', 'runs_full', f'flag_{a}_s45', 'results.jsonl'))]
    fin = [r for r in rows if r.get('failed_step') != 'agent']
    ff = [r for r in fin if r['instance_id'] in fresh]
    cc[a] = {'finished': len(fin), 'finished_resolved': sum(bool(r.get('resolved')) for r in fin),
             'finished_fresh': len(ff), 'finished_fresh_resolved': sum(bool(r.get('resolved')) for r in ff)}
out['swe_completion'] = cc
json.dump(out, open(os.path.join(SHI, 'results', 'referee_v2_stats.json'), 'w'), indent=1)
print(json.dumps({k: out[k] for k in ('batch_adjusted', 'without_pilot', 'loop_level', 'H2', 'k45_seed_max_tokens_share', 'swe_completion')}, indent=1))

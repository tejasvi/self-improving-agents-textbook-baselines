"""Statistics added in the second internal review round of the paper. Writes results/referee_v2_stats_r2.json.

S1  signal terminations (agent_rc 137/143) and 600 s time-outs per agent and batch, for Haiku 4.5, gpt-oss and Haiku 5.5;
S2  L with one retry (L@2): raw and seed-adjusted contrasts with loop 3's agent, also without the pilot problems;
S3  H8 literal reading (best redesign on all of F vs loop 3), raw and adjusted;
S4  timing of the concurrent batches and seed-vs-seed differences between them;
S10 gpt-oss compute-matched reference: the seed resampled k times (first run passing the sample tests) on F1;
    budget hits per batch (spent >= 99% of the budget).
"""
import collections, json, os, re, sys
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
sys.path.insert(0, os.path.join(SHI, 'analysis'))
import seed_at_k as SK
SP = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))
F = SP['fresh']; F1, F2 = F[:116], F[116:]
PILOT = set(json.load(open(os.path.join(SHI, 'data/lcb/splits_v1.json')))['pilot'])
FNP = [t for t in F if t not in PILOT]
B = 10000; out = {}

def recs(fn): return [json.loads(l) for l in open(os.path.join(SHI, 'results', fn))]
def rates(fn):
    R = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in recs(fn): R[r['agent']][r['task']].append(1.0 if r.get('passed') else 0.0)
    return {a: {t: float(np.mean(v)) for t, v in d.items()} for a, d in R.items()}
def boot_vec(d, seed=0):
    d = np.asarray(d, float); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(1))
    return {'diff': round(100 * float(d.mean()), 6), 'lo': round(100 * float(ms[int(.025 * B)]), 6), 'hi': round(100 * float(ms[int(.975 * B) - 1]), 6), 'n': len(d)}
def diff(x, y, ts): return boot_vec([x[t] - y[t] for t in ts if t in x and t in y])
def gdiff(xa, xs, ya, ys, ts):
    ts = [t for t in ts if t in xa and t in xs and t in ya and t in ys]
    return boot_vec([(xa[t] - xs[t]) - (ya[t] - ys[t]) for t in ts])

# ---- S1 / budget hits
term = {}
for fn, budget in (('F_final_k45.jsonl', 1.0), ('F1_seeds_k45.jsonl', 1.0), ('X_claude-haiku-4-5.jsonl', 1.0),
                   ('X_claude-sonnet-4-6.jsonl', 1.0), ('F_final_oss.jsonl', 0.25), ('F_grid_oss.jsonl', 0.25),
                   ('F_redesign_oss.jsonl', 0.25), ('F_final.jsonl', 0.25), ('F_seeds.v2.jsonl', 0.25)):
    c = collections.defaultdict(lambda: [0, 0, 0, 0])
    for r in recs(fn):
        x = c[r['agent']]; x[0] += 1
        x[1] += r.get('agent_rc') in (137, 143) and not r.get('agent_timed_out')
        x[2] += bool(r.get('agent_timed_out')); x[3] += (r.get('usd') or 0) >= 0.99 * budget
    term[fn] = {a: {'n': v[0], 'signal_pct': round(100 * v[1] / v[0], 6), 'timeout_pct': round(100 * v[2] / v[0], 6),
                    'budget_pct': round(100 * v[3] / v[0], 6), 'signal_n': v[1], 'timeout_n': v[2], 'budget_n': v[3]}
                for a, v in c.items()}
out['terminations'] = term

# ---- S2: L@2 raw and adjusted, all F and without pilot problems
G = rates('F_grid.jsonl'); A = rates('F_ablate.jsonl'); Rd = rates('F_redesign.jsonl')
full3 = 'abl_v2_A_dgm_s3__g024_0__full'
Lr = collections.defaultdict(list)
for r in recs('F_grid.jsonl'):
    if r['agent'] == 'grid_L':
        sol = os.path.join(SHI, 'runs', 'F_grid', 'grid_L', f"{r['task']}_r{r['rep']}", 'repo', 'solution.py')
        Lr[r['task']].append((bool(r['passed']), sol, bool(r.get('empty'))))
L2 = {}
for t in F:
    if len(Lr[t]) < 2: continue
    pubs = [SK.public_pass(t, sol, e) for (_, sol, e) in Lr[t][:2]]
    a = 0.0
    for i, j in ((0, 1), (1, 0)):
        a += Lr[t][i][0] if pubs[i] else Lr[t][j][0]
    L2[t] = a / 2
json.dump(SK._cache, open(SK._cache_path, 'w'))
out['L2'] = {'raw_F': diff(L2, A[full3], F), 'adj_F': gdiff(L2, G['grid_none'], A[full3], A['abl_seed_dgm'], F),
             'raw_FNP': diff(L2, A[full3], FNP), 'adj_FNP': gdiff(L2, G['grid_none'], A[full3], A['abl_seed_dgm'], FNP)}
# ---- M2 / S2: pre-specified natural candidates against loop 3 on all of F (raw and adjusted)
out['prespec'] = {'EBLP_raw_F': diff(G['grid_EBLP'], A[full3], F), 'EBLP_adj_F': gdiff(G['grid_EBLP'], G['grid_none'], A[full3], A['abl_seed_dgm'], F),
                  'L_raw_F': diff(G['grid_L'], A[full3], F), 'L_adj_F': gdiff(G['grid_L'], G['grid_none'], A[full3], A['abl_seed_dgm'], F)}
Lc = [a for a in G if 'L' in a.split('_', 1)[1] and a != 'grid_none']
f2 = {a: diff(G[a], A[full3], F2)['diff'] for a in Lc}
fF = {a: diff(G[a], A[full3], F) for a in Lc}
out['L_combos_vs_loop3'] = {'F2_min': min(f2.values()), 'F2_max': max(f2.values()), 'n': len(Lc),
                            'F_min': min(v['diff'] for v in fF.values()), 'F_max': max(v['diff'] for v in fF.values()),
                            'F_miss_margin': sum(1 for v in fF.values() if v['lo'] < -3), 'F_sig_behind': sum(1 for v in fF.values() if v['hi'] < 0)}
# ---- S3: H8 literal reading
for m in ('opus', 'sonnet'):
    c = [a for a in Rd if a.startswith(f'rd_{m}_r')]
    lit = max(c, key=lambda a: (float(np.mean([Rd[a][t] for t in F])), a))
    out[f'H8_literal_{m}'] = {'agent': lit, 'raw_F': diff(Rd[lit], A[full3], F), 'adj_F': gdiff(Rd[lit], Rd['rd_seed_dgm'], A[full3], A['abl_seed_dgm'], F)}
# ---- S4: batch timing and seed-vs-seed
def first_last(log):
    ts = re.findall(r'^\[(\d\d:\d\d:\d\d)\]', open(os.path.join(SHI, 'results', log)).read(), re.M)
    return (ts[0], ts[-1]) if ts else None
out['batch_times'] = {k: first_last(f'{k}.log') for k in ('F_grid', 'F_ablate', 'F_redesign')}
out['seed_vs_seed'] = {'ablate_minus_redesign_F2': diff(A['abl_seed_dgm'], Rd['rd_seed_dgm'], F2),
                       'ablate_minus_grid_F': diff(A['abl_seed_dgm'], G['grid_none'], F),
                       'ablate_minus_redesign_F': diff(A['abl_seed_dgm'], Rd['rd_seed_dgm'], F)}
# ---- S10: gpt-oss seed@k on F1 (F1_seeds_oss x4 + the final batch's seed run)
AT = collections.defaultdict(list)
for fn, root, agent in (('F1_seeds_oss.jsonl', 'F1_seeds_oss', 'oss_seed_dgm'), ('F_final_oss.jsonl', 'F_final_oss', 'foss_seed_dgm')):
    for r in recs(fn):
        if r['agent'] != agent or r['task'] not in F1: continue
        sol = os.path.join(SHI, 'runs', root, agent, f"{r['task']}_r{r['rep']}", 'repo', 'solution.py')
        AT[r['task']].append((bool(r['passed']), r.get('usd') or 0.0, sol, bool(r.get('empty'))))
pubs = {(t, i): SK.public_pass(t, AT[t][i][2], AT[t][i][3]) for t in F1 for i in range(len(AT[t]))}
json.dump(SK._cache, open(SK._cache_path, 'w'))
rng = np.random.default_rng(0); kmax = min(len(AT[t]) for t in F1); sk = {}
for k in range(1, kmax + 1):
    acc, cost, per = [], [], {}
    for t in F1:
        n = len(AT[t]); a = c = 0.0
        for _ in range(200):
            order = rng.permutation(n)[:k]; cc = 0.0; ch = None
            for i in order:
                cc += AT[t][i][1]
                if pubs[(t, i)]: ch = i; break
            if ch is None: ch = order[-1]
            a += AT[t][ch][0]; c += cc
        per[t] = a / 200; acc.append(a / 200); cost.append(c / 200)
    sk[k] = {'acc': round(100 * float(np.mean(acc)), 6), 'usd_per_task': round(float(np.mean(cost)), 5), 'per': per}
FO = rates('F_final_oss.jsonl'); loop = 'foss_v3_O_dgm_s1__g007_0'
lu = float(np.mean([r.get('usd') or 0 for r in recs('F_final_oss.jsonl') if r['agent'] == loop]))
k = next((k for k in sorted(sk) if sk[k]['usd_per_task'] >= lu), max(sk))
out['oss_seed_at_k'] = {'curve': {k_: {kk: v[kk] for kk in ('acc', 'usd_per_task')} for k_, v in sk.items()}, 'loop_usd': round(lu, 5), 'k': k,
                        'cost_reached': sk[k]['usd_per_task'] >= lu,
                        'loop_minus_seed_at_k_F1': boot_vec([FO[loop][t] - sk[k]['per'][t] for t in F1 if t in FO[loop]])}
json.dump(out, open(os.path.join(SHI, 'results', 'referee_v2_stats_r2.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'terminations'}, indent=1)[:5000])
for fn, d in term.items(): print(fn, {a: (v['signal_pct'], v['timeout_pct'], v['budget_pct']) for a, v in d.items()})

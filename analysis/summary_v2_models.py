"""Loops under other task models: Haiku 4.5 (v3_K45_*, exploratory) and gpt-oss-120b (v3_O_*, G-model).

Reads results/F_final_k45.jsonl / F_final_oss.jsonl (+ manifests). Per agent: F, F1, F2 pass rate, $/run, gain vs the
same-batch DGM seed (paired bootstrap over problems). For Haiku 4.5 also a compute-matched baseline from
results/F1_seeds_k45.jsonl (the DGM seed run 8 times per F1 problem; submit the first run whose solution passes the
statement's sample tests; ordering-averaged, as analysis/seed_at_k.py), compared with each loop best on F1 at the
smallest k whose cost reaches the agent's. Output: results/summary_v2_models.json.
"""
import collections, json, os, sys
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
sys.path.insert(0, os.path.join(SHI, 'analysis'))
import seed_at_k as SK
F = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))['fresh']; F1, F2 = F[:116], F[116:]

def load(tag):
    p = os.path.join(SHI, 'results', f'{tag}.jsonl')
    if not os.path.exists(p): return None
    runs = collections.defaultdict(lambda: collections.defaultdict(list)); usd = collections.defaultdict(list)
    for l in open(p):
        r = json.loads(l); runs[r['agent']][r['task']].append(1.0 if r.get('passed') else 0.0); usd[r['agent']].append(r.get('usd') or 0.0)
    return runs, usd

def rate(d, ts): xs = [np.mean(d[t]) for t in ts if t in d]; return round(100 * float(np.mean(xs)), 6) if xs else None

def boot(x, y, ts, B=10000, seed=0):
    ts = [t for t in ts if t in x and t in y]
    d = np.array([np.mean(x[t]) - np.mean(y[t]) for t in ts]); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(axis=1))
    return {'diff': round(100 * d.mean(), 6), 'lo': round(100 * ms[int(.025 * B)], 6), 'hi': round(100 * ms[int(.975 * B) - 1], 6), 'n': len(ts)}

def seed_at_k_k45():
    p = os.path.join(SHI, 'results', 'F1_seeds_k45.jsonl')
    if not os.path.exists(p): return None
    A = collections.defaultdict(list)
    for l in open(p):
        r = json.loads(l)
        sol = os.path.join(SHI, 'runs', 'F1_seeds_k45', r['agent'], f"{r['task']}_r{r['rep']}", 'repo', 'solution.py')
        A[r['task']].append((bool(r['passed']), r.get('usd') or 0.0, sol, bool(r.get('empty'))))
    pubs = {(t, i): SK.public_pass(t, A[t][i][2], A[t][i][3]) for t in F1 for i in range(len(A[t]))}
    json.dump(SK._cache, open(SK._cache_path, 'w'))
    rng = np.random.default_rng(0); kmax = min(len(A[t]) for t in F1); out = {}
    for k in range(1, kmax + 1):
        acc = []; cost = []; per = {}
        for t in F1:
            n = len(A[t]); a = c = 0.0
            for _ in range(200):
                order = rng.permutation(n)[:k]; cc = 0.0; ch = None
                for i in order:
                    cc += A[t][i][1]
                    if pubs[(t, i)]: ch = i; break
                if ch is None: ch = order[-1]
                a += A[t][ch][0]; c += cc
            per[t] = a / 200; acc.append(a / 200); cost.append(c / 200)
        out[k] = {'acc': round(100 * float(np.mean(acc)), 6), 'usd_per_task': round(float(np.mean(cost)), 5), 'per_task': per}
    return out

def main():
    res = {}
    for which, tag in (('k45', 'F_final_k45'), ('oss', 'F_final_oss')):
        L = load(tag)
        if not L: continue
        runs, usd = L; man = json.load(open(os.path.join(SHI, 'results', f'{tag}_manifest.json')))
        seed = runs.get(f'f{which}_seed_dgm'); tab = {}
        for a in sorted(runs):
            tab[a] = {'F': rate(runs[a], F), 'F1': rate(runs[a], F1), 'F2': rate(runs[a], F2), 'n_runs': sum(len(v) for v in runs[a].values()),
                      'usd_per_run': round(float(np.mean(usd[a])), 4),
                      'gain_vs_seed_F': boot(runs[a], seed, F) if seed and a != f'f{which}_seed_dgm' else None}
        res[which] = {'manifest': man, 'agents': tab}
        if which == 'k45':
            sk = seed_at_k_k45()
            if sk:
                res[which]['seed_at_k'] = {k: {kk: v[kk] for kk in ('acc', 'usd_per_task')} for k, v in sk.items()}
                cmp = {}
                for e, ent in man['arms'].items():
                    a = ent['agent_name']
                    if a not in runs or a.endswith('seed_dgm'): continue
                    u = float(np.mean([x for x in usd[a]]))   # cost per run of the agent (all F)
                    ks = sorted(sk); k = next((k for k in ks if sk[k]['usd_per_task'] >= u), ks[-1])
                    per = sk[k]['per_task']; x = {t: [np.mean(runs[a][t])] for t in F1 if t in runs[a]}
                    y = {t: [per[t]] for t in F1}
                    cmp[a] = {'agent_usd_per_run': round(u, 4), 'k': k, 'k_cost_reached': sk[k]['usd_per_task'] >= u,
                              'seed_at_k_usd': sk[k]['usd_per_task'], 'agent_minus_seed_at_k_F1': boot(x, y, F1)}
                res[which]['compute_matched'] = cmp
    json.dump(res, open(os.path.join(SHI, 'results', 'summary_v2_models.json'), 'w'), indent=1)
    for w, r in res.items():
        print('==', w)
        for a, v in r['agents'].items(): print(f"  {a:45s} F={v['F']} F1={v['F1']} ${v['usd_per_run']}/run gain={v['gain_vs_seed_F']}")
        if 'seed_at_k' in r: print('  seed@k', {k: (v['acc'], v['usd_per_task']) for k, v in r['seed_at_k'].items()})
        if 'compute_matched' in r: print('  matched', json.dumps(r['compute_matched']))

if __name__ == '__main__':
    main()

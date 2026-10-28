"""Round-2 loop analysis: G-power (6 DGM + 6 placebo loops), B2 random-diagnosis loops, G-search (HGM-style), no-hint
loops; all on the Haiku 5.5 task model. Fresh gains come from the common final batch (results/F_final.jsonl and
results/F_final_manifest.json, exp/final_batch.py), so every loop best and the seed are measured in one period.

Per loop: reported best (ladder_report.loop_best), its selection score S, S gain over the seed's selection mean (v1
reference: seed runs + placebo copies, results/summary.json), fresh gain on F with a paired bootstrap CI, cost per run,
and selection-minus-fresh inflation. Placebo loops: best S against the order-statistics prediction
(seed mean + sd * E[max of n standard normals], n = full evaluations). Output: results/summary_v2_loops.json.
"""
import json, os, sys
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
sys.path.insert(0, os.path.join(SHI, 'analysis'))
from collect import collect
import ladder_report as LR
from curves import emax
F = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))['fresh']
GROUPS = {'dgm_v2': ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3'], 'dgm_v3': ['v3_A_dgm_s4', 'v3_A_dgm_s5', 'v3_A_dgm_s6'],
          'random_v3': ['v3_RM_s1', 'v3_RM_s2', 'v3_RM_s3'], 'hgm_v3': ['v3_H_hgm_s1', 'v3_H_hgm_s2', 'v3_H_hgm_s3'],
          'nohint_v2': ['v2_A_nohint_s1', 'v2_A_nohint_s2']}
PLACEBO = ['v2_B_placebo_s1', 'v2_B_placebo_s2', 'v2_B_placebo_s3', 'v3_B_placebo_s4', 'v3_B_placebo_s5', 'v3_B_placebo_s6']

def fin_rates():
    p = os.path.join(SHI, 'results', 'F_final.jsonl')
    if not os.path.exists(p): return None, None
    runs, usd = {}, {}
    for l in open(p):
        r = json.loads(l)
        runs.setdefault(r['agent'], {}).setdefault(r['task'], []).append(1.0 if r.get('passed') else 0.0)
        usd.setdefault(r['agent'], []).append(r.get('usd') or 0.0)
    rates = {a: {t: np.mean(v) for t, v in d.items()} for a, d in runs.items()}
    return rates, {a: float(np.mean(v)) for a, v in usd.items()}

def boot(x, y, B=10000, seed=0):
    ts = [t for t in F if t in x and t in y]
    d = np.array([x[t] - y[t] for t in ts]); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(axis=1))
    return {'diff': round(100 * d.mean(), 6), 'lo': round(100 * ms[int(.025 * B)], 6), 'hi': round(100 * ms[int(.975 * B) - 1], 6), 'n': len(ts)}

def main():
    v1 = json.load(open(os.path.join(SHI, 'results', 'summary.json')))
    SD = v1['seedDgm_S_runs']; out = {'seed_S': SD, 'loops': {}, 'groups': {}, 'placebo': []}
    rates, usd = fin_rates()
    man = json.load(open(os.path.join(SHI, 'results', 'F_final_manifest.json')))['arms'] if rates else {}
    seed = rates.get('fin_seed_dgm') if rates else None
    for g, arms in GROUPS.items():
        infl, gains = [], []
        for e in arms:
            cfg, st, recs = collect(e); b = LR.loop_best(recs)
            rec = {'generation': st.get('generation'), 'best': b and b['aid'], 'S': b and b['sel'],
                   'S_gain_pts': b and round(100 * (b['sel'] - SD['mean']), 6)}
            ent = man.get(e)
            if rates and ent and ent['agent_name'] in rates and seed:
                fg = boot(rates[ent['agent_name']], seed); rec['F_gain'] = fg; rec['usd_per_run'] = usd[ent['agent_name']]
                rec['inflation_pts'] = round(rec['S_gain_pts'] - fg['diff'], 6) if b else None
                gains.append(fg['diff']); infl.append(rec['inflation_pts'])
                if ent['best'] != (b and b['aid']): rec['note'] = f"final batch used {ent['best']}, current best {b and b['aid']}"
            out['loops'][e] = rec
        if gains:
            out['groups'][g] = {'n': len(gains), 'mean_F_gain': round(float(np.mean(gains)), 6),
                                'mean_inflation': round(float(np.mean(infl)), 6), 'inflations': infl, 'F_gains': gains}
    dg = [x for g in ('dgm_v2', 'dgm_v3') for x in out['groups'].get(g, {}).get('inflations', [])]
    if len(dg) >= 3:   # H2 with power: mean selection-minus-fresh inflation over all DGM loops, bootstrap over loops
        rng = np.random.default_rng(1); a = np.array(dg)
        ms = np.sort(a[rng.integers(0, len(a), size=(10000, len(a)))].mean(axis=1))
        out['H2_power'] = {'n_loops': len(a), 'mean_inflation': round(float(a.mean()), 6),
                           'lo': round(float(ms[250]), 6), 'hi': round(float(ms[9749]), 6)}
    for e in PLACEBO:
        cfg, st, recs = collect(e)
        full = [r for r in recs if r['aid'] != 'initial' and r['compiled'] and r['sel_full']]
        if not full: continue
        n = len(full); best = max(r['sel'] for r in full)
        out['placebo'].append({'exp': e, 'generation': st.get('generation'), 'n_full': n, 'best_S': best,
                               'pred': SD['mean'] + SD['sd'] * emax(n)})
    json.dump(out, open(os.path.join(SHI, 'results', 'summary_v2_loops.json'), 'w'), indent=1)
    print(json.dumps({k: out[k] for k in ('groups', 'placebo')}, indent=1)[:3000])
    if 'H2_power' in out: print('H2_power', out['H2_power'])

if __name__ == '__main__':
    main()

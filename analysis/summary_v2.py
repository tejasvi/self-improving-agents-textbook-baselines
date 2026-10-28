"""Round-2 analysis (PREREG_v2 H6-H9; rules in DEVIATIONS.md entry 'ANALYSIS RULES for H6-H8').

Reads results/F_grid.jsonl, F_ablate.jsonl, F_redesign.jsonl and, when present, F_final.jsonl. Scores are per-problem
pass rates averaged over reps, then over problems; CIs are paired bootstrap over problems (95%, 10,000 resamples).
Writes results/summary_v2.json and results/summary_v2.txt. Points are percentage points.
"""
import collections, json, os, random
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
SP = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))
F = SP['fresh']; F1 = F[:116]; F2 = F[116:]
B = 10000; MARGIN = 3.0

def load(name):
    p = os.path.join(SHI, 'results', f'{name}.jsonl')
    runs = collections.defaultdict(lambda: collections.defaultdict(list)); usd = collections.defaultdict(list)
    if not os.path.exists(p): return None
    for l in open(p):
        try: r = json.loads(l)
        except Exception: continue
        runs[r['agent']][r['task']].append(1.0 if r.get('passed') else 0.0)
        usd[r['agent']].append(r.get('usd') or 0.0)
    return {'runs': runs, 'usd': usd}

def rates(d, agent):
    return {t: sum(v) / len(v) for t, v in d['runs'][agent].items() if v}

def score(r, tasks):
    xs = [r[t] for t in tasks if t in r]
    return (100 * sum(xs) / len(xs) if xs else None), len(xs)

def boot(ra, rb, tasks, seed=0):
    """Mean difference ra - rb over tasks covered by both, with a paired bootstrap 95% CI (points)."""
    ts = [t for t in tasks if t in ra and t in rb]
    if len(ts) < 10: return None
    d = np.array([ra[t] - rb[t] for t in ts]); n = len(d); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, n, size=(B, n))].mean(axis=1))
    return {'diff': round(100 * float(d.mean()), 6), 'lo': round(100 * float(ms[int(0.025 * B)]), 6),
            'hi': round(100 * float(ms[int(0.975 * B) - 1]), 6), 'n': n}

def mean_rates(rs):
    ts = set.intersection(*[set(r) for r in rs]) if rs else set()
    return {t: sum(r[t] for r in rs) / len(rs) for t in ts}

def table(d, prefix, ref):
    out = {}
    rr = rates(d, ref) if ref in d['runs'] else None
    for a in sorted(d['runs']):
        r = rates(d, a); s, n = score(r, F); s1, _ = score(r, F1); s2, _ = score(r, F2)
        nr = sum(len(v) for v in d['runs'][a].values())
        out[a] = {'F': s and round(s, 6), 'F1': s1 and round(s1, 6), 'F2': s2 and round(s2, 6), 'n_tasks': n, 'n_runs': nr,
                  'usd_per_run': round(sum(d['usd'][a]) / max(1, len(d['usd'][a])), 5),
                  'gain_vs_seed': boot(r, rr, F) if rr and a != ref else None}
    return out

def pick_by_F1(d, agents):
    sc = {a: score(rates(d, a), F1)[0] for a in agents}
    sc = {a: s for a, s in sc.items() if s is not None}
    return max(sc, key=lambda a: (sc[a], a)) if sc else None

def noninf(ci):
    """Supported if the lower 95% bound of (candidate - comparator) is >= -MARGIN."""
    if not ci: return 'pending'
    return 'supported' if ci['lo'] >= -MARGIN else 'not supported'

def main():
    S = {'margin_points': MARGIN}; txt = []
    G = load('F_grid'); A = load('F_ablate'); R = load('F_redesign'); FIN = load('F_final')
    full3 = 'abl_v2_A_dgm_s3__g024_0__full'
    fulls = ['abl_v2_A_dgm_s1__g002_1__full', 'abl_v2_A_dgm_s2__g003_0__full', full3]
    if A:
        S['ablate'] = table(A, 'abl_', 'abl_seed_dgm')
        # H9: leave-one-out drops relative to 'full', per lineage
        h9 = {}
        for f in fulls:
            if f not in A['runs']: continue
            stem = f[:-len('full')]; rf = rates(A, f); rs = rates(A, 'abl_seed_dgm')
            g = boot(rf, rs, F); drops = {}
            man = json.load(open(os.path.join(SHI, 'harness', 'ablate', stem[len('abl_'):].rstrip('_'), 'manifest.json')))
            clean = {n: all(st in ('ok', 'empty') for _, st in v['applied']) for n, v in man['variants'].items()}
            for a in A['runs']:
                if a.startswith(stem + 'minus_'):
                    n = a[len(stem):]; drops[n] = dict(boot(rf, rates(A, a), F) or {}, applies_cleanly=clean.get(n))
            only = {a[len(stem):]: dict(boot(rates(A, a), rs, F) or {}, applies_cleanly=clean.get(a[len(stem):]))
                    for a in A['runs'] if a.startswith(stem + 'only_')}
            n_edits = len(man['lineage']); n_clean = sum(1 for n in drops if drops[n].get('applies_cleanly'))
            # H9 as registered needs every leave-one-out variant; with rejected hunks it is not testable
            top2 = sorted([v['diff'] for v in drops.values() if v.get('applies_cleanly') and 'diff' in v], reverse=True)[:2]
            testable = n_clean == n_edits
            frac = (sum(top2) / g['diff']) if testable and g and g['diff'] > 0 and top2 else None
            h9[stem.strip('_')] = {'full_gain': g, 'n_edits': n_edits, 'n_loo_clean': n_clean, 'loo_drops': drops,
                                   'only_gains': only, 'top2_share_of_gain': frac and round(frac, 3),
                                   'H9': ('not testable (leave-one-out variants with rejected hunks)' if not testable
                                          else ('supported' if frac >= 0.8 else 'not supported'))}
        if 'abl_v2_A_dgm_s3__g024_0__semantic_cap4096' in A['runs']:
            h9['loop3_semantic_cap_drop'] = boot(rates(A, full3), rates(A, 'abl_v2_A_dgm_s3__g024_0__semantic_cap4096'), F)
            h9['cap16k_vs_loop3_full'] = boot(rates(A, 'abl_seed_dgm_cap16k'), rates(A, full3), F) \
                if 'abl_seed_dgm_cap16k' in A['runs'] else None
        S['H9'] = h9
    if G:
        S['grid'] = table(G, 'grid_', 'grid_none')
        if A and full3 in A['runs']:
            r3 = rates(A, full3); cands = [a for a in G['runs'] if a != 'grid_none']
            w = pick_by_F1(G, cands)
            h6 = {'winner_by_F1': w, 'winner_vs_loop3_on_F2': boot(rates(G, w), r3, F2) if w else None,
                  'EBLP_vs_loop3_on_F': boot(rates(G, 'grid_EBLP'), r3, F) if 'grid_EBLP' in G['runs'] else None,
                  'L_vs_loop3_on_F': boot(rates(G, 'grid_L'), r3, F) if 'grid_L' in G['runs'] else None,
                  'usd_per_run_winner': w and S['grid'][w]['usd_per_run'],
                  'usd_per_run_loop3': S['ablate'][full3]['usd_per_run']}
            h6['H6'] = noninf(h6['winner_vs_loop3_on_F2'])
            S['H6'] = h6
    if R:
        S['redesign'] = table(R, 'rd_', 'rd_seed_dgm')
        if A and all(f in A['runs'] for f in fulls):
            r3 = rates(A, full3); loops_mean = mean_rates([rates(A, f) for f in fulls]); h8 = {}
            for m in ('opus', 'sonnet'):
                cands = [a for a in R['runs'] if a.startswith(f'rd_{m}_r')]
                if not cands: continue
                w = pick_by_F1(R, cands)
                h8[m] = {'winner_by_F1': w, 'winner_vs_loop3_on_F2': boot(rates(R, w), r3, F2) if w else None,
                         'mean_redesign_vs_mean_loop_best_on_F': boot(mean_rates([rates(R, a) for a in cands]), loops_mean, F)}
                h8[m]['H8_best'] = noninf(h8[m]['winner_vs_loop3_on_F2'])
                h8[m]['H8_mean'] = noninf(h8[m]['mean_redesign_vs_mean_loop_best_on_F'])
            S['H8'] = h8
    if FIN:
        S['final'] = table(FIN, 'fin_', 'fin_seed_dgm')
        mp = os.path.join(SHI, 'results', 'F_final_manifest.json')
        if os.path.exists(mp):
            man = json.load(open(mp))['arms']
            def grp(prefix):
                rs = []
                for e, v in man.items():
                    if e.startswith(prefix) and v['agent_name'] in FIN['runs']: rs.append(rates(FIN, v['agent_name']))
                return rs
            groups = {'dgm_v2': grp('v2_A_dgm_'), 'nohint_v2': grp('v2_A_nohint_'), 'dgm_v3': grp('v3_A_dgm_'),
                      'random_v3': grp('v3_RM_'), 'hgm_v3': grp('v3_H_hgm_')}
            seed = rates(FIN, 'fin_seed_dgm'); h7 = {}
            for g, rs in groups.items():
                if rs: h7[f'{g}_mean_gain'] = boot(mean_rates(rs), seed, F); h7[f'{g}_n'] = len(rs)
            dgm_all = groups['dgm_v2'] + groups['dgm_v3']
            if groups['random_v3'] and groups['dgm_v2']:
                h7['random_minus_dgm_v2'] = boot(mean_rates(groups['random_v3']), mean_rates(groups['dgm_v2']), F)
                h7['H7'] = noninf(h7['random_minus_dgm_v2'])
            if groups['random_v3'] and dgm_all:
                h7['random_minus_dgm_all6'] = boot(mean_rates(groups['random_v3']), mean_rates(dgm_all), F)
            if groups['hgm_v3'] and dgm_all:
                h7['hgm_minus_dgm_all6'] = boot(mean_rates(groups['hgm_v3']), mean_rates(dgm_all), F)
            S['H7'] = h7
    json.dump(S, open(os.path.join(SHI, 'results', 'summary_v2.json'), 'w'), indent=1)
    for k in ('grid', 'ablate', 'redesign', 'final'):
        if k not in S: continue
        txt.append(f'== {k} (F, F1, F2 in %, gain vs same-batch seed with 95% CI)')
        for a, v in S[k].items():
            g = v['gain_vs_seed']; gs = f"{g['diff']:+.1f} [{g['lo']:+.1f},{g['hi']:+.1f}]" if g else ''
            txt.append(f"{a:55s} F={v['F']} F1={v['F1']} F2={v['F2']} n={v['n_tasks']}/{v['n_runs']} ${v['usd_per_run']:.4f}/run {gs}")
    for k in ('H6', 'H7', 'H8', 'H9'):
        if k in S: txt.append(f'== {k}\n' + json.dumps(S[k], indent=1))
    open(os.path.join(SHI, 'results', 'summary_v2.txt'), 'w').write('\n'.join(txt) + '\n')
    print('\n'.join(txt[:80]))

if __name__ == '__main__':
    main()

"""Round-2 numbers for the paper: reads results/summary_v2.json, results/l_at_k.json, adas_p4/full/final_table.json
(and, when present, the flagship and final-batch results) and writes paper/numbers_v2.tex (macros, letters-only names,
prefix 'v') and generated table bodies paper/tab_grid.tex, paper/tab_redesign.tex, paper/tab_adas.tex.
Missing inputs leave their macros as '--'. Run analysis/summary_v2.py first.
"""
import json, os, re
SHI = os.path.expanduser('~/shi_eval')
mac = {}

def m(name, val, fmt='{:.1f}'):
    assert re.fullmatch(r'[A-Za-z]+', name), name
    mac[name] = fmt.format(val) if isinstance(val, (int, float)) and not isinstance(val, bool) else str(val)

def ci(prefix, d, sign=True):
    """d = {'diff','lo','hi'} or [diff, lo, hi] in points -> macros prefix, prefixlo, prefixhi."""
    if d is None: return
    v = [d['diff'], d['lo'], d['hi']] if isinstance(d, dict) else d
    v = [0.0 if abs(x) < 0.05 else x for x in v]   # no '-0.0' / '+-0.0'
    f = '{:+.1f}' if sign else '{:.1f}'
    fmt = lambda x: '0.0' if x == 0.0 else f.format(x)
    m(prefix, fmt(v[0])); m(prefix + 'lo', fmt(v[1])); m(prefix + 'hi', fmt(v[2]))

def ci_abs(prefix, d):
    """Unsigned magnitude of a contrast, for use with direction words ('fewer', 'behind'): |diff| with the interval
    mirrored when the contrast is negative. Writes prefix+'Abs', prefix+'Abslo', prefix+'Abshi'."""
    if d is None: return
    v = [d['diff'], d['lo'], d['hi']] if isinstance(d, dict) else list(d)
    if v[0] < 0: v = [-v[0], -v[2], -v[1]]
    v = [0.0 if abs(x) < 0.05 else x for x in v]   # no '-0.0'
    m(prefix + 'Abs', v[0], '{:.1f}'); m(prefix + 'Abslo', v[1], '{:.1f}'); m(prefix + 'Abshi', v[2], '{:.1f}')

def load(p):
    p = os.path.join(SHI, p)
    return json.load(open(p)) if os.path.exists(p) else None

WORD = {'none': 'none', 'E': 'E', 'B': 'B', 'L': 'L', 'P': 'P'}
def grid_name(sub):   # letters-only macro stem for a subset ('EBLP' -> 'EBLP', 'none' -> 'None')
    return 'None' if sub == 'none' else sub

def main():
    S = load('results/summary_v2.json') or {}
    # ---- B1 grid
    G = S.get('grid', {}); rows = []
    if G:
        seed = G['grid_none']
        m('vgridSeedF', seed['F']); m('vgridSeedUsd', 1000 * seed['usd_per_run'], '{:.1f}')
        withL = [v for a, v in G.items() if 'L' in a.split('_', 1)[1] and a != 'grid_none']
        noL = [v for a, v in G.items() if 'L' not in a.split('_', 1)[1] and a != 'grid_none']
        m('vgridWithLmin', min(v['gain_vs_seed']['diff'] for v in withL), '{:+.1f}')
        m('vgridWithLmax', max(v['gain_vs_seed']['diff'] for v in withL), '{:+.1f}')
        m('vgridNoLmin', min(v['gain_vs_seed']['diff'] for v in noL), '{:+.1f}')
        m('vgridNoLmax', max(v['gain_vs_seed']['diff'] for v in noL), '{:+.1f}')
        for sub in ('L', 'P', 'E', 'B', 'EBLP'):
            v = G.get(f'grid_{sub}')
            if v:
                ci(f'vgrid{grid_name(sub)}gain', v['gain_vs_seed']); m(f'vgrid{grid_name(sub)}F', v['F'])
                m(f'vgrid{grid_name(sub)}usd', 1000 * v['usd_per_run'], '{:.1f}')
        order = ['none', 'E', 'B', 'P', 'EB', 'EP', 'BP', 'EBP', 'L', 'EL', 'BL', 'LP', 'EBL', 'ELP', 'BLP', 'EBLP']
        emp = load('results/grid_empty.json') or {}
        for sub in order:
            v = G.get(f'grid_{sub}')
            if not v: continue
            g = v['gain_vs_seed']
            gs = f"${g['diff']:+.1f}$ [${g['lo']:+.1f}$, ${g['hi']:+.1f}$]" if g else '--'
            label = '(seed)' if sub == 'none' else ', '.join(sub)
            e = emp.get(f'grid_{sub}')
            rows.append(f"{label} & {v['F']:.1f} & {gs} & {1000 * v['usd_per_run']:.1f} & {e if e is not None else '--'} \\\\")
        open(os.path.join(SHI, 'paper', 'tab_grid.tex'), 'w').write('\n'.join(rows) + '\n')
    # ---- H6, loop bests in the same period (F_ablate)
    A = S.get('ablate', {})
    full = {'One': 'abl_v2_A_dgm_s1__g002_1__full', 'Two': 'abl_v2_A_dgm_s2__g003_0__full', 'Three': 'abl_v2_A_dgm_s3__g024_0__full'}
    for k, a in full.items():
        if a in A:
            ci(f'vloop{k}gain', A[a]['gain_vs_seed']); m(f'vloop{k}F', A[a]['F']); m(f'vloop{k}usd', 1000 * A[a]['usd_per_run'])
    if 'abl_seed_dgm_cap16k' in A: ci('vcapgain', A['abl_seed_dgm_cap16k']['gain_vs_seed'])
    if G and full['Three'] in A:
        u3 = A[full['Three']]['usd_per_run']; combos = [v for a, v in G.items() if a != 'grid_none']
        m('vgridMaxCostShare', 100 * max(v['usd_per_run'] for v in combos) / u3, '{:.0f}')
        m('vgridLCostShare', 100 * G['grid_L']['usd_per_run'] / u3, '{:.0f}')
        m('vgridEBLPCostShare', 100 * G['grid_EBLP']['usd_per_run'] / u3, '{:.0f}')
    H6 = S.get('H6')
    if H6:
        m('vHsixWinner', H6['winner_by_F1'].replace('grid_', '').replace('none', 'seed'))
        ci('vHsixFtwo', H6['winner_vs_loop3_on_F2']); ci('vHsixEBLP', H6['EBLP_vs_loop3_on_F']); ci('vHsixL', H6['L_vs_loop3_on_F'])
        m('vHsixVerdict', H6['H6'])
    H9 = S.get('H9', {})
    if 'loop3_semantic_cap_drop' in H9: ci('vsemcapdrop', H9['loop3_semantic_cap_drop'])
    if 'cap16k_vs_loop3_full' in H9: ci('vcapvsloopthree', H9['cap16k_vs_loop3_full']); ci_abs('vcapvsloopthree', H9['cap16k_vs_loop3_full'])
    sem = A.get('abl_v2_A_dgm_s3__g024_0__semantic_cap4096')
    if sem: m('vsemcapF', sem['F'])
    l3 = H9.get('abl_v2_A_dgm_s3__g024_0')
    if l3:
        ci('vlastedit', l3['loo_drops'].get('minus_g024_0'))
        m('vlinThreeN', l3['n_edits'], '{:d}'); m('vlinThreeClean', l3['n_loo_clean'], '{:d}')
    for key, word in (('abl_v2_A_dgm_s1__g002_1', 'One'), ('abl_v2_A_dgm_s2__g003_0', 'Two')):
        if key in H9: m(f'vlin{word}N', H9[key]['n_edits'], '{:d}'); m(f'vlin{word}Clean', H9[key]['n_loo_clean'], '{:d}')
    # ---- compute-matched follow-up
    L = load('results/l_at_k.json')
    if L:
        m('vLoneAcc', L['L_at_1']['acc']); m('vLoneUsd', 1000 * L['L_at_1']['usd_per_task'])
        m('vLtwoAcc', L['L_at_2']['acc']); m('vLtwoUsd', 1000 * L['L_at_2']['usd_per_task'])
        m('vLthreeAcc', L['loop3_best']['acc']); m('vLthreeUsd', 1000 * L['loop3_best']['usd_per_task'])
        ci('vLtwoMinusLoop', L['L2_minus_loop3']); ci('vLoneMinusLoop', L['L1_minus_loop3'])
        m('vLtwoCostShare', 100 * L['L_at_2']['usd_per_task'] / L['loop3_best']['usd_per_task'], '{:.0f}')
    # ---- B3 redesign
    R = S.get('redesign', {}); H8 = S.get('H8', {}); rrows = []
    if R:
        caps = load('results/redesign_caps.json') or {}
        order = lambda a: (0 if 'opus' in a else 1 if 'sonnet' in a else 2, a)
        for a in sorted(R, key=order):
            v = R[a]; g = v['gain_vs_seed']
            gs = f"${g['diff']:+.1f}$ [${g['lo']:+.1f}$, ${g['hi']:+.1f}$]" if g else '--'
            nm = {'rd_seed_dgm': 'DGM seed', 'rd_seed_dgm_cap16k': 'cap-only seed', 'rd_seed_strong': 'engineered seed'}
            mm = re.match(r'rd_(opus|sonnet)_r(\d)', a)
            label = nm.get(a) or (f"{mm.group(1).capitalize()} redesign {int(mm.group(2)) + 1}" if mm else a)
            rrows.append(f"{label} & {caps.get(a, '--')} & {v['F']:.1f} & {gs} & {1000 * v['usd_per_run']:.1f} \\\\")
        open(os.path.join(SHI, 'paper', 'tab_redesign.tex'), 'w').write('\n'.join(rrows) + '\n')
        for mod, word in (('opus', 'Opus'), ('sonnet', 'Sonnet')):
            h = H8.get(mod)
            if not h: continue
            ci(f'vHeight{word}best', h['winner_vs_loop3_on_F2']); ci(f'vHeight{word}mean', h['mean_redesign_vs_mean_loop_best_on_F'])
            m(f'vHeight{word}bestVerdict', h['H8_best']); m(f'vHeight{word}meanVerdict', h['H8_mean'])
    # ---- P4 ADAS
    D = load('adas_p4/full/final_table.json'); arows = []
    if D:
        names = {'mgsm': 'MGSM', 'drop': 'DROP (F1)', 'gpqa': 'GPQA', 'mmlu': 'MMLU'}
        words = {'mgsm': 'Mgsm', 'drop': 'Drop', 'gpqa': 'Gpqa', 'mmlu': 'Mmlu'}
        for dom in ('mgsm', 'drop', 'gpqa', 'mmlu'):
            d = D['domains'].get(dom)
            if not d: continue
            ag = d['agents']; p = d['paired']
            am = p.get('a - matched CoT-SC'); ac = p.get('a - cot')
            arch = (d.get('archive_gpt35_test') or {})
            ci(f'vadas{words[dom]}', {'diff': am['diff'], 'lo': am['ci95'][0], 'hi': am['ci95'][1]})
            m(f'vadas{words[dom]}N', d['matched_N'], '{:d}')
            ag_a, ag_m, ag_c = ag['best_val'], ag['matched'], ag['cot']
            arch_txt = arch.get('gain_a_minus_cotsc')
            m(f'vadas{words[dom]}arch', arch_txt if arch_txt is not None else '--', '{:+.1f}')
            arows.append(f"{names[dom]} & {ag_a['score']:.1f} ({ag_a['calls_per_q']:.0f}) & {ag_m['score']:.1f} ({ag_m['calls_per_q']:.0f}) & "
                         f"{ag_c['score']:.1f} & ${am['diff']:+.1f}$ [${am['ci95'][0]:+.1f}$, ${am['ci95'][1]:+.1f}$] & "
                         f"${ac['diff']:+.1f}$ & {('$%+.1f$' % arch_txt) if isinstance(arch_txt, (int, float)) else '--'} \\\\")
        open(os.path.join(SHI, 'paper', 'tab_adas.tex'), 'w').write('\n'.join(arows) + '\n')
    # ---- loops under other task models (results/summary_v2_models.json)
    M = load('results/summary_v2_models.json') or {}
    K = M.get('k45')
    if K:
        A = K['agents']
        def ag(name): return A.get(name) or {}
        m('vkSeedF', ag('fk45_seed_dgm').get('F')); m('vkSeedUsd', 1000 * ag('fk45_seed_dgm').get('usd_per_run', 0))
        m('vkStrongF', ag('fk45_seed_strong').get('F')); ci('vkStronggain', ag('fk45_seed_strong').get('gain_vs_seed_F'))
        m('vkStrongUsd', 1000 * ag('fk45_seed_strong').get('usd_per_run', 0))
        for e, w in (('v3_K45_dgm_s1', 'One'), ('v3_K45_dgm_s2', 'Two')):
            a = K['manifest']['arms'][e]['agent_name']
            if a in A:
                m(f'vk{w}F', A[a]['F']); ci(f'vk{w}gain', A[a]['gain_vs_seed_F']); m(f'vk{w}Usd', 1000 * A[a]['usd_per_run'])
        sk = K.get('seed_at_k') or {}
        if sk:
            kmax = max(sk, key=lambda k: int(k)); m('vkSeedAtKmax', sk[kmax]['acc']); m('vkSeedAtKk', int(kmax), '{:d}')
            m('vkSeedAtKusd', 1000 * sk[kmax]['usd_per_task'])
        cm = K.get('compute_matched') or {}
        a2 = K['manifest']['arms']['v3_K45_dgm_s2']['agent_name']
        if a2 in cm: ci('vkTwoMatched', cm[a2]['agent_minus_seed_at_k_F1']); ci_abs('vkTwoMatched', cm[a2]['agent_minus_seed_at_k_F1'])
    kx = load('results/k45_strong_minus_s2.json')
    if kx: ci('vkStrongMinusTwo', kx)
    O = M.get('oss')
    if O:
        A = O['agents']
        m('voSeedF', A.get('foss_seed_dgm', {}).get('F')); ci('voStronggain', A.get('foss_seed_strong', {}).get('gain_vs_seed_F'))
        for e, w in (('v3_O_dgm_s1', 'One'), ('v3_O_dgm_s3', 'Three')):
            a = O['manifest']['arms'][e]['agent_name']
            if a in A: m(f'vo{w}F', A[a]['F']); ci(f'vo{w}gain', A[a]['gain_vs_seed_F']); m(f'vo{w}Usd', 1000 * A[a]['usd_per_run'])
    og = load('results/oss_grid_summary.json')
    if og:
        for k, v in og.items():
            if isinstance(v, dict) and 'diff' in v: ci(k, v)
            elif isinstance(v, (int, float, str)): m(k, v)
    orr = load('results/oss_redesign_summary.json')
    if orr:
        for k, v in orr.items():
            if isinstance(v, dict) and 'diff' in v: ci(k, v)
            elif isinstance(v, int): m(k, v, '{:d}')
            elif isinstance(v, float): m(k, v)
    e = load('results/k45_seed_empty.json')
    if e: m('vkSeedEmpty', e['pct'], '{:.0f}')
    # ---- H7 / G-power / G-search (results/summary_v2.json H7, results/summary_v2_loops.json)
    H7 = S.get('H7')
    if H7:
        for k, w in (('dgm_v2_mean_gain', 'vhDgmTwo'), ('dgm_v3_mean_gain', 'vhDgmThree'), ('random_v3_mean_gain', 'vhRandom'),
                     ('hgm_v3_mean_gain', 'vhHgm'), ('nohint_v2_mean_gain', 'vhNohint'), ('random_minus_dgm_v2', 'vhRandomMinusDgm'),
                     ('random_minus_dgm_all6', 'vhRandomMinusDgmAll'), ('hgm_minus_dgm_all6', 'vhHgmMinusDgmAll')):
            if H7.get(k): ci(w, H7[k])
        if 'H7' in H7: m('vhSevenVerdict', H7['H7'])
        if H7.get('random_minus_dgm_v2'): ci_abs('vhRandomMinusDgm', H7['random_minus_dgm_v2'])
    LP = load('results/summary_v2_loops.json')
    if LP:
        hp = LP.get('H2_power')
        if hp: ci('vhInfl', {'diff': hp['mean_inflation'], 'lo': hp['lo'], 'hi': hp['hi']}); m('vhInflN', hp['n_loops'], '{:d}')
        pl = LP.get('placebo') or []
        if pl:
            m('vhPlaceboN', len(pl), '{:d}'); m('vhPlaceboMin', 100 * min(x['best_S'] for x in pl), '{:.0f}')
            m('vhPlaceboMax', 100 * max(x['best_S'] for x in pl), '{:.0f}')
            m('vhPlaceboPred', 100 * sum(x['pred'] for x in pl) / len(pl), '{:.0f}')
        rows = []
        lab = {'dgm_v2': 'DGM', 'dgm_v3': 'DGM (more loops)', 'random_v3': 'random diagnosis', 'hgm_v3': 'HGM-style', 'nohint_v2': 'DGM, no hints'}
        groups = {'dgm_v2': ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3'], 'nohint_v2': ['v2_A_nohint_s1', 'v2_A_nohint_s2'],
                  'dgm_v3': ['v3_A_dgm_s4', 'v3_A_dgm_s5', 'v3_A_dgm_s6'], 'random_v3': ['v3_RM_s1', 'v3_RM_s2', 'v3_RM_s3'],
                  'hgm_v3': ['v3_H_hgm_s1', 'v3_H_hgm_s2', 'v3_H_hgm_s3']}
        for g, arms in groups.items():
            for i, e in enumerate(arms):
                v = LP['loops'].get(e) or {}; fg = v.get('F_gain')
                gs = f"${fg['diff']:+.1f}$ [${fg['lo']:+.1f}$, ${fg['hi']:+.1f}$]" if fg else '--'
                Sv = f"{100 * v['S']:.0f}" if v.get('S') is not None else '--'
                inf = f"${v['inflation_pts']:+.1f}$" if v.get('inflation_pts') is not None else '--'
                usd = f"{1000 * v['usd_per_run']:.1f}" if v.get('usd_per_run') is not None else '--'
                rows.append(f"{lab[g] if i == 0 else ''} & {i + 1} & {Sv} & {gs} & {inf} & {usd} \\\\")
            rows.append('\\midrule')
        open(os.path.join(SHI, 'paper', 'tab_loops.tex'), 'w').write('\n'.join(rows[:-1]) + '\n')
    LV = load('results/loops_vs_L.json')
    if LV:
        m('vlvN', LV['n_loops'], '{:d}'); m('vlvWorse', LV['n_worse'], '{:d}'); m('vlvBetter', LV['n_better'], '{:d}')
        ci('vlvBest', LV['best_vs_L']); ci('vlvLgain', LV['L_gain']); ci('vlvCapgain', LV['cap_gain'])
    W = load('results/flagship_summary.json')
    if W:
        names = {'dgm_init': 'Init', 'dgm_best': 'Best', 'moves': 'Moves', 'moves_retry': 'Retry'}
        for a, w in names.items():
            v = W['agents'].get(a)
            if not v: continue
            m(f'vswe{w}Fresh', v['fresh_rate']); m(f'vswe{w}FreshN', v['fresh_resolved'], '{:d}'); m(f'vswe{w}FreshOf', v['fresh_n'], '{:d}')
            m(f'vswe{w}Sel', round(100 * v['dgm_selection_resolved'] / max(1, v['dgm_selection_n']), 1))
            m(f'vswe{w}SelN', v['dgm_selection_resolved'], '{:d}'); m(f'vswe{w}SelOf', v['dgm_selection_n'], '{:d}')
            if v.get('usd_mean') is not None: m(f'vswe{w}Usd', v['usd_mean'], '{:.2f}')
            m(f'vswe{w}Early', v['early_endings'], '{:d}'); m(f'vswe{w}Runs', v['runs'], '{:d}')
        for (x, y), w in {('moves', 'dgm_best'): 'MovesMinusBest', ('dgm_best', 'dgm_init'): 'BestMinusInit',
                          ('moves', 'dgm_init'): 'MovesMinusInit', ('moves_retry', 'dgm_best'): 'RetryMinusBest',
                          ('moves_retry', 'moves'): 'RetryMinusMoves', ('moves_retry', 'dgm_init'): 'RetryMinusInit'}.items():
            for sset, suf in (('fresh', ''), ('dgm_selection', 'Sel')):
                pr = W['pairs'].get(f'{x} - {y} | {sset}')
                if pr:
                    ci(f'vswe{w}{suf}', pr); m(f'vswe{w}{suf}P', pr['mcnemar_p'], '{:.2g}')
                    m(f'vswe{w}{suf}Xonly', pr['x_only'], '{:d}'); m(f'vswe{w}{suf}Yonly', pr['y_only'], '{:d}')
        m('vsweInterim', 'yes' if 'dgm_best' in W.get('interim_sources', []) and not os.path.exists(
            os.path.join(SHI, 'flagship', 'runs_full', 'flag_dgm_best_s45', 'results.jsonl')) else 'no')
    RS = load('results/referee_v2_stats.json')
    if RS:
        ba = RS['batch_adjusted']
        for k, w in (('H6_EBLP_vs_loop3_F2_adj', 'vbaHsix'), ('L_vs_loop3_F_adj', 'vbaL'), ('H8_opus_best_vs_loop3_F2_adj', 'vbaOpusBest'),
                     ('H8_opus_mean_vs_mean_loops_F_adj', 'vbaOpusMean'), ('H8_sonnet_best_vs_loop3_F2_adj', 'vbaSonnetBest'),
                     ('H8_sonnet_mean_vs_mean_loops_F_adj', 'vbaSonnetMean')):
            ci(w, ba[k]); ci_abs(w, ba[k])
        m('vhsixLitBest', ba['H6_literal_best_on_F'].replace('grid_', '')); ci('vhsixLit', ba['H6_literal_vs_loop3_F_raw'])
        ci('vhsixLitAdj', ba['H6_literal_vs_loop3_F_adj'])
        v1s = load('results/summary.json')
        if v1s: m('vhThreeRatio', v1s['hypotheses']['H3']['ratio'], '{:.2f}')
        npl = RS['without_pilot']
        ci('vnpLgain', npl['L_gain_final_FNP']); ci('vnpLoopThreeVsL', npl['loop3_vs_L_final_FNP'])
        m('vnpWorse', npl['loops_vs_L_FNP_n_worse'], '{:d}'); m('vnpBetter', npl['loops_vs_L_FNP_n_better'], '{:d}')
        ci('vnpHsix', npl['H6_EBLP_vs_loop3_F2_raw_FNP']); m('vnpN', RS['n_pilot_in_F'], '{:d}')
        ci('vcapVsLoopFin', npl['cap_vs_loop3_final_F']); ci_abs('vcapVsLoopFin', npl['cap_vs_loop3_final_F'])
        ci('vLVsCapFin', npl['L_vs_cap_final_F'])
        ll = RS['loop_level']
        for k, w in (('hgm_vs_dgm6', 'vllHgm'), ('random_vs_dgm3', 'vllRandomThree'), ('random_vs_dgm6', 'vllRandomSix')):
            m(w + 'P', ll[k]['p'], '{:.2f}'); m(w + 'T', ll[k]['t'], '{:.1f}'); m(w + 'Df', ll[k]['df'], '{:.0f}')
        h2 = RS['H2']
        m('vhtwoMean', h2['hierarchical_mean'], '{:+.1f}'); m('vhtwoLo', h2['hierarchical_lo'], '{:+.1f}'); m('vhtwoHi', h2['hierarchical_hi'], '{:+.1f}')
        m('vhtwoMinInfl', min(v['inflation'] for v in h2['per_loop'].values()), '{:.1f}')
        m('vhtwoMaxInfl', max(v['inflation'] for v in h2['per_loop'].values()), '{:.1f}')
        m('vkMaxTok', RS['k45_seed_max_tokens_share']['pct'], '{:.1f}')
        sc = RS['swe_completion']
        for a, w in (('dgm_init', 'Init'), ('dgm_best', 'Best'), ('moves', 'Moves'), ('moves_retry', 'Retry')):
            v = sc[a]; m(f'vswe{w}FinFresh', 100 * v['finished_fresh_resolved'] / v['finished_fresh'], '{:.1f}')
            m(f'vswe{w}FinFreshN', v['finished_fresh_resolved'], '{:d}'); m(f'vswe{w}FinFreshOf', v['finished_fresh'], '{:d}')
        to = RS['timeouts_pct']
        m('vtoOssSeed', to['F_final_oss.jsonl']['foss_seed_dgm'], '{:.0f}'); m('vtoOssL', to['F_grid_oss.jsonl']['ossgrid_L'], '{:.0f}')
        m('vtoOssLoop', to['F_grid_oss.jsonl']['ossgrid_loopbest'], '{:.0f}')
        m('vtoOssMin', min(v for d in to.values() for a, v in d.items() if 'oss' in a or 'rdoss' in a), '{:.0f}')
        m('vtoOssMax', max(v for d in to.values() for a, v in d.items() if 'oss' in a or 'rdoss' in a), '{:.0f}')
    # unsigned variants of contrasts that appear next to direction words
    for name, src in (('vsweBestMinusInit', 'dgm_best - dgm_init | fresh'), ('vsweRetryMinusMoves', 'moves_retry - moves | fresh'),
                      ('vsweMovesMinusBest', 'moves - dgm_best | fresh'), ('vsweMovesMinusInit', 'moves - dgm_init | fresh'),
                      ('vsweMovesMinusBestSel', 'moves - dgm_best | dgm_selection')):
        if W and W['pairs'].get(src): ci_abs(name, W['pairs'][src])
    if G:
        ci_abs('vgridPgain', G['grid_P']['gain_vs_seed'])
    if H6:
        ci_abs('vHsixL', H6['L_vs_loop3_on_F']); ci_abs('vHsixFtwo', H6['winner_vs_loop3_on_F2'])
    for mod, word in (('opus', 'Opus'), ('sonnet', 'Sonnet')):
        h = (S.get('H8') or {}).get(mod)
        if h: ci_abs(f'vHeight{word}best', h['winner_vs_loop3_on_F2'])
    if O:
        ci_abs('voStronggain', O['agents'].get('foss_seed_strong', {}).get('gain_vs_seed_F'))
    og2 = load('results/oss_grid_summary.json')
    if og2: ci_abs('vogEgain', og2['vogEgain']); ci_abs('vogWinnerFtwo', og2['vogWinnerFtwo'])
    if orr: ci_abs('vorMeanVsLoop', orr['vorMeanVsLoop'])
    SN = load('results/flagship_sensitivity.json')
    if SN:
        for a, w in (('dgm_init', 'Init'), ('dgm_best', 'Best'), ('moves', 'Moves'), ('moves_retry', 'Retry')):
            v = SN['agents'][a]['fresh']; m(f'vsens{w}Fresh', 100 * v['kept_resolved'] / v['n'], '{:.1f}')
            m(f'vsens{w}FreshN', v['kept_resolved'], '{:d}')
        for k, w in (('moves - dgm_best | fresh', 'vsensMovesMinusBest'), ('dgm_best - dgm_init | fresh', 'vsensBestMinusInit'),
                     ('moves - dgm_init | fresh', 'vsensMovesMinusInit'), ('moves - dgm_best | dgm60', 'vsensMovesMinusBestSel'),
                     ('dgm_best - dgm_init | dgm60', 'vsensBestMinusInitSel'), ('moves_retry - dgm_best | fresh', 'vsensRetryMinusBest')):
            ci(w, SN['pairs'][k]); ci_abs(w, SN['pairs'][k]); m(w + 'P', SN['pairs'][k]['mcnemar_p'], '{:.2g}')
        ss = load('flagship/runs_full/sensitivity/sens_summary.json')
        rows = [json.loads(l) for l in open(os.path.join(SHI, 'flagship', 'runs_full', 'sensitivity', 'sens_results.jsonl'))]
        b = [r for r in rows if r['agent'] == 'dgm_best']
        m('vsensBestPatched', sum(1 for r in b if r.get('had_patch')), '{:d}')
        m('vsensBestPatchedResolved', sum(1 for r in b if r.get('had_patch') and r.get('resolved')), '{:d}')
        m('vsensBestPriorPass', sum(1 for r in b if r.get('prior_test_score_1') is True), '{:d}')
    FR = load('flagship/runs_full/final_report.json')
    if FR:
        ec = FR['agents']['dgm_best']['early_codes']
        m('vsweBestEarlySig', int(ec.get('137', 0)) + int(ec.get('143', 0)), '{:d}'); m('vsweBestEarlyOne', int(ec.get('1', 0)), '{:d}')
        # machine load during the run: share of runs with per-minute load samples, and rates by per-agent load tertile
        ags = FR['agents']; srcs = [v['load_sources'] for v in ags.values()]
        m('vloadSampledPct', 100 * sum(x['sampled'] + x['partly_sampled'] for x in srcs) / sum(sum(x.values()) for x in srcs), '{:.0f}')
        m('vloadFullPct', 100 * sum(x['sampled'] for x in srcs) / sum(sum(x.values()) for x in srcs), '{:.0f}')
        m('vloadPartPct', 100 * sum(x['partly_sampled'] for x in srcs) / sum(sum(x.values()) for x in srcs), '{:.0f}')
        m('vloadMovesApprox', ags['moves']['load_sources']['approx'], '{:d}')
        m('vloadMax', max(t['load_range'][1] for v in ags.values() for t in v['load_tertiles'].values()), '{:.0f}')
        for a, w in (('dgm_init', 'Init'), ('dgm_best', 'Best'), ('moves', 'Moves'), ('moves_retry', 'Retry')):
            for tk, tw in (('low', 'Lo'), ('mid', 'Mid'), ('high', 'Hi')):
                t = ags[a]['load_tertiles'][tk]
                for rk, rw in (('early_rate', 'early'), ('resolve_rate', 'res')):
                    m(f'v{rw}{w}{tw}', 100 * round(t[rk] * t['n']) / t['n'], '{:.0f}')   # counts recovered from the stored rate
    PE = load('results/pilot_empty.json')
    if PE:
        m('vpilotRuns', PE['runs'], '{:d}'); m('vpilotNoSol', PE['no_solution'], '{:d}')
        m('vpilotEmptyResp', PE['no_solution_ending_on_empty_response'], '{:d}')
    KS = load('results/swe_kill_scan.json')
    if KS:
        m('vsweKillLogs', KS['logs_with_kill'], '{:d}'); m('vsweKillOf', KS['logs_found'], '{:d}')
        m('vsweKillNonEmpty', KS['logs_nonempty'], '{:d}'); m('vsweKillEmpty', KS['logs_found'] - KS['logs_nonempty'], '{:d}')
        m('vsweKillNone', KS['logs_nonempty'] - KS['logs_with_kill'], '{:d}')
    MS = load('results/misc_v2.json')
    if MS:
        for a, w in (('dgm_init', 'Init'), ('dgm_best', 'Best'), ('moves', 'Moves'), ('moves_retry', 'Retry')):
            m(f'vswe{w}MedMin', MS[f'swe_median_min_{a}'], '{:.0f}')
        m('vdropWorse', MS['drop_worse'], '{:d}'); m('vdropWorseLonger', MS['drop_worse_longer'], '{:d}')
        m('vdropLenAgent', MS['drop_median_len_agent'], '{:.0f}'); m('vdropLenCot', MS['drop_median_len_cotsc'], '{:.0f}')
    R2 = load('results/referee_v2_stats_r2.json')
    if R2:
        ci('vltwoRaw', R2['L2']['raw_F']); ci('vltwoAdj', R2['L2']['adj_F']); ci('vltwoRawNP', R2['L2']['raw_FNP'])
        ps = R2['prespec']
        for k, w in (('EBLP_raw_F', 'vpsEBLPRaw'), ('EBLP_adj_F', 'vpsEBLPAdj'), ('L_raw_F', 'vpsLRaw'), ('L_adj_F', 'vpsLAdj')):
            ci(w, ps[k]); ci_abs(w, ps[k])
        lc = R2['L_combos_vs_loop3']
        m('vlcFtwoMin', lc['F2_min'], '{:+.1f}'); m('vlcFtwoMax', lc['F2_max'], '{:+.1f}'); m('vlcN', lc['n'], '{:d}')
        m('vlcMiss', lc['F_miss_margin'], '{:d}'); m('vlcSig', lc['F_sig_behind'], '{:d}')
        m('vlcFMin', lc['F_min'], '{:+.1f}'); m('vlcFMax', lc['F_max'], '{:+.1f}')
        for mod, w in (('opus', 'Opus'), ('sonnet', 'Sonnet')):
            h = R2[f'H8_literal_{mod}']; ci(f'vheightLit{w}Raw', h['raw_F']); ci(f'vheightLit{w}Adj', h['adj_F'])
            ci_abs(f'vheightLit{w}Raw', h['raw_F'])
        sv = R2['seed_vs_seed']; ci('vsvAblRedFtwo', sv['ablate_minus_redesign_F2']); ci('vsvAblGridF', sv['ablate_minus_grid_F'])
        ci('vsvAblRedF', sv['ablate_minus_redesign_F'])
        bt = R2['batch_times']
        m('vbtGrid', f"{bt['F_grid'][0][:5]} to {bt['F_grid'][1][:5]}"); m('vbtAbl', f"{bt['F_ablate'][0][:5]} to {bt['F_ablate'][1][:5]}")
        m('vbtRed', f"{bt['F_redesign'][0][:5]} to {bt['F_redesign'][1][:5]}")
        tm = R2['terminations']
        m('vsigKSeed', tm['F_final_k45.jsonl']['fk45_seed_dgm']['signal_pct'], '{:.0f}')
        m('vsigKSeedTr', tm['X_claude-haiku-4-5.jsonl']['seed_dgm']['signal_pct'], '{:.0f}')
        m('vsigKOne', tm['F_final_k45.jsonl']['fk45_v3_K45_dgm_s1__g008_0']['signal_pct'], '{:.0f}')
        m('vsigKTwo', tm['F_final_k45.jsonl']['fk45_v3_K45_dgm_s2__g006_1']['signal_pct'], '{:.0f}')
        m('vsigKStrong', tm['F_final_k45.jsonl']['fk45_seed_strong']['signal_pct'], '{:.0f}')
        m('vsigKAone', tm['X_claude-haiku-4-5.jsonl']['A1best']['signal_pct'], '{:.0f}')
        m('vsigSSeed', tm['X_claude-sonnet-4-6.jsonl']['seed_dgm']['signal_pct'], '{:.0f}')
        m('vsigHSeed', tm['F_seeds.v2.jsonl']['seed_dgm']['signal_pct'], '{:.1f}')
        m('vbudKTwo', tm['F_final_k45.jsonl']['fk45_v3_K45_dgm_s2__g006_1']['budget_pct'], '{:.0f}')
        m('vtoKTwo', tm['F_final_k45.jsonl']['fk45_v3_K45_dgm_s2__g006_1']['timeout_pct'], '{:.0f}')
        m('vtoKOne', tm['F_final_k45.jsonl']['fk45_v3_K45_dgm_s1__g008_0']['timeout_pct'], '{:.0f}')
        m('vbudKStrong', tm['F_final_k45.jsonl']['fk45_seed_strong']['budget_pct'], '{:.0f}')
        m('vbudTrKThreeN', tm['X_claude-haiku-4-5.jsonl']['A3best']['budget_n'], '{:d}')
        m('vbudTrSThreeN', tm['X_claude-sonnet-4-6.jsonl']['A3best']['budget_n'], '{:d}')
        m('vtoOssThree', tm['F_final_oss.jsonl']['foss_v3_O_dgm_s3__g006_0']['timeout_pct'], '{:.0f}')
        osk = R2['oss_seed_at_k']; kk = str(osk['k'])
        m('vossSkK', osk['k'], '{:d}'); m('vossSkAcc', osk['curve'][kk]['acc']); m('vossSkUsd', 1000 * osk['curve'][kk]['usd_per_task'])
        m('vossLoopUsd', 1000 * osk['loop_usd']); ci('vossLoopMinusSk', osk['loop_minus_seed_at_k_F1'])
    H5 = load('results/h5_both_loops.json')
    if H5:
        for k, w in (('claude-haiku-4-5|A1best', 'vhfiveKOne'), ('claude-haiku-4-5|A3best', 'vhfiveKThree'),
                     ('claude-sonnet-4-6|A1best', 'vhfiveSOne'), ('claude-sonnet-4-6|A3best', 'vhfiveSThree')):
            ci(w, H5[k])
    if H7 and H7.get('hgm_minus_dgm_all6'): ci_abs('vhHgmMinusDgmAll', H7['hgm_minus_dgm_all6'])
    if l3: ci_abs('vlastedit', l3['loo_drops'].get('minus_g024_0'))
    if 'loop3_semantic_cap_drop' in H9: ci_abs('vsemcapdrop', H9['loop3_semantic_cap_drop'])
    # rows for the references measured in the final batch (seed, cap-only seed, L), appended to the loop table
    if LV and S.get('final'):
        fin = S['final']; extra = ['\\midrule']
        for name, lab in (('fin_seed_dgm', 'seed'), ('fin_seed_dgm_cap16k', 'cap-only seed'), ('fin_grid_L', 'L (textbook move)')):
            v = fin.get(name)
            if not v: continue
            g = v.get('gain_vs_seed'); gs = f"${g['diff']:+.1f}$ [${g['lo']:+.1f}$, ${g['hi']:+.1f}$]" if g else f"$F$ = {v['F']:.1f}\\%"
            extra.append(f"{lab} & -- & -- & {gs} & -- & {1000 * v['usd_per_run']:.1f} \\\\")
        tl = os.path.join(SHI, 'paper', 'tab_loops.tex')
        if os.path.exists(tl):
            body = open(tl).read().rstrip('\n').split('\n')
            body = [b for b in body if not b.startswith(('seed &', 'cap-only seed &', 'L (textbook move) &'))]
            while body and body[-1] == '\\midrule': body.pop()
            open(tl, 'w').write('\n'.join(body + extra) + '\n')
    KG = load('results/k45_grid_summary.json')
    if KG:
        for k, v in KG.items():
            if isinstance(v, dict) and 'diff' in v: ci(k, v); ci_abs(k, v)
            elif isinstance(v, int): m(k, v, '{:d}')
            elif isinstance(v, float): m(k, v)
    with open(os.path.join(SHI, 'paper', 'numbers_v2.tex'), 'w') as f:
        for k in sorted(mac): f.write(f'\\newcommand{{\\{k}}}{{{mac[k]}}}\n')
    print(f'{len(mac)} macros; tables: grid {len(rows)} rows, redesign {len(rrows)}, adas {len(arows)}')

if __name__ == '__main__':
    main()

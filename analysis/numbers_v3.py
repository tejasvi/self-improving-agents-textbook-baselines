"""Third-round (PREREG_v3) macros for the paper: reads results/r3_swe.json (E1), results/r3_redesign_lf.json (E3) and,
when present, results/r3_loops.json (E2); writes paper/numbers_v3.tex. Values are rounded here, once."""
import json, os
SHI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mac = {}
def m(name, val, fmt='{:.1f}'):
    assert name.isalpha(), name
    s = fmt.format(val) if not isinstance(val, str) else val
    if s.startswith('-') and float(s) == 0: s = s[1:]
    if s.startswith('+') and float(s) == 0: s = '0.0' if '.' in s else '0'
    mac[name] = s
def ci(p, d, sign=True):
    f = '{:+.1f}' if sign else '{:.1f}'
    m(p, d['diff'], f); m(p + 'lo', d['lo'], f); m(p + 'hi', d['hi'], f)
def ci_abs(p, d):
    v = [d['diff'], d['lo'], d['hi']]
    if v[0] < 0: v = [-v[0], -v[2], -v[1]]
    v = [0.0 if abs(x) < 0.05 else x for x in v]
    m(p + 'Abs', v[0]); m(p + 'Abslo', v[1]); m(p + 'Abshi', v[2])
def pval(name, p):   # for math mode: two significant digits, powers of ten below 0.001
    if p < 0.001:
        mant, ex = f'{p:.1e}'.split('e'); m(name, f'{mant}\\times10^{{{int(ex)}}}')
    else:
        m(name, p, '{:.2g}')
def load(p):
    p = os.path.join(SHI, p); return json.load(open(p)) if os.path.exists(p) else None
E1 = load('results/r3_swe.json')
if E1:
    m('wN', E1['n_tasks'], '{:d}')
    for a, w in (('dgm_init_16k', 'Init'), ('dgm_best_16k', 'Best'), ('moves', 'Moves')):
        v = E1['agents'][a]
        m(f'w{w}N', v['resolved'], '{:d}'); m(f'w{w}Rate', v['rate']); m(f'w{w}Early', v['early'], '{:d}')
        m(f'w{w}Usd', v['usd_mean'], '{:.2f}'); m(f'w{w}Min', v['wall_median_min'], '{:.0f}')
        m(f'w{w}Kept', E1['sensitivity']['rates'][a])
    codes = E1['agents']['dgm_best_16k']['early_codes']
    m('wBestEarlySig', int(codes.get('137', 0)) + int(codes.get('143', 0)), '{:d}'); m('wBestEarlyOne', int(codes.get('1', 0)), '{:d}')
    for k, w in (('H11_moves_minus_best16k', 'wMovesBest'), ('H12_best16k_minus_init16k', 'wBestInit'), ('H13_moves_minus_init16k', 'wMovesInit')):
        d = E1['contrasts'][k]; ci(w, d); ci_abs(w, d); pval(w + 'P', d['mcnemar_p'])
    for k, w in (('H11', 'wsMovesBest'), ('H12', 'wsBestInit'), ('H13', 'wsMovesInit')):
        d = E1['sensitivity'][k]; ci(w, d); ci_abs(w, d); pval(w + 'P', d['mcnemar_p'])
    cb = E1['cross_batch']
    for k, w in (('best16k_minus_v2best', 'wxBest'), ('init16k_minus_v2init', 'wxInit'), ('moves_r3_minus_moves_v2', 'wxMoves')):
        ci(w, cb[k]); ci_abs(w, cb[k])
    for a, w in (('dgm_init', 'Init'), ('dgm_best', 'Best'), ('moves', 'Moves')):
        m(f'wv{w}Rate', cb['v2_rates_same_tasks'][a]); m(f'wv{w}Early', cb['v2_early_same_tasks'][a], '{:d}')
    m('wBestEarlyBoth', cb['best_early_both_rounds'], '{:d}')
    oo = E1['oom']; assert len(oo['kills']) == 1, oo['kills']
    m('wOomN', len(oo['kills']), '{:d}'); m('wOomInProg', len(oo['in_progress'][0]), '{:d}')
    m('wOomEarlyTen', len(oo['early_within_10min'][0]), '{:d}')
    import datetime as dt
    k0 = dt.datetime.fromisoformat(oo['kills'][0]); later = [dt.datetime.fromisoformat(x[2]) for x in oo['in_progress'][0] if x[3]]
    m('wOomEarlyLater', len(later), '{:d}'); m('wOomGapMin', min((t - k0).total_seconds() for t in later) / 60, '{:.0f}')
lp = os.path.join(SHI, 'flagship', 'runs_r3', 'loadlog.tsv')
if os.path.exists(lp):
    lv = [float(l.split('\t')[1]) for l in open(lp) if not l.startswith('utc')]
    m('wLoadMax', max(lv), '{:.0f}')
lp2 = os.path.join(SHI, 'flagship', 'runs_full', 'loadlog.tsv')   # second round, same one-minute samples
if os.path.exists(lp2):
    m('wvLoadMax', max(float(l.split('\t')[1]) for l in open(lp2) if not l.startswith('utc')), '{:.0f}')
E3 = load('results/r3_redesign_lf.json')
if E3:
    m('lfSeedF', E3['agents']['lf_seed_dgm']['F'])
    ci('lfMeanFree', E3['mean_logfree_gain']); ci('lfMeanBased', E3['mean_logbased_gain'])
    ci('lfDiff', E3['logfree_minus_logbased']); ci_abs('lfDiff', E3['logfree_minus_logbased'])
    m('lfRaised', E3['H15a_logfree_raised'], '{:d}')
    g = [E3['agents'][f'lf_opuslf_r{i}']['gain_vs_seed']['diff'] for i in range(5)]
    m('lfGainMin', min(g)); m('lfGainMax', max(g))
    xr = E3['exploratory_raisers']
    ci('lfRaiseFree', xr['logfree_gain']); ci('lfRaiseBased', xr['logbased_gain'])
    ci('lfRaiseDiff', xr['logfree_minus_logbased']); ci_abs('lfRaiseDiff', xr['logfree_minus_logbased'])
    kf = [a for a in (f'lf_opuslf_r{i}' for i in range(5)) if a not in xr['logfree']]
    kb = [a for a in (f'lf_opus_r{i}' for i in range(5)) if a not in xr['logbased']]
    assert len(kf) == 1 and len(kb) == 1, (kf, kb)
    m('lfKeepFree', E3['agents'][kf[0]]['gain_vs_seed']['diff'], '{:+.1f}'); m('lfKeepBased', E3['agents'][kb[0]]['gain_vs_seed']['diff'], '{:+.1f}')
E2 = load('results/r3_loops.json')
if E2:
    m('rcSeedF', E2['seed_F']); ci('rcL', E2['L'])
    for gname, w in (('clean_random', 'Clean'), ('dgm_all', 'DgmAll'), ('dgm_same_time', 'DgmNew'), ('dgm_earlier', 'DgmOld'), ('random_v2', 'RandOld')):
        ci(f'rc{w}', E2['groups'][gname]['mean_gain'])
    for k, w in (('H14_clean_minus_dgm_all', 'rcHfourteen'), ('clean_minus_dgm_same_time', 'rcCleanNew'), ('clean_minus_random_v2', 'rcCleanOld'),
                 ('dgm_same_time_minus_dgm_earlier', 'rcNewOld')):
        d = E2[k]; ci(w, d); ci_abs(w, d); m(w + 'P', d['welch_p'], '{:.2f}')
    m('rcHfourteenVerdict', 'supported' if E2['H14_noninferior'] else 'not supported')
    for k, w in (('exploratory_random_v2_minus_dgm_all', 'rcRandAll'), ('exploratory_random_v2_minus_dgm_first_round', 'rcRandFirst')):
        d = E2[k]; ci(w, d); ci_abs(w, d); m(w + 'P', d['welch_p'], '{:.2f}')
    ci('rcLoopThreeL', E2['exploratory_loop3_minus_L']); ci_abs('rcLoopThreeL', E2['exploratory_loop3_minus_L'])
    for e, w in (('v4_RMC_s11', 'One'), ('v4_RMC_s12', 'Two'), ('v4_RMC_s13', 'Three'), ('v4_RMC_s14', 'Four'), ('v4_RMC_s15', 'Five')):
        m('rcLoop' + w, E2['loops'][e]['gain']['diff'], '{:+.1f}')
    gs = E2['groups']['clean_random']['loop_gains']; m('rcCleanMin', min(gs), '{:+.1f}'); m('rcCleanMax', max(gs), '{:+.1f}')
    gd = E2['groups']['dgm_all']['loop_gains']; m('rcDgmMin', min(gd), '{:+.1f}'); m('rcDgmMax', max(gd), '{:+.1f}')
with open(os.path.join(SHI, 'paper', 'numbers_v3.tex'), 'w') as f:
    for k in sorted(mac): f.write(f'\\newcommand{{\\{k}}}{{{mac[k]}}}\n')
print(len(mac), 'macros')

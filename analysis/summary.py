"""Compute every headline number of the paper from result files; write results/summary.json and paper/numbers.tex.

Rerun after the loops finish (exp/finish.sh does): the paper's numbers come only from here (\\input{numbers.tex}).
Conventions: fresh gains are paired by problem against the seed's mean over its fresh reruns; pooled fresh = F1 and F2
(232 problems) when both exist; best-of-n ties are broken by the earliest member (pre-registered); 95% bootstrap CIs.
"""
import json, os, sys, glob, collections, re
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from collect import collect, read_evals
from curves import curve, emax
import ladder_report as LR
SHI = os.path.expanduser('~/shi_eval')
SP = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json'))); F1 = SP['fresh'][:116]; F2 = SP['fresh'][116:]; F = SP['fresh']
out = {}; mac = {}
rng = np.random.default_rng(1)

def m(name, val, fmt='{:.1f}'):
    assert re.fullmatch(r'[A-Za-z]+', name), name
    mac[name] = fmt.format(val) if isinstance(val, (int, float, np.floating, np.integer)) else str(val)
def pts(x): return 100 * x
def pair_text(vals, fmt, unit='', each=' each'):
    """'v1 and v2 unit' or 'v unit each' when all formatted values coincide (state shared values once)."""
    f = [fmt.format(v) for v in vals]
    if len(set(f)) == 1: return f'{f[0]}{unit}{each}'
    return (', '.join(f[:-1]) + ' and ' + f[-1] + unit) if len(f) > 1 else f[0] + unit
def boot(g, B=4000):
    g = np.asarray(g, float); bs = g[rng.integers(0, len(g), (B, len(g)))].mean(1)
    return float(g.mean()), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
def idx_key(aid):
    nums = [int(x) for x in re.findall(r'\d+', aid)]; return nums

# ---------- seed references ----------
SEED_POOLS = ['F_seeds.v2.jsonl', 'F1_seeds_extra.jsonl', 'F1_seeds_extra2.jsonl', 'F1_seeds_extra3.jsonl']
def seed_runs(name):
    d = collections.defaultdict(list)
    for fn in SEED_POOLS:
        p = os.path.join(SHI, 'results', fn)
        if not os.path.exists(p): continue
        for l in open(p):
            r = json.loads(l)
            if r['agent'] == name: d[r['task']].append(r)
    return d
def seed_fresh(name):
    # reference = mean over every available run of the unchanged seed (morning and evening batches pooled)
    return {t: float(np.mean([float(r['passed']) for r in v])) for t, v in seed_runs(name).items()}
ref = {'seed_dgm': seed_fresh('seed_dgm'), 'seed_strong': seed_fresh('seed_strong')}

def seed_S_runs(strong):
    vals = []
    for d in glob.glob(os.path.join(SHI, 'exps', 'v2_*')):
        cfg = json.load(open(os.path.join(d, 'config.json')))
        if ('strong' in cfg['seed_dir']) != strong: continue
        cfg_, st, recs = collect(os.path.basename(d))
        for r in recs:   # the seed itself, and placebo copies (identical code)
            if r['sel_full'] and (r['aid'] == 'initial' or (cfg['mode'] == 'placebo' and r['compiled'])):
                vals.append(r['sel'])
    return np.array(vals)
for nm, strong in (('Dgm', False), ('Strong', True)):
    v = seed_S_runs(strong)
    out[f'seed{nm}_S_runs'] = dict(n=int(len(v)), mean=float(v.mean()), sd=float(v.std(ddof=1)), max=float(v.max()))
    m(f'seed{nm}Smean', pts(v.mean())); m(f'seed{nm}Ssd', pts(v.std(ddof=1))); m(f'seed{nm}Sn', len(v), '{:d}')
    m(f'seed{nm}Smax', pts(v.max()), '{:.0f}')
    k = 'seed_strong' if strong else 'seed_dgm'
    m(f'seed{nm}Fone', pts(np.mean([ref[k][t] for t in F1]))); m(f'seed{nm}Fall', pts(np.mean([ref[k][t] for t in F])))
SD = out['seedDgm_S_runs']; SS = out['seedStrong_S_runs']

# ---------- placebo ----------
pl = []
for e in ['v2_B_placebo_s1', 'v2_B_placebo_s2', 'v2_B_placebo_s3']:
    cfg, st, recs = collect(e)
    full = [r for r in recs if r['sel_full'] and r['compiled']]
    best = max(r['sel'] for r in full); n = len(full)
    pl.append(dict(exp=e, gen=st['generation'], n_full=n, best_S=best, pred=SD['mean'] + SD['sd'] * emax(n)))
out['placebo'] = pl
for i, x in enumerate(pl):
    m(f'placeboBest{"ABC"[i]}', pts(x['best_S']), '{:.0f}'); m(f'placeboN{"ABC"[i]}', x['n_full'], '{:d}')
    m(f'placeboPred{"ABC"[i]}', pts(x['pred']))
cfg, st, recs = collect('v2_E_strong_placebo_s1')
fulls = [r for r in recs if r['sel_full'] and r['compiled']]
out['strong_placebo'] = dict(gen=st['generation'], n_full=len(fulls), best_S=max(r['sel'] for r in fulls),
                             pred=SS['mean'] + SS['sd'] * emax(len(fulls)))
m('placeboNtext', (f"{pl[0]['n_full']} copies each" if len({x['n_full'] for x in pl}) == 1 else f"{min(x['n_full'] for x in pl)} to {max(x['n_full'] for x in pl)} copies"))
m('placeboPredText', pair_text([pts(x['pred']) for x in pl], '{:.1f}', '\\%', ' for each loop'))
m('strongPlaceboBest', pts(out['strong_placebo']['best_S']), '{:.0f}'); m('strongPlaceboPred', pts(out['strong_placebo']['pred']))
m('strongPlaceboGen', st['generation'], '{:d}'); m('strongPlaceboN', len(fulls), '{:d}')

# ---------- loop bests ----------
def fresh_vec(exp, aid, tasks):
    d = {}
    for stg in ('fresh1', 'fresh2'):
        ev = read_evals(os.path.join(SHI, 'exps', exp, 'agents', aid), stg).get(0, {})
        for t, r in ev.items(): d[t] = (float(r['passed']), r.get('usd', 0.0))
    if not all(t in d for t in tasks): return None, None
    return np.array([d[t][0] for t in tasks]), float(np.mean([d[t][1] for t in tasks]))
def sel_reruns(exp, aid):
    ev = read_evals(os.path.join(SHI, 'exps', exp, 'agents', aid), 'sel')
    S = SP['small'] + SP['medium']
    return [float(np.mean([v[t]['passed'] for t in S])) for rep, v in sorted(ev.items()) if all(t in v for t in S)]
sk = json.load(open(os.path.join(SHI, 'results', 'seed_at_k.json')))
def matched_k(seedname, usd):
    ks = sorted((int(k) for k in sk[seedname] if k.isdigit()))
    for k in ks:
        if sk[seedname][str(k)]['usd_per_task'] >= usd: return k, True
    return ks[-1], False
loops = {}
LOOPS = [('LoopA', 'v2_A_dgm_s1', 'seed_dgm'), ('LoopB', 'v2_A_dgm_s2', 'seed_dgm'), ('LoopC', 'v2_A_dgm_s3', 'seed_dgm'),
         ('NohintA', 'v2_A_nohint_s1', 'seed_dgm'), ('NohintB', 'v2_A_nohint_s2', 'seed_dgm'),
         ('StrongA', 'v2_E_strong_dgm_s1', 'seed_strong'), ('StrongB', 'v2_E_strong_dgm_s2', 'seed_strong')]
for key, e, sn in LOOPS:
    cfg, st, recs = collect(e); b = LR.loop_best(recs)
    if not b or b['aid'] == 'initial': continue
    base = SS if 'strong' in sn else SD
    rec = dict(exp=e, aid=b['aid'], best_gen=b['gen'], loop_gen=st['generation'], S=b['sel'], S_gain=b['sel'] - base['mean'])
    v1, u1 = fresh_vec(e, b['aid'], F1)
    if v1 is not None:
        g = v1 - np.array([ref[sn][t] for t in F1]); rec['F1'] = float(v1.mean()); rec['usd'] = u1; rec['F1_gain'] = boot(g)
        m(f'gain{key}', pts(rec['F1_gain'][0])); m(f'gain{key}lo', pts(rec['F1_gain'][1]), '{:+.1f}'); m(f'gain{key}hi', pts(rec['F1_gain'][2]), '{:+.1f}')
        m(f'fone{key}', pts(rec['F1'])); m(f'usd{key}', 1000 * u1, '{:.1f}')
        k, reached = matched_k(sn, u1); pt = sk[sn][str(k)]['per_task_acc']
        d = v1 - np.array([pt[t] for t in F1]); rec['vs_seed_at_k'] = dict(k=k, cost_reached=reached, diff=boot(d))
        m(f'vsk{key}', pts(rec['vs_seed_at_k']['diff'][0]), '{:+.1f}'); m(f'vsk{key}lo', pts(rec['vs_seed_at_k']['diff'][1]), '{:+.1f}')
        m(f'vsk{key}hi', pts(rec['vs_seed_at_k']['diff'][2]), '{:+.1f}'); m(f'vsk{key}k', k, '{:d}')
    va, ua = fresh_vec(e, b['aid'], F)
    if va is not None:
        g = va - np.array([ref[sn][t] for t in F]); rec['F_gain'] = boot(g)
        m(f'gainall{key}', pts(rec['F_gain'][0])); m(f'gainall{key}lo', pts(rec['F_gain'][1]), '{:+.1f}'); m(f'gainall{key}hi', pts(rec['F_gain'][2]), '{:+.1f}')
    rr = sel_reruns(e, b['aid'])
    if rr: rec['S_reruns'] = rr; m(f'Srerun{key}', pts(np.mean(rr)), '{:.0f}')
    m(f'S{key}', pts(b['sel']), '{:.0f}'); m(f'Sgain{key}', pts(rec['S_gain'])); m(f'gen{key}', st['generation'], '{:d}')
    m(f'bgen{key}', b['gen'] + 1 if isinstance(b['gen'], int) else 0, '{:d}')
    loops[key] = rec
out['loops'] = loops

# ---------- ladder (single edits, chains) ----------
def ladder(exp, sn):
    cfg, st, recs = collect(exp)
    kids = [r for r in recs if r['aid'] != 'initial' and r['mode'] != 'placebo']
    base = np.array([ref[sn][t] for t in F1])
    mem = []
    for r in kids:
        if r['compiled'] and r['sel_full']:
            v, u = fresh_vec(exp, r['aid'], F1)
            if v is not None: mem.append((r, v - base))
    attempted = len(kids); failed = sum(1 for r in kids if not r['compiled'])
    res = dict(attempted=attempted, failed=failed, evaluated=len(mem))
    if mem:
        mat = np.array([g for _, g in mem]); est, lo, hi = LR.boot_mean_ci(mat)
        res.update(mean=float(est), lo=float(lo), hi=float(hi))
        # intention-to-treat: children that failed to compile (or never reached the full selection set) keep the seed (gain 0)
        res['itt_mean'] = float(mat.mean(1).sum() / max(1, len(mem) + failed))   # failed children count as unchanged
        best = sorted(mem, key=lambda x: (-x[0]['sel'], idx_key(x[0]['aid'])))[0]
        res.update(best=best[0]['aid'], best_S=best[0]['sel'], best_gain=boot(best[1]))
    return res
lad = {}
for key, e, sn in [('Cone', 'v2_C1_nolog', 'seed_dgm'), ('Ctwo', 'v2_C2_single', 'seed_dgm'), ('Cthree', 'v2_C3_nohint', 'seed_dgm'),
                   ('Done', 'v2_D_chain1', 'seed_dgm'), ('Dtwo', 'v2_D_chain2', 'seed_dgm'),
                   ('SCone', 'v2_E_strong_C1_nolog', 'seed_strong'), ('SCtwo', 'v2_E_strong_C2_single', 'seed_strong')]:
    r = ladder(e, sn); lad[key] = r
    m(f'lad{key}att', r['attempted'], '{:d}'); m(f'lad{key}fail', r['failed'], '{:d}'); m(f'lad{key}n', r['evaluated'], '{:d}')
    if 'mean' in r:
        m(f'lad{key}', pts(r['mean']), '{:+.1f}'); m(f'lad{key}lo', pts(r['lo']), '{:+.1f}'); m(f'lad{key}hi', pts(r['hi']), '{:+.1f}')
        m(f'lad{key}itt', pts(r['itt_mean']), '{:+.1f}')
        m(f'lad{key}best', pts(r['best_gain'][0]), '{:+.1f}'); m(f'lad{key}bestS', pts(r['best_S']), '{:.0f}')
    else:
        for suf in ('', 'lo', 'hi', 'itt', 'best', 'bestS'): m(f'lad{key}{suf}', '--')
out['ladder'] = lad
cfg, st, recs = collect('v2_C2_single')
kinds = collections.Counter((r['kind'], bool(r['compiled'])) for r in recs if r['aid'] != 'initial')
out['C2_kinds'] = {f'{k}|{"compiled" if c else "failed"}': v for (k, c), v in kinds.items()}
m('ctwoEmptyOK', kinds.get(('empty_patch', True), 0), '{:d}'); m('ctwoEmptyFail', kinds.get(('empty_patch', False), 0), '{:d}')
m('ctwoStochOK', kinds.get(('stochasticity', True), 0), '{:d}'); m('ctwoStochFail', kinds.get(('stochasticity', False), 0), '{:d}')
m('ctwoTaskOK', kinds.get(('task', True), 0), '{:d}')
# loop-3 lineage kinds
a = loops.get('LoopC', {}).get('aid'); lin = []
while a and a != 'initial':
    mm = json.load(open(os.path.join(SHI, 'exps', 'v2_A_dgm_s3', 'agents', a, 'meta.json'))); lin.append(mm.get('kind')); a = mm['parent']
out['loopC_lineage_kinds'] = list(reversed(lin))
m('linCn', len(lin), '{:d}'); m('linCempty', sum(1 for k in lin if k == 'empty_patch'), '{:d}')

# ---------- compute-matched curve ----------
for nm, k in (('Dgm', 'seed_dgm'), ('Strong', 'seed_strong')):
    m(f'atk{nm}kmax', sk[k]['kmax'], '{:d}')
    for kk, word in (('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('6', 'Six'), ('8', 'Eight'), ('12', 'Twelve')):
        if kk in sk[k]:
            m(f'atk{nm}{word}', pts(sk[k][kk]['acc'])); m(f'atk{nm}{word}usd', 1000 * sk[k][kk]['usd_per_task'], '{:.1f}')
            m(f'orc{nm}{word}', pts(sk[k][kk]['oracle_any_pass']))
cap = os.path.join(SHI, 'results', 'F1_cap16k.jsonl')
if os.path.exists(cap):
    d = collections.defaultdict(list); usd = []
    for l in open(cap):
        r = json.loads(l); d[r['task']].append(float(r['passed'])); usd.append(r.get('usd', 0))
    if all(t in d for t in F1):
        v = np.array([np.mean(d[t]) for t in F1]); g = v - np.array([ref['seed_dgm'][t] for t in F1])
        out['cap16k'] = dict(F1=float(v.mean()), gain=boot(g), usd=float(np.mean(usd)), reps=float(np.mean([len(d[t]) for t in F1])))
        m('capFone', pts(v.mean())); m('capGain', pts(out['cap16k']['gain'][0]), '{:+.1f}'); m('capGainlo', pts(out['cap16k']['gain'][1]), '{:+.1f}')
        m('capGainhi', pts(out['cap16k']['gain'][2]), '{:+.1f}'); m('capUsd', 1000 * out['cap16k']['usd'], '{:.1f}')

# ---------- quirk ----------
if os.path.exists(os.path.join(SHI, 'results', 'quirk.json')):
    q = json.load(open(os.path.join(SHI, 'results', 'quirk.json'))); out['quirk'] = q
    for key, e in (('QA', 'E_strong_dgm_s1'), ('QB', 'E_strong_dgm_s2'), ('QC', 'A_dgm_s1'), ('QD', 'A_dgm_s2')):
        if e in q:
            m(f'{key}meas', pts(q[e]['measured_gain']), '{:+.0f}'); m(f'{key}corr', pts(q[e]['corrected_gain']), '{:+.0f}')
            m(f'{key}rho', q[e]['spearman_v1_v2'], '{:.2f}'); m(f'{key}n', q[e]['n_agents'], '{:d}')

# ---------- transfer: every evaluated agent ----------
import transfer_report as TR
tr = {}
for key, mdl in (('Hfour', 'claude-haiku-4-5'), ('Sfour', 'claude-sonnet-4-6'), ('Sfive', 'claude-sonnet-5-5'),
                 ('Gem', 'gemini-2.5-flash'), ('Oss', 'openai_gpt-oss-120b-maas')):
    d = TR.load(f'X_{mdl}')
    if not d or not d.get('seed_dgm'): continue
    row = {}
    for ag in ('seed_dgm', 'seed_strong', 'A1best', 'A2best', 'A3best', 'C2best', 'E2best'):
        ts = [t for t in F1 if d[ag].get(t)]
        if len(ts) >= 100: row[ag] = dict(n=len(ts), acc=float(np.mean([np.mean(d[ag][t]) for t in ts])))
    for ag in ('A1best', 'A2best', 'A3best', 'C2best'):
        g = TR.gain(d, ag, 'seed_dgm')
        if g: row[ag + '_gain'] = [float(x) for x in g[:3]]
    g = TR.gain(d, 'E2best', 'seed_strong')
    if g: row['E2best_gain_vs_strong'] = [float(x) for x in g[:3]]
    g = TR.gain(d, 'seed_strong', 'seed_dgm')
    if g: row['strong_minus_dgm'] = [float(x) for x in g[:3]]
    # runs that hit the per-task budget (censored) and cost ratio of the loop-3 agent to the seed
    raw = collections.defaultdict(list)
    for l in open(os.path.join(SHI, 'results', f'X_{mdl}.jsonl')):
        r = json.loads(l); raw[r['agent']].append(r)
    for ag in ('seed_dgm', 'seed_strong', 'A3best', 'A1best'):
        if raw.get(ag):
            budget = 1.0 if mdl != 'openai_gpt-oss-120b-maas' else 0.25
            row.setdefault('capped', {})[ag] = sum(1 for r in raw[ag] if r.get('usd', 0) >= 0.98 * budget)
            row.setdefault('usd', {})[ag] = float(np.mean([r.get('usd', 0) for r in raw[ag]]))
    if 'usd' in row and 'A3best' in row['usd'] and row['usd'].get('seed_dgm'):
        row['A3best_cost_ratio'] = row['usd']['A3best'] / row['usd']['seed_dgm']
    tr[mdl] = row
    if 'capped' in row:
        m(f'tr{key}capThree', row['capped'].get('A3best', 0), '{:d}'); m(f'tr{key}capSeed', row['capped'].get('seed_dgm', 0), '{:d}')
    if 'seed_dgm' in row: m(f'tr{key}seed', pts(row['seed_dgm']['acc']))
    if 'seed_strong' in row: m(f'tr{key}strong', pts(row['seed_strong']['acc']))
    for ag, w in (('A3best', 'three'), ('A1best', 'one')):
        if ag + '_gain' in row:
            m(f'tr{key}{w}', pts(row[ag + '_gain'][0]), '{:+.1f}'); m(f'tr{key}{w}lo', pts(row[ag + '_gain'][1]), '{:+.1f}'); m(f'tr{key}{w}hi', pts(row[ag + '_gain'][2]), '{:+.1f}')
out['transfer'] = tr
ratios = [v['A3best_cost_ratio'] for k, v in tr.items() if 'A3best_cost_ratio' in v]
ratios.append(loops['LoopC']['usd'] / (sk['seed_dgm']['1']['usd_per_task'])) if 'LoopC' in loops and 'usd' in loops['LoopC'] else None
if ratios: m('costRatioRange', f"{min(ratios):.0f} to {max(ratios):.0f}")
nz = sum(1 for k, v in tr.items() if 'A1best_gain' in v and v['A1best_gain'][1] <= 0)
m('aOneZeroCount', nz, '{:d}')

# ---------- retrospective ----------
rt = json.load(open(os.path.join(SHI, 'results', 'retro.json'))); out['retro'] = rt
m('retroSweSel', pts(rt['dgm_swe']['best_sel'])); m('retroSweOther', pts(rt['dgm_swe']['best_other']))
m('retroPolySel', pts(rt['dgm_polyglot']['sel_gain']), '{:.0f}'); m('retroPolyHeld', pts(rt['dgm_polyglot']['heldout_gain']), '{:.0f}')
ad = {x['domain']: x for x in rt['adas']}
for dom, key in (('mgsm', 'Mgsm'), ('drop', 'Drop'), ('mmlu', 'Mmlu'), ('gpqa', 'Gpqa'), ('arc', 'Arc')):
    m(f'adas{key}rho', ad[dom]['spearman_val_test'], '{:.2f}'); m(f'adas{key}infl', ad[dom]['inflation'], '{:.1f}')
import re as _re
def _adas_rows(dom):
    d = json.load(open(os.path.join(SHI, 'ext', 'adas', dom + '_gpt3.5_results.json')))
    def pm(x):
        mm = _re.search(r'Median: ([-\d.]+)%', x or ''); return float(mm.group(1)) if mm else None
    return [(e['generation'], pm(e.get('fitness')), pm(e.get('test_fitness'))) for e in d if pm(e.get('fitness')) is not None and pm(e.get('test_fitness')) is not None]
for dom, key in (('mmlu', 'Mmlu'), ('gpqa', 'Gpqa')):
    base = [r for r in _adas_rows(dom) if r[0] == 'initial']
    bb = max(base, key=lambda r: r[1])
    m(f'adas{key}baseShift', float(np.mean([r[1] - r[2] for r in base])), '{:+.1f}'); m(f'adas{key}bestBaseLoss', bb[1] - bb[2], '{:.1f}')
    m(f'adas{key}gainOverBestBase', ad[dom]['test_gain_vs_best_val_baseline'], '{:+.1f}')

# ---------- pre-registered hypotheses (tests with 95% bootstrap CIs, fresh set F where available) ----------
S_TASKS = SP['small'] + SP['medium']
def seed_S_pertask(strong):
    """per-task pass rate of the unchanged seed on S over all its runs (own evaluations + placebo copies)."""
    d = collections.defaultdict(list)
    for dd in glob.glob(os.path.join(SHI, 'exps', 'v2_*')):
        cfg = json.load(open(os.path.join(dd, 'config.json')))
        if ('strong' in cfg['seed_dir']) != strong: continue
        for ad in glob.glob(os.path.join(dd, 'agents', '*')):
            mp = os.path.join(ad, 'meta.json')
            if not os.path.exists(mp): continue
            mm = json.load(open(mp))
            if not (os.path.basename(ad) == 'initial' or (cfg['mode'] == 'placebo' and mm.get('compiled'))): continue
            ev = {**read_evals(ad, 'small').get(0, {}), **read_evals(ad, 'medium').get(0, {})}
            if all(t in ev for t in S_TASKS):
                for t in S_TASKS: d[t].append(float(ev[t]['passed']))
    return {t: float(np.mean(v)) for t, v in d.items()}
seedS = {False: seed_S_pertask(False), True: seed_S_pertask(True)}
def agent_S_vec(exp, aid):
    ad = os.path.join(SHI, 'exps', exp, 'agents', aid)
    ev = {**read_evals(ad, 'small').get(0, {}), **read_evals(ad, 'medium').get(0, {})}
    return np.array([float(ev[t]['passed']) for t in S_TASKS]) if all(t in ev for t in S_TASKS) else None
def boot_diff_ci(gS, gF, B=4000, q=(2.5, 97.5)):
    a = gS[rng.integers(0, len(gS), (B, len(gS)))].mean(1); b = gF[rng.integers(0, len(gF), (B, len(gF)))].mean(1)
    d = a - b; return float(gS.mean() - gF.mean()), float(np.percentile(d, q[0])), float(np.percentile(d, q[1]))
H = {}
# H1: placebo best above the seed mean and inside the 95% predictive interval of the maximum, leave-one-loop-out
h1 = []
pl_runs = {}
for x in pl:
    cfg_, st_, recs_ = collect(x['exp'])
    pl_runs[x['exp']] = [r['sel'] for r in recs_ if r['sel_full'] and r['compiled']]
for x in pl:
    others = [v for e2, vv in pl_runs.items() if e2 != x['exp'] for v in vv] + [SD['mean']]
    mu, sd = float(np.mean(others)), float(np.std(others, ddof=1))
    sims = (mu + sd * rng.standard_normal((20000, x['n_full']))).max(1)
    lo, hi = np.percentile(sims, 2.5), np.percentile(sims, 97.5)
    h1.append(dict(exp=x['exp'], best=x['best_S'], mu_loo=mu, sd_loo=sd, pi=[float(lo), float(hi)], inside=bool(lo <= x['best_S'] <= hi),
                   above_mean=bool(x['best_S'] > mu)))
H['H1'] = dict(runs=h1, verdict='supported' if all(r['inside'] and r['above_mean'] for r in h1) else 'not supported')
# H2: inflation = S gain - F gain > 0 (CI) and F gain > 0 (CI), per DGM loop
h2 = []
for key in ('LoopA', 'LoopB', 'LoopC'):
    if key not in loops: continue
    e, aid = loops[key]['exp'], loops[key]['aid']
    vS = agent_S_vec(e, aid); vF, _ = fresh_vec(e, aid, F) if fresh_vec(e, aid, F)[0] is not None else fresh_vec(e, aid, F1)
    tasksF = F if fresh_vec(e, aid, F)[0] is not None else F1
    gS = vS - np.array([seedS[False][t] for t in S_TASKS]); gF = vF - np.array([ref['seed_dgm'][t] for t in tasksF])
    inf = boot_diff_ci(gS, gF); fg_ = boot(gF)
    h2.append(dict(loop=key, inflation=inf, fresh=fg_, set='F' if tasksF is F else 'F1'))
n_inf = sum(1 for r in h2 if r['inflation'][1] > 0); n_f = sum(1 for r in h2 if r['fresh'][1] > 0)
H['H2'] = dict(loops=h2, verdict='supported' if (n_inf == len(h2) and n_f == len(h2)) else ('partially supported' if n_inf > 0 and n_f == len(h2) else 'not supported'))
# H3: best log-free single edit reaches 80% of the loops' mean fresh gain
L5 = float(np.mean([loops[k]['F1_gain'][0] for k in ('LoopA', 'LoopB', 'LoopC') if k in loops])) if h2 else None  # F1 for every loop: the single edits were evaluated on F1 only
L2 = lad['Cone'].get('best_gain', [None])[0]
H['H3'] = dict(L2=L2, L5=L5, ratio=(L2 / L5 if (L2 is not None and L5) else None),
               verdict='supported' if (L2 is not None and L5 is not None and L2 >= 0.8 * L5) else 'not supported')
# H4: strong-seed loops: equivalence of fresh gain to 0 within +-3 points (90% CI inside), selection gain > 0
h4 = []
for key in ('StrongA', 'StrongB'):
    if key not in loops: continue
    e, aid = loops[key]['exp'], loops[key]['aid']
    vF, _ = fresh_vec(e, aid, F)
    if vF is None: continue
    gF = vF - np.array([ref['seed_strong'][t] for t in F]); bsF = gF[rng.integers(0, len(gF), (4000, len(gF)))].mean(1)
    h4.append(dict(loop=key, fresh=float(gF.mean()), ci90=[float(np.percentile(bsF, 5)), float(np.percentile(bsF, 95))], S_gain=loops[key]['S_gain']))
equiv = all(-0.03 <= r['ci90'][0] and r['ci90'][1] <= 0.03 for r in h4) and all(r['S_gain'] > 0 for r in h4)
H['H4'] = dict(loops=h4, verdict='supported' if equiv else ('not supported' if all(r['ci90'][0] > 0.03 for r in h4) else 'not established'))
# H5: gain of the loop-3 agent shrinks under Haiku 4.5 and Sonnet 4.6 vs the search model (paired difference of gains, F1)
def model_task_pass(tag, agent):
    d = TR.load(tag); return {t: float(np.mean(v)) for t, v in d.get(agent, {}).items()} if d else {}
h5 = {}
vC, _ = fresh_vec('v2_A_dgm_s3', loops.get('LoopC', {}).get('aid', 'none'), F1) if 'LoopC' in loops else (None, None)
if vC is not None:
    gHaiku55 = vC - np.array([ref['seed_dgm'][t] for t in F1])
    for mdl in ('claude-haiku-4-5', 'claude-sonnet-4-6'):
        a = model_task_pass(f'X_{mdl}', 'A3best'); b = model_task_pass(f'X_{mdl}', 'seed_dgm')
        if all(t in a and t in b for t in F1):
            g = np.array([a[t] - b[t] for t in F1]); h5[mdl] = boot(g - gHaiku55)
H['H5'] = dict(diff_vs_search_model=h5, verdict='supported' if h5 and all(v[2] < 0 for v in h5.values()) else 'not established')
out['hypotheses'] = H
for h, v in H.items(): m('verdict' + {'1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five'}[h[1]], v['verdict'])
m('hTwoInfl', '; '.join(f"{100 * r['inflation'][0]:.1f} [{100 * r['inflation'][1]:+.1f}, {100 * r['inflation'][2]:+.1f}]" for r in h2))
m('hFourCI', '; '.join(f"{100 * r['fresh']:+.1f} [90\\% CI {100 * r['ci90'][0]:+.1f}, {100 * r['ci90'][1]:+.1f}]" for r in h4))
if h5: m('hFiveDiff', '; '.join(f"{ {'claude-haiku-4-5': 'Haiku 4.5', 'claude-sonnet-4-6': 'Sonnet 4.6'}[k]} {100 * v[0]:+.1f} [{100 * v[1]:+.1f}, {100 * v[2]:+.1f}]" for k, v in h5.items()))
m('placeboGainRange', f"{100 * min(x['best_S'] - SD['mean'] for x in pl):.1f} to {100 * max(x['best_S'] - SD['mean'] for x in pl):.1f}")
# pre-registered ladder contrasts (point estimates; F1)
L1 = lad['Cone'].get('mean'); L3 = lad['Ctwo'].get('mean'); L4 = lad['Ctwo'].get('best_gain', [None])[0]
L5F1 = float(np.mean([loops[k]['F1_gain'][0] for k in ('LoopA', 'LoopB', 'LoopC') if k in loops]))
out['ladder_contrasts'] = dict(L1=L1, L2_minus_L1=(L2 - L1) if None not in (L1, L2) else None, L4_minus_L2=(L4 - L2) if None not in (L2, L4) else None,
                              L5_minus_L4=(L5F1 - L4) if L4 is not None else None)
_cn = {'L1': 'conLone', 'L2_minus_L1': 'conLtwoMinusLone', 'L4_minus_L2': 'conLfourMinusLtwo', 'L5_minus_L4': 'conLfiveMinusLfour'}
for k, v in out['ladder_contrasts'].items():
    if v is not None: m(_cn[k], pts(v), '{:+.1f}')
# seed failure profile on F (empty solution share)
runs = [r for v in seed_runs('seed_dgm').values() for r in v if r['task'] in F]
emp = sum(bool(r.get('empty')) for r in runs); fails = sum(not r['passed'] for r in runs)
m('seedEmptyShare', 100 * emp / len(runs), '{:.0f}'); m('seedEmptyOfFail', 100 * emp / max(1, fails), '{:.0f}')
# pilot-leakage sensitivity: F problems that were in the pilot that preceded the engineered seed
pilot = set(json.load(open(os.path.join(SHI, 'data/lcb/splits_v1.json')))['pilot'])
Fnp = [t for t in F if t not in pilot]
d_all = np.array([ref['seed_strong'][t] - ref['seed_dgm'][t] for t in F]); d_np = np.array([ref['seed_strong'][t] - ref['seed_dgm'][t] for t in Fnp])
out['pilot_leak'] = dict(n_pilot_in_F=len(F) - len(Fnp), strong_minus_dgm_all=boot(d_all), strong_minus_dgm_nonpilot=boot(d_np))
m('pilotInF', len(F) - len(Fnp), '{:d}'); m('strongMinusDgmAll', pts(d_all.mean())); m('strongMinusDgmNP', pts(d_np.mean()))
# improver swap (exploratory): same diagnoses implemented on the seed's code by the seed vs by loop 3's best agent
if os.path.exists(os.path.join(SHI, 'exps', 'v2_R_swap', 'agents')):
    cfg_, st_, recs_ = collect('v2_R_swap'); sw = {}; parts = []
    def agents_word(n): return 'one working agent' if n == 1 else f'{n} working agents'
    for arm, who in (('seedEd', 'The seed agent'), ('evoEd', 'Loop 3\'s best agent')):
        rs = [r for r in recs_ if r['aid'].startswith(arm)]
        metas = {r['aid']: json.load(open(os.path.join(SHI, 'exps', 'v2_R_swap', 'agents', r['aid'], 'meta.json'))) for r in rs}
        done = [r for r in rs if metas[r['aid']].get('done')]
        empty = [r for r in done if metas[r['aid']].get('failed') == 'empty_model_patch']
        working = [r for r in done if r['compiled']]
        broken = [r for r in done if not r['compiled'] and r not in empty]
        gains = []
        for r in working:
            v, u = fresh_vec('v2_R_swap', r['aid'], F1)
            if v is not None: gains.append(float(np.mean(v - np.array([ref['seed_dgm'][t] for t in F1]))))
        Sm = float(np.mean([r['sel'] for r in working if r['sel_full']])) if any(r['sel_full'] for r in working) else None
        sw[arm] = dict(n=len(rs), done=len(done), empty=len(empty), broken=len(broken), working=len(working), S_mean=Sm,
                       F1_gain_mean=float(np.mean(gains)) if gains else None, n_F1=len(gains))
        t = f"{who} returned no edit for {len(empty)} of the {len(rs)} diagnoses" if empty else (f"{who} returned an edit for every diagnosis" if len(done) == len(rs) else f"{who} returned an edit in each of its {len(done)} finished attempts")
        t += f"; {len(broken)} of its edits left an agent that wrote no solution" if broken else ''
        t += f", and {agents_word(len(working))} remained" + (f" (mean selection score {100 * Sm:.1f}\\%" if Sm is not None else '')
        if gains: t += f"; mean fresh gain {100 * np.mean(gains):+.1f} points over {len(gains)} with fresh results)"
        elif Sm is not None: t += '; no fresh results yet)'
        if len(done) < len(rs): t += f"; {len(rs) - len(done)} attempts were still running"
        parts.append(t + '.')
    out['swap'] = sw
    m('swapText', ' '.join(parts))
    ev_lines = {'working': [], 'broken': []}
    for r in recs_:
        if not r['aid'].startswith('evoEd'): continue
        mm = json.load(open(os.path.join(SHI, 'exps', 'v2_R_swap', 'agents', r['aid'], 'meta.json')))
        if not mm.get('done') or mm.get('failed'): continue
        ev_lines['working' if r['compiled'] else 'broken'].append(mm.get('patch_lines', 0))
    out['swap_patch_lines'] = ev_lines
    if ev_lines['working'] and ev_lines['broken']:
        m('swapLinesText', f"broken edits changed {min(ev_lines['broken'])}--{max(ev_lines['broken'])} lines, working ones {min(ev_lines['working'])}--{max(ev_lines['working'])}")
# shared-value phrasing for prose (state a shared value once)
if 'NohintA' in loops and 'NohintB' in loops and 'F1_gain' in loops['NohintA'] and 'F1_gain' in loops['NohintB']:
    m('nohintPairText', pair_text([pts(loops['NohintA']['F1_gain'][0]), pts(loops['NohintB']['F1_gain'][0])], '+{:.1f}', ' points'))
if all(k in loops and 'F_gain' in loops[k] for k in ('StrongA', 'StrongB')):
    m('strongFPairText', pair_text([pts(loops['StrongA']['F_gain'][0]), pts(loops['StrongB']['F_gain'][0])], '{:.1f}', ' points', ' each'))
if 'quirk' in out and all(e in out['quirk'] for e in ('E_strong_dgm_s1', 'E_strong_dgm_s2')):
    q = out['quirk']
    m('quirkStrongCorrText', pair_text([pts(q['E_strong_dgm_s1']['corrected_gain']), pts(q['E_strong_dgm_s2']['corrected_gain'])], '+{:.0f}', ' points', ' each'))
    m('quirkStrongMeasText', pair_text([pts(q['E_strong_dgm_s1']['measured_gain']), pts(q['E_strong_dgm_s2']['measured_gain'])], '+{:.0f}', ' points', ' each'))
json.dump(out, open(os.path.join(SHI, 'results', 'summary.json'), 'w'), indent=1, default=float)
os.makedirs(os.path.join(SHI, 'paper'), exist_ok=True)
names = {'1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five'}
with open(os.path.join(SHI, 'paper', 'numbers.tex'), 'w') as f:
    for k, v in sorted(mac.items()):
        k2 = re.sub(r'\d', lambda mm: names[mm.group(0)], k)
        f.write(f'\\newcommand{{\\n{k2}}}{{{v}}}\n')
print(json.dumps({k: mac[k] for k in sorted(mac)}, indent=0))

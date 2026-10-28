"""PREREG_v3 E1: SWE-bench at equal output budget. Reads flagship/runs_r3/r3_<agent>/results.jsonl (dgm_init_16k,
dgm_best_16k, moves; one batch, 65 fresh tasks of flagship/swe/r3_fresh65.json), overridden by regrade.json where an
evaluation was graded again, and optionally flagship/runs_r3/sensitivity/sens_results.jsonl (patches present at an
early ending graded as if kept). Exploratory cross-batch references: v2 runs of the same tasks
(flagship/runs_full/final_report_runs.tsv). Writes results/r3_swe.json (unrounded).
H11: moves >= dgm_best_16k - 3 (non-inferiority); H12: dgm_best_16k - dgm_init_16k (two-sided); H13: moves - dgm_init_16k."""
import csv, datetime as dt, glob, json, math, os, re
import numpy as np
SHI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(SHI, 'flagship'); R = os.path.join(F, 'runs_r3')
TASKS = json.load(open(os.path.join(F, 'swe', 'r3_fresh65.json')))
AG = ['dgm_init_16k', 'dgm_best_16k', 'moves']

def load(a):
    d = os.path.join(R, f'r3_{a}')
    res = {}
    for l in open(os.path.join(d, 'results.jsonl')):
        r = json.loads(l); res[r['instance_id']] = r
    rg = json.load(open(os.path.join(d, 'regrade.json'))) if os.path.exists(os.path.join(d, 'regrade.json')) else {}
    for iid, v in rg.get('regraded', {}).items():
        if iid in res and v.get('after') is not None: res[iid]['resolved'] = v['after']
    return res

def code(r):
    if r.get('failed_step') != 'agent': return None
    m = re.search(r'exit code (-?\d+)', r.get('harness_error') or '')
    return m.group(1) if m else 'other'

def boot(x, y, B=10000, seed=0):
    d = np.array(x, float) - np.array(y, float); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(1))
    b = int(sum(1 for a, c in zip(x, y) if a and not c)); c_ = int(sum(1 for a, c in zip(x, y) if c and not a))
    n = b + c_; p = min(1.0, 2 * sum(math.comb(n, k) for k in range(0, min(b, c_) + 1)) / 2 ** n) if n else 1.0
    return {'diff': 100 * float(d.mean()), 'lo': 100 * float(ms[int(.025 * B)]), 'hi': 100 * float(ms[int(.975 * B) - 1]),
            'n': len(d), 'x_only': b, 'y_only': c_, 'mcnemar_p': p}

runs = {a: load(a) for a in AG}
T = [t for t in TASKS if all(t in runs[a] for a in AG)]
out = {'n_tasks': len(T), 'agents': {}, 'contrasts': {}}
res = {a: [bool(runs[a][t]['resolved']) for t in T] for a in AG}
for a in AG:
    rs = [runs[a][t] for t in T]; codes = {}
    for r in rs:
        c = code(r)
        if c: codes[c] = codes.get(c, 0) + 1
    out['agents'][a] = {'resolved': sum(res[a]), 'rate': 100 * sum(res[a]) / len(T),
                        'early': sum(1 for r in rs if r.get('failed_step') == 'agent'), 'early_codes': codes,
                        'budget_hits': sum(1 for r in rs if r.get('budget_hit')),
                        'usd_mean': float(np.mean([r['usd'] for r in rs])), 'usd_total': float(sum(r['usd'] for r in rs)),
                        'wall_median_min': float(np.median([r['wall_s'] for r in rs])) / 60}
out['contrasts']['H11_moves_minus_best16k'] = boot(res['moves'], res['dgm_best_16k'])
out['contrasts']['H12_best16k_minus_init16k'] = boot(res['dgm_best_16k'], res['dgm_init_16k'])
out['contrasts']['H13_moves_minus_init16k'] = boot(res['moves'], res['dgm_init_16k'])
out['H11_noninferior'] = out['contrasts']['H11_moves_minus_best16k']['lo'] > -3
out['H11_superior'] = out['contrasts']['H11_moves_minus_best16k']['lo'] > 0
c12 = out['contrasts']['H12_best16k_minus_init16k']; out['H12_significant'] = c12['lo'] > 0 or c12['hi'] < 0
# sensitivity: early-ended patches kept
sp = os.path.join(R, 'sensitivity', 'sens_results.jsonl')
if os.path.exists(sp):
    kept = {a: dict(zip(T, res[a])) for a in AG}
    for l in open(sp):
        r = json.loads(l)
        if r.get('agent') in kept and r.get('instance_id') in kept[r['agent']] and r.get('resolved'):
            kept[r['agent']][r['instance_id']] = True
    rk = {a: [kept[a][t] for t in T] for a in AG}
    out['sensitivity'] = {'rates': {a: 100 * sum(rk[a]) / len(T) for a in AG},
                          'H11': boot(rk['moves'], rk['dgm_best_16k']), 'H12': boot(rk['dgm_best_16k'], rk['dgm_init_16k']),
                          'H13': boot(rk['moves'], rk['dgm_init_16k'])}
# exploratory cross-batch references: v2 runs (4,096-token agents and moves) on the same tasks
v2 = {}
tsv = os.path.join(F, 'runs_full', 'final_report_runs.tsv')
if os.path.exists(tsv):
    v2e = {}
    for r in csv.DictReader(open(tsv), delimiter='\t'):
        v2.setdefault(r['agent'], {})[r['instance_id']] = r['resolved'] == 'True'
        v2e.setdefault(r['agent'], {})[r['instance_id']] = r['early'] == 'True'
    T2 = [t for t in T if all(t in v2.get(a, {}) for a in ('dgm_init', 'dgm_best', 'moves'))]
    def sel(a, src): return [src[a][t] for t in T2]
    r3m = {a: dict(zip(T, res[a])) for a in AG}
    out['cross_batch'] = {'n_tasks': len(T2),
                          'v2_rates_same_tasks': {a: 100 * sum(sel(a, v2)) / len(T2) for a in ('dgm_init', 'dgm_best', 'moves')},
                          'v2_early_same_tasks': {a: sum(sel(a, v2e)) for a in ('dgm_init', 'dgm_best', 'moves')},
                          'best_early_both_rounds': sum(1 for t in T2 if v2e['dgm_best'][t] and runs['dgm_best_16k'][t].get('failed_step') == 'agent'),
                          'best16k_minus_v2best': boot([r3m['dgm_best_16k'][t] for t in T2], sel('dgm_best', v2)),
                          'init16k_minus_v2init': boot([r3m['dgm_init_16k'][t] for t in T2], sel('dgm_init', v2)),
                          'moves_r3_minus_moves_v2': boot([r3m['moves'][t] for t in T2], sel('moves', v2))}
# kernel OOM kills (runs_r3/oom.log): runs in progress at each kill, and early endings within 10 minutes after it
oomp = os.path.join(R, 'oom.log')
if os.path.exists(oomp):
    kills = sorted({dt.datetime.fromisoformat(l.split()[0]) for l in open(oomp) if 'Killed process' in l})
    st = []
    for a in AG:
        for p in glob.glob(os.path.join(R, f'r3_{a}', 'status', '*.a3.json')):
            s = json.load(open(p)); t0 = dt.datetime.fromisoformat(s['t0_utc'])
            st.append((a, s['instance_id'], t0, t0 + dt.timedelta(seconds=s['wall_s']), s.get('failed_step') == 'agent'))
    out['oom'] = {'kills': [k.isoformat() for k in kills], 'n_status': len(st),
                  'in_progress': [[[a, i, t1.isoformat(), e] for a, i, t0, t1, e in st if t0 <= k <= t1] for k in kills],
                  'early_within_10min': [[[a, i, t1.isoformat()] for a, i, t0, t1, e in st if e and 0 <= (t1 - k).total_seconds() <= 600]
                                         for k in kills]}
json.dump(out, open(os.path.join(SHI, 'results', 'r3_swe.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('agents',)}, indent=1)[:2500])
for a, v in out['agents'].items(): print(a, {k: (round(x, 2) if isinstance(x, float) else x) for k, x in v.items()})

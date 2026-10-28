"""Full-run final report (on the SWE-bench machine): per agent and subset resolved counts (driver grading, overridden by re-grades),
cost, early endings (exit codes), budget hits, per-run mean machine load over the run's wall-clock window, and early-ending /
resolve rates by load tertile per agent. Writes runs_full/final_report.json, final_report_runs.tsv, final_report.txt.
Load source: runs_full/loadlog.tsv (60 s samples from 2026-10-24T08:54:28Z); runs that ended before that use a linear
interpolation of the sparse load readings taken at the 30-min checks (marked 'approx'); none at all -> 'not_sampled'."""
import bisect, datetime as dt, json, os, re, statistics as st
F = os.path.expanduser('~/shi_eval/flagship'); R = f'{F}/runs_full'
import sys
AGENTS = sys.argv[1:] or ['dgm_init', 'dgm_best', 'moves', 'moves_retry']
SUB = {i: 'fresh' for i in json.load(open(f'{F}/swe/fresh_gold.json'))}
SUB.update({i: 'dgm60' for i in json.load(open(f'{F}/swe/dgm60_gold.json'))})
P = lambda s: dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
SPARSE = [('2026-10-24T06:41:03Z', 107.68), ('2026-10-24T06:41:57Z', 89.19), ('2026-10-24T06:52:40Z', 5.55),
          ('2026-10-24T07:22:49Z', 75.06), ('2026-10-24T07:52:53Z', 98.67), ('2026-10-24T08:22:51Z', 126.53),
          ('2026-10-24T08:52:56Z', 144.32)]           # load1 at the 30-min checks before the sampler started
SP = [(P(t).timestamp(), v) for t, v in SPARSE]
LT, LV = [], []
for line in open(f'{R}/loadlog.tsv'):
    if line.startswith('utc'): continue
    t, l1, *_ = line.split('\t'); LT.append(P(t).timestamp()); LV.append(float(l1))
def interp(x):
    if x <= SP[0][0]: return SP[0][1]
    for (a, va), (b, vb) in zip(SP, SP[1:]):
        if a <= x <= b: return va + (vb - va) * (x - a) / (b - a)
    return SP[-1][1]
def mean_load(t0, t1):
    i, j = bisect.bisect_left(LT, t0), bisect.bisect_right(LT, t1)
    if j > i: return round(st.mean(LV[i:j]), 1), 'sampled' if t0 >= LT[0] else 'partly_sampled'
    if t1 < (LT[0] if LT else 0) and t0 >= SP[0][0] - 600:
        xs = [t0 + k * (t1 - t0) / 10 for k in range(11)]; return round(st.mean(interp(x) for x in xs), 1), 'approx'
    return None, 'not_sampled'
rows, rep = [], {'agents': {}, 'regrades': {}}
for A in AGENTS:
    d = f'{R}/flag_{A}_s45'; res = {json.loads(l)['instance_id']: json.loads(l) for l in open(f'{d}/results.jsonl')}
    rg = json.load(open(f'{d}/regrade.json')) if os.path.exists(f'{d}/regrade.json') else {'regraded': {}}
    rep['regrades'][A] = {i: v for i, v in rg.get('regraded', {}).items()}
    for iid, r in res.items():
        resolved = r['resolved']
        if iid in rg.get('regraded', {}) and rg['regraded'][iid].get('after') is not None: resolved = rg['regraded'][iid]['after']
        stp = None; sf = f'{d}/status/{iid}.a0.json'
        if os.path.exists(sf): stp = json.load(open(sf))
        t0 = P(stp['t0_utc']).timestamp() if stp and stp.get('t0_utc') else None
        load, src = mean_load(t0, t0 + (stp['wall_s'] or 0)) if t0 else (None, 'not_sampled')
        code = (re.search(r'exit code (-?\d+)', r.get('harness_error') or '') or [None, None])[1] if r.get('failed_step') == 'agent' else None
        rows.append(dict(agent=A, instance_id=iid, subset=SUB.get(iid, '?'), resolved=bool(resolved), usd=r['usd'],
                         early=r.get('failed_step') == 'agent', exit_code=code, budget_hit=r.get('budget_hit'),
                         calls=r.get('calls'), wall_s=r.get('wall_s'), t0=stp and stp.get('t0_utc'), mean_load=load, load_src=src))
for A in AGENTS:
    rs = [r for r in rows if r['agent'] == A]; usd = [r['usd'] for r in rs]
    codes = {}
    for r in rs:
        if r['early']: codes[r['exit_code'] or 'other'] = codes.get(r['exit_code'] or 'other', 0) + 1
    by_sub = {s: f"{sum(r['resolved'] for r in rs if r['subset'] == s)}/{sum(1 for r in rs if r['subset'] == s)}" for s in ('fresh', 'dgm60')}
    ld = sorted(r['mean_load'] for r in rs if r['mean_load'] is not None)
    terc = {}
    if len(ld) >= 3:
        c1, c2 = ld[len(ld) // 3], ld[2 * len(ld) // 3]
        for name, lo, hi in (('low', -1, c1), ('mid', c1, c2), ('high', c2, 1e9)):
            g = [r for r in rs if r['mean_load'] is not None and (lo < r['mean_load'] <= hi if name != 'low' else r['mean_load'] <= hi)]
            terc[name] = dict(load_range=[lo if lo >= 0 else ld[0], hi if hi < 1e9 else ld[-1]], n=len(g),
                              early_rate=round(sum(r['early'] for r in g) / max(len(g), 1), 3),
                              resolve_rate=round(sum(r['resolved'] for r in g) / max(len(g), 1), 3))
    rep['agents'][A] = dict(n=len(rs), resolved=sum(r['resolved'] for r in rs), resolved_by_subset=by_sub,
                            usd_total=round(sum(usd), 2), usd_mean=round(st.mean(usd), 3), usd_median=round(st.median(usd), 3),
                            early=sum(r['early'] for r in rs), early_codes=codes, budget_hits=sum(bool(r['budget_hit']) for r in rs),
                            load_sources={s: sum(1 for r in rs if r['load_src'] == s) for s in ('sampled', 'partly_sampled', 'approx', 'not_sampled')},
                            load_tertiles=terc)
json.dump(rep, open(f'{R}/final_report.json', 'w'), indent=1)
cols = ['agent', 'instance_id', 'subset', 'resolved', 'usd', 'early', 'exit_code', 'budget_hit', 'calls', 'wall_s', 't0', 'mean_load', 'load_src']
with open(f'{R}/final_report_runs.tsv', 'w') as f:
    f.write('\t'.join(cols) + '\n')
    for r in rows: f.write('\t'.join(str(r[c]) for c in cols) + '\n')
with open(f'{R}/final_report.txt', 'w') as f:
    for A, a in rep['agents'].items():
        f.write(f"{A}: resolved {a['resolved']}/{a['n']} (fresh {a['resolved_by_subset']['fresh']}, dgm60 {a['resolved_by_subset']['dgm60']}); "
                f"${a['usd_total']} total, ${a['usd_mean']} mean, ${a['usd_median']} median; early {a['early']} {a['early_codes']}; "
                f"budget hits {a['budget_hits']}; load src {a['load_sources']}\n")
        for k, v in a['load_tertiles'].items(): f.write(f"   load {k} {v['load_range']}: n={v['n']} early={v['early_rate']} resolved={v['resolve_rate']}\n")
    f.write(f"regrades: {json.dumps(rep['regrades'])}\n")
print(open(f'{R}/final_report.txt').read())

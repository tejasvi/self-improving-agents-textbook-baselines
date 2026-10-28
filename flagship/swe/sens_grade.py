"""Sensitivity analysis (decision 2026-10-25, added during internal review): grade the patch each early-ended run (failed_step == 'agent')
had in the repository when it ended -- diag/<iid>_current_patch.diff from the harness's diagnostics copy-out; missing or
empty = no patch -- as if the harness had kept it. DGM's own preds_to_jsonl filter (drops test-file hunks), then the
official swebench run_evaluation with the driver's dataset and settings, run_id sens_<agent>, <= 16 workers, inside
runs_full/sensitivity/sens_<agent>/ (the original results are not touched). Predictions without a report are re-graded
alone with <= 4 workers (run_id sens_<agent>_regrade), as in the main run.
Usage (on the SWE-bench machine): $PY -I sens_grade.py [WORKERS]  -> runs_full/sensitivity/{sens_results.jsonl, sens_summary.json}"""
import glob, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
F = os.path.expanduser('~/shi_eval/flagship'); R = f'{F}/runs_full'; OUT = f'{R}/sensitivity'
sys.path.insert(0, os.path.join(F, 'dgm_repo'))
from swe_bench.report import preds_to_jsonl
AGENTS = ['dgm_init', 'dgm_best', 'moves', 'moves_retry']
DATASET = 'princeton-nlp/SWE-bench_Verified'
workers = sys.argv[1] if len(sys.argv) > 1 else '16'
SUB = {i: 'fresh' for i in json.load(open(f'{F}/swe/fresh_gold.json'))}
SUB.update({i: 'dgm60' for i in json.load(open(f'{F}/swe/dgm60_gold.json'))})

def evaluate(od, jsonl, run_id, n_workers):
    with open(os.path.join(od, 'eval.log'), 'a') as lf:
        return subprocess.run([sys.executable, '-I', '-m', 'swebench.harness.run_evaluation', '--dataset_name', DATASET,
                               '--predictions_path', jsonl, '--max_workers', str(n_workers), '--run_id', run_id],
                              cwd=od, stdout=lf, stderr=subprocess.STDOUT).returncode

def report(od, run_id, iid):
    rp = os.path.join(od, 'logs', 'run_evaluation', run_id, f'sens_{A}', iid, 'report.json')
    return bool(json.load(open(rp))[iid].get('resolved')) if os.path.exists(rp) else None

rows, summ = [], {}
for A in AGENTS:
    tag = f'flag_{A}_s45'; d = f'{R}/{tag}'; diag = f'{d}/predictions/{tag}_0/diag'
    res = {json.loads(l)['instance_id']: json.loads(l) for l in open(f'{d}/results.jsonl')}
    early = sorted(i for i, r in res.items() if r.get('failed_step') == 'agent')
    od = f'{OUT}/sens_{A}'; os.makedirs(od, exist_ok=True)
    preds, prior = {}, {}
    for iid in early:
        p = f'{diag}/{iid}_current_patch.diff'
        preds[iid] = {'instance_id': iid, 'model_name_or_path': f'sens_{A}',
                      'model_patch': open(p, errors='replace').read() if os.path.exists(p) else ''}
        if A == 'dgm_best':      # an earlier attempt logged a passing regression-test score (agent's own "Test score: 1.0")
            txt = ''.join(open(c, errors='replace').read() for c in [f'{diag}/{iid}.md'] + glob.glob(f'{diag}/{iid}_*.md')
                          if os.path.exists(c))
            prior[iid] = None if not txt.strip() else bool(re.search(r'Test score: 1(?:\.0+)?(?![\d.])', txt))
    jsonl = preds_to_jsonl(od, preds) if preds else None                  # DGM's filter: drops test-file hunks
    filt = {json.loads(l)['instance_id']: json.loads(l)['model_patch'] for l in open(jsonl)} if jsonl else {}
    had = {i: bool((filt.get(i) or '').strip()) for i in early}
    rc = evaluate(od, jsonl, f'sens_{A}', workers) if any(had.values()) else None
    out = {i: report(od, f'sens_{A}', i) for i in early}
    missing = [i for i in early if had[i] and out[i] is None]
    rc2 = None
    if missing:                                                            # re-grade alone at low concurrency
        sub = os.path.join(od, 'regrade_preds.jsonl')
        with open(sub, 'w') as f:
            for i in missing: f.write(json.dumps({'instance_id': i, 'model_name_or_path': f'sens_{A}', 'model_patch': filt[i]}) + '\n')
        rc2 = evaluate(od, sub, f'sens_{A}_regrade', 4)
        for i in missing: out[i] = report(od, f'sens_{A}_regrade', i)
    for i in early:
        rows.append(dict(instance_id=i, agent=A, subset=SUB.get(i, '?'), had_patch=had[i], resolved=bool(out[i]),
                         graded=(out[i] is not None) if had[i] else None, prior_test_score_1=prior.get(i) if A == 'dgm_best' else None))
    orig = {s: sum(1 for i, r in res.items() if r['resolved'] and SUB.get(i) == s) for s in ('fresh', 'dgm60')}
    gain = {s: sum(1 for r in rows if r['agent'] == A and r['resolved'] and r['subset'] == s) for s in ('fresh', 'dgm60')}
    n_sub = {s: sum(1 for i in res if SUB.get(i) == s) for s in ('fresh', 'dgm60')}
    summ[A] = dict(original_resolved=sum(orig.values()), original_by_subset={s: f'{orig[s]}/{n_sub[s]}' for s in orig},
                   kept_resolved=sum(orig.values()) + sum(gain.values()),
                   kept_by_subset={s: f'{orig[s] + gain[s]}/{n_sub[s]}' for s in orig},
                   early_ended=len(early), early_with_nonempty_patch=sum(had.values()), early_resolved_if_kept=sum(gain.values()),
                   no_report_after_regrade=[i for i in early if had[i] and out[i] is None], eval_rc=rc, regrade_rc=rc2)
    if A == 'dgm_best':
        summ[A]['early_with_prior_test_score_1'] = sum(1 for i in early if prior[i])
        summ[A]['early_prior_score_unknown_no_chat'] = sum(1 for i in early if prior[i] is None)
    print(A, json.dumps(summ[A]), flush=True)
with open(f'{OUT}/sens_results.jsonl', 'w') as f:
    for r in rows: f.write(json.dumps(r) + '\n')
json.dump(summ, open(f'{OUT}/sens_summary.json', 'w'), indent=1)

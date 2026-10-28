"""Re-grade, alone and at low concurrency, every prediction whose official evaluation produced no report (timeout or
error), decision 2026-10-24. Usage (on the SWE-bench machine): $PY -I regrade.py RUNDIR [--workers 4] [--dry-run]
Reads RUNDIR/predictions/<tag>_0/all_preds.jsonl (DGM's filtered predictions, as graded by the driver) and the driver's
evaluation logs (run_id <tag>_0); re-runs swebench run_evaluation for the affected instances only with run_id
<tag>_0_regrade; writes RUNDIR/regrade.json (cause per instance, outcome before -> after)."""
import argparse, json, os, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument('rundir'); ap.add_argument('--workers', type=int, default=4)
ap.add_argument('--dry-run', action='store_true'); a = ap.parse_args()
rd = os.path.realpath(a.rundir); tag = os.path.basename(rd); rid = f'{tag}_0'
pf = os.path.join(rd, 'predictions', rid, 'all_preds.jsonl')   # absent when the run produced no prediction at all
preds = [json.loads(l) for l in open(pf)] if os.path.exists(pf) else []
def log_dir(run_id, iid): return os.path.join(rd, 'logs', 'run_evaluation', run_id, rid, iid)
todo, cause = [], {}
for p in preds:
    iid = p['instance_id']
    if not (p.get('model_patch') or '').strip(): continue                     # empty patch: not run by swebench, unresolved
    if os.path.exists(os.path.join(log_dir(rid, iid), 'report.json')): continue
    lg = os.path.join(log_dir(rid, iid), 'run_instance.log')
    txt = open(lg, errors='replace').read() if os.path.exists(lg) else ''
    cause[iid] = ('timeout' if 'timed out' in txt.lower() else 'patch_apply_failed' if 'Patch Apply Failed' in txt
                  else 'no_log' if not txt else 'error')
    todo.append(p)
print(f'{tag}: {len(todo)} predictions without a report: {cause}', flush=True)
out = {'tag': tag, 'candidates': cause, 'regraded': {}}
if todo and not a.dry_run:
    sub = os.path.join(rd, 'regrade_preds.jsonl')
    with open(sub, 'w') as f:
        for p in todo: f.write(json.dumps(p) + '\n')
    with open(os.path.join(rd, 'regrade.log'), 'a') as lf:
        rc = subprocess.run([sys.executable, '-I', '-m', 'swebench.harness.run_evaluation', '--dataset_name',
                             'princeton-nlp/SWE-bench_Verified', '--predictions_path', sub, '--max_workers', str(a.workers),
                             '--run_id', f'{rid}_regrade'], cwd=rd, stdout=lf, stderr=subprocess.STDOUT).returncode
    out['eval_rc'] = rc
    for p in todo:
        iid = p['instance_id']; rp = os.path.join(log_dir(f'{rid}_regrade', iid), 'report.json')
        new = json.load(open(rp))[iid].get('resolved') if os.path.exists(rp) else None
        lg = os.path.join(log_dir(f'{rid}_regrade', iid), 'run_instance.log')
        txt = open(lg, errors='replace').read() if os.path.exists(lg) else ''
        out['regraded'][iid] = {'cause': cause[iid], 'before': None, 'after': new,
                                'after_cause': None if new is not None else ('timeout' if 'timed out' in txt.lower()
                                               else 'patch_apply_failed' if 'Patch Apply Failed' in txt else 'error')}
    print(json.dumps(out['regraded']), flush=True)
json.dump(out, open(os.path.join(rd, 'regrade.json'), 'w'), indent=1)

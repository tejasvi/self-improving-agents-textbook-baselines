"""Gold validation ($0 model spend): run each instance's gold patch through the official swebench evaluation
(swebench 2.1.0 run_evaluation, fresh container per instance) and record which instances the gold patch resolves.
Instances it does not resolve are excluded for every agent (decision 2026-10-24).
Usage (on the SWE-bench machine): $PY -I gold_validate.py OUTDIR WORKERS IDS.json [IDS.json ...]  -> OUTDIR/gold_validation.json"""
import json, os, subprocess, sys, time, datetime
from datasets import load_dataset
out, workers, lists = os.path.realpath(sys.argv[1]), sys.argv[2], sys.argv[3:]
ids = []
for p in lists: ids += json.load(open(p))
assert len(set(ids)) == len(ids), 'duplicate ids'
os.makedirs(out, exist_ok=True)
ds = {e['instance_id']: e for e in load_dataset('princeton-nlp/SWE-bench_Verified')['test']}
model, run_id = 'gold', 'gold_validation'
preds = os.path.join(out, 'gold_preds.jsonl')
with open(preds, 'w') as f:
    for i in ids:
        f.write(json.dumps({'instance_id': i, 'model_name_or_path': model, 'model_patch': ds[i]['patch']}) + '\n')
t0 = time.time()
with open(os.path.join(out, 'eval.log'), 'a') as lf:
    rc = subprocess.run([sys.executable, '-I', '-m', 'swebench.harness.run_evaluation', '--dataset_name',
                         'princeton-nlp/SWE-bench_Verified', '--predictions_path', preds, '--max_workers', workers,
                         '--run_id', run_id], cwd=out, stdout=lf, stderr=subprocess.STDOUT).returncode
res = {}
for i in ids:
    rp = os.path.join(out, 'logs', 'run_evaluation', run_id, model, i, 'report.json')
    if not os.path.exists(rp):
        res[i] = {'resolved': None, 'note': 'no report (evaluation error)'}; continue
    r = json.load(open(rp))[i]; ts = r.get('tests_status', {})
    res[i] = {'resolved': bool(r.get('resolved')), 'patch_applied': r.get('patch_successfully_applied'),
              'f2p_fail': len(ts.get('FAIL_TO_PASS', {}).get('failure', [])), 'p2p_fail': len(ts.get('PASS_TO_PASS', {}).get('failure', []))}
summary = dict(n=len(ids), resolved=sum(1 for v in res.values() if v['resolved']),
               not_resolved=sorted(i for i, v in res.items() if v['resolved'] is False),
               no_report=sorted(i for i, v in res.items() if v['resolved'] is None),
               eval_rc=rc, wall_s=round(time.time() - t0), workers=int(workers),
               end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
json.dump(dict(summary=summary, instances=res), open(os.path.join(out, 'gold_validation.json'), 'w'), indent=1)
print(json.dumps(summary))

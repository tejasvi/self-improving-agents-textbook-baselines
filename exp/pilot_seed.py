"""Pilot: DGM seed harness on the 80 pilot tasks, 2 reps each (Haiku 5.5)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import batch
SHI = os.path.expanduser('~/shi_eval')
sp = json.load(open(os.path.join(SHI, 'data/lcb/splits_v1.json')))
jobs = []
for rep in range(2):
    for tid in sp['pilot']:
        jobs.append(dict(exp='pilot2', agent_dir=os.path.join(SHI, 'harness/seed_dgm'), agent_name='seed_dgm',
                         task_id=tid, rep=rep, outdir=os.path.join(SHI, f'runs/pilot2/seed_dgm/{tid}/r{rep}')))
batch.run_jobs(jobs, os.path.join(SHI, 'results/pilot2.jsonl'), workers=int(sys.argv[1]) if len(sys.argv) > 1 else 16)

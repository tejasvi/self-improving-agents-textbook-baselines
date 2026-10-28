"""Dev check of harnesses on hard tasks EXCLUDED from the study pool (private tests 20-60 MB)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import batch, lcb
SHI = os.path.expanduser('~/shi_eval')
I = lcb.index()
dev = sorted(t['id'] for t in I.values() if t['difficulty'] == 'hard' and 20e6 < t['private_bytes'] <= 60e6)[:int(sys.argv[2])]
agents = sys.argv[1].split(',')
jobs = []
for a in agents:
    for tid in dev:
        jobs.append(dict(exp='dev1', agent_dir=os.path.join(SHI, 'harness', a), agent_name=a, task_id=tid, rep=0,
                         outdir=os.path.join(SHI, f'runs/dev1/{a}/{tid}'), timeout=600))
print(len(dev), 'dev tasks')
batch.run_jobs(jobs, os.path.join(SHI, 'results/dev1.jsonl'), workers=20)

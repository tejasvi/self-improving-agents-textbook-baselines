"""Evaluate harness code dirs on a task split (fresh / S / F1) with reps and an optional model override.

usage: eval_agents.py TAG SPLIT REPS MODEL WORKERS name=path [name=path ...]
       SPLIT in {fresh, fresh1, sel} (sel = small+medium); MODEL e.g. claude-haiku-5-5
Results: results/<TAG>.jsonl (resume-safe). Agent run dirs are not kept (chat logs kept).
"""
import json, os, sys
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import batch
SHI = os.path.expanduser('~/shi_eval')

def tasks_for(split, splits_file='splits_hard_v1.json'):
    sp = json.load(open(os.path.join(SHI, 'data/lcb', splits_file)))
    if split == 'fresh': return sp['fresh']
    if split == 'fresh1': return sp['fresh'][:116]
    if split == 'fresh2': return sp['fresh'][116:]
    if split == 'sel': return sp['small'] + sp['medium']
    raise ValueError(split)

def main(tag, split, reps, model, workers, agents, timeout=600):
    T = tasks_for(split)
    jobs = []
    for rep in range(reps):
        for name, path in agents:
            for tid in T:
                jobs.append(dict(exp=tag, agent_dir=path, agent_name=name, task_id=tid, rep=rep, model=model, timeout=timeout,
                                 outdir=os.path.join(SHI, 'runs', tag, name.replace('/', '_'), f'{tid}_r{rep}')))
    print(f'{tag}: {len(agents)} agents x {len(T)} tasks x {reps} reps = {len(jobs)} jobs, model {model}', flush=True)
    budget = float(os.environ.get('EVAL_BUDGET', '0.25'))
    batch.run_jobs(jobs, os.path.join(SHI, 'results', f'{tag}.jsonl'), workers=workers, model=model, budget=budget, log_every=100)

if __name__ == '__main__':
    tag, split, reps, model, workers = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
    agents = [tuple(a.split('=', 1)) for a in sys.argv[6:]]
    main(tag, split, reps, model, workers, agents)

"""Like eval_agents.py, but jobs are ordered rep -> task -> agent, so partial results stay balanced across agents
(and drift hits all agents alike).

usage: eval_interleaved.py TAG SPLIT REPS MODEL WORKERS name=path [name=path ...]
"""
import json, os, random, sys
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
sys.path.insert(0, os.path.expanduser('~/shi_eval/exp'))
import batch
from eval_agents import tasks_for
SHI = os.path.expanduser('~/shi_eval')

def main(tag, split, reps, model, workers, agents, timeout=600):
    T = list(tasks_for(split))
    jobs = []
    for rep in range(reps):
        order = T[:]; random.Random(1000 + rep).shuffle(order)
        for tid in order:
            for name, path in agents:
                jobs.append(dict(exp=tag, agent_dir=path, agent_name=name, task_id=tid, rep=rep, model=model, timeout=timeout,
                                 outdir=os.path.join(SHI, 'runs', tag, name.replace('/', '_'), f'{tid}_r{rep}')))
    print(f'{tag}: {len(agents)} agents x {len(T)} tasks x {reps} reps = {len(jobs)} jobs, model {model}', flush=True)
    budget = float(os.environ.get('EVAL_BUDGET', '0.25'))
    batch.run_jobs(jobs, os.path.join(SHI, 'results', f'{tag}.jsonl'), workers=workers, model=model, budget=budget, log_every=100)

if __name__ == '__main__':
    tag, split, reps, model, workers = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
    agents = [tuple(a.split('=', 1)) for a in sys.argv[6:]]
    main(tag, split, reps, model, workers, agents)

"""Fresh-set evaluation daemon with one shared task pool across all agents of all v2 arms.

Repeatedly finds finished compiled children (and nothing else) whose fresh1 results are incomplete and submits
(agent, task) jobs to a single pool, so slow tasks never block other agents. Stops when STOP_FRESH3 exists.
"""
import os, sys, json, glob, time, threading, concurrent.futures as cf
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
sys.path.insert(0, os.path.expanduser('~/shi_eval/exp'))
import run_task, lcb
from eval_agents import tasks_for
SHI = os.path.expanduser('~/shi_eval')
STAGE = sys.argv[1] if len(sys.argv) > 1 else 'fresh1'
WORKERS = int(sys.argv[2]) if len(sys.argv) > 2 else 48
PATTERN = sys.argv[3] if len(sys.argv) > 3 else 'v2_*'
T = tasks_for(STAGE); I = lcb.index()
locks = {}; inflight = set(); glock = threading.Lock()

def file_lock(p):
    with glock:
        return locks.setdefault(p, threading.Lock())

def done_tasks(path):
    s = set()
    if os.path.exists(path):
        for l in open(path):
            r = json.loads(l)
            if r.get('rep', 0) == 0: s.add(r['task'])
    return s

def job(exp, aid, tid):
    ad = os.path.join(SHI, 'exps', exp, 'agents', aid)
    cfg = json.load(open(os.path.join(SHI, 'exps', exp, 'config.json')))
    run_id = f'{exp}|{aid}|{STAGE}|{tid}|0'
    try:
        r = run_task.run_agent(os.path.join(ad, 'code'), I[tid], run_id, os.path.join(ad, 'runs', STAGE, f'{tid}_r0'),
                               model=cfg['task_model'], budget=cfg.get('task_budget', 0.25), timeout=cfg.get('task_timeout', 600))
    except Exception as e:
        r = {'run': run_id, 'task': tid, 'passed': False, 'empty': True, 'error': repr(e)[:300]}
    r['rep'] = 0; r['stage'] = STAGE
    p = os.path.join(ad, 'evals', f'{STAGE}.jsonl'); os.makedirs(os.path.dirname(p), exist_ok=True)
    with file_lock(p):
        with open(p, 'a') as f: f.write(json.dumps(r) + '\n')
    with glock: inflight.discard((exp, aid, tid))

pool = cf.ThreadPoolExecutor(WORKERS)
while not os.path.exists(os.path.join(SHI, 'STOP_FRESH3')):
    queued = 0
    for mp in sorted(glob.glob(os.path.join(SHI, 'exps', PATTERN, 'agents', 'g*', 'meta.json'))):
        try: m = json.load(open(mp))
        except Exception: continue
        if not m.get('done') or not m.get('compiled') or m.get('mode') == 'placebo': continue
        exp = mp.split('/')[-4]; aid = m['aid']
        have = done_tasks(os.path.join(os.path.dirname(mp), 'evals', f'{STAGE}.jsonl'))
        for tid in T:
            key = (exp, aid, tid)
            with glock:
                if tid in have or key in inflight: continue
                inflight.add(key)
            pool.submit(job, exp, aid, tid); queued += 1
    print(time.strftime('%H:%M:%S'), 'queued', queued, 'inflight', len(inflight), flush=True)
    time.sleep(300)

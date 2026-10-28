"""Prioritized fresh-set evaluation (F1) across arms with one shared pool; keeps the pool queue short.

Priority: (0) current best-by-S agent of every loop arm, (1) every fully evaluated child of the ladder arms
(single steps, chains), (2) other fully evaluated archive members of loop arms. Children that did not reach the
full selection evaluation are skipped. Stops when STOP_FRESH4 exists.
"""
import os, sys, json, glob, time, threading, concurrent.futures as cf
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
sys.path.insert(0, os.path.expanduser('~/shi_eval/exp'))
sys.path.insert(0, os.path.expanduser('~/shi_eval/analysis'))
import run_task, lcb
from eval_agents import tasks_for
from collect import collect
SHI = os.path.expanduser('~/shi_eval')
STAGE = sys.argv[1] if len(sys.argv) > 1 else 'fresh1'
WORKERS = int(sys.argv[2]) if len(sys.argv) > 2 else 64
PATTERN = sys.argv[3] if len(sys.argv) > 3 else 'v2_*'
T = tasks_for(STAGE); I = lcb.index()
glock = threading.Lock(); flocks = {}; inflight = set(); pending = [0]

def done_tasks(ad):
    p = os.path.join(ad, 'evals', f'{STAGE}.jsonl'); s = set()
    if os.path.exists(p):
        for l in open(p):
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
    with glock: fl = flocks.setdefault(p, threading.Lock())
    with fl:
        with open(p, 'a') as f: f.write(json.dumps(r) + '\n')
    with glock: inflight.discard((exp, aid, tid)); pending[0] -= 1

def targets():
    out = []
    for d in sorted(glob.glob(os.path.join(SHI, 'exps', PATTERN))):
        exp = os.path.basename(d)
        try: cfg, st, recs = collect(exp)
        except Exception: continue
        full = [r for r in recs if r['aid'] != 'initial' and r['compiled'] and r['sel_full']]
        if cfg['mode'] == 'placebo': continue
        is_loop = os.path.exists(os.path.join(d, 'dgm_metadata.jsonl')) and cfg['mode'] == 'dgm' and 'C2' not in exp
        if is_loop:
            arch = [r for r in full if r['in_archive']]
            if arch:
                b = max(arch, key=lambda r: r['sel']); out.append((0, exp, b['aid']))
                out += [(2, exp, r['aid']) for r in arch if r['aid'] != b['aid']]
        else:
            out += [(1, exp, r['aid']) for r in full]
    return sorted(out)

pool = cf.ThreadPoolExecutor(WORKERS)
while not os.path.exists(os.path.join(SHI, 'STOP_FRESH4')):
    sub = 0
    for pr, exp, aid in targets():
        if pending[0] >= 2 * WORKERS: break
        ad = os.path.join(SHI, 'exps', exp, 'agents', aid); have = done_tasks(ad)
        for tid in T:
            if pending[0] >= 2 * WORKERS: break
            key = (exp, aid, tid)
            with glock:
                if tid in have or key in inflight: continue
                inflight.add(key); pending[0] += 1
            pool.submit(job, exp, aid, tid); sub += 1
    print(time.strftime('%H:%M:%S'), 'submitted', sub, 'pending', pending[0], flush=True)
    time.sleep(60)

"""Run many (agent, task, rep) jobs concurrently; results appended to a JSONL (resume-safe)."""
import json, os, sys, time, threading, argparse, concurrent.futures as cf, traceback
sys.path.insert(0, os.path.dirname(__file__))
import run_task, lcb
SHI = os.path.expanduser('~/shi_eval')

def run_jobs(jobs, results_path, workers=16, model='claude-haiku-5-5', budget=0.25, timeout=900, keep=False,
             log_every=20):
    """jobs: list of dicts {agent_dir, agent_name, task_id, rep, outdir}. Returns list of results."""
    done = set()
    if os.path.exists(results_path):
        for l in open(results_path):
            try: r = json.loads(l); done.add((r['agent'], r['task'], r['rep']))
            except Exception: pass
    todo = [j for j in jobs if (j['agent_name'], j['task_id'], j['rep']) not in done]
    lock = threading.Lock(); I = lcb.index(); out = []; t0 = time.time(); n = [0]
    def one(j):
        run_id = f"{j['exp']}|{j['agent_name']}|{j['task_id']}|{j['rep']}"
        try:
            r = run_task.run_agent(j['agent_dir'], I[j['task_id']], run_id, j['outdir'], model=j.get('model', model),
                                   budget=j.get('budget', budget), timeout=j.get('timeout', timeout), keep_repo=keep)
        except Exception as e:
            r = {'run': run_id, 'task': j['task_id'], 'passed': False, 'error': repr(e)[:500], 'trace': traceback.format_exc()[-1500:]}
        r.update(agent=j['agent_name'], rep=j['rep'], exp=j['exp'], model=j.get('model', model))
        with lock:
            with open(results_path, 'a') as f: f.write(json.dumps(r) + '\n')
            n[0] += 1
            if n[0] % log_every == 0 or n[0] == len(todo):
                print(f'[{time.strftime("%H:%M:%S")}] {n[0]}/{len(todo)} done, {time.time()-t0:.0f}s', flush=True)
        return r
    with cf.ThreadPoolExecutor(workers) as ex:
        for r in ex.map(one, todo): out.append(r)
    return out

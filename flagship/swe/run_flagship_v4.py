"""Flagship driver (v4 = v3 + --keep-order): run one agent through DGM's SWE-bench harness (agent inside the task container) on a list of
SWE-bench Verified instances, with the task model routed by this VM's proxy, then grade with the official swebench
evaluation exactly as DGM's swe_bench/report.py does. Writes <out>/results.jsonl, <out>/summary.json,
<out>/run_meta.a<K>.json and one <out>/status/<instance>.a<K>.json per instance and attempt.

Run on shi-swe-1:
  source ~/shi_eval/flagship/swe/env.sh
  $PY -I $F/swe/run_flagship.py --agent-dir $F/agents/dgm_init/dgm --instances ID1,ID2   (or a JSON list file) \
      --model claude-haiku-4-5 --budget 5 --workers 8 --out $F/runs/<name> [--patch P ...] [--attempt K] [--harness clean]

- --agent-dir must end in /dgm (DGM's harness copies the agent files from a cwd named .../dgm) and its
  llm_withtools.py must have CLAUDE_MODEL = 'claude-3-5-sonnet-20241022' (the proxy token decides the real model).
- One proxy token per instance and attempt: run id '<tag>/<iid>' (attempt 0) or '<tag>.a<K>/<iid>' (attempt K), each
  with the full --budget. The spend of every attempt counts: results sum the ledger rows of attempts 0..K.
- Re-runs (after a preemption or an infrastructure failure): same --out, --attempt K+1. Skipped: instances with a
  prediction JSON (DGM's harness does this too) and instances whose last attempt failed in the agent step (an agent
  outcome, not infrastructure) unless --rerun-agent-failures. Refuses to reuse an attempt number that already has ledger
  rows for an instance it would run. Diagnostics of an earlier attempt move to diag/a<k>/.
- --patch: model patches applied in the container before the agent runs (DGM's lineage mechanism), in order.
- --harness proxy (default): swe/dgm_harness_proxy.py; --harness clean: swe/dgm_harness_proxy_clean.py (same, plus removal
  of .pytest_cache dirs and of the untracked files the test patch adds, after DGM's setup step and before the agent).
- Harness-side code (swe_bench/*, prompts.testrepo_prompt, utils.common_utils) comes from the DGM repo copy, as in DGM,
  where the harness runs from the base repo and only the container sees the agent's code.
"""
import argparse, datetime, glob, json, os, re, shutil, socket, statistics, subprocess, sys, time
sys.dont_write_bytecode = True
F = os.path.expanduser('~/shi_eval/flagship')
DGM_REPO = os.path.join(F, 'dgm_repo')
INFRA = os.path.expanduser('~/shi_eval/infra')
SWE = os.path.dirname(os.path.abspath(__file__))
for p in (DGM_REPO, INFRA, SWE):
    sys.path.insert(0, p)
import run_task                                   # unmodified infra copy: mint() with this VM's secret, spent() via the socket
from llm_proxy_cache import PRICES               # prices of the proxy file running on this VM (llm_proxy_cache.py)
import dgm_harness_proxy as H                     # DGM harness.py + flagship changes (harness_proxy.diff)
from swe_bench.report import load_predictions, preds_to_jsonl   # DGM's own report helpers

PROXY_HOST, PROXY_PORT = '172.17.0.1', 8080
AGENT_FILES = ['coding_agent.py', 'requirements.txt', 'pytest.ini', 'tools', 'utils', 'tests', 'prompts', 'llm.py',
               'llm_withtools.py']           # what DGM's harness copies into the container
MODEL_LINE = "CLAUDE_MODEL = 'claude-3-5-sonnet-20241022'"
DATASET = 'princeton-nlp/SWE-bench_Verified'
TS = re.compile(r'^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3}) ')
STEPS = [('Setting up environment', 'setup'), ('Applying model patches', 'setup'), ('Installing more requirements', 'setup'),
         ('Running the agent', 'agent'), ('Copying output files back to host', 'copyout')]   # harness log markers


def git(d, *args):
    r = subprocess.run(['git', '-C', d, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def run_id_for(tag, iid, k):
    return f'{tag}/{iid}' if k == 0 else f'{tag}.a{k}/{iid}'


def spent_many(runs):
    out = {}
    for i in range(0, len(runs), 100):
        out.update(run_task.spent(runs=runs[i:i + 100]))
    return out


def log_part(path, start):
    """Lines of the per-instance docker log from byte offset `start` (the harness appends to it across attempts)."""
    try:
        with open(path, errors='replace') as f:
            f.seek(start); return f.read().splitlines()
    except FileNotFoundError:
        return []


def log_times(lines):
    """Seconds before the agent (container, eval.sh setup, pip) and in the agent step."""
    first = start = end = None
    for line in lines:
        m = TS.match(line)
        if not m: continue
        t = datetime.datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S,%f').timestamp()
        first = first or t
        if line.rstrip().endswith('- Running the agent'): start = t
        elif line.rstrip().endswith('- Copying output files back to host'): end = t
    return (round(start - first, 1) if first and start else None), (round(end - start, 1) if start and end else None)


def failed_step(lines):
    step = 'container'
    for line in lines:
        for marker, name in STEPS:
            if line.rstrip().endswith('- ' + marker): step = name
    return step


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--agent-dir', required=True)
    ap.add_argument('--instances', required=True, help='comma-separated instance ids, or a JSON file with a list of ids')
    ap.add_argument('--model', required=True, help='proxy model id (a key of llm_proxy.PRICES)')
    ap.add_argument('--budget', type=float, required=True, help='USD per run and attempt, enforced by the proxy token')
    ap.add_argument('--workers', type=int, default=2, help='parallel task containers (DGM harness max_workers)')
    ap.add_argument('--eval-workers', type=int, default=None, help='swebench run_evaluation --max_workers (default: --workers)')
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default=None)
    ap.add_argument('--patch', action='append', default=[])
    ap.add_argument('--attempt', type=int, default=0)
    ap.add_argument('--rerun-agent-failures', action='store_true')
    ap.add_argument('--no-eval', action='store_true')
    ap.add_argument('--harness', choices=['proxy', 'clean'], default='proxy')
    ap.add_argument('--keep-order', action='store_true', help='run instances in the --instances list order')
    a = ap.parse_args()
    global H
    if a.harness == 'clean':
        import dgm_harness_proxy_clean as H

    agent = os.path.realpath(a.agent_dir)
    if not agent.endswith('/dgm'): sys.exit(f'agent dir must end in /dgm: {agent}')
    missing = [f for f in AGENT_FILES if not os.path.exists(os.path.join(agent, f))]
    if missing: sys.exit(f'agent dir lacks {missing}')
    lines = [l.strip() for l in open(os.path.join(agent, 'llm_withtools.py')) if l.startswith('CLAUDE_MODEL')]
    if lines != [MODEL_LINE]: sys.exit(f'llm_withtools.py CLAUDE_MODEL line is {lines}, want [{MODEL_LINE!r}]')
    if a.model not in PRICES: sys.exit(f'model {a.model} has no price in llm_proxy_cache.PRICES')
    patches = [os.path.realpath(p) for p in a.patch]
    for p in patches:
        if not os.path.isfile(p): sys.exit(f'missing patch {p}')
    if os.path.isfile(a.instances): ids = json.load(open(a.instances))
    else: ids = [x for x in a.instances.split(',') if x]
    if len(set(ids)) != len(ids): sys.exit('duplicate instance ids')
    out = os.path.realpath(a.out); tag = a.tag or os.path.basename(out); K = a.attempt
    status_dir = os.path.join(out, 'status'); pred_dname = os.path.join(out, 'predictions', f'{tag}_0')
    try:
        socket.create_connection((PROXY_HOST, PROXY_PORT), timeout=5).close()
        g = run_task.spent()
    except Exception as e:
        sys.exit(f'proxy/forwarder not reachable: {e!r} (start with ~/shi_eval/flagship/swe/start_proxy.sh)')

    def last_status(iid):
        fs = [(int(m.group(1)), p) for p in glob.glob(os.path.join(status_dir, f'{iid}.a*.json'))
              for m in [re.search(r'\.a(\d+)\.json$', p)] if m]
        return json.load(open(max(fs)[1])) if fs else None
    todo = []
    for iid in ids:
        if os.path.exists(os.path.join(pred_dname, f'{iid}.json')): continue
        st = last_status(iid)
        if st and st.get('failed_step') == 'agent' and not a.rerun_agent_failures: continue
        todo.append(iid)
    used = spent_many([run_id_for(tag, i, K) for i in todo])
    clash = [i for i in todo if used.get(run_id_for(tag, i, K), {}).get('calls', 0) > 0]
    if clash: sys.exit(f'attempt {K} already has ledger rows for {len(clash)} instances (e.g. {clash[0]}): use --attempt {K + 1}')
    cap = float(open(os.path.expanduser('~/shi_eval/ledger/global_cap.txt')).read().strip())
    print(f'attempt {K}: {len(todo)} of {len(ids)} instances to run; proxy spent ${g["total"]:.4f} of cap ${cap:.2f}; '
          f'this attempt at most ~${len(todo) * a.budget:.2f}', flush=True)
    if g['total'] + len(todo) * a.budget > cap:
        print('WARNING: runs may stop at the global cap (proxy answers "[budget exhausted]")', flush=True)

    os.makedirs(status_dir, exist_ok=True)
    ddir = os.path.join(pred_dname, 'diag')
    for iid in todo:                              # keep an earlier attempt's diagnostics
        st = last_status(iid)
        olds = glob.glob(os.path.join(ddir, f'{iid}.md')) + glob.glob(os.path.join(ddir, f'{iid}_*'))
        if st and olds:
            dst = os.path.join(ddir, f'a{st["attempt"]}'); os.makedirs(dst, exist_ok=True)
            for p in olds: shutil.move(p, os.path.join(dst, os.path.basename(p)))
    meta = dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), tag=tag, attempt=K,
                agent_dir=agent, agent_head=git(agent, 'rev-parse', 'HEAD'), agent_diff=git(agent, 'diff', 'HEAD'),
                model=a.model, budget_usd=a.budget, workers=a.workers, patches=patches, instances=ids, run_now=todo,
                keep_order=a.keep_order,
                harness=('swe/dgm_harness_proxy_clean.py (harness_proxy.diff + harness_proxy_clean.diff)' if a.harness == 'clean'
                         else 'swe/dgm_harness_proxy.py (harness_proxy.diff)'), dataset=DATASET,
                swebench_commit=git(os.path.join(F, 'dl', 'SWE-bench'), 'rev-parse', 'HEAD'))
    json.dump(meta, open(os.path.join(out, f'run_meta.a{K}.json'), 'w'), indent=1)

    os.environ['ANTHROPIC_BASE_URL'] = f'http://{PROXY_HOST}:{PROXY_PORT}'
    os.environ.pop('ANTHROPIC_API_KEY', None)
    H.api_key_for = lambda iid: run_task.mint(run_id_for(tag, iid, K), a.model, a.budget, single_tool_call=True)
    orig = H.process_entry
    def timed(entry, *args, **kw):
        iid = entry['instance_id']; logf = os.path.join(pred_dname, f'{iid}_docker.log')
        off = os.path.getsize(logf) if os.path.exists(logf) else 0
        t0 = time.time(); r = orig(entry, *args, **kw); wall = round(time.time() - t0, 1)
        part = log_part(logf, off); setup_s, agent_s = log_times(part)
        st = dict(instance_id=iid, attempt=K, success=r.get('success'), error=r.get('error'),
                  failed_step=None if r.get('success') else failed_step(part), wall_s=wall, setup_s=setup_s,
                  agent_s=agent_s, t0_utc=datetime.datetime.fromtimestamp(t0, datetime.timezone.utc).isoformat(timespec='seconds'))
        json.dump(st, open(os.path.join(status_dir, f'{iid}.a{K}.json'), 'w'), indent=1)
        return r
    H.process_entry = timed
    if a.keep_order:   # DGM's harness iterates the dataset order; hand it the rows in the --instances order instead
        pos = {iid: k for k, iid in enumerate(ids)}; _load = H.load_dataset
        H.load_dataset = lambda *x, **kw: {'test': sorted(_load(*x, **kw)['test'], key=lambda e: pos.get(e['instance_id'], len(pos)))}

    t_agents = 0.0
    if todo:                                      # never call the harness with an empty list: DGM's harness then runs ALL tasks
        os.chdir(agent)                           # DGM's harness copies the agent files from a cwd named .../dgm
        t_run = time.time()
        dnames = H.harness(test_task_list=todo, num_samples=-1, max_workers=a.workers, model_name_or_path=tag,
                           model_patch_paths=patches or None, num_evals=1, num_evals_parallel=1,
                           pred_dname=os.path.join(out, 'predictions'))
        t_agents = round(time.time() - t_run, 1)
        assert str(dnames[0]) == pred_dname, (dnames, pred_dname)
    os.chdir(out)
    run_id = os.path.basename(pred_dname)         # '<tag>_0' as in DGM (model_name_or_path + eval idx)

    eval_rc = None; t_eval = 0.0
    preds = load_predictions([pred_dname]) if os.path.isdir(pred_dname) else {}
    if preds and not a.no_eval:
        jsonl = preds_to_jsonl(pred_dname, preds)    # DGM's filter: drops patch hunks to test files
        cmd = [sys.executable, '-I', '-m', 'swebench.harness.run_evaluation', '--dataset_name', DATASET,
               '--predictions_path', jsonl, '--max_workers', str(a.eval_workers or a.workers), '--run_id', run_id]
        t1 = time.time()
        with open(os.path.join(out, 'eval.log'), 'a') as lf:
            eval_rc = subprocess.run(cmd, cwd=out, stdout=lf, stderr=subprocess.STDOUT).returncode
        t_eval = round(time.time() - t1, 1)

    spend = spent_many([run_id_for(tag, i, k) for i in ids for k in range(K + 1)])
    rows = []
    for iid in ids:
        p = preds.get(iid); patch = (p or {}).get('model_patch') or ''
        rep_path = os.path.join(out, 'logs', 'run_evaluation', run_id, run_id, iid, 'report.json')
        rep = json.load(open(rep_path)).get(iid, {}) if os.path.exists(rep_path) else None
        ts = (rep or {}).get('tests_status', {})
        att = [spend.get(run_id_for(tag, iid, k), {}) for k in range(K + 1)]
        tot = lambda key: sum(x.get(key, 0) or 0 for x in att)
        st = last_status(iid) or {}
        # resolved: from the swebench report; an empty patch is unresolved; no prediction / no report = unknown (None)
        resolved = rep.get('resolved') if rep is not None else (False if p is not None and not patch.strip() else None)
        last_usd = (att[st['attempt']].get('usd', 0.0) if st else 0.0) or 0.0
        rows.append(dict(
            instance_id=iid, resolved=resolved, prediction=p is not None, patch_lines=len(patch.splitlines()),
            patch_empty=not patch.strip(),
            f2p_pass=len(ts.get('FAIL_TO_PASS', {}).get('success', [])) if ts else None,
            f2p_fail=len(ts.get('FAIL_TO_PASS', {}).get('failure', [])) if ts else None,
            p2p_fail=len(ts.get('PASS_TO_PASS', {}).get('failure', [])) if ts else None,
            usd=round(tot('usd'), 4), usd_attempts=[round(x.get('usd', 0.0), 4) for x in att], calls=tot('calls'),
            inp=tot('inp'), cache_read=tot('cr'), cache_write=tot('cw'), out=tot('out'), proxy_errors=tot('errors'),
            budget_hit=last_usd >= a.budget, attempts=len([x for x in att if x.get('calls')]),
            last_attempt=st.get('attempt'), wall_s=st.get('wall_s'), setup_s=st.get('setup_s'), agent_s=st.get('agent_s'),
            harness_ok=st.get('success'), failed_step=st.get('failed_step'), harness_error=st.get('error')))
    with open(os.path.join(out, 'results.jsonl'), 'w') as f:
        for r in rows: f.write(json.dumps(r) + '\n')
    n = len(rows); usd = [r['usd'] for r in rows]
    summ = dict(tag=tag, model=a.model, agent_dir=agent, harness=a.harness, attempt=K, n=n, resolved=sum(1 for r in rows if r['resolved']),
                predictions=sum(r['prediction'] for r in rows), empty_patches=sum(r['patch_empty'] for r in rows if r['prediction']),
                agent_failures=sum(1 for r in rows if r['failed_step'] == 'agent'), budget_hits=sum(r['budget_hit'] for r in rows),
                usd_total=round(sum(usd), 4), usd_mean=round(statistics.mean(usd), 4) if usd else 0,
                usd_median=round(statistics.median(usd), 4) if usd else 0,
                inp_total=sum(r['inp'] for r in rows), cache_read_total=sum(r['cache_read'] for r in rows),
                cache_write_total=sum(r['cache_write'] for r in rows), out_total=sum(r['out'] for r in rows),
                harness_wall_s=t_agents, eval_wall_s=t_eval, eval_rc=eval_rc, workers=a.workers,
                end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
    json.dump(summ, open(os.path.join(out, 'summary.json'), 'w'), indent=1)
    for r in rows:
        print(f"{r['instance_id']:32s} resolved={r['resolved']} patch_lines={r['patch_lines']} usd={r['usd']:.4f} "
              f"calls={r['calls']} in={r['inp']} cr={r['cache_read']} cw={r['cache_write']} out={r['out']} "
              f"wall={r['wall_s']}s agent={r['agent_s']}s budget_hit={r['budget_hit']} failed_step={r['failed_step']} "
              f"{r['harness_error'] or ''}", flush=True)
    print(json.dumps(summ), flush=True)


if __name__ == '__main__':
    main()

"""Leak check: run DGM's in-container setup step (swe_bench/harness.py process_entry: copy eval.sh, `/bin/bash /eval.sh`,
`rm /eval.sh`, i.e. hidden test patch applied, tests run, modified test files reset) in a fresh task container exactly as
the harness does, then report what an agent would find in /testbed: pytest's cache (lastfailed / nodeids vs the hidden
FAIL_TO_PASS / PASS_TO_PASS ids) and the files the hidden test patch added. No agent, no LLM calls.
Usage (on the SWE-bench machine): $PY -I leak_check.py OUTDIR IID [IID ...]   -> OUTDIR/leak_check.json
"""
import datetime, json, os, re, sys
sys.dont_write_bytecode = True
F = os.path.expanduser('~/shi_eval/flagship')
sys.path.insert(0, os.path.join(F, 'dgm_repo'))
from pathlib import Path
import docker
from datasets import load_dataset
from swebench.harness.test_spec import make_test_spec
from swebench.harness.docker_build import build_container, cleanup_container
from swe_bench.utils import copy_to_container, log_container_output, remove_existing_container, setup_logger

out = Path(os.path.realpath(sys.argv[1])); ids = sys.argv[2:]
out.mkdir(parents=True, exist_ok=True); os.chdir(out)
ds = {e['instance_id']: e for e in load_dataset('princeton-nlp/SWE-bench_Verified')['test'] if e['instance_id'] in set(ids)}
client = docker.from_env()
results = {}
for iid in ids:
    entry = ds[iid]
    f2p, p2p = json.loads(entry['FAIL_TO_PASS']), json.loads(entry['PASS_TO_PASS'])
    added = re.findall(r'^--- /dev/null\n\+\+\+ b/(\S+)', entry['test_patch'], re.M)
    logger = setup_logger(str(out / f'{iid}_docker.log'))
    run_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    test_spec = make_test_spec(entry)
    remove_existing_container(client, test_spec.get_instance_container_name(run_id))
    container = build_container(test_spec, client, run_id, logger, True, force_rebuild=False)
    container.start()
    r = dict(instance_id=iid, repo=entry['repo'], test_cmd=test_spec.eval_script.splitlines()[-2][:120], f2p=f2p)
    try:
        # --- DGM harness setup step, as in process_entry ---
        eval_file = out / f'{iid}_eval.sh'
        eval_file.write_text(test_spec.eval_script)
        copy_to_container(container, eval_file, '/eval.sh')
        res = container.exec_run("/bin/bash /eval.sh", workdir='/')
        r['eval_sh_exit'] = res.exit_code
        (out / f'{iid}_eval_output.txt').write_bytes(res.output)
        try: log_container_output(res)                  # the harness would stop the instance here on a non-zero exit
        except Exception as e: r['harness_would_fail'] = str(e)
        container.exec_run("rm /eval.sh", workdir='/')
        # --- inspection: what the agent would find ---
        def sh(cmd):
            x = container.exec_run(['bash', '-c', cmd], workdir='/'); return x.exit_code, x.output.decode(errors='replace')
        _, caches = sh("find /testbed -path '*/.pytest_cache/v/cache/*' -type f 2>/dev/null")
        r['pytest_cache_files'] = caches.split()
        lf = {}
        for p in r['pytest_cache_files']:
            if p.endswith('/lastfailed'):
                try: lf.update(json.loads(sh(f'cat {p}')[1]))
                except Exception: pass
        nodeids = []
        for p in r['pytest_cache_files']:
            if p.endswith('/nodeids'):
                try: nodeids += json.loads(sh(f'cat {p}')[1])
                except Exception: pass
        r['lastfailed_ids'] = sorted(lf)
        r['lastfailed_in_f2p'] = sorted(set(lf) & set(f2p)); r['lastfailed_in_p2p'] = sorted(set(lf) & set(p2p))
        r['f2p_in_lastfailed'] = f'{len(set(f2p) & set(lf))}/{len(f2p)}'
        r['f2p_in_nodeids'] = f'{len(set(f2p) & set(nodeids))}/{len(f2p)}'
        r['added_test_files'] = {a: sh(f'test -e /testbed/{a}')[0] == 0 for a in added}
        r['git_status_untracked'] = [l for l in sh('git -C /testbed status --porcelain --untracked-files=all')[1].splitlines()]
        r['git_status_ignored'] = [l for l in sh('git -C /testbed status --porcelain --ignored --untracked-files=normal')[1].splitlines()
                                   if l.startswith('!!')][:30]
        r['tracked_diff_stat'] = sh('git -C /testbed diff --stat')[1].strip()[-300:]
    finally:
        cleanup_container(client, container, logger)
    results[iid] = r
    print(json.dumps({k: r[k] for k in ('instance_id', 'eval_sh_exit', 'pytest_cache_files', 'f2p_in_lastfailed', 'f2p_in_nodeids',
                                       'added_test_files', 'git_status_untracked') if k in r}), flush=True)
json.dump(results, open(out / 'leak_check.json', 'w'), indent=1)

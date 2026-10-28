"""Verify the clean harness step (swe/dgm_harness_proxy_clean.py: clean_hidden_test_residue) on given instances, with
no agent: DGM's setup step exactly as in the harness, then the clean step (the same function), then
 (1) no .pytest_cache left under /testbed (lastfailed gone), (2) the test patch's added files gone,
 (3) the environment still works: the instance's test command on its test files that still exist (after the reset they
     are the base versions), statuses parsed with swebench's own log parser, PASS_TO_PASS tests counted.
Usage (on the SWE-bench machine): $PY -I clean_check.py OUTDIR IID[=FALLBACK_TEST_FILE] ...  -> OUTDIR/clean_check.json, OUTDIR/PASS
(FALLBACK_TEST_FILE is run when no test file of the instance is left, e.g. when its only test file was added.)"""
import datetime, json, os, shlex, sys
sys.dont_write_bytecode = True
F = os.path.expanduser('~/shi_eval/flagship')
for p in (os.path.join(F, 'dgm_repo'), os.path.join(F, 'swe')):
    sys.path.insert(0, p)
from pathlib import Path
import docker
from datasets import load_dataset
from swebench.harness.test_spec import make_test_spec, get_test_directives
from swebench.harness.constants import MAP_REPO_VERSION_TO_SPECS
from swebench.harness.log_parsers import MAP_REPO_TO_PARSER
from swebench.harness.docker_build import build_container, cleanup_container
from swe_bench.utils import copy_to_container, log_container_output, remove_existing_container, setup_logger
from dgm_harness_proxy_clean import clean_hidden_test_residue

out = Path(os.path.realpath(sys.argv[1])); args = sys.argv[2:]
out.mkdir(parents=True, exist_ok=True); os.chdir(out)
want = {a.split('=')[0]: (a.split('=', 1)[1] if '=' in a else None) for a in args}
ds = {e['instance_id']: e for e in load_dataset('princeton-nlp/SWE-bench_Verified')['test'] if e['instance_id'] in want}
client = docker.from_env(); results = {}; ok_all = True
for iid, fallback in want.items():
    entry = ds[iid]; p2p = json.loads(entry['PASS_TO_PASS'])
    logger = setup_logger(str(out / f'{iid}_docker.log'))
    run_id = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    spec = make_test_spec(entry)
    remove_existing_container(client, spec.get_instance_container_name(run_id))
    container = build_container(spec, client, run_id, logger, True, force_rebuild=False)
    container.start()
    r = dict(instance_id=iid)
    try:
        eval_file = out / f'{iid}_eval.sh'; eval_file.write_text(spec.eval_script)        # DGM setup step, as in process_entry
        copy_to_container(container, eval_file, '/eval.sh')
        log_container_output(container.exec_run("/bin/bash /eval.sh", workdir='/'))
        log_container_output(container.exec_run("rm /eval.sh", workdir='/'))
        clean_hidden_test_residue(container, entry, out)                                  # the clean step under test
        r['clean_log'] = json.load(open(out / 'clean' / f'{iid}.json'))
        sh = lambda c: container.exec_run(['bash', '-c', c], workdir='/')
        r['lastfailed_left'] = sh("find /testbed -path '*/.pytest_cache/v/cache/lastfailed'").output.decode().split()
        r['pytest_cache_left'] = sh("find /testbed -type d -name .pytest_cache").output.decode().split()
        r['added_left'] = r['clean_log']['left_added_files']
        r['git_status'] = sh('git -C /testbed status --porcelain --untracked-files=all').output.decode().splitlines()
        # environment check: the instance's test command on its remaining test files (or the fallback file)
        files = [d for d in get_test_directives(entry) if sh(f'test -e /testbed/{shlex.quote(d)}').exit_code == 0] or \
                ([fallback] if fallback else [])
        test_cmd = MAP_REPO_VERSION_TO_SPECS[entry['repo']][entry['version']]['test_cmd']
        cmd = f"source /opt/miniconda3/bin/activate && conda activate testbed && cd /testbed && {test_cmd} {' '.join(map(shlex.quote, files))}"
        res = sh(cmd); log = res.output.decode(errors='replace')
        (out / f'{iid}_envcheck.txt').write_text(cmd + '\n\n' + log)
        st = MAP_REPO_TO_PARSER[entry['repo']](log)
        present = [t for t in p2p if t in st]
        r.update(env_cmd=f'{test_cmd} {" ".join(files)}', env_exit=res.exit_code, n_tests_parsed=len(st),
                 passed=sum(1 for v in st.values() if v == 'PASSED'), failed=sum(1 for v in st.values() if v in ('FAILED', 'ERROR')),
                 p2p_total=len(p2p), p2p_present=len(present), p2p_passed=sum(1 for t in present if st[t] == 'PASSED'),
                 p2p_not_passed=[t for t in present if st[t] != 'PASSED'][:10])
        r['ok'] = (not r['lastfailed_left'] and not r['pytest_cache_left'] and not r['added_left'] and r['passed'] > 0
                   and r['p2p_passed'] == r['p2p_present'])
    finally:
        cleanup_container(client, container, logger)
    ok_all &= bool(r.get('ok')); results[iid] = r
    print(json.dumps({k: r.get(k) for k in ('instance_id', 'ok', 'lastfailed_left', 'pytest_cache_left', 'added_left', 'env_cmd',
                                           'env_exit', 'passed', 'failed', 'p2p_total', 'p2p_present', 'p2p_passed')}), flush=True)
json.dump(results, open(out / 'clean_check.json', 'w'), indent=1)
if ok_all: (out / 'PASS').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds') + '\n')
print('ALL OK' if ok_all else 'NOT ALL OK', flush=True)

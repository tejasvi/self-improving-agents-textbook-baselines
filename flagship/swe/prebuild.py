"""Prebuild swebench (2.1.0, DGM's pinned version) base/env/instance images for a list of SWE-bench Verified ids, once,
before any agent batch. Usage: $PY -I prebuild.py IDS.json OUTDIR WORKERS
Writes OUTDIR/prebuild_failures.json and OUTDIR/prebuild_summary.json; swebench build logs go to OUTDIR/logs/build_images/."""
import json, os, sys, time, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import docker
from datasets import load_dataset
from swebench.harness.test_spec import make_test_spec
from swebench.harness.docker_build import build_env_images, build_instance_image

ids, outdir, W = json.load(open(sys.argv[1])), os.path.realpath(sys.argv[2]), int(sys.argv[3])
os.makedirs(outdir, exist_ok=True); os.chdir(outdir)       # swebench writes logs/build_images/... relative to cwd
ds = load_dataset('princeton-nlp/SWE-bench_Verified')['test']
want = set(ids); entries = [e for e in ds if e['instance_id'] in want]
assert len(entries) == len(want), (len(entries), len(want))
client = docker.from_env()
specs = [make_test_spec(e) for e in entries]
def exists(tag):
    try: client.images.get(tag); return True
    except docker.errors.ImageNotFound: return False
t0 = time.time()
print(f'{datetime.datetime.now(datetime.timezone.utc):%H:%M:%SZ} {len(specs)} instances, '
      f'{len({s.env_image_key for s in specs})} env images, already built: {sum(exists(s.instance_image_key) for s in specs)}', flush=True)
_, env_failed = build_env_images(client, specs, False, W)
t_env = time.time() - t0
todo = [s for s in specs if s.env_image_key not in env_failed]
inst_failed = {}
with ThreadPoolExecutor(max_workers=W) as ex:
    futs = {ex.submit(build_instance_image, s, client, None, False): s for s in todo}
    for i, f in enumerate(as_completed(futs), 1):
        s = futs[f]
        try: f.result()
        except Exception as e: inst_failed[s.instance_id] = f'{type(e).__name__}: {str(e)[:400]}'
        if i % 20 == 0: print(f'{datetime.datetime.now(datetime.timezone.utc):%H:%M:%SZ} instance images {i}/{len(todo)}, failed {len(inst_failed)}', flush=True)
by_env = {}
for s in specs:
    if s.env_image_key in env_failed:
        by_env.setdefault(s.env_image_key, {'repo': s.repo, 'version': s.version, 'instances': []})['instances'].append(s.instance_id)
missing = sorted(s.instance_id for s in specs if not exists(s.instance_image_key))
fail = dict(env_failed=by_env, instance_failed=inst_failed, missing_instance_images=missing,
            n_instances=len(specs), n_missing=len(missing))
json.dump(fail, open(os.path.join(outdir, 'prebuild_failures.json'), 'w'), indent=1)
summ = dict(n_instances=len(specs), n_env_images=len({s.env_image_key for s in specs}), env_failed=len(env_failed),
            instance_failed=len(inst_failed), missing=len(missing), env_wall_s=round(t_env), total_wall_s=round(time.time() - t0),
            workers=W, end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
json.dump(summ, open(os.path.join(outdir, 'prebuild_summary.json'), 'w'), indent=1)
print(json.dumps(summ), flush=True)

"""Check, offline, that swebench builds the test specs of the given instances from the cached requirement files and
that their instance images exist locally. Usage: r3_check_specs.py INSTANCES_JSON"""
import json, sys, subprocess
import requests
assert requests.get.__name__ == '_get', 'sitecustomize shim not active'
from datasets import load_dataset
from swebench.harness.test_spec import make_test_spec
ids = set(json.load(open(sys.argv[1])))
ds = [e for e in load_dataset('princeton-nlp/SWE-bench_Verified', split='test') if e['instance_id'] in ids]
imgs = set(subprocess.run(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'], capture_output=True, text=True).stdout.split())
ok = miss = err = 0
for e in ds:
    try:
        ts = make_test_spec(e)
    except Exception as x:
        err += 1; print('ERR', e['instance_id'], type(x).__name__, str(x)[:120]); continue
    key = ts.instance_image_key
    if key in imgs or key + ':latest' in imgs: ok += 1
    else: miss += 1; print('MISSING image', key)
print(f'{len(ds)} instances: specs ok, image present {ok}, image missing {miss}, spec errors {err}')

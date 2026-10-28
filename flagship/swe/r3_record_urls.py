"""List the raw.githubusercontent.com URLs that swebench's test-spec code requests for given instances (run on the SWE
machine, which has no internet egress): requests.get is replaced by a recorder that answers 404, and make_test_spec is
called for each instance. Usage: r3_record_urls.py INSTANCES_JSON OUT_JSON"""
import json, sys
import requests
seen = []
class R:
    status_code = 404; text = ''; ok = False
def rec(url, *a, **kw):
    seen.append(url); return R()
requests.get = rec
from datasets import load_dataset
from swebench.harness.test_spec import make_test_spec
ids = set(json.load(open(sys.argv[1])))
ds = [e for e in load_dataset('princeton-nlp/SWE-bench_Verified', split='test') if e['instance_id'] in ids]
err = {}
for e in ds:
    try:
        make_test_spec(e)
    except Exception as x:
        err[e['instance_id']] = type(x).__name__
urls = sorted(set(seen))
json.dump({'urls': urls, 'errors': err, 'n': len(ds)}, open(sys.argv[2], 'w'), indent=1)
print(len(ds), 'instances;', len(urls), 'urls;', len(err), 'instances raised (expected where every path answered 404)')

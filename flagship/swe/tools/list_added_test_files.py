"""Fresh/pilot instances whose hidden test_patch ADDS files, with repo and test command family."""
import json, os, re
from datasets import load_dataset
F = os.path.expanduser('~/shi_eval/flagship')
fresh = set(json.load(open(f'{F}/swe/fresh_300.json'))); pilot = set(json.load(open(f'{F}/swe/pilot20.json')))
from swebench.harness.constants import MAP_REPO_VERSION_TO_SPECS
for e in load_dataset('princeton-nlp/SWE-bench_Verified')['test']:
    if e['instance_id'] not in fresh: continue
    added = re.findall(r'^--- /dev/null\n\+\+\+ b/(\S+)', e['test_patch'], re.M)
    cmd = MAP_REPO_VERSION_TO_SPECS[e['repo']][e['version']]['test_cmd']
    if added or (e['instance_id'] in pilot and 'pytest' in cmd):
        print(e['instance_id'], 'PILOT' if e['instance_id'] in pilot else '-', repr(cmd[:40]), added[:3], len(json.loads(e['FAIL_TO_PASS'])))

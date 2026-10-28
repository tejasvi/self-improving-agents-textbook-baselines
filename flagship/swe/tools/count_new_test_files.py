"""Count SWE-bench Verified instances whose test_patch ADDS files (they are not reset by the eval script's
'git checkout <base> <modified test files>', so DGM's in-container setup run leaves them in /testbed)."""
import json, os, re
from datasets import load_dataset
F = os.path.expanduser('~/shi_eval/flagship')
fresh = set(json.load(open(f'{F}/swe/fresh_300.json')))
ds = load_dataset('princeton-nlp/SWE-bench_Verified')['test']
def added(tp):
    return re.findall(r'^--- /dev/null\n\+\+\+ b/(\S+)', tp, re.M)
tot = {'fresh': [0, 0], 'dgm200': [0, 0]}
ex = []
for e in ds:
    k = 'fresh' if e['instance_id'] in fresh else 'dgm200'
    a = added(e['test_patch']); tot[k][0] += 1; tot[k][1] += bool(a)
    if a and len(ex) < 5: ex.append((e['instance_id'], a[:2]))
print({k: f'{v[1]}/{v[0]} instances add test files' for k, v in tot.items()})
for x in ex: print(' ', x)

"""List SWE-bench Verified instances outside DGM's subsets (small/medium/big = 200), grouped by repo and difficulty."""
import json, os, sys, collections
from datasets import load_dataset
F = os.path.expanduser('~/shi_eval/flagship')
sub = set()
for n in ('small', 'medium', 'big'):
    sub |= set(json.load(open(f'{F}/dgm_repo/swe_bench/subsets/{n}.json')))
ds = load_dataset('princeton-nlp/SWE-bench_Verified')['test']
fresh = [e for e in ds if e['instance_id'] not in sub]
print('verified', len(ds), 'dgm subsets', len(sub), 'in verified', len(sub & {e['instance_id'] for e in ds}), 'fresh', len(fresh))
c = collections.Counter((e['repo'], e['difficulty']) for e in fresh)
for k, v in sorted(c.items()): print(' ', k, v)
out = os.path.join(F, 'swe', 'fresh_300.json')
json.dump(sorted(e['instance_id'] for e in fresh), open(out, 'w'), indent=0)
print('wrote', out)
for repo in sys.argv[1:]:
    for e in fresh:
        if e['repo'] == repo and e['difficulty'] == '<15 min fix':
            print(repo, e['instance_id'], e['version'], len(json.loads(e['FAIL_TO_PASS'])), len(json.loads(e['PASS_TO_PASS'])), len(e['problem_statement']))

"""After gold validation: keep only instances the gold patch resolves (decision 2026-10-24: exclude the rest for every agent).
Writes swe/{fresh_gold,dgm60_gold,pilot20_gold}.json and prints the excluded ids per list."""
import json, os
F = os.path.expanduser('~/shi_eval/flagship'); S = f'{F}/swe'
g = json.load(open(f'{F}/runs/gold_validation/gold_validation.json'))['instances']
ok = {i for i, v in g.items() if v['resolved']}
for src, dst in (('fresh_built', 'fresh_gold'), ('dgm60_built', 'dgm60_gold'), ('pilot20', 'pilot20_gold')):
    ids = json.load(open(f'{S}/{src}.json')); keep = [i for i in ids if i in ok]
    json.dump(keep, open(f'{S}/{dst}.json', 'w'), indent=0)
    print(f'{dst}: {len(keep)}/{len(ids)} kept; excluded: {[i for i in ids if i not in ok]}')

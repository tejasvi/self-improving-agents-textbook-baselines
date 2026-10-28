"""After the prebuild: list instances excluded because their images do not build under stock swebench 2.1.0 (decision
2026-10-24: drop them, no change to swebench), with fresh / DGM-subset membership, and write the paired instance lists
that remain. Usage: $PY -I make_exclusions.py PREBUILD_DIR  -> swe/excluded_build_failures.json, fresh_built.json,
dgm60_built.json"""
import json, os, sys
F = os.path.expanduser('~/shi_eval/flagship'); S = f'{F}/dgm_repo/swe_bench/subsets'
fail = json.load(open(os.path.join(sys.argv[1], 'prebuild_failures.json')))
subset = {}
for n in ('small', 'medium', 'big'):
    for i in json.load(open(f'{S}/{n}.json')): subset[i] = f'dgm_{n}'
fresh = json.load(open(f'{F}/swe/fresh_300.json')); dgm60 = json.load(open(f'{F}/swe/dgm_selection_60.json'))
rows = []
for key, v in fail['env_failed'].items():
    for i in v['instances']:
        rows.append(dict(instance_id=i, repo=v['repo'], version=v['version'], set=subset.get(i, 'fresh'),
                         reason=f'env image {key} fails to build under stock swebench 2.1.0'))
for i, err in fail['instance_failed'].items():
    rows.append(dict(instance_id=i, set=subset.get(i, 'fresh'), reason=f'instance image fails to build: {err[:200]}'))
listed = {r['instance_id'] for r in rows}
for i in fail['missing_instance_images']:
    if i not in listed: rows.append(dict(instance_id=i, set=subset.get(i, 'fresh'), reason='instance image missing after prebuild'))
excl = {r['instance_id'] for r in rows}
json.dump(sorted(rows, key=lambda r: r['instance_id']), open(f'{F}/swe/excluded_build_failures.json', 'w'), indent=1)
json.dump([i for i in fresh if i not in excl], open(f'{F}/swe/fresh_built.json', 'w'), indent=0)
json.dump([i for i in dgm60 if i not in excl], open(f'{F}/swe/dgm60_built.json', 'w'), indent=0)
print(f'excluded {len(excl)}: ' + ', '.join(f"{r['instance_id']} ({r['set']})" for r in rows))
print(f'fresh_built {len([i for i in fresh if i not in excl])}, dgm60_built {len([i for i in dgm60 if i not in excl])}')

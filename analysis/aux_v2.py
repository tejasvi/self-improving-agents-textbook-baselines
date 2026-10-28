"""Auxiliary round-2 tables: empty-patch share per grid variant (results/grid_empty.json) and the output cap each
one-shot redesign chose (results/redesign_caps.json, read from the redesign's llm_withtools.py)."""
import collections, json, os, re
SHI = os.path.expanduser('~/shi_eval')
c = collections.defaultdict(lambda: [0, 0])
for l in open(os.path.join(SHI, 'results', 'F_grid.jsonl')):
    r = json.loads(l); c[r['agent']][0] += 1; c[r['agent']][1] += bool(r.get('empty'))
json.dump({a: round(100 * e / n, 1) for a, (n, e) in c.items()}, open(os.path.join(SHI, 'results', 'grid_empty.json'), 'w'), indent=1)
caps = {}
for t in ('opus', 'sonnet'):
    for i in range(5):
        src = open(os.path.join(SHI, 'harness', 'redesign', f'{t}_r{i}', 'llm_withtools.py')).read()
        consts = dict(re.findall(r'^([A-Z_]+)\s*=\s*(\d+)\s*$', src, re.M))
        vals = []
        for v in re.findall(r'max_tokens\s*=\s*([A-Za-z_0-9]+)', src):
            vals.append(int(v) if v.isdigit() else int(consts[v]) if v in consts else None)
        vals = [v for v in vals if v]
        caps[f'rd_{t}_r{i}'] = max(vals) if vals else None
caps.update({'rd_seed_dgm': 4096, 'rd_seed_dgm_cap16k': 16000, 'rd_seed_strong': 16000})
json.dump(caps, open(os.path.join(SHI, 'results', 'redesign_caps.json'), 'w'), indent=1)
print(json.dumps(caps))

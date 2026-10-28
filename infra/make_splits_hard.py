"""Hard-task pool (LCB difficulty=hard, private tests <= 20 MB): fixed shuffle -> small(10) / medium(40) / fresh(rest)."""
import json, random, os, collections
SHI = os.path.expanduser('~/shi_eval')
T = [json.loads(l) for l in open(os.path.join(SHI, 'data/lcb/index.jsonl'))]
pool = sorted([t['id'] for t in T if t['difficulty'] == 'hard' and t['private_bytes'] <= 20_000_000])
rng = random.Random(20261023 + 1)
rng.shuffle(pool)
sp = {'pool_rule': 'difficulty==hard and private_bytes<=2e7', 'seed': 20261024,
      'small': pool[:10], 'medium': pool[10:50], 'fresh': pool[50:]}
json.dump(sp, open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json'), 'w'), indent=0)
I = {t['id']: t for t in T}
for k in ('small', 'medium', 'fresh'):
    print(k, len(sp[k]), collections.Counter(I[x]['testtype'] for x in sp[k]), collections.Counter(I[x]['platform'] for x in sp[k]))

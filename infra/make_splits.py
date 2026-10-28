"""Fixed random splits of the LCB pool (private tests <= 5 MB): pilot / selection (staged) / fresh."""
import json, random, os, collections
SHI = os.path.expanduser('~/shi_eval')
T = [json.loads(l) for l in open(os.path.join(SHI, 'data/lcb/index.jsonl'))]
pool = sorted([t for t in T if t['private_bytes'] <= 5_000_000], key=lambda t: t['id'])
rng = random.Random(20261023)
by = collections.defaultdict(list)
for t in pool: by[t['difficulty']].append(t['id'])
for k in by: rng.shuffle(by[k])
# stratified pilot of 80, then the rest shuffled together
pilot = by['easy'][:27] + by['medium'][:27] + by['hard'][:26]
rest = by['easy'][27:] + by['medium'][27:] + by['hard'][26:]
rng.shuffle(rest)
splits = {'pool_rule': 'private_bytes<=5e6', 'seed': 20261023, 'pilot': pilot, 'rest': rest}
json.dump(splits, open(os.path.join(SHI, 'data/lcb/splits_v1.json'), 'w'), indent=0)
print(len(pool), len(pilot), len(rest))

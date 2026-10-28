"""Progress curves: best-so-far selection score by generation for loop arms; placebo vs order-statistics prediction.

Seed noise model: S-scores of the unchanged seed across all arms' 'initial' evaluations (same grader) give mean m and
sd s; a placebo archive of k full evaluations is predicted to show max ~ m + s * E[max of k iid N(0,1)].
"""
import json, os, sys, glob, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from collect import collect
SHI = os.path.expanduser('~/shi_eval')

def emax(k, sims=200000, rng=np.random.default_rng(0)):
    return float(rng.standard_normal((sims // max(1, k) + 1, k)).max(1).mean()) if k > 0 else 0.0

def seed_stats(prefix, strong):
    vals = []
    for d in glob.glob(os.path.join(SHI, 'exps', prefix + '*')):
        cfg = json.load(open(os.path.join(d, 'config.json')))
        if ('strong' in cfg['seed_dir']) != strong: continue
        _, _, recs = collect(os.path.basename(d))
        ini = next((r for r in recs if r['aid'] == 'initial' and r['sel_full']), None)
        if ini: vals.append(ini['sel'])
    return np.array(vals)

def curve(exp):
    cfg, st, recs = collect(exp)
    by = {r['aid']: r for r in recs}
    meta = [json.loads(l) for l in open(os.path.join(SHI, 'exps', exp, 'dgm_metadata.jsonl'))] if os.path.exists(os.path.join(SHI, 'exps', exp, 'dgm_metadata.jsonl')) else []
    best = by['initial']['sel'] if by.get('initial') else None; out = [(0, best, 'initial', 1)]
    nfull = 1
    for g in meta:
        for c in g['children_compiled']:
            r = by.get(c)
            if r and r['sel_full'] and c in g['archive']:
                nfull += 1
                if r['sel'] > best: best = r['sel']; out.append((g['generation'] + 1, best, c, nfull))
        out.append((g['generation'] + 1, best, None, nfull))
    return out

if __name__ == '__main__':
    prefix = sys.argv[1] if len(sys.argv) > 1 else 'v2_'
    for strong in (False, True):
        v = seed_stats(prefix, strong)
        if len(v) == 0: continue
        print(f"seed ({'strong' if strong else 'dgm'}) S over {len(v)} arms: mean={v.mean():.3f} sd={v.std(ddof=1):.3f} min={v.min():.2f} max={v.max():.2f}")
        for d in sorted(glob.glob(os.path.join(SHI, 'exps', prefix + '*'))):
            e = os.path.basename(d); cfg = json.load(open(os.path.join(d, 'config.json')))
            if ('strong' in cfg['seed_dir']) != strong or cfg['mode'] not in ('dgm', 'placebo') or 'C2' in e: continue
            c = curve(e)
            last = c[-1]
            pred = v.mean() + v.std(ddof=1) * emax(last[3])
            print(f"  {e:24} gens={last[0]:2} full_evals={last[3]:3} best_S={last[1]:.3f}  placebo-pred max={pred:.3f}  "
                  f"jumps={[(g, round(b, 2), a) for g, b, a, _ in c if a and a != 'initial']}")

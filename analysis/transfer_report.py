"""Cross-model transfer: each harness evaluated on F1 under other task models; paired gain vs the same model's seed.

Haiku 5.5 reference: seeds from F_seeds.v2 (3 reps), evolved agents from their fresh1 evals (1 rep).
"""
import json, os, sys, collections
import numpy as np
SHI = os.path.expanduser('~/shi_eval')
SP = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json'))); F1 = SP['fresh'][:116]
rng = np.random.default_rng(7)
AG = {'A3best': ('v2_A_dgm_s3', 'g010_1'), 'A1best': ('v2_A_dgm_s1', 'g002_1'), 'A2best': ('v2_A_dgm_s2', 'g003_0'),
      'C2best': ('v2_C2_single', 'g000_0'), 'E2best': ('v2_E_strong_dgm_s2', 'g004_0')}

def load(tag):
    d = collections.defaultdict(lambda: collections.defaultdict(list)); p = os.path.join(SHI, 'results', f'{tag}.jsonl')
    if not os.path.exists(p): return d
    for l in open(p):
        r = json.loads(l); d[r['agent']][r['task']].append(float(r['passed']))
    return d

def haiku55():
    d = collections.defaultdict(lambda: collections.defaultdict(list))
    for l in open(os.path.join(SHI, 'results', 'F_seeds.v2.jsonl')):
        r = json.loads(l); d[r['agent']][r['task']].append(float(r['passed']))
    for name, (e, a) in AG.items():
        p = os.path.join(SHI, 'exps', e, 'agents', a, 'evals', 'fresh1.jsonl')
        if os.path.exists(p):
            for l in open(p):
                r = json.loads(l); d[name][r['task']].append(float(r['passed']))
    return d

def gain(d, a, b):
    ts = [t for t in F1 if d[a].get(t) and d[b].get(t)]
    if len(ts) < 100: return None
    x = np.array([np.mean(d[a][t]) - np.mean(d[b][t]) for t in ts])
    bs = x[rng.integers(0, len(x), (4000, len(x)))].mean(1)
    return x.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5), len(ts)

if __name__ == '__main__':
    models = {'claude-haiku-5-5 (search model)': haiku55()}
    for m in ['claude-haiku-4-5', 'claude-sonnet-4-6', 'claude-sonnet-5-5', 'gemini-2.5-flash', 'openai_gpt-oss-120b-maas']:
        models[m] = load(f'X_{m}')
    for m, d in models.items():
        if not d: continue
        sd = np.mean([np.mean(d['seed_dgm'][t]) for t in F1 if d['seed_dgm'].get(t)]) if d.get('seed_dgm') else float('nan')
        ss = np.mean([np.mean(d['seed_strong'][t]) for t in F1 if d['seed_strong'].get(t)]) if d.get('seed_strong') else float('nan')
        line = f'{m:34} seed_dgm={sd:.3f} seed_strong={ss:.3f} |'
        for a in ['A3best', 'A1best', 'A2best', 'C2best']:
            g = gain(d, a, 'seed_dgm')
            if g: line += f' {a} {g[0]:+.3f} [{g[1]:+.3f},{g[2]:+.3f}];'
        g = gain(d, 'E2best', 'seed_strong')
        if g: line += f' E2best-vs-strong {g[0]:+.3f} [{g[1]:+.3f},{g[2]:+.3f}]'
        print(line)

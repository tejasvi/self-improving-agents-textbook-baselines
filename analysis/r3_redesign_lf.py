"""PREREG_v3 E3: one-shot redesigns without failure logs (opuslf_r0-4) against v2's log-based Opus redesigns
(opus_r0-4), one batch with the DGM seed (results/F_redesign_lf.jsonl; all 232 fresh problems, two runs each).
H15: (a) at least four of five log-free redesigns raise the output cap above 4,096; (b) mean fresh gain of the
log-free redesigns >= mean of the log-based ones - 3 points (paired bootstrap over problems, 10,000 resamples).
Exploratory: the redesigns that raise the cap, log-free vs log-based.
Writes results/r3_redesign_lf.json (unrounded)."""
import json, os, re, collections
import numpy as np
SHI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = collections.defaultdict(lambda: collections.defaultdict(list)); usd = collections.defaultdict(list)
for l in open(os.path.join(SHI, 'results', 'F_redesign_lf.jsonl')):
    r = json.loads(l); R[r['agent']][r['task']].append(float(r['passed'])); usd[r['agent']].append(r.get('usd') or 0)
T = sorted(set.intersection(*[set(v) for v in R.values()]))
def vec(a): return np.array([np.mean(R[a][t]) for t in T])
def boot(d, B=10000, seed=0):
    d = np.asarray(d, float); rng = np.random.default_rng(seed)
    ms = np.sort(d[rng.integers(0, len(d), size=(B, len(d)))].mean(1))
    return {'diff': 100 * float(d.mean()), 'lo': 100 * float(ms[int(.025 * B)]), 'hi': 100 * float(ms[int(.975 * B) - 1]), 'n': len(d)}
seed = vec('lf_seed_dgm')
lf = [f'lf_opuslf_r{i}' for i in range(5)]; lb = [f'lf_opus_r{i}' for i in range(5)]
out = {'n_tasks': len(T), 'agents': {}}
for a in ['lf_seed_dgm'] + lf + lb:
    if a not in R: continue
    v = vec(a); out['agents'][a] = {'F': 100 * float(v.mean()), 'usd_per_run': float(np.mean(usd[a])),
                                    'gain_vs_seed': boot(v - seed) if a != 'lf_seed_dgm' else None}
mlf = np.mean([vec(a) for a in lf], axis=0); mlb = np.mean([vec(a) for a in lb], axis=0)
out['mean_logfree_gain'] = boot(mlf - seed); out['mean_logbased_gain'] = boot(mlb - seed)
out['logfree_minus_logbased'] = boot(mlf - mlb)
caps = {}
for i in range(5):
    for tag in ('opuslf', 'opus'):
        p = os.path.join(SHI, 'harness', 'redesign', f'{tag}_r{i}', 'llm_withtools.py')
        s = open(p).read() if os.path.exists(p) else ''
        m = re.findall(r'max_tokens=([0-9_]+)', s)
        if not m:   # max_tokens=NAME with NAME = <number> defined in the file
            for name in re.findall(r'max_tokens=([A-Z][A-Z0-9_]*)', s):
                m = re.findall(rf'^\s*{name}\s*=\s*([0-9_]+)', s, re.M)
                if m: break
        caps[f'{tag}_r{i}'] = int(m[0].replace('_', '')) if m else None
out['caps'] = caps
out['H15a_logfree_raised'] = sum(1 for i in range(5) if (caps.get(f'opuslf_r{i}') or 0) > 4096)
out['H15a'] = out['H15a_logfree_raised'] >= 4
out['H15b'] = out['logfree_minus_logbased']['lo'] > -3
rl = [f'lf_opuslf_r{i}' for i in range(5) if (caps.get(f'opuslf_r{i}') or 0) > 4096]
rb = [f'lf_opus_r{i}' for i in range(5) if (caps.get(f'opus_r{i}') or 0) > 4096]
mrl = np.mean([vec(a) for a in rl], axis=0); mrb = np.mean([vec(a) for a in rb], axis=0)
out['exploratory_raisers'] = {'logfree': rl, 'logbased': rb, 'logfree_gain': boot(mrl - seed), 'logbased_gain': boot(mrb - seed),
                              'logfree_minus_logbased': boot(mrl - mrb)}
json.dump(out, open(os.path.join(SHI, 'results', 'r3_redesign_lf.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'agents'}, indent=1)[:1500])

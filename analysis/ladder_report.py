"""Gain ladder on fresh tasks (F1), DGM seed and strong seed, with paired bootstrap over tasks.

Seed fresh reference = seed's pass rate per task averaged over all its fresh reps (F_seeds.v2: 3 reps on F; loop arms
also re-evaluate the seed only on S). L1 = mean over prior-only single-step children, L2 = best-by-S of those,
L3/L4 the same for task-log single steps, L5 = DGM-loop best (per run), P = placebo best (zero by construction).
All children are compared on the same F1 tasks they were evaluated on (1 rep each).
"""
import json, os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from collect import collect, read_evals
SHI = os.path.expanduser('~/shi_eval')
SP = json.load(open(os.path.join(SHI, 'data/lcb/splits_hard_v1.json')))
F1 = SP['fresh'][:116]
rng = np.random.default_rng(12345)

def seed_ref(name):
    d = collections.defaultdict(list)
    for l in open(os.path.join(SHI, 'results', 'F_seeds.v2.jsonl')):
        r = json.loads(l)
        if r['agent'] == name: d[r['task']].append(float(r['passed']))
    return {t: np.mean(v) for t, v in d.items()}

def f1_vec(exp, aid):
    ev = read_evals(os.path.join(SHI, 'exps', exp, 'agents', aid), 'fresh1').get(0, {})
    if not all(t in ev for t in F1): return None
    return np.array([float(ev[t]['passed']) for t in F1])

def boot_mean_ci(mat, B=4000):
    """mat: (n_members, n_tasks) of gains; resample tasks and members."""
    mat = np.atleast_2d(mat); m, n = mat.shape
    est = mat.mean()
    bs = []
    for _ in range(B):
        ti = rng.integers(0, n, n); mi = rng.integers(0, m, m)
        bs.append(mat[np.ix_(mi, ti)].mean())
    return est, np.percentile(bs, 2.5), np.percentile(bs, 97.5)

def arm_members(exp):
    cfg, st, recs = collect(exp)
    out = []
    for r in recs:
        if r['aid'] == 'initial' or not r['compiled'] or not r['sel_full']: continue
        v = f1_vec(exp, r['aid'])
        if v is not None: out.append((r['aid'], r['sel'], v))
    return cfg, st, recs, out

def loop_best(recs):
    full = [r for r in recs if r['sel_full'] and r['compiled'] and (r['in_archive'] or r['aid'] == 'initial')]
    return max(full, key=lambda r: r['sel']) if full else None

def report(seedname, arms):
    ref = seed_ref(seedname); base = np.array([ref[t] for t in F1])
    print(f'\n=== {seedname}: seed F1 mean {base.mean():.3f}')
    for label, exps, kind in arms:
        mats = []; bests = []
        for e in exps:
            if not os.path.exists(os.path.join(SHI, 'exps', e)): continue
            cfg, st, recs, mem = arm_members(e)
            if kind in ('mean', 'best') and mem:
                if kind == 'mean': mats += [v - base for _, _, v in mem]
                else:
                    b = max(mem, key=lambda x: x[1]); bests.append((e, b[0], b[1], b[2] - base))
            if kind == 'loop':
                b = loop_best(recs)
                if b and b['aid'] != 'initial':
                    v = f1_vec(e, b['aid'])
                    bests.append((e, b['aid'], b['sel'], None if v is None else v - base))
        if kind == 'mean' and mats:
            est, lo, hi = boot_mean_ci(np.array(mats)); print(f'{label:34} n_members={len(mats):3}  F1 gain {est:+.3f} [{lo:+.3f}, {hi:+.3f}]')
        for e, a, s, g in bests:
            if g is None: print(f'{label:34} {e}:{a} S={s:.2f}  F1 pending'); continue
            est, lo, hi = boot_mean_ci(g[None, :]); print(f'{label:34} {e}:{a} S={s:.2f}  F1 gain {est:+.3f} [{lo:+.3f}, {hi:+.3f}]')

if __name__ == '__main__':
    report('seed_dgm', [('L1 prior-only single step (mean)', ['v2_C1_nolog'], 'mean'),
                        ('L2 prior-only best-of-n', ['v2_C1_nolog'], 'best'),
                        ('L3 task-log single step (mean)', ['v2_C2_single'], 'mean'),
                        ('L4 task-log best-of-n', ['v2_C2_single'], 'best'),
                        ('L3n log-only (no hint) single (mean)', ['v2_C3_nohint'], 'mean'),
                        ('L4n log-only (no hint) best-of-n', ['v2_C3_nohint'], 'best'),
                        ('L5n DGM loop without hints, best', ['v2_A_nohint_s1', 'v2_A_nohint_s2'], 'loop'),
                        ('D log-free chain (all members)', ['v2_D_chain1', 'v2_D_chain2'], 'mean'),
                        ('L5 DGM loop best', ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3'], 'loop'),
                        ('loop members (mean)', ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3'], 'mean')])
    report('seed_strong', [('L1 prior-only single step (mean)', ['v2_E_strong_C1_nolog'], 'mean'),
                           ('L2 prior-only best-of-n', ['v2_E_strong_C1_nolog'], 'best'),
                           ('L3 task-log single step (mean)', ['v2_E_strong_C2_single'], 'mean'),
                           ('L4 task-log best-of-n', ['v2_E_strong_C2_single'], 'best'),
                           ('L5 DGM loop best', ['v2_E_strong_dgm_s1', 'v2_E_strong_dgm_s2'], 'loop'),
                           ('loop members (mean)', ['v2_E_strong_dgm_s1', 'v2_E_strong_dgm_s2'], 'mean')])

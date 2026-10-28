"""Evaluator-quirk natural experiment: v1-grader arms (grade_driver.py shadowed builtin pow) re-graded with v2.

For each v1 arm: the seed's and every archive agent's selection score under v1 (what the loop saw) and under v2 (same saved
solutions, corrected grader); the v1-best agent's measured gain vs its corrected gain; rank agreement of the two graders.
Requires exp/regrade.py exp <arm> small medium to have produced evals/*.v2.jsonl.
"""
import json, os, glob, sys
import numpy as np
from scipy.stats import spearmanr
SHI = os.path.expanduser('~/shi_eval')

def sel(ad, suffix=''):
    d = {}
    for st in ('small', 'medium'):
        p = f'{ad}/evals/{st}{suffix}.jsonl'
        if os.path.exists(p):
            for l in open(p):
                r = json.loads(l)
                if r.get('rep', 0) == 0: d[r['task']] = r['passed']
    return d

if __name__ == '__main__':
    out = {}
    for e in sys.argv[1:] or ['E_strong_dgm_s1', 'E_strong_dgm_s2', 'A_dgm_s1', 'A_dgm_s2', 'B_placebo_s1']:
        st = json.load(open(f'{SHI}/exps/{e}/state.json'))
        rows = []
        for ad in glob.glob(f'{SHI}/exps/{e}/agents/*'):
            a = os.path.basename(ad); v1 = sel(ad); v2 = sel(ad, '.v2')
            if len(v1) == 50 and len(v2) == 50 and a in st['archive']:
                rows.append((a, np.mean(list(v1.values())), np.mean(list(v2.values()))))
        ini = [r for r in rows if r[0] == 'initial'][0]; best = max(rows, key=lambda r: r[1])
        rho = spearmanr([r[1] for r in rows], [r[2] for r in rows]).correlation
        out[e] = dict(gen=st['generation'], n_agents=len(rows), seed_v1=ini[1], seed_v2=ini[2], best_v1_agent=best[0],
                      best_v1=best[1], best_v1_under_v2=best[2], measured_gain=best[1] - ini[1],
                      corrected_gain=best[2] - ini[2], best_v2=max(r[2] for r in rows), spearman_v1_v2=rho)
        print(e, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in out[e].items()})
    json.dump(out, open(f'{SHI}/results/quirk.json', 'w'), indent=1)

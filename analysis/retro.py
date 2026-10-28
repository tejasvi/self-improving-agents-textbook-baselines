"""Retrospective audit of released self-improvement artifacts (no model calls).

DGM (Zhang et al., released Drive logs): selection-set vs non-selection performance of the reported best agent,
lineage of the gain, share of children per diagnosis type. ADAS (Hu et al., released archives): validation vs test
of the best-by-validation discovered agent, rank correlation across candidates.
"""
import json, os, re, sys, glob
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
from dgm_load import load_run
SHI = os.path.expanduser('~/shi_eval')
X = os.path.join(SHI, 'ext', 'dgm_drive', 'x')

def dgm_swe(run='swe_dgm'):
    gens, A = load_run(os.path.join(X, run))
    I = A['initial']; S = I['resolved'] | I['unresolved'] | I['empty']
    full = [a for a in A.values() if (a['n'] or 0) >= 190]
    best = max(full, key=lambda a: a['acc']) if full else max((a for a in A.values() if a['n']), key=lambda a: a['acc'])
    allt = best['resolved'] | best['unresolved'] | best['empty']
    sel = len(best['resolved'] & S) / len(allt & S); other = len(best['resolved'] - S) / max(1, len(allt - S))
    ini_sel = len(I['resolved'] & S) / len(S)
    # all 200-evaluated agents: selection vs other
    pairs = []
    for a in full:
        t = a['resolved'] | a['unresolved'] | a['empty']
        pairs.append((len(a['resolved'] & S) / len(t & S), len(a['resolved'] - S) / len(t - S)))
    return dict(run=run, best=best['run_id'], n_sel=len(allt & S), n_other=len(allt - S), best_sel=sel, best_other=other,
                init_sel=ini_sel, full_agents=len(full),
                mean_sel_of_full=float(np.mean([p[0] for p in pairs])) if pairs else None,
                mean_other_of_full=float(np.mean([p[1] for p in pairs])) if pairs else None)

def dgm_polyglot(run='polyglot_results/polyglot_dgm', paper_full=0.307):
    A = {os.path.basename(os.path.dirname(m)): json.load(open(m)) for m in glob.glob(os.path.join(X, run, '*', 'metadata.json'))}
    deep = set()
    for d in A.values():
        dp = d.get('overall_performance_deep')
        if dp: deep |= set(dp['total_resolved_ids']) | set(dp['total_unresolved_ids']) | set(dp['total_emptypatch_ids'])
    R = set(A['initial']['overall_performance']['total_resolved_ids'])
    deep_agents = [d for d in A.values() if d.get('overall_performance_deep')]
    best = max(deep_agents, key=lambda d: d['overall_performance_deep']['accuracy_score'])
    b50 = best['overall_performance_deep']['accuracy_score']
    full_solved = round(paper_full * 225); other = (full_solved - round(b50 * 50)) / 175
    return dict(run=run, deep_evaluated=len(deep_agents), parent_selection_tasks=10, best_sel50=b50, init_sel50=len(R & deep) / 50,
                init_other175=len(R - deep) / 175, best_other175_implied=other,
                sel_gain=b50 - len(R & deep) / 50, heldout_gain=other - len(R - deep) / 175)

def adas():
    def p(s):
        m = re.search(r'\(([-\d.]+)%, ([-\d.]+)%\), Median: ([-\d.]+)%', s or '')
        return float(m.group(3)) if m else None
    out = []
    for f in ['drop', 'mgsm', 'mmlu', 'gpqa', 'arc']:
        d = json.load(open(os.path.join(SHI, 'ext', 'adas', f + '_gpt3.5_results.json')))
        rows = [(e['generation'], e['name'], p(e.get('fitness')), p(e.get('test_fitness'))) for e in d]
        rows = [r for r in rows if r[2] is not None and r[3] is not None]
        gen = [r for r in rows if r[0] != 'initial']; base = [r for r in rows if r[0] == 'initial']
        bg = max(gen, key=lambda r: r[2]); bb = max(base, key=lambda r: r[2])
        out.append(dict(domain=f, n_candidates=len(gen), best_val=bg[2], best_test=bg[3], inflation=bg[2] - bg[3],
                        spearman_val_test=float(stats.spearmanr([r[2] for r in gen], [r[3] for r in gen]).correlation),
                        test_gain_vs_best_val_baseline=bg[3] - bb[3], test_gain_vs_best_test_baseline=bg[3] - max(r[3] for r in base)))
    return out

if __name__ == '__main__':
    res = {'dgm_swe': dgm_swe(), 'dgm_swe_noselfimprove': None, 'dgm_polyglot': dgm_polyglot(), 'adas': adas()}
    print(json.dumps(res, indent=1, default=float))
    json.dump(res, open(os.path.join(SHI, 'results', 'retro.json'), 'w'), indent=1, default=float)

"""ADAS P4 final table: per domain and agent, test score with a 95% bootstrap CI, calls and $ per question; paired
differences a - matched CoT-SC, a - cot, d - matched CoT-SC (and a - cotsc5, the analog of ADAS's reported gain) with
95% paired bootstrap CIs over questions (GPQA: clusters = the 5 repeats of a question); next to them the gains ADAS's
archive reports with gpt-3.5 on test (test medians). Scores in % (DROP: F1 0-100).
Usage: python -I final_table.py [RUN_DIR] [SUFFIX]   (defaults: adas_p4/full, -full); also writes RUN_DIR/final_table.json
"""
import json, os, re, sys
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.expanduser('~/shi_eval/adas_p4'))
import adas_port as P
import run_eval as R

B = 10000
GPQA_Q = 166   # ADAS GPQA test list = questions[32:] * 5, so item idx belongs to question idx % 166
FULL = {'mgsm': 800, 'drop': 800, 'gpqa': 830, 'mmlu': 800}
NAMES = {'best_val': 'a (best val)', 'best_test': 'd (best test)', 'cot': 'cot', 'cotsc5': 'cotsc5 (archive)'}


def load(run_dir, dom, label):
    p = os.path.join(run_dir, f'{dom}__{label}.jsonl')
    return {r['idx']: r for r in map(json.loads, open(p))} if os.path.exists(p) else None


def scale(dom, s):
    return s if dom == 'drop' else 100.0 * s


def boot(vals, clusters, seed):
    """Mean and 95% percentile bootstrap CI, resampling clusters (one cluster per item when clusters is None)."""
    vals = np.asarray(vals, float)
    if clusters is None: clusters = np.arange(len(vals))
    ids, inv = np.unique(np.asarray(clusters), return_inverse=True)
    sums = np.bincount(inv, weights=vals, minlength=len(ids)); cnts = np.bincount(inv, minlength=len(ids)).astype(float)
    pick = np.random.default_rng(seed).integers(0, len(ids), size=(B, len(ids)))
    means = sums[pick].sum(1) / cnts[pick].sum(1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(vals.mean()), float(lo), float(hi), len(ids)


def clusters_for(dom, idxs):
    return [i % GPQA_Q for i in idxs] if dom == 'gpqa' else None


def main():
    run_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/shi_eval/adas_p4/full')
    sfx = sys.argv[2] if len(sys.argv) > 2 else '-full'
    out = {'run_dir': run_dir, 'bootstrap_resamples': B, 'domains': {}}
    for dom in P.DOMAINS:
        a = load(run_dir, dom, 'best_val' + sfx)
        if a is None:
            print(f'\n== {dom}: no best_val results yet'); continue
        mean_calls = sum(r['calls'] for r in a.values()) / len(a)
        n_match = int(np.floor(mean_calls + 0.5))
        labels = {'best_val': 'best_val', 'matched': f'cotsc{n_match}', 'cot': 'cot', 'cotsc5': 'cotsc5', 'best_test': 'best_test'}
        pk, A = R.picks(dom)
        same_d = pk['best_test'] == pk['best_val']
        recs = {k: (a if k == 'best_val' else (a if (k == 'best_test' and same_d) else load(run_dir, dom, v + sfx)))
                for k, v in labels.items()}
        if dom == 'gpqa':   # repeats of a question share the gold answer
            for k, rs in recs.items():
                if rs:
                    g = {}
                    for i, r in rs.items(): assert g.setdefault(i % GPQA_Q, r['gold']) == r['gold'], 'GPQA cluster mismatch'
        D = out['domains'][dom] = {'n_items_full': FULL[dom], 'matched_N': n_match,
                                   'best_val_mean_calls': round(mean_calls, 3), 'agents': {}, 'paired': {}, 'archive_gpt35_test': {}}
        print(f'\n== {dom}: matched CoT-SC N = round({mean_calls:.3f}) = {n_match}'
              + ('; d is the same archive entry as a' if same_d else ''))
        print(f'{"agent":<22}{"arch":>5}{"n":>5}{"score %":>9}{"95% CI":>16}{"calls/q":>9}{"$/q":>9}{"fail":>6}{"err":>5}{">4096":>7}')
        for k, rs in recs.items():
            lab = labels[k] + ('' if k != 'matched' else ' (matched)')
            if k == 'best_test' and same_d:
                print(f'{NAMES[k]:<22} = a'); continue
            if k == 'cotsc5' and labels['matched'] == 'cotsc5':
                print(f'{NAMES[k]:<22} = matched (N=5)'); continue
            if not rs:
                print(f'{lab:<22} missing'); continue
            idxs = sorted(rs)
            m, lo, hi, nq = boot([scale(dom, rs[i]['score']) for i in idxs], clusters_for(dom, idxs), seed=1)
            calls = np.mean([rs[i]['calls'] for i in idxs]); usd = np.mean([rs[i]['usd_proxy'] for i in idxs])
            fail = sum(1 for i in idxs for c in rs[i]['call_log'] if c.get('parse') in ('fail', 'api_error', 'proxy_stop'))
            err = sum(1 for i in idxs if rs[i]['agent_error']); over = sum(c.get('over4096', 0) for i in idxs for c in rs[i]['call_log'])
            arch = pk.get(k, pk['cotsc5'] if k == 'matched' else '')
            name = NAMES.get(k, lab)
            print(f'{name:<22}{arch:>5}{len(idxs):>5}{m:>9.2f}  [{lo:6.2f},{hi:6.2f}]{calls:>9.2f}{usd:>9.5f}{fail:>6}{err:>5}{over:>7}')
            D['agents'][k] = {'label': labels[k], 'archive_index': arch, 'n': len(idxs), 'n_clusters': nq, 'score': m,
                              'ci95': [lo, hi], 'calls_per_q': float(calls), 'usd_per_q': float(usd), 'usd_total': float(usd * len(idxs)),
                              'parse_fail_calls': fail, 'agent_errors': err, 'calls_over_4096': over}
        nclu = len({i % GPQA_Q for i in a}) if dom == 'gpqa' else len(a)
        print(f'paired differences (points; 95% paired bootstrap CI, {B} resamples of '
              + (f'{nclu} GPQA questions with their repeats)' if dom == 'gpqa' else f'{nclu} questions)'))
        for name, x, y in (('a - matched CoT-SC', 'best_val', 'matched'), ('a - cot', 'best_val', 'cot'),
                           ('d - matched CoT-SC', 'best_test', 'matched'), ('a - cotsc5 (archive N=5)', 'best_val', 'cotsc5')):
            rx, ry = recs.get(x), recs.get(y)
            if not rx or not ry:
                print(f'  {name:<26} missing'); continue
            common = sorted(set(rx) & set(ry))
            diff = [scale(dom, rx[i]['score']) - scale(dom, ry[i]['score']) for i in common]
            m, lo, hi, nq = boot(diff, clusters_for(dom, common), seed=2)
            better = sum(1 for d in diff if d > 0); worse = sum(1 for d in diff if d < 0)
            print(f'  {name:<26}{m:+8.2f}  [{lo:+6.2f},{hi:+6.2f}]   n={len(common)}  (x better {better}, worse {worse})'
                  + ('   [d = a]' if x == 'best_test' and same_d else ''))
            D['paired'][name] = {'diff': m, 'ci95': [lo, hi], 'n': len(common), 'n_clusters': nq, 'x_better': better, 'x_worse': worse}
        ta, tsc, tcot = (P.median(A[pk[k]]['test_fitness']) for k in ('best_val', 'cotsc5', 'cot'))
        print(f'archive (gpt-3.5, test medians): a {ta:.1f}, CoT-SC {tsc:.1f}, CoT {tcot:.1f} -> '
              f'gain a - CoT-SC {ta - tsc:+.1f}, a - CoT {ta - tcot:+.1f}')
        D['archive_gpt35_test'] = {'a': ta, 'cotsc5': tsc, 'cot': tcot, 'gain_a_minus_cotsc': ta - tsc, 'gain_a_minus_cot': ta - tcot}
        have = [recs[k] for k in ('best_val', 'matched', 'cot', 'cotsc5', 'best_test') if recs.get(k)]
        common = sorted(set.intersection(*[set(r) for r in have]))
        top = 100.0 if dom == 'drop' else 1.0
        allc = sum(1 for i in common if all(r[i]['score'] >= top for r in have))
        D['all_agents_full_score_share'] = allc / max(len(common), 1)
        print(f'observation (7b, ceiling): every agent scored full marks on {allc}/{len(common)} items ({100 * allc / max(len(common), 1):.1f}%)')
        if dom == 'drop':
            offs = {}
            for f in ('fitness', 'test_fitness'):
                o = []
                for e in A:
                    lo_, hi_, md = map(float, re.search(r'\(([\-0-9.]+)%, ([\-0-9.]+)%\), Median: ([\-0-9.]+)%', e[f]).groups())
                    o.append(md - hi_)
                offs[f] = (sum(1 for v in o if v > 0), len(o), min(o), float(np.median(o)), max(o))
            D['archive_median_above_ci'] = offs
            print(f'observation (7c): DROP archive medians lie above their own 95% CI upper bound in {offs["fitness"][0]}/{offs["fitness"][1]} '
                  f'validation (by {offs["fitness"][2]:.1f}-{offs["fitness"][4]:.1f}, median {offs["fitness"][3]:.1f} points) and '
                  f'{offs["test_fitness"][0]}/{offs["test_fitness"][1]} test entries (by {offs["test_fitness"][2]:.1f}-{offs["test_fitness"][4]:.1f}, '
                  f'median {offs["test_fitness"][3]:.1f}); the archive gains above use those medians')
    tot = sum(ag['usd_total'] for d in out['domains'].values() for ag in d['agents'].values())
    out['usd_total_agents'] = tot
    print(f'\nmodel spend in these results (proxy, per-question tags): ${tot:.2f}')
    json.dump(out, open(os.path.join(run_dir, 'final_table.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()

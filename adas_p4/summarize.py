"""Table for an ADAS P4 run directory (default: adas_p4/pilot): per domain x agent accuracy, calls/q, $/q, parse
counts, plus the projected cost of the full test sets. Usage: python -I summarize.py [RUN_DIR]"""
import glob, json, os, re, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.expanduser('~/shi_eval/adas_p4'))

FULL = {'mgsm': 800, 'drop': 800, 'gpqa': 830, 'mmlu': 800}   # ADAS test sets (GPQA: 166 questions x 5 repeats)
ORDER = ['best_val', 'cotsc', 'cot', 'cotsc5', 'best_test']


def key(agent):
    base = 'cotsc' if re.fullmatch(r'cotsc\d+', agent) and agent != 'cotsc5' else agent
    return ORDER.index(base) if base in ORDER else 99


def ci_anomalies(domain):
    """Archive entries whose reported median lies outside their own 95% CI (validation, test)."""
    import adas_port as P
    bad = {'fitness': 0, 'test_fitness': 0}
    A = P.archive(domain)
    for e in A:
        for f in bad:
            m = re.search(r'\(([\-0-9.]+)%, ([\-0-9.]+)%\), Median: ([\-0-9.]+)%', e.get(f) or '')
            if m and not float(m.group(1)) <= float(m.group(3)) <= float(m.group(2)): bad[f] += 1
    return bad, len(A)


def main():
    run_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/shi_eval/adas_p4/pilot')
    rows = []
    for p in sorted(glob.glob(os.path.join(run_dir, '*.summary.json'))):
        s = json.load(open(p))
        rows.append(s)
    total_proj = 0.0; total_spent = 0.0
    for dom in FULL:
        R = sorted([r for r in rows if r['domain'] == dom], key=lambda r: key(r['agent']))
        if not R: continue
        bad, n_arch = ci_anomalies(dom)
        print(f'\n== {dom}  (full test {FULL[dom]} items; archive {n_arch} entries, median outside own CI: '
              f'val {bad["fitness"]}, test {bad["test_fitness"]})')
        print(f'{"agent":<12}{"arch":>5}{"val/test(gpt3.5)":>18}{"n":>4}{"score":>8}{"calls/q":>9}{"$/q":>10}'
              f'{"$full":>8}{"fail":>6}{"nonJSON":>8}{"coerce":>7}{">4096":>6}{"err":>5}')
        dom_proj = 0.0
        for r in R:
            m = r['meta']
            if 'same_as' in m:
                print(f'{r["agent"]:<12} same code as {m["same_as"]} (not re-run)'); continue
            pr = r['parse']; ncalls = sum(pr.values())
            nonjson = sum(v for k, v in pr.items() if k in ('pyliteral', 'keyed'))
            vt = f'{m.get("val_median", "")}/{m.get("test_median", "")}' if 'val_median' in m else f'N={m.get("N")}'
            proj = r['usd_per_q'] * FULL[dom]; dom_proj += proj; total_spent += r['usd_proxy']
            print(f'{r["agent"]:<12}{m["archive_index"]:>5}{vt:>18}{r["n"]:>4}{r["score_mean"]:>8.3f}{r["calls_mean"]:>9.2f}'
                  f'{r["usd_per_q"]:>10.5f}{proj:>8.2f}{pr.get("fail", 0) + pr.get("api_error", 0):>6}{nonjson:>8}'
                  f'{sum(r["coerced"].values()):>7}{r.get("over4096", 0):>6}{r["agent_errors"]:>5}'
                  + (f'   [{ncalls} calls; parse {pr}]'))
        total_proj += dom_proj
        print(f'   projected full-test cost, all agents above: ${dom_proj:.2f}')
        # paired best_val vs matched CoT-SC on the same items
        A = {r['agent']: r for r in R}
        if 'best_val' in A and 'calls_mean' in A['best_val']:
            cand = f'cotsc{int(A["best_val"]["calls_mean"] + 0.5)}'   # run_eval's cotscN label (round half up)
            if os.path.exists(os.path.join(run_dir, f'{dom}__{cand}.jsonl')):
                sa = {json.loads(l)['idx']: json.loads(l)['score'] for l in open(os.path.join(run_dir, f'{dom}__best_val.jsonl'))}
                sb = {json.loads(l)['idx']: json.loads(l)['score'] for l in open(os.path.join(run_dir, f'{dom}__{cand}.jsonl'))}
                common = sorted(set(sa) & set(sb))
                d = sum(sa[i] - sb[i] for i in common) / max(len(common), 1)
                print(f'   paired best_val - {cand} on {len(common)} items: {d:+.3f} '
                      f'(best_val better {sum(sa[i] > sb[i] for i in common)}, worse {sum(sa[i] < sb[i] for i in common)})')
    print(f'\nspent in this run dir (proxy, per-question tags): ${total_spent:.3f}; projected full test sets: ${total_proj:.2f}')


if __name__ == '__main__':
    main()

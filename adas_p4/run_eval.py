"""Evaluate ADAS agents on one domain's test set with claude-haiku-5-5 (port: adas_port.py).

Agents: best_val = non-initial archive entry with the highest validation median (ties: first in archive order);
best_test = same on test_fitness (sensitivity only, never used for selection); cot / cotsc5 = the archive's initial
'Chain-of-Thought' / 'Self-Consistency with Chain-of-Thought' entries; cotsc<k> = that CoT-SC code with N = k;
cotscN = cotsc<k> with k = mean calls per question of best_val in --out-dir, rounded half up (DROP's archive CoT-SC
adds one final-decision call after its k samples).
Usage: python -I run_eval.py --domain mgsm --agents best_val,cot,cotsc5,best_test,cotscN --limit 20 --out-dir DIR
"""
import argparse, json, math, os, sys, threading, time, urllib.parse
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.expanduser('~/shi_eval/adas_p4'))
import adas_port as P

SC_LINE = 'N = 5 # Number of CoT agents'


def picks(domain):
    A = P.archive(domain)
    disc = [i for i, e in enumerate(A) if e['generation'] != 'initial']
    init = {e['name']: i for i, e in enumerate(A) if e['generation'] == 'initial'}
    return {'best_val': max(disc, key=lambda i: P.median(A[i]['fitness'])),
            'best_test': max(disc, key=lambda i: P.median(A[i]['test_fitness'])),
            'cot': init['Chain-of-Thought'], 'cotsc5': init['Self-Consistency with Chain-of-Thought']}, A


def read_jsonl(path):
    return [json.loads(l) for l in open(path)]


def resolve(domain, agent, out_dir, suffix=''):
    """(label, code, meta) for an agent name; label (+ suffix) is used in run tags and file names."""
    pk, A = picks(domain)
    if agent in pk:
        i = pk[agent]; e = A[i]
        meta = {'archive_index': i, 'name': e['name'], 'generation': e['generation'],
                'val_median': P.median(e['fitness']), 'test_median': P.median(e['test_fitness'])}
        if agent == 'best_test' and i == pk['best_val']: meta['same_as'] = 'best_val'
        return agent + suffix, e['code'], meta
    if agent.startswith('cotsc'):
        k = agent[5:]
        if k == 'N':
            recs = read_jsonl(os.path.join(out_dir, f'{domain}__best_val{suffix}.jsonl'))
            mean_calls = sum(r['calls'] for r in recs) / len(recs)
            k = int(math.floor(mean_calls + 0.5))
            meta_n = {'matched_to': 'best_val', 'best_val_mean_calls': round(mean_calls, 3), 'best_val_n': len(recs)}
        else:
            k = int(k); meta_n = {}
        code = A[pk['cotsc5']]['code']
        assert code.count(SC_LINE) == 1, 'CoT-SC template line not found exactly once'
        meta = {'archive_index': pk['cotsc5'], 'name': f'CoT-SC N={k} (archive CoT-SC code, N replaced)', 'N': k, **meta_n}
        if k == 5: meta['same_as'] = 'cotsc5'
        return f'cotsc{k}{suffix}', code.replace(SC_LINE, f'N = {k} # Number of CoT agents'), meta
    raise SystemExit(f'unknown agent {agent}')


def prefix_spend(tries=5):
    """All 'adas_p4|' spend. Retried: the proxy's /prefix handler iterates its run table unlocked and sometimes dies
    with 'dictionary changed size during iteration' (infra/llm_proxy.py do_GET)."""
    for k in range(tries):
        try:
            return P.run_task.spent(prefix=urllib.parse.quote('adas_p4|'))['usd']
        except Exception:
            if k == tries - 1: raise
            time.sleep(2)


def spend_guard(cap, interval=30):
    """Daemon thread: once all 'adas_p4|' spend reaches `cap`, start no new questions (P.STOP)."""
    def loop():
        while not P.STOP.is_set():
            try:
                usd = prefix_spend()
                if usd >= cap:
                    print(f'spend guard: adas_p4 spend ${usd:.2f} >= ${cap}; no new questions', flush=True); P.STOP.set()
            except Exception as e:
                print(f'spend guard: {e}', flush=True)
            time.sleep(interval)
    threading.Thread(target=loop, daemon=True).start()


def summarize(recs):
    n = len(recs)
    parse, coerced, stops = {}, {}, {}
    for r in recs:
        for c in r['call_log']:
            parse[c.get('parse', 'none')] = parse.get(c.get('parse', 'none'), 0) + 1
            stops[str(c.get('stop'))] = stops.get(str(c.get('stop')), 0) + 1
            for t in c.get('coerced', []): coerced[t] = coerced.get(t, 0) + 1
    calls = [r['calls'] for r in recs]
    return {'n': n, 'score_mean': round(sum(r['score'] for r in recs) / n, 4) if n else None,
            'calls_mean': round(sum(calls) / n, 3) if n else None, 'calls_min': min(calls, default=None),
            'calls_max': max(calls, default=None), 'usd_proxy': round(sum(r['usd_proxy'] for r in recs), 5),
            'usd_local': round(sum(r['usd_local'] for r in recs), 5),
            'usd_per_q': round(sum(r['usd_proxy'] for r in recs) / n, 6) if n else None,
            'agent_errors': sum(1 for r in recs if r['agent_error']), 'task_mismatch': sum(1 for r in recs if not r['task_ok']),
            'parse': parse, 'coerced': coerced, 'stop': stops,
            'reordered': sum(c.get('reordered', 0) for r in recs for c in r['call_log']),
            'over4096': sum(c.get('over4096', 0) for r in recs for c in r['call_log']),
            'odd_keys': sum(1 for r in recs for c in r['call_log'] if 'keys' in c),
            'calls_mismatch_proxy': sum(1 for r in recs if r['calls'] != r['calls_proxy']),
            'wall_mean': round(sum(r['wall'] for r in recs) / n, 1) if n else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--domain', required=True, choices=P.DOMAINS)
    ap.add_argument('--agents', required=True)
    ap.add_argument('--limit', type=int, default=None, help='first K test items only (pilot)')
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--workers', type=int, default=10, help="ADAS's --max_workers (questions in flight)")
    ap.add_argument('--suffix', default='', help='appended to agent labels (run tags, file names), e.g. -smoke')
    ap.add_argument('--max-usd', type=float, default=14.0, help="stop before an agent once all 'adas_p4|' spend exceeds this")
    a = ap.parse_args()
    out_dir = os.path.abspath(a.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    S, U = P.load_domain(a.domain)   # chdir to the ADAS repo: only absolute paths below
    args = P.adas_args(a.domain, max_workers=a.workers)
    items = P.test_items(U, a.domain, args)
    print(f'{a.domain}: {len(items)} test items; limit {a.limit}', flush=True)
    spend_guard(a.max_usd)
    for agent in a.agents.split(','):
        label, code, meta = resolve(a.domain, agent, out_dir, a.suffix)
        base = os.path.join(out_dir, f'{a.domain}__{label}')
        if 'same_as' in meta:
            print(f'{label}: same code as {meta["same_as"]}, not re-run', flush=True)
            json.dump({'domain': a.domain, 'agent': label, 'meta': meta}, open(base + '.summary.json', 'w'), indent=1)
            continue
        for ext in ('.jsonl', '.partial.jsonl'):
            if os.path.exists(base + ext): raise SystemExit(f'{base}{ext} exists; use a new --out-dir or label')
        if P.STOP.is_set(): raise SystemExit('stop flag set (proxy budget answer or spend guard); stopping')
        spent = prefix_spend()
        if spent > a.max_usd: raise SystemExit(f'adas_p4 spend ${spent:.2f} > --max-usd {a.max_usd}; stopping')
        open(base + '.code.py', 'w').write(code)
        t0 = time.time()
        recs = P.Evaluation(S, a.domain, label, items, a.limit, base + '.partial.jsonl').run(code, args)
        with open(base + '.jsonl', 'w') as f:
            for r in recs: f.write(json.dumps(r) + '\n')
        summ = {'domain': a.domain, 'agent': label, 'meta': meta, 'limit': a.limit, 'n_test_items': len(items),
                'elapsed_s': round(time.time() - t0, 1), **summarize(recs)}
        json.dump(summ, open(base + '.summary.json', 'w'), indent=1)
        print(json.dumps({k: summ[k] for k in ('agent', 'n', 'score_mean', 'calls_mean', 'usd_per_q', 'agent_errors',
                                                'task_mismatch', 'parse', 'coerced', 'stop', 'over4096', 'elapsed_s')}), flush=True)
    if P.STOP.is_set(): raise SystemExit('stop flag set (proxy budget answer or spend guard); results above may be partial')


if __name__ == '__main__':
    main()

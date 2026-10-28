"""Summarize a pilot results JSONL: pass rate by difficulty, empties, cost, wall, rep agreement."""
import json, sys, os, collections, statistics as S
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import lcb
I = lcb.index()
R = [json.loads(l) for l in open(sys.argv[1])]
print('n', len(R), 'errors', sum('error' in r for r in R))
by = collections.defaultdict(list)
for r in R: by[I[r['task']]['difficulty']].append(r)
for d in ('easy', 'medium', 'hard'):
    rs = by.get(d, [])
    if not rs: continue
    print(f"{d:6} n={len(rs):3} pass={sum(r['passed'] for r in rs)/len(rs):.2f} empty={sum(bool(r.get('empty')) for r in rs)/len(rs):.2f} "
          f"usd/run={S.mean(r.get('usd',0) for r in rs):.4f} wall_med={S.median(r.get('wall',0) for r in rs):.0f}s "
          f"wall_p90={sorted(r.get('wall',0) for r in rs)[int(.9*len(rs))]:.0f}s calls_med={S.median(r.get('calls',0) for r in rs)}")
print(f"overall pass={sum(r['passed'] for r in R)/len(R):.3f} total_usd={sum(r.get('usd',0) for r in R):.3f}")
p = collections.defaultdict(dict)
for r in R: p[r['task']][r['rep']] = r['passed']
both = [v for v in p.values() if len(v) == 2]
print('tasks with 2 reps', len(both), 'agree', sum(v[0] == v[1] for v in both),
      'pass-both', sum(v[0] and v[1] for v in both), 'fail-both', sum((not v[0]) and (not v[1]) for v in both))
print(collections.Counter(((r.get('grade') or {}).get('first_fail') or {}).get('kind') if not r['passed'] else 'pass' for r in R))
print('agent timeouts', sum(bool(r.get('agent_timed_out')) for r in R), 'rc!=0', sum(r.get('agent_rc', 0) != 0 for r in R))

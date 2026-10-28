"""One-line status per experiment: generation, archive, children, best S score, spend."""
import json, os, sys, glob
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import run_task
SHI = os.path.expanduser('~/shi_eval')

def perf(adir):
    R = U = E = 0
    for st in ('small', 'medium', 'big'):
        p = os.path.join(adir, 'evals', f'{st}.jsonl')
        if not os.path.exists(p): continue
        for l in open(p):
            r = json.loads(l)
            if r.get('rep', 0): continue
            if r['passed']: R += 1
            elif r.get('empty'): E += 1
            else: U += 1
    n = R + U + E
    return (R / n if n else 0.0), n, E

exps = sys.argv[1:] or sorted(os.listdir(os.path.join(SHI, 'exps')))
tot = 0.0
for e in exps:
    d = os.path.join(SHI, 'exps', e)
    if not os.path.isdir(d): continue
    st = json.load(open(os.path.join(d, 'state.json'))) if os.path.exists(os.path.join(d, 'state.json')) else {'generation': 0, 'archive': ['initial']}
    agents = [os.path.basename(a) for a in glob.glob(os.path.join(d, 'agents', '*'))]
    rows = []
    for a in agents:
        s, n, emp = perf(os.path.join(d, 'agents', a))
        if n: rows.append((n >= 50, s, n, emp, a))
    full = sorted([r for r in rows if r[0]], key=lambda r: -r[1])
    ini = next((r for r in rows if r[4] == 'initial'), None)
    m = [json.load(open(p)) for p in glob.glob(os.path.join(d, 'agents', 'g*', 'meta.json'))]
    failed = sum(1 for x in m if x.get('failed')); comp = sum(1 for x in m if x.get('compiled'))
    usd = run_task.spent(prefix=e + '|')['usd']; tot += usd
    best = full[0] if full else None
    print(f"{e:14} gen={st['generation']:2} arch={len(st['archive']):2} kids={len(m):2} comp={comp:2} fail={failed:2} "
          f"init={ini[1]:.2f}/{ini[2]}" if ini else f"{e:14} gen={st['generation']:2} init=NA", end='')
    if best: print(f" best={best[1]:.2f}({best[4]}) n_full={len(full)}", end='')
    print(f" ${usd:.2f}")
print(f"total ${tot:.2f}; proxy {run_task.spent()}")

"""Collect per-agent records across experiments: lineage, kind, S score (selection), fresh scores, cost."""
import json, os, glob, sys, collections
SHI = os.path.expanduser('~/shi_eval')

def read_evals(adir, stage):
    p = os.path.join(adir, 'evals', f'{stage}.jsonl')
    out = collections.defaultdict(dict)   # rep -> task -> result
    if os.path.exists(p):
        for l in open(p):
            r = json.loads(l); out[r.get('rep', 0)][r['task']] = r
    return out

def score(ev, tasks=None):
    """mean pass over tasks for each rep; returns (mean over reps, n_tasks, per-rep list)."""
    reps = []
    for rep, d in sorted(ev.items()):
        ts = tasks if tasks is not None else list(d)
        if tasks is not None and not all(t in d for t in ts): continue
        if ts: reps.append(sum(d[t]['passed'] for t in ts) / len(ts))
    return (sum(reps) / len(reps) if reps else None), (len(tasks) if tasks else (len(next(iter(ev.values()))) if ev else 0)), reps

def collect(exp):
    d = os.path.join(SHI, 'exps', exp)
    cfg = json.load(open(os.path.join(d, 'config.json')))
    S = cfg['splits']['small'] + cfg['splits']['medium']
    st = json.load(open(os.path.join(d, 'state.json'))) if os.path.exists(os.path.join(d, 'state.json')) else {'archive': ['initial'], 'generation': 0}
    recs = []
    for ad in sorted(glob.glob(os.path.join(d, 'agents', '*'))):
        aid = os.path.basename(ad)
        mp = os.path.join(ad, 'meta.json')
        if not os.path.exists(mp): continue
        m = json.load(open(mp))
        small = read_evals(ad, 'small'); med = read_evals(ad, 'medium')
        s0 = {**small.get(0, {}), **med.get(0, {})}
        sel_n = len(s0); sel = sum(r['passed'] for r in s0.values()) / sel_n if sel_n else None
        full = all(t in s0 for t in S)
        f1 = read_evals(ad, 'fresh1'); f2 = read_evals(ad, 'fresh2')
        rec = dict(exp=exp, aid=aid, parent=m.get('parent'), gen=m.get('gen'), mode=m.get('mode', 'seed'), kind=m.get('kind'),
                   entry=m.get('entry'), compiled=m.get('compiled', aid == 'initial'), failed=m.get('failed'),
                   in_archive=aid in st['archive'], patch_lines=m.get('patch_lines'),
                   sel=sel, sel_n=sel_n, sel_full=full,
                   sel_empty=sum(bool(r.get('empty')) for r in s0.values()),
                   sel_usd=sum(r.get('usd', 0) for r in s0.values()),
                   f1={rep: sum(r['passed'] for r in v.values()) / len(v) for rep, v in f1.items() if v},
                   f1_n={rep: len(v) for rep, v in f1.items()},
                   f2={rep: sum(r['passed'] for r in v.values()) / len(v) for rep, v in f2.items() if v},
                   f1_usd=sum(r.get('usd', 0) for v in f1.values() for r in v.values()) / max(1, sum(len(v) for v in f1.values())),
                   t0=m.get('t0'), t1=m.get('t1'))
        recs.append(rec)
    return cfg, st, recs

if __name__ == '__main__':
    for e in sys.argv[1:]:
        cfg, st, recs = collect(e)
        for r in recs:
            print(e, r['aid'], r['mode'], r['kind'], 'comp' if r['compiled'] else '-', f"sel={r['sel']}", r['sel_n'], 'f1=', r['f1'])

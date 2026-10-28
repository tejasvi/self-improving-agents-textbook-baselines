"""Non-iterative ladder arms built on dgm_lcb.Run.

single  : n children of the seed, each from one diagnosis (mode 'dgm' = DGM task-log diagnosis incl. its
          25% stochasticity / empty-patch prompts; mode 'nolog' = log-free diagnosis). Evaluated like loop children.
chain   : k sequential log-free steps; each compiled child is accepted without looking at its score.
"""
import os, sys, json, argparse, concurrent.futures as cf
sys.path.insert(0, os.path.expanduser('~/shi_eval/exp'))
import dgm_lcb

def single(exp, mode, n, par=4):
    R = dgm_lcb.Run(exp); R.ensure_initial()
    p = R.perf('initial')
    fails = p['total_emptypatch_ids'] + p['total_unresolved_ids'] or p['total_resolved_ids']
    entries = [R.rng.choice(fails) for _ in range(n)]
    with cf.ThreadPoolExecutor(par) as ex:
        list(ex.map(lambda i: R.attempt('initial', entries[i], 0, i, mode), range(n)))

def chain(exp, k):
    R = dgm_lcb.Run(exp); R.ensure_initial()
    cur = 'initial'
    for step in range(k):
        child = R.attempt(cur, None, step, 0, 'nolog')
        m = R.meta(child)
        if m.get('compiled'): cur = child
        with open(os.path.join(R.dir, 'chain.jsonl'), 'a') as f:
            f.write(json.dumps({'step': step, 'child': child, 'compiled': m.get('compiled'), 'accepted_parent_next': cur}) + '\n')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('kind', choices=['single', 'chain']); ap.add_argument('exp')
    ap.add_argument('--mode', default='dgm'); ap.add_argument('--n', type=int, default=24); ap.add_argument('--par', type=int, default=4)
    a = ap.parse_args()
    if a.kind == 'single': single(a.exp, a.mode, a.n, a.par)
    else: chain(a.exp, a.n)

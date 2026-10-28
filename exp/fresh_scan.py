"""Evaluate finished agents of an experiment on fresh tasks (incremental, resume-safe).

usage: fresh_scan.py EXP [EXP ...] --stage fresh1|fresh --which compiled|archive|initial --reps R --workers W
Results go to agents/<aid>/evals/<stage>.jsonl (rep index kept). Placebo children are skipped (identical code
to the seed); the seed 'initial' is always included.
"""
import os, sys, json, argparse, glob, concurrent.futures as cf
sys.path.insert(0, os.path.expanduser('~/shi_eval/exp'))
import dgm_lcb
from eval_agents import tasks_for

def targets(R, which, with_initial=False):
    st = R.state(); out = ['initial'] if with_initial else []
    for p in sorted(glob.glob(os.path.join(R.dir, 'agents', 'g*', 'meta.json'))):
        m = json.load(open(p))
        if not m.get('done') or m.get('mode') == 'placebo': continue
        if which == 'compiled' and m.get('compiled'): out.append(m['aid'])
        if which == 'archive' and m['aid'] in st['archive']: out.append(m['aid'])
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('exps', nargs='+')
    ap.add_argument('--stage', default='fresh1'); ap.add_argument('--which', default='compiled')
    ap.add_argument('--reps', type=int, default=1); ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--only', default=None, help='comma list of agent ids')
    ap.add_argument('--with-initial', action='store_true')
    a = ap.parse_args()
    T = tasks_for(a.stage)
    for e in a.exps:
        R = dgm_lcb.Run(e); R.pool = cf.ThreadPoolExecutor(a.workers)
        ags = a.only.split(',') if a.only else targets(R, a.which, a.with_initial)
        for aid in ags:
            for rep in range(a.reps):
                res = R.eval_tasks(aid, a.stage, T, rep=rep)
                print(e, aid, a.stage, rep, f'{sum(r["passed"] for r in res)}/{len(res)}', flush=True)

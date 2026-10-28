"""Improver-swap test (pre-registered secondary): does an evolved agent make better modifications than the seed?

The same problem statements (DGM diagnoses of the seed, taken from the C2 single-step arm) are implemented on a
fresh copy of the SEED's code by two editors: (a) the seed agent itself, (b) an evolved agent (loop best) used as
the editor. Children of both arms are evaluated like loop children (staged S) and later on F1.
"""
import os, sys, json, shutil, subprocess, argparse, concurrent.futures as cf
sys.path.insert(0, os.path.expanduser('~/shi_eval/exp'))
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import dgm_lcb, sandbox, run_task
import dgm_prompts as P
from dgm_lcb import git, copy_code

def edit_with(R, editor_code, child, ps):
    """Run editor_code's coding agent on a copy of the seed's code; return patch text."""
    work = os.path.join(R.adir(child), 'selfmod'); os.makedirs(work, exist_ok=True)
    repo = os.path.join(work, 'dgm'); copy_code(os.path.join(R.adir('initial'), 'code'), repo)
    with open(os.path.join(repo, '.gitignore'), 'a') as f: f.write('\nself_evo.md\nmodel_patch.diff\n__pycache__/\n')
    git(repo, 'init', '-q'); git(repo, 'add', '-A'); git(repo, 'commit', '-q', '-m', 'base')
    base = git(repo, 'rev-parse', 'HEAD').stdout.strip()
    tok = run_task.mint(f'{R.exp}|selfmod|{child}', R.cfg['selfmod_model'], R.cfg.get('selfmod_budget', 2.0))
    cmd = ['timeout', '1800', 'python3', '/editor/coding_agent.py', '--problem_statement', ps, '--git_dir', '/dgm/',
           '--chat_history_file', '/dgm/self_evo.md', '--base_commit', base, '--outdir', '/dgm/',
           '--test_description', P.test_description_dgm_repo, '--self_improve']
    r = sandbox.run(cmd, rw=[(repo, '/dgm')], ro=[(editor_code, '/editor')], sock=run_task.SOCK, cwd='/',
                    env={'ANTHROPIC_BASE_URL': 'http://127.0.0.1:8080', 'ANTHROPIC_API_KEY': tok}, timeout=1900, mem_gb=8)
    open(os.path.join(work, 'stderr.txt'), 'wb').write(r['err'][-200000:])
    pf = os.path.join(repo, 'model_patch.diff')
    if os.path.exists(pf): return open(pf, errors='replace').read()
    git(repo, 'add', '-A', check=False)
    return git(repo, 'diff', '--cached', base, check=False).stdout

def one(R, i, arm, editor_code, ps):
    child = f'{arm}_{i:02d}'
    if R.meta(child) and R.meta(child).get('done'): return child
    if os.path.exists(R.adir(child)): shutil.rmtree(R.adir(child))
    os.makedirs(R.adir(child))
    m = {'aid': child, 'parent': 'initial', 'mode': 'swap_' + arm, 'kind': 'swap', 'gen': 0, 'problem_statement': ps}
    R.save_meta(child, m)
    patch = edit_with(R, editor_code, child, ps)
    open(os.path.join(R.adir(child), 'patch.diff'), 'w').write(patch)
    m['patch_lines'] = patch.count('\n')
    if not patch.strip():
        m.update(done=True, failed='empty_model_patch', compiled=False); R.save_meta(child, m); return child
    m['patch_applied'] = R.materialize('initial', child, patch); R.save_meta(child, m)
    R.evaluate_staged(child)
    m = R.meta(child); m.update(done=True, compiled=R.is_compiled(child)); R.save_meta(child, m)
    return child

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('exp'); ap.add_argument('--evolved', required=True)
    ap.add_argument('--source', default='v2_C2_single'); ap.add_argument('--n', type=int, default=12)
    a = ap.parse_args()
    R = dgm_lcb.Run(a.exp); R.ensure_initial()
    src = os.path.join(dgm_lcb.SHI, 'exps', a.source, 'agents')
    pss = []
    for d in sorted(os.listdir(src)):
        mp = os.path.join(src, d, 'meta.json')
        if d.startswith('g') and os.path.exists(mp):
            ps = json.load(open(mp)).get('problem_statement')
            if ps: pss.append(ps)
    pss = pss[:a.n]
    json.dump(pss, open(os.path.join(R.dir, 'problem_statements.json'), 'w'), indent=1)
    seed_code = os.path.join(R.adir('initial'), 'code')
    jobs = [(i, 'seedEd', seed_code, ps) for i, ps in enumerate(pss)] + [(i, 'evoEd', a.evolved, ps) for i, ps in enumerate(pss)]
    with cf.ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda j: one(R, *j), jobs))

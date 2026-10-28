"""PREREG_v2 B4: lineage ablation of a loop's best agent.

For lineage seed -> a1 -> ... -> an (each ai stores patch.diff against its parent's code), build
  full      : all n patches re-applied in order to the seed (checked against the agent's stored code),
  minus_ai  : all patches except ai, in order,
  only_ai   : the seed plus ai alone.
Patches are applied as in dgm_lcb.materialize (git apply --reject); a patch with rejected hunks is recorded as such.
Variants with identical code are merged. Output: harness/ablate/<exp>__<aid>/<variant>/ and manifest.json.

usage: lineage_ablate.py EXP AID   -> prints name=path arguments for exp/eval_interleaved.py
"""
import filecmp, hashlib, json, os, shutil, subprocess, sys
SHI = os.path.expanduser('~/shi_eval')
IGN = shutil.ignore_patterns('.git', '__pycache__', '*.pyc', '.pytest_cache', 'self_evo.md', 'model_patch.diff')

def lineage(exp, aid):
    out = []
    while aid and aid != 'initial':
        m = json.load(open(os.path.join(SHI, 'exps', exp, 'agents', aid, 'meta.json')))
        out.append((aid, open(os.path.join(SHI, 'exps', exp, 'agents', aid, 'patch.diff'), errors='replace').read(), m.get('kind')))
        aid = m['parent']
    return out[::-1]

def apply_all(seed, patches, dest):
    shutil.copytree(seed, dest, ignore=IGN)
    status = []
    for aid, p in patches:
        if not p.strip(): status.append((aid, 'empty')); continue
        subprocess.run(['git', 'init', '-q'], cwd=dest, check=True)
        subprocess.run(['git', 'add', '-A'], cwd=dest, check=True)
        subprocess.run(['git', '-c', 'user.email=a@b', '-c', 'user.name=a', 'commit', '-q', '-m', 'x'], cwd=dest, check=True)
        r = subprocess.run(['git', 'apply', '--reject', '--whitespace=nowarn', '-'], cwd=dest, input=p, text=True, capture_output=True)
        shutil.rmtree(os.path.join(dest, '.git'), ignore_errors=True)
        rej = []
        for root, _, fs in os.walk(dest):
            for f in fs:
                if f.endswith('.rej') or f.endswith('.orig'):
                    if f.endswith('.rej'): rej.append(os.path.relpath(os.path.join(root, f), dest))
                    os.remove(os.path.join(root, f))
        status.append((aid, 'ok' if r.returncode == 0 else f'rejected hunks in {rej}'))
    return status

def tree_hash(d):
    h = hashlib.sha256()
    for root, dirs, fs in sorted(os.walk(d)):
        dirs.sort()
        for f in sorted(fs):
            p = os.path.join(root, f); h.update(os.path.relpath(p, d).encode()); h.update(open(p, 'rb').read())
    return h.hexdigest()

def same_tree(a, b):
    c = filecmp.dircmp(a, b, ignore=['__pycache__', '.git', '.pytest_cache', 'self_evo.md', 'model_patch.diff'])
    def ok(c):
        if c.left_only or c.right_only or c.diff_files or c.funny_files: return False
        return all(ok(s) for s in c.subdirs.values())
    return ok(c)

def main(exp, aid):
    cfg = json.load(open(os.path.join(SHI, 'exps', exp, 'config.json')))
    seed = cfg['seed_dir']; lin = lineage(exp, aid)
    out = os.path.join(SHI, 'harness', 'ablate', f'{exp}__{aid}'); os.makedirs(out, exist_ok=False)
    man = {'exp': exp, 'aid': aid, 'seed_dir': seed, 'lineage': [(a, k, len(p.splitlines())) for a, p, k in lin], 'variants': {}}
    plan = [('full', [(a, p) for a, p, _ in lin])]
    for i, (a, _, _) in enumerate(lin):
        plan.append((f'minus_{a}', [(b, p) for j, (b, p, _) in enumerate(lin) if j != i]))
        plan.append((f'only_{a}', [(a, lin[i][1])]))
    sc = os.path.join(out, '_seed'); shutil.copytree(seed, sc, ignore=IGN); seen = {tree_hash(sc): 'seed'}; shutil.rmtree(sc)
    for name, patches in plan:
        d = os.path.join(out, name); st = apply_all(seed, patches, d); th = tree_hash(d)
        v = {'applied': st, 'tree': th[:16]}
        if th in seen: v['same_as'] = seen[th]; shutil.rmtree(d)
        else: seen[th] = name
        man['variants'][name] = v
    man['full_matches_stored_code'] = same_tree(os.path.join(out, 'full'), os.path.join(SHI, 'exps', exp, 'agents', aid, 'code')) \
        if os.path.isdir(os.path.join(out, 'full')) else None
    json.dump(man, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)
    args = [f'abl_{exp}__{aid}__{n}={os.path.join(out, n)}' for n, v in man['variants'].items() if 'same_as' not in v]
    print(json.dumps({k: man[k] for k in ('lineage', 'full_matches_stored_code')}), file=sys.stderr)
    for n, v in man['variants'].items(): print(n, v, file=sys.stderr)
    print(' '.join(args))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

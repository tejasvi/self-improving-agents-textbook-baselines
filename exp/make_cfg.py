"""Write an experiment config for dgm_lcb.Run."""
import json, os, sys
SHI = os.path.expanduser('~/shi_eval')
def make(exp, mode='dgm', seed=1, max_generation=40, task_model='claude-haiku-5-5', selfmod_model='claude-haiku-5-5',
         diag_model='claude-sonnet-5-5', seed_dir=None, splits='splits_hard_v1.json', task_workers=16, **kw):
    sp = json.load(open(os.path.join(SHI, 'data/lcb', splits)))
    cfg = dict(exp=exp, mode=mode, seed=seed, max_generation=max_generation, selfimprove_size=2,
               task_model=task_model, selfmod_model=selfmod_model, diag_model=diag_model,
               seed_dir=seed_dir or os.path.join(SHI, 'harness/seed_dgm'),
               splits={'small': sp['small'], 'medium': sp['medium']}, splits_file=splits,
               test_more_threshold=0.4, noise_leeway=0.1, update_archive='keep_better',
               task_budget=0.25, task_timeout=900, selfmod_budget=2.0, diag_budget=1.0, task_workers=task_workers)
    cfg.update(kw)
    d = os.path.join(SHI, 'exps', exp); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'config.json')
    if os.path.exists(p): raise SystemExit(f'exists: {p}')
    json.dump(cfg, open(p, 'w'), indent=1)
    return cfg
if __name__ == '__main__':
    args = dict(a.split('=', 1) for a in sys.argv[2:])
    for k in ('seed', 'max_generation', 'task_workers', 'task_timeout'):
        if k in args: args[k] = int(args[k])
    print(json.dumps(make(sys.argv[1], **args), indent=1)[:600])

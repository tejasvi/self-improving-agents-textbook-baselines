"""DGM-style open-ended self-improvement on LiveCodeBench (port of jennyzzt/dgm polyglot mode).

Faithful to DGM: archive of agents, parent choice `score_child_prop`, 2 self-improvement attempts per
generation, diagnosis prompts (25% stochasticity hint, empty-patch hint, else task-log diagnosis),
self-modification by the parent agent itself on its own repository, staged evaluation (small 10 ->
medium 50 when >= 40% on small), archive update `keep_better` (score >= initial - 0.1).
Additions for the study: placebo mode (children are exact copies), log-free diagnosis, explicit
model/role assignment through the proxy, full persistence for later fresh-task evaluation.
"""
import json, os, sys, math, random, shutil, subprocess, time, threading, argparse, re, http.client, socket
import concurrent.futures as cf
sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
sys.path.insert(0, os.path.expanduser('~/shi_eval/exp'))
import sandbox, lcb, run_task
import dgm_prompts as P

SHI = os.path.expanduser('~/shi_eval')
SEED = os.path.join(SHI, 'harness', 'seed_dgm')
CODE_FILES = ['coding_agent.py', 'tools/', 'utils/']
EXCLUDE = {'utils/evo_utils.py', 'utils/docker_utils.py', 'utils/swe_log_parsers.py', 'utils/eval_utils.py',
           'prompts/self_improvement_prompt.py'}

def git(cwd, *args, check=True):
    env = dict(os.environ, GIT_AUTHOR_NAME='dgm', GIT_AUTHOR_EMAIL='d@l', GIT_COMMITTER_NAME='dgm', GIT_COMMITTER_EMAIL='d@l')
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, env=env, check=check)

def copy_code(src, dst):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', 'self_evo.md',
                                                            'model_patch.diff', '.pytest_cache'))

def llm_text(model, system, user, run, budget=1.0, max_tokens=8192):
    """Host-side single LLM call through the proxy (same accounting as agents)."""
    tok = run_task.mint(run, model, budget, single_tool_call=False)
    body = json.dumps({'model': model, 'max_tokens': max_tokens, 'system': system,
                       'messages': [{'role': 'user', 'content': user}]})
    for attempt in range(4):
        try:
            c = run_task._UDSConn(run_task.SOCK); c.timeout = 900
            c.request('POST', '/v1/messages', body=body, headers={'content-type': 'application/json', 'x-api-key': tok})
            r = json.loads(c.getresponse().read())
            if r.get('type') == 'error': raise RuntimeError(str(r)[:300])
            return ''.join(b.get('text', '') for b in r.get('content', []) if b.get('type') == 'text')
        except Exception as e:
            err = e; time.sleep(5 * (attempt + 1))
    raise err

def extract_json_between_markers(text):
    """As DGM llm.extract_json_between_markers: ```json ... ``` block, else first JSON object."""
    for m in re.finditer(r'```json(.*?)```', text, re.DOTALL):
        try: return json.loads(m.group(1).strip())
        except Exception:
            s = re.sub(r'[\x00-\x1F\x7F]', '', m.group(1).strip())
            try: return json.loads(s)
            except Exception: pass
    for m in re.finditer(r'\{.*\}', text, re.DOTALL):
        try: return json.loads(m.group(0))
        except Exception: pass
    return None

class Run:
    def __init__(self, exp, cfg=None):
        self.dir = os.path.join(SHI, 'exps', exp); self.exp = exp
        os.makedirs(self.dir, exist_ok=True)
        cpath = os.path.join(self.dir, 'config.json')
        if cfg is not None and not os.path.exists(cpath):
            json.dump(cfg, open(cpath, 'w'), indent=1)
        self.cfg = json.load(open(cpath))
        self.rng = random.Random(self.cfg['seed'])
        self.lock = threading.Lock()
        self.pool = cf.ThreadPoolExecutor(self.cfg.get('task_workers', 16))
        self.I = lcb.index()

    # ---------- agents ----------
    def adir(self, aid): return os.path.join(self.dir, 'agents', aid)
    def meta(self, aid):
        p = os.path.join(self.adir(aid), 'meta.json')
        return json.load(open(p)) if os.path.exists(p) else None
    def save_meta(self, aid, m):
        with open(os.path.join(self.adir(aid), 'meta.json.tmp'), 'w') as f: json.dump(m, f, indent=1)
        os.replace(os.path.join(self.adir(aid), 'meta.json.tmp'), os.path.join(self.adir(aid), 'meta.json'))
    def lineage(self, aid):
        out = []
        while aid and aid != 'initial':
            out.append(aid); aid = self.meta(aid)['parent']
        return list(reversed(out))

    def ensure_initial(self):
        if self.meta('initial'): return
        os.makedirs(self.adir('initial'))
        copy_code(self.cfg.get('seed_dir', SEED), os.path.join(self.adir('initial'), 'code'))
        self.save_meta('initial', {'aid': 'initial', 'parent': None, 'kind': 'seed', 'evals': {}})
        self.evaluate_staged('initial')

    # ---------- evaluation ----------
    def eval_tasks(self, aid, stage, task_ids, rep=0, model=None):
        """Run agent on tasks (parallel); store per-task results in evals/<stage>.jsonl; return list."""
        edir = os.path.join(self.adir(aid), 'evals'); os.makedirs(edir, exist_ok=True)
        path = os.path.join(edir, f'{stage}.jsonl')
        have = {}
        if os.path.exists(path):
            for l in open(path):
                r = json.loads(l); have[(r['task'], r['rep'])] = r
        todo = [t for t in task_ids if (t, rep) not in have]
        code = os.path.join(self.adir(aid), 'code')
        model = model or self.cfg['task_model']
        def one(tid):
            outdir = os.path.join(self.adir(aid), 'runs', stage, f'{tid}_r{rep}')
            run_id = f"{self.exp}|{aid}|{stage}|{tid}|{rep}"
            try:
                r = run_task.run_agent(code, self.I[tid], run_id, outdir, model=model,
                                       budget=self.cfg.get('task_budget', 0.25), timeout=self.cfg.get('task_timeout', 900))
            except Exception as e:
                r = {'run': run_id, 'task': tid, 'passed': False, 'empty': True, 'error': repr(e)[:300]}
            r['rep'] = rep; r['stage'] = stage
            with self.lock:
                with open(path, 'a') as f: f.write(json.dumps(r) + '\n')
            return r
        res = list(self.pool.map(one, todo))
        return [have[(t, rep)] for t in task_ids if (t, rep) in have] + res

    def perf(self, aid, stages=('small', 'medium', 'big')):
        """DGM overall_performance over all evaluated stage files (rep 0)."""
        R, U, E = [], [], []
        for st in stages:
            p = os.path.join(self.adir(aid), 'evals', f'{st}.jsonl')
            if not os.path.exists(p): continue
            for l in open(p):
                r = json.loads(l)
                if r.get('rep', 0) != 0: continue
                (R if r['passed'] else (E if r.get('empty') else U)).append(r['task'])
        n = len(R) + len(U) + len(E)
        return {'accuracy_score': len(R) / n if n else 0.0, 'total_submitted_instances': n,
                'total_resolved_ids': R, 'total_unresolved_ids': U, 'total_emptypatch_ids': E}

    def evaluate_staged(self, aid):
        S = self.cfg['splits']
        res = self.eval_tasks(aid, 'small', S['small'])
        solved = sum(r['passed'] for r in res)
        if solved >= len(S['small']) * self.cfg.get('test_more_threshold', 0.4):
            self.eval_tasks(aid, 'medium', S['medium'])
        if self.cfg.get('big_stage') and S.get('big'):
            p = self.perf(aid)
            if p['total_submitted_instances'] >= len(S['small']) + len(S['medium']):
                if p['accuracy_score'] >= self.full_eval_threshold():
                    self.eval_tasks(aid, 'big', S['big'])
        m = self.meta(aid); m['perf'] = self.perf(aid); self.save_meta(aid, m)
        return m['perf']

    def full_eval_threshold(self):
        S = self.cfg['splits']; full = len(S['small']) + len(S['medium']) + len(S.get('big', []))
        scores = [self.perf('initial')['accuracy_score']]
        for a in self.state()['archive']:
            p = self.perf(a)
            if p['total_submitted_instances'] >= 0.9 * full: scores.append(p['accuracy_score'])
        thr = sorted(scores, reverse=True)[1] if len(scores) > 1 else scores[0]
        return max(thr, 0.4)

    # ---------- state ----------
    def state(self):
        p = os.path.join(self.dir, 'state.json')
        return json.load(open(p)) if os.path.exists(p) else {'generation': 0, 'archive': ['initial']}
    def save_state(self, s):
        json.dump(s, open(os.path.join(self.dir, 'state.json.tmp'), 'w'), indent=1)
        os.replace(os.path.join(self.dir, 'state.json.tmp'), os.path.join(self.dir, 'state.json'))

    def is_compiled(self, aid):
        p = self.perf(aid)
        return p['total_submitted_instances'] >= len(self.cfg['splits']['small']) and \
            (len(p['total_resolved_ids']) + len(p['total_unresolved_ids'])) > 0

    # ---------- DGM choices ----------
    def choose_selfimproves(self, archive, k):
        cands = {}
        for a in archive:
            p = self.perf(a)
            cands[a] = {'score': p['accuracy_score'], 'children': 0, 'perf': p}
        for a in archive:
            par = self.meta(a)['parent']
            if a != 'initial' and par in cands: cands[par]['children'] += 1
        commits = list(cands)
        if self.cfg.get('baseline') == 'no_darwin':
            parents = commits[-1:] * k
        else:
            sc = [1 / (1 + math.exp(-10 * (cands[c]['score'] - 0.5))) for c in commits]
            ch = [1 / (1 + cands[c]['children']) for c in commits]
            w = [a * b for a, b in zip(sc, ch)]; tot = sum(w)
            parents = self.rng.choices(commits, [x / tot for x in w], k=k)
        out = []
        for par in parents:
            p = cands[par]['perf']
            ids = p['total_emptypatch_ids'] + p['total_unresolved_ids']
            if not ids: ids = p['total_resolved_ids'] + ids
            out.append((par, self.rng.choice(ids)))
        return out

    # ---------- diagnosis ----------
    def code_text(self, parent):
        root = os.path.join(self.adir('initial'), 'code'); parts = []
        for fp in CODE_FILES:
            full = os.path.join(root, fp)
            if os.path.isfile(full):
                parts += [f'# {fp}', open(full).read().strip()]
            elif os.path.isdir(full):
                for r, _, files in os.walk(full):
                    for f in sorted(files):
                        if f.endswith('.py'):
                            rel = os.path.relpath(os.path.join(r, f), root)
                            if rel not in EXCLUDE: parts += [f'# {rel}', open(os.path.join(r, f)).read().strip()]
        for i, a in enumerate(self.lineage(parent)):
            pf = os.path.join(self.adir(a), 'patch.diff')
            parts += [f'# Patch {i + 1}: {a}/model_patch.diff', open(pf).read().strip()]
        return '\n'.join(parts)

    def task_logs(self, parent, tid):
        """md_log, eval_log, predicted_patch, test_patch for the parent's run on task tid."""
        for st in ('small', 'medium', 'big'):
            d = os.path.join(self.adir(parent), 'runs', st, f'{tid}_r0')
            if os.path.exists(d): break
        else:
            return None
        md = open(os.path.join(d, 'out', 'chat.md'), errors='replace').read() if os.path.exists(os.path.join(d, 'out', 'chat.md')) else ''
        md = '\n'.join(l for l in md.splitlines() if not l.startswith('Error in get_response_withtools')).strip() or 'No logs available.'
        if len(md) > 250000: md = md[:250000] + '\n<log clipped>'
        res = json.load(open(os.path.join(d, 'result.json'))) if os.path.exists(os.path.join(d, 'result.json')) else {}
        ff = (res.get('grade') or {}).get('first_fail') or {}
        sol = os.path.join(d, 'repo', 'solution.py')
        pred = open(sol).read() if os.path.exists(sol) else 'No predicted patch available. Assume the agent failed.'
        if res.get('empty'): pred = '(empty patch: solution.py was not changed)'
        else: pred = f'--- solution.py (final content)\n{pred}'
        if ff.get('kind') in ('wrong_answer', 'runtime_error', 'timeout'):
            test_patch = f"Hidden test case #{ff.get('idx')}:\nInput:\n{ff.get('input','')}\nExpected output:\n{ff.get('expected','')}"
        else:
            test_patch = 'Hidden test cases are not shown for this failure.'
        if res.get('passed'): eval_log = 'All hidden tests passed.'
        elif res.get('empty'): eval_log = 'empty_patch: no solution was written, so all hidden tests failed.'
        else:
            eval_log = f"Result: FAILED ({ff.get('kind')}) after passing {(res.get('grade') or {}).get('n_run', 0)} of {(res.get('grade') or {}).get('n_tests', '?')} hidden tests."
            if ff.get('got') is not None: eval_log += f"\nProgram output on the failing test:\n{ff.get('got')}"
            if ff.get('stderr'): eval_log += f"\nError output:\n{ff.get('stderr')}"
        return md, eval_log, pred, test_patch, bool(res.get('empty'))

    def diagnose(self, parent, entry, mode, run_tag):
        """Returns (problem_statement, kind, raw_text)."""
        if mode == 'randommove':   # PREREG_v2 B2: diagnosis replaced by a uniformly drawn generic request
            import random_moves
            k = self.rng.randrange(len(random_moves.MOVES))
            ps = P.coding_agent_summary_lcb + P.problem_description_prompt.format(
                implementation_suggestion=random_moves.MOVES[k], problem_description=random_moves.MOVES[k])
            return ps, f'randommove:{k}', None
        sysmsg = P.coding_agent_summary_lcb + P.diagnose_system_message.format(code=self.code_text(parent))
        if mode == 'nolog':
            kind = 'nolog'; user = P.diagnose_prompt_nolog
        else:
            md, ev, pred, testp, empty = self.task_logs(parent, entry)
            if mode == 'nohint':   # exploratory arm: task-log diagnosis only, none of DGM's hand-written hint prompts
                kind = 'task_nohint'
                user = P.lcb_issue_prompt + P.diagnose_prompt.format(md_log=md, eval_log=ev, predicted_patch=pred,
                                                                    test_patch=testp, github_issue=lcb.problem_statement(self.I[entry]))
            elif self.rng.random() < 0.25:
                kind = 'stochasticity'; user = P.diagnose_prompt_stochasticity.format(md_log=md)
            elif empty:
                kind = 'empty_patch'; user = P.diagnose_prompt_emptypatches.format(md_log=md)
            else:
                kind = 'task'
                user = P.lcb_issue_prompt + P.diagnose_prompt.format(md_log=md, eval_log=ev, predicted_patch=pred,
                                                                    test_patch=testp, github_issue=lcb.problem_statement(self.I[entry]))
        for attempt in range(4):
            raw = llm_text(self.cfg['diag_model'], sysmsg, user, run=f'{self.exp}|diag|{run_tag}|{attempt}',
                           budget=self.cfg.get('diag_budget', 1.0))
            j = extract_json_between_markers(raw)
            if j and 'implementation_suggestion' in j and 'problem_description' in j:
                ps = P.coding_agent_summary_lcb + P.problem_description_prompt.format(
                    implementation_suggestion=j['implementation_suggestion'], problem_description=j['problem_description'])
                return ps, kind, raw
        return None, kind, raw

    # ---------- self-modification ----------
    def self_modify(self, parent, child, problem_statement):
        """Run the parent's coding agent on a copy of its own repo; return the patch text ('' if none)."""
        work = os.path.join(self.adir(child), 'selfmod'); os.makedirs(work, exist_ok=True)
        repo = os.path.join(work, 'dgm')
        copy_code(os.path.join(self.adir(parent), 'code'), repo)
        with open(os.path.join(repo, '.gitignore'), 'a') as f: f.write('\nself_evo.md\nmodel_patch.diff\n__pycache__/\n')
        git(repo, 'init', '-q'); git(repo, 'add', '-A'); git(repo, 'commit', '-q', '-m', 'a nonsense commit message')
        base = git(repo, 'rev-parse', 'HEAD').stdout.strip()
        tok = run_task.mint(f'{self.exp}|selfmod|{child}', self.cfg['selfmod_model'], self.cfg.get('selfmod_budget', 2.0))
        cmd = ['timeout', '1800', 'python3', '/dgm/coding_agent.py', '--problem_statement', problem_statement,
               '--git_dir', '/dgm/', '--chat_history_file', '/dgm/self_evo.md', '--base_commit', base,
               '--outdir', '/dgm/', '--test_description', P.test_description_dgm_repo, '--self_improve']
        r = sandbox.run(cmd, rw=[(repo, '/dgm')], sock=run_task.SOCK, cwd='/',
                        env={'ANTHROPIC_BASE_URL': 'http://127.0.0.1:8080', 'ANTHROPIC_API_KEY': tok},
                        timeout=1900, mem_gb=8)
        open(os.path.join(work, 'stderr.txt'), 'wb').write(r['err'][-200000:])
        if os.path.exists(os.path.join(repo, 'self_evo.md')): shutil.copy(os.path.join(repo, 'self_evo.md'), os.path.join(work, 'self_evo.md'))
        pf = os.path.join(repo, 'model_patch.diff')
        if os.path.exists(pf):
            patch = open(pf, errors='replace').read()
        else:  # agent crashed before writing it; take the diff ourselves (same as DGM diff_versus_commit)
            git(repo, 'add', '-A', check=False)
            patch = git(repo, 'diff', '--cached', base, check=False).stdout
        return patch

    def materialize(self, parent, child, patch):
        code = os.path.join(self.adir(child), 'code')
        copy_code(os.path.join(self.adir(parent), 'code'), code)
        if not patch.strip(): return True
        git(code, 'init', '-q'); git(code, 'add', '-A'); git(code, 'commit', '-q', '-m', 'parent')
        p = subprocess.run(['git', 'apply', '--reject', '--whitespace=nowarn', '-'], cwd=code, input=patch, text=True,
                           capture_output=True)
        shutil.rmtree(os.path.join(code, '.git'), ignore_errors=True)
        for r, _, fs in os.walk(code):
            for f in fs:
                if f.endswith('.rej') or f.endswith('.orig'): os.remove(os.path.join(r, f))
        return p.returncode == 0

    # ---------- one self-improvement attempt ----------
    def attempt(self, parent, entry, gen, idx, mode):
        child = f'g{gen:03d}_{idx}'
        if self.meta(child) and self.meta(child).get('done'): return child
        if os.path.exists(self.adir(child)): shutil.rmtree(self.adir(child))
        os.makedirs(self.adir(child))
        m = {'aid': child, 'parent': parent, 'entry': entry, 'gen': gen, 'mode': mode, 't0': time.time()}
        self.save_meta(child, m)
        if mode == 'placebo':
            patch = ''; m['kind'] = 'placebo'
        else:
            ps, kind, raw = self.diagnose(parent, entry, mode if mode in ('nolog', 'nohint', 'randommove') else 'task', child)
            m.update(kind=kind, problem_statement=ps, diag_raw=raw[-20000:] if raw else None)
            self.save_meta(child, m)
            if not ps:
                m.update(done=True, failed='diagnosis'); self.save_meta(child, m); return child
            patch = self.self_modify(parent, child, ps)
        open(os.path.join(self.adir(child), 'patch.diff'), 'w').write(patch)
        m['patch_lines'] = patch.count('\n')
        if mode != 'placebo' and not patch.strip():
            m.update(done=True, failed='empty_model_patch'); self.save_meta(child, m); return child
        ok = self.materialize(parent, child, patch)
        m['patch_applied'] = ok; self.save_meta(child, m)
        self.evaluate_staged(child)
        m = self.meta(child); m.update(done=True, compiled=self.is_compiled(child), t1=time.time())
        self.save_meta(child, m)
        return child

    def generation(self):
        s = self.state(); gen = s['generation']
        entries = self.choose_selfimproves(s['archive'], self.cfg.get('selfimprove_size', 2))
        mode = self.cfg.get('mode', 'dgm')
        with cf.ThreadPoolExecutor(len(entries)) as ex:
            kids = list(ex.map(lambda pe: self.attempt(pe[1][0], pe[1][1], gen, pe[0], mode), enumerate(entries)))
        init = self.perf('initial')['accuracy_score'] - self.cfg.get('noise_leeway', 0.1)
        compiled = [k for k in kids if self.meta(k).get('compiled')]
        for k in compiled:
            if self.cfg.get('update_archive', 'keep_better') == 'keep_all' or self.perf(k)['accuracy_score'] >= init:
                s['archive'].append(k)
        with open(os.path.join(self.dir, 'dgm_metadata.jsonl'), 'a') as f:
            f.write(json.dumps({'generation': gen, 'selfimprove_entries': entries, 'children': kids,
                                'children_compiled': compiled, 'archive': s['archive'], 'ts': time.time()}) + '\n')
        s['generation'] = gen + 1; self.save_state(s)

    def best(self):
        """DGM-reported best: highest accuracy among agents with the most evaluated tasks (ties -> earliest)."""
        s = self.state(); best = None
        for a in s['archive']:
            p = self.perf(a); key = (p['total_submitted_instances'], p['accuracy_score'])
            if best is None or key > best[0]: best = (key, a)
        return best[1]

    def run(self):
        self.ensure_initial()
        while self.state()['generation'] < self.cfg['max_generation']:
            if os.path.exists(os.path.join(SHI, 'STOP')) or os.path.exists(os.path.join(self.dir, 'STOP')): break
            self.generation()

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('exp'); a = ap.parse_args()
    Run(a.exp).run()

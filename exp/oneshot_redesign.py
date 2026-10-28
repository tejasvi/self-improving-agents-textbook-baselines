"""PREREG_v2 B3: one-shot expert redesign (diagnosis without search).

One model call sees the DGM seed's code and the logs of 5 failed selection-set runs of the seed (the same log material
DGM's diagnosis step sees: chat log, evaluation result, final solution, failing hidden test), and returns a revised
harness. No evaluation feedback. Output: harness/redesign/<tag>_r<i>/ (seed copy + returned files) and raw responses.

usage: oneshot_redesign.py MODEL TAG N
"""
import json, os, random, re, shutil, subprocess, sys
sys.path.insert(0, os.path.expanduser('~/shi_eval/exp')); sys.path.insert(0, os.path.expanduser('~/shi_eval/infra'))
import dgm_lcb, dgm_prompts as P, lcb
SHI = os.path.expanduser('~/shi_eval')
SEED = os.path.join(SHI, 'harness', 'seed_dgm')

def clip(s, n=30000):
    return s if len(s) <= n else s[:n // 2] + '\n<... log clipped ...>\n' + s[-n // 2:]

def code_dump(root):
    parts = []
    for r, ds, fs in sorted(os.walk(root)):
        ds[:] = sorted(d for d in ds if d not in ('.git', '__pycache__', 'tests', '.pytest_cache'))
        for f in sorted(fs):
            if f.endswith('.py') or f in ('requirements.txt',):
                p = os.path.join(r, f); parts.append(f'<file path="{os.path.relpath(p, root)}">\n{open(p).read()}\n</file>')
    return '\n\n'.join(parts)

def failures(R):
    out = []
    for st in ('small', 'medium'):
        for l in open(os.path.join(R.adir('initial'), 'evals', f'{st}.jsonl')):
            r = json.loads(l)
            if r.get('rep', 0) == 0 and not r.get('passed'): out.append(r['task'])
    out = sorted(set(out)); return random.Random(2026).sample(out, 5)

def prompt(R, tasks):
    logs = []
    for i, t in enumerate(tasks):
        md, ev, pred, testp, empty = R.task_logs('initial', t)
        logs.append(f'## Failed run {i + 1}\n### Problem statement\n{lcb.problem_statement(R.I[t])}\n### Agent chat log\n{clip(md)}\n'
                    f'### Evaluation\n{ev}\n### Final solution\n{clip(pred, 8000)}\n### Failing hidden test\n{clip(testp, 4000)}')
    return (P.coding_agent_summary_lcb +
            "\n# The agent's code\n\n" + code_dump(SEED) +
            "\n\n# Logs of five runs where the agent failed\n\n" + '\n\n'.join(logs) +
            "\n\n# Your task\n\nRevise this coding agent so that it solves as many hard problems of this kind as possible. "
            "You get no further feedback, so make the changes you are confident will help, and keep the agent working: "
            "coding_agent.py must keep its command-line interface, every tool must keep the tool_info()/tool_function() "
            "interface, and model names and API access (client creation, environment variables) must stay as they are. "
            "Return every file you change in full, each wrapped exactly as <file path=\"relative/path.py\">...</file>; "
            "files you do not return stay unchanged.")

def materialize(raw, dest):
    shutil.copytree(SEED, dest, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', '.pytest_cache'))
    files = re.findall(r'<file path="([^"]+)">\n?(.*?)</file>', raw, re.DOTALL)
    written = []
    for rel, body in files:
        rel = os.path.normpath(rel)
        if rel.startswith('..') or os.path.isabs(rel): continue
        p = os.path.join(dest, rel); os.makedirs(os.path.dirname(p) or dest, exist_ok=True)
        open(p, 'w').write(body.rstrip('\n') + '\n'); written.append(rel)
    bad = []
    for r, _, fs in os.walk(dest):
        for f in fs:
            if f.endswith('.py'):
                c = subprocess.run([sys.executable, '-m', 'py_compile', os.path.join(r, f)], capture_output=True, text=True)
                if c.returncode: bad.append(os.path.relpath(os.path.join(r, f), dest))
    shutil.rmtree(os.path.join(dest, '__pycache__'), ignore_errors=True)
    for r, ds, _ in os.walk(dest):
        for d in ds:
            if d == '__pycache__': shutil.rmtree(os.path.join(r, d), ignore_errors=True)
    return written, bad

def main(model, tag, n):
    R = dgm_lcb.Run('v2_A_dgm_s1'); tasks = failures(R)
    user = prompt(R, tasks)
    out = os.path.join(SHI, 'harness', 'redesign'); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, f'{tag}_prompt.txt'), 'w').write(user)
    man = {'model': model, 'tasks': tasks, 'prompt_chars': len(user), 'samples': {}}
    for i in range(n):
        name = f'{tag}_r{i}'; dest = os.path.join(out, name)
        if os.path.exists(dest): continue
        raw = dgm_lcb.llm_text(model, 'You are an expert engineer of LLM-based coding agents.', user,
                               run=f'v3_B3|{tag}|{i}', budget=4.0, max_tokens=20000)
        open(os.path.join(out, f'{name}.raw.txt'), 'w').write(raw)
        written, bad = materialize(raw, dest)
        man['samples'][name] = {'written': written, 'compile_errors': bad, 'raw_chars': len(raw)}
        print(name, man['samples'][name], flush=True)
    json.dump(man, open(os.path.join(out, f'{tag}_manifest.json'), 'w'), indent=1)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))

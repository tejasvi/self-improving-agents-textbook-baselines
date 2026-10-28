"""Write swe/dgm_harness_proxy_clean.py = swe/dgm_harness_proxy.py + one more step (decision 2026-10-24, "clean" variant):
right after DGM's setup step (eval.sh + rm /eval.sh) and before the agent starts, remove (i) every .pytest_cache
directory under /testbed (also .tox/*/.pytest_cache) and (ii) the files the instance's test_patch adds ('--- /dev/null')
that git shows as untracked, and (iii) __pycache__/<stem>.*.pyc of every .py file the test patch adds or modifies
(decision 2026-10-24). Nothing else. Saves the diff against dgm_harness_proxy.py."""
import difflib, sys
src, dst, diff = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src).read()
helper = '''def clean_hidden_test_residue(container, entry, out_dname):
    """flagship clean variant: after DGM's setup step (eval.sh applied the hidden test patch, ran the tests and reset only
    the modified test files) and before the agent starts, remove (i) every .pytest_cache directory under /testbed (also
    .tox/*/.pytest_cache), (ii) the files the instance's test_patch adds ('--- /dev/null') that git shows as untracked and
    (iii) __pycache__/<stem>.*.pyc of every .py file the test patch adds or modifies (compiled copies of the hidden tests).
    Nothing else (no git clean: build artifacts stay). Logs removals and remaining residue to <out_dname>/clean/<id>.json."""
    import re
    iid = entry['instance_id']
    def run(cmd):
        return container.exec_run(cmd, workdir='/').output.decode(errors='replace')
    def caches():
        return [d for d in run(['find', '/testbed', '-type', 'd', '-name', '.pytest_cache', '-prune']).split('\\n')
                if d.startswith('/testbed/') and d.endswith('/.pytest_cache')]
    rec = {'instance_id': iid, 'removed_pytest_cache_dirs': [], 'removed_added_files': [], 'removed_test_patch_pyc': []}
    for d in caches():
        run(['rm', '-rf', '--', d]); rec['removed_pytest_cache_dirs'].append(d)
    added = re.findall(r'^--- /dev/null\\n\\+\\+\\+ b/(\\S+)', entry['test_patch'], re.M)
    if added:
        untracked = {e[3:] for e in run(['git', '-C', '/testbed', 'status', '--porcelain', '-z', '--untracked-files=all']).split('\\0')
                     if e.startswith('?? ')}
        for p in added:
            if p in untracked:
                run(['rm', '-f', '--', '/testbed/' + p]); rec['removed_added_files'].append(p)
    # left in place (logged only): caches/added files still present, empty dirs of removed files, compiled test-patch files
    rec['left_pytest_cache_dirs'] = caches()
    rec['left_added_files'] = [p for p in added if container.exec_run(['test', '-e', '/testbed/' + p], workdir='/').exit_code == 0]
    rec['left_empty_dirs'] = sorted({d for p in rec['removed_added_files'] for d in [os.path.dirname('/testbed/' + p)]
                                     if run(['find', d, '-maxdepth', '0', '-empty']).strip() == d})
    def pycs():
        found = []
        for p in re.findall(r'^\\+\\+\\+ b/(\\S+)\\.py$', entry['test_patch'], re.M):
            d, b = os.path.split(p)
            found += run(['bash', '-c', f'ls /testbed/{d}/__pycache__/{b}.*.pyc 2>/dev/null']).split()
        return found
    for f in pycs():
        if f.startswith('/testbed/') and '/__pycache__/' in f and f.endswith('.pyc'):
            run(['rm', '-f', '--', f]); rec['removed_test_patch_pyc'].append(f)
    rec['left_test_patch_pyc'] = pycs()
    (out_dname / 'clean').mkdir(exist_ok=True)
    (out_dname / 'clean' / f'{iid}.json').write_text(json.dumps(rec, indent=1))
    safe_log(f"flagship clean: {json.dumps(rec)}")

def process_entry(entry, out_dname, model_name_or_path, model_patch_paths):
'''
subs = [
    ("def process_entry(entry, out_dname, model_name_or_path, model_patch_paths):\n", helper),
    ("        exec_result = container.exec_run(\"rm /eval.sh\", workdir='/')  # remove eval script\n"
     "        log_container_output(exec_result)\n",
     "        exec_result = container.exec_run(\"rm /eval.sh\", workdir='/')  # remove eval script\n"
     "        log_container_output(exec_result)\n"
     "        clean_hidden_test_residue(container, entry, out_dname)  # flagship clean variant: hidden-test residue out\n"),
]
t = s
for old, new in subs:
    assert t.count(old) == 1, (old[:60], t.count(old))
    t = t.replace(old, new)
open(dst, 'w').write(t)
open(diff, 'w').writelines(difflib.unified_diff(s.splitlines(True), t.splitlines(True), 'swe/dgm_harness_proxy.py', 'swe/dgm_harness_proxy_clean.py'))
print('ok', len(s), '->', len(t))

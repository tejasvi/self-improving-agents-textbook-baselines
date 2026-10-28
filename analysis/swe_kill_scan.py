"""SWE-bench run, reported best agent: how many saved chat logs of early-ended runs contain a process-kill command
(pkill, killall or kill -9), and how many of those logs are non-empty. Reads flagship/runs_full/final_report_runs.tsv and the logs under
flagship/runs_full/flag_dgm_best_s45/predictions/*/ (diag/<task>.md for early-ended runs). Writes results/swe_kill_scan.json."""
import csv, glob, json, os, re

SHI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(SHI, 'flagship', 'runs_full')
PAT = re.compile(r'\bpkill\b|\bkillall\b|\bkill\s+-9\b')
rows = [r for r in csv.DictReader(open(os.path.join(RUNS, 'final_report_runs.tsv')), delimiter='\t')
        if r['agent'] == 'dgm_best' and r['early'] == 'True']
found = nonempty = hits = 0
for r in rows:
    cands = glob.glob(os.path.join(RUNS, 'flag_dgm_best_s45', 'predictions', '*', 'diag', r['instance_id'] + '.md'))
    if not cands:
        continue
    found += 1
    texts = [open(c, errors='replace').read() for c in cands]
    nonempty += any(t.strip() for t in texts)
    if any(PAT.search(t) for t in texts):
        hits += 1
out = {'early_runs': len(rows), 'logs_found': found, 'logs_nonempty': nonempty, 'logs_with_kill': hits}
json.dump(out, open(os.path.join(SHI, 'results', 'swe_kill_scan.json'), 'w'), indent=1)
print(out)

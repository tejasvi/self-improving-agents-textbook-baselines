"""Small descriptive numbers for the paper: median wall-clock minutes per SWE agent (flagship/runs_full/
final_report_runs.tsv) and DROP answer lengths where ADAS's best-by-validation agent scores below matched CoT-SC
(adas_p4/full). Writes results/misc_v2.json."""
import csv, json, os, statistics
SHI = os.path.expanduser('~/shi_eval'); out = {}
rows = list(csv.DictReader(open(os.path.join(SHI, 'flagship', 'runs_full', 'final_report_runs.tsv')), delimiter='\t'))
key = 'agent' if 'agent' in rows[0] else list(rows[0].keys())[0]
wall = next(k for k in rows[0] if k.startswith('wall'))
for a in ('dgm_init', 'dgm_best', 'moves', 'moves_retry'):
    w = [float(r[wall]) for r in rows if r[key] == a and r[wall] not in ('', 'None')]
    out[f'swe_median_min_{a}'] = round(statistics.median(w) / 60.0, 0)
B = os.path.join(SHI, 'adas_p4', 'full')
def load(tag): return {r['idx']: r for r in map(json.loads, open(os.path.join(B, tag + '.jsonl')))}
A = load('drop__best_val-full'); C = load('drop__cotsc10-full')
def num(x):
    try: return float(x)
    except Exception: return None
worse = [i for i in A if i in C and num(A[i]['score']) is not None and num(C[i]['score']) is not None and num(A[i]['score']) < num(C[i]['score'])]
la = [len(str(A[i]['pred'])) for i in worse]; lc = [len(str(C[i]['pred'])) for i in worse]
out['drop_worse'] = len(worse); out['drop_worse_longer'] = sum(a > c for a, c in zip(la, lc))
out['drop_median_len_agent'] = statistics.median(la); out['drop_median_len_cotsc'] = statistics.median(lc)
json.dump(out, open(os.path.join(SHI, 'results', 'misc_v2.json'), 'w'), indent=1); print(out)

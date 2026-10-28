"""Summarize ADAS archives: initial entries, best-by-validation and best-by-test discovered agents."""
import json, os, re, sys
EXT = os.path.expanduser('~/shi_eval/ext/adas')

def median(s):
    m = re.search(r'Median: ([\-0-9.]+)%', s or '')
    return float(m.group(1)) if m else None

def load(domain):
    return json.load(open(f'{EXT}/{domain}_gpt3.5_results.json'))

if __name__ == '__main__':
    for d in sys.argv[1:] or ['mgsm', 'drop', 'gpqa', 'mmlu']:
        A = load(d)
        print(f'== {d}: {len(A)} entries; keys {sorted(A[0].keys())}')
        for i, e in enumerate(A):
            print(f"  [{i:2d}] gen={str(e.get('generation')):>7} val={median(e.get('fitness'))} test={median(e.get('test_fitness'))} "
                  f"name={e.get('name')!r} codelen={len(e.get('code',''))}")

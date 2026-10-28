"""Second pilot (DGM seed, 80 problems x 2): how many runs ended without a solution, and how many of those ended on an
empty response (the last assistant message has empty text). Reads results/pilot2.jsonl and the chat logs under
runs/pilot2/seed_dgm/<task>/r<rep>/out/chat.md (not part of the release); writes results/pilot_empty.json."""
import json, os

SHI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
END = "{'role': 'assistant', 'content': [{'type': 'text', 'text': ''}]}]"
rs = [json.loads(l) for l in open(os.path.join(SHI, 'results', 'pilot2.jsonl'))]
nosol = [r for r in rs if r.get('empty')]
ended_empty = 0
for r in nosol:
    p = os.path.join(SHI, 'runs', 'pilot2', 'seed_dgm', r['task'], f"r{r['rep']}", 'out', 'chat.md')
    t = open(p, errors='replace').read() if os.path.exists(p) else ''
    ended_empty += t.rstrip().endswith(END)
out = {'runs': len(rs), 'no_solution': len(nosol), 'no_solution_ending_on_empty_response': ended_empty}
json.dump(out, open(os.path.join(SHI, 'results', 'pilot_empty.json'), 'w'), indent=1)
print(out)

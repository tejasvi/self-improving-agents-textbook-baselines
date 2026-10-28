"""Load DGM released run logs (Drive archive) into per-agent records."""
import json, os, glob, sys

def read_jsonl_concat(path):
    L = open(path).read(); dec = json.JSONDecoder(); i = 0; out = []
    while i < len(L):
        while i < len(L) and L[i].isspace(): i += 1
        if i >= len(L): break
        o, j = dec.raw_decode(L, i); out.append(o); i = j
    return out

def load_run(rundir):
    gens = read_jsonl_concat(os.path.join(rundir, 'dgm_metadata.jsonl'))
    agents = {}
    for m in glob.glob(os.path.join(rundir, '*', 'metadata.json')):
        rid = os.path.basename(os.path.dirname(m))
        try: d = json.load(open(m))
        except Exception as e: print('bad', m, e, file=sys.stderr); continue
        op = d.get('overall_performance') or {}
        agents[rid] = dict(
            run_id=rid, parent=d.get('parent_commit'), entry=d.get('entry'),
            n=op.get('total_submitted_instances'), acc=op.get('accuracy_score'),
            resolved=set(op.get('total_resolved_ids') or []),
            unresolved=set(op.get('total_unresolved_ids') or []),
            empty=set(op.get('total_emptypatch_ids') or []),
            keys=sorted(d.keys()))
    return gens, agents

if __name__ == '__main__':
    gens, agents = load_run(sys.argv[1])
    print('generations', len(gens), 'agents', len(agents))
    from collections import Counter
    print(Counter(a['n'] for a in agents.values()))
    a = next(iter(agents.values())); print(a['keys'])
    for rid, a in sorted(agents.items(), key=lambda kv: -(kv[1]['acc'] or 0))[:8]:
        print(rid, a['parent'], a['entry'], a['n'], a['acc'], len(a['resolved']), len(a['unresolved']), len(a['empty']))

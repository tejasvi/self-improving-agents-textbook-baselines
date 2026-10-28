"""Split normalized LCB tasks into a light index plus one test file per task."""
import json, os, sys
src = sys.argv[1]; outdir = sys.argv[2]
os.makedirs(os.path.join(outdir, 'tests'), exist_ok=True)
with open(os.path.join(outdir, 'index.jsonl'), 'w') as idx:
    for line in open(src):
        t = json.loads(line)
        priv = t.pop('private'); pub = t['public']
        sz = sum(len(x['input']) + len(x['output']) for x in priv)
        maxin = max([len(x['input']) for x in priv] + [0])
        with open(os.path.join(outdir, 'tests', t['id'] + '.json'), 'w') as f:
            json.dump({'public': pub, 'private': priv}, f)
        t.update(n_private=len(priv), private_bytes=sz, max_input_bytes=maxin)
        idx.write(json.dumps(t) + '\n')

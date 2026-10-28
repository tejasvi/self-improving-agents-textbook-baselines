"""Normalize LiveCodeBench code_generation_lite into tasks.jsonl (safe decoding: no pickle globals allowed)."""
import json, base64, zlib, pickle, io, sys, os, glob, hashlib

class NoGlobals(pickle.Unpickler):
    def find_class(self, module, name):
        raise pickle.UnpicklingError(f'blocked global {module}.{name}')

def decode_private(s):
    try:
        return json.loads(s)
    except Exception:
        raw = zlib.decompress(base64.b64decode(s.encode('utf-8')))
        obj = NoGlobals(io.BytesIO(raw)).load()
        return json.loads(obj) if isinstance(obj, (str, bytes)) else obj

src = sys.argv[1]; dst = sys.argv[2]
n = 0; stats = []
with open(dst, 'w') as out:
    for fn in sorted(glob.glob(os.path.join(src, 'test*.jsonl'))):
        for line in open(fn):
            r = json.loads(line)
            pub = json.loads(r['public_test_cases']); priv = decode_private(r['private_test_cases'])
            meta = json.loads(r.get('metadata') or '{}')
            tt = (pub or priv)[0]['testtype']
            t = dict(id=r['question_id'], title=r['question_title'], platform=r['platform'], contest=r['contest_id'],
                     date=r['contest_date'], difficulty=r['difficulty'], statement=r['question_content'],
                     starter_code=r['starter_code'], testtype=tt, func_name=meta.get('func_name'),
                     public=[{'input': x['input'], 'output': x['output']} for x in pub],
                     private=[{'input': x['input'], 'output': x['output']} for x in priv], src=os.path.basename(fn))
            sz = sum(len(x['input']) + len(x['output']) for x in t['private'])
            stats.append((len(t['private']), sz))
            out.write(json.dumps(t) + '\n'); n += 1
import statistics as S
print('tasks', n)
print('private tests per task: median', S.median(a for a, b in stats), 'max', max(a for a, b in stats))
print('private bytes per task: median', S.median(b for a, b in stats), 'p90', sorted(b for a, b in stats)[int(.9 * n)], 'max', max(b for a, b in stats))

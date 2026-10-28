"""Offline checks (no model calls): test-set rebuild == ADAS task_queue, adapter parsing, FORMAT_INST key order."""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.expanduser('~/shi_eval/adas_p4'))
import adas_port as P, run_eval as R

dom = sys.argv[1]
S, U = P.load_domain(dom)
args = P.adas_args(dom, max_workers=4)
print('args', vars(args))
items = P.test_items(U, dom, args)
print('items', len(items), 'first gold', items[0][1], '| task head', repr(items[0][0][:90]))
recs = P.Evaluation(S, dom, 'offline_check', items, 6).run("def forward(self, taskInfo):\n    return None\n", args)
print('task_ok', [r['task_ok'] for r in recs], 'calls', [r['calls'] for r in recs], 'scores', [r['score'] for r in recs])
# format instruction -> requested key order
a = S.LLMAgentBase(['thinking', 'answer', 'confidence'], 'X')
sp, _ = a.generate_prompt([S.Info('task', 'User', 'Q', -1)], 'do it')
print('requested_keys', P.requested_keys(sp)); print('system prompt:', repr(sp))
for t in ['{"thinking": "a", "answer": 5}', '```json\n{"answer": "B", "thinking": "x"}\n```', 'Sure.\n{"a": {"b": 1}} trailing',
          '{"x": "line\nbreak"}', 'no json here', '{"thinking": "unterminated']:
    print(repr(t[:30]), '->', P.extract_json(t))
pk, A = R.picks(dom)
for k, i in pk.items():
    ns = {}; exec(A[i]['code'], vars(S), ns); print(k, i, A[i]['name'], 'compiles:', list(ns))

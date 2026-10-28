"""Adapter unit checks on reply styles seen from claude-haiku-5-5 (no model calls)."""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.expanduser('~/shi_eval/adas_p4'))
import adas_port as P
K2 = ['thinking', 'answer']; K3 = ['final_verdict', 'teacher_feedback', 'student_feedback']
cases = [
 ("```json\n{'thinking': 'The ratio is 7:13, so 20 parts; 120 / 20 = 6. Sugar is 7 * 6 = 42.', 'answer': '42'}\n```", K2, {'thinking': 'The ratio is 7:13, so 20 parts; 120 / 20 = 6. Sugar is 7 * 6 = 42.', 'answer': '42'}, 'pyliteral'),
 ("{'final_verdict': 'The student's answer of 10 liters is correct.', 'teacher_feedback': 'Clear; the 'hint' helped.', 'student_feedback': 'Good, it's right.'}", K3,
  {'final_verdict': "The student's answer of 10 liters is correct.", 'teacher_feedback': "Clear; the 'hint' helped.", 'student_feedback': "Good, it's right."}, 'keyed'),
 ("```json\n{'thinking': 'Uwiano wa sukari ni 7:13. Ni 'sawa'.', 'answer': 42}\n```", K2, {'thinking': "Uwiano wa sukari ni 7:13. Ni 'sawa'.", 'answer': '42'}, 'keyed'),
 ('{"thinking": "He said "hi" twice", "answer": "B"}', K2, {'thinking': 'He said "hi" twice', 'answer': 'B'}, 'keyed'),
 ("{'thinking': 'x', 'answer': 'C',}", K2, {'thinking': 'x', 'answer': 'C'}, 'pyliteral'),
 ('{"answer": "D", "thinking": "reordered"}', K2, {'answer': 'D', 'thinking': 'reordered'}, 'direct'),
 ("{'thinking': 'truncated reply with no clos", K2, None, 'fail'),
 ("I think the answer is B.", K2, None, 'fail'),
]
bad = 0
for text, keys, want, how in cases:
    d, h = P.extract_json(text, keys)
    if d is not None: d = {k: P._to_str(v)[0] for k, v in d.items()}
    ok = (d == want and h == how)
    bad += not ok
    print('OK ' if ok else 'BAD', h, d if not ok else '')
print('bad', bad)
sys.exit(1 if bad else 0)

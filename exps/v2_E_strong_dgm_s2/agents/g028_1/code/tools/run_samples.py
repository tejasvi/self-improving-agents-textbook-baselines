import re
import os
import subprocess
import sys
import difflib
import tempfile

_MAX_CLIP = 3000


def tool_info():
    return {
        "name": "run_samples",
        "description": """Run a stdin/stdout Python solution on the sample test cases of a problem and compare its output with the expected sample output EXACTLY (after whitespace normalization of line ends and surrounding blanks).\n
* Provide either `statement_text` (the raw problem statement; sample blocks such as 'Sample Input 1' / 'Sample Output 1', 'Example', 'Input:' / 'Output:' are parsed automatically) or `samples` (a list of {input, output} objects).\n
* Returns a per-sample PASS/MISMATCH report with expected output, actual output and a unified diff, followed by a summary line 'x/y samples exactly matched'.\n
* A MISMATCH on a problem that accepts any valid answer still matters: graders may compare exactly, so try canonical variants of the construction until all samples match.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python solution file (run as `python3 <solution_path>` with the sample input on stdin)."
                },
                "statement_text": {
                    "type": "string",
                    "description": "Optional. The raw problem statement text from which sample input/output blocks are extracted."
                },
                "samples": {
                    "type": "array",
                    "description": "Optional. Explicit list of sample pairs; each item is an object with string fields 'input' and 'output'.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "input": {"type": "string", "description": "Sample input text."},
                            "output": {"type": "string", "description": "Expected sample output text."}
                        },
                        "required": ["input", "output"]
                    }
                },
                "timeout": {
                    "type": "integer",
                    "description": "Per-sample time limit in seconds (default 10)."
                }
            },
            "required": ["solution_path"]
        }
    }


def _norm(s):
    lines = [ln.strip() for ln in (s or '').replace('\r\n', '\n').replace('\r', '\n').split('\n')]
    while lines and lines[-1] == '':
        lines.pop()
    while lines and lines[0] == '':
        lines.pop(0)
    return '\n'.join(lines)


def _clip(s, n=_MAX_CLIP):
    s = s or ''
    if len(s) <= n:
        return s
    return s[: n // 2] + f"\n... <{len(s) - n} characters clipped> ...\n" + s[-n // 2:]


def parse_samples(text):
    """Tolerant extraction of (input, output) pairs from a statement."""
    if not text:
        return []
    pairs = []
    # Header-based blocks: 'Sample Input 1' / 'Sample Output 1', 'Example Input', 'Input:' / 'Output:'
    hdr = re.compile(
        r'^[ \t#*_]*(?:(?:sample|example)[ \t]*)?(input|output)\b[ \t]*(?:#?[ \t]*\d+)?[ \t]*[:.]?[*_ \t]*$',
        re.IGNORECASE | re.MULTILINE)
    matches = list(hdr.finditer(text))
    ins, outs = [], []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end]
        # Stop the body at the next section heading-ish line (e.g. '### Note') if present
        body = re.split(r'\n[ \t#*_]*(?:note|explanation|example\b|sample\b|constraints|input\b|output\b)', body,
                        flags=re.IGNORECASE)[0]
        body = body.strip('\n')
        kind = m.group(1).lower()
        if kind == 'input':
            ins.append(body)
        else:
            outs.append(body)
    # Pair in order; a dangling input followed by output is the usual case.
    if ins and len(ins) == len(outs):
        for a, b in zip(ins, outs):
            if a.strip() or b.strip():
                pairs.append({'input': a, 'output': b})
    else:
        # Fallback: 'Input' header followed directly by its 'Output' in sequence
        seq = [(m.group(1).lower(), text[m.end():(matches[i + 1].start() if i + 1 < len(matches) else len(text))])
               for i, m in enumerate(matches)]
        cur_in = None
        for kind, body in seq:
            body = body.strip('\n')
            if kind == 'input':
                cur_in = body
            elif cur_in is not None:
                pairs.append({'input': cur_in, 'output': body})
                cur_in = None
    return pairs


def _run(solution_path, inp, timeout):
    try:
        p = subprocess.run([sys.executable, solution_path], input=inp, capture_output=True, text=True,
                           timeout=timeout, errors='replace')
    except subprocess.TimeoutExpired:
        return None, f"Error: timed out after {timeout} seconds."
    if p.returncode != 0:
        return p.stdout, f"Error: exit code {p.returncode}\n{_clip(p.stderr, 1500)}"
    return p.stdout, None


def tool_function(solution_path, statement_text=None, samples=None, timeout=10):
    try:
        timeout = max(1, min(int(timeout or 10), 120))
    except Exception:
        timeout = 10
    if not solution_path or not os.path.exists(solution_path):
        return f"Error: solution file not found: {solution_path}"

    pairs = []
    if samples:
        for s in samples:
            if isinstance(s, dict):
                pairs.append({'input': str(s.get('input', '')), 'output': str(s.get('output', ''))})
    if not pairs and statement_text:
        pairs = parse_samples(statement_text)
    if not pairs:
        return ("Error: no sample input/output pairs found. Pass `samples` as a list of {input, output} "
                "objects, or `statement_text` containing 'Sample Input N' / 'Sample Output N' blocks.")

    lines = []
    passed = 0
    for idx, pr in enumerate(pairs, 1):
        inp = pr['input'].rstrip('\n') + '\n'
        exp_raw = pr['output']
        out, err = _run(solution_path, inp, timeout)
        actual_raw = out or ''
        if err is not None:
            lines.append(f"Sample {idx}: MISMATCH (runtime error)")
            lines.append(f"expected:\n{_clip(exp_raw)}")
            lines.append(f"actual:\n{_clip(actual_raw)}")
            lines.append(err)
            lines.append('')
            continue
        exp_n, act_n = _norm(exp_raw), _norm(actual_raw)
        if exp_n == act_n:
            passed += 1
            lines.append(f"Sample {idx}: PASS")
        else:
            lines.append(f"Sample {idx}: MISMATCH")
            lines.append(f"expected:\n{_clip(exp_n)}")
            lines.append(f"actual:\n{_clip(act_n)}")
            diff = difflib.unified_diff(exp_n.split('\n'), act_n.split('\n'),
                                        fromfile='expected', tofile='actual', lineterm='')
            lines.append(_clip('\n'.join(diff)))
        lines.append('')
    total = len(pairs)
    lines.append(f"{passed}/{total} samples exactly matched")
    return '\n'.join(lines)

import os
import re
import subprocess
import time


def tool_info():
    return {
        "name": "run_samples",
        "description": """Run a Python solution against the sample input/output pairs found in a problem statement.

* Parses 'Sample Input N' / 'Sample Output N' blocks (and 'Input:' / 'Output:' blocks) from the problem text.
* Runs `python3 <solution_path>` on each sample input (fed via stdin) with a per-run timeout.
* Compares whitespace-normalized output with the expected output.
* Returns a plain-text report with one entry per sample: PASS, WRONG ANSWER (expected vs actual),
  TIMEOUT, or RUNTIME ERROR (with stderr). The raw results are returned for you to analyze.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python solution file to run, e.g. '/repo/solution.py'."
                },
                "problem_text": {
                    "type": "string",
                    "description": "The problem statement text containing the samples (or a path to a file containing it)."
                },
                "timeout_sec": {
                    "type": "number",
                    "description": "Per-sample timeout in seconds. Defaults to 10."
                }
            },
            "required": ["solution_path", "problem_text"]
        }
    }


_HEADER_RE = re.compile(
    r'^\s*(?:(sample)\s+)?(input|output)\s*(\d*)\s*(:)?\s*(.*?)\s*$',
    re.IGNORECASE,
)
_FENCE_RE = re.compile(r'^\s*```')


def parse_samples(text):
    """
    Return a list of (input_text, expected_output_text) tuples in order of appearance.
    Recognizes headers like 'Sample Input 1', 'Sample Output 1', 'Input:', 'Output:',
    and 'Input 2:' / 'Output 2:'. Markdown code fences are ignored.
    """
    samples = []
    cur_in = None
    cur_out = None
    mode = None  # 'in' or 'out' or None

    def flush():
        nonlocal cur_in, cur_out, mode
        if cur_in is not None and cur_out is not None:
            samples.append((_clean(cur_in), _clean(cur_out)))
        cur_in, cur_out, mode = None, None, None

    for line in (text or '').splitlines():
        if _FENCE_RE.match(line):
            continue
        m = _HEADER_RE.match(line)
        is_header = False
        if m:
            has_sample, kind, _num, colon, rest = m.groups()
            # Only treat as a header if it is clearly a sample header.
            if has_sample or colon or _num:
                is_header = True
                kind = kind.lower()
                if kind == 'input':
                    if cur_out is not None:
                        flush()
                    cur_in = [rest] if rest else []
                    cur_out = None
                    mode = 'in'
                else:
                    if cur_in is None:
                        continue
                    cur_out = [rest] if rest else []
                    mode = 'out'
        if is_header:
            continue
        if mode == 'in':
            cur_in.append(line)
        elif mode == 'out':
            if line.strip().lower().startswith('explanation'):
                flush()
                continue
            if not line.strip() and cur_out and any(l.strip() for l in cur_out):
                flush()
                continue
            cur_out.append(line)
    flush()
    return samples


def _clean(lines):
    text = "\n".join(lines).strip("\n")
    return text.strip()


def _normalize_tokens(text):
    return text.split()


def _load_problem_text(problem_text):
    if problem_text and len(problem_text) < 4096 and '\n' not in problem_text and os.path.isfile(problem_text):
        try:
            with open(problem_text, 'r') as f:
                return f.read()
        except OSError:
            pass
    return problem_text or ''


def tool_function(solution_path, problem_text, timeout_sec=None):
    timeout = float(timeout_sec) if timeout_sec else 10.0
    if not os.path.isfile(solution_path):
        return f"Error: solution file not found: {solution_path}"

    samples = parse_samples(_load_problem_text(problem_text))
    if not samples:
        return "Error: no sample input/output pairs found in the problem text."

    abs_path = os.path.abspath(solution_path)
    cwd = os.path.dirname(abs_path)
    lines = [f"Found {len(samples)} sample(s). Solution: {abs_path}"]
    all_passed = True
    for idx, (inp, expected) in enumerate(samples, start=1):
        input_text = inp + "\n"
        start = time.time()
        try:
            proc = subprocess.run(
                ["python3", abs_path],
                input=input_text,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
            )
        except subprocess.TimeoutExpired:
            all_passed = False
            lines.append(f"Sample {idx}: TIMEOUT (exceeded {timeout}s)\nInput:\n{inp}")
            continue
        elapsed = time.time() - start

        if proc.returncode != 0:
            all_passed = False
            lines.append(
                f"Sample {idx}: RUNTIME ERROR (exit {proc.returncode}, {elapsed:.3f}s)\n"
                f"Input:\n{inp}\nstderr:\n{proc.stderr[-2000:]}"
            )
            continue

        if _normalize_tokens(proc.stdout) == _normalize_tokens(expected):
            lines.append(f"Sample {idx}: PASS ({elapsed:.3f}s)")
        else:
            all_passed = False
            lines.append(
                f"Sample {idx}: WRONG ANSWER ({elapsed:.3f}s)\n"
                f"Input:\n{inp}\nExpected output:\n{expected}\nActual output:\n{proc.stdout.strip()}"
                + (f"\nstderr:\n{proc.stderr[-1000:]}" if proc.stderr.strip() else "")
            )

    lines.append("ALL SAMPLES PASSED." if all_passed else "SOME SAMPLES FAILED.")
    return "\n".join(lines)

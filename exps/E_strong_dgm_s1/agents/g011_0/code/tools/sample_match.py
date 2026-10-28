import os
import subprocess
import sys

MAX_CASES = 200
MAX_TIMEOUT = 60
CLIP = 1500


def tool_info():
    return {
        "name": "sample_match",
        "description": """Check whether a Python solution reproduces the EXACT expected output of every sample case.

* Input: `solution_path` (a Python program that reads stdin and writes stdout) and `cases`, a list of objects, each with `input` (the stdin text) and `expected_output` (the sample output copied from the problem statement).
* For each case it runs `python3 solution_path` with the input on stdin and compares its stdout with expected_output, ignoring only differences in whitespace (line breaks, spaces, tabs, trailing spaces).
* Returns a raw report per case: MATCH or MISMATCH, with the expected and actual output, plus a final summary line `EXACT MATCH: k/n`.
* IMPORTANT: a MISMATCH may still be a valid answer for problems that accept several answers, but a grader without a special checker compares stdout against one reference output and would reject it. Treat any mismatch as a risk: try deterministic variants of the construction (ordering, bit assignment, smallest/largest/first-found answer, iteration direction) until every sample matches exactly, while keeping the answer valid.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python solution file (reads stdin, writes stdout), e.g. /path/to/solution.py."
                },
                "cases": {
                    "type": "array",
                    "description": "List of sample cases. Each case is an object with the stdin text and the expected stdout copied from the problem statement.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "Exact stdin text for this sample."
                            },
                            "expected_output": {
                                "type": "string",
                                "description": "Exact expected stdout text for this sample, copied from the problem statement."
                            }
                        },
                        "required": ["input", "expected_output"]
                    }
                },
                "timeout": {
                    "type": "integer",
                    "description": "Per-case time limit in seconds (default 10)."
                }
            },
            "required": ["solution_path", "cases"]
        }
    }


def _clip(s, n=CLIP):
    s = s or ""
    if len(s) <= n:
        return s
    return s[:n] + f"...<{len(s) - n} more chars>"


def _normalize(s):
    return " ".join((s or "").split())


def tool_function(solution_path, cases, timeout=10):
    try:
        timeout = int(timeout) if timeout is not None else 10
    except (TypeError, ValueError):
        timeout = 10
    timeout = max(1, min(timeout, MAX_TIMEOUT))

    if not isinstance(cases, list) or not cases:
        return "Error: `cases` must be a non-empty array of objects with `input` and `expected_output`."
    if len(cases) > MAX_CASES:
        return f"Error: too many cases ({len(cases)}); the maximum is {MAX_CASES}."
    if not os.path.isfile(solution_path):
        return f"Error: solution file not found: {solution_path}"

    lines = []
    matched = 0
    n = len(cases)
    for i, case in enumerate(cases, 1):
        if not isinstance(case, dict) or "input" not in case or "expected_output" not in case:
            lines.append(f"Case {i}: MISMATCH (malformed case: needs string fields `input` and `expected_output`)")
            continue
        inp = str(case["input"])
        exp = str(case["expected_output"])
        try:
            proc = subprocess.run(
                [sys.executable, solution_path],
                input=inp, capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            lines.append(f"Case {i}: MISMATCH (timed out after {timeout}s)\n"
                         f"  input: {_clip(inp, 300)!r}")
            continue
        except Exception as e:
            lines.append(f"Case {i}: MISMATCH (failed to run: {e})")
            continue

        actual = proc.stdout or ""
        if proc.returncode != 0:
            lines.append(f"Case {i}: MISMATCH (exit code {proc.returncode})\n"
                         f"  input: {_clip(inp, 300)!r}\n"
                         f"  stderr: {_clip(proc.stderr, 600)!r}\n"
                         f"  actual stdout: {_clip(actual)!r}")
            continue

        if _normalize(actual) == _normalize(exp):
            matched += 1
            lines.append(f"Case {i}: MATCH")
        else:
            lines.append(f"Case {i}: MISMATCH\n"
                         f"  input: {_clip(inp, 300)!r}\n"
                         f"  expected: {_clip(exp)!r}\n"
                         f"  actual:   {_clip(actual)!r}")

    lines.append(f"EXACT MATCH: {matched}/{n} samples")
    if matched < n:
        lines.append(
            "WARNING: some samples do not match exactly. Even if your output is a valid answer, "
            "a grader without a special checker compares stdout against one reference output and "
            "would reject it. Try deterministic variants of the construction (ordering, bit assignment, "
            "smallest/largest/first-found answer, iteration direction) until all samples match exactly, "
            "while keeping the answer valid."
        )
    return "\n".join(lines)

import subprocess
import sys
import os
import tempfile


def tool_info():
    return {
        "name": "stress_test",
        "description": """Compare a solution against a canonical brute force on generated inputs, using exact output equality (whitespace-normalized).
* `generator_path` is a Python script that takes one integer argument (the seed) and prints one test input to stdout. It is run for seeds 0..num_tests-1.
* `solution_path` and `brute_path` are Python programs that read stdin and write stdout. Both are run with `python3 -I` on each generated input.
* The brute force should print the canonical answer (the same tie-break rule as the reference), since outputs are compared for exact equality.
* Returns raw data only: on the first mismatch, the input, both outputs, and raw stderr / timeout info. If all tests match, returns a success message with the number of tests run.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the solution Python file under test."
                },
                "brute_path": {
                    "type": "string",
                    "description": "Path to the brute-force reference Python file that prints the canonical answer."
                },
                "generator_path": {
                    "type": "string",
                    "description": "Path to a Python script that takes a seed integer as its argument and prints one input to stdout."
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of seeds to test (seeds 0..num_tests-1). Default 200."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Per-run time limit in seconds. Default 10."
                },
                "max_output_lines": {
                    "type": "integer",
                    "description": "Maximum number of lines shown for each printed block in a failure report. Default 40."
                }
            },
            "required": ["solution_path", "brute_path", "generator_path"]
        }
    }


def _run_py(path, data, timeout, args=()):
    try:
        p = subprocess.run(
            [sys.executable, "-I", path, *args],
            input=data, capture_output=True, text=True, timeout=timeout,
            env={"PATH": os.environ.get("PATH", "")},
        )
        return p.stdout, p.stderr, p.returncode, False
    except subprocess.TimeoutExpired as e:
        out = e.stdout if isinstance(e.stdout, str) else (e.stdout or b"").decode(errors="replace")
        err = e.stderr if isinstance(e.stderr, str) else (e.stderr or b"").decode(errors="replace")
        return out, err, None, True


def _norm(s):
    return " ".join(s.split())


def _clip_lines(text, max_lines):
    """Keep at most max_lines lines (head and tail) so failure reports stay compact."""
    lines = text.splitlines()
    if max_lines is None or max_lines <= 0 or len(lines) <= max_lines:
        return text
    head = max_lines // 2
    tail = max_lines - head
    omitted = len(lines) - head - tail
    return "\n".join(lines[:head] + [f"... <{omitted} lines omitted> ..."] + lines[-tail:])


def run_differential(solution_path, brute_path, generator_path, num_tests=200, timeout=10, max_output_lines=40):
    """Run the differential test over seeds 0..num_tests-1.

    Returns (n_pass, n_total, max_solution_time, failure_text). failure_text is None when all seeds pass.
    Reusable by other tools (e.g. the harness evaluation in coding_agent.py).
    """
    import time
    num_tests = int(num_tests)
    timeout = int(timeout)
    max_time = 0.0
    for i in range(num_tests):
        gen_out, gen_err, gen_rc, gen_to = _run_py(generator_path, "", timeout, args=(str(i),))
        if gen_to or gen_rc != 0:
            return i, num_tests, max_time, (
                f"Generator failed for seed {i}: timeout={gen_to}, exit code={gen_rc}\n"
                f"stderr:\n{_clip_lines(gen_err, max_output_lines)}")
        inp = gen_out
        b_out, b_err, b_rc, b_to = _run_py(brute_path, inp, timeout)
        t0 = time.time()
        s_out, s_err, s_rc, s_to = _run_py(solution_path, inp, timeout)
        max_time = max(max_time, time.time() - t0)
        if b_to or b_rc != 0:
            return i, num_tests, max_time, (
                f"Brute force failed at seed {i}: timeout={b_to}, exit code={b_rc}\n"
                f"INPUT:\n{_clip_lines(inp, max_output_lines)}\n"
                f"BRUTE stderr:\n{_clip_lines(b_err, max_output_lines)}")
        if s_to or s_rc != 0 or _norm(s_out) != _norm(b_out):
            reason = "timed out" if s_to else (f"runtime error (exit code {s_rc})" if s_rc != 0 else "wrong answer")
            text = (
                f"Mismatch at seed {i} (of {num_tests}): {reason}.\n"
                f"INPUT:\n{_clip_lines(inp, max_output_lines)}\n"
                f"EXPECTED (brute) stdout:\n{_clip_lines(b_out, max_output_lines)}\n"
                f"ACTUAL (solution) stdout:\n{_clip_lines(s_out, max_output_lines)}\n"
            )
            if s_err.strip():
                text += f"ACTUAL stderr:\n{_clip_lines(s_err, max_output_lines)}\n"
            return i, num_tests, max_time, text
    return num_tests, num_tests, max_time, None


def tool_function(solution_path, brute_path, generator_path, num_tests=200, timeout=10, max_output_lines=40):
    n_pass, n_total, _, failure = run_differential(
        solution_path, brute_path, generator_path, num_tests=num_tests, timeout=timeout,
        max_output_lines=max_output_lines)
    if failure is not None:
        return failure
    return f"All {n_total} tests passed (exact match after whitespace normalization)."

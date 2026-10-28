import difflib
import os
import subprocess
import tempfile
import time

DEFAULT_TIMEOUT = 10.0


def tool_info():
    return {
        "name": "run_samples",
        "description": """Run a Python solution script against a list of test cases.\n
* Each case is run as `python3 solution_path` with the case's `input` fed to standard input.\n
* A case PASSES if the stripped stdout equals the stripped `expected` string (line endings and trailing whitespace are ignored).\n
* For every case the tool reports PASS/FAIL, the actual stdout, the raw stderr (full traceback, unparsed), the exit code and the elapsed time.\n
* For failing cases whose stdout differs from the expected output, the tool prints a unified diff. Even if the answer is valid, hidden tests may require an exact match, so canonicalize the output to match the sample.\n
* Optional `checker_path`: a Python script run as `python3 checker_path input_file output_file`; it prints OK if the output is valid, otherwise BAD. With it, each case is labeled EXACT, VALID_BUT_DIFFERENT, or INVALID.
* Use this to run all sample tests, and also to check the solution on extra inputs (e.g. stress-test cases or maximum-size inputs).\n
* Pass inputs as exact strings, e.g. "3\\n1 2 3\\n". Do not rely on the shell `echo` to build inputs.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python solution file to run with python3."
                },
                "cases": {
                    "type": "array",
                    "description": "List of test cases to run.",
                    "items": {
                        "type": "object",
                        "description": "A single test case.",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "Exact text fed to the program's standard input."
                            },
                            "expected": {
                                "type": "string",
                                "description": "Exact expected standard output."
                            }
                        },
                        "required": ["input", "expected"]
                    }
                },
                "timeout": {
                    "type": "number",
                    "description": "Timeout in seconds for each case. Defaults to 10 if omitted."
                },
                "exact_required": {
                    "type": "boolean",
                    "description": "If true (default), a case whose output differs from expected is reported as a failure with a diff, because hidden tests may compare exactly. Set to false to only report validity-based results."
                },
                "checker_path": {
                    "type": "string",
                    "description": "Optional path to a Python checker script. It is run as `python3 checker_path input_file output_file` and must print OK if the output is valid, or BAD otherwise. Used to label cases as VALID_BUT_DIFFERENT or INVALID."
                }
            },
            "required": ["solution_path", "cases"]
        }
    }


def _normalize(text):
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()


def _run_case(solution_path, case_input, timeout):
    start = time.time()
    try:
        proc = subprocess.run(
            ["python3", solution_path],
            input=case_input,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start
        return proc.stdout, proc.stderr, proc.returncode, elapsed, False
    except subprocess.TimeoutExpired as e:
        elapsed = time.time() - start
        out = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = e.stderr.decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        return out, err, None, elapsed, True


def _run_checker(checker_path, case_input, actual_stdout, timeout):
    tmp_dir = tempfile.mkdtemp(prefix="checker_")
    in_path = os.path.join(tmp_dir, "input.txt")
    out_path = os.path.join(tmp_dir, "output.txt")
    with open(in_path, "w") as f:
        f.write(case_input)
    with open(out_path, "w") as f:
        f.write(actual_stdout)
    try:
        proc = subprocess.run(
            ["python3", checker_path, in_path, out_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        verdict = proc.stdout.strip().split("\n")[0].strip() if proc.stdout.strip() else ""
        return verdict.upper() == "OK"
    except subprocess.TimeoutExpired:
        return False


def tool_function(solution_path, cases, timeout=None, exact_required=True, checker_path=None):
    if timeout is None:
        timeout = DEFAULT_TIMEOUT
    timeout = float(timeout)
    if exact_required is None:
        exact_required = True
    exact_required = bool(exact_required)

    if not isinstance(cases, list) or len(cases) == 0:
        return "Error: 'cases' must be a non-empty list of objects with 'input' and 'expected'."

    results = []
    passed = 0
    for idx, case in enumerate(cases, start=1):
        case_input = case.get("input", "")
        expected = case.get("expected", "")
        stdout, stderr, returncode, elapsed, timed_out = _run_case(solution_path, case_input, timeout)
        matches = _normalize(stdout) == _normalize(expected)
        ran_ok = (not timed_out) and returncode == 0
        ok = ran_ok and matches
        label = None
        if checker_path and ran_ok:
            valid = _run_checker(checker_path, case_input, stdout, timeout)
            if matches:
                label = "EXACT"
            elif valid:
                label = "VALID_BUT_DIFFERENT"
            else:
                label = "INVALID"
            if not exact_required and valid:
                ok = True
        elif checker_path:
            label = "INVALID"
        if ok:
            passed += 1
        status = "PASS" if ok else "FAIL"
        block = [f"=== Case {idx}: {status} ==="]
        if label is not None:
            block.append(f"Label: {label}")
        if timed_out:
            block.append(f"TIMED OUT after {timeout}s")
        block.append(f"Exit code: {returncode}")
        block.append(f"Elapsed: {elapsed:.3f}s")
        block.append(f"--- input ---\n{case_input}")
        block.append(f"--- expected ---\n{expected}")
        block.append(f"--- actual stdout ---\n{stdout}")
        block.append(f"--- stderr ---\n{stderr}")
        if not ok and ran_ok and not matches:
            diff_lines = difflib.unified_diff(
                _normalize(expected).split("\n"),
                _normalize(stdout).split("\n"),
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
            diff_text = "\n".join(diff_lines)
            if exact_required:
                block.append("OUTPUT DIFFERS FROM SAMPLE: even if the answer is valid, hidden tests may require exact match; try to canonicalize to the sample output")
            else:
                block.append("OUTPUT DIFFERS FROM SAMPLE (exact_required=false, so this is informational)")
            block.append(f"--- diff (expected -> actual) ---\n{diff_text}")
        results.append("\n".join(block))

    summary = f"Summary: {passed}/{len(cases)} cases passed."
    return summary + "\n\n" + "\n\n".join(results)

import difflib
import subprocess


def tool_info():
    return {
        "name": "run_samples",
        "description": """Run a Python solution program on a list of sample inputs and compare its output with the expected outputs.\n
* The solution is executed as `python3 solution_path`, with each sample's `input` written to standard input.\n
* Output is compared to `expected` line by line after stripping trailing whitespace, so the comparison is exact otherwise.\n
* Returns a report with PASS/FAIL for every sample. For failing samples it includes a unified diff (expected vs actual), the actual output, and stderr.\n
* Use it on ALL samples from the problem statement. Any mismatch is a bug to fix, even if the statement says any valid answer is accepted.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python solution file to run (executed with python3)."
                },
                "samples": {
                    "type": "array",
                    "description": "List of sample test cases. Each item is an object with an 'input' string (fed to stdin) and an 'expected' string (expected stdout).",
                    "items": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "Exact standard input for the sample."
                            },
                            "expected": {
                                "type": "string",
                                "description": "Exact expected standard output for the sample."
                            }
                        },
                        "required": ["input", "expected"]
                    }
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds for each sample run. Defaults to 10."
                }
            },
            "required": ["solution_path", "samples"]
        }
    }


def _normalize_lines(text):
    return [line.rstrip() for line in text.splitlines()]


def tool_function(solution_path, samples, timeout=10):
    if timeout is None:
        timeout = 10
    if not samples:
        return "Error: no samples provided."

    reports = []
    passed = 0
    for idx, sample in enumerate(samples, start=1):
        sample_input = sample.get("input", "")
        expected = sample.get("expected", "")
        header = f"=== Sample {idx} ==="
        try:
            proc = subprocess.run(
                ["python3", solution_path],
                input=sample_input,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as e:
            stderr = e.stderr
            if isinstance(stderr, bytes):
                stderr = stderr.decode(errors="replace")
            reports.append(
                f"{header}\nFAIL (timed out after {timeout}s)\n"
                f"--- stderr ---\n{stderr or ''}"
            )
            continue
        except Exception as e:
            reports.append(f"{header}\nFAIL (could not run solution: {e})")
            continue

        actual = proc.stdout
        exp_lines = _normalize_lines(expected)
        act_lines = _normalize_lines(actual)
        if proc.returncode == 0 and exp_lines == act_lines:
            passed += 1
            reports.append(f"{header}\nPASS")
            continue

        diff = "\n".join(
            difflib.unified_diff(
                exp_lines,
                act_lines,
                fromfile="expected",
                tofile="actual",
                lineterm="",
            )
        )
        status = "FAIL"
        if proc.returncode != 0:
            status += f" (exit code {proc.returncode})"
        reports.append(
            f"{header}\n{status}\n"
            f"--- diff (expected vs actual) ---\n{diff or '(no line differences)'}\n"
            f"--- actual output ---\n{actual}\n"
            f"--- stderr ---\n{proc.stderr}"
        )

    summary = f"Summary: {passed}/{len(samples)} samples passed."
    return "\n\n".join(reports) + "\n\n" + summary

import subprocess

MAX_OUTPUT_CHARS = 4000
DEFAULT_TIMEOUT = 20  # seconds per test case


def tool_info():
    return {
        "name": "run_io_tests",
        "description": """Run a program on several stdin inputs and compare its stdout with the expected outputs.

* `command` is the shell command that runs the solution and reads from standard input, e.g. 'python3 solution.py'.
* Each entry in `test_cases` has an `input` (fed to stdin) and an `expected_output` (compared with stdout).
* Comparison ignores trailing whitespace on each line and trailing blank lines.
* Returns a summary with PASS/FAIL for every case; for failing cases it shows the expected output, the actual output, and stderr.
* This tool does NOT modify any files.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command that runs the solution and reads stdin, e.g. 'python3 solution.py'."
                },
                "test_cases": {
                    "type": "array",
                    "description": "The list of test cases to run.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "Exact text to feed to the program's standard input."
                            },
                            "expected_output": {
                                "type": "string",
                                "description": "Exact expected text the program should print to standard output."
                            }
                        },
                        "required": ["input", "expected_output"]
                    }
                },
                "working_dir": {
                    "type": "string",
                    "description": "Optional directory in which to run the command. Defaults to the current directory."
                }
            },
            "required": ["command", "test_cases"]
        }
    }


def _normalize(text):
    lines = [line.rstrip() for line in (text or "").replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def _truncate(text):
    if len(text) > MAX_OUTPUT_CHARS:
        return text[:MAX_OUTPUT_CHARS] + "\n... [truncated]"
    return text


def _run_case(command, test_input, cwd, timeout):
    """Run one test case. Returns (status, actual_stdout, stderr)."""
    try:
        proc = subprocess.run(
            command,
            shell=True,
            input=test_input,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", f"Timed out after {timeout} seconds"
    if proc.returncode != 0:
        return "ERROR", proc.stdout, proc.stderr
    return "OK", proc.stdout, proc.stderr


def tool_function(command, test_cases, working_dir=None):
    try:
        if not isinstance(test_cases, list) or not test_cases:
            return "Error: `test_cases` must be a non-empty list of objects with 'input' and 'expected_output'."

        results = []
        passed = 0
        for idx, case in enumerate(test_cases, start=1):
            if not isinstance(case, dict) or "input" not in case or "expected_output" not in case:
                results.append(f"Case {idx}: FAIL (malformed test case, needs 'input' and 'expected_output')")
                continue

            test_input = str(case["input"])
            expected = str(case["expected_output"])
            status, actual, stderr = _run_case(command, test_input, working_dir, DEFAULT_TIMEOUT)

            if status == "OK" and _normalize(actual) == _normalize(expected):
                passed += 1
                results.append(f"Case {idx}: PASS")
                continue

            if status == "OK":
                reason = "output mismatch"
            elif status == "TIMEOUT":
                reason = "timeout"
            else:
                reason = "runtime error (non-zero exit code)"
            results.append(
                f"Case {idx}: FAIL ({reason})\n"
                f"--- input ---\n{_truncate(test_input)}\n"
                f"--- expected output ---\n{_truncate(expected)}\n"
                f"--- actual output ---\n{_truncate(actual or '')}\n"
                f"--- stderr ---\n{_truncate(stderr or '')}"
            )

        summary = f"{passed}/{len(test_cases)} test cases passed."
        return summary + "\n\n" + "\n\n".join(results)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print(tool_function(
        "cat",
        [{"input": "hello\n", "expected_output": "hello\n"}, {"input": "a\n", "expected_output": "b\n"}],
    ))

import os
import re
import subprocess
import sys

SAMPLE_PATTERN = re.compile(
    r'Sample Input\s*(\d*)\s*\n(.*?)\nSample Output\s*\1\s*\n(.*?)(?=\nSample Input|\n## Task|\Z)',
    re.S,
)

TIMEOUT_SECONDS = 10


def tool_info():
    return {
        "name": "sample_tester",
        "description": """Extracts all 'Sample Input N' / 'Sample Output N' pairs from the problem statement, runs the given Python solution file on each sample input (timeout 10s), and reports for each sample whether the actual stdout matches the expected output exactly (token-wise comparison), together with the expected output, the actual output and the raw stderr.

* Pass the full problem statement text as `problem_statement`.
* `solution_path` is the path to the Python solution file to run (default: solution.py).
* The report is returned as plain text; errors are returned raw, not parsed.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "problem_statement": {
                    "type": "string",
                    "description": "The full text of the problem statement containing the sample inputs and outputs."
                },
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python solution file to run on each sample input. Defaults to solution.py."
                }
            },
            "required": ["problem_statement", "solution_path"]
        }
    }


def extract_samples(problem_statement):
    """Return a list of (index, input_text, expected_output_text) tuples."""
    samples = []
    for match in SAMPLE_PATTERN.finditer(problem_statement or ''):
        index = match.group(1) or str(len(samples) + 1)
        samples.append((index, match.group(2), match.group(3)))
    return samples


def _run_one(solution_path, input_text):
    try:
        proc = subprocess.run(
            [sys.executable, solution_path],
            input=input_text if input_text.endswith('\n') else input_text + '\n',
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        return proc.stdout, proc.stderr, proc.returncode, False
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout.decode(errors='replace') if isinstance(e.stdout, bytes) else (e.stdout or '')
        stderr = e.stderr.decode(errors='replace') if isinstance(e.stderr, bytes) else (e.stderr or '')
        return stdout, stderr, None, True


def tool_function(problem_statement, solution_path='solution.py'):
    samples = extract_samples(problem_statement)
    if not samples:
        return "No 'Sample Input N' / 'Sample Output N' pairs found in the problem statement."

    if not os.path.exists(solution_path):
        return f"Solution file not found: {solution_path}"

    lines = []
    passed = 0
    for index, input_text, expected_text in samples:
        actual_stdout, stderr, returncode, timed_out = _run_one(solution_path, input_text.strip('\n') + '\n')
        if timed_out:
            status = 'FAIL (timeout)'
        else:
            match = actual_stdout.split() == expected_text.split()
            status = 'PASS' if match else 'FAIL'
        if status == 'PASS':
            passed += 1
        lines.append(f"=== Sample {index}: {status} ===")
        lines.append("Input:")
        lines.append(input_text.strip('\n'))
        lines.append("Expected output:")
        lines.append(expected_text.strip('\n'))
        lines.append("Actual output:")
        lines.append(actual_stdout.strip('\n'))
        if timed_out:
            lines.append(f"Timed out after {TIMEOUT_SECONDS} seconds.")
        else:
            lines.append(f"Exit code: {returncode}")
        lines.append("Stderr (raw):")
        lines.append(stderr.rstrip('\n'))
        lines.append("")

    lines.insert(0, f"Sample tests: {passed}/{len(samples)} passed (exact token match).")
    lines.insert(1, "")
    return "\n".join(lines)

import os
import subprocess
import tempfile
import time


def tool_info():
    return {
        "name": "stress_test",
        "description": """Stress-test a solution against a brute-force reference on random small inputs.

* generator_cmd is run as: <generator_cmd> <seed>  and must print one test input to stdout.
* solution_cmd and brute_cmd are run with the input on stdin; their stdout is compared (whitespace-trimmed, line by line).
* If checker_cmd is given, it is run as: <checker_cmd> <input_file> <solution_output_file> <brute_output_file>
  and must exit with code 0 when the solution output is valid (use this when multiple answers are valid).
  If brute_cmd is omitted, only the solution is run and the checker (if any) is required to validate it.
* Seeds 1..num_tests are tried in order. Returns 'ALL PASSED' with the max run time, or the first failing seed
  with its input, expected output and actual output, or a timeout notice.
* Commands are executed through the shell; use absolute paths or paths relative to the working directory.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_cmd": {
                    "type": "string",
                    "description": "Shell command that runs the solution; reads stdin and writes stdout. E.g. 'python3 /tmp/sol.py'."
                },
                "brute_cmd": {
                    "type": "string",
                    "description": "Shell command for the brute-force reference solution. Optional if checker_cmd is given."
                },
                "generator_cmd": {
                    "type": "string",
                    "description": "Shell command for the input generator. It is called with the seed as its single argument and prints one input to stdout. E.g. 'python3 /tmp/gen.py'."
                },
                "checker_cmd": {
                    "type": "string",
                    "description": "Optional shell command validating a solution output when multiple answers are valid. Called as: <checker_cmd> <input_file> <solution_output_file> <brute_output_file>; exit code 0 means valid."
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of random tests to run (seeds 1..num_tests)."
                },
                "timeout_sec": {
                    "type": "number",
                    "description": "Per-process timeout in seconds. Defaults to 10."
                }
            },
            "required": ["solution_cmd", "generator_cmd", "num_tests"]
        }
    }


def _run(cmd, input_text, timeout):
    """Run a shell command with input_text on stdin. Returns (returncode, stdout, stderr, elapsed, timed_out)."""
    start = time.time()
    try:
        proc = subprocess.run(
            cmd, shell=True, input=input_text, capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode, proc.stdout, proc.stderr, time.time() - start, False
    except subprocess.TimeoutExpired:
        return None, "", "", time.time() - start, True


def _normalize(text):
    return [line.rstrip() for line in text.strip().splitlines()]


def tool_function(solution_cmd, generator_cmd, num_tests, brute_cmd=None, checker_cmd=None, timeout_sec=None):
    timeout = float(timeout_sec) if timeout_sec else 10.0
    num_tests = int(num_tests)
    if num_tests <= 0:
        return "Error: num_tests must be positive."
    if not brute_cmd and not checker_cmd:
        return "Error: provide brute_cmd or checker_cmd to validate outputs."

    max_time = 0.0
    max_time_seed = None
    with tempfile.TemporaryDirectory() as tmpdir:
        for seed in range(1, num_tests + 1):
            rc, input_text, gen_err, _, gen_timeout = _run(f"{generator_cmd} {seed}", "", timeout)
            if gen_timeout:
                return f"Generator timed out on seed {seed}."
            if rc != 0:
                return f"Generator failed on seed {seed} (exit {rc}):\n{gen_err}"

            sol_rc, sol_out, sol_err, sol_t, sol_to = _run(solution_cmd, input_text, timeout)
            if sol_t > max_time:
                max_time, max_time_seed = sol_t, seed
            if sol_to:
                return (
                    f"TIMEOUT: solution exceeded {timeout}s on seed {seed}.\n"
                    f"Input:\n{input_text}"
                )

            brute_out = None
            if brute_cmd:
                br_rc, brute_out, br_err, _, br_to = _run(brute_cmd, input_text, timeout)
                if br_to or br_rc != 0:
                    return f"Brute-force reference failed on seed {seed} (exit {br_rc}, timeout={br_to}):\n{br_err}"

            if sol_rc != 0:
                return (
                    f"RUNTIME ERROR on seed {seed} (exit {sol_rc}).\n"
                    f"Input:\n{input_text}\nstderr:\n{sol_err}"
                )

            if checker_cmd:
                in_path = os.path.join(tmpdir, "input.txt")
                sol_path = os.path.join(tmpdir, "sol_out.txt")
                brute_path = os.path.join(tmpdir, "brute_out.txt")
                with open(in_path, "w") as f:
                    f.write(input_text)
                with open(sol_path, "w") as f:
                    f.write(sol_out)
                with open(brute_path, "w") as f:
                    f.write(brute_out or "")
                ck_rc, ck_out, ck_err, _, ck_to = _run(
                    f"{checker_cmd} {in_path} {sol_path} {brute_path}", "", timeout
                )
                if ck_to or ck_rc != 0:
                    return (
                        f"WRONG ANSWER on seed {seed} (checker exit {ck_rc}).\n"
                        f"Input:\n{input_text}\nSolution output:\n{sol_out}\n"
                        f"Reference output:\n{brute_out or ''}\nchecker output:\n{ck_out}{ck_err}"
                    )
            elif _normalize(sol_out) != _normalize(brute_out):
                return (
                    f"WRONG ANSWER on seed {seed}.\n"
                    f"Input:\n{input_text}\n"
                    f"Expected output (brute):\n{brute_out}\n"
                    f"Actual output (solution):\n{sol_out}"
                )

    result = f"ALL PASSED ({num_tests} tests)."
    if max_time_seed is not None:
        result += f" Max solution run time: {max_time:.3f}s (seed {max_time_seed})."
    return result

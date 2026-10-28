import subprocess

def tool_info():
    return {
        "name": "stress_test",
        "description": """Differential stress tester. Compares a solution program against a reference brute-force program on many random inputs.\n
* Each generator run is `<generator_cmd> <seed>`; its stdout is the test input.\n
* The same input is fed to `<solution_cmd>` and `<brute_cmd>` via stdin.\n
* Runs seeds 1..num_tests and stops at the first case where the stripped outputs differ.\n
* Returns either 'ALL TESTS PASSED' with the number of cases, or the first mismatching input together with the raw outputs of both programs (no parsing is done).\n
* Commands are executed through the shell, so use absolute paths, e.g. `python3 /tmp/stress/brute.py`.\n
* Put scratch files (brute.py, gen.py) outside the repository, e.g. under /tmp.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_cmd": {
                    "type": "string",
                    "description": "Shell command that runs the solution; reads the test input on stdin and writes the answer to stdout."
                },
                "brute_cmd": {
                    "type": "string",
                    "description": "Shell command that runs the brute-force reference solver; reads the test input on stdin and writes the answer to stdout."
                },
                "generator_cmd": {
                    "type": "string",
                    "description": "Shell command that generates a random small test input on stdout. The seed is passed as the last argument."
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of random test cases to run (seeds 1..num_tests)."
                }
            },
            "required": ["solution_cmd", "brute_cmd", "generator_cmd", "num_tests"]
        }
    }

def _run(cmd, stdin_text, timeout):
    """Returns (stdout, error). error is set on timeout; stdout is '' in that case."""
    try:
        proc = subprocess.run(
            cmd, shell=True, input=stdin_text, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "", f"TIMEOUT after {timeout}s"
    out = proc.stdout
    if proc.returncode != 0:
        out += f"\n[exit code {proc.returncode}] stderr:\n{proc.stderr}"
    return out, None

def tool_function(solution_cmd: str, brute_cmd: str, generator_cmd: str, num_tests: int, timeout: float = 10.0) -> str:
    try:
        num_tests = int(num_tests)
    except (TypeError, ValueError):
        return f"Error: num_tests must be an integer, got {num_tests!r}"
    if num_tests <= 0:
        return "Error: num_tests must be positive."

    for seed in range(1, num_tests + 1):
        gen_cmd = f"{generator_cmd} {seed}"
        try:
            gen = subprocess.run(gen_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return f"Error: generator timed out on seed {seed} (command: {gen_cmd})"
        if gen.returncode != 0:
            return f"Error: generator failed on seed {seed} (exit {gen.returncode}): {gen.stderr}"
        test_input = gen.stdout

        sol_out, sol_err = _run(solution_cmd, test_input, timeout)
        brute_out, brute_err = _run(brute_cmd, test_input, timeout)

        if sol_err or brute_err or sol_out.strip() != brute_out.strip():
            return (
                f"MISMATCH at seed {seed} (of {num_tests}).\n"
                f"--- input ---\n{test_input}\n"
                f"--- solution output ({solution_cmd}){' ' + sol_err if sol_err else ''} ---\n{sol_out}\n"
                f"--- brute output ({brute_cmd}){' ' + brute_err if brute_err else ''} ---\n{brute_out}\n"
            )

    return f"ALL TESTS PASSED: {num_tests} random cases matched between solution and brute force."

if __name__ == "__main__":
    print(tool_function("cat", "cat", "echo 1", 3))

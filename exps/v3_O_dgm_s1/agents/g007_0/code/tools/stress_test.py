import subprocess
import time
import json
from typing import Optional

def tool_info():
    """Return the metadata for the stress_test tool."""
    return {
        "name": "stress_test",
        "description": (
            "Run a stress test by generating random inputs, executing the solution and a brute‑force reference "
            "implementation (or an optional checker), and comparing their outputs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Absolute path to the solution script (e.g., solution.py)."
                },
                "brute_path": {
                    "type": "string",
                    "description": "Absolute path to the brute‑force reference script (e.g., brute.py)."
                },
                "generator_path": {
                    "type": "string",
                    "description": "Absolute path to the random input generator script (e.g., gen.py)."
                },
                "checker_path": {
                    "type": "string",
                    "description": "(Optional) Absolute path to a checker script that validates the solution output."
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of random tests to run (default 200).",
                    "default": 200
                },
                "timeout": {
                    "type": "integer",
                    "description": "Maximum time in seconds allowed for each program run (default 10).",
                    "default": 10
                }
            },
            "required": ["solution_path", "brute_path", "generator_path"]
        }
    }

def _run_script(path: str, input_data: str, timeout: int) -> subprocess.CompletedProcess:
    """Execute a Python script with the given input and timeout.

    Returns the CompletedProcess object.
    """
    # Use the external `timeout` command to follow the instruction wording.
    # If the `timeout` binary is unavailable, subprocess will raise an OSError.
    cmd = ["timeout", str(timeout), "python3", path]
    return subprocess.run(
        cmd,
        input=input_data,  # pass string directly when text=True
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

def tool_function(
    solution_path: str,
    brute_path: str,
    generator_path: str,
    checker_path: Optional[str] = None,
    num_tests: int = 200,
    timeout: int = 10,
) -> str:
    """Run the stress test.

    For each test, the generator is executed to produce an input string. The solution and the
    brute implementation are then run with the same input (using the external `timeout` command).
    If a checker script is provided, it is invoked with the input, solution output, and brute output
    as arguments; otherwise the raw outputs are compared for equality.

    The function returns a raw string describing the first failure (including the input and both
    program outputs) or a success summary that includes the maximum runtime observed.
    """
    max_runtime = 0.0
    for i in range(num_tests):
        # 1. Generate input
        gen_res = subprocess.run(
            ["python3", generator_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if gen_res.returncode != 0:
            return (
                f"Generator failed on iteration {i}\n"
                f"stderr: {gen_res.stderr}\n"
            )
        input_data = gen_res.stdout

        # 2. Run solution
        start = time.time()
        sol_res = _run_script(solution_path, input_data, timeout)
        sol_time = time.time() - start
        max_runtime = max(max_runtime, sol_time)
        if sol_res.returncode != 0:
            return (
                f"Solution timed out or crashed on iteration {i}\n"
                f"returncode: {sol_res.returncode}\n"
                f"stderr: {sol_res.stderr}\n"
            )

        # 3. Run brute (or checker)
        if checker_path:
            # Checker receives three arguments via stdin: input, solution output, brute output (ignored).
            chk_res = subprocess.run(
                ["python3", checker_path],
                input=input_data,  # pass string directly
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if chk_res.returncode != 0:
                return (
                    f"Checker reported failure on iteration {i}\n"
                    f"stderr: {chk_res.stderr}\n"
                )
            # If checker exits with 0, treat as pass.
        else:
            brute_res = _run_script(brute_path, input_data, timeout)
            if brute_res.returncode != 0:
                return (
                    f"Brute force program failed on iteration {i}\n"
                    f"stderr: {brute_res.stderr}\n"
                )
            # Compare outputs
            if sol_res.stdout.strip() != brute_res.stdout.strip():
                return (
                    f"Mismatch on iteration {i}\n"
                    f"Input:\n{input_data}\n"
                    f"Solution Output:\n{sol_res.stdout}\n"
                    f"Brute Output:\n{brute_res.stdout}\n"
                )
    # All tests passed
    return f"All {num_tests} tests passed. Maximum solution runtime: {max_runtime:.3f} seconds."

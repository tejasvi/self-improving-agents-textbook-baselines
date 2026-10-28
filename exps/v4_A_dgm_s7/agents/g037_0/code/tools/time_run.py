import subprocess
import time


def tool_info():
    return {
        "name": "time_run",
        "description": """Run a command on a given input file and report its wall time and whether it timed out.

* The input file is fed to the command's stdin.
* Use this with a max-size worst-case input file to check the solution is fast enough.
* Returns the exit code, wall time in seconds, a timeout flag, and the first lines of stdout.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to run, e.g. 'python3 /tmp/sol.py'."
                },
                "input_file": {
                    "type": "string",
                    "description": "Path to a file whose contents are fed to the command's stdin."
                },
                "timeout_sec": {
                    "type": "number",
                    "description": "Timeout in seconds. Defaults to 10."
                }
            },
            "required": ["command", "input_file"]
        }
    }


def tool_function(command, input_file, timeout_sec=None):
    timeout = float(timeout_sec) if timeout_sec else 10.0
    try:
        with open(input_file, "r") as f:
            data = f.read()
    except OSError as e:
        return f"Error: cannot read input file: {e}"

    start = time.time()
    try:
        proc = subprocess.run(command, shell=True, input=data, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"TIMEOUT after {timeout}s (wall time limit exceeded)."
    elapsed = time.time() - start

    out_lines = proc.stdout.splitlines()
    preview = "\n".join(out_lines[:20])
    if len(out_lines) > 20:
        preview += f"\n... ({len(out_lines) - 20} more lines)"
    return (
        f"exit code: {proc.returncode}\n"
        f"wall time: {elapsed:.3f}s\n"
        f"timed out: no\n"
        f"stdout (first lines):\n{preview}\n"
        f"stderr:\n{proc.stderr[-2000:]}"
    )

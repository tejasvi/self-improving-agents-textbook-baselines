import os
import signal
import subprocess

DEFAULT_TIMEOUT = 120
MAX_TIMEOUT = 900
MAX_OUTPUT_CHARS = 12000


def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell.\n
* Each call runs in a FRESH bash process (`bash -c`): `cd`, shell variables, and activated environments do NOT persist between calls. Use absolute paths, or chain commands with `&&` (e.g. `cd /repo && python3 sol.py < /tmp/in.txt`).\n
* Stdin of the command is closed (/dev/null). To feed input to a program use redirection or pipes, e.g. `python3 /repo/sol.py < /tmp/in1.txt` or `printf '3\\n1 2 3\\n' | python3 /repo/sol.py`.\n
* The command is killed after `timeout` seconds (default 120). Use the `time` builtin or `timeout` command to measure/limit the running time of your solution.\n
* You don't have access to the internet via this tool.\n
* To create multi-line files (tests, brute-force solutions, generators) prefer the editor tool, or a heredoc: `cat > /tmp/gen.py << 'EOF' ... EOF`.\n
* Very long output is truncated (head and tail kept); avoid commands producing huge output.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to run."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Optional timeout in seconds for this command (default 120, max 900)."
                }
            },
            "required": ["command"]
        }
    }


def _truncate(text, limit=MAX_OUTPUT_CHARS):
    if len(text) <= limit:
        return text
    head = limit * 2 // 3
    tail = limit - head
    omitted = len(text) - head - tail
    return text[:head] + f"\n... <{omitted} characters truncated> ...\n" + text[-tail:]


def run_command(command, timeout=None):
    """Run a command in a fresh bash process. Returns (stdout, stderr, returncode, timed_out)."""
    try:
        t = int(timeout) if timeout is not None else DEFAULT_TIMEOUT
    except Exception:
        t = DEFAULT_TIMEOUT
    t = max(1, min(t, MAX_TIMEOUT))

    proc = subprocess.Popen(
        ["/bin/bash", "-c", command],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
        env=os.environ.copy(),
    )
    timed_out = False
    try:
        out, err = proc.communicate(timeout=t)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
        try:
            out, err = proc.communicate(timeout=10)
        except Exception:
            out, err = b"", b""
    out = (out or b"").decode("utf-8", errors="replace")
    err = (err or b"").decode("utf-8", errors="replace")
    return out, err, proc.returncode, timed_out, t


class BashSession:
    """Compatibility wrapper: each run executes in a fresh bash process."""
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self._timeout = timeout

    def run(self, command):
        out, err, _, _, _ = run_command(command, self._timeout)
        return out.strip(), err.strip()


def tool_function(command, timeout=None):
    try:
        out, err, code, timed_out, t = run_command(command, timeout)
        result = ""
        out = out.strip()
        err = err.strip()
        if out:
            result += _truncate(out)
        if err:
            result += "\nError:\n" + _truncate(err)
        if timed_out:
            result += f"\nError: command timed out after {t} seconds and was killed."
        elif code not in (0, None) and not err:
            result += f"\n(exit code {code})"
        elif code not in (0, None):
            result += f"\n(exit code {code})"
        return result.strip()
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        print(tool_function(' '.join(sys.argv[1:])))

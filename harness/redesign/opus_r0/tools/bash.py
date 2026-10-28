import os
import signal
import subprocess


DEFAULT_TIMEOUT = 120
MAX_TIMEOUT = 900
MAX_STREAM_CHARS = 15000


def tool_info():
    return {
        "name": "bash",
        "description": """Run a command in a bash shell (bash -c).\n
* Each call runs in a FRESH shell: `cd`, variables and other shell state do NOT persist between calls. Chain commands with `&&` or `;` within one call.\n
* The default working directory is the task repository (when known).\n
* Standard input is /dev/null, so commands never wait for input. To feed input to a program use a file redirect or a pipe, e.g. `python3 solution.py < /tmp/in1.txt`.\n
* The command is killed after `timeout` seconds (default 120, max 900). For timing a solution, prefer `time timeout 20 python3 solution.py < big.txt > /dev/null`.\n
* Very long output is truncated (head and tail are kept); avoid printing huge outputs.\n
* You don't have access to the internet.\n
* Non-empty stderr is reported after an 'Error:' marker; a non-zero exit code is also reported.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to run."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Optional timeout in seconds (default 120, max 900)."
                }
            },
            "required": ["command"]
        }
    }


class BashSession:
    """Kept for backward compatibility; each command now runs in its own subprocess."""
    def __init__(self):
        self._started = False
        self._timeout = float(DEFAULT_TIMEOUT)

    def run(self, command):
        return tool_function(command)


def _truncate(text, limit=MAX_STREAM_CHARS):
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + f"\n... [{len(text) - limit} characters truncated] ...\n" + text[-half:]


def _kill_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def tool_function(command, timeout=None):
    try:
        t = DEFAULT_TIMEOUT if timeout is None else int(timeout)
    except Exception:
        t = DEFAULT_TIMEOUT
    t = max(1, min(MAX_TIMEOUT, t))

    cwd = os.environ.get("AGENT_WORKDIR")
    if not cwd or not os.path.isdir(cwd):
        cwd = None

    try:
        proc = subprocess.Popen(
            ["/bin/bash", "-c", command],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            start_new_session=True,
            env=os.environ.copy(),
        )
    except Exception as e:
        return f"Error: failed to start command: {e}"

    timed_out = False
    try:
        out, err = proc.communicate(timeout=t)
    except subprocess.TimeoutExpired:
        timed_out = True
        _kill_group(proc)
        try:
            out, err = proc.communicate(timeout=5)
        except Exception:
            out, err = b"", b""

    out = (out or b"").decode("utf-8", errors="replace").strip()
    err = (err or b"").decode("utf-8", errors="replace").strip()

    result = ""
    if out:
        result += _truncate(out)
    if err:
        result += "\nError:\n" + _truncate(err)
    if timed_out:
        result += f"\nError: command timed out after {t} seconds and was killed."
    elif proc.returncode not in (0, None):
        result += f"\n(exit code {proc.returncode})"
    return result.strip()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        print(tool_function(' '.join(sys.argv[1:])))

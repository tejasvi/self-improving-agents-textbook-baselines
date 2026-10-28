import os
import signal
import subprocess

DEFAULT_TIMEOUT = 120
MAX_TIMEOUT = 900
MAX_OUTPUT_CHARS = 15000


def tool_info():
    return {
        "name": "bash",
        "description": """Run a command in a bash shell.\n
* Each call runs in a FRESH, non-interactive bash process: `cd`, shell variables and other state do NOT persist between calls. Use absolute paths or chain commands, e.g. `cd /dir && python3 x.py`.\n
* Standard input is /dev/null, so commands never wait for interactive input. To feed input to a program, redirect from a file: `python3 solution.py < /tmp/in.txt`, or use a heredoc.\n
* The command is killed after `timeout` seconds (default 120, max 900). Use `timeout N cmd` inside the command for finer control of individual programs.\n
* Long output is truncated; avoid commands that print huge amounts of text.\n
* stderr is reported after 'Error:' and a non-zero exit code is reported.\n
* You don't have access to the internet.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to run."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Optional timeout in seconds for the whole command (default 120, max 900)."
                }
            },
            "required": ["command"]
        }
    }


class BashSession:
    """Kept for backward compatibility; each command now runs in its own process."""
    def __init__(self):
        self._timeout = DEFAULT_TIMEOUT

    def run(self, command, timeout=None):
        return _run(command, timeout or self._timeout)


def _truncate(text, max_chars=MAX_OUTPUT_CHARS):
    if len(text) <= max_chars:
        return text
    head = max_chars * 2 // 3
    tail = max_chars - head
    return text[:head] + f"\n... <{len(text) - max_chars} characters truncated> ...\n" + text[-tail:]


def _run(command, timeout):
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
        out, err = proc.communicate(timeout=timeout)
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
    out = (out or b"").decode(errors="replace")
    err = (err or b"").decode(errors="replace")
    return out, err, proc.returncode, timed_out


def tool_function(command, timeout=None):
    try:
        try:
            t = int(timeout) if timeout is not None else DEFAULT_TIMEOUT
        except Exception:
            t = DEFAULT_TIMEOUT
        t = max(1, min(t, MAX_TIMEOUT))
        out, err, code, timed_out = _run(command, t)
        result = ""
        if out.strip():
            result += _truncate(out.strip())
        if err.strip():
            result += "\nError:\n" + _truncate(err.strip())
        if timed_out:
            result += f"\nError: command timed out after {t} seconds and was killed."
        elif code not in (0, None):
            result += f"\n(exit code {code})"
        result = result.strip()
        return result if result else "(no output)"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        print(tool_function(' '.join(sys.argv[1:])))

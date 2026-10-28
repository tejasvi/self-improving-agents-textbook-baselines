import os
import signal
import subprocess

DEFAULT_TIMEOUT = 120
MAX_TIMEOUT = 900
MAX_OUTPUT_CHARS = 20000


def tool_info():
    return {
        "name": "bash",
        "description": """Run a command in a bash shell.\n
* Each call runs in a FRESH, non-interactive bash shell (state such as `cd` or variables is NOT kept between calls). Chain commands, e.g. `cd /work/repo && python3 solution.py < /tmp/in1.txt`.\n
* Standard input of the command is closed (/dev/null). To feed input to a program, use redirection (`< file`), a pipe, or a heredoc.\n
* The command is killed after `timeout` seconds (default 120, max 900). Use `timeout` for long stress tests.\n
* Do not start background processes (`&`); they will be killed or block the call.\n
* You don't have access to the internet via this tool.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Very long output is truncated in the middle; avoid commands that print huge amounts of output.""",
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


def _truncate(text, limit=MAX_OUTPUT_CHARS):
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + f"\n\n... <{len(text) - limit} characters truncated> ...\n\n" + text[-half:]


def _normalize_timeout(timeout):
    try:
        t = float(timeout) if timeout is not None else DEFAULT_TIMEOUT
    except Exception:
        t = DEFAULT_TIMEOUT
    if t <= 0:
        t = DEFAULT_TIMEOUT
    return max(1.0, min(t, float(MAX_TIMEOUT)))


def run_command(command, timeout=DEFAULT_TIMEOUT):
    """Run a command; returns (stdout, stderr, returncode, timed_out)."""
    timeout = _normalize_timeout(timeout)
    shell = "/bin/bash" if os.path.exists("/bin/bash") else "bash"
    proc = subprocess.Popen(
        [shell, "-c", command],
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
    out = (out or b"").decode("utf-8", errors="replace")
    err = (err or b"").decode("utf-8", errors="replace")
    return out, err, proc.returncode, timed_out


def tool_function(command, timeout=None):
    try:
        t = _normalize_timeout(timeout)
        out, err, rc, timed_out = run_command(command, t)
        result = out.strip()
        err = err.strip()
        if err:
            result += "\nError:\n" + err
        if timed_out:
            result += f"\nError: command timed out after {int(t)} seconds and was killed."
        elif rc not in (0, None):
            result += f"\n[exit code {rc}]"
        result = result.strip()
        if not result:
            result = "(no output)"
        return _truncate(result)
    except Exception as e:
        return f"Error: {str(e)}"


class BashSession:
    """Kept for backward compatibility: runs each command in a fresh shell."""
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        self._timeout = timeout

    def run(self, command):
        return tool_function(command, self._timeout)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        print(tool_function(' '.join(sys.argv[1:])))

import os
import signal
import subprocess

DEFAULT_TIMEOUT = 120
MAX_OUTPUT_CHARS = 12000


def tool_info():
    return {
        "name": "bash",
        "description": """Run a command in a bash shell (bash -c).\n
* Each call runs in a FRESH shell: state (cwd, variables) is NOT persistent between calls. Use absolute paths or `cd /dir && ...` inside the same command.\n
* Standard input is /dev/null. To feed input to a program, use redirection, e.g. `python3 solution.py < /tmp/in.txt` or a heredoc.\n
* You don't have access to the internet via this tool.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* To write a file, you can use a heredoc: cat > /tmp/file.py << 'EOF' ... EOF\n
* Avoid commands that produce huge output; long output is truncated.\n
* Commands are killed after `timeout` seconds (default 120). Use `time` or `timeout` to measure/limit run time of programs.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to run."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Optional timeout in seconds (default 120, max 600)."
                }
            },
            "required": ["command"]
        }
    }


class BashSession:
    """Kept for backwards compatibility; each command runs in a fresh shell."""
    def __init__(self):
        self._timeout = DEFAULT_TIMEOUT

    def run(self, command):
        return _run(command, self._timeout)


def _truncate(text, max_chars=MAX_OUTPUT_CHARS):
    if len(text) <= max_chars:
        return text
    half = max_chars // 2
    return text[:half] + f"\n... [truncated {len(text) - max_chars} characters] ...\n" + text[-half:]


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
            proc.kill()
        try:
            out, err = proc.communicate(timeout=5)
        except Exception:
            out, err = b"", b""
    out = (out or b"").decode(errors="replace")
    err = (err or b"").decode(errors="replace")
    return out, err, proc.returncode, timed_out


def tool_function(command, timeout=None):
    try:
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        try:
            timeout = int(timeout)
        except Exception:
            timeout = DEFAULT_TIMEOUT
        timeout = max(1, min(timeout, 600))
        out, err, code, timed_out = _run(command, timeout)
        result = ""
        if out.strip():
            result += _truncate(out.strip())
        if err.strip():
            result += "\nError:\n" + _truncate(err.strip())
        if timed_out:
            result += f"\nError: command timed out after {timeout} seconds and was killed."
        elif code not in (0, None) and not err.strip():
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

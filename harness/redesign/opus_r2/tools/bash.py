import os
import signal
import subprocess

DEFAULT_TIMEOUT = 120
MAX_TIMEOUT = 600
MAX_OUTPUT_CHARS = 20000


def tool_info():
    return {
        "name": "bash",
        "description": """Run a command in a bash shell (bash -c).\n
* Each call runs in a NEW shell: state (cwd, variables) is NOT kept between calls, so use absolute paths or `cd /dir && ...`.\n
* stdin is /dev/null. To feed input to a program, use redirection, e.g. `python3 solution.py < in.txt` or a heredoc.\n
* Commands are killed after `timeout` seconds (default 120, max 600).\n
* You don't have access to the internet.\n
* Long outputs are truncated; avoid commands producing huge output (redirect to a file and inspect with head/tail).\n
* Useful for running solutions on sample inputs, stress testing against brute force, and timing (`time python3 solution.py < big.txt`).""",
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
    """Kept for backward compatibility; commands run via tool_function."""
    def __init__(self):
        self._started = False
        self._timeout = float(DEFAULT_TIMEOUT)

    def run(self, command):
        return tool_function(command)


def _truncate(text):
    if len(text) > MAX_OUTPUT_CHARS:
        half = MAX_OUTPUT_CHARS // 2
        return text[:half] + f"\n... <{len(text) - 2 * half} characters truncated> ...\n" + text[-half:]
    return text


def tool_function(command, timeout=None):
    try:
        t = DEFAULT_TIMEOUT if timeout is None else int(timeout)
    except Exception:
        t = DEFAULT_TIMEOUT
    t = max(1, min(t, MAX_TIMEOUT))

    try:
        proc = subprocess.Popen(
            ["/bin/bash", "-c", command],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
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
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
        try:
            out, err = proc.communicate(timeout=5)
        except Exception:
            out, err = b"", b""

    out = (out or b"").decode(errors="replace").strip()
    err = (err or b"").decode(errors="replace").strip()

    result = ""
    if out:
        result += _truncate(out)
    if err:
        result += "\nError:\n" + _truncate(err)
    if timed_out:
        result += f"\nError: command timed out after {t} seconds and was killed."
    elif proc.returncode not in (0, None):
        result += f"\n(exit code {proc.returncode})"
    result = result.strip()
    return result if result else "(no output)"


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        print(tool_function(' '.join(sys.argv[1:])))

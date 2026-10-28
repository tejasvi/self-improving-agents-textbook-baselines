import os
import signal
import subprocess

DEFAULT_TIMEOUT = 120
MAX_TIMEOUT = 600
MAX_OUTPUT_CHARS = 20000


def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell (each call runs in a fresh `bash -c`; shell state such as cwd or variables is NOT kept between calls, but files persist).\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* Standard input is empty (/dev/null); to feed input to a program use a pipe or redirection, e.g. `python3 sol.py < input.txt` or `echo '3 1 2' | python3 sol.py`.\n
* stdout is returned; stderr is returned after an 'Error:' marker; a non-zero exit code is reported.\n
* Very long output is truncated (head and tail are kept), so avoid printing huge data.\n
* Commands are killed after the timeout (default 120 seconds, max 600).\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.""",
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
    """Kept for backward compatibility; commands are executed via tool_function."""
    def __init__(self):
        self._timeout = DEFAULT_TIMEOUT

    def run(self, command):
        return tool_function(command, self._timeout)


def _truncate(s, limit=MAX_OUTPUT_CHARS):
    if len(s) > limit:
        half = limit // 2
        return s[:half] + f"\n... <{len(s) - limit} characters truncated> ...\n" + s[-half:]
    return s


def tool_function(command, timeout=None):
    try:
        t = DEFAULT_TIMEOUT if not timeout else max(1, min(int(timeout), MAX_TIMEOUT))
    except Exception:
        t = DEFAULT_TIMEOUT
    try:
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
                proc.kill()
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
        elif proc.returncode != 0:
            result += f"\n(exit code {proc.returncode})"
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

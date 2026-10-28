import os
import subprocess

_STATE = {'cwd': None}

def tool_info():
    return {
        "name": "bash",
        "description": """Run a bash command and return its output.\n
* Each call runs in a fresh non-interactive shell with stdin closed (programs that read stdin must be given input, e.g. `python3 solution.py < input.txt`).\n
* The working directory persists between calls (a `cd` carries over); environment variables do not.\n
* Default time limit is 60 seconds; pass `timeout` (max 300) for longer commands.\n
* Long outputs are truncated (head and tail are kept). There is no internet access.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The bash command to run."},
                "timeout": {"type": "integer", "description": "Time limit in seconds (default 60, max 300)."}
            },
            "required": ["command"]
        }
    }

def _clip(s, n=4000):
    if len(s) <= n:
        return s
    return s[: n // 2] + f"\n... <{len(s) - n} characters clipped> ...\n" + s[-n // 2:]

def tool_function(command=None, timeout=60):
    if not command or not str(command).strip():
        return "Error: bash requires a `command` argument (a non-empty string). Re-issue the call with `command` set."
    cwd = _STATE['cwd'] or os.getcwd()
    timeout = max(1, min(int(timeout or 60), 300))
    marker = '__CWD_MARKER__'
    script = f"cd {cwd!r} 2>/dev/null; {command}\n__rc=$?; echo; echo {marker}$(pwd); exit $__rc"
    try:
        p = subprocess.run(['bash', '-c', script], stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=timeout, errors='replace')
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or '') if isinstance(e.stdout, str) else ''
        return _clip(out) + f"\nError: command timed out after {timeout} seconds."
    out = p.stdout
    if marker in out:
        out, _, newcwd = out.rpartition(marker)
        _STATE['cwd'] = newcwd.strip() or cwd
    res = out.rstrip()
    if p.stderr.strip():
        res += "\nSTDERR:\n" + p.stderr.rstrip()
    if p.returncode != 0:
        res += f"\n(exit code {p.returncode})"
    return _clip(res.strip()) or "(no output)"

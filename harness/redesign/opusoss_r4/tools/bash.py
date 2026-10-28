import asyncio
import os
import signal

MAX_OUTPUT_CHARS = 20000


def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* Each call runs in a FRESH shell: shell state (cwd, variables) is NOT kept between calls. Use absolute paths, or chain commands with && in one call.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Never run a program that reads standard input without providing input (use `< file`, a pipe, or a heredoc), otherwise it hangs until timeout.\n
* Commands time out after 120 seconds; use `timeout 10 ...` for programs that might be slow or loop forever.\n
* Output longer than 20000 characters is truncated; avoid commands that produce huge output.\n
* Useful for writing helper scripts (e.g. under /tmp), running tests, brute-force comparisons and timing.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to run."
                }
            },
            "required": ["command"]
        }
    }

class BashSession:
    """A session of a bash shell."""
    def __init__(self):
        self._started = False
        self._process = None
        self._timed_out = False
        self._timeout = 120.0  # seconds
        self._sentinel = "<<exit>>"
        self._output_delay = 0.2  # seconds

    async def start(self):
        if self._started:
            return
        self._process = await asyncio.create_subprocess_shell(
            "/bin/bash -i",
            preexec_fn=os.setsid,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=os.environ.copy(),
            limit=64 * 1024 * 1024,
        )
        self._started = True

    def stop(self):
        if not self._started:
            return
        try:
            if self._process.returncode is None:
                try:
                    os.killpg(os.getpgid(self._process.pid), signal.SIGKILL)
                except Exception:
                    self._process.kill()
        except Exception:
            pass
        self._process = None
        self._started = False

    async def run(self, command):
        if not self._started:
            raise ValueError("Session has not started.")
        if self._process.returncode is not None:
            raise ValueError(f"Bash has exited with returncode {self._process.returncode}")
        if self._timed_out:
            raise ValueError(
                f"Timed out: bash has not returned in {self._timeout} seconds and must be restarted."
            )

        self._process.stdin.write(
            command.encode() + f"\necho '{self._sentinel}'\n".encode()
        )
        await self._process.stdin.drain()

        try:
            output = None
            stderr_data = ''
            max_iters = int(self._timeout / self._output_delay) + 1
            for _ in range(max_iters):
                await asyncio.sleep(self._output_delay)
                stdout_data = self._process.stdout._buffer.decode(errors='ignore')
                stderr_data = self._process.stderr._buffer.decode(errors='ignore')
                if self._sentinel in stdout_data:
                    output = stdout_data[: stdout_data.index(self._sentinel)]
                    break

            if output is None:
                self._timed_out = True
                raise ValueError(
                    f"Timed out: command did not finish in {self._timeout} seconds (it was killed). "
                    f"If it reads stdin, provide input; otherwise make it faster or use `timeout`."
                )

            self._process.stdout._buffer.clear()
            self._process.stderr._buffer.clear()

            return output.strip(), stderr_data.strip()

        except Exception as e:
            self._timed_out = True
            raise ValueError(str(e))

def filter_error(error):
    filtered_lines = []
    i = 0
    error_lines = error.splitlines()
    n = len(error_lines)
    while i < n:
        line = error_lines[i]
        if "Inappropriate ioctl for device" in line or "no job control in this shell" in line:
            i += 1
            continue
        if line.strip() == '<<exit>>' or line.strip().endswith("echo '<<exit>>'"):
            i += 1
            continue
        filtered_lines.append(line)
        i += 1
    return '\n'.join(filtered_lines).strip()

def truncate(s, limit=MAX_OUTPUT_CHARS):
    if len(s) > limit:
        half = limit // 2
        return s[:half] + f"\n... <output truncated, {len(s) - limit} chars omitted> ...\n" + s[-half:]
    return s

async def tool_function_call(command):
    """Execute a command in the bash shell."""
    bash_session = BashSession()
    try:
        await bash_session.start()
        output, error = await bash_session.run(command)
        error = filter_error(error)
        result = ""
        if output:
            result += truncate(output)
        if error:
            result += "\nError:\n" + truncate(error)
        return result.strip()
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        bash_session.stop()

def tool_function(command):
    return asyncio.run(tool_function_call(command))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        input_command = ' '.join(sys.argv[1:])
        result = tool_function(input_command)
        print(result)

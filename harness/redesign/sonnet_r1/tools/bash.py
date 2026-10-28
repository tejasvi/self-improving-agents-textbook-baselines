import asyncio
import os
import signal
import subprocess

COMMAND_TIMEOUT = 180  # seconds
MAX_OUTPUT_CHARS = 8000

def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* Each call runs in a fresh shell (state such as cwd/env vars is NOT kept between calls); stdin is empty, so never rely on reading from stdin interactively. Use files or pipes (e.g. `python3 sol.py < input.txt`).\n
* Commands are killed after 180 seconds; use `timeout N cmd` for potentially slow programs.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.""",
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
            env=os.environ.copy()  # Ensures inheritance of the current environment
        )
        self._started = True

    def stop(self):
        if not self._started:
            return
        if self._process.returncode is None:
            self._process.terminate()
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
        
        # Send command
        self._process.stdin.write(
            command.encode() + f"; echo '{self._sentinel}'\n".encode()
        )
        await self._process.stdin.drain()

        # Read output until sentinel
        try:
            output = ''
            start_time = asyncio.get_event_loop().time()
            
            while True:
                if asyncio.get_event_loop().time() - start_time > self._timeout:
                    self._timed_out = True
                    raise ValueError(
                        f"Timed out: bash has not returned in {self._timeout} seconds and must be restarted."
                    )
                
                await asyncio.sleep(self._output_delay)
                # Read from the internal buffer
                stdout_data = self._process.stdout._buffer.decode(errors='ignore')
                stderr_data = self._process.stderr._buffer.decode(errors='ignore')
                
                if self._sentinel in stdout_data:
                    output = stdout_data[: stdout_data.index(self._sentinel)]
                    break

            # Clear buffers
            self._process.stdout._buffer.clear()
            self._process.stderr._buffer.clear()

            output = output.strip()
            error = stderr_data.strip()

            return output, error

        except Exception as e:
            self._timed_out = True
            raise ValueError(str(e))

def filter_error(error):
    # Filter out errors that we do not want to see
    filtered_lines = []
    i = 0
    error_lines = error.splitlines()
    while i < len(error_lines):
        line = error_lines[i]

        # Skip the next lines if ioctl error, add relevant lines
        if "Inappropriate ioctl for device" in line:
            i += 3
            if i < len(error_lines) and '<<exit>>' in error_lines[i]:
                i += 1
            while i < len(error_lines) - 1:
                filtered_lines.append(error_lines[i])
                i += 1
            i += 1
            continue

        filtered_lines.append(line)
        i += 1
    return '\n'.join(filtered_lines).strip()

def _truncate(text, max_chars=MAX_OUTPUT_CHARS):
    if len(text) <= max_chars:
        return text
    half = max_chars // 2
    return text[:half] + "\n...<output truncated>...\n" + text[-half:]

def tool_function(command):
    """Execute a command in a fresh bash process with stdin closed and a timeout."""
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
            out_b, err_b = proc.communicate(timeout=COMMAND_TIMEOUT)
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
                out_b, err_b = proc.communicate(timeout=5)
            except Exception:
                out_b, err_b = b"", b""

        output = (out_b or b"").decode(errors="replace").strip()
        error = (err_b or b"").decode(errors="replace").strip()
        output = _truncate(output)
        error = _truncate(error)

        result = ""
        if output:
            result += output
        if timed_out:
            result += f"\nError:\nCommand timed out after {COMMAND_TIMEOUT} seconds and was killed."
        if error:
            result += "\nError:\n" + error
        return result.strip()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Example usage
    import sys

    # Check if the script is called with arguments
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        # Extract the command from the command-line arguments
        input_command = ' '.join(sys.argv[1:])
        result = tool_function(input_command)
        print(result)

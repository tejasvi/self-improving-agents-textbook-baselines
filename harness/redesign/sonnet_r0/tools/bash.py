import asyncio
import os
import signal
import subprocess

def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* Each call runs in a fresh shell with a hard timeout of 120 seconds (the command is killed on timeout); use `timeout N` for programs that may run long.\n
* Standard input is empty; redirect files into programs with `< file`.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output, and avoid `find` over large directory trees.\n
* If you start a background process, redirect its stdout/stderr to a file (e.g. `cmd > out.txt 2>&1 &`).""",
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

def _truncate(text, max_len=20000):
    if len(text) > max_len:
        half = max_len // 2
        return text[:half] + "\n<output clipped>\n" + text[-half:]
    return text

def tool_function(command):
    """Execute a command in a fresh bash shell with a hard timeout."""
    timeout = 120
    try:
        proc = subprocess.Popen(
            ["/bin/bash", "-c", command],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            preexec_fn=os.setsid,
            env=os.environ.copy(),
        )
        try:
            out, err = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except Exception:
                pass
            try:
                out, err = proc.communicate(timeout=5)
            except Exception:
                out, err = "", ""
            partial = _truncate((out or "").strip(), 5000)
            return (
                f"Error: command timed out after {timeout} seconds and was killed.\n"
                f"Partial output:\n{partial}"
            ).strip()

        result = ""
        out = (out or "").strip()
        err = (err or "").strip()
        if out:
            result += out
        if err:
            result += "\nError:\n" + err
        return _truncate(result.strip())
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

import asyncio
import os
import signal

def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* State is persistent across command calls and discussions with the user.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.\n
* Commands time out after about 120 seconds. On timeout the shell is killed and restarted automatically, so you can keep working; wrap long-running programs with `timeout N cmd` (e.g. `timeout 10 python3 sol.py`).\n
* Avoid long compound commands (many chained `&&`/`;` steps or long loops). Run heavy steps as separate calls.\n
* There is no `restart` parameter. Do not pass one; just issue a new command.""",
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
    def __init__(self, timeout=120.0):
        self._started = False
        self._process = None
        self._timed_out = False
        self._timeout = timeout  # seconds
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

    def _kill_process_group(self):
        """Kill the shell and any children it spawned (the shell runs in its own session)."""
        if self._process is None:
            return
        try:
            os.killpg(self._process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            try:
                self._process.kill()
            except ProcessLookupError:
                pass

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

        # Read output until sentinel, bounded by a deadline
        loop = asyncio.get_event_loop()
        deadline = loop.time() + self._timeout
        output = ''
        stdout_data = ''
        stderr_data = ''
        found = False
        while loop.time() < deadline:
            await asyncio.sleep(self._output_delay)
            # Read from the internal buffer
            stdout_data = self._process.stdout._buffer.decode(errors='ignore')
            stderr_data = self._process.stderr._buffer.decode(errors='ignore')
            if self._sentinel in stdout_data:
                output = stdout_data[: stdout_data.index(self._sentinel)]
                found = True
                break

        if not found:
            # Timed out: kill the hung shell and mark this session as restarted
            self._timed_out = True
            self._kill_process_group()
            self._started = False
            self._process = None
            raise ValueError(
                f"Timed out: command did not finish within {self._timeout} seconds. "
                "The bash shell was killed and restarted automatically. "
                "Avoid long compound commands and wrap long-running programs with `timeout N`."
            )

        # Clear buffers
        self._process.stdout._buffer.clear()
        self._process.stderr._buffer.clear()

        output = output.strip()
        error = stderr_data.strip()
        return output, error

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

async def tool_function_call(command):
    """Execute a command in the bash shell."""
    try:
        bash_session = BashSession()

        if not bash_session._started:
            await bash_session.start()

        output, error = await bash_session.run(command)
        error = filter_error(error)
        result = ""
        if output:
            result += output
        if error:
            result += "\nError:\n" + error
        return result.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def tool_function(command):
    return asyncio.run(tool_function_call(command))

if __name__ == "__main__":
    # Example usage
    import sys

    # Check if the script is called with arguments
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        # Extract the command from the command-line arguments
        input_command = ' '.join(sys.argv[1:])
        # Run the tool_function asynchronously
        result = tool_function(input_command)
        print(result)
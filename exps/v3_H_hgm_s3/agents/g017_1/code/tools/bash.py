import asyncio
import os

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
    """
    Remove interactive-shell noise from stderr: job-control/ioctl warnings and the echoed
    prompt/command lines (which contain the sentinel). Keeps only real program errors.
    """
    noise_markers = (
        "Inappropriate ioctl for device",
        "cannot set terminal process group",
        "no job control in this shell",
    )
    kept = []
    for line in error.splitlines():
        if any(m in line for m in noise_markers):
            continue
        if '<<exit>>' in line or line.lstrip().startswith(('bash-', '> ')):
            continue
        kept.append(line)
    return '\n'.join(kept).strip()

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
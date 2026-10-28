import subprocess
import asyncio

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
    """A lightweight Bash session used by the tests.

    The original implementation used an asynchronous interactive shell. For the
    purposes of the test suite we only need a ``run`` method that returns a tuple
    ``(stdout, stderr)``. This implementation executes the command via
    ``subprocess.run`` with ``shell=True`` and captures both streams.
    """
    def __init__(self):
        self._started = False
        self._timeout = 120.0

    async def start(self):
        # No persistent process is required; just mark as started.
        self._started = True

    async def run(self, command: str):
        if not self._started:
            raise ValueError("Session has not started.")
        # Execute the command synchronously in a thread pool to avoid blocking the event loop.
        loop = asyncio.get_event_loop()
        def _run():
            completed = subprocess.run(
                command,
                shell=True,
                executable="/bin/bash",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self._timeout,
            )
            return completed.stdout, completed.stderr, completed.returncode
        stdout, stderr, returncode = await loop.run_in_executor(None, _run)
        return stdout, stderr

def tool_function(command: str) -> str:
    """Execute a bash command and return its combined stdout and stderr.

    The implementation uses ``subprocess.run`` with ``shell=True`` to mimic a
    typical interactive bash session.  Output and error streams are captured and
    concatenated; any leading/trailing whitespace is stripped for a clean
    result.  Errors are reported with the prefix ``Error:`` to be consistent
    with other tools.
    """
    try:
        completed = subprocess.run(
            command,
            shell=True,
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = completed.stdout.strip()
        error = completed.stderr.strip()
        if completed.returncode != 0:
            # Include both output and error for debugging
            result = ""
            if output:
                result += output + "\n"
            result += f"Error: {error}" if error else "Error: Command failed"
            return result.strip()
        # Successful execution – combine stdout and stderr (stderr may contain warnings)
        if error:
            return f"{output}\nError:\n{error}".strip()
        return output
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python bash.py '<command>'")
    else:
        cmd = " ".join(sys.argv[1:])
        print(tool_function(cmd))

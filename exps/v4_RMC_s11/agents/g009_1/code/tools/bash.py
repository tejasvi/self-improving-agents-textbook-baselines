import asyncio
import os
import signal

MAX_OUTPUT_CHARS = 16000  # truncate very long stdout/stderr
COMMAND_TIMEOUT = 120.0  # seconds per command


def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* Each command runs non-interactively with standard input closed, so commands that read from stdin will get EOF.\n
* Each command is limited to %d seconds; longer commands are killed.\n
* Very long output is truncated.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.""" % int(COMMAND_TIMEOUT),
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


def truncate_output(text, limit=MAX_OUTPUT_CHARS):
    """Keep the head and tail of very long output, dropping the middle."""
    if len(text) <= limit:
        return text
    half = limit // 2
    omitted = len(text) - 2 * half
    return (
        text[:half]
        + f"\n... [output truncated: {omitted} characters omitted] ...\n"
        + text[-half:]
    )


class BashSession:
    """Runs bash commands non-interactively, one subprocess per command."""

    def __init__(self, timeout=COMMAND_TIMEOUT):
        self._timeout = timeout
        self._started = False

    async def start(self):
        self._started = True

    def stop(self):
        self._started = False

    async def run(self, command):
        if not self._started:
            raise ValueError("Session has not started.")

        process = await asyncio.create_subprocess_exec(
            "/bin/bash", "-c", command,
            stdin=asyncio.subprocess.DEVNULL,  # standard input is closed
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=os.environ.copy(),
            start_new_session=True,  # own process group so we can kill children
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=self._timeout
            )
        except asyncio.TimeoutError:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
            await process.wait()
            raise ValueError(
                f"Timed out: command did not finish within {self._timeout} seconds and was killed."
            )

        output = stdout.decode(errors='ignore').strip()
        error = stderr.decode(errors='ignore').strip()
        return truncate_output(output), truncate_output(error)


def filter_error(error):
    # Kept for compatibility; filters out terminal ioctl noise if present.
    return '\n'.join(
        line for line in error.splitlines()
        if "Inappropriate ioctl for device" not in line
    ).strip()


async def tool_function_call(command):
    """Execute a command in a non-interactive bash shell."""
    try:
        bash_session = BashSession()
        await bash_session.start()
        try:
            output, error = await bash_session.run(command)
        finally:
            bash_session.stop()
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

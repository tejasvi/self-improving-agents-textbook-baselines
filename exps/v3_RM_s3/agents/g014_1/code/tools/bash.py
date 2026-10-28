import asyncio
import os
import signal
import subprocess

MAX_OUTPUT_CHARS = 16000  # total characters returned per stream before truncation
DEFAULT_TIMEOUT = 120.0  # seconds allowed per command


def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* Each command runs non-interactively with standard input closed, so commands that wait for user input will fail instead of hanging.\n
* Each command is limited to 120 seconds; longer commands are killed.\n
* Very long outputs are truncated (the beginning and end are kept).\n
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


def truncate_output(text, max_chars=MAX_OUTPUT_CHARS):
    """Keep the head and tail of very long output, marking the omitted middle."""
    if len(text) <= max_chars:
        return text
    half = max_chars // 2
    omitted = len(text) - 2 * half
    return (
        text[:half]
        + f"\n... [{omitted} characters truncated] ...\n"
        + text[-half:]
    )


class BashSession:
    """Runs bash commands non-interactively, one subprocess per command."""

    def __init__(self):
        self._started = False
        self._timeout = DEFAULT_TIMEOUT  # seconds
        self._max_output_chars = MAX_OUTPUT_CHARS

    async def start(self):
        self._started = True

    def stop(self):
        self._started = False

    async def run(self, command):
        """Run a command. Returns (stdout, stderr) as strings.

        Raises ValueError if the command exceeds the timeout.
        """
        if not self._started:
            raise ValueError("Session has not started.")

        process = await asyncio.create_subprocess_exec(
            "/bin/bash", "-c", command,
            stdin=subprocess.DEVNULL,  # standard input is closed for the command
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=os.environ.copy(),
            start_new_session=True,  # own process group, so the whole tree can be killed
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

        output = truncate_output(stdout.decode(errors='ignore').strip(), self._max_output_chars)
        error = truncate_output(stderr.decode(errors='ignore').strip(), self._max_output_chars)
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
    """Execute a command in a non-interactive bash shell."""
    try:
        bash_session = BashSession()
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

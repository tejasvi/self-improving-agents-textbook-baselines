import asyncio
import os
import signal
import subprocess
import tempfile

MAX_OUTPUT_CHARS = 16000  # truncate longer outputs (keep head and tail)
COMMAND_TIMEOUT = 120.0  # seconds per command


def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* Each command runs in a fresh non-interactive shell: standard input is closed, so commands that wait for user input will fail. Pass input via pipes, heredocs or arguments instead.\n
* Shell state (variables, working directory) is NOT preserved between calls; use absolute paths or chain commands with && in a single call.\n
* Each command is killed if it runs longer than %d seconds.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output; output longer than %d characters is truncated.\n
* Please run long lived commands in the background, e.g. 'nohup cmd > log 2>&1 &', and check the log later.""" % (int(COMMAND_TIMEOUT), MAX_OUTPUT_CHARS),
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
    """Keep the head and tail of very long output, marking the omitted middle."""
    if len(text) <= limit:
        return text
    half = limit // 2
    omitted = len(text) - 2 * half
    return f"{text[:half]}\n... [{omitted} characters truncated] ...\n{text[-half:]}"


class BashSession:
    """Runs bash commands non-interactively, one fresh shell per command."""

    def __init__(self, timeout=None):
        self._timeout = COMMAND_TIMEOUT if timeout is None else timeout

    async def run(self, command):
        """Run `command` and return (stdout, stderr, returncode).

        Output goes to temporary files rather than pipes, so a background job that
        inherits the descriptors cannot keep this call blocked after bash has exited.
        Raises ValueError if the command exceeds the timeout (the process group is killed).
        """
        with tempfile.TemporaryFile() as out_f, tempfile.TemporaryFile() as err_f:
            process = await asyncio.create_subprocess_exec(
                "/bin/bash", "-c", command,
                stdin=subprocess.DEVNULL,  # close stdin: nothing can block on input
                stdout=out_f,
                stderr=err_f,
                env=os.environ.copy(),
                start_new_session=True,  # own process group so we can kill children too
            )
            try:
                await asyncio.wait_for(process.wait(), timeout=self._timeout)
            except asyncio.TimeoutError:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
                await process.wait()
                raise ValueError(
                    f"Timed out: command did not finish within {self._timeout} seconds and was killed."
                )
            out_f.seek(0)
            err_f.seek(0)
            return (
                out_f.read().decode(errors="replace"),
                err_f.read().decode(errors="replace"),
                process.returncode,
            )


async def tool_function_call(command):
    """Execute a command in a non-interactive bash shell."""
    try:
        session = BashSession()
        output, error, _ = await session.run(command)
        output = truncate_output(output.strip())
        error = truncate_output(error.strip())
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
        result = tool_function(input_command)
        print(result)

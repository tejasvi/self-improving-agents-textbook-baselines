import subprocess
import sys
import time
import os

def tool_info():
    return {
        "name": "benchmark",
        "description": """Run a command on an input file with a timeout and report wall-clock time.
Executes a command (Python script, compiled binary, etc.) with the given input and measures execution time.
Returns the wall-clock time, stdout, stderr, and return code.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Command to execute (e.g., 'python solution.py' or './solution')"
                },
                "input_file": {
                    "type": "string",
                    "description": "Path to input file to pass to command via stdin"
                },
                "timeout_seconds": {
                    "type": "number",
                    "description": "Timeout in seconds (e.g., 5.0)"
                }
            },
            "required": ["command", "input_file", "timeout_seconds"]
        }
    }

def tool_function(command, input_file, timeout_seconds):
    """
    Run a command on an input file and report wall-clock time.
    
    Args:
        command: Command string to execute
        input_file: Path to input file
        timeout_seconds: Timeout in seconds
    
    Returns:
        String containing timing and execution results
    """
    try:
        # Read input file
        if not os.path.exists(input_file):
            return f"Error: Input file not found: {input_file}"
        
        with open(input_file, 'r') as f:
            input_data = f.read()
        
        # Run command with timing
        start_time = time.time()
        try:
            result = subprocess.run(
                command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                shell=True
            )
            elapsed_time = time.time() - start_time
            
            output = f"Wall-clock time: {elapsed_time:.3f}s (timeout: {timeout_seconds}s)\n"
            output += f"Return code: {result.returncode}\n\n"
            
            if result.stdout:
                output += f"=== STDOUT ===\n{result.stdout}\n"
            
            if result.stderr:
                output += f"=== STDERR ===\n{result.stderr}\n"
            
            if result.returncode != 0 and not result.stderr:
                output += f"Command exited with non-zero code: {result.returncode}\n"
            
            return output
            
        except subprocess.TimeoutExpired:
            elapsed_time = time.time() - start_time
            return f"TIMEOUT: Command exceeded {timeout_seconds}s (ran for ~{elapsed_time:.1f}s)"
        
    except Exception as e:
        return f"Error running benchmark: {str(e)}"

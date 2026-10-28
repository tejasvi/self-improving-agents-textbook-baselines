import subprocess
import time
import tempfile
from pathlib import Path


def tool_info():
    return {
        "name": "run_benchmark",
        "description": """Run a solution on a max-size input to measure performance under worst-case constraints.
Executes the solution in a subprocess with either a max-size input file or output from a generator script.
Returns 'OK in X.XXXs' on success, or 'TIMEOUT after Ns' / stderr on runtime error.
The timeout prevents TLE solutions from blocking the agent.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the solution.py file to benchmark"
                },
                "input_path": {
                    "type": "string",
                    "description": "Optional: path to a file containing the max-size input"
                },
                "generator_path": {
                    "type": "string",
                    "description": "Optional: path to a script that generates a max-size input when run"
                },
                "generator_args": {
                    "type": "string",
                    "description": "Optional: arguments to pass to the generator script (e.g., 'worst_case' or 'max_n')"
                },
                "timeout_sec": {
                    "type": "number",
                    "description": "Timeout in seconds (default: 10.0)"
                }
            },
            "required": ["solution_path"]
        }
    }


def tool_function(
    solution_path,
    input_path=None,
    generator_path=None,
    generator_args=None,
    timeout_sec=10.0
):
    """
    Run a solution on a max-size input and measure performance.
    
    Args:
        solution_path: Path to the solution.py file to benchmark
        input_path: Optional path to a file with the max-size input
        generator_path: Optional path to a script that generates max-size input
        generator_args: Optional arguments to pass to the generator
        timeout_sec: Timeout in seconds (default: 10.0)
    
    Returns:
        'OK in X.XXXs' on success (first 200 chars of output),
        'TIMEOUT after Ns' on timeout,
        or error details on runtime error
    """
    try:
        solution_path = Path(solution_path)
        
        # Validate solution path exists
        if not solution_path.exists():
            return f"Error: solution_path {solution_path} does not exist"
        
        # Get input data
        test_input = None
        
        if input_path:
            input_path = Path(input_path)
            if not input_path.exists():
                return f"Error: input_path {input_path} does not exist"
            with open(input_path, 'r') as f:
                test_input = f.read()
        
        elif generator_path:
            generator_path = Path(generator_path)
            if not generator_path.exists():
                return f"Error: generator_path {generator_path} does not exist"
            
            # Run generator to produce input
            try:
                cmd = ["python3", str(generator_path)]
                if generator_args:
                    cmd.append(generator_args)
                
                gen_result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout_sec
                )
                
                if gen_result.returncode != 0:
                    return f"Error: generator failed with: {gen_result.stderr}"
                
                test_input = gen_result.stdout
            except subprocess.TimeoutExpired:
                return f"Error: generator timed out after {timeout_sec}s"
        
        else:
            return "Error: must provide either input_path or generator_path"
        
        if not test_input:
            return "Error: no input data generated"
        
        # Run the solution with the input
        try:
            start_time = time.time()
            result = subprocess.run(
                ["python3", str(solution_path)],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            elapsed = time.time() - start_time
            
            if result.returncode != 0:
                # Runtime error
                error_output = result.stderr[:500]
                return f"RUNTIME ERROR: {error_output}"
            
            # Success - return timing and first 200 chars of output
            output_preview = result.stdout[:200]
            if len(result.stdout) > 200:
                output_preview += "..."
            
            return f"OK in {elapsed:.3f}s\nOutput (first 200 chars): {output_preview}"
        
        except subprocess.TimeoutExpired:
            return f"TIMEOUT after {timeout_sec}s (algorithm too slow for max constraints)"
        
    except Exception as e:
        return f"Fatal error in run_benchmark: {str(e)}"


if __name__ == "__main__":
    # Example usage
    print(tool_info())

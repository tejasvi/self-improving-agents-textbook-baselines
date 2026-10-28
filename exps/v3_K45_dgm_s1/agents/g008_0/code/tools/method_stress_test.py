import subprocess
import os
import sys
import tempfile
import json
import traceback

def tool_info():
    return {
        "name": "method_stress_test",
        "description": """Run a stress test comparing a Solution class method against a brute-force reference.
Runs a random input generator multiple times, executes both the solution and brute-force reference
with a timeout, and reports the first mismatch or 'all passed'. Returns timing information for each test.
This tool is designed for class-based tasks where the solution implements a method of a Solution class.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python file containing the Solution class"
                },
                "method_name": {
                    "type": "string",
                    "description": "Name of the method to test (e.g., 'timeRequiredToBuy')"
                },
                "brute_path": {
                    "type": "string",
                    "description": "Path to the Python file defining either a brute(*args) function or a Solution class with the same method name"
                },
                "generator_path": {
                    "type": "string",
                    "description": "Path to the Python script that takes a seed argument and prints a JSON list of positional arguments for the method"
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of random test cases to run (e.g., 200)"
                },
                "timeout_per_test": {
                    "type": "number",
                    "description": "Timeout per test in seconds (e.g., 2.0)"
                }
            },
            "required": ["solution_path", "method_name", "brute_path", "generator_path", "num_tests", "timeout_per_test"]
        }
    }

def _create_runner_script(module_path, class_name, method_name, args_json):
    """
    Create a temporary runner script that imports the module, instantiates the class,
    calls the method with the given args, and returns the result as JSON.
    
    Args:
        module_path: Path to the Python file
        class_name: Name of the class (e.g., 'Solution')
        method_name: Name of the method to call
        args_json: JSON string representing the list of arguments
    
    Returns:
        The code to execute as a string
    """
    code = f"""
import sys
import json
import importlib.util

# Import the module
spec = importlib.util.spec_from_file_location("module", {repr(module_path)})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Get the class and create an instance
cls = getattr(module, {repr(class_name)})
instance = cls()

# Get the method
method = getattr(instance, {repr(method_name)})

# Parse the arguments
args = json.loads({repr(args_json)})

# Call the method
result = method(*args)

# Print the result as JSON
print(json.dumps(result))
"""
    return code

def tool_function(solution_path, method_name, brute_path, generator_path, num_tests, timeout_per_test):
    """
    Run stress tests comparing solution method against brute-force reference.
    
    Args:
        solution_path: Path to solution file containing Solution class
        method_name: Name of method to test
        brute_path: Path to brute-force reference file
        generator_path: Path to test case generator
        num_tests: Number of test cases to run
        timeout_per_test: Timeout per test in seconds
    
    Returns:
        String containing test results or error messages
    """
    try:
        results = []
        first_mismatch = None
        passed_count = 0
        total_solution_time = 0
        total_brute_time = 0
        
        # Get absolute paths
        solution_path = os.path.abspath(solution_path)
        brute_path = os.path.abspath(brute_path)
        generator_path = os.path.abspath(generator_path)
        
        for seed in range(num_tests):
            # Generate test case
            try:
                gen_result = subprocess.run(
                    [sys.executable, generator_path, str(seed)],
                    capture_output=True,
                    text=True,
                    timeout=timeout_per_test
                )
                args_json = gen_result.stdout.strip()
                if gen_result.returncode != 0:
                    results.append(f"Test {seed}: Generator failed: {gen_result.stderr}")
                    continue
            except subprocess.TimeoutExpired:
                results.append(f"Test {seed}: Generator timeout")
                continue
            except Exception as e:
                results.append(f"Test {seed}: Generator error: {str(e)}")
                continue
            
            # Run solution method
            solution_output = None
            solution_time = None
            solution_error = None
            try:
                runner_code = _create_runner_script(solution_path, "Solution", method_name, args_json)
                import time
                start = time.time()
                sol_result = subprocess.run(
                    [sys.executable, "-c", runner_code],
                    capture_output=True,
                    text=True,
                    timeout=timeout_per_test
                )
                solution_time = time.time() - start
                solution_output = sol_result.stdout.strip()
                if sol_result.returncode != 0:
                    solution_error = sol_result.stderr
            except subprocess.TimeoutExpired:
                solution_error = f"TIMEOUT ({timeout_per_test}s)"
            except Exception as e:
                solution_error = str(e)
            
            # Run brute-force (try both function and method approaches)
            brute_output = None
            brute_time = None
            brute_error = None
            try:
                # First try: assume brute_path has a brute(*args) function
                runner_code = f"""
import sys
import json
import importlib.util

# Import the brute module
spec = importlib.util.spec_from_file_location("brute_module", {repr(brute_path)})
brute_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(brute_module)

# Try to call brute function
args = json.loads({repr(args_json)})
try:
    result = brute_module.brute(*args)
except AttributeError:
    # If brute function doesn't exist, try calling the method on Solution class
    cls = getattr(brute_module, 'Solution')
    instance = cls()
    method = getattr(instance, {repr(method_name)})
    result = method(*args)

print(json.dumps(result))
"""
                import time
                start = time.time()
                brute_result = subprocess.run(
                    [sys.executable, "-c", runner_code],
                    capture_output=True,
                    text=True,
                    timeout=timeout_per_test
                )
                brute_time = time.time() - start
                brute_output = brute_result.stdout.strip()
                if brute_result.returncode != 0:
                    brute_error = brute_result.stderr
            except subprocess.TimeoutExpired:
                brute_error = f"TIMEOUT ({timeout_per_test}s)"
            except Exception as e:
                brute_error = str(e)
            
            # Compare results
            if solution_error or brute_error:
                if not first_mismatch:
                    first_mismatch = {
                        "test": seed,
                        "args": args_json[:500] if len(args_json) > 500 else args_json,
                        "solution_error": solution_error,
                        "brute_error": brute_error,
                        "solution_output": solution_output[:100] if solution_output else None,
                        "brute_output": brute_output[:100] if brute_output else None
                    }
                results.append(f"Test {seed}: FAIL (solution_error={solution_error}, brute_error={brute_error})")
            elif solution_output != brute_output:
                if not first_mismatch:
                    first_mismatch = {
                        "test": seed,
                        "args": args_json[:500] if len(args_json) > 500 else args_json,
                        "solution_output": solution_output[:200] if solution_output else None,
                        "brute_output": brute_output[:200] if brute_output else None
                    }
                results.append(f"Test {seed}: MISMATCH")
            else:
                passed_count += 1
                if solution_time:
                    total_solution_time += solution_time
                if brute_time:
                    total_brute_time += brute_time
                results.append(f"Test {seed}: PASS (sol={solution_time:.3f}s, brute={brute_time:.3f}s)")
        
        # Format output
        output = f"Method Stress Test Results ({passed_count}/{num_tests} passed)\n"
        if passed_count > 0:
            output += f"Average solution time: {total_solution_time/passed_count:.3f}s\n"
            output += f"Average brute-force time: {total_brute_time/passed_count:.3f}s\n"
        
        if first_mismatch:
            output += f"\nFirst Mismatch at Test {first_mismatch['test']}:\n"
            output += f"Arguments (first 500 chars):\n{first_mismatch['args']}\n"
            if first_mismatch.get('solution_error'):
                output += f"Solution error: {first_mismatch['solution_error']}\n"
            elif first_mismatch.get('solution_output'):
                output += f"Solution output (first 200 chars): {first_mismatch['solution_output']}\n"
            if first_mismatch.get('brute_error'):
                output += f"Brute-force error: {first_mismatch['brute_error']}\n"
            elif first_mismatch.get('brute_output'):
                output += f"Brute-force output (first 200 chars): {first_mismatch['brute_output']}\n"
        else:
            output += "\nAll tests passed!"
        
        output += "\n\nTest Details (last 20):\n"
        output += "\n".join(results[-20:])
        
        return output
        
    except Exception as e:
        return f"Error running method stress test: {str(e)}\n{traceback.format_exc()}"

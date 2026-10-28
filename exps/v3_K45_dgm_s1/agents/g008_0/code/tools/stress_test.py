import subprocess
import os
import sys
import tempfile

def tool_info():
    return {
        "name": "stress_test",
        "description": """Run a stress test comparing a solution against a brute-force reference.
Runs a random input generator multiple times, executes both the solution and brute-force reference
with a timeout, and reports the first mismatch or 'all passed'. Returns timing information for each test.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Absolute path to the solution file (Python script or compiled binary)"
                },
                "brute_path": {
                    "type": "string",
                    "description": "Absolute path to the brute-force reference file (Python script or compiled binary)"
                },
                "generator_path": {
                    "type": "string",
                    "description": "Absolute path to the random input generator script (generates test cases on stdout)"
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of random test cases to run (e.g., 100)"
                },
                "timeout_per_test": {
                    "type": "number",
                    "description": "Timeout per test in seconds (e.g., 2.0)"
                }
            },
            "required": ["solution_path", "brute_path", "generator_path", "num_tests", "timeout_per_test"]
        }
    }

def tool_function(solution_path, brute_path, generator_path, num_tests, timeout_per_test):
    """
    Run stress tests comparing solution against brute-force reference.
    
    Args:
        solution_path: Path to solution file
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
        
        for seed in range(num_tests):
            # Generate test case
            try:
                gen_result = subprocess.run(
                    [sys.executable, generator_path, str(seed)],
                    capture_output=True,
                    text=True,
                    timeout=timeout_per_test
                )
                test_input = gen_result.stdout
                if gen_result.returncode != 0:
                    results.append(f"Test {seed}: Generator failed: {gen_result.stderr}")
                    continue
            except subprocess.TimeoutExpired:
                results.append(f"Test {seed}: Generator timeout")
                continue
            except Exception as e:
                results.append(f"Test {seed}: Generator error: {str(e)}")
                continue
            
            # Run solution
            solution_output = None
            solution_time = None
            solution_error = None
            try:
                import time
                start = time.time()
                sol_result = subprocess.run(
                    [sys.executable, solution_path],
                    input=test_input,
                    capture_output=True,
                    text=True,
                    timeout=timeout_per_test
                )
                solution_time = time.time() - start
                solution_output = sol_result.stdout
                if sol_result.returncode != 0:
                    solution_error = sol_result.stderr
            except subprocess.TimeoutExpired:
                solution_error = f"TIMEOUT ({timeout_per_test}s)"
            except Exception as e:
                solution_error = str(e)
            
            # Run brute-force
            brute_output = None
            brute_time = None
            brute_error = None
            try:
                import time
                start = time.time()
                brute_result = subprocess.run(
                    [sys.executable, brute_path],
                    input=test_input,
                    capture_output=True,
                    text=True,
                    timeout=timeout_per_test
                )
                brute_time = time.time() - start
                brute_output = brute_result.stdout
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
                        "input": test_input[:200] if len(test_input) > 200 else test_input,
                        "solution_error": solution_error,
                        "brute_error": brute_error,
                        "solution_output": solution_output[:100] if solution_output else None,
                        "brute_output": brute_output[:100] if brute_output else None
                    }
                results.append(f"Test {seed}: FAIL (solution_error={solution_error}, brute_error={brute_error})")
            elif solution_output.strip() != brute_output.strip():
                if not first_mismatch:
                    first_mismatch = {
                        "test": seed,
                        "input": test_input[:200] if len(test_input) > 200 else test_input,
                        "solution_output": solution_output[:100] if solution_output else None,
                        "brute_output": brute_output[:100] if brute_output else None
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
        output = f"Stress Test Results ({passed_count}/{num_tests} passed)\n"
        output += f"Average solution time: {total_solution_time/max(passed_count, 1):.3f}s\n"
        output += f"Average brute-force time: {total_brute_time/max(passed_count, 1):.3f}s\n"
        
        if first_mismatch:
            output += f"\nFirst Mismatch at Test {first_mismatch['test']}:\n"
            output += f"Input (first 200 chars):\n{first_mismatch['input']}\n"
            if first_mismatch.get('solution_error'):
                output += f"Solution error: {first_mismatch['solution_error']}\n"
            elif first_mismatch.get('solution_output'):
                output += f"Solution output (first 100 chars): {first_mismatch['solution_output']}\n"
            if first_mismatch.get('brute_error'):
                output += f"Brute-force error: {first_mismatch['brute_error']}\n"
            elif first_mismatch.get('brute_output'):
                output += f"Brute-force output (first 100 chars): {first_mismatch['brute_output']}\n"
        else:
            output += "\nAll tests passed!"
        
        output += "\n\nTest Details:\n"
        output += "\n".join(results[-20:])  # Show last 20 test results
        
        return output
        
    except Exception as e:
        return f"Error running stress test: {str(e)}"

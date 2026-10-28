import subprocess
import sys
import json
import importlib.util
import tempfile
import traceback

def tool_info():
    return {
        "name": "run_examples",
        "description": """Run examples against a Solution class method.
Loads a Solution class from a Python file, calls a specified method on each example with a per-example timeout,
and returns a plain-text report containing pass/fail status, actual vs expected output, and any tracebacks.
The examples parameter is a JSON string of a list of objects with 'args' (list) and 'expected' (the expected return value).""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python file containing the Solution class"
                },
                "method_name": {
                    "type": "string",
                    "description": "Name of the method to call on the Solution instance"
                },
                "examples": {
                    "type": "string",
                    "description": "JSON string of a list of examples, where each example is {\"args\": [...], \"expected\": ...}"
                }
            },
            "required": ["solution_path", "method_name", "examples"]
        }
    }

def tool_function(solution_path, method_name, examples):
    """
    Run examples against a Solution class method.
    
    Args:
        solution_path: Path to the Python file containing the Solution class
        method_name: Name of the method to call
        examples: JSON string of examples list
    
    Returns:
        Plain-text report of results
    """
    try:
        # Parse examples
        try:
            examples_list = json.loads(examples)
        except json.JSONDecodeError as e:
            return f"Error parsing examples JSON: {str(e)}"
        
        # Load the Solution class
        try:
            spec = importlib.util.spec_from_file_location("solution_module", solution_path)
            if spec is None or spec.loader is None:
                return f"Error: Could not load module from {solution_path}"
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            return f"Error loading solution module: {str(e)}\n{traceback.format_exc()}"
        
        # Get the Solution class
        try:
            Solution = getattr(module, 'Solution')
        except AttributeError:
            return f"Error: Solution class not found in {solution_path}"
        
        # Run each example
        results = []
        passed_count = 0
        failed_count = 0
        
        for i, example in enumerate(examples_list):
            try:
                # Extract args and expected
                if isinstance(example, dict):
                    args = example.get('args', [])
                    expected = example.get('expected')
                else:
                    results.append(f"Example {i}: INVALID (not a dict)")
                    failed_count += 1
                    continue
                
                # Validate args is a list
                if not isinstance(args, list):
                    results.append(f"Example {i}: INVALID (args is not a list)")
                    failed_count += 1
                    continue
                
                # Create instance and call method
                try:
                    instance = Solution()
                    method = getattr(instance, method_name, None)
                    if method is None:
                        results.append(f"Example {i}: INVALID (method {method_name} not found)")
                        failed_count += 1
                        continue
                    
                    # Call with timeout using subprocess
                    actual = _call_with_timeout(solution_path, method_name, args, timeout=5.0)
                    
                    # Compare
                    if actual == expected:
                        results.append(f"Example {i}: PASS")
                        passed_count += 1
                    else:
                        results.append(
                            f"Example {i}: FAIL\n"
                            f"  Args: {json.dumps(args)}\n"
                            f"  Expected: {json.dumps(expected)}\n"
                            f"  Actual: {json.dumps(actual)}"
                        )
                        failed_count += 1
                
                except subprocess.TimeoutExpired:
                    results.append(
                        f"Example {i}: TIMEOUT\n"
                        f"  Args: {json.dumps(args)}"
                    )
                    failed_count += 1
                except Exception as e:
                    results.append(
                        f"Example {i}: ERROR\n"
                        f"  Args: {json.dumps(args)}\n"
                        f"  Error: {str(e)}\n"
                        f"  Traceback:\n{traceback.format_exc()}"
                    )
                    failed_count += 1
            
            except Exception as e:
                results.append(f"Example {i}: EXCEPTION - {str(e)}")
                failed_count += 1
        
        # Format output
        output = f"Examples Test Results ({passed_count}/{len(examples_list)} passed)\n"
        output += "=" * 60 + "\n"
        output += "\n".join(results)
        
        return output
    
    except Exception as e:
        return f"Error running examples: {str(e)}\n{traceback.format_exc()}"


def _call_with_timeout(solution_path, method_name, args, timeout=5.0):
    """
    Call a Solution method with a timeout using subprocess.
    """
    runner_code = f"""
import sys
import json
import importlib.util

# Import the module
spec = importlib.util.spec_from_file_location("solution_module", {repr(solution_path)})
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Get the Solution class
Solution = getattr(module, 'Solution')
instance = Solution()
method = getattr(instance, {repr(method_name)})

# Parse args
args = json.loads({repr(json.dumps(args))})

# Call the method
result = method(*args)

# Print result as JSON
print(json.dumps(result))
"""
    
    result = subprocess.run(
        [sys.executable, "-c", runner_code],
        capture_output=True,
        text=True,
        timeout=timeout
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Method call failed: {result.stderr}")
    
    try:
        return json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        # If output is not JSON, treat as string
        return result.stdout.strip()

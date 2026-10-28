import subprocess
import json
import difflib
from pathlib import Path


def tool_info():
    return {
        "name": "run_samples",
        "description": """Run a solution against sample test cases extracted from the problem statement.
For each sample, the tool runs `python3 solution_path` with the sample input and compares the actual output against the expected output.
Returns PASS/FAIL per sample, showing the actual output, expected output, and a unified diff.
Also notes whether any differences are whitespace-only. Use this to detect mismatches early.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the solution.py file to test"
                },
                "samples": {
                    "type": "array",
                    "description": "List of sample test cases, each with 'input' and 'expected_output' strings"
                }
            },
            "required": ["solution_path", "samples"]
        }
    }


def tool_function(solution_path, samples, timeout_sec=5.0):
    """
    Run a solution against sample test cases.
    
    Args:
        solution_path: Path to the solution.py file
        samples: List of dicts with 'input' and 'expected_output' keys
        timeout_sec: Timeout per test in seconds
    
    Returns:
        String with test results for each sample, including PASS/FAIL, outputs, and diffs
    """
    try:
        solution_path = Path(solution_path)
        
        # Validate path exists
        if not solution_path.exists():
            return f"Error: solution_path {solution_path} does not exist"
        
        # Validate samples format
        if not isinstance(samples, list):
            return f"Error: samples must be a list of dicts with 'input' and 'expected_output' keys"
        
        results = []
        all_passed = True
        
        for idx, sample in enumerate(samples):
            if not isinstance(sample, dict) or 'input' not in sample or 'expected_output' not in sample:
                return f"Error: sample {idx} must be a dict with 'input' and 'expected_output' keys"
            
            sample_input = sample['input']
            expected_output = sample['expected_output'].strip()
            
            try:
                # Run solution with timeout
                sol_result = subprocess.run(
                    ["python3", str(solution_path)],
                    input=sample_input,
                    capture_output=True,
                    text=True,
                    timeout=timeout_sec
                )
                
                if sol_result.returncode != 0:
                    results.append(
                        f"Sample {idx}: FAIL\n"
                        f"  Error: Solution exited with code {sol_result.returncode}\n"
                        f"  Stderr: {sol_result.stderr}"
                    )
                    all_passed = False
                else:
                    actual_output = sol_result.stdout.strip()
                    
                    if actual_output == expected_output:
                        results.append(f"Sample {idx}: PASS")
                    else:
                        all_passed = False
                        # Check if it's whitespace-only difference
                        is_whitespace_only = (
                            actual_output.replace(' ', '').replace('\n', '').replace('\t', '')
                            == expected_output.replace(' ', '').replace('\n', '').replace('\t', '')
                        )
                        
                        # Generate unified diff
                        diff_lines = list(difflib.unified_diff(
                            expected_output.splitlines(keepends=True),
                            actual_output.splitlines(keepends=True),
                            fromfile=f'expected',
                            tofile=f'actual',
                            lineterm=''
                        ))
                        diff_str = ''.join(diff_lines).strip()
                        
                        whitespace_note = " (whitespace-only difference)" if is_whitespace_only else ""
                        results.append(
                            f"Sample {idx}: FAIL{whitespace_note}\n"
                            f"  Expected output:\n{expected_output}\n"
                            f"  Actual output:\n{actual_output}\n"
                            f"  Diff:\n{diff_str if diff_str else '(no diff)'}"
                        )
            
            except subprocess.TimeoutExpired:
                all_passed = False
                results.append(
                    f"Sample {idx}: FAIL\n"
                    f"  Error: Solution timed out (exceeded {timeout_sec}s)"
                )
            except Exception as e:
                all_passed = False
                results.append(
                    f"Sample {idx}: FAIL\n"
                    f"  Error: {str(e)}"
                )
        
        # Summarize results
        summary = "ALL PASSED" if all_passed else f"SOME FAILED ({len([r for r in results if 'FAIL' in r])} failures)"
        result_str = f"Sample Test Results: {summary}\n" + '\n'.join(results)
        
        return result_str
        
    except Exception as e:
        return f"Fatal error in run_samples: {str(e)}"


if __name__ == "__main__":
    # Example usage
    print(tool_info())

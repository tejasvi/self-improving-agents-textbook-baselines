from tools import stress_test


def tool_info():
    return {
        "name": "diff_test",
        "description": """Differential test: compare a solution against a brute-force reference on generated random inputs, using exact output equality (whitespace-normalized).
* `generator_path` is a Python script that takes one integer argument (the seed) and prints one input to stdout. It is run for seeds 0..num_tests-1.
* `solution_path` and `brute_path` are Python programs that read stdin and write stdout.
* Reports the first mismatch (INPUT, EXPECTED from brute, ACTUAL from solution) or an all-pass count. Output is kept compact by `max_output_lines`.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the solution Python file under test."
                },
                "brute_path": {
                    "type": "string",
                    "description": "Path to the brute-force reference Python file."
                },
                "generator_path": {
                    "type": "string",
                    "description": "Path to a generator script taking a seed integer and printing one input."
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of seeds to test (seeds 0..num_tests-1). Default 200."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Per-run time limit in seconds. Default 10."
                },
                "max_output_lines": {
                    "type": "integer",
                    "description": "Maximum number of lines shown per printed block in a failure report. Default 40."
                }
            },
            "required": ["solution_path", "brute_path", "generator_path"]
        }
    }


def tool_function(solution_path, brute_path, generator_path, num_tests=200, timeout=10, max_output_lines=40):
    return stress_test.tool_function(
        solution_path, brute_path, generator_path,
        num_tests=num_tests, timeout=timeout, max_output_lines=max_output_lines)

import os
import subprocess
import tempfile


def tool_info():
    return {
        'name': 'stress_test',
        'description': (
            'Randomized comparison of a solution against a brute-force reference. For seed = 1..iterations, '
            'runs generator_path with the seed as its argument (it prints one test input to stdout), then runs '
            'the solution and the brute force on that input with python3. Outputs are compared after whitespace '
            'normalization, or, if checker_path is given, the checker is run as `checker input_file output_file '
            'brute_output_file` (it must exit 0 if the solution output is valid) and the brute output is only used '
            'as a reference. Returns the first failing seed with the input and both outputs, or "ALL OK". '
            'Pass absolute paths. Use generators that produce both Yes and No style cases for decision problems.'
        ),
        'input_schema': {
            'type': 'object',
            'properties': {
                'solution_path': {
                    'type': 'string',
                    'description': 'Absolute path to the solution Python file (reads stdin, writes stdout).',
                },
                'brute_path': {
                    'type': 'string',
                    'description': 'Absolute path to the brute-force reference Python file (reads stdin, writes stdout).',
                },
                'generator_path': {
                    'type': 'string',
                    'description': 'Absolute path to a Python generator. It is called as `python3 generator.py SEED` and prints one test input to stdout.',
                },
                'iterations': {
                    'type': 'integer',
                    'description': 'Number of seeds to test (seeds 1..iterations). Defaults to 200.',
                },
                'timeout': {
                    'type': 'number',
                    'description': 'Timeout in seconds for each program run. Defaults to 5.',
                },
                'checker_path': {
                    'type': 'string',
                    'description': 'Optional absolute path to a checker/validator. Called as `python3 checker.py INPUT_FILE OUTPUT_FILE BRUTE_OUTPUT_FILE`; exit code 0 means the solution output is valid.',
                },
            },
            'required': ['solution_path', 'brute_path', 'generator_path'],
        },
    }


def _run(args, input_text, timeout):
    """Run a command; returns (ok, stdout, detail)."""
    try:
        proc = subprocess.run(args, input=input_text, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, '', f'timeout after {timeout}s'
    if proc.returncode != 0:
        return False, proc.stdout, f'exit code {proc.returncode}: {proc.stderr.strip()[-800:]}'
    return True, proc.stdout, ''


def _norm(text):
    return text.split()


def tool_function(solution_path, brute_path, generator_path, iterations=200, timeout=5, checker_path=None):
    python = 'python3'
    try:
        iterations = int(iterations) if iterations is not None else 200
    except (TypeError, ValueError):
        iterations = 200
    try:
        timeout = float(timeout) if timeout is not None else 5.0
    except (TypeError, ValueError):
        timeout = 5.0
    for label, path in (('solution_path', solution_path), ('brute_path', brute_path),
                        ('generator_path', generator_path)):
        if not path or not os.path.isabs(path) or not os.path.isfile(path):
            return f'ERROR: {label} must be an existing absolute file path (got {path!r}).'
    if checker_path and (not os.path.isabs(checker_path) or not os.path.isfile(checker_path)):
        return f'ERROR: checker_path must be an existing absolute file path (got {checker_path!r}).'

    with tempfile.TemporaryDirectory() as tmpdir:
        for seed in range(1, iterations + 1):
            ok, test_input, detail = _run([python, generator_path, str(seed)], '', timeout)
            if not ok:
                return f'GENERATOR FAILED at seed {seed}: {detail}'
            test_input = test_input if test_input.endswith('\n') else test_input + '\n'

            ok, brute_out, detail = _run([python, brute_path], test_input, timeout)
            if not ok:
                return f'BRUTE FAILED at seed {seed}\ninput:\n{test_input}\nbrute: {detail}'

            ok, sol_out, detail = _run([python, solution_path], test_input, timeout)
            if not ok:
                return (f'SOLUTION FAILED at seed {seed}: {detail}\n'
                        f'input:\n{test_input}\nbrute output:\n{brute_out.strip()}')

            if checker_path:
                in_file = os.path.join(tmpdir, 'in.txt')
                out_file = os.path.join(tmpdir, 'out.txt')
                brute_file = os.path.join(tmpdir, 'brute.txt')
                with open(in_file, 'w') as f:
                    f.write(test_input)
                with open(out_file, 'w') as f:
                    f.write(sol_out)
                with open(brute_file, 'w') as f:
                    f.write(brute_out)
                ok, check_out, detail = _run([python, checker_path, in_file, out_file, brute_file], '', timeout)
                if not ok:
                    return (f'CHECKER REJECTED at seed {seed}: {detail} {check_out.strip()}\n'
                            f'input:\n{test_input}\nsolution output:\n{sol_out.strip()}\n'
                            f'brute output:\n{brute_out.strip()}')
            elif _norm(sol_out) != _norm(brute_out):
                return (f'MISMATCH at seed {seed}\ninput:\n{test_input}\n'
                        f'solution output:\n{sol_out.strip()}\nbrute output:\n{brute_out.strip()}')

    return 'ALL OK'

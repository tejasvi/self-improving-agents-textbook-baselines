import re
import subprocess

SAMPLE_RE = re.compile(
    r'Sample Input\s*(\d+)\s*\n(.*?)\n\s*Sample Output\s*\1\s*\n(.*?)(?=\n\s*\n|\n\s*Sample Input|\n## |\Z)',
    re.DOTALL,
)

# Statements that accept several different correct outputs. For these, byte/token differences
# are not failures by themselves: a validator / brute-force existence checker is needed.
MULTI_ANSWER_RE = re.compile(
    r'any of them|multiple solutions|any valid|any one of|if there are multiple',
    re.IGNORECASE,
)

DIFFERENT_LABEL = 'DIFFERENT (multi-answer problem: write a validator)'
MULTI_SUMMARY = 'MULTI-ANSWER: samples not exact; validate with a checker'


def tool_info():
    return {
        'name': 'run_samples',
        'description': (
            'Run a Python solution file on every sample input found in the problem statement and '
            'compare its output with the expected sample output. Reports PASS or MISMATCH (with expected '
            'and actual output) for each sample, and a final summary line. Any mismatch is a failure, '
            'even if the output is a different valid answer, because the grader may compare exactly.'
        ),
        'input_schema': {
            'type': 'object',
            'properties': {
                'solution_path': {
                    'type': 'string',
                    'description': 'Path to the Python solution file (reads stdin, writes stdout).',
                },
                'problem_text': {
                    'type': 'string',
                    'description': 'The full problem statement containing "Sample Input N" / "Sample Output N" blocks.',
                },
                'python': {
                    'type': 'string',
                    'description': 'Python interpreter to use. Defaults to python3.',
                },
            },
            'required': ['solution_path', 'problem_text'],
        },
    }


def _norm(text):
    return text.split()


def tool_function(solution_path, problem_text, python='python3'):
    python = python or 'python3'  # optional arg may arrive as None
    pairs = SAMPLE_RE.findall(problem_text or '')
    if not pairs:
        return 'No "Sample Input N" / "Sample Output N" pairs found in problem_text.'

    multi_answer = bool(MULTI_ANSWER_RE.search(problem_text or ''))
    lines = []
    failures = 0
    multi_differs = 0
    for idx, inp, expected in pairs:
        inp_text = inp.strip('\n') + '\n'
        try:
            proc = subprocess.run(
                [python, solution_path],
                input=inp_text,
                capture_output=True,
                text=True,
                timeout=10,
            )
            got = proc.stdout
            if proc.returncode != 0:
                lines.append(f'Sample {idx}: MISMATCH (runtime error, exit code {proc.returncode})')
                lines.append(f'expected: {expected.strip()}')
                lines.append(f'got: {got.strip()}')
                lines.append(f'stderr: {proc.stderr.strip()[-1000:]}')
                failures += 1
                continue
        except subprocess.TimeoutExpired:
            lines.append(f'Sample {idx}: MISMATCH (timeout after 10s)')
            failures += 1
            continue

        if _norm(got) == _norm(expected):
            lines.append(f'Sample {idx}: PASS')
        elif multi_answer:
            multi_differs += 1
            lines.append(f'Sample {idx}: {DIFFERENT_LABEL}')
            lines.append(f'expected: {expected.strip()}')
            lines.append(f'got: {got.strip()}')
        else:
            lines.append(f'Sample {idx}: MISMATCH')
            lines.append(f'expected: {expected.strip()}')
            lines.append(f'got: {got.strip()}')
            failures += 1

    if failures == 0 and multi_differs == 0:
        lines.append('ALL SAMPLES EXACT MATCH')
    if failures:
        lines.append(f'{failures} SAMPLE(S) DIFFER')
    if multi_differs:
        lines.append(MULTI_SUMMARY)
    return '\n'.join(lines)

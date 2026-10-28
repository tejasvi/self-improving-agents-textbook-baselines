import os
import re
import subprocess

def tool_info():
    return {
        "name": "run_samples",
        "description": """Extract the sample input/output pairs from a problem statement and run a Python solution on each of them.\n
* For each sample it reports PASS (whitespace-normalised tokens identical to the expected output) or DIFFERS, together with the expected and the actual raw output.\n
* Use it after writing the solution. If any sample DIFFERS, do not accept the difference just because the statement allows several answers: the grader may compare outputs exactly. Revise the construction so that the output matches the sample byte for byte.\n
* Samples are recognised from headers such as 'Sample Input 1' / 'Sample Output 1', 'Input:' / 'Output:' / 'Expected output:' and similar variants.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "problem_text": {
                    "type": "string",
                    "description": "The full problem statement text containing the sample inputs and outputs."
                },
                "solution_path": {
                    "type": "string",
                    "description": "Absolute path to the Python solution file to run. Defaults to /dgm/solution.py."
                },
                "command": {
                    "type": "string",
                    "description": "Optional run command prefix. Defaults to 'python3 <solution_path>'. The sample input is fed on standard input."
                }
            },
            "required": ["problem_text"]
        }
    }

TIMEOUT_SECONDS = 10

_INPUT_HEADER = re.compile(
    r'^[ \t#*_`>]*(?:sample[ \t]+input|example[ \t]+input|input)[ \t]*(\d*)[ \t]*[:.]?[*_`]*[ \t]*$',
    re.IGNORECASE | re.MULTILINE,
)
_OUTPUT_HEADER = re.compile(
    r'^[ \t#*_`>]*(?:sample[ \t]+output|example[ \t]+output|expected[ \t]+output|output)[ \t]*(\d*)[ \t]*[:.]?[*_`]*[ \t]*$',
    re.IGNORECASE | re.MULTILINE,
)
_HEADER_ANY = re.compile(
    r'^[ \t#*_`>]*(?:sample[ \t]+input|example[ \t]+input|input|sample[ \t]+output|example[ \t]+output|expected[ \t]+output|output)[ \t]*\d*[ \t]*[:.]?[*_`]*[ \t]*$',
    re.IGNORECASE | re.MULTILINE,
)


def _strip_fence(block):
    # A sample block ends at the first blank line (text after it is prose, not data).
    block = block.lstrip('\n')
    parts = re.split(r'\n[ \t]*\n', block, maxsplit=1)
    block = parts[0]
    lines = [l for l in block.split('\n') if not l.strip().startswith('```')]
    return '\n'.join(lines).strip('\n')


def parse_samples(problem_text):
    """
    Return a list of (input_text, expected_output_text) pairs in order of appearance.
    Blocks are matched by the 'k' index when present, otherwise by order.
    """
    inputs = []   # list of (index, text)
    outputs = []  # list of (index, text)
    headers = list(_HEADER_ANY.finditer(problem_text))
    for i, m in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(problem_text)
        body = problem_text[m.end():end]
        line = m.group(0)
        mi = _INPUT_HEADER.match(line)
        mo = _OUTPUT_HEADER.match(line)
        if mi:
            inputs.append((mi.group(1), _strip_fence(body)))
        elif mo:
            outputs.append((mo.group(1), _strip_fence(body)))

    pairs = []
    if inputs and outputs:
        out_by_idx = {}
        for idx, text in outputs:
            out_by_idx.setdefault(idx, text)
        for k, (idx, text) in enumerate(inputs):
            if idx and idx in out_by_idx:
                pairs.append((text, out_by_idx[idx]))
            elif not idx and k < len(outputs):
                pairs.append((text, outputs[k][1]))
    return pairs


def _tokens(text):
    return text.split()


def tool_function(problem_text: str, solution_path: str = "/dgm/solution.py", command: str = None) -> str:
    try:
        pairs = parse_samples(problem_text or "")
    except Exception as e:
        return f"Error parsing samples: {e}"
    if not pairs:
        return "No sample input/output pairs were found in the problem text."

    if command:
        cmd = command
        argv = None
    else:
        cmd = None
        argv = ["python3", solution_path]

    reports = []
    all_pass = True
    for k, (inp, expected) in enumerate(pairs, 1):
        errored = False
        try:
            if argv is not None:
                proc = subprocess.run(argv, input=inp + "\n", capture_output=True, text=True,
                                      timeout=TIMEOUT_SECONDS, cwd=os.path.dirname(solution_path) or None)
            else:
                proc = subprocess.run(cmd, shell=True, input=inp + "\n", capture_output=True, text=True,
                                      timeout=TIMEOUT_SECONDS)
            actual = proc.stdout
            err = proc.stderr
            status_note = "" if proc.returncode == 0 else f"\n(exit code {proc.returncode})\nstderr:\n{err}"
            errored = proc.returncode != 0
        except subprocess.TimeoutExpired:
            actual = ""
            status_note = f"\n(timed out after {TIMEOUT_SECONDS}s)"
            errored = True
        except Exception as e:
            actual = ""
            status_note = f"\n(failed to run: {e})"
            errored = True

        if not errored and _tokens(actual) == _tokens(expected):
            status = "PASS"
        else:
            status = "DIFFERS"
            all_pass = False
        reports.append(
            f"Sample {k}: {status}\n"
            f"--- input ---\n{inp}\n"
            f"--- expected output ---\n{expected}\n"
            f"--- actual output ---\n{actual}{status_note}"
        )

    summary = "All samples PASS." if all_pass else "Some samples DIFFER: revise the solution to match the expected outputs exactly."
    return summary + "\n\n" + "\n\n".join(reports)

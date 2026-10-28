import glob
import os
import subprocess

MAX_SHOW = 800  # max characters shown for expected/actual output per sample


def tool_info():
    return {
        "name": "sample_check",
        "description": """Run the solution on every sample input and compare its output with the expected sample output, token by token.\n
* For each `sampleN.in` (matched by `samples_glob`, default 'sample*.in') that has a `sampleN.out` next to it, the solution command is run through the shell with stdin taken from the .in file.\n
* Stdout is compared with the .out file after whitespace-token normalization. Each sample is reported as 'sampleN: EXACT' or 'sampleN: DIFFERENT', and DIFFERENT samples show the expected and actual output.\n
* A final line says 'ALL EXACT' or reports how many samples differ. A DIFFERENT result on a problem that allows several valid answers means the output may not match the hidden reference: try deterministic tie-break variants before accepting it.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_cmd": {
                    "type": "string",
                    "description": "Shell command that runs the solution reading stdin and writing stdout, e.g. 'python3 solution.py'. Default 'python3 solution.py'."
                },
                "samples_glob": {
                    "type": "string",
                    "description": "Glob pattern (relative to the working directory) matching the sample input files, e.g. 'sample*.in'. Default 'sample*.in'."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Time limit in seconds for each sample run. Default 10."
                }
            },
            "required": []
        }
    }


def _cwd():
    try:
        from tools import bash as _bash
        cwd = _bash._STATE.get('cwd')
        if cwd and os.path.isdir(cwd):
            return cwd
    except Exception:
        pass
    return os.getcwd()


def _clip(s, n=MAX_SHOW):
    if s is None:
        return ""
    s = s.rstrip()
    if len(s) <= n:
        return s
    return s[: n // 2] + f"\n... <{len(s) - n} characters truncated> ...\n" + s[-n // 2:]


def tool_function(solution_cmd='python3 solution.py', samples_glob='sample*.in', timeout=10):
    try:
        return _check(solution_cmd or 'python3 solution.py', samples_glob or 'sample*.in',
                      int(timeout) if timeout else 10)
    except Exception as e:
        return f"Error: sample_check failed internally: {type(e).__name__}: {e}"


def _check(solution_cmd, samples_glob, timeout):
    timeout = max(1, min(timeout, 300))
    cwd = _cwd()
    pattern = samples_glob if os.path.isabs(samples_glob) else os.path.join(cwd, samples_glob)
    in_files = sorted(glob.glob(pattern))
    if not in_files:
        return f"Error: no files match '{samples_glob}' in {cwd}."

    lines = []
    total = 0
    differ = 0
    for in_path in in_files:
        base = in_path[:-len('.in')] if in_path.endswith('.in') else in_path
        out_path = base + '.out'
        if not os.path.isfile(out_path):
            continue
        total += 1
        name = os.path.basename(base)
        with open(in_path, 'rb') as fin:
            try:
                p = subprocess.run(solution_cmd, shell=True, cwd=cwd, stdin=fin,
                                   capture_output=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                differ += 1
                lines.append(f"{name}: DIFFERENT (timed out after {timeout} seconds)")
                continue
        actual = p.stdout.decode('utf-8', errors='replace')
        err = p.stderr.decode('utf-8', errors='replace')
        with open(out_path, 'r', encoding='utf-8', errors='replace') as f:
            expected = f.read()
        if p.returncode != 0:
            differ += 1
            lines.append(f"{name}: DIFFERENT (exit code {p.returncode})\n"
                         f"actual stderr:\n{_clip(err)}")
            continue
        if actual.split() == expected.split():
            lines.append(f"{name}: EXACT")
        else:
            differ += 1
            lines.append(f"{name}: DIFFERENT\nexpected:\n{_clip(expected)}\nactual:\n{_clip(actual)}")

    if total == 0:
        return f"Error: no sample file in {cwd} matching '{samples_glob}' has a matching .out file."
    if differ == 0:
        lines.append(f"ALL EXACT ({total} samples)")
    else:
        lines.append(f"{differ} samples differ: possible canonical-answer mismatch "
                     f"(of {total} samples). Do not accept this just because several answers are allowed; "
                     f"try deterministic tie-break variants.")
    return "\n".join(lines)

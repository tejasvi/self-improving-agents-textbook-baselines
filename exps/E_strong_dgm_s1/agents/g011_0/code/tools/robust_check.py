import os
import shutil
import subprocess
import sys
import tempfile

PRELUDES = [
    ("none", ""),
    ("math", "from math import *\n"),
    ("typing", "from typing import *\n"),
    ("itertools_collections_functools",
     "from itertools import *\nfrom collections import *\nfrom functools import *\n"),
    ("all", "from math import *\nfrom typing import *\nfrom itertools import *\nfrom collections import *\nfrom functools import *\n"),
]


def tool_info():
    return {
        "name": "robust_check",
        "description": """Simulate the hidden grader's environment for a Python solution and report raw results.

* Copies the solution to a temp directory and runs it with `python3 -I` on every input file, under several preludes: none, `from math import *`, `from typing import *`, `from itertools/collections/functools import *`, and all of them combined. The prelude is prepended to the solution code, mimicking a harness that star-imports modules into the namespace (for example `math.pow` shadows the builtin 3-argument `pow`).
* Returns a raw table with one row per (variant, input): variant name, input file, exit code, stdout head, and stderr tail, plus a line stating which variants produce output different from the baseline (no prelude).
* Errors are NOT parsed; read the raw output and fix the solution accordingly.
* If no input files are given, the solution is run once with empty stdin.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {"type": "string", "description": "Path to the Python solution file (e.g. solution.py)."},
                "input_files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Paths to input files to feed to the solution's stdin, one run per file."
                },
                "timeout": {"type": "integer", "description": "Per-run time limit in seconds (default 10)."}
            },
            "required": ["solution_path"]
        }
    }


def _clip(s, n):
    s = s or ""
    if len(s) <= n:
        return s
    return s[:n] + f"...<{len(s) - n} more chars>"


def _tail(s, n):
    s = s or ""
    if len(s) <= n:
        return s
    return f"<{len(s) - n} earlier chars>..." + s[-n:]


def tool_function(solution_path, input_files=None, timeout=10):
    try:
        timeout = max(1, min(int(timeout or 10), 120))
    except (TypeError, ValueError):
        timeout = 10
    if not os.path.isfile(solution_path):
        return f"Error: solution file not found: {solution_path}"
    with open(solution_path, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()
    input_files = list(input_files or [])
    for p in input_files:
        if not os.path.isfile(p):
            return f"Error: input file not found: {p}"

    # Each input is (label, bytes-of-stdin)
    inputs = []
    if not input_files:
        inputs.append(("<empty stdin>", b""))
    else:
        for p in input_files:
            with open(p, "rb") as f:
                inputs.append((p, f.read()))

    lines = []
    failures = []
    outputs = {}  # (variant, input label) -> stdout
    tmpdir = tempfile.mkdtemp(prefix="robust_check_")
    try:
        for vname, prelude in PRELUDES:
            path = os.path.join(tmpdir, f"variant_{vname}.py")
            with open(path, "w", encoding="utf-8") as f:
                f.write(prelude + code)
            for label, data in inputs:
                try:
                    p = subprocess.run([sys.executable, "-I", path], input=data, capture_output=True,
                                       timeout=timeout, cwd=tmpdir)
                    rc = str(p.returncode)
                    out = p.stdout.decode("utf-8", errors="replace")
                    err = p.stderr.decode("utf-8", errors="replace")
                except subprocess.TimeoutExpired as e:
                    rc = f"TIMEOUT({timeout}s)"
                    out = (e.stdout or b"").decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
                    err = (e.stderr or b"").decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
                outputs[(vname, label)] = out
                if rc != "0":
                    failures.append(f"{vname} on {label} (exit {rc})")
                lines.append(
                    f"variant={vname} | input={label} | exit={rc}\n"
                    f"  stdout(head): {_clip(out.strip(), 300)!r}\n"
                    f"  stderr(tail): {_tail(err.strip(), 800)!r}"
                )
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # Compare every variant against the baseline ("none") per input.
    diffs = []
    for vname, _ in PRELUDES[1:]:
        for label, _ in inputs:
            base = outputs.get(("none", label))
            cur = outputs.get((vname, label))
            if base is not None and cur is not None and base.strip() != cur.strip():
                diffs.append(f"{vname} on {label}")
    summary = "\n".join(lines)
    if failures:
        summary += "\n\nNON-ZERO EXIT: " + "; ".join(failures)
    if diffs:
        summary += "\n\nDIFFERENT OUTPUTS vs baseline (variant none): " + "; ".join(diffs)
    else:
        summary += "\n\nAll variants produced the same stdout as the baseline (variant none)."
    return summary

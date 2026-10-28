import os
import subprocess
import sys
import time
from decimal import Decimal, Context, InvalidOperation

MAX_TESTS = 2000
MAX_TIMEOUT = 60
MAX_INPUTS_CLIP = 300
TOP_K = 10
PREC = 60
CLIP = 600


def tool_info():
    return {
        "name": "precision_check",
        "description": """Measure the numeric accuracy of a solution's floating-point output against a high-precision reference program.

* Inputs: either `input_files` (explicit stdin files), or `generator_path` run as `generator <seed>` for seeds seed_start..seed_start+num_tests-1.
* For each input, runs `solution_path` and `reference_path` (a program written with fractions.Fraction or decimal that prints the exact/high-precision answer). Files ending in .py run with the current Python interpreter; other files run directly.
* From each output, takes the FIRST whitespace-separated token that parses as a finite number (decimal.Decimal) and computes abs error = |sol - ref| and rel error = abs error / |ref|.
* Returns a raw report: the worst 10 cases (by relative error) with input head, both raw outputs, abs and rel error; the max abs and max rel error overall; and an explicit WARNING line if any relative error exceeds `rel_threshold`.
* Errors are NOT interpreted: runs that crash, time out, or print no number are listed raw with their stderr tail.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the solution program (reads stdin, prints the numeric answer)."
                },
                "reference_path": {
                    "type": "string",
                    "description": "Path to the high-precision reference program (reads stdin, prints the high-precision answer, e.g. using fractions.Fraction or decimal with >= 50 digits)."
                },
                "generator_path": {
                    "type": "string",
                    "description": "Optional path to an input generator, run as `generator <seed>`, printing one test input to stdout. Used when input_files is not given."
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of seeds to test when using generator_path (default 50)."
                },
                "seed_start": {
                    "type": "integer",
                    "description": "First seed value when using generator_path (default 0)."
                },
                "input_files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of input files to feed to both programs (takes precedence over generator_path)."
                },
                "rel_threshold": {
                    "type": "number",
                    "description": "Relative error threshold; the report warns if the max relative error exceeds it (default 1e-11)."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Per-run time limit in seconds for generator, solution and reference (default 10)."
                }
            },
            "required": ["solution_path", "reference_path"]
        }
    }


def _cmd(path):
    if path.endswith(".py"):
        return [sys.executable, path]
    return [os.path.abspath(path)]


def _clip(s, n=CLIP):
    s = s or ""
    if len(s) <= n:
        return s
    return s[:n] + f"...<{len(s) - n} more chars>"


def _run(cmd, data, timeout):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, input=data, capture_output=True, timeout=timeout)
        return {
            "timeout": False,
            "rc": p.returncode,
            "stdout": p.stdout.decode("utf-8", errors="replace"),
            "stderr": p.stderr.decode("utf-8", errors="replace"),
            "elapsed": time.time() - t0,
        }
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = e.stderr.decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        return {"timeout": True, "rc": None, "stdout": out, "stderr": err, "elapsed": time.time() - t0}


_CTX = Context(prec=PREC)


def _first_number(text):
    """First whitespace token that parses as a finite Decimal, or None."""
    for tok in (text or "").split():
        try:
            d = _CTX.create_decimal(tok)
        except (InvalidOperation, ValueError):
            continue
        if d.is_finite():
            return d
    return None


def _errors(sol_val, ref_val):
    """Return (abs_err, rel_err) as Decimals; rel is None when ref is 0 and abs > 0."""
    diff = _CTX.abs(_CTX.subtract(sol_val, ref_val))
    if ref_val == 0:
        rel = Decimal(0) if diff == 0 else None
    else:
        rel = _CTX.divide(diff, _CTX.abs(ref_val))
    return diff, rel


def _fmt(d):
    if d is None:
        return "undefined(ref=0)"
    return f"{d:.6E}"


def tool_function(solution_path, reference_path, generator_path=None, num_tests=50, seed_start=0,
                  input_files=None, rel_threshold=1e-11, timeout=10):
    try:
        num_tests = max(1, min(int(num_tests if num_tests is not None else 50), MAX_TESTS))
    except (TypeError, ValueError):
        num_tests = 50
    try:
        seed_start = int(seed_start if seed_start is not None else 0)
    except (TypeError, ValueError):
        seed_start = 0
    try:
        timeout = max(1, min(int(timeout if timeout is not None else 10), MAX_TIMEOUT))
    except (TypeError, ValueError):
        timeout = 10
    try:
        rel_threshold = float(rel_threshold) if rel_threshold is not None else 1e-11
    except (TypeError, ValueError):
        rel_threshold = 1e-11

    for label, p in [("solution", solution_path), ("reference", reference_path)]:
        if not p or not os.path.isfile(p):
            return f"Error: {label} file not found: {p}"
    if not input_files and (not generator_path or not os.path.isfile(generator_path)):
        return "Error: provide input_files or an existing generator_path."
    for p in (input_files or []):
        if not os.path.isfile(p):
            return f"Error: input file not found: {p}"

    # Build the list of (label, stdin bytes)
    inputs = []
    gen_failure = None
    if input_files:
        for p in input_files:
            with open(p, "rb") as f:
                inputs.append((p, f.read()))
    else:
        gen_cmd = _cmd(generator_path)
        for k in range(num_tests):
            seed = seed_start + k
            g = _run(gen_cmd + [str(seed)], b"", timeout)
            if g["timeout"] or g["rc"] != 0:
                gen_failure = (seed, g)
                break
            inputs.append((f"seed {seed}", g["stdout"].encode("utf-8")))

    sol_cmd = _cmd(solution_path)
    ref_cmd = _cmd(reference_path)

    rows = []          # dicts for each input with both numbers
    raw_issues = []    # runs with no number / crash / timeout, shown raw
    max_abs = None
    max_rel = None
    max_rel_label = None
    compared = 0  # inputs where both programs printed a number

    for label, data in inputs:
        sol = _run(sol_cmd, data, timeout)
        ref = _run(ref_cmd, data, timeout)
        head = _clip(data.decode("utf-8", errors="replace").strip(), 200)
        if ref["timeout"] or ref["rc"] != 0:
            raw_issues.append(
                f"[REFERENCE {'TIMEOUT' if ref['timeout'] else 'exit=' + str(ref['rc'])}] input={label}\n"
                f"  input head: {head!r}\n  reference stdout: {_clip(ref['stdout'], 200)!r}\n"
                f"  reference stderr tail: {_clip(ref['stderr'][-400:], 400)!r}")
            continue
        if sol["timeout"] or sol["rc"] != 0:
            raw_issues.append(
                f"[SOLUTION {'TIMEOUT' if sol['timeout'] else 'exit=' + str(sol['rc'])}] input={label}\n"
                f"  input head: {head!r}\n  solution stdout: {_clip(sol['stdout'], 200)!r}\n"
                f"  solution stderr tail: {_clip(sol['stderr'][-400:], 400)!r}")
            continue
        sv = _first_number(sol["stdout"])
        rv = _first_number(ref["stdout"])
        if sv is None or rv is None:
            raw_issues.append(
                f"[NO NUMBER] input={label}\n  input head: {head!r}\n"
                f"  solution stdout: {_clip(sol['stdout'], 200)!r}\n"
                f"  reference stdout: {_clip(ref['stdout'], 200)!r}")
            continue
        compared += 1
        abs_e, rel_e = _errors(sv, rv)
        if max_abs is None or abs_e > max_abs:
            max_abs = abs_e
        if rel_e is None:
            # reference is exactly 0 but solution is not: relative error is infinite
            rel_inf = True
        else:
            rel_inf = False
            if max_rel is None or rel_e > max_rel:
                max_rel = rel_e
                max_rel_label = label
        rows.append({
            "label": label, "head": head,
            "sol_out": _clip(sol["stdout"].strip(), 200),
            "ref_out": _clip(ref["stdout"].strip(), 200),
            "sv": sv, "rv": rv, "abs": abs_e, "rel": rel_e, "rel_inf": rel_inf,
        })

    # Sort: infinite (ref==0) first, then by rel desc
    rows.sort(key=lambda r: (0 if r["rel_inf"] else 1, -(r["rel"] or 0), -r["abs"]))
    top = rows[:TOP_K]

    out = []
    out.append(f"Compared {compared} input(s) with both programs producing a number "
               f"({len(inputs)} input(s) total).")
    if gen_failure is not None:
        seed, g = gen_failure
        status = "TIMEOUT" if g["timeout"] else f"exit={g['rc']}"
        out.append(f"GENERATOR FAILED at seed {seed} ({status}); stopped early. stderr: "
                   f"{_clip(g['stderr'][-400:], 400)!r}")
    if compared:
        any_inf = any(r["rel_inf"] for r in rows)
        out.append(f"MAX_ABS_ERROR: {_fmt(max_abs)}")
        if any_inf:
            out.append("MAX_REL_ERROR: inf (reference is 0 but solution is nonzero on "
                       f"{sum(1 for r in rows if r['rel_inf'])} input(s))")
        else:
            out.append(f"MAX_REL_ERROR: {_fmt(max_rel)} (at {max_rel_label})")
        exceeds = any_inf or (max_rel is not None and max_rel > Decimal(repr(rel_threshold)))
        if exceeds:
            out.append(f"WARNING: relative error exceeds rel_threshold={rel_threshold:g} on at least one input.")
        else:
            out.append(f"OK: max relative error is within rel_threshold={rel_threshold:g}.")
        out.append("")
        out.append(f"Worst {len(top)} case(s) by relative error:")
        for i, r in enumerate(top, 1):
            out.append(
                f"#{i} input={r['label']}\n"
                f"  input head: {r['head']!r}\n"
                f"  solution output: {r['sol_out']!r}  (first number {_fmt(r['sv'])})\n"
                f"  reference output: {r['ref_out']!r}  (first number {_fmt(r['rv'])})\n"
                f"  abs error: {_fmt(r['abs'])}  rel error: "
                f"{'inf' if r['rel_inf'] else _fmt(r['rel'])}")
    if raw_issues:
        out.append("")
        out.append(f"Raw run issues ({len(raw_issues)}):")
        out.extend(raw_issues[:TOP_K])
        if len(raw_issues) > TOP_K:
            out.append(f"...<{len(raw_issues) - TOP_K} more issue(s)>")
    return "\n".join(out)

import os
import shutil
import subprocess
import sys
import tempfile
import time

MAX_TESTS = 100000
MAX_TIMEOUT = 60
CLIP = 4000


def tool_info():
    return {
        "name": "stress_test",
        "description": """Run a randomized/exhaustive stress test of a solution against a brute-force reference.

* For each seed i in [seed_start, seed_start + num_tests): runs `generator_path i` (the seed is passed as argv[1]; the generator prints one test input to stdout), feeds that input via stdin to both `solution_path` and `brute_path`, and compares their whitespace-normalized stdout.
* Each run of solution/brute/generator has its own `timeout` (seconds). Files ending in .py are run with the current Python interpreter; other files are executed directly.
* Stops at the first mismatch and returns the raw result: the failing seed, the input, both outputs (with exit codes and runtimes), and both stderr streams, plus the number of passing tests and the maximum solution runtime.
* Errors are NOT parsed; read the raw output and interpret it yourself.
* For exhaustive coverage, make the generator map the seed to the i-th case of an enumeration of small inputs.
* Optional tolerance mode: if `rel_tol` and/or `abs_tol` is given, outputs are compared token by token; tokens that both parse as floats are equal when within tolerance (|a-b| <= max(abs_tol, rel_tol*|b|)), other tokens must match exactly. Without them, comparison is exact whitespace-normalized text.
* The max numeric deviation seen across all tests is reported on the final line, even on PASS.
* Checker mode (for problems with several valid answers): if `checker_path` is given, `brute_path` is optional. For each seed the generator input is saved to a temp file and the solution output to another; the checker is run as `checker input_file output_file [brute_output_file]` (brute_output_file is passed only when brute_path is also given). Exit code 0 means the case passes; any other exit code is a failure. The checker's raw stdout/stderr is reported on failure. In checker mode outputs are NOT compared with each other; the checker alone decides validity.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the solution program (reads stdin, writes stdout), e.g. solution.py."
                },
                "brute_path": {
                    "type": "string",
                    "description": "Path to the brute-force reference program (reads stdin, writes stdout). Required unless checker_path is given; when both are given, the brute output is also passed to the checker as its third argument."
                },
                "checker_path": {
                    "type": "string",
                    "description": "Optional path to a checker program for multi-answer problems, run as `checker input_file output_file [brute_output_file]`. Exit code 0 = valid, anything else = failure; its stdout/stderr are reported raw on failure. If given, brute_path becomes optional."
                },
                "generator_path": {
                    "type": "string",
                    "description": "Path to the input generator. It is run as `generator <seed>` and must print one test input to stdout."
                },
                "num_tests": {
                    "type": "integer",
                    "description": "Number of seeds to test (default 300)."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Per-run time limit in seconds for the generator, solution and brute force (default 10)."
                },
                "seed_start": {
                    "type": "integer",
                    "description": "First seed value (default 0)."
                },
                "rel_tol": {
                    "type": "number",
                    "description": "Optional relative tolerance for numeric tokens (e.g. 1e-9). If omitted (and abs_tol omitted), outputs must match exactly."
                },
                "abs_tol": {
                    "type": "number",
                    "description": "Optional absolute tolerance for numeric tokens. If omitted, defaults to 0 when rel_tol is given."
                }
            },
            "required": ["solution_path", "generator_path"]
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
    """Run a command with stdin=data. Returns a dict with raw results."""
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
        return {
            "timeout": True,
            "rc": None,
            "stdout": out,
            "stderr": err,
            "elapsed": time.time() - t0,
        }


def _describe(name, r):
    if r["timeout"]:
        status = f"TIMEOUT after {r['elapsed']:.2f}s"
    else:
        status = f"exit={r['rc']}, time={r['elapsed']:.2f}s"
    return (
        f"--- {name} output ({status}) ---\n{_clip(r['stdout'])}\n"
        f"--- {name} stderr ---\n{_clip(r['stderr'])}\n"
    )


def _to_float(tok):
    try:
        v = float(tok)
    except ValueError:
        return None
    return v


def _compare(sol_out, brute_out, rel_tol, abs_tol):
    """Return (ok, max_deviation).

    ok: exact whitespace-normalized equality when no tolerance is set; otherwise
        tokens that both parse as floats must be within tolerance, other tokens exact.
    max_deviation: largest |a-b| over numeric token pairs that differ (always measured).
    """
    a_tokens = sol_out.split()
    b_tokens = brute_out.split()
    tol_mode = rel_tol is not None or abs_tol is not None
    if not tol_mode:
        ok = " ".join(a_tokens) == " ".join(b_tokens)
    else:
        ok = len(a_tokens) == len(b_tokens)
    rt = rel_tol if rel_tol is not None else 0.0
    at = abs_tol if abs_tol is not None else 0.0
    max_dev = 0.0
    if len(a_tokens) == len(b_tokens):
        for x, y in zip(a_tokens, b_tokens):
            if x == y:
                continue
            fx, fy = _to_float(x), _to_float(y)
            if fx is None or fy is None:
                if tol_mode:
                    ok = False
                continue
            dev = abs(fx - fy)
            if dev != dev:  # NaN (e.g. inf vs inf differing text, or nan)
                if tol_mode:
                    ok = False
                continue
            max_dev = max(max_dev, dev)
            if tol_mode and dev > max(at, rt * abs(fy)):
                ok = False
    elif tol_mode:
        ok = False
    return ok, max_dev


def _check_case(checker_path, input_file, output_file, brute_output_file, timeout):
    """Run `checker input_file output_file [brute_output_file]`. Returns the raw run dict."""
    args = _cmd(checker_path) + [input_file, output_file]
    if brute_output_file is not None:
        args.append(brute_output_file)
    t0 = time.time()
    try:
        p = subprocess.run(args, capture_output=True, timeout=timeout)
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


def _checker_mode(solution_path, brute_path, generator_path, checker_path, num_tests, timeout, seed_start):
    gen_cmd = _cmd(generator_path)
    sol_cmd = _cmd(solution_path)
    brute_cmd = _cmd(brute_path) if brute_path else None
    tmpdir = tempfile.mkdtemp(prefix="stress_checker_")
    in_file = os.path.join(tmpdir, "input.txt")
    out_file = os.path.join(tmpdir, "output.txt")
    bout_file = os.path.join(tmpdir, "brute_output.txt")
    passes = 0
    max_time = 0.0
    max_time_seed = None
    try:
        for k in range(num_tests):
            seed = seed_start + k
            g = _run(gen_cmd + [str(seed)], b"", timeout)
            if g["timeout"] or g["rc"] != 0:
                status = f"TIMEOUT after {timeout}s" if g["timeout"] else f"exit={g['rc']}"
                return (
                    f"GENERATOR FAILED at seed {seed} ({status}) after {passes} passing tests.\n"
                    f"--- generator stderr ---\n{_clip(g['stderr'])}"
                )
            data = g["stdout"].encode("utf-8")
            with open(in_file, "wb") as f:
                f.write(data)

            sol = _run(sol_cmd, data, timeout)
            if sol["elapsed"] > max_time:
                max_time = sol["elapsed"]
                max_time_seed = seed
            if sol["timeout"] or sol["rc"] != 0:
                return (
                    f"SOLUTION FAILED at seed {seed} (test {k + 1} of {num_tests}) after {passes} passing tests.\n"
                    f"--- input ---\n{_clip(g['stdout'])}\n"
                    + _describe("solution", sol)
                )
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(sol["stdout"])

            brute_arg = None
            if brute_cmd is not None:
                brute = _run(brute_cmd, data, timeout)
                if brute["timeout"] or brute["rc"] != 0:
                    return (
                        f"BRUTE FORCE FAILED at seed {seed} after {passes} passing tests.\n"
                        f"--- input ---\n{_clip(g['stdout'])}\n"
                        + _describe("brute", brute)
                    )
                with open(bout_file, "w", encoding="utf-8") as f:
                    f.write(brute["stdout"])
                brute_arg = bout_file

            chk = _check_case(checker_path, in_file, out_file, brute_arg, timeout)
            if chk["timeout"] or chk["rc"] != 0:
                status = f"TIMEOUT after {timeout}s" if chk["timeout"] else f"exit={chk['rc']}"
                return (
                    f"CHECKER REJECTED at seed {seed} (test {k + 1} of {num_tests}, checker {status}) "
                    f"after {passes} passing tests.\n"
                    f"--- input ---\n{_clip(g['stdout'])}\n"
                    f"--- solution output (time={sol['elapsed']:.2f}s) ---\n{_clip(sol['stdout'])}\n"
                    f"--- solution stderr ---\n{_clip(sol['stderr'])}\n"
                    f"--- checker stdout ---\n{_clip(chk['stdout'])}\n"
                    f"--- checker stderr ---\n{_clip(chk['stderr'])}\n"
                )
            passes += 1
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    return (
        f"PASS (checker mode): {passes}/{num_tests} tests accepted by checker "
        f"(seeds {seed_start}..{seed_start + num_tests - 1}).\n"
        f"Max solution runtime: {max_time:.2f}s (seed {max_time_seed})."
    )


def tool_function(solution_path, brute_path=None, generator_path=None, num_tests=300, timeout=10, seed_start=0,
                  rel_tol=None, abs_tol=None, checker_path=None):
    try:
        rel_tol = float(rel_tol) if rel_tol is not None else None
    except (TypeError, ValueError):
        rel_tol = None
    try:
        abs_tol = float(abs_tol) if abs_tol is not None else None
    except (TypeError, ValueError):
        abs_tol = None

    try:
        num_tests = max(1, min(int(num_tests if num_tests is not None else 300), MAX_TESTS))
    except (TypeError, ValueError):
        num_tests = 300
    try:
        timeout = max(1, min(int(timeout if timeout is not None else 10), MAX_TIMEOUT))
    except (TypeError, ValueError):
        timeout = 10
    try:
        seed_start = int(seed_start if seed_start is not None else 0)
    except (TypeError, ValueError):
        seed_start = 0

    if not brute_path and not checker_path:
        return "Error: provide brute_path (exact comparison) or checker_path (checker mode)."
    if not generator_path:
        return "Error: generator_path is required."

    to_check = [("solution", solution_path), ("generator", generator_path)]
    if brute_path:
        to_check.append(("brute", brute_path))
    if checker_path:
        to_check.append(("checker", checker_path))
    for label, p in to_check:
        if not p or not os.path.isfile(p):
            return f"Error: {label} file not found: {p}"

    if checker_path:
        return _checker_mode(solution_path, brute_path, generator_path, checker_path,
                             num_tests, timeout, seed_start)

    sol_cmd = _cmd(solution_path)
    brute_cmd = _cmd(brute_path)
    gen_cmd = _cmd(generator_path)

    passes = 0
    max_time = 0.0
    max_time_seed = None
    max_dev = 0.0
    max_dev_seed = None
    for k in range(num_tests):
        seed = seed_start + k
        g = _run(gen_cmd + [str(seed)], b"", timeout)
        if g["timeout"] or g["rc"] != 0:
            status = f"TIMEOUT after {timeout}s" if g["timeout"] else f"exit={g['rc']}"
            return (
                f"GENERATOR FAILED at seed {seed} ({status}) after {passes} passing tests.\n"
                f"--- generator stderr ---\n{_clip(g['stderr'])}"
            )
        data = g["stdout"].encode("utf-8")

        sol = _run(sol_cmd, data, timeout)
        if sol["elapsed"] > max_time:
            max_time = sol["elapsed"]
            max_time_seed = seed
        brute = _run(brute_cmd, data, timeout)

        if brute["timeout"] or brute["rc"] != 0:
            return (
                f"BRUTE FORCE FAILED at seed {seed} after {passes} passing tests.\n"
                f"--- input ---\n{_clip(g['stdout'])}\n"
                + _describe("brute", brute)
            )

        same = False
        dev = 0.0
        if not sol["timeout"] and sol["rc"] == 0:
            same, dev = _compare(sol["stdout"], brute["stdout"], rel_tol, abs_tol)
        if dev > max_dev:
            max_dev = dev
            max_dev_seed = seed
        if not same:
            return (
                f"MISMATCH at seed {seed} (test {k + 1} of {num_tests}) after {passes} passing tests.\n"
                f"--- input ---\n{_clip(g['stdout'])}\n"
                + _describe("solution", sol)
                + _describe("brute", brute)
                + f"Max solution runtime so far: {max_time:.2f}s (seed {max_time_seed})\n"
                + f"MAX_NUMERIC_DEVIATION: {max_dev:.3g} (seed {max_dev_seed})"
            )
        passes += 1

    return (
        f"PASS: {passes}/{num_tests} tests matched (seeds {seed_start}..{seed_start + num_tests - 1}).\n"
        f"Max solution runtime: {max_time:.2f}s (seed {max_time_seed}).\n"
        f"MAX_NUMERIC_DEVIATION: {max_dev:.3g} (seed {max_dev_seed}) "
        f"[abs deviation over numeric tokens that differed; mode: "
        f"{'exact' if rel_tol is None and abs_tol is None else f'tolerance rel_tol={rel_tol} abs_tol={abs_tol}'}]"
    )

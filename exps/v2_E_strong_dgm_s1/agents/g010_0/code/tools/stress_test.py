import os
import shutil
import subprocess
import tempfile

DEFAULT_SCALES = [1, 2, 3, 5, 8]
MAX_SHOW = 1500  # max characters shown for an input/output in the report


def tool_info():
    return {
        "name": "stress_test",
        "description": """Stress-test a program against a generator, an optional brute-force reference and an optional checker.\n
* `generator_cmd` is run as `<generator_cmd> <seed> <scale>` and must print one test input to stdout. Use the scale to control size (tiny / medium / large, duplicate-heavy cases).\n
* `solution_cmd` is run with the generated input on stdin (e.g. `python3 solution.py`).\n
* `reference_cmd` (optional) is a slow brute-force program run on the same input on stdin. Without a checker, its normalized output (whitespace-separated tokens) must equal the solution's output.\n
* `checker_cmd` (optional) is run as `<checker_cmd> input_file output_file [reference_output_file]`. Exit code 0 means the solution output is valid. Use it for problems with several valid answers (it should verify constraints and the answer, e.g. that printed indices really sum to X).\n
* Runs every seed in range(seeds_per_scale) for every scale in `scales`. Each run has a `timeout` in seconds.\n
* Returns a per-scale pass/fail summary and, for the first failure, the input (truncated if large), the solution output, the reference output and the checker/stderr output.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_cmd": {
                    "type": "string",
                    "description": "Shell command that runs the solution reading stdin and writing stdout, e.g. 'python3 solution.py'."
                },
                "generator_cmd": {
                    "type": "string",
                    "description": "Shell command invoked as '<generator_cmd> seed scale' that prints one test input to stdout, e.g. 'python3 gen.py'."
                },
                "reference_cmd": {
                    "type": "string",
                    "description": "Optional shell command for a brute-force reference solution reading stdin, e.g. 'python3 brute.py'."
                },
                "checker_cmd": {
                    "type": "string",
                    "description": "Optional shell command invoked as '<checker_cmd> input_file output_file [reference_output_file]'; exit code 0 means valid."
                },
                "scales": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of integer scales passed to the generator. Default [1, 2, 3, 5, 8]."
                },
                "seeds_per_scale": {
                    "type": "integer",
                    "description": "Number of seeds (0 .. seeds_per_scale-1) to run for each scale. Default 100."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Time limit in seconds for each single run of the generator, solution, reference or checker. Default 10."
                },
                "require_exact": {
                    "type": "boolean",
                    "description": "If true, and both reference_cmd and checker_cmd are given, an output that the checker accepts but that differs from the reference output (normalized whitespace tokens) counts as a failure. Default false (exact mismatches are only reported as informational)."
                }
            },
            "required": ["solution_cmd", "generator_cmd"]
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
    if len(s) <= n:
        return s
    return s[: n // 2] + f"\n... <{len(s) - n} characters truncated> ...\n" + s[-n // 2:]


def _run(cmd, cwd, timeout, stdin_path=None, args=()):
    """Run `cmd args...` through the shell. Returns (status, stdout_text, stderr_text).
    status is 'ok', 'timeout', 'crash' (nonzero exit) or 'error' (could not start)."""
    full = cmd if not args else cmd + " " + " ".join(str(a) for a in args)
    stdin = open(stdin_path, 'rb') if stdin_path else subprocess.DEVNULL
    try:
        p = subprocess.run(full, shell=True, cwd=cwd, stdin=stdin, capture_output=True,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return 'timeout', '', f"timed out after {timeout} seconds"
    except Exception as e:
        return 'error', '', f"could not run: {e}"
    finally:
        if stdin_path:
            stdin.close()
    out = p.stdout.decode('utf-8', errors='replace')
    err = p.stderr.decode('utf-8', errors='replace')
    if p.returncode != 0:
        return 'crash', out, f"exit code {p.returncode}\n{err}"
    return 'ok', out, err


def _norm(s):
    return s.split()


def tool_function(solution_cmd, generator_cmd, reference_cmd=None, checker_cmd=None,
                  scales=None, seeds_per_scale=100, timeout=10, require_exact=False):
    tmpdir = tempfile.mkdtemp(prefix="stress_")
    try:
        return _stress(solution_cmd, generator_cmd, reference_cmd, checker_cmd,
                       scales, seeds_per_scale, timeout, tmpdir, bool(require_exact))
    except Exception as e:
        return f"Error: stress_test failed internally: {type(e).__name__}: {e}"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _stress(solution_cmd, generator_cmd, reference_cmd, checker_cmd, scales, seeds_per_scale, timeout, tmpdir,
            require_exact=False):
    if not solution_cmd or not generator_cmd:
        return "Error: solution_cmd and generator_cmd are required."
    if not scales:
        scales = list(DEFAULT_SCALES)
    scales = [int(s) for s in scales]
    seeds_per_scale = int(seeds_per_scale) if seeds_per_scale is not None else 100
    seeds_per_scale = max(1, min(seeds_per_scale, 100000))
    timeout = int(timeout) if timeout else 10
    timeout = max(1, min(timeout, 300))
    cwd = _cwd()

    in_path = os.path.join(tmpdir, "input.txt")
    out_path = os.path.join(tmpdir, "output.txt")
    ref_out_path = os.path.join(tmpdir, "ref_output.txt")

    summary = []
    total = 0
    total_pass = 0
    first_fail = None  # dict with details
    exact_total = 0
    exact_total_ok = 0
    first_diff = None  # first checker-accepted output that differs from the reference
    both = bool(checker_cmd and reference_cmd)
    mode = ("checker" if checker_cmd else ("reference" if reference_cmd else "no-oracle (only run checks)"))

    for scale in scales:
        passed = 0
        ran = 0
        fails = 0
        exact = 0
        for seed in range(seeds_per_scale):
            ran += 1
            total += 1
            # 1. generate the input
            st, gen_out, gen_err = _run(generator_cmd, cwd, timeout, args=[seed, scale])
            if st != 'ok':
                fails += 1
                if first_fail is None:
                    first_fail = dict(kind=f"generator {st}", scale=scale, seed=seed, input=None,
                                      sol="", ref="", info=f"generator {st}: {gen_err}")
                continue
            with open(in_path, 'w') as f:
                f.write(gen_out)
            inp_text = gen_out

            def fail(kind, sol_out="", ref_out="", info=""):
                nonlocal fails, first_fail
                fails += 1
                if first_fail is None:
                    first_fail = dict(kind=kind, scale=scale, seed=seed, input=inp_text,
                                      sol=sol_out, ref=ref_out, info=info)

            # 2. reference output (optional)
            ref_out = None
            if reference_cmd:
                st, ro, re_ = _run(reference_cmd, cwd, timeout, stdin_path=in_path)
                if st != 'ok':
                    # the brute force is not trusted to be correct; report it as a failure of the setup
                    fail(f"reference {st}", "", ro, re_)
                    continue
                ref_out = ro
                with open(ref_out_path, 'w') as f:
                    f.write(ro)

            # 3. solution output
            st, so, se = _run(solution_cmd, cwd, timeout, stdin_path=in_path)
            if st != 'ok':
                fail(f"solution {st}", so, ref_out or "", se)
                continue
            with open(out_path, 'w') as f:
                f.write(so)

            # 4. verdict
            if checker_cmd:
                args = [in_path, out_path] + ([ref_out_path] if reference_cmd else [])
                st, co, ce = _run(checker_cmd, cwd, timeout, args=args)
                if st != 'ok':
                    fail(f"checker rejected ({st})", so, ref_out or "", (ce or co).strip())
                    continue
                if both:
                    exact_total += 1
                    if _norm(so) == _norm(ref_out):
                        exact += 1
                        exact_total_ok += 1
                    else:
                        if first_diff is None:
                            first_diff = dict(scale=scale, seed=seed, input=inp_text, sol=so, ref=ref_out)
                        if require_exact:
                            fail("valid but differs from reference (require_exact)", so, ref_out, "")
                            continue
            elif reference_cmd:
                if _norm(so) != _norm(ref_out):
                    fail("output mismatch with reference", so, ref_out, "")
                    continue
            passed += 1
            total_pass += 1
        line = f"scale {scale}: {passed}/{ran} passed" + (f", {fails} failed" if fails else "")
        if both:
            line += f"; exact-match-with-reference: {exact}/{ran}"
        summary.append(line)

    lines = [f"Stress test: mode={mode}, scales={scales}, seeds_per_scale={seeds_per_scale}, timeout={timeout}s",
             f"Total: {total_pass}/{total} passed"]
    lines += summary
    if both:
        lines.append(f"canonical (exact-match-with-reference) rate: {exact_total_ok}/{exact_total}")
        if first_diff is not None:
            fd = first_diff
            inp = fd['input']
            lines.append(f"Informational: first output valid per checker but differs from reference "
                         f"(scale={fd['scale']} seed={fd['seed']}):")
            lines.append(("--- input ---\n" + inp.rstrip()) if len(inp) <= MAX_SHOW
                         else f"--- input (truncated, {len(inp)} chars total) ---\n" + _clip(inp).rstrip())
            lines.append("--- solution output ---\n" + _clip(fd['sol']).rstrip())
            lines.append("--- reference output ---\n" + _clip(fd['ref']).rstrip())
            lines.append("Note: Solution is valid but differs from reference; if the grader compares exact output "
                         "against the reference/sample answer, align tie-breaking.")
    if first_fail is None:
        lines.append("ALL PASSED")
    else:
        ff = first_fail
        lines.append(f"FAILED ({ff['kind']}) at scale={ff['scale']} seed={ff['seed']}")
        if ff['input'] is not None:
            inp = ff['input']
            if len(inp) <= MAX_SHOW:
                lines.append("--- input ---\n" + inp.rstrip())
            else:
                lines.append(f"--- input (truncated, {len(inp)} chars total) ---\n" + _clip(inp).rstrip())
        if ff['sol'] != "":
            lines.append("--- solution output ---\n" + _clip(ff['sol']).rstrip())
        if ff['ref'] != "":
            lines.append("--- reference output ---\n" + _clip(ff['ref']).rstrip())
        if ff['info']:
            lines.append("--- stderr / checker output ---\n" + _clip(ff['info']).rstrip())
    return "\n".join(lines)

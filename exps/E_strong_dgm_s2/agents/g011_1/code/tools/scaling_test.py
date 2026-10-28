import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time

DEFAULT_KINDS = ['random', 'all_same', 'two_values', 'sorted', 'max_distinct']
DEFAULT_MAX = 100000
DRIVER_NAME = '_driver.py'
SOL_NAME = '_sol.py'
GEN_NAME = '_gen.py'


def tool_info():
    return {
        "name": "scaling_test",
        "description": """Time the final solution on structured, adversarial inputs at several input sizes and report how the runtime scales.\n
* MUST be run on the final solution (the file you are about to submit), after the sample tests pass.
* You write the generator: `python3 <generator_path> <n> <kind> <seed>` must print either the stdin text (mode 'stdin') or a JSON list of the method's arguments (mode 'method'). Use kinds such as all-identical elements, one dominant value, maximum number of distinct values, sorted, reverse-sorted, random, and worst cases for your algorithm.
* mode 'stdin': the solution is a complete program reading stdin. mode 'method': the solution defines `class Solution` and the method `method_name` is called with the JSON args; the internal call time is measured.
* Each (kind, size) run is executed in an isolated subprocess (`python3 -I`, scrubbed environment) under a wall-clock `timeout` in seconds. The `sizes` list is run in the given order; the LAST size should be the maximum constraint. Default sizes are doubling values up to 100000.
* Output: raw elapsed times per (kind, size), TIMEOUT / CRASH markers with stderr, and the log-log slope between consecutive sizes (slope = log(t2/t1) / log(n2/n1)). The tool does not judge the results: read the slope yourself. A slope near 2 at n=2*10^4 (or near 1 for linear-time solutions) is a red flag that the algorithm is quadratic. Any run over about 1.5s at max size must be fixed.
* If a kind times out at some size, larger sizes of that kind are not run (marked SKIPPED) to save time.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {
                    "type": "string",
                    "description": "Path to the Python solution file to time (e.g. /path/to/solution.py)."
                },
                "mode": {
                    "type": "string",
                    "description": "Either 'stdin' or 'method'. 'stdin' for a complete program reading standard input; 'method' for a `Solution` class method."
                },
                "method_name": {
                    "type": "string",
                    "description": "Name of the Solution method to call (required in 'method' mode)."
                },
                "generator_path": {
                    "type": "string",
                    "description": "Path to a Python generator script, invoked as `python3 gen.py <n> <kind> <seed>`. It prints the stdin text (stdin mode) or a JSON list of method arguments (method mode)."
                },
                "kinds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Input kinds passed to the generator as <kind>. Default: ['random','all_same','two_values','sorted','max_distinct']."
                },
                "sizes": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Input sizes n passed to the generator, in increasing order. The last one should be the max constraint. Default: doubling sizes 1000, 2000, 4000, ... up to 100000."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Wall-clock time limit per run in seconds (default 10, max 60)."
                }
            },
            "required": ["solution_path", "generator_path", "mode"]
        }
    }


def _clip(s, n=1500):
    if len(s) <= n:
        return s
    return s[: n // 2] + f"\n... <{len(s) - n} characters clipped> ...\n" + s[-n // 2:]


def _default_sizes():
    sizes = []
    n = 1000
    while n < DEFAULT_MAX:
        sizes.append(n)
        n *= 2
    sizes.append(DEFAULT_MAX)
    return sizes


def _as_text(x):
    if x is None:
        return ''
    if isinstance(x, bytes):
        return x.decode(errors='replace')
    return x


def _run_isolated(cmd, cwd, env, data, timeout):
    """Run a command; return (status, stdout, stderr, elapsed) with status in OK/TIMEOUT/CRASH."""
    start = time.time()
    try:
        p = subprocess.run(cmd, input=data, capture_output=True, text=True, cwd=cwd, env=env,
                           timeout=timeout, errors='replace')
    except subprocess.TimeoutExpired as e:
        return 'TIMEOUT', _as_text(e.stdout), _as_text(e.stderr), time.time() - start
    elapsed = time.time() - start
    if p.returncode != 0:
        return 'CRASH', p.stdout, p.stderr, elapsed
    return 'OK', p.stdout, p.stderr, elapsed


def _make_driver(method_name):
    # The driver loads the copied solution by file path (python -I does not add the script dir to sys.path).
    return f'''import importlib.util, json, sys, time, os
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("_sol_mod", os.path.join(here, {SOL_NAME!r}))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
with open(os.path.join(here, "_args.json")) as f:
    args = json.load(f)
obj = mod.Solution()
fn = getattr(obj, {method_name!r})
t0 = time.perf_counter()
res = fn(*args)
t1 = time.perf_counter()
print(repr(res))
print("__INTERNAL_ELAPSED__ %.6f" % (t1 - t0))
'''


def _slope(n1, t1, n2, t2):
    if t1 is None or t2 is None or t1 <= 0 or t2 <= 0 or n1 <= 0 or n2 <= 0 or n1 == n2:
        return None
    return math.log(t2 / t1) / math.log(n2 / n1)


def tool_function(solution_path, generator_path, mode='stdin', method_name=None, kinds=None,
                  sizes=None, timeout=10):
    if mode not in ('stdin', 'method'):
        return f"Error: mode must be 'stdin' or 'method', got {mode!r}"
    if mode == 'method' and not method_name:
        return "Error: method_name is required in 'method' mode."
    if not os.path.isfile(solution_path):
        return f"Error: solution file not found: {solution_path}"
    if not os.path.isfile(generator_path):
        return f"Error: generator file not found: {generator_path}"
    try:
        timeout = max(1, min(int(timeout or 10), 60))
    except (TypeError, ValueError):
        timeout = 10
    if isinstance(kinds, str):
        kinds = [kinds]
    if not kinds:
        kinds = list(DEFAULT_KINDS)
    if sizes is None or len(sizes) == 0:
        sizes = _default_sizes()
    if isinstance(sizes, (int, str)):
        sizes = [sizes]
    try:
        sizes = [int(s) for s in sizes]
    except (TypeError, ValueError):
        return f"Error: sizes must be integers, got {sizes!r}"
    if any(s <= 0 for s in sizes):
        return "Error: sizes must be positive integers."

    sol_abs = os.path.abspath(solution_path)
    gen_abs = os.path.abspath(generator_path)
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin')}
    py = sys.executable

    out = []
    out.append(f"== scaling_test: mode={mode}, method={method_name}, timeout={timeout}s, sizes={sizes} ==")

    with tempfile.TemporaryDirectory() as tmp:
        shutil.copyfile(sol_abs, os.path.join(tmp, SOL_NAME))
        gen_copy = os.path.join(tmp, GEN_NAME)
        shutil.copyfile(gen_abs, gen_copy)
        if mode == 'method':
            with open(os.path.join(tmp, DRIVER_NAME), 'w') as f:
                f.write(_make_driver(method_name))

        for kind in kinds:
            out.append(f"\n-- kind: {kind} --")
            out.append(f"{'n':>10} | {'status':<8} | {'wall_s':>9} | {'internal_s':>10} | {'slope':>6}")
            prev = None  # (n, time)
            timed_out = False
            for n in sizes:
                if timed_out:
                    out.append(f"{n:>10} | SKIPPED  | (a smaller size of this kind timed out)")
                    prev = None
                    continue
                # generate input
                g_status, g_out, g_err, _ = _run_isolated(
                    [py, '-I', GEN_NAME, str(n), kind, '0'], tmp, env, '', timeout)
                if g_status != 'OK':
                    out.append(f"{n:>10} | GEN_{g_status} | generator stderr: {_clip(g_err.strip())}")
                    prev = None
                    continue
                if mode == 'method':
                    try:
                        args = json.loads(g_out)
                    except ValueError as e:
                        out.append(f"{n:>10} | GEN_BAD  | generator did not print a JSON list: {e}; got {_clip(g_out.strip(), 200)!r}")
                        prev = None
                        continue
                    if not isinstance(args, list):
                        out.append(f"{n:>10} | GEN_BAD  | generator must print a JSON list of args")
                        prev = None
                        continue
                    with open(os.path.join(tmp, '_args.json'), 'w') as f:
                        json.dump(args, f)
                    cmd = [py, '-I', DRIVER_NAME]
                    data = ''
                else:
                    cmd = [py, '-I', SOL_NAME]
                    data = g_out

                status, s_out, s_err, wall = _run_isolated(cmd, tmp, env, data, timeout)
                internal = None
                if mode == 'method' and status == 'OK':
                    for line in s_out.splitlines():
                        if line.startswith('__INTERNAL_ELAPSED__'):
                            try:
                                internal = float(line.split()[1])
                            except (IndexError, ValueError):
                                pass
                if status == 'TIMEOUT':
                    timed_out = True
                    out.append(f"{n:>10} | TIMEOUT  | >{timeout:>8.3f} | {'-':>10} | {'-':>6}")
                    prev = None
                    continue
                if status == 'CRASH':
                    out.append(f"{n:>10} | CRASH    | {wall:>9.3f} | {'-':>10} | {'-':>6}")
                    out.append(f"    stderr: {_clip(s_err.strip())}")
                    prev = None
                    continue
                timing = internal if internal is not None else wall
                slope = _slope(prev[0], prev[1], n, timing) if prev else None
                slope_s = f"{slope:6.2f}" if slope is not None else f"{'-':>6}"
                internal_s = f"{internal:10.4f}" if internal is not None else f"{'-':>10}"
                out.append(f"{n:>10} | OK       | {wall:9.4f} | {internal_s} | {slope_s}")
                prev = (n, timing)

    return "\n".join(out)

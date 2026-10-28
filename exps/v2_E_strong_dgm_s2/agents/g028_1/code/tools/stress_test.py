import os
import subprocess
import sys
import tempfile
import json

# Driver executed in a subprocess. It loads the solution, the brute force and the
# generator, runs exhaustive enumeration (if the generator provides enumerate_all)
# and then random cases with growing sizes, and writes a JSON result to result_path.
_DRIVER = r'''
import sys, json, random, signal, importlib.util, os, io, copy, traceback, itertools, contextlib, inspect

sol_path, brute_path, gen_path, num_cases, per_call, method, result_path, checker_path, stdin_mode, max_size = sys.argv[1:11]
num_cases = int(num_cases)
per_call = float(per_call)
stdin_mode = stdin_mode == "1"
MAX_SIZE = max(1, int(max_size))
ENUM_CAP = 20000
SHRINK_BUDGET = 400
REPR_CAP = 2000

def finish(d):
    with open(result_path, "w") as f:
        json.dump(d, f)
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)  # not catchable by the surrounding except BaseException blocks

def clip(s):
    s = str(s)
    return s if len(s) <= REPR_CAP else s[:REPR_CAP] + "...<clipped>"

def load(path, name):
    d = os.path.dirname(os.path.abspath(path))
    if d not in sys.path:
        sys.path.insert(0, d)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

try:
    # In stdin_mode the solution/brute scripts are executed per case, not imported here.
    sol_mod = None if stdin_mode else load(sol_path, "_stress_solution")
    brute_mod = None if stdin_mode else load(brute_path, "_stress_brute")
    gen_mod = load(gen_path, "_stress_gen")
except BaseException:
    finish({"status": "error", "message": "Failed to import a file:\n" + traceback.format_exc(limit=5)})

if not hasattr(gen_mod, "gen"):
    finish({"status": "error", "message": "generator file must define gen(rng, size)"})

checker_fn = None
if checker_path:
    try:
        chk_mod = load(checker_path, "_stress_checker")
    except BaseException:
        finish({"status": "error", "message": "Failed to import checker file:\n" + traceback.format_exc(limit=5)})
    if not hasattr(chk_mod, "check"):
        finish({"status": "error", "message": "checker file must define check(input_obj, actual_output, expected_output)"})
    checker_fn = chk_mod.check

# Generator accepts a third positional parameter -> pass regime index.
try:
    _gen_params = list(inspect.signature(gen_mod.gen).parameters.values())
    GEN_TAKES_REGIME = len([p for p in _gen_params if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]) >= 3 \
        or any(p.kind == p.VAR_POSITIONAL for p in _gen_params)
except (TypeError, ValueError):
    GEN_TAKES_REGIME = False

def make_stdin_fn(path, which):
    with open(path, "r", errors="replace") as f:
        src_text = f.read()
    code = compile(src_text, path, "exec")
    def run(x):
        old_in, old_out = sys.stdin, sys.stdout
        out = io.StringIO()
        sys.stdin = io.StringIO(x)
        sys.stdout = out
        try:
            g = {"__name__": "__main__", "__builtins__": __builtins__}
            exec(code, g)
        except SystemExit as e:
            if e.code not in (None, 0):
                raise RuntimeError(f"{which} script called sys.exit({e.code!r})")
        finally:
            sys.stdin, sys.stdout = old_in, old_out
        return out.getvalue()
    return run

def make_fn(mod, which):
    if stdin_mode:
        return make_stdin_fn(sol_path if which == "solution" else brute_path, which)
    if method:
        if not hasattr(mod, "Solution"):
            raise AttributeError(f"{which} file has no class Solution (method={method!r})")
        inst = mod.Solution()
        m = getattr(inst, method)
        return lambda x: m(*x)
    if not hasattr(mod, "solve"):
        raise AttributeError(f"{which} file must define solve(input_obj)")
    return mod.solve

try:
    sol_fn = make_fn(sol_mod, "solution")
    brute_fn = make_fn(brute_mod, "brute")
except BaseException:
    finish({"status": "error", "message": "Setup failed:\n" + traceback.format_exc(limit=5)})

class _Timeout(BaseException):
    pass

def _on_alarm(signum, frame):
    raise _Timeout()

signal.signal(signal.SIGALRM, _on_alarm)

def call(fn, x):
    """Returns (status, value); status in ok|timeout|exc. Input is deep-copied so mutation is harmless."""
    buf = io.StringIO()
    signal.setitimer(signal.ITIMER_REAL, per_call)
    try:
        with contextlib.redirect_stdout(buf):
            v = fn(copy.deepcopy(x))
        return ("ok", v)
    except _Timeout:
        return ("timeout", None)
    except Exception:
        return ("exc", traceback.format_exc(limit=4))
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)

def same(a, b):
    if isinstance(a, str) and isinstance(b, str):
        return a.strip() == b.strip()
    try:
        return a == b
    except Exception:
        return False

def check(x):
    """Returns None if solution is acceptable, else (kind, expected, actual_text, note).
    Without a checker, the output must equal the brute output. With a checker, the brute output
    is only a reference; check(x, actual, expected) must return True."""
    bs, bv = call(brute_fn, x)
    if bs != "ok":
        return ("brute_" + bs, None, bv or "brute force failed", "")
    ss, sv = call(sol_fn, x)
    if ss == "timeout":
        return ("solution_timeout", bv, f"timed out after {per_call} seconds", "")
    if ss == "exc":
        return ("solution_exception", bv, sv, "")
    if checker_fn is None:
        if not same(sv, bv):
            return ("mismatch", bv, sv, "")
        return None
    try:
        res = checker_fn(copy.deepcopy(x), sv, bv)
    except BaseException:
        return ("checker_exception", bv, sv, traceback.format_exc(limit=4))
    if res is not True:
        return ("mismatch", bv, sv, str(res) if res is not None and res is not False else "checker returned False")
    return None

def candidates(x, top_tuple=False):
    """Yield strictly smaller variants of x (lazily)."""
    if isinstance(x, bool):
        return
    if isinstance(x, int):
        out = []
        if x != 0:
            out.append(0)
            if x > 0:
                out += [x // 2, x - 1]
            else:
                out += [-((-x) // 2), x + 1]
        for c in dict.fromkeys(out):
            if c != x:
                yield c
        return
    if isinstance(x, str):
        if stdin_mode:
            lines = x.split("\n")
            for i in range(len(lines)):
                yield "\n".join(lines[:i] + lines[i + 1:])
        for i in range(len(x)):
            yield x[:i] + x[i + 1:]
        return
    if isinstance(x, (list, tuple)):
        if not top_tuple:
            for i in range(len(x)):
                yield type(x)(list(x[:i]) + list(x[i + 1:]))
        for i in range(len(x)):
            for c in candidates(x[i]):
                lst = list(x)
                lst[i] = c
                yield type(x)(lst)
        return

def shrink(x, kind):
    cur = x
    budget = SHRINK_BUDGET
    changed = True
    while changed and budget > 0:
        changed = False
        for cand in candidates(cur, top_tuple=bool(method) and isinstance(cur, tuple)):
            budget -= 1
            if budget <= 0:
                break
            f = check(cand)
            if f is not None and f[0] == kind:
                cur = cand
                changed = True
                break
    return cur

def fail_result(x, f, count, phase):
    kind = f[0]
    shrunk = shrink(x, kind)
    f2 = check(shrunk)
    if f2 is None or f2[0] != kind:
        shrunk, f2 = x, f
    kind, expected, actual, note = f2
    if stdin_mode and isinstance(shrunk, str):
        shown_input = clip(shrunk)
    else:
        shown_input = clip(repr(shrunk))
    msg = (
        f"FAILED ({kind}) during {phase} after {count} cases.\n"
        f"Input (shrunk): {shown_input}\n"
        f"Expected: {clip(repr(expected))}\n"
        f"Actual: {clip(actual if isinstance(actual, str) and kind != 'mismatch' else repr(actual))}"
    )
    if note:
        msg += f"\nChecker note: {clip(note)}"
    return {"status": "fail", "cases": count, "message": msg}

count = 0
# Phase 1: exhaustive enumeration of tiny inputs, if provided.
if hasattr(gen_mod, "enumerate_all"):
    try:
        it = gen_mod.enumerate_all()
        for x in itertools.islice(iter(it), ENUM_CAP):
            count += 1
            f = check(x)
            if f is not None:
                finish(fail_result(x, f, count, "exhaustive enumeration"))
    except BaseException:
        finish({"status": "error", "message": "enumerate_all() failed:\n" + traceback.format_exc(limit=5), "cases": count})

# Phase 2: random cases with growing sizes.
# Schedule: first third of cases ramp over small sizes (1..min(10, MAX_SIZE)),
# the remaining cases ramp from 1 up to MAX_SIZE.
SMALL_CAP = min(10, MAX_SIZE)
n_small = num_cases // 3
n_big = num_cases - n_small

def size_for(i):
    if i < n_small:
        return 1 + (i * SMALL_CAP) // max(1, n_small - 1) if n_small > 1 else 1
    j = i - n_small
    return 1 + (j * MAX_SIZE) // max(1, n_big - 1) if n_big > 1 else MAX_SIZE

for i in range(num_cases):
    size = size_for(i)
    regime = i % 4
    rng = random.Random(i * 7919 + 12345)
    try:
        x = gen_mod.gen(rng, size, regime) if GEN_TAKES_REGIME else gen_mod.gen(rng, size)
    except BaseException:
        finish({"status": "error", "message": "gen(rng, size) failed:\n" + traceback.format_exc(limit=5), "cases": count})
    count += 1
    f = check(x)
    if f is not None:
        finish(fail_result(x, f, count, f"random case {i} (size {size}, regime {regime})"))

finish({"status": "pass", "cases": count,
        "message": f"All {count} cases passed (exhaustive enumeration: {'yes' if hasattr(gen_mod, 'enumerate_all') else 'not provided'}; random cases: {num_cases}; max_size: {MAX_SIZE}; checker: {'yes' if checker_fn else 'no'}; stdin_mode: {stdin_mode})."})
'''


def tool_info():
    return {
        "name": "stress_test",
        "description": """Stress-test a solution against a brute-force reference using a random input generator.\n
* The solution, brute-force, and generator are Python files. Solution and brute files each expose `solve(input_obj)` returning the output (or, if `method` is given, a class `Solution` whose method of that name is called with the elements of a tuple input).
* The generator file exposes `gen(rng, size)` returning an input object, where `rng` is a `random.Random` instance and `size` grows from 1 upward. Optionally it exposes `enumerate_all()` yielding all tiny inputs; these are run first, exhaustively.
* Generated inputs must include degenerate cases (minimum size, all equal, extreme values, etc.); do not filter them out in the generator.
* Output is compared as a whole (strings compared after stripping whitespace). On failure, the tool returns the shrunk failing input with the expected (brute) and actual (solution) outputs, or the exception/timeout. On success it returns the number of cases run.
* Each solve call is limited by `timeout` seconds; the whole run is limited to about 280 seconds, so reduce `num_cases` if needed.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "solution_path": {"type": "string", "description": "Path to the solution Python file (absolute or relative to the current directory)."},
                "brute_path": {"type": "string", "description": "Path to the brute-force reference Python file. Must be independent of the algorithm under test."},
                "generator_path": {"type": "string", "description": "Path to the generator Python file exposing gen(rng, size) and optionally enumerate_all()."},
                "num_cases": {"type": "integer", "description": "Number of random cases to run after enumeration (default 300)."},
                "timeout": {"type": "integer", "description": "Per-call timeout in seconds for each solve call (default 5)."},
                "method": {"type": "string", "description": "Optional. If given, solution and brute files define class Solution with this method name; generated inputs must be tuples of positional arguments."},
                "checker_path": {"type": "string", "description": "Optional. Python file defining check(input_obj, actual_output, expected_output) that returns True if actual_output is a valid answer for input_obj (expected_output is the brute-force output, usable as a reference for the optimum/existence), or an error string otherwise. Use it for problems that accept any valid answer; without it, outputs must match the brute force exactly (whitespace-stripped)."},
                "stdin_mode": {"type": "boolean", "description": "Optional. If true, solution and brute are stdin/stdout scripts (not solve() functions) and gen returns the input as a string. Each case runs in-process, so thousands of cases are fast."},
                "max_size": {"type": "integer", "description": "Optional. Largest size passed to gen(rng, size) (default 60, max 500). The first third of cases use small sizes, the rest ramp up to max_size. If gen accepts a third argument, it receives regime = i % 4 (0..3) to vary value range and duplicate density."}
            },
            "required": ["solution_path", "brute_path", "generator_path"]
        }
    }


def tool_function(solution_path, brute_path, generator_path, num_cases=300, timeout=5, method=None,
                  checker_path=None, stdin_mode=False, max_size=60):
    for label, p in (("solution_path", solution_path), ("brute_path", brute_path), ("generator_path", generator_path)):
        if not p or not os.path.isfile(os.path.abspath(p)):
            return f"Error: {label} does not exist: {p}"
    if checker_path and not os.path.isfile(os.path.abspath(checker_path)):
        return f"Error: checker_path does not exist: {checker_path}"
    try:
        num_cases = max(0, min(int(num_cases if num_cases is not None else 300), 100000))
        timeout = max(1, min(int(timeout if timeout is not None else 5), 60))
        max_size = max(1, min(int(max_size if max_size is not None else 60), 500))
    except (TypeError, ValueError):
        return "Error: num_cases, timeout and max_size must be integers."
    fd, result_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    try:
        cmd = [sys.executable, "-c", _DRIVER,
               os.path.abspath(solution_path), os.path.abspath(brute_path), os.path.abspath(generator_path),
               str(num_cases), str(timeout), method or "", result_path,
               os.path.abspath(checker_path) if checker_path else "",
               "1" if stdin_mode else "0", str(max_size)]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=280, stdin=subprocess.DEVNULL,
                               errors="replace")
        except subprocess.TimeoutExpired:
            return ("Error: stress test exceeded the 280 second overall limit. "
                    "Reduce num_cases, or make the solution/brute faster.")
        try:
            with open(result_path) as f:
                content = f.read()
        except OSError:
            content = ""
        if not content.strip():
            err = (p.stderr or "").strip()[-3000:]
            return "Error: stress test driver produced no result.\n" + (err or "(no stderr)")
        res = json.loads(content)
        msg = res.get("message", "")
        if res.get("status") == "pass":
            return f"PASS: {msg}"
        if res.get("status") == "fail":
            return msg
        return f"ERROR: {msg}"
    finally:
        try:
            os.remove(result_path)
        except OSError:
            pass

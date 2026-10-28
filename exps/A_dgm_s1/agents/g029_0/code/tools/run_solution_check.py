import json
import subprocess
import sys

# Runs a single call of a solution in a FRESH python process, mimicking how a grader
# imports and invokes the solution. Returns full stdout, stderr and any traceback.

_RUNNER = r'''
import importlib.util, json, sys, traceback
module_path, class_name, method_name, args_json = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
try:
    spec = importlib.util.spec_from_file_location("solution_under_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    args = json.loads(args_json)
    if class_name:
        obj = getattr(module, class_name)()
        func = getattr(obj, method_name)
    else:
        func = getattr(module, method_name)
    result = func(*args)
    print("RESULT: " + json.dumps(result, default=repr))
except SystemExit:
    raise
except BaseException:
    sys.stdout.flush()
    print("TRACEBACK:\n" + traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
'''


def tool_info():
    return {
        "name": "run_solution_check",
        "description": """Run a solution function/method in a fresh Python subprocess, the way a grader would, and return its result.\n
* Imports the module from module_path (by file path), instantiates class_name (if given), and calls method_name with the JSON list args_json.\n
* Returns the RESULT (JSON-encoded return value), the full stdout, the full stderr, and any traceback.\n
* Use this to reproduce grader-style invocations of the final solution file and check its behavior in a clean interpreter.\n
* Leave class_name empty to call a module-level function (e.g. for complete stdin/stdout programs, use bash with a pipe instead).""",
        "input_schema": {
            "type": "object",
            "properties": {
                "module_path": {
                    "type": "string",
                    "description": "Absolute path to the Python file containing the solution."
                },
                "class_name": {
                    "type": "string",
                    "description": "Name of the class to instantiate (e.g. 'Solution'). Empty string to call a module-level function."
                },
                "method_name": {
                    "type": "string",
                    "description": "Name of the method or function to call."
                },
                "args_json": {
                    "type": "string",
                    "description": "JSON-encoded list of positional arguments, e.g. '[[1, 2, 3], 5]'."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds for the subprocess (default 20)."
                }
            },
            "required": ["module_path", "class_name", "method_name", "args_json"]
        }
    }


def tool_function(module_path, class_name, method_name, args_json, timeout=20):
    try:
        json.loads(args_json)
    except Exception as e:
        return f"Error: args_json is not valid JSON: {e}"
    try:
        timeout = int(timeout) if timeout else 20
    except Exception:
        timeout = 20
    try:
        proc = subprocess.run(
            [sys.executable, "-c", _RUNNER, module_path, class_name or "", method_name, args_json],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = e.stderr.decode(errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        return f"Timed out after {timeout} seconds.\nSTDOUT:\n{out}\nSTDERR:\n{err}"

    parts = []
    result_lines = [l for l in proc.stdout.splitlines() if l.startswith("RESULT: ")]
    if result_lines:
        parts.append(result_lines[-1])
    other_stdout = "\n".join(l for l in proc.stdout.splitlines() if not l.startswith("RESULT: ")).strip()
    parts.append(f"STDOUT:\n{other_stdout}" if other_stdout else "STDOUT: (empty)")
    stderr = proc.stderr.strip()
    parts.append(f"STDERR:\n{stderr}" if stderr else "STDERR: (empty)")
    parts.append(f"Exit code: {proc.returncode}")
    return "\n".join(parts)

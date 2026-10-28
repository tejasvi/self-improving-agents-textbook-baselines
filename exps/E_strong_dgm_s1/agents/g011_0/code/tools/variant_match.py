import os
import shutil
import subprocess
import sys
import tempfile

MAX_CASES = 200
MAX_VARIANTS = 30
MAX_TIMEOUT = 60
CLIP = 1500


def tool_info():
    return {
        "name": "variant_match",
        "description": """Compare several candidate solution variants (for a multi-answer problem) on the sample cases.

* Input: `variant_paths` (array of Python solution files, e.g. variants/v1.py, variants/v2.py, ...) and `cases`, a list of objects with `input` (stdin text) and `expected_output` (sample output copied from the statement).
* For every variant and every sample it runs `python3 variant` on the input and records whether the stdout matches expected_output exactly (whitespace-normalized: line breaks/spaces ignored). It reports `EXACT MATCH: k/n` per variant.
* If `checker_path` is given, every variant output is also checked by the checker run as `checker input_file output_file` (exit code 0 = valid answer, anything else = invalid; the checker's raw stdout/stderr is reported). Validity is reported per variant and per sample.
* Returns the raw per-variant results and a ranking: variants sorted by (number of valid outputs, number of exact sample matches), best first. Use the ranking together with the structural naturalness of each construction to pick the final variant; do NOT pick a variant only because it fits the samples with arbitrary constants.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "variant_paths": {
                    "type": "array",
                    "description": "List of paths to candidate solution files (each reads stdin and writes stdout).",
                    "items": {
                        "type": "string",
                        "description": "Path to one candidate solution file."
                    }
                },
                "cases": {
                    "type": "array",
                    "description": "List of sample cases. Each case is an object with the stdin text and the expected stdout copied from the problem statement.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "input": {
                                "type": "string",
                                "description": "Exact stdin text for this sample."
                            },
                            "expected_output": {
                                "type": "string",
                                "description": "Exact expected stdout text for this sample, copied from the problem statement."
                            }
                        },
                        "required": ["input", "expected_output"]
                    }
                },
                "checker_path": {
                    "type": "string",
                    "description": "Optional path to a checker program run as `checker input_file output_file` (exit code 0 = valid answer). If omitted, only exact sample matches are reported."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Per-run time limit in seconds for each variant and the checker (default 10)."
                }
            },
            "required": ["variant_paths", "cases"]
        }
    }


def _clip(s, n=CLIP):
    s = s or ""
    if len(s) <= n:
        return s
    return s[:n] + f"...<{len(s) - n} more chars>"


def _normalize(s):
    return " ".join((s or "").split())


def _cmd(path):
    if path.endswith(".py"):
        return [sys.executable, path]
    return [os.path.abspath(path)]


def _run(cmd, data, timeout):
    try:
        p = subprocess.run(cmd, input=data, capture_output=True, timeout=timeout)
        return {
            "timeout": False,
            "rc": p.returncode,
            "stdout": p.stdout.decode("utf-8", errors="replace"),
            "stderr": p.stderr.decode("utf-8", errors="replace"),
        }
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = e.stderr.decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        return {"timeout": True, "rc": None, "stdout": out, "stderr": err}


def tool_function(variant_paths, cases, checker_path=None, timeout=10):
    try:
        timeout = int(timeout) if timeout is not None else 10
    except (TypeError, ValueError):
        timeout = 10
    timeout = max(1, min(timeout, MAX_TIMEOUT))

    if not isinstance(variant_paths, list) or not variant_paths:
        return "Error: `variant_paths` must be a non-empty array of file paths."
    if len(variant_paths) > MAX_VARIANTS:
        return f"Error: too many variants ({len(variant_paths)}); the maximum is {MAX_VARIANTS}."
    if not isinstance(cases, list) or not cases:
        return "Error: `cases` must be a non-empty array of objects with `input` and `expected_output`."
    if len(cases) > MAX_CASES:
        return f"Error: too many cases ({len(cases)}); the maximum is {MAX_CASES}."
    for c in cases:
        if not isinstance(c, dict) or "input" not in c or "expected_output" not in c:
            return "Error: every case must be an object with `input` and `expected_output`."
    for p in variant_paths:
        if not isinstance(p, str) or not os.path.isfile(p):
            return f"Error: variant file not found: {p}"
    if checker_path is not None and not os.path.isfile(checker_path):
        return f"Error: checker file not found: {checker_path}"

    tmpdir = tempfile.mkdtemp(prefix="variant_match_")
    in_file = os.path.join(tmpdir, "input.txt")
    out_file = os.path.join(tmpdir, "output.txt")
    try:
        results = []
        for vpath in variant_paths:
            cmd = _cmd(vpath)
            matched = 0
            valid = 0
            details = []
            for i, c in enumerate(cases):
                inp = str(c["input"])
                exp = str(c["expected_output"])
                r = _run(cmd, inp.encode("utf-8"), timeout)
                if r["timeout"]:
                    status = f"TIMEOUT after {timeout}s"
                    exact = False
                elif r["rc"] != 0:
                    status = f"RUNTIME ERROR exit={r['rc']}"
                    exact = False
                else:
                    exact = _normalize(r["stdout"]) == _normalize(exp)
                    status = "MATCH" if exact else "MISMATCH"
                if exact:
                    matched += 1

                ok_text = "n/a (no checker)"
                if checker_path is not None:
                    if not r["timeout"] and r["rc"] == 0:
                        with open(in_file, "w", encoding="utf-8") as f:
                            f.write(inp)
                        with open(out_file, "w", encoding="utf-8") as f:
                            f.write(r["stdout"])
                        chk = _run(_cmd(checker_path) + [in_file, out_file], b"", timeout)
                        if not chk["timeout"] and chk["rc"] == 0:
                            valid += 1
                            ok_text = "VALID"
                        else:
                            st = f"TIMEOUT after {timeout}s" if chk["timeout"] else f"exit={chk['rc']}"
                            ok_text = (f"INVALID (checker {st}; checker stdout={_clip(chk['stdout'], 400)!r}; "
                                       f"checker stderr={_clip(chk['stderr'], 400)!r})")
                    else:
                        ok_text = "INVALID (no output)"

                if not exact or (checker_path is not None and not ok_text.startswith("VALID")):
                    details.append(
                        f"  case {i + 1}: {status}; validity: {ok_text}\n"
                        f"    input: {_clip(inp, 300)!r}\n"
                        f"    expected: {_clip(exp, 300)!r}\n"
                        f"    actual: {_clip(r['stdout'], 300)!r}"
                        + (f"\n    stderr: {_clip(r['stderr'], 300)!r}" if r["stderr"] and not exact else "")
                    )
                else:
                    details.append(f"  case {i + 1}: {status}; validity: {ok_text}")
            results.append({
                "path": vpath,
                "matched": matched,
                "valid": valid if checker_path is not None else None,
                "details": details,
            })

        n = len(cases)
        ranked = sorted(
            results,
            key=lambda r: (-(r["valid"] if r["valid"] is not None else 0), -r["matched"]),
        )

        lines = []
        for r in results:
            lines.append(f"=== {r['path']} ===")
            lines.append(f"EXACT MATCH: {r['matched']}/{n}")
            if checker_path is not None:
                lines.append(f"VALID: {r['valid']}/{n}")
            lines.extend(r["details"])
            lines.append("")
        lines.append("RANKING (best first):")
        for i, r in enumerate(ranked):
            v = f", valid {r['valid']}/{n}" if checker_path is not None else ""
            lines.append(f"{i + 1}. {r['path']}: exact {r['matched']}/{n}{v}")
        return "\n".join(lines)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

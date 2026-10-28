import argparse
import ast
import subprocess
import tempfile
import logging
from logging.handlers import RotatingFileHandler
import os
import threading
import json
import re
import time

from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent, simple_chat
from utils.git_utils import diff_versus_commit, reset_to_commit, apply_patch

# reset_to_commit(git_dname, commit)
# apply_patch(git_dname, patch_str)

# TEST COMMANDS for different languages
# IMPORTANT: TEST COMMAND SHOULD BE RUN UNDER git_tempdir!!
NPM_TEST_COMMANDS = [
    ["sh", "-c", "set -e"],
    ["sh", "-c", "[ ! -e node_modules ] && ln -s /npm-install/node_modules ."],
    ["sh", "-c", "[ ! -e package-lock.json ] && ln -s /npm-install/package-lock.json ."],
    ["sed", "-i", "s/\\bxtest(/test(/g", "*.spec.js"],
    ["npm", "run", "test"]
]

CPP_TEST_COMMANDS = [
    ["sh", "-c", "set -e"],
    ["sh", "-c", "[ ! -d \"build\" ] && mkdir build"],
    ["sh", "-c", "cd build"],
    ["cmake", "-DEXERCISM_RUN_ALL_TESTS=1", "-G", "Unix Makefiles", ".."],
    ["make"],
    ["sh", "-c", "cd ../"]
]

TEST_COMMANDS = {
    "python": [["pytest", "-rA", "--tb=long"]],
    "rust": [["cargo", "test", "--", "--include-ignored"]],
    "go": [["go", "test", "./..."]],
    "javascript": NPM_TEST_COMMANDS,
    "cpp": CPP_TEST_COMMANDS,
    "java": [["./gradlew", "test"]],
}

# Harness executed in a subprocess for Solution-class tasks.
# argv: solution_path, method_name, args_file (a Python literal list of arguments)
HARNESS_SOURCE = """import ast
import importlib.util
import sys
import threading
import traceback

_state = {"error": None}

def _main():
    try:
        sol_path, method, args_path = sys.argv[1], sys.argv[2], sys.argv[3]
        spec = importlib.util.spec_from_file_location("solution_under_test", sol_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with open(args_path) as f:
            args = ast.literal_eval(f.read())
        result = getattr(mod.Solution(), method)(*args)
        print(repr(result))
    except BaseException:
        _state["error"] = traceback.format_exc()

if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    threading.stack_size(256 * 1024 * 1024)
    t = threading.Thread(target=_main)
    t.start()
    t.join()
    sys.stdout.flush()
    if _state["error"] is not None:
        sys.stderr.write(_state["error"])
        sys.exit(1)
"""

# Thread-local storage for logger instances
thread_local = threading.local()

def get_thread_logger():
    """
    Get the logger instance specific to the current thread.
    Returns None if no logger has been set for this thread.
    """
    return getattr(thread_local, 'logger', None)

def set_thread_logger(logger):
    """
    Set the logger instance for the current thread.
    """
    thread_local.logger = logger

def setup_logger(log_file='./chat_history.md', level=logging.INFO):
    """
    Set up a logger with both file and console handlers.
    """
    # Create logger with a unique name based on thread ID
    logger = logging.getLogger(f'AgenticSystem-{threading.get_ident()}')
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # Create formatters
    file_formatter = logging.Formatter('%(message)s')
    
    # Create and set up file handler
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    
    # Store logger in thread-local storage
    set_thread_logger(logger)
    
    return logger

def safe_log(message, level=logging.INFO):
    """
    Thread-safe logging function that ensures messages go to the correct logger.
    """
    logger = get_thread_logger()
    if logger:
        logger.log(level, message)
    else:
        print(f"Warning: No logger found for thread {threading.get_ident()}")

def _is_test_file(path):
    """
    Return True if `path` looks like a test file (test directories, test_*.py,
    *_test.*, *.spec.*, *.test.*, conftest.py).
    """
    norm = path.replace('\\', '/').strip()
    parts = [p for p in norm.split('/') if p]
    if not parts:
        return False
    basename = parts[-1]
    dirs = parts[:-1]
    test_dirs = {'test', 'tests', 'spec', 'specs', '__tests__'}
    if any(d.lower() in test_dirs for d in dirs):
        return True
    lower = basename.lower()
    if lower == 'conftest.py':
        return True
    if lower.startswith('test_') or lower.startswith('test.'):
        return True
    if '_test.' in lower or '.spec.' in lower or '.test.' in lower:
        return True
    return False

class AgenticSystem:
    def __init__(
            self,
            problem_statement,
            git_tempdir,
            base_commit,
            chat_history_file='./chat_history.md',
            test_description=None,
            self_improve=False,
            language='python'
        ):
        self.problem_statement = problem_statement
        self.git_tempdir = git_tempdir
        self.base_commit = base_commit
        self.chat_history_file = chat_history_file
        self.test_description = test_description
        self.self_improve = self_improve
        self.language = language

        # Set the code model based on whether self-improvement is enabled
        self.code_model = CLAUDE_MODEL if not self_improve else OPENAI_MODEL

        # Initialize logger and store it in thread-local storage
        self.logger = setup_logger(chat_history_file)
        
        # Clear the log file
        with open(chat_history_file, 'w') as f:
            f.write('')

    def get_current_edits(self):
        diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        new_msg_history = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"# Current Repo Edits\n{diff}",
                    }
                ],
            }
        ]
        return new_msg_history

    def _changed_files(self):
        """
        Return the list of modified, added, or untracked file paths in git_tempdir.
        """
        result = subprocess.run(
            ["git", "-C", self.git_tempdir, "status", "--porcelain", "--untracked-files=all"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        files = []
        for line in result.stdout.decode(errors='replace').splitlines():
            if len(line) < 4:
                continue
            path = line[3:]
            if ' -> ' in path:  # rename: keep the new path
                path = path.split(' -> ', 1)[1]
            path = path.strip()
            if len(path) >= 2 and path[0] == '"' and path[-1] == '"':
                path = path[1:-1]
            files.append(path)
        return files

    def _has_source_patch(self):
        """
        True if at least one changed file is not a test file.
        """
        return any(not _is_test_file(f) for f in self._changed_files())

    @staticmethod
    def _parse_sample_json(text):
        """
        Parse a JSON array out of an LLM response. Tolerates fenced code blocks, literal newlines
        inside strings (strict=False), and Python-style literals (True/None) as a fallback.
        Returns the parsed list, or None on failure.
        """
        candidates = []
        fence = re.search(r"```(?:json|python)?\s*\n(.*?)```", text, re.DOTALL)
        if fence:
            candidates.append(fence.group(1))
        start, end = text.find("["), text.rfind("]")
        if start != -1 and end > start:
            candidates.append(text[start:end + 1])
        for cand in candidates:
            cand = cand.strip()
            try:
                data = json.loads(cand, strict=False)
                if isinstance(data, list):
                    return data
            except Exception:
                pass
            try:
                data = ast.literal_eval(cand)
                if isinstance(data, list):
                    return data
            except Exception:
                pass
        return None

    def _extract_samples(self):
        """
        Ask the LLM to extract the sample tests from the problem statement.
        Returns a list of {"input": str, "output": str, "args": list[str]} dicts (empty list on failure).
        - "input": exact stdin text (for stdin-style programs; may be "" for Solution-class tasks)
        - "output": exact expected output (for Solution-class tasks, a Python literal of the return value)
        - "args": for Solution-class tasks, one Python-literal expression per method parameter, in order
        """
        prompt = f"""Extract the sample test cases from the problem statement below.

Return ONLY a JSON array (no prose) of objects with these keys:
[{{"input": "<exact stdin text, or \\"\\" if the task is a function/method>",
   "output": "<exact expected output text; for a function/method task, the expected return value written as a Python literal>",
   "args": ["<python literal for argument 1>", "<python literal for argument 2>", "..."]}}, ...]

Rules:
- Copy the sample inputs and outputs exactly, preserving line breaks.
- "args" is only used for function/method tasks (e.g. a `Solution` class with a method). For stdin-style tasks use [].
- For function/method tasks, each entry of "args" must be a valid Python literal (e.g. "[1, 2, 3]", "\\"abc\\"", "True") for one parameter of the method, in order.
- If there are no samples, return [].

<problem_statement>
{self.problem_statement}
</problem_statement>
"""
        data = None
        for attempt in range(3):  # bounded retries: API errors return "" and parse failures are possible
            text = simple_chat(prompt, model=self.code_model, max_tokens=8192, logging=safe_log) or ""
            data = self._parse_sample_json(text)
            if data is not None:
                break
            safe_log(f"[samples] attempt {attempt}: could not parse extraction response. head:\n{text[:500]}")
        if data is None:
            return []
        samples = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "input" in item and "output" in item:
                    raw_args = item.get("args", [])
                    if not isinstance(raw_args, list):
                        raw_args = []
                    samples.append({
                        "input": str(item["input"]),
                        "output": str(item["output"]),
                        "args": [str(a) for a in raw_args],
                    })
        return samples

    def _detect_mode(self, solution_path):
        """
        Inspect the solution file with ast. If it defines `class Solution` with a public method,
        return ("class", method_name). Otherwise return ("stdin", None).
        """
        if not solution_path or not os.path.exists(solution_path):
            return "stdin", None
        try:
            with open(solution_path, "r", encoding="utf-8", errors="replace") as f:
                tree = ast.parse(f.read())
        except Exception:
            return "stdin", None
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == "Solution":
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("_"):
                        return "class", item.name
        return "stdin", None

    def _get_harness_dir(self):
        """
        Directory outside the repo (in /tmp) holding the generated harness and argument files.
        """
        if not getattr(self, "_harness_dir", None):
            self._harness_dir = tempfile.mkdtemp(prefix="agent_harness_")
            with open(os.path.join(self._harness_dir, "harness.py"), "w") as f:
                f.write(HARNESS_SOURCE)
        return self._harness_dir

    def _run_candidate(self, solution_path, mode, method, payload, timeout, tag="run"):
        """
        Run the solution once.
        - stdin mode: payload is the stdin text; runs `python3 solution.py`.
        - class mode: payload is a Python-literal list text of method args; runs the harness.
        Returns dict with keys: returncode, stdout, stderr, elapsed, timed_out.
        """
        start = time.time()
        if mode == "class":
            hdir = self._get_harness_dir()
            args_path = os.path.join(hdir, f"{tag}_args.txt")
            with open(args_path, "w") as f:
                f.write(payload)
            cmd = ["python3", os.path.join(hdir, "harness.py"), solution_path, method, args_path]
            stdin_text = None
        else:
            cmd = ["python3", solution_path]
            stdin_text = payload
        try:
            proc = subprocess.run(
                cmd, input=stdin_text, capture_output=True, text=True,
                timeout=timeout, cwd=self.git_tempdir,
            )
            return {
                "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr,
                "elapsed": time.time() - start, "timed_out": False,
            }
        except subprocess.TimeoutExpired as e:
            def _txt(x):
                if x is None:
                    return ""
                return x.decode(errors="replace") if isinstance(x, bytes) else x
            return {
                "returncode": None, "stdout": _txt(e.stdout), "stderr": _txt(e.stderr),
                "elapsed": time.time() - start, "timed_out": True,
            }

    @staticmethod
    def _outputs_match(actual, expected):
        """
        Compare outputs. Tries Python-literal equality first (class mode returns repr), then whitespace tokens.
        """
        try:
            if ast.literal_eval(actual.strip()) == ast.literal_eval(expected.strip()):
                return True
        except Exception:
            pass
        return actual.split() == expected.split()

    def _run_samples(self, solution_path, samples):
        """
        Run the solution on each sample (stdin-style or Solution-class harness).
        Returns (report, all_passed). The report is raw plain text.
        """
        if not samples:
            return "No samples were extracted from the problem statement; verify manually with your own tests.", False
        if not solution_path or not os.path.exists(solution_path):
            return f"Solution file not found: {solution_path}", False

        mode, method = self._detect_mode(solution_path)
        blocks = []
        all_passed = True
        for i, sample in enumerate(samples):
            if mode == "class":
                payload = "[" + ", ".join(sample.get("args", [])) + "]"
                if not sample.get("args") and not sample["input"].strip():
                    payload = "[]"
            else:
                payload = sample["input"]
                if payload and not payload.endswith("\n"):
                    payload += "\n"
            res = self._run_candidate(solution_path, mode, method, payload, timeout=10, tag=f"sample{i}")
            if res["timed_out"]:
                actual, stderr = "", "TIMEOUT: exceeded 10 seconds"
                status_note = "timeout"
                passed = False
            else:
                actual, stderr = res["stdout"], res["stderr"]
                status_note = f"exit code {res['returncode']}"
                if mode == "class":
                    passed = res["returncode"] == 0 and self._outputs_match(actual, sample["output"])
                else:
                    passed = res["returncode"] == 0 and actual.split() == sample["output"].split()
            if not passed:
                all_passed = False
            shown_input = sample["input"] if mode == "stdin" else f"args: {payload}"
            blocks.append(
                f"=== Sample {i + 1} ({'PASS' if passed else 'FAIL'}, {status_note}, time {res['elapsed']:.3f}s) ===\n"
                f"--- input ---\n{shown_input}\n"
                f"--- expected output ---\n{sample['output']}\n"
                f"--- actual output ---\n{actual}\n"
                f"--- stderr ---\n{stderr}\n"
            )
        summary = "ALL SAMPLES PASSED" if all_passed else "SOME SAMPLES FAILED"
        return f"{summary}\n\n" + "\n".join(blocks), all_passed

    def _generate_stress_inputs(self, solution_path):
        """
        Ask the LLM for a generator script defining gen_cases(), which returns a list of (name, args)
        with max-constraint adversarial inputs. Runs it in a subprocess with a timeout.
        args is a list of Python values (one per method parameter) for class mode, or a stdin string otherwise.
        Returns (mode, method, cases) where cases is a list of (name, payload_text) pairs ready for _run_candidate.
        """
        mode, method = self._detect_mode(solution_path)
        if mode == "class":
            shape = ("args must be a list with one Python value per parameter of the method, "
                     "in order (lists, ints, strings, etc.)")
        else:
            shape = "args must be a single string: the exact stdin text of the program"
        prompt = f"""Write a Python script that generates adversarial, MAX-SIZE test inputs for the problem below.

<problem_statement>
{self.problem_statement}
</problem_statement>

Requirements:
- Define a function `gen_cases()` that returns a Python list of tuples `(name, args)`.
- `name` is a short descriptive string. {shape}.
- Derive sizes from the stated constraints: use the maximum allowed sizes (or as close as the constraints allow), and respect every constraint (value ranges, string alphabets, guaranteed properties).
- Cover different structures, for example: all identical elements, random values, sorted ascending/descending, few distinct values, alternating patterns, worst-case shapes for typical algorithms. Include at least 5 cases and at most 12.
- Use `random.seed(12345)` for reproducibility. Do not read files or the network.
- Do NOT print anything. Do not call gen_cases() at module level; just define it (plus any helpers and imports).

Return ONLY the Python code in a single ```python code block.
"""
        cases = []
        for attempt in range(2):  # bounded retries: LLM output or generator script may be broken
            cases = self._run_generator_once(prompt, mode, method)
            if cases:
                break
            safe_log(f"[perf] generator attempt {attempt} produced no usable cases.")
        safe_log(f"[perf] generated {len(cases)} stress case(s).")
        return mode, method, cases

    def _run_generator_once(self, prompt, mode, method):
        """
        One LLM call + subprocess execution of the generated gen_cases(). Returns a list of (name, payload).
        """
        text = simple_chat(prompt, model=self.code_model, max_tokens=8192, logging=safe_log) or ""
        m = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
        code = m.group(1) if m else text
        driver = (
            code
            + "\n\n_cases = gen_cases()\n"
            + "print('__CASES__' + repr(list(_cases)))\n"
        )
        gen_dir = self._get_harness_dir()
        gen_path = os.path.join(gen_dir, "gen_cases.py")
        with open(gen_path, "w") as f:
            f.write(driver)
        try:
            proc = subprocess.run(
                ["python3", gen_path], capture_output=True, text=True, timeout=30, cwd=gen_dir,
            )
        except subprocess.TimeoutExpired:
            safe_log("[perf] generator timed out.")
            return []
        line = next((ln for ln in proc.stdout.splitlines() if ln.startswith("__CASES__")), None)
        if line is None:
            safe_log(f"[perf] generator produced no cases. stderr:\n{proc.stderr[-2000:]}")
            return []
        try:
            raw_cases = ast.literal_eval(line[len("__CASES__"):])
        except Exception as e:
            safe_log(f"[perf] could not parse generator output: {e}")
            return []

        cases = []
        for idx, item in enumerate(raw_cases[:12]):
            if not (isinstance(item, (list, tuple)) and len(item) == 2):
                continue
            name, args = str(item[0]), item[1]
            if mode == "class":
                if not isinstance(args, (list, tuple)):
                    continue
                payload = repr(list(args))
            else:
                if not isinstance(args, str):
                    continue
                payload = args if args.endswith("\n") else args + "\n"
            cases.append((name, payload))
        return cases

    def _run_perf(self, solution_path, cases, mode=None, method=None, timeout=3.0, slow_threshold=1.5):
        """
        Run the solution on each (name, payload) case with a strict timeout.
        Returns (report, needs_repair). The report is raw text with elapsed time, output and stderr per case.
        """
        if mode is None:
            mode, method = self._detect_mode(solution_path)
        needs_repair = False
        blocks = []
        for i, (name, payload) in enumerate(cases):
            res = self._run_candidate(solution_path, mode, method, payload, timeout=timeout, tag=f"perf{i}")
            if res["timed_out"]:
                status = f"TIMEOUT (exceeded {timeout:g}s)"
                needs_repair = True
            elif res["returncode"] != 0:
                status = f"CRASH (exit code {res['returncode']})"
                needs_repair = True
            elif res["elapsed"] > slow_threshold:
                status = f"SLOW (exceeded {slow_threshold:g}s)"
                needs_repair = True
            else:
                status = "OK"
            out = res["stdout"]
            if len(out) > 300:
                out = out[:300] + f"... [truncated, {len(res['stdout'])} chars total]"
            err = res["stderr"]
            if len(err) > 2000:
                err = err[-2000:] + "\n... [stderr truncated to last 2000 chars]"
            blocks.append(
                f"=== Case {i + 1}: {name} ({status}, time {res['elapsed']:.3f}s) ===\n"
                f"--- output (truncated) ---\n{out}\n"
                f"--- stderr ---\n{err}\n"
            )
        return "\n".join(blocks), needs_repair

    def _solution_path(self):
        """
        Pick the solution file: a changed non-test file (prefer solution.py), else None.
        """
        candidates = [f for f in self._changed_files() if not _is_test_file(f)]
        if not candidates:
            return None
        for f in candidates:
            if os.path.basename(f) == "solution.py":
                return os.path.join(self.git_tempdir, f)
        return os.path.join(self.git_tempdir, candidates[0])

    def forward(self):
        """
        The forward function for the AgenticSystem.
        """
        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        instruction = f"""{task}

Follow this step-by-step workflow:
1) Inspect the repository: use bash (e.g. `ls -la`, `cat`) and the editor tool to view existing files, and determine which file the solution must be written to (use the file named in the problem statement; if none is named, use the existing solution/entry file in the repo).
2) Reason about the algorithm and the complexity needed for the input constraints before writing code. State the time complexity in terms of the constraints before coding and confirm it fits in Python within ~2 seconds.
3) Write the implementation to the required file using the editor tool's `create` or `edit` command. The file MUST be written to disk.
4) Run the program on every sample input in the problem statement with bash and compare its output with the expected output. Fix any mismatch and re-run until all samples pass.
5) For tricky or hard problems, also write a brute-force implementation and stress-test the solution against it on many small random inputs; fix any differences.
6) Never end your turn with only text. Replying without writing the solution file to disk counts as FAILURE. Only finish after the solution file has been written and verified.
"""
        init_edit = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        safe_log(f"[attempt 0] initial chat finished; source patch present: {self._has_source_patch()}")

        for attempt in range(3):
            if self._has_source_patch():
                safe_log(f"[retry {attempt}] source patch detected; stopping retries.")
                break
            current_diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
            changed = self._changed_files()
            safe_log(f"[retry {attempt + 1}] no non-test source change. changed files: {changed}")
            retry_msg = f"""{task}

The current state of the repository has NO source change: the diff is empty or only touches test files.

Changed files so far: {changed if changed else '(none)'}

Current diff:
{current_diff if current_diff.strip() else '(empty)'}

This is a strict instruction: immediately use the editor tool (`create` or `edit`) to write the solution file for the problem to disk, then verify it by running it with bash on all sample inputs. Do not reply with text only. Do not only edit test files.
"""
            retry_history = chat_with_agent(retry_msg, model=self.code_model, msg_history=[], logging=safe_log)
            safe_log(f"[retry {attempt + 1}] chat finished; source patch present: {self._has_source_patch()}")

        # Verification and repair phase: run the samples and have the agent fix failures.
        samples = self._extract_samples()
        safe_log(f"[verify] extracted {len(samples)} sample(s).")
        for round_idx in range(3 if samples else 0):
            solution_path = self._solution_path()
            report, all_passed = self._run_samples(solution_path, samples)
            safe_log(f"[verify round {round_idx}] solution: {solution_path}\n{report}")
            if all_passed:
                safe_log(f"[verify round {round_idx}] all samples passed; stopping.")
                break
            current_diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
            repair_msg = f"""{task}

The solution has been run against the sample tests from the problem statement, and it did NOT pass. Raw report:

{report}

Current diff:
{current_diff if current_diff.strip() else '(empty)'}

Instructions:
- Read the report carefully: compare expected vs. actual output, and check stderr and runtime (timeouts mean the algorithm is too slow).
- Fix the solution file with the editor tool (`edit` or `create`, which overwrites).
- Write a brute-force implementation and a random stress test comparing it against the solution on many small inputs. If multiple answers are valid, write a validity checker instead of comparing exact outputs; note that any valid answer is accepted only if the problem says so.
- Generate a max-size input allowed by the constraints and time the solution on it.
- Re-run the solution on all sample inputs with bash and confirm they pass before finishing.
- Do not reply with text only; finish only after the fixes are written to disk and verified.
"""
            chat_with_agent(repair_msg, model=self.code_model, msg_history=[], logging=safe_log)
            safe_log(f"[verify round {round_idx}] repair chat finished.")

        # Performance phase: generate adversarial max-size inputs, time the solution, and repair if slow.
        solution_path = self._solution_path()
        if solution_path and os.path.exists(solution_path):
            mode, method = self._detect_mode(solution_path)
            cases = []
            try:
                _, _, cases = self._generate_stress_inputs(solution_path)
            except Exception as e:
                safe_log(f"[perf] stress input generation failed: {e}")
            if not cases:
                safe_log("[perf] no stress cases available; skipping performance phase.")
            for round_idx in range(3 if cases else 0):
                solution_path = self._solution_path()
                if not solution_path:
                    break
                report, needs_repair = self._run_perf(solution_path, cases, mode=mode, method=method)
                safe_log(f"[perf round {round_idx}] solution: {solution_path}\n{report}")
                if not needs_repair:
                    safe_log(f"[perf round {round_idx}] all stress cases fast enough; stopping.")
                    break
                current_diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
                perf_msg = f"""{task}

The solution passes the samples, but it is too slow or crashes on large adversarial inputs. Raw performance report
(each case: runtime, output, stderr; timeouts exceed 3 seconds, SLOW means above 1.5 seconds):

{report}

Current diff:
{current_diff if current_diff.strip() else '(empty)'}

Instructions:
- Compute the worst-case operation count of your algorithm in terms of the constraints (e.g. n, the value ranges). If it is more than ~5e7 simple operations, design a fundamentally better algorithm (e.g. reduce DP states, use prefix minimums, exploit the problem structure) rather than adding heuristics or early-exit pruning.
- Keep the same required interface (the stdin program, or the `Solution` class method signature).
- Fix the solution file with the editor tool (`edit` or `create`, which overwrites).
- Re-verify correctness: re-run the sample inputs with bash and, if possible, compare against a brute-force implementation on small random inputs.
- Re-time on the max-size inputs and confirm they run comfortably within the limit.
- Do not reply with text only; finish only after the fixes are written to disk and verified.
"""
                chat_with_agent(perf_msg, model=self.code_model, msg_history=[], logging=safe_log)
                safe_log(f"[perf round {round_idx}] repair chat finished.")

def main():
    parser = argparse.ArgumentParser(description='Process repository with an agentic system.')
    parser.add_argument('--problem_statement', required=True, help='The problem statement to process')
    parser.add_argument('--git_dir', required=True, help='Path to git repository directory')
    parser.add_argument('--base_commit', required=True, help='Base commit hash to compare against')
    parser.add_argument('--chat_history_file', required=True, help='Path to chat history file')
    parser.add_argument('--outdir', required=False, default="/dgm/", help='Output directory')
    parser.add_argument('--test_description', default=None, required=False, help='Description of how to test the repository')
    parser.add_argument('--self_improve', default=False, action='store_true', help='Whether to self-improve the repository or solving swe')
    parser.add_argument('--language', required=False, default="python", choices=['cpp', 'java', 'python', 'go', 'rust', 'javascript'], help='Task\'s programming language')
    args = parser.parse_args()

    # Process the repository
    agentic_system = AgenticSystem(
        problem_statement=args.problem_statement,
        git_tempdir=args.git_dir,
        base_commit=args.base_commit,
        chat_history_file=args.chat_history_file,
        test_description=args.test_description,
        self_improve=args.self_improve,
        language=args.language,
    )

    # Run the agentic system to try to solve the problem
    agentic_system.forward()

    # Get code diff and save to model_patch.diff
    model_patch = diff_versus_commit(args.git_dir, args.base_commit)
    model_patch_outfile = os.path.join(args.outdir, 'model_patch.diff') if args.outdir else 'model_patch.diff'
    with open(model_patch_outfile, 'w') as f:
        f.write(model_patch)

if __name__ == "__main__":
    main()

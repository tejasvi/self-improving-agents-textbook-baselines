import argparse
import glob
import shutil
import subprocess
import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import os
import threading
import re
import resource

from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
from utils.git_utils import diff_versus_commit, reset_to_commit, apply_patch
from tools.stress_test import run_differential, _clip_lines

# Harness evaluation settings
MAX_ATTEMPTS = 4
NUM_DIFF_TESTS = 200
FAST_LIMIT_SECONDS = 2.0
RUN_TIMEOUT = 10
MAX_NOTES_CHARS = 4000
MEMORY_LIMIT_BYTES = 1024 * 1024 * 1024  # 1 GB address space per candidate run

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

    # Basenames that count as tests/helpers rather than primary source edits.
    _NON_SOURCE_PATTERNS = ('test*', '*_test.py', 'brute*', 'gen*', 'stress*', 'sample*', 'README*', 'readme*')

    @staticmethod
    def _is_stub_function(fn_node):
        """True if a function body is only pass / ... / docstring."""
        import ast
        for stmt in fn_node.body:
            if isinstance(stmt, ast.Pass):
                continue
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and (
                    stmt.value.value is Ellipsis or isinstance(stmt.value.value, str)):
                continue
            return False
        return True

    def _solution_has_stub(self):
        """Checks solution.py (if present) for any function whose body is only pass/.../docstring."""
        import ast
        path = os.path.join(self.git_tempdir, 'solution.py')
        if not os.path.isfile(path):
            return False
        try:
            with open(path) as f:
                tree = ast.parse(f.read())
        except Exception:
            return False
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and self._is_stub_function(node):
                return True
        return False

    def _has_source_edit(self):
        """True only if the diff vs base commit touches a non-test/non-helper file with added lines,
        and solution.py (if present) has no stub functions."""
        import fnmatch
        diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        current_path = None
        added = {}
        for line in diff.splitlines():
            if line.startswith('diff --git '):
                parts = line.split(' ')
                # format: diff --git a/<path> b/<path>
                current_path = parts[-1][2:] if len(parts) >= 4 and parts[-1].startswith('b/') else None
                if current_path is not None:
                    added.setdefault(current_path, 0)
            elif current_path is not None and line.startswith('+') and not line.startswith('+++'):
                if line[1:].strip():
                    added[current_path] += 1

        has_edit = False
        for path, n_added in added.items():
            base = os.path.basename(path)
            if path.startswith(('dev/', 'candidates/')):
                continue
            if any(fnmatch.fnmatch(base, pat) for pat in self._NON_SOURCE_PATTERNS):
                continue
            if n_added > 0:
                has_edit = True
                break
        if not has_edit:
            return False
        if self._solution_has_stub():
            return False
        return True

    # ---------------------------------------------------------------
    # Harness-run evaluation (no LLM involved)
    # ---------------------------------------------------------------
    _SAMPLE_HEADER_RE = re.compile(r'^\s*Sample\s+(Input|Output)\s*(\d+)\s*:?\s*(.*)$', re.IGNORECASE)
    _SAMPLE_STOP_RE = re.compile(
        r'^\s*(Sample\b|Explanation|Example|Note\b|Constraints|Input\b|Output\b|#|Notes?\b|Time limit|Memory limit)',
        re.IGNORECASE)

    def _extract_samples(self):
        """Parse 'Sample Input N' / 'Sample Output N' blocks from the statement into dev/samples/N.in and N.out.
        Returns the number of sample pairs written."""
        blocks = {}  # (kind, n) -> list of lines
        current = None
        for line in self.problem_statement.splitlines():
            m = self._SAMPLE_HEADER_RE.match(line)
            if m:
                kind, n, rest = m.group(1).lower(), int(m.group(2)), m.group(3)
                current = (kind, n)
                blocks.setdefault(current, [])
                if rest.strip():
                    blocks[current].append(rest.strip())
                continue
            if current is None:
                continue
            stripped = line.strip()
            if stripped.startswith('```'):
                if blocks[current]:
                    current = None  # closing fence ends the block
                continue
            if self._SAMPLE_STOP_RE.match(line):
                current = None
                continue
            if stripped == '':
                if blocks[current]:
                    current = None  # blank line after content ends the block
                continue
            blocks[current].append(line.rstrip())
        samples_dir = self._dev_path('samples')
        os.makedirs(samples_dir, exist_ok=True)
        written = 0
        for (kind, n), lines in sorted(blocks.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            if kind != 'input' or not lines or ('output', n) not in blocks or not blocks[('output', n)]:
                continue
            out_lines = blocks[('output', n)]
            with open(os.path.join(samples_dir, f"{n}.in"), 'w') as f:
                f.write("\n".join(lines) + "\n")
            with open(os.path.join(samples_dir, f"{n}.out"), 'w') as f:
                f.write("\n".join(out_lines) + "\n")
            written += 1
        return written

    def _dev_path(self, *parts):
        return os.path.join(self.git_tempdir, 'dev', *parts)

    @staticmethod
    def _canon(text):
        """Exact comparison, ignoring only trailing whitespace on each line and at the end."""
        return "\n".join(line.rstrip() for line in text.strip().splitlines())

    @staticmethod
    def _limit_memory():
        resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES))

    @staticmethod
    def _run_candidate(path, data, timeout):
        """Run a python candidate on stdin data. Returns (stdout, stderr, returncode, timed_out, elapsed)."""
        start = time.time()
        try:
            p = subprocess.run(
                [sys.executable, "-I", path], input=data, capture_output=True, text=True,
                timeout=timeout, env={"PATH": os.environ.get("PATH", "")},
                preexec_fn=AgenticSystem._limit_memory,
            )
            return p.stdout, p.stderr, p.returncode, False, time.time() - start
        except subprocess.TimeoutExpired as e:
            out = e.stdout if isinstance(e.stdout, str) else (e.stdout or b"").decode(errors="replace")
            err = e.stderr if isinstance(e.stderr, str) else (e.stderr or b"").decode(errors="replace")
            return out, err, None, True, time.time() - start

    def _evaluate_candidate(self, path):
        """Evaluate a candidate solution file against the dev/ workspace.

        (a) dev/samples/*.in vs *.out (exact match), (b) differential test vs dev/brute.py using
        dev/gen.py over NUM_DIFF_TESTS seeds, (c) timing on dev/max.in.
        Returns dict: n_pass, n_total, max_time (seconds, inf on timeout), failure_text (None if all pass).
        """
        result = {"n_pass": 0, "n_total": 0, "max_time": 0.0, "failure_text": None}
        failures = []
        if not os.path.isfile(path):
            result["failure_text"] = f"Candidate file {path} does not exist."
            return result

        # (a) samples
        in_files = sorted(glob.glob(self._dev_path('samples', '*.in')))
        sample_max_time = 0.0
        sample_failure_reported = False
        for in_file in in_files:
            out_file = in_file[:-3] + '.out'
            if not os.path.isfile(out_file):
                continue
            result["n_total"] += 1
            with open(in_file) as f:
                data = f.read()
            with open(out_file) as f:
                expected = f.read()
            out, err, rc, to, elapsed = self._run_candidate(path, data, RUN_TIMEOUT)
            sample_max_time = max(sample_max_time, elapsed)
            if not to and rc == 0 and self._canon(out) == self._canon(expected):
                result["n_pass"] += 1
            elif not sample_failure_reported:
                sample_failure_reported = True
                reason = ("timed out after %d seconds" % RUN_TIMEOUT) if to else (
                    f"runtime error (exit code {rc})" if rc != 0 else "wrong answer")
                stderr_tail = "\n".join(err.strip().splitlines()[-15:]) if err.strip() else ""
                failures.append(
                    f"SAMPLE {os.path.basename(in_file)} failed: {reason}.\n"
                    f"INPUT:\n{_clip_lines(data, 40)}\n"
                    f"EXPECTED:\n{_clip_lines(expected, 40)}\n"
                    f"ACTUAL:\n{_clip_lines(out, 40)}\n"
                    + (f"STDERR (tail; MemoryError means the 1 GB memory limit was exceeded):\n{stderr_tail}\n"
                       if stderr_tail else ""))
        result["max_time"] = sample_max_time

        # (b) differential test
        brute = self._dev_path('brute.py')
        gen = self._dev_path('gen.py')
        if os.path.isfile(brute) and os.path.isfile(gen):
            n_pass, n_total, diff_time, diff_failure = run_differential(
                path, brute, gen, num_tests=NUM_DIFF_TESTS, timeout=RUN_TIMEOUT, max_output_lines=40)
            result["n_total"] += n_total
            result["n_pass"] += n_pass
            result["max_time"] = max(result["max_time"], diff_time)
            if diff_failure is not None:
                failures.append(diff_failure)

        # (c) timing on the max-size input
        max_in = self._dev_path('max.in')
        if os.path.isfile(max_in):
            with open(max_in) as f:
                data = f.read()
            out, err, rc, to, elapsed = self._run_candidate(path, data, 20)
            if to:
                result["max_time"] = float('inf')
                failures.append("TIMING: dev/max.in timed out after 20 seconds.")
            else:
                result["max_time"] = max(result["max_time"], elapsed)
                if rc != 0:
                    failures.append(f"TIMING: dev/max.in run failed (exit code {rc}).\nSTDERR:\n{_clip_lines(err, 40)}")
            if result["max_time"] > FAST_LIMIT_SECONDS:
                failures.append(f"SPEED: slowest run took {result['max_time']:.2f}s; limit is {FAST_LIMIT_SECONDS}s.")

        if result["n_total"] == 0:
            failures.append("The harness found no usable samples (dev/samples/N.in + N.out pairs were not found), "
                            "so this candidate was NOT tested and counts as a failure.")
        if failures:
            result["failure_text"] = "\n".join(failures)
        return result

    @staticmethod
    def _is_passing(ev):
        return ev["n_total"] > 0 and ev["n_pass"] == ev["n_total"] and ev["failure_text"] is None

    @staticmethod
    def _rank_key(ev):
        """Higher is better: all samples passed, then pass count, then speed."""
        all_ok = ev["n_total"] > 0 and ev["n_pass"] == ev["n_total"] and ev["n_total"] > 0
        return (all_ok, ev["n_pass"], -ev["max_time"])

    def _read_notes(self):
        path = self._dev_path('NOTES.md')
        if not os.path.isfile(path):
            return "(dev/NOTES.md does not exist yet)"
        with open(path) as f:
            text = f.read()
        if len(text) > MAX_NOTES_CHARS:
            text = "...(earlier notes clipped)...\n" + text[-MAX_NOTES_CHARS:]
        return text

    def _followup_prompt(self, task, has_solution, eval_report):
        """Short, self-contained prompt for attempts 2..N. Replaces the full previous message history."""
        brute_exists = os.path.isfile(self._dev_path('brute.py'))
        notes = self._read_notes()
        sample_failed = "SAMPLE " in (eval_report or "") and " failed:" in (eval_report or "")
        slow = "SPEED:" in (eval_report or "") or "TIMING:" in (eval_report or "")
        if not has_solution:
            if brute_exists:
                directive = ("solution.py still has no implementation. Immediately write a solution into solution.py "
                             "based on dev/brute.py (read it first; it already contains the reference logic). "
                             "Make it correct first, then check it against dev/brute.py.")
            else:
                directive = ("solution.py still has no implementation and dev/brute.py does not exist. Immediately write "
                             "dev/brute.py (a simple correct brute force), then write a correct but possibly slow "
                             "solution.py based on it.")
        elif sample_failed or slow:
            directive = ("The brute force in dev/brute.py is correct but too slow for the constraints; use it as an "
                         "oracle to derive an efficient algorithm: tabulate brute-force answers for small parameters, "
                         "look for formulas or patterns, then verify with diff_test against the oracle and run the "
                         "large sample. The failing sample below is the concrete evidence; make it pass.")
        else:
            directive = ("continue from the existing dev/ files; fix the failures or try a different approach. "
                         "Reuse dev/ files (brute.py, gen.py, samples/, max.in, NOTES.md).")
        return f"""{task}

Previous attempt summary (earlier conversation is not available; this is all you get):

<dev_notes file="dev/NOTES.md">
{notes}
</dev_notes>

<evaluation_report>
{eval_report}
</evaluation_report>

{directive}

Working rules: never print more than 40 lines from any command; summarize tables instead of printing them.
Keep each reply under about 400 words; make tool calls with all required arguments; write large files in a single editor `create` call rather than printing them.
Keep reasoning brief, and after each fix re-run the samples and dev/gen.py-based differential test."""

    def forward(self):
        """
        The forward function for the AgenticSystem.
        Runs up to MAX_ATTEMPTS attempts, evaluates each candidate with the harness, and keeps the best one.
        """
        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        method = """FIRST ACTION: view solution.py and immediately write a complete first-draft implementation using the editor tool; refine afterwards.
Keep each reply short; do not write long analyses before making a tool call.
Keep each reply under about 400 words; make tool calls with all required arguments; write large files in a single editor `create` call rather than printing them.
Dev sample files already exist: dev/samples/N.in and dev/samples/N.out were extracted from the statement automatically. Do not recreate them; use them as they are.

Dev workspace (persistent across attempts, keep helper artifacts here, under <repo>/dev/):
- Within your first 5 tool calls, write a brute force at dev/brute.py and a working (even if slow) solution.py. Save the samples from the statement to dev/samples/N.in and dev/samples/N.out (exact text).
- Write dev/gen.py that takes a seed argument and prints one small random input. Write dev/max.in with a maximum-size input.
- Keep running findings, hypotheses and what failed in dev/NOTES.md, updated as you go.
- Never print more than 40 lines from any command. Summarize tables instead of printing them.
- Stop exploring after a bounded budget (about 15 tool calls of investigation) and write code.

Work like a careful competitive programmer:
1. Read the statement and constraints. Choose an algorithm whose complexity fits the limits; Python does roughly 10^7 simple operations per second, so aim for well under that.
2. Complexity check before coding: write the worst-case operation count as a formula in n (and any other parameters, e.g. alphabet size, number of queries), evaluated at the maximum constraints. If it is above roughly 3*10^7 simple operations, find a better algorithm before writing code. Early-exit pruning, memoization shortcuts, and sorting candidates do NOT bound the worst case, so they do not count as a fix.
3. Decide whether multiple outputs can be valid (look for phrases like "any", "one of", "multiple solutions", "arbitrary", "in any order"). If so, assume the grader compares the output as exact text with a single reference output. Write a brute force that lists all valid answers for each sample and determine which tie-break rule reproduces ALL sample outputs (try: lexicographically smallest, smallest indices first, first found in natural order). Implement exactly that rule in solution.py, even if it requires extra work, as long as complexity stays within limits. Never stop at a merely valid answer.
4. Write the solution in solution.py with the editor tool.
5. Run it on every sample in the statement and compare with the expected outputs exactly (exact string equality, not just validity). For a stdin program use `python3 solution.py < sample1.txt`; for a `Solution` class method write a small driver script that calls the method on the sample arguments (add `from typing import *` and any imports you need at the top of solution.py).
6. Write a generator with structured adversarial kinds, including all-identical elements, a single dominant value, the maximum number of distinct values, sorted and reverse-sorted inputs, and the inputs that are worst for your algorithm. Run `scaling_test` on solution.py at max size (and a few smaller sizes) and read the times and log-log slope yourself. Fix any run over 1.5s, and fix any slope near 2 at n=2*10^4 (it means the algorithm is quadratic). Do this on the final solution.
7. Write a brute-force reference for small inputs and a random small-input generator, then run the `diff_test` tool (or `stress_test`) with a few hundred cases comparing solution.py with the brute force. If the answer is not unique, the brute force must output the canonical answer chosen in step 3, and the comparison must be exact string equality, not a validity check. Fix every mismatch.
8. Generate a maximum-size input and check that solution.py finishes in well under 2 seconds.
9. Keep iterating until all checks pass.
10. Before finishing, run the final solution through the run_clean tool on all samples AND on a max-size input (run_clean runs it in a clean isolated subprocess like the grader does), and compare each output to the sample's exact expected output. Read all stderr carefully and fix any crash or traceback it shows.
11. Avoid environment-fragile constructs: do not use 3-argument pow (e.g. pow(a, MOD-2, MOD)); write a small hand-written modular power helper `def mpow(b, e, m)` with a loop instead. Avoid threading and recursion-limit tricks; prefer iterative code.
12. Do a last re-read of solution.py for edge cases such as N=1, empty input, and the smallest/largest constraints.
The final solution.py is what gets graded; helper files are ignored."""
        candidate_dir = os.path.join(self.git_tempdir, 'candidates')
        os.makedirs(candidate_dir, exist_ok=True)
        solution_path = os.path.join(self.git_tempdir, 'solution.py')

        best = None  # (key, path, attempt, ev)
        try:
            n_samples = self._extract_samples()
            safe_log(f"[setup] extracted {n_samples} sample pair(s) into dev/samples/")
        except Exception as e:  # never let parsing break the run
            safe_log(f"[setup] sample extraction failed: {e!r}")
        eval_report = ""
        for attempt in range(MAX_ATTEMPTS):
            num = attempt + 1
            if attempt == 0:
                prompt = f"{task}\n\n{method}"
            else:
                prompt = self._followup_prompt(task, self._has_source_edit(), eval_report)
            safe_log(f"[attempt {num}/{MAX_ATTEMPTS}] starting")
            chat_with_agent(prompt, model=self.code_model, msg_history=[], logging=safe_log)

            has_solution = self._has_source_edit()
            if not has_solution:
                safe_log(f"[attempt {num}] no usable solution.py written")
                eval_report = ("solution.py was not written with a real implementation in this attempt. "
                               "Write the brute-force-based fallback immediately.")
                continue

            cand_path = os.path.join(candidate_dir, f"attempt{num}.py")
            shutil.copyfile(solution_path, cand_path)
            ev = self._evaluate_candidate(cand_path)
            safe_log(f"[attempt {num}] harness: pass {ev['n_pass']}/{ev['n_total']}, max_time {ev['max_time']:.3f}s")
            key = self._rank_key(ev)
            if best is None or key > best[0]:
                best = (key, cand_path, num, ev)
            if self._is_passing(ev) and ev["max_time"] <= FAST_LIMIT_SECONDS:
                safe_log(f"[attempt {num}] passing and fast; stopping")
                break
            eval_report = (f"Harness pass count: {ev['n_pass']}/{ev['n_total']}, slowest run {ev['max_time']:.2f}s.\n"
                           + (ev["failure_text"] or "All checks passed, but the run was too slow."))

        if best is not None and best[3]["n_total"] > 0:
            shutil.copyfile(best[1], solution_path)
            ok = self._is_passing(best[3])
            safe_log(f"[final] solution.py set to attempt {best[2]} (pass {best[3]['n_pass']}/{best[3]['n_total']}, "
                     f"all_passed={ok}, max_time {best[3]['max_time']:.3f}s)")
            if not ok:
                safe_log("[final] WARNING: no candidate passed every sample; kept the best-scoring one.")
        elif best is not None:
            safe_log(f"[final] best candidate (attempt {best[2]}) had no usable samples; solution.py left unchanged")
        else:
            safe_log("[final] no candidate was produced; solution.py left unchanged")

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

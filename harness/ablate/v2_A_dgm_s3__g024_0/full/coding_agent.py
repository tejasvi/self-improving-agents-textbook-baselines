import argparse
import ast
import subprocess
import logging
import time
from logging.handlers import RotatingFileHandler
import os
import re
import threading

from llm import create_client, get_response_from_llm
from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
from utils.git_utils import diff_versus_commit, reset_to_commit, apply_patch

# Explicit output budget for fallback calls (thinking models can exhaust small defaults).
LARGE_MAX_TOKENS = 16384

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

    def _get_changed_files(self):
        """
        Return the list of files changed relative to base_commit, including untracked files.
        """
        changed = set()
        commands = [
            ["git", "-C", self.git_tempdir, "diff", "--name-only", self.base_commit],
            ["git", "-C", self.git_tempdir, "ls-files", "--others", "--exclude-standard"],
        ]
        for cmd in commands:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            for line in result.stdout.decode(errors='replace').splitlines():
                line = line.strip()
                if line:
                    changed.add(line)
        return sorted(changed)

    def _is_test_file(self, path):
        """
        Heuristically decide whether a path refers to a test file.
        """
        test_tokens = {'test', 'tests', 'spec', 'specs', 'conftest'}
        normalized = path.replace('\\', '/')
        parts = [p for p in normalized.split('/') if p]
        if not parts:
            return False
        # Directory components must match exactly
        for part in parts[:-1]:
            if part.lower() in test_tokens:
                return True
        # Filename: split into words on non-alphanumeric characters
        filename = parts[-1].lower()
        words = re.split(r'[^a-z0-9]+', filename)
        return any(w in test_tokens for w in words)

    def _is_stub_patch(self):
        """
        True if the target file is unchanged from base_commit, or if it still contains only
        stub bodies (`pass` or `NotImplementedError`).
        """
        target = self._target_file()
        unchanged = subprocess.run(
            ["git", "-C", self.git_tempdir, "diff", "--quiet", self.base_commit, "--", target],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        ).returncode == 0
        if unchanged:
            return True
        path = os.path.join(self.git_tempdir, target)
        if not os.path.isfile(path):
            return True
        try:
            with open(path, 'r', errors='replace') as fh:
                tree = ast.parse(fh.read())
        except Exception:
            return False  # Unparseable code is not a recognised stub; let it count as a patch.
        bodies = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body = [s for s in node.body
                        if not (isinstance(s, ast.Expr) and isinstance(getattr(s, 'value', None), ast.Constant)
                                and isinstance(s.value.value, str))]  # skip docstrings
                bodies.append(body)
        if not bodies:
            return False
        def is_stub(body):
            if not body:
                return True
            if len(body) != 1:
                return False
            stmt = body[0]
            if isinstance(stmt, ast.Pass):
                return True
            if isinstance(stmt, ast.Raise) and stmt.exc is not None:
                exc = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
                return isinstance(exc, ast.Name) and exc.id == 'NotImplementedError'
            return False
        return all(is_stub(b) for b in bodies)

    def _has_source_patch(self):
        """
        True if at least one changed file is not a test file, and the target is not just a stub.
        """
        changed_source = any(not self._is_test_file(f) for f in self._get_changed_files())
        return changed_source and not self._is_stub_patch()

    def _target_file(self):
        """
        Infer the primary source file to edit: first backticked *.py name in the problem
        statement that exists in the repo (or is named there), falling back to solution.py.
        """
        candidates = re.findall(r'`([\w./-]+\.py)`', self.problem_statement or '')
        for cand in candidates:
            if not cand.startswith('test') and '/test' not in cand and not os.path.basename(cand).startswith('test_'):
                return cand
        return 'solution.py'

    def _duplicates_problem(self, text):
        """
        True if the file's content is mostly contained in the problem statement (e.g. a README
        that repeats the task), so including it would duplicate the problem in the prompt.
        """
        problem_lines = {l.strip() for l in (self.problem_statement or '').splitlines() if l.strip()}
        file_lines = [l.strip() for l in text.splitlines() if l.strip()]
        if not file_lines:
            return False
        overlap = sum(1 for l in file_lines if l in problem_lines)
        return overlap / len(file_lines) >= 0.6

    def _build_condensed_prompt(self, target, max_listing=50):
        """
        Compact version of the task prompt: the problem statement appears once, the repo snapshot
        has a truncated listing and no README/problem-duplicate files.
        """
        target_path = os.path.join(self.git_tempdir, target)
        snapshot = self._snapshot_repo(max_files=5, max_listing=max_listing)
        return (
            f"I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.\n\n"
            f"<problem_description>\n{self.problem_statement}\n</problem_description>\n\n"
            f"{snapshot}\n\n"
            f"The repository currently has no source patch. Your very first action must be an editor create/edit call "
            f"on {target_path} (the primary source file) that implements the solution. Then run it via bash on the "
            f"sample inputs, and finish with a short summary."
        )

    def _snapshot_repo(self, max_files=10, max_file_bytes=8 * 1024, max_listing=200):
        """
        Deterministically collect the repo file listing (git ls-files) and the contents of
        small text files (solution.py, README, starter files), without involving the LLM.
        """
        try:
            result = subprocess.run(
                ["git", "-C", self.git_tempdir, "ls-files"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            files = [l.strip() for l in result.stdout.decode(errors='replace').splitlines() if l.strip()]
        except Exception as e:
            files = []
            safe_log(f"Snapshot: git ls-files failed: {e}")
        listing = files[:max_listing]
        listing_text = "\n".join(listing)
        if len(files) > max_listing:
            listing_text += f"\n... ({len(files) - max_listing} more files not shown)"

        # Priority: target file, README, then other small files that look like starters.
        target = self._target_file()
        def priority(f):
            base = os.path.basename(f).lower()
            if f == target:
                return 0
            if base.startswith('readme'):
                return 1
            if base == 'solution.py':
                return 2
            if base.endswith('.py') and not self._is_test_file(f):
                return 3
            return 4
        ordered = sorted(files, key=lambda f: (priority(f), f))

        contents = []
        for f in ordered:
            if len(contents) >= max_files:
                break
            if priority(f) >= 4 and f != target:
                continue
            path = os.path.join(self.git_tempdir, f)
            try:
                if not os.path.isfile(path) or os.path.getsize(path) >= max_file_bytes:
                    continue
                with open(path, 'rb') as fh:
                    raw = fh.read()
                if b'\0' in raw:
                    continue
                text = raw.decode('utf-8', errors='replace')
            except Exception:
                continue
            if f != target and self._duplicates_problem(text):
                continue  # the problem statement is already included verbatim in the prompt
            contents.append(f"--- {f} ---\n{text}")

        return f"Repository files (git ls-files):\n{listing_text}\n\n" + "\n\n".join(contents)

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
        workflow = """
Follow this workflow step by step:
1. Explore the repository: list the files and read the relevant code, tests, and any README or specification.
2. Identify the primary source file that must be changed. If the task names a file (e.g. solution.py) and it does not exist, create it. First derive an algorithm that fits the constraints (N up to 2e5 implies O(N log N) or better); a brute force is only for testing, never for solution.py.
3. Implement the solution by actually calling the editor tool (command=create or command=edit) on the source file. Do not only describe the code in text. The final solution must meet the stated constraints; an exponential or brute-force baseline must not be the final answer.
4. Test it: run the program via bash with the sample inputs from the problem statement and with your own edge cases. For interactive problems, write a small local judge/simulator and run your solution against it.
5. Finally verify with `git status` and `git diff` that the source file has actually changed. Fix any problems you find.

IMPORTANT RULES:
- You MUST make changes using the editor tool. Do not just answer in text.
- If the task names an output file such as solution.py, create it.
- Responding with text only and no file edits counts as failure.
- Modifying only test files does not solve the task; the primary source file must be changed.
"""
        target = self._target_file()
        snapshot = self._snapshot_repo()
        instruction = (
            f"{task}\n{workflow}\n"
            f"Current repository contents:\n{snapshot}\n\n"
            f"Your first action must be an editor create/edit on {os.path.join(self.git_tempdir, target)} "
            f"(the primary source file) that implements the solution."
        )
        msg_history = []
        msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=msg_history, logging=safe_log)
        safe_log(f"Initial attempt finished. Changed files: {self._get_changed_files()}")

        if self._has_source_patch():
            safe_log("Source patch detected after initial attempt; skipping retries.")
        else:
            # Bounded escalation ladder. Each strategy starts a fresh conversation (never reuse a
            # history that may end with an empty assistant turn) and stops once a source patch exists.
            target = self._target_file()
            full_prompt = (
                f"{task}\n{self._snapshot_repo()}\n\n"
                f"The repository currently has no source patch. Your very first action must be an editor "
                f"create/edit call on {os.path.join(self.git_tempdir, target)} (the primary source file) "
                f"that implements the solution. Then run it via bash on the sample inputs, and finish with a summary."
            )
            condensed_prompt = self._build_condensed_prompt(target)
            alternate_model = OPENAI_MODEL if self.code_model == CLAUDE_MODEL else CLAUDE_MODEL
            strategies = [
                ("current model, full prompt", self.code_model, full_prompt, None),
                ("current model, condensed prompt, temp=0.7", self.code_model, condensed_prompt, 0.7),
                ("alternate model, condensed prompt", alternate_model, condensed_prompt, None),
            ]
            for idx, (name, model, prompt, temperature) in enumerate(strategies):
                if idx == 1:
                    time.sleep(5)  # brief pause before re-trying the same model
                safe_log(f"Escalation strategy {idx + 1}/{len(strategies)}: {name} (model={model}); target: {target}")
                try:
                    msg_history = chat_with_agent(
                        prompt, model=model, msg_history=[], logging=safe_log, temperature=temperature,
                        max_tokens=LARGE_MAX_TOKENS,
                    )
                except Exception as e:
                    safe_log(f"Strategy {idx + 1} raised {e!r}")
                    continue
                has_patch = self._has_source_patch()
                safe_log(f"Strategy {idx + 1} finished. Changed files: {self._get_changed_files()}, "
                         f"source patch: {has_patch}")
                if has_patch:
                    safe_log(f"Source patch produced by strategy {idx + 1} ({name}, model={model}).")
                    break
            else:
                safe_log("All escalation strategies finished without a source patch.")

        self._run_verification(msg_history)

        if not self._has_source_patch():
            safe_log("Last-resort attempt: requesting the complete solution as a code block (no tools).")
            self._last_resort_write()
            safe_log(f"Last-resort finished. Changed files: {self._get_changed_files()}, "
                     f"source patch: {self._has_source_patch()}")

    def _last_message_text(self, msg_history):
        """Return the text of the last assistant message in msg_history, or '' if none."""
        for msg in reversed(msg_history or []):
            if msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            if isinstance(content, str):
                return content
            for block in content or []:
                text = block.get("text") if isinstance(block, dict) else getattr(block, "text", None)
                if text:
                    return text
            return ""
        return ""

    def _verification_prompt(self, round_idx, max_rounds):
        """Build the mandatory stress-test verification prompt for one round."""
        target = self._target_file()
        target_path = os.path.join(self.git_tempdir, target)
        retry_note = ""
        if round_idx > 0:
            retry_note = (
                f"This is verification round {round_idx + 1} of {max_rounds}: the previous round did not finish "
                f"with a clean stress test. Re-check the solution from scratch against the brute force.\n\n"
            )
        return f"""{retry_note}Verification phase (mandatory). Do not finish until this is done.

The solution at {target_path} passing the sample tests is NOT enough; subtle modelling errors are common. Verify it against an independent brute-force reference.

1. Create scratch files ONLY under /tmp/stress/ (never inside {self.git_tempdir}):
   - /tmp/stress/brute.py: an EXHAUSTIVE search that follows the literal rules of the problem statement directly (e.g. enumerate all choices / all permutations / all subsets / BFS over states). Do NOT re-implement the same idea or formula as the solution; it must be an independent, obviously-correct method. Keep it fast enough for small inputs.
   - /tmp/stress/gen.py: takes a seed as its last argument (sys.argv[-1]), seeds `random` with it, and prints ONE random small input that respects all the problem's constraints. Include edge cases (minimum sizes, all-equal values, duplicates, boundary values) with reasonable probability.
2. Make sure the solution can be run on stdin/stdout (or, if the task is a `Solution` class method, write a small wrapper in /tmp/stress/ that imports it from {target_path} and calls the method on the parsed input, then prints the result).
3. Run the differential stress test with the `stress_test` tool, e.g. solution_cmd="python3 {target_path}", brute_cmd="python3 /tmp/stress/brute.py", generator_cmd="python3 /tmp/stress/gen.py", num_tests=1000. Run at least 500 cases (up to 2000). If the tool is unavailable, write /tmp/stress/stress.py yourself that loops over seeds with subprocess timeouts and compares outputs.
4. If there is ANY mismatch (or a timeout/crash):
   a. Minimise the failing input by hand until it is tiny, and examine both outputs.
   b. Reason explicitly about which modelling assumption of the solution is wrong (for example a wrong cost model, a missed case, an off-by-one, a greedy that is not optimal, or a misread rule). Do not guess blindly; check the brute force first if you suspect it.
   c. Fix {target_path} with the editor tool (use str_replace for targeted edits).
   d. Rerun the stress test until it reports no mismatches over the full number of cases.
5. Timing (mandatory, before you may report success): generate a maximum-size input that respects the constraints (for example via a small script in /tmp/stress/) and time the solution with `time` via bash. If it takes more than about 1 second, or exceeds the constraints' intended complexity, optimise the algorithm (not just micro-optimise) and re-run the stress test to confirm it still agrees with the brute force. Never leave an exponential or brute-force solution as the final answer.
6. Run the sample tests from the problem statement once more.
7. Finally run `git -C {self.git_tempdir} status` and `git -C {self.git_tempdir} diff` to confirm that the only changes are to the source file(s) and that no scratch files (brute.py, gen.py, stress.py, timing inputs, __pycache__ or similar) were left in the repository. Delete any that were.

When everything is done, end your reply with a short report that includes the stress test summary (number of cases, seeds, result) and the timing of the max-size input. If and only if the stress test passed with zero mismatches, include the exact marker line `STRESS TEST PASSED` in that final reply."""

    def _history_ran_bash(self, msg_history):
        """
        True if any assistant turn in msg_history invoked the bash tool (Claude tool_use block).
        Manual-tool histories record calls as text, so they are matched by the tool name too.
        """
        for msg in msg_history or []:
            if msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            blocks = content if isinstance(content, list) else []
            for block in blocks:
                if isinstance(block, dict):
                    btype, name = block.get("type"), block.get("name")
                else:
                    btype, name = getattr(block, "type", None), getattr(block, "name", None)
                if btype == "tool_use" and name == "bash":
                    return True
                text = (block.get("text") if isinstance(block, dict) else getattr(block, "text", None)) or ""
                if btype == "text" and "'tool_name': bash" in text:
                    return True
        return False

    def _run_verification(self, msg_history, max_rounds=2):
        """
        Mandatory differential-testing phase: a bounded number of rounds (no unbounded loops),
        each a chat_with_agent call that reuses the message history. A round counts as verified only
        when the agent's final turn is non-empty, contains the STRESS TEST PASSED marker, and the
        solution was actually executed (a bash run appears in the history). Empty turns and never-run
        solutions are reported as unverified.
        """
        if not self._has_source_patch():
            safe_log("Verification skipped: no source patch present.")
            return msg_history
        verified = False
        for round_idx in range(max_rounds):
            safe_log(f"Verification round {round_idx + 1}/{max_rounds} starting.")
            prompt = self._verification_prompt(round_idx, max_rounds)
            msg_history = chat_with_agent(prompt, model=self.code_model, msg_history=msg_history, logging=safe_log)
            final_text = self._last_message_text(msg_history)
            if not final_text.strip():
                safe_log(f"Verification round {round_idx + 1}/{max_rounds}: last assistant turn is empty; "
                         f"treating as NOT verified.")
                continue
            ran = self._history_ran_bash(msg_history)
            if not ran:
                safe_log(f"Verification round {round_idx + 1}/{max_rounds}: no bash run found in history; "
                         f"solution was never executed, treating as NOT verified.")
            passed = "STRESS TEST PASSED" in final_text and ran
            safe_log(f"Verification round {round_idx + 1}/{max_rounds} finished. "
                     f"Marker found: {passed}. Changed files: {self._get_changed_files()}")
            if passed:
                verified = True
                break
        if not verified:
            safe_log(f"Verification: NOT verified after {max_rounds} rounds.")
        return msg_history

    def _last_resort_write(self):
        """
        Tool-free fallback: ask the LLM for the complete target file in a fenced code block,
        then write it from Python so the patch is never empty. Tries the code model first,
        then the alternate model. Never raises on empty or malformed responses.
        """
        target = self._target_file()
        target_path = os.path.join(self.git_tempdir, target)
        existing = ''
        if os.path.isfile(target_path):
            with open(target_path, 'r', errors='replace') as fh:
                existing = fh.read()
        prompt = (
            f"Solve the following problem by writing the COMPLETE contents of the file `{target}`.\n\n"
            f"<problem_description>\n{self.problem_statement}\n</problem_description>\n\n"
            f"Current contents of {target}:\n```python\n{existing}\n```\n\n"
            f"Reply with ONLY the complete file in a single ```python code block. No other text."
        )
        alternate_model = OPENAI_MODEL if self.code_model == CLAUDE_MODEL else CLAUDE_MODEL
        code = None
        for model in [self.code_model, alternate_model]:
            try:
                client, client_model = create_client(model)
                content, _ = get_response_from_llm(
                    msg=prompt,
                    client=client,
                    model=client_model,
                    system_message="You are an expert competitive programmer. Output only code.",
                    msg_history=[],
                    max_tokens=LARGE_MAX_TOKENS,
                )
            except Exception as e:
                safe_log(f"Last-resort LLM call failed (model={model}): {e!r}")
                continue
            content = content if isinstance(content, str) else ''
            safe_log(f"Last-resort response (model={model}): raw content length {len(content)}")
            code = self._extract_code(content)
            if code is not None:
                break
            safe_log(f"Last-resort: no usable code found in response from model={model}.")
        if code is None:
            safe_log("Last-resort: giving up; no code could be extracted from any model.")
            return
        if 'from typing import List' in existing and 'from typing import List' not in code:
            code = 'from typing import List\n\n' + code
        os.makedirs(os.path.dirname(target_path) or '.', exist_ok=True)
        with open(target_path, 'w') as fh:
            fh.write(code if code.endswith('\n') else code + '\n')
        safe_log(f"Last-resort: wrote {target}.")

    def _extract_code(self, content):
        """
        Return the first fenced code block in content, or the raw text if it parses as Python.
        Returns None when neither is available.
        """
        match = re.search(r'```(?:python|py)?\s*\n(.*?)```', content or '', re.DOTALL)
        if match and match.group(1).strip():
            return match.group(1)
        raw = (content or '').strip()
        if raw:
            try:
                ast.parse(raw)
                return raw
            except SyntaxError:
                pass
        return None

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

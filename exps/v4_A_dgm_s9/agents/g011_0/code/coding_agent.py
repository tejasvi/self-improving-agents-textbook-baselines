import argparse
import hashlib
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import threading

from llm import create_client, get_response_from_llm
from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
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


DEFAULT_SOLUTION_FILES = {
    "python": "solution.py",
    "cpp": "solution.cpp",
    "java": "Solution.java",
    "go": "solution.go",
    "rust": "solution.rs",
    "javascript": "solution.js",
}

def _block_text(block):
    """Return the text of a content block (dict or object), or ''."""
    if isinstance(block, dict):
        return block.get("text") or ""
    return getattr(block, "text", None) or ""

def _block_type(block):
    if isinstance(block, dict):
        return block.get("type")
    return getattr(block, "type", None)

def _history_has_tool_use(msg_history):
    """
    True if the history contains any tool use: Claude-style 'tool_use' content blocks,
    OpenAI-style 'tool_calls' on messages or 'tool' role messages, or the manual
    '<tool_use>' text format.
    """
    for msg in msg_history or []:
        if isinstance(msg, dict):
            role = msg.get("role")
            if role == "tool" or msg.get("tool_calls"):
                return True
            content = msg.get("content")
        else:
            if getattr(msg, "tool_calls", None):
                return True
            role = getattr(msg, "role", None)
            content = getattr(msg, "content", None)
        if isinstance(content, str):
            if "<tool_use>" in content:
                return True
            continue
        for block in content or []:
            if _block_type(block) in ("tool_use", "tool_result"):
                return True
            if "<tool_use>" in _block_text(block):
                return True
    return False

def _last_assistant_text(msg_history):
    """Return the text of the final assistant message in the history ('' if none)."""
    for msg in reversed(msg_history or []):
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", None)
        if role != "assistant":
            continue
        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", None)
        if isinstance(content, str):
            text = content
        else:
            text = "".join(_block_text(b) for b in (content or []))
        return text.strip()
    return ""

def _is_empty_assistant_msg(msg):
    """True if msg is an assistant turn with whitespace-only text and no tool use."""
    role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", None)
    if role != "assistant":
        return False
    if _history_has_tool_use([msg]):
        return False
    content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", None)
    if isinstance(content, str):
        text = content
    else:
        text = "".join(_block_text(b) for b in (content or []))
    return not text.strip()

def _sanitize_history(msg_history):
    """
    Drop trailing assistant messages that are empty/whitespace-only with no tool use.
    Returns [] if nothing useful remains.
    """
    hist = list(msg_history or [])
    for _ in range(len(hist)):
        if hist and _is_empty_assistant_msg(hist[-1]):
            hist.pop()
        else:
            break
    return hist

VERIFIED_TOKEN = "VERIFIED_OK"
NOT_VERIFIED_TOKEN = "NOT_VERIFIED"

def _has_verified_ok(msg_history):
    """True if the last assistant text carries the VERIFIED_OK verdict (and not NOT_VERIFIED)."""
    text = _last_assistant_text(msg_history)
    return VERIFIED_TOKEN in text and NOT_VERIFIED_TOKEN not in text

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

    def _git(self, *args):
        """Run a git command in the task repo and return its stdout (empty string on failure)."""
        result = subprocess.run(
            ["git", "-C", self.git_tempdir, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return result.stdout.decode('utf-8', errors='replace')

    def _changed_files(self):
        """
        Return the sorted list of files changed versus base_commit, including untracked files.
        """
        files = set()
        # Tracked changes versus base commit
        for line in self._git("diff", "--name-only", self.base_commit).splitlines():
            if line.strip():
                files.add(line.strip())
        # Working tree status (covers untracked files, and uncommitted changes)
        for line in self._git("status", "--porcelain", "-uall").splitlines():
            if len(line) < 4:
                continue
            path = line[3:]
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            path = path.strip().strip('"')
            if path:
                files.add(path)
        return sorted(files)

    def _is_test_path(self, p):
        """
        Heuristic: a path is a test file if its lowercased basename contains "test"
        (or "conftest"), or if it lives under a tests/ or test/ directory.
        """
        normalized = p.replace("\\", "/").lower()
        parts = [c for c in normalized.split("/") if c]
        if not parts:
            return False
        basename, dirs = parts[-1], parts[:-1]
        if "test" in basename or "conftest" in basename:
            return True
        if any(c in ("tests", "test") for c in dirs):
            return True
        return False

    def _has_source_edit(self):
        """
        True if at least one changed non-test file exists and the repo diff is non-empty.
        """
        changed = self._changed_files()
        has_source = any(not self._is_test_path(f) for f in changed)
        diff = diff_versus_commit(self.git_tempdir, self.base_commit)
        return bool(has_source and str(diff).strip())

    def _solution_hash(self, solution_file):
        """Hash of the solution file contents (or of the whole repo diff if no file is known)."""
        if solution_file:
            path = os.path.join(self.git_tempdir, solution_file)
            try:
                with open(path, "rb") as f:
                    return hashlib.sha256(f.read()).hexdigest()
            except OSError:
                return "missing"
        return hashlib.sha256(str(diff_versus_commit(self.git_tempdir, self.base_commit)).encode()).hexdigest()

    def _extract_solution_filename(self):
        """
        Find the required output filename mentioned in the problem statement (e.g. solution.py).
        Returns None if no filename is mentioned.
        """
        matches = re.findall(r'[\w\-./]+\.(?:py|cpp|java|go|rs|js|ts)\b', self.problem_statement or "")
        for m in matches:
            if not self._is_test_path(m):
                return m
        return None

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
        solution_file = self._extract_solution_filename()
        target_hint = (
            f"The solution file is `{solution_file}` (named in the problem statement)."
            if solution_file else
            "Identify the file the problem names; if none is named, create a sensible solution file in the repo root."
        )
        workflow = f"""
Follow this workflow:
1. Inspect the repository with bash: run `ls -la {self.git_tempdir}`, `cat` any existing relevant files, and locate the file the task names. {target_hint}
2. Think through the algorithm and its time/space complexity against the constraints in the problem statement.
3. Write the full solution with the editor tool (use `create` if the file is missing, `edit` otherwise).
4. Run the solution on every sample input/output from the problem statement with bash, and fix any mismatch.
5. Test a worst-case-sized input with bash to confirm the solution runs within the time limit.

IMPORTANT RULES:
- You MUST modify or create the source file using the editor tool. A text-only reply without file edits is a failure.
- Do not only write tests; the actual solution source file must be created or edited.
- Finishing with a known failing test is a failure. Announcing a fix without a tool call that applies it is also a failure: if you state a plan, follow it with an actual tool call.
- For problems with a small-case formulation, write a brute-force solution and a random stress test comparing it against your solution, and run it.
"""
        instruction = f"{task}\n\nPlease analyze the problem description carefully. Then make edits to the code files to complete the instruction.\n{workflow}"

        msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        msg_history = self._ensure_source_edit(task, solution_file, msg_history)

        # Bounded verify-and-repair loop: never finish with a known-failing solution.
        verify_prompt = (
            "Audit your work. Re-read the solution file with the editor view command. "
            "Run all samples from the problem statement. "
            "If you have not run a randomized brute-force comparison, write one now (a brute-force or "
            "reference solution plus a random small-case generator) and run it. "
            "If ANY output mismatches, or if your previous message described a fix you have not yet applied, "
            "apply the fix with the editor tool now and re-run. "
            "Finish your reply with exactly one line: VERIFIED_OK if all samples and the brute-force "
            "comparison pass with zero mismatches, otherwise NOT_VERIFIED."
        )
        stronger_hint = (
            "\nYour previous check did not verify the solution and you made no change to the solution file. "
            "Rethink the algorithm from first principles: test small cases by hand, examine the smallest "
            "counterexample from your brute-force comparison, and derive the correct logic before editing."
        )
        last_verdict_unchanged = False
        for verify_round in range(4):
            if not self._has_source_edit():
                safe_log(f"[verify-loop] skipping round={verify_round}: no source edit")
                break
            msg_history = _sanitize_history(msg_history)
            before_hash = self._solution_hash(solution_file)
            round_prompt = verify_prompt
            if verify_round > 0 and last_verdict_unchanged:
                round_prompt = verify_prompt + stronger_hint
            msg_history = chat_with_agent(
                round_prompt, model=self.code_model, msg_history=msg_history, logging=safe_log
            )
            after_hash = self._solution_hash(solution_file)
            verified = _has_verified_ok(msg_history)
            last_verdict_unchanged = (before_hash == after_hash) and not verified
            safe_log(
                f"[verify-loop] round={verify_round} verified={verified} "
                f"solution_changed={before_hash != after_hash}"
            )
            if verified:
                break

        max_retries = 3
        failure_class = None
        retries_used = 0
        for attempt in range(max_retries):
            has_edit = self._has_source_edit()
            changed = self._changed_files()
            safe_log(f"[verify] attempt={attempt} has_source_edit={has_edit} changed_files={changed}")
            if has_edit:
                failure_class = None
                break

            failure_class = self._classify_failure(msg_history)
            safe_log(f"[verify] attempt={attempt} failure_class={failure_class}")
            is_last = attempt == max_retries - 1
            file_hint = solution_file or DEFAULT_SOLUTION_FILES.get(self.language, "solution.py")
            nudge = (
                f"Call the editor tool now: command=create, path={self.git_tempdir}/{file_hint}, "
                f"file_text=<complete solution>. Then run the samples with bash."
            )
            if attempt == 0:
                corrective = (
                    f"Your previous reply was {'empty' if failure_class == 'empty_reply' else 'incomplete'} "
                    f"and made no source edits. " + nudge
                )
            else:
                corrective = (
                    f"Still no non-test source change. Currently changed files: "
                    f"{changed if changed else '(none)'}.\n" + nudge
                )
            if is_last:
                corrective += (
                    "\nFinal attempt: write your best effort now, even if unsure. "
                    "An imperfect patch is better than none."
                )

            retries_used += 1
            safe_log(f"[retry] attempt={attempt} class={failure_class} retry={retries_used}")
            if failure_class == "empty_reply":
                # Broken history: start fresh with the task text plus the nudge.
                msg_history = chat_with_agent(
                    f"{task}\n{corrective}", model=self.code_model, msg_history=[], logging=safe_log
                )
            else:
                msg_history = chat_with_agent(
                    corrective, model=self.code_model, msg_history=msg_history, logging=safe_log
                )

        fallback_used = False
        if not self._has_source_edit():
            fallback_used = True
            safe_log(f"[fallback] no source edit after {retries_used} retries; class={failure_class}")
            self._write_fallback_solution(solution_file)

        final_has_edit = self._has_source_edit()
        safe_log(
            f"[verify] final has_source_edit={final_has_edit} fallback_used={fallback_used} "
            f"retries={retries_used} failure_class={failure_class} changed_files={self._changed_files()}"
        )

    def _solution_is_valid(self, path):
        """
        True if the file exists and is non-empty; for Python also requires py_compile to pass.
        Returns (ok, error_message).
        """
        try:
            with open(path, "r") as f:
                content = f.read()
        except OSError as e:
            return False, f"cannot read {path}: {e}"
        if not content.strip():
            return False, f"{path} is empty"
        if path.endswith(".py"):
            result = subprocess.run(
                ["python", "-m", "py_compile", path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            if result.returncode != 0:
                return False, result.stderr.decode("utf-8", errors="replace")
        return True, ""

    def _ensure_source_edit(self, task, solution_file, msg_history):
        """
        Guarantee a non-test source edit exists. Retries from a clean history with
        progressively simpler prompts (bounded), then falls back to a no-tool solution request.
        """
        if self._has_source_edit():
            safe_log("[ensure] source edit present after first turn")
            return msg_history

        target = solution_file or DEFAULT_SOLUTION_FILES.get(self.language, "solution.py")
        target_path = f"{self.git_tempdir}/{target}"
        prompts = [
            f"{task}\nYour FIRST action must be a call to the editor tool: command=create, path={target_path}, "
            f"file_text=<complete solution>. Do not reply with text only. (Use command=edit if the file exists.)",
            f"Call the editor tool now: command=create, path={target_path}, file_text=<complete solution>. "
            f"No text reply.\n<problem_description>\n{self.problem_statement}\n</problem_description>",
            f"Write the solution to {target_path} using the editor tool immediately.",
        ]
        for attempt in range(3):
            safe_log(f"[ensure] attempt={attempt} no source edit yet; retrying from clean history")
            msg_history = chat_with_agent(
                prompts[attempt], model=self.code_model, msg_history=[], logging=safe_log
            )
            msg_history = _sanitize_history(msg_history)
            if self._has_source_edit():
                safe_log(f"[ensure] source edit produced on attempt={attempt}")
                return msg_history

        safe_log("[ensure] still no source edit after attempts; using no-tool fallback")
        self._write_fallback_solution(solution_file)
        target_file = os.path.join(self.git_tempdir, target)
        ok, err = self._solution_is_valid(target_file)
        safe_log(f"[ensure] fallback valid={ok}")
        if not ok:
            safe_log(f"[ensure] re-running fallback with error: {err[:500]}")
            self._write_fallback_solution(solution_file, extra_note=f"The previous attempt failed to compile/validate with:\n{err}\nFix it.")
            ok, err = self._solution_is_valid(target_file)
            safe_log(f"[ensure] second fallback valid={ok}")
        return msg_history

    def _classify_failure(self, msg_history):
        """
        Classify why the last turn produced no source edit:
          'tests_only'    - files changed, but all are test files
          'empty_reply'   - no tool use and the last assistant text is empty
          'no_tool_calls' - no tool use, but some text was produced
        """
        changed = self._changed_files()
        if changed and all(self._is_test_path(f) for f in changed):
            return "tests_only"
        if not _history_has_tool_use(msg_history) and not _last_assistant_text(msg_history):
            return "empty_reply"
        return "no_tool_calls"

    def _write_fallback_solution(self, solution_file, extra_note=""):
        """
        Last resort: ask for the complete solution as a single fenced code block (no tools)
        and write it to the target file.
        """
        target_name = solution_file or DEFAULT_SOLUTION_FILES.get(self.language, "solution.py")
        target_path = os.path.join(self.git_tempdir, target_name)
        prompt = (
            f"Output ONLY the complete contents of the solution file `{target_name}` "
            f"in a single ```{self.language} code block, no tools, no explanation.\n\n"
            f"<problem_description>\n{self.problem_statement}\n</problem_description>"
            + (f"\n\n{extra_note}" if extra_note else "")
        )
        try:
            client, client_model = create_client(self.code_model)
            response, _ = get_response_from_llm(
                msg=prompt,
                client=client,
                model=client_model,
                system_message="You are a competitive programming expert. Reply with code only.",
                msg_history=[],
            )
        except Exception as e:
            safe_log(f"[fallback] LLM call failed: {e}", level=logging.WARNING)
            return False

        match = re.search(r"```(?:python|cpp|java|go|rust|javascript)?\n(.*?)```", response or "", re.DOTALL)
        if not match or not match.group(1).strip():
            safe_log("[fallback] no code block found in reply", level=logging.WARNING)
            return False

        os.makedirs(os.path.dirname(target_path) or ".", exist_ok=True)
        with open(target_path, "w") as f:
            f.write(match.group(1))
        safe_log(f"[fallback] wrote {target_path} ({len(match.group(1))} chars)")
        return True

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

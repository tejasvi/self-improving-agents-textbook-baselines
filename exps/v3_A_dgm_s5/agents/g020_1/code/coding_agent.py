import argparse
import subprocess
import sys
import logging
import fnmatch
from logging.handlers import RotatingFileHandler
import os
import threading
import re

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
        Return the list of changed or untracked file paths in git_tempdir (relative to repo root).
        """
        result = subprocess.run(
            ["git", "-C", self.git_tempdir, "status", "--porcelain", "--untracked-files=all"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        paths = []
        for line in result.stdout.decode('utf-8', errors='replace').splitlines():
            if len(line) < 4:
                continue
            path = line[3:]
            if ' -> ' in path:  # renamed: keep the new path
                path = path.split(' -> ', 1)[1]
            path = path.strip().strip('"')
            if path:
                paths.append(path)
        return paths

    @staticmethod
    def _is_test_path(path):
        """
        Return True if the path looks like a test or scratch file (tests, brute-force, stress, samples).
        """
        normalized = path.replace('\\', '/')
        parts = [p for p in normalized.split('/') if p]
        if not parts:
            return False
        basename = parts[-1]
        dirs = parts[:-1]
        if any(d in ('tests', 'test') for d in dirs):
            return True
        if fnmatch.fnmatch(basename, 'test_*.py') or fnmatch.fnmatch(basename, '*_test.py'):
            return True
        if any(basename.startswith(prefix) for prefix in ('brute', 'stress', 'sample')):
            return True
        if 'test' in basename:
            return True
        return False

    def _has_valid_patch(self):
        """
        A valid patch is non-empty and touches at least one file that is not a test/scratch file.
        """
        diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        if not diff.strip():
            return False
        changed = self._changed_files()
        return any(not self._is_test_path(p) for p in changed)

    def _patch_status_description(self):
        diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        if not diff.strip():
            return "empty"
        return "test-only"

    MAX_TARGET_CHARS = 8000

    @staticmethod
    def _block_field(block, key):
        if isinstance(block, dict):
            return block.get(key)
        return getattr(block, key, None)

    @classmethod
    def _message_has_content(cls, msg):
        """
        Return True if an assistant message has non-empty text or a tool_use block.
        """
        content = cls._block_field(msg, 'content') if not isinstance(msg, dict) else msg.get('content')
        if isinstance(content, str):
            return bool(content.strip())
        if not isinstance(content, list):
            return False
        for block in content:
            btype = cls._block_field(block, 'type')
            if btype == 'tool_use':
                return True
            if btype == 'text':
                text = cls._block_field(block, 'text')
                if isinstance(text, str) and text.strip():
                    return True
        return False

    @classmethod
    def _sanitize_history(cls, msg_history):
        """
        Remove trailing assistant messages that have no non-empty text and no tool_use.
        Returns [] if nothing meaningful remains.
        """
        if not isinstance(msg_history, list):
            return []
        history = list(msg_history)
        while history:
            last = history[-1]
            role = last.get('role') if isinstance(last, dict) else getattr(last, 'role', None)
            if role == 'assistant' and not cls._message_has_content(last):
                history.pop()
            else:
                break
        if not history:
            return []
        return history

    @staticmethod
    def _summarize_last_assistant(msg_history):
        if not isinstance(msg_history, list):
            return "no history"
        for msg in reversed(msg_history):
            role = msg.get('role') if isinstance(msg, dict) else getattr(msg, 'role', None)
            if role == 'assistant':
                content = msg.get('content') if isinstance(msg, dict) else getattr(msg, 'content', None)
                text = str(content)
                return f"len={len(text)} preview={text[:200]!r}"
        return "no assistant message"

    def _safe_chat(self, prompt, history):
        """
        Call chat_with_agent without letting exceptions abort the run.
        Returns the sanitized resulting history, or the previous history on failure.
        """
        previous = self._sanitize_history(history)
        try:
            result = chat_with_agent(prompt, model=self.code_model, msg_history=history, logging=safe_log)
            return self._sanitize_history(result)
        except Exception:
            import traceback
            safe_log(
                "chat_with_agent raised an exception:\n" + traceback.format_exc(),
                level=logging.ERROR,
            )
            safe_log(
                f"History length at failure: {len(history) if isinstance(history, list) else 'n/a'}; "
                f"last assistant: {self._summarize_last_assistant(history)}",
                level=logging.ERROR,
            )
            return previous

    SAMPLE_INPUT_RE = re.compile(
        r'Sample Input\s*\d*\s*:?[ \t]*\n(.*?)(?=\n\s*Sample Output|\n\s*Output\b|\Z)',
        re.DOTALL | re.IGNORECASE,
    )
    STARTUP_ERROR_MARKERS = (
        'ImportError', 'ModuleNotFoundError', 'SyntaxError', 'IndentationError',
        'NameError',
    )

    def _parse_sample_input(self):
        """
        Extract the first 'Sample Input' block from the problem statement, or None.
        """
        m = self.SAMPLE_INPUT_RE.search(self.problem_statement or '')
        if not m:
            return None
        lines = [ln for ln in m.group(1).splitlines() if not ln.strip().startswith('```')]
        text = '\n'.join(lines).strip()
        return text + '\n' if text else None

    def _smoke_check(self):
        """
        Run the target solution file once with the first parsed sample input (or empty input
        if none can be parsed). Returns (ok, report) where report holds returncode, stdout, stderr.
        Class-based tasks are checked by importing the module instead.
        """
        target_path, target_content = self._find_target_file()
        if target_path is None:
            return True, "No target file found; smoke check skipped."

        if target_content and 'class Solution' in target_content:
            code = (
                "import importlib.util, sys\n"
                "spec = importlib.util.spec_from_file_location('solution', sys.argv[1])\n"
                "mod = importlib.util.module_from_spec(spec)\n"
                "spec.loader.exec_module(mod)\n"
            )
            cmd = [sys.executable, "-c", code, target_path]
            sample_input = ""
            has_sample = False
        else:
            cmd = [sys.executable, target_path]
            sample_input = self._parse_sample_input()
            has_sample = sample_input is not None
            if not has_sample:
                sample_input = ""

        try:
            proc = subprocess.run(
                cmd,
                input=sample_input,
                capture_output=True,
                text=True,
                timeout=20,
                cwd=self.git_tempdir,
            )
        except subprocess.TimeoutExpired as e:
            # A slow solution is not a crash; do not treat timeout as a startup failure.
            out = e.stdout.decode('utf-8', 'replace') if isinstance(e.stdout, bytes) else (e.stdout or '')
            err = e.stderr.decode('utf-8', 'replace') if isinstance(e.stderr, bytes) else (e.stderr or '')
            return True, f"Timed out after 20s (not treated as a crash).\nstdout:\n{out}\nstderr:\n{err}"

        report = (
            f"returncode: {proc.returncode}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}"
        )
        if has_sample:
            ok = proc.returncode == 0 and 'Traceback' not in proc.stderr
        else:
            # Empty input may legitimately hit input()/EOF; only startup-type errors are failures.
            startup_failure = proc.returncode != 0 and any(m in proc.stderr for m in self.STARTUP_ERROR_MARKERS)
            ok = not startup_failure
        return ok, report

    def _find_target_file(self):
        """
        Locate the primary non-test .py file in git_tempdir (solution.py, a class Solution file,
        or a file with a TODO/pass stub). Returns (abs_path, content) or (None, None).
        """
        try:
            result = subprocess.run(
                ["git", "-C", self.git_tempdir, "ls-files"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            tracked = result.stdout.decode('utf-8', errors='replace').splitlines()
        except Exception:
            tracked = []

        candidates = []
        for rel in tracked:
            rel = rel.strip()
            if not rel.endswith('.py') or self._is_test_path(rel):
                continue
            full = os.path.join(self.git_tempdir, rel)
            try:
                with open(full, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
            except OSError:
                continue
            basename = os.path.basename(rel)
            if basename == 'solution.py':
                priority = 0
            elif 'class Solution' in content:
                priority = 1
            elif 'TODO' in content or re.search(r'^\s*pass\s*$', content, re.MULTILINE):
                priority = 2
            else:
                continue
            candidates.append((priority, rel, full, content))

        if not candidates:
            return None, None
        candidates.sort(key=lambda c: (c[0], c[1]))
        _, _, full, content = candidates[0]
        if len(content) > self.MAX_TARGET_CHARS:
            content = content[:self.MAX_TARGET_CHARS] + "\n... [truncated]"
        return full, content

    def _patch_outcome(self):
        if self._has_valid_patch():
            return "valid"
        return self._patch_status_description()

    def forward(self):
        """
        The forward function for the AgenticSystem.
        """
        target_path, target_content = self._find_target_file()
        if target_path is None:
            target_desc = (
                f"No obvious starter file was found in {self.git_tempdir}; create the solution file "
                f"(e.g. {self.git_tempdir}/solution.py) with the editor tool."
            )
        else:
            target_desc = (
                f"Edit this file: {target_path}. Current content:\n"
                f"```python\n{target_content}\n```\n"
                f"You must modify this file with the editor tool."
            )
        is_class_based = bool(target_content and 'class Solution' in target_content)
        if is_class_based:
            verify_hint = (
                "This is a class-based task: verify by importing the Solution class through a bash command "
                "(e.g. python3 -c \"from solution import Solution; ...\" run from the repo directory) "
                "instead of run_samples, which only feeds stdin to a script."
            )
        else:
            verify_hint = (
                "Verify with run_samples on every sample you extracted (it runs the file via stdin)."
            )

        instruction = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

{target_desc}

Steps:
1. Write a working draft of the solution into the file above with the editor tool right away.
2. Then verify it: {verify_hint} Check every sample from the problem statement and match the expected output exactly.
3. If anything fails, fix the file and re-verify. Optionally write a brute-force checker and a random stress test in a separate non-solution file (e.g. under tests/) and compare.
4. Do not only edit test or scratch files; the solution file must contain the final implementation.
5. Only the Python standard library is guaranteed to be installed; do not import numpy/scipy etc. unless you have run an import to confirm it works.
"""

        safe_log("Attempt 0: initial call to coding agent")
        msg_history = self._safe_chat(instruction, [])
        safe_log(f"Attempt 0 outcome: {self._patch_outcome()}")

        for attempt in range(3):
            if self._has_valid_patch():
                safe_log(f"Patch check before retry {attempt}: valid")
                break
            safe_log(f"Retry {attempt}: outcome={self._patch_outcome()}; starting fresh history")
            target_hint = (
                f"Target file: {target_path}\nCurrent content:\n```python\n{target_content}\n```\n"
                if target_path else
                f"Target file: create the solution file in {self.git_tempdir}.\n"
            )
            if attempt == 0:
                extra = "Write a correct, efficient solution."
            elif attempt == 1:
                extra = "Write the simplest correct solution, even if brute force."
            else:
                extra = "Write the simplest correct solution, even if brute force. Do not analyze further; write it now."
            prompt = (
                f"Solve this programming problem.\n\n<problem_description>\n{self.problem_statement}\n</problem_description>\n\n"
                f"{target_hint}\n"
                f"Call the editor tool now to write the full solution into this file; do not reply with text only. "
                f"{extra}"
            )
            msg_history = self._safe_chat(prompt, [])
            safe_log(f"Retry {attempt} outcome: {self._patch_outcome()}")

        smoke_ok = None
        for smoke_attempt in range(3):
            smoke_ok, smoke_report = self._smoke_check()
            safe_log(f"Smoke check {smoke_attempt}: {'passed' if smoke_ok else 'FAILED'}")
            if smoke_ok:
                break
            safe_log(f"Smoke check report:\n{smoke_report}")
            msg_history = self._safe_chat(
                f"Running your solution produced this error:\n{smoke_report}\n"
                f"Fix solution.py (the standard library only if a module is missing), then re-run the samples.",
                msg_history,
            )
        smoke_status = "passed" if smoke_ok else "FAILED"

        if self._has_valid_patch():
            safe_log(f"Agent finished with a valid patch (smoke check: {smoke_status})")
        else:
            safe_log(
                "LAST RESORT: model still made no valid non-test edit after retries; final outcome: "
                f"{self._patch_outcome()} (smoke check: {smoke_status})",
                level=logging.WARNING,
            )

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

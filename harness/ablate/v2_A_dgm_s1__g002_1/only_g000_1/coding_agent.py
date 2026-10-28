import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import sys
import threading

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

    def _changed_files(self, diff):
        """
        Parse the file paths touched by a git diff (from 'diff --git a/X b/X' lines).
        """
        if not diff:
            return []
        paths = []
        for match in re.finditer(r'^diff --git a/(.+?) b/(.+)$', diff, flags=re.MULTILINE):
            path = match.group(2).strip()
            if path not in paths:
                paths.append(path)
        return paths

    def _is_test_file(self, path):
        """
        Heuristically decide whether a path refers to a test file.
        """
        lowered = path.lower().replace('\\', '/')
        parts = lowered.split('/')
        basename = parts[-1]
        stem = basename.rsplit('.', 1)[0]
        if 'test' in basename:
            return True
        if 'tests' in parts[:-1]:
            return True
        if '.spec.' in basename:
            return True
        if stem.endswith('_test'):
            return True
        return False

    def _has_source_edit(self):
        """
        True only if the current diff is non-empty and touches at least one non-test file.
        """
        diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        if not diff.strip():
            return False
        return any(not self._is_test_file(p) for p in self._changed_files(diff))

    def _current_diff(self):
        return str(diff_versus_commit(self.git_tempdir, self.base_commit))

    def _python_compile_errors(self, diff):
        """
        For Python tasks, run `python -m py_compile` on changed non-test .py files.
        Returns raw error text (empty string if everything compiles).
        """
        if self.language != 'python':
            return ''
        errors = []
        for path in self._changed_files(diff):
            if not path.endswith('.py') or self._is_test_file(path):
                continue
            full_path = os.path.join(self.git_tempdir, path)
            if not os.path.exists(full_path):
                continue
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', full_path],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
            )
            if result.returncode != 0:
                errors.append(result.stdout.decode('utf-8', errors='replace'))
        return '\n'.join(errors).strip()

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
IMPORTANT: You must act through tools. Use the editor tool and the bash tool to write code. A reply that contains only text and no tool calls is a failure and will not be graded.

Follow this workflow:
(a) Explore the repository with the tools: list files, read the relevant existing code, any examples, and any tests.
(b) Think through the algorithm or the fix carefully, including edge cases and constraints.
(c) Actually write or modify the source files using the editor tool (or bash). The solution must live in the source code, NOT only in test files. If the task names a file (for example solution.py), create it at {self.git_tempdir}/solution.py exactly.
(d) Run and test the code with bash. Write small tests of your own for the examples and edge cases. For interactive problems, write a small mock judge script that feeds input to your program and checks its output, and run your solution against it.
(e) Verify that every required file exists and is non-empty, and that the code compiles and runs. Fix any problems you find and repeat (d) and (e).

Finish only when the required source file(s) contain your complete solution."""
        init_edit = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)

        # Patch verification with a bounded retry loop
        for attempt in range(3):
            if self._has_source_edit():
                break
            current_diff = self._current_diff()
            diff_text = current_diff if current_diff.strip() else "(empty diff)"
            safe_log(f"[retry {attempt + 1}] No valid source edits detected; diff: {diff_text[:500]}")
            retry_prompt = f"""{task}
The previous attempt produced no source-code edits. The current repository diff is:
{diff_text}

Only test files, or nothing at all, were changed. This is not acceptable. Immediately use the editor tool (or bash) to write the complete solution into the proper source file (for example {self.git_tempdir}/solution.py if the task names that file). Do not reply with text only. After writing, run the code with bash to verify it, then finish."""
            init_edit = chat_with_agent(retry_prompt, model=self.code_model, msg_history=[], logging=safe_log)

        # Optional sanity check for Python: compile changed non-test files, feed raw errors back once
        if self._has_source_edit():
            compile_errors = self._python_compile_errors(self._current_diff())
            if compile_errors:
                safe_log(f"py_compile errors:\n{compile_errors}")
                fix_prompt = f"""{task}
Your current solution fails to compile with `python -m py_compile`. The raw error output is:
{compile_errors}

Use the editor tool to fix these errors in the source file(s), then verify by running the code with bash."""
                init_edit = chat_with_agent(fix_prompt, model=self.code_model, msg_history=[], logging=safe_log)
            else:
                safe_log("py_compile check passed for changed non-test files.")
        else:
            safe_log("No valid source edits after retries; skipping py_compile check.")

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

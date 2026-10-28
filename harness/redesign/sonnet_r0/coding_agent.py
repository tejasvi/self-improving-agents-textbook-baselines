import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
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

    def _has_edits(self):
        try:
            diff = diff_versus_commit(self.git_tempdir, self.base_commit)
            return bool(str(diff).strip())
        except Exception as e:
            safe_log(f"Error computing diff: {e}")
            return False

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
        workflow = f"""
Follow this workflow. The solution file is in {self.git_tempdir} (normally `solution.py`); the hidden tests are run against it, so the work is only counted if the file is actually written.

1. Look at the repository quickly (`ls {self.git_tempdir}` and `cat` the starter file). Do NOT run `find` over large trees; keep every shell command short.
2. Think carefully about the problem: restate it, derive constraints on complexity (e.g. n up to 1e5 / 1e6 needs O(n log n) or O(n) in Python; use fast input via sys.stdin, avoid recursion depth issues - use iterative algorithms or raise the recursion limit and avoid deep recursion). Work out the algorithm by hand against the examples before coding.
3. WRITE A FIRST COMPLETE SOLUTION TO THE SOLUTION FILE EARLY (even if it is a simple correct baseline), using the editor tool. For a "complete program" task the file must read stdin and print to stdout. For a `Solution` class task keep the class/method signature from the starter code, and add the needed imports at the top (e.g. `from typing import List`, `import heapq`, `from collections import defaultdict`...) because the starter code may lack them. Do not read from stdin for class tasks.
4. Test it: write a small test runner (in /tmp, not in the repo) running all the sample inputs from the problem statement and compare with the expected outputs. Always use `timeout 20 python3 ...` when running programs.
5. Write a brute-force solution (in /tmp) that is obviously correct for small inputs, generate many random small inputs, and compare it to your solution (stress test). Fix any discrepancies. Think about edge cases (n=1, all equal, negatives, maximum values, big numbers).
6. Test performance with maximum-size inputs (generate them in /tmp) and make sure the run time is well within a few seconds; optimize if not.
7. Finish only when the solution file contains your final, tested solution. Keep helper/test files out of the repo directory.

If your reasoning about the best algorithm is not converging, still write the best correct (possibly slower) solution you have into the file first, then improve it. Never end your turn without having written the solution file.
"""
        instruction = f"{task}\n{workflow}\nPlease analyze the problem description carefully. Then make edits to the code files to complete the instruction."

        # Main attempt
        try:
            chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        except Exception as e:
            safe_log(f"Error in main attempt: {e}")

        # If no solution was written, retry (bounded) with fresh context
        for attempt in range(3):
            if self._has_edits():
                break
            retry_instruction = f"""{task}
NOTE: A previous attempt ended without writing any solution; the repository in {self.git_tempdir} is still unchanged (or the solution file is still the starter stub). You MUST use the editor/bash tools to write a complete solution into the solution file in this attempt. Begin by looking at the starter file with `cat`, then briefly reason about the algorithm, then write the file IMMEDIATELY with a correct solution (a simple correct baseline is fine), and only afterwards test and improve it.
{workflow}"""
            try:
                chat_with_agent(retry_instruction, model=self.code_model, msg_history=[], logging=safe_log)
            except Exception as e:
                safe_log(f"Error in retry attempt {attempt}: {e}")

        # Verification pass with fresh context (only if something was written)
        if self._has_edits():
            review_instruction = f"""{task}
A solution has already been written into the repository in {self.git_tempdir}. Your job now is to rigorously verify and, if necessary, fix it.

Steps:
1. `cat` the current solution file and understand it.
2. Run it on all the sample inputs from the problem statement (use `timeout 20 python3 ...`; put test scripts in /tmp, not in the repo).
3. Write an obviously-correct brute force solution in /tmp and stress test the solution against it on many random small inputs, including edge cases. If there is any mismatch or crash, find the bug and fix the solution file.
4. Test with maximum-size inputs for performance (must run in a few seconds in Python); optimize if needed (fast IO, avoid recursion, avoid O(n^2)).
5. Make sure the solution file keeps the required interface (complete stdin/stdout program, or the `Solution` class method with required imports like `from typing import List`).
Do not leave helper files in the repo. If the solution is already correct and fast, leave it unchanged."""
            try:
                chat_with_agent(review_instruction, model=self.code_model, msg_history=[], logging=safe_log)
            except Exception as e:
                safe_log(f"Error in review pass: {e}")

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

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
    os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)
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


WORKFLOW_GUIDE = """
# How to work

You are solving a competitive programming problem in Python. Hidden tests (including large, adversarial and edge-case inputs) will be used to judge your solution, so correctness AND efficiency both matter. Work methodically:

1. **Explore the repository first.** List the directory `{git_dir}` and read the existing files to find out where the solution must be written (e.g. an existing stub file, a `Solution` class with a given method signature, or a script that reads stdin and writes stdout). Respect the exact file name, class name, method name and signature that are expected. Do NOT modify or delete any provided test files.

2. **Understand the problem precisely.** Re-read the statement. Note the input/output format exactly, all constraints (sizes, value ranges), and special cases (n = 0/1, duplicates, negative numbers, overflow-free big values, empty strings, multiple test cases, etc.). Work through the provided examples by hand to make sure your understanding matches the expected outputs.

3. **Design an algorithm that fits the constraints.** Estimate the complexity. Assume pure Python performs roughly 10^7 simple operations per second at best, so e.g. n = 2*10^5 typically needs O(n log n) or better. Think about the correct technique (greedy with proof, DP, binary search, graphs, two pointers, prefix sums, segment/Fenwick trees, number theory, etc.). If unsure about correctness of a greedy idea, verify it against brute force.

4. **Implement the solution** in the correct file. Python-specific guidelines:
   - For stdin programs: read all input fast (`data = sys.stdin.buffer.read().split()`), and write output once (`sys.stdout.write("\\n".join(...))`). Print exactly the required format.
   - Avoid deep recursion (convert to iterative), or if recursion is unavoidable, raise `sys.setrecursionlimit` and run in a `threading.Thread` with a larger `threading.stack_size`.
   - Avoid unnecessary object creation in hot loops; prefer local variables, lists over dicts where possible, and built-ins (sorted, heapq, bisect, itertools, collections).
   - For `Solution` class tasks: keep the exact method signature, include required imports (e.g. `from typing import List, Optional`, `import heapq`, `from collections import ...`) at the top of the file, and do not read stdin or print anything.

5. **Test thoroughly** using the bash tool:
   - Run the solution on every example from the statement and compare outputs exactly.
   - Write a simple, obviously-correct brute-force solution and a random small-input generator, then run a stress test comparing both on hundreds of random cases. Fix any mismatch.
   - Generate a maximum-size (worst-case) input and time your solution (`time python3 sol.py < big.txt`). Optimize if it is too slow.
   - Check edge cases explicitly (minimum sizes, all-equal values, extreme values).
   - If the repository contains its own tests, run them too.
   - Put all scratch files (brute force, generators, test inputs) in `/tmp`, NOT inside `{git_dir}`, so that they don't pollute the final solution.

6. **Finish cleanly.** Make sure the final solution file in `{git_dir}` contains only the final, clean solution (no debug prints), then re-run the examples one last time.

Tool notes: each bash call runs in a fresh shell (use absolute paths or `cd <dir> && ...`). Standard input of commands is empty unless you redirect it (e.g. `python3 sol.py < /tmp/in.txt` or `echo "..." | python3 sol.py`). Use the editor tool's `str_replace` for targeted edits and `create`/`edit` for whole files.
"""


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

    def _current_diff(self):
        try:
            return str(diff_versus_commit(self.git_tempdir, self.base_commit))
        except Exception as e:
            safe_log(f"Error computing diff: {e}")
            return ""

    def _test_section(self):
        if self.test_description:
            return f"\n<test_description>\n{self.test_description}\n</test_description>\n"
        return ""

    def forward(self):
        """
        The forward function for the AgenticSystem.
        """
        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>
{self._test_section()}
Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        guide = WORKFLOW_GUIDE.format(git_dir=self.git_tempdir)
        instruction = f"{task}\n{guide}\n\nPlease analyze the problem description carefully, then implement, test, and refine your solution following the steps above."

        try:
            chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        except Exception as e:
            safe_log(f"Error in first pass: {e}")

        diff = self._current_diff()
        if not diff.strip():
            # Nothing was produced; try once more from scratch.
            safe_log("No edits produced in first pass; retrying.")
            try:
                chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
            except Exception as e:
                safe_log(f"Error in retry pass: {e}")
            return

        # Verification / refinement pass with fresh context
        review = f"""I have uploaded a code repository in the directory {self.git_tempdir}. A solution has already been written for the following problem, but it has not been independently verified.

<problem_description>
{self.problem_statement}
</problem_description>
{self._test_section()}
<current_edits>
{diff}
</current_edits>

Your job is to act as a strict reviewer and tester, and fix the solution in {self.git_tempdir} if anything is wrong:
1. Re-read the problem and check that the solution's file location, class/method signature and I/O format exactly match what is required.
2. Check the algorithm's correctness (think about counterexamples) and its time complexity against the constraints in Python.
3. Run all examples from the statement. Write a brute-force solution and a random generator in /tmp and stress test on many small random cases. Time the solution on a maximum-size worst-case input.
4. If you find any bug, wrong output, or performance problem, fix the solution (rewrite with a better algorithm if needed) and re-test.
5. Keep scratch files in /tmp only; leave only the clean final solution in {self.git_tempdir}.
If everything is verified correct and fast enough, make no further changes and briefly state that it is verified.

Tool notes: each bash call runs in a fresh shell (use absolute paths). Standard input of commands is empty unless you redirect it.
"""
        try:
            chat_with_agent(review, model=self.code_model, msg_history=[], logging=safe_log)
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

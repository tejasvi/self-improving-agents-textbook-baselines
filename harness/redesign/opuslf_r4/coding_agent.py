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
# How to work (follow these steps carefully)

## 1. Explore
- List the files in {repo} (e.g. `ls -la {repo}` / `find {repo} -not -path '*/.git*'`) and read any existing files. There may be a stub, a starter `Solution` class, or a file that is clearly meant to hold the solution.
- Determine the required form of the answer:
  * A complete program reading standard input and writing standard output, OR
  * A method of a given `Solution` class. In that case keep the class name, method name, parameter names/order and signature EXACTLY as given.
- If the repository already contains a file intended for the solution, write your solution there. If the problem statement names a file, use that. Otherwise create `{repo}/solution.py`.

## 2. Analyze before coding
- Re-read the statement carefully: input format, output format (exact spacing, case, precision, "-1"/"NO" conventions), multiple test cases, constraints.
- Derive an algorithm whose complexity fits the constraints. Plain Python does roughly 10^7 simple operations per second; aim for well under that for the worst case. Think about the correct approach (greedy proof, DP, graph algorithm, binary search, math, data structures, etc.) and verify it by hand on the examples before writing code.
- List tricky edge cases: minimum sizes (n=1, empty), maximum sizes, all-equal values, negative numbers, overflow-free big ints, duplicates, disconnected graphs, etc.

## 3. Implement
- For stdin programs: read all input fast (`data = sys.stdin.buffer.read().split()`), build output in a list and print once with `'\\n'.join(...)`. Wrap logic in `main()` and call it.
- Avoid deep recursion (rewrite iteratively, or use an explicit stack). If recursion is unavoidable, raise the recursion limit and run in a thread with a larger stack size.
- For `Solution` classes: include the imports you need at the top of the file (e.g. `from typing import List, Optional`, `import collections`, `import heapq`, `from functools import lru_cache`), and do not read stdin or print anything.
- Do not leave debug prints in the final solution.

## 4. Test thoroughly (this is essential)
- Put ALL scratch files (tests, brute force, generators, harnesses) in /tmp, NEVER inside {repo}. Only the final solution should be changed in {repo}.
- Run the solution on every example from the statement and compare to the expected output exactly (e.g. `python3 sol.py < /tmp/in1.txt` and `diff`). For a `Solution` class, write a small harness in /tmp that imports the file (add the repo to sys.path) and calls the method on the examples.
- Write a simple, obviously-correct brute-force solution in /tmp, plus a random small-input generator, and run a stress-test loop (hundreds of random cases, bounded with a `for` loop) comparing the two. If they ever differ, minimize the failing case, understand the bug, and fix it.
- Generate a worst-case (maximum constraints) input and time the solution (`time python3 ...`). If it is too slow, optimize the algorithm or the constant factor.
- Re-run all tests after every fix.

## 5. Finish
- Make sure the final file in {repo} contains only the clean, final solution and that no scratch files are left in {repo}.
- Briefly summarize the algorithm, its complexity, and what tests you ran.
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

    def _base_context(self):
        ctx = f"""I have uploaded a code repository in the directory {self.git_tempdir}. It is used to solve a competitive programming problem in Python.

<problem_description>
{self.problem_statement}
</problem_description>
"""
        if self.test_description:
            ctx += f"\n<test_description>\n{self.test_description}\n</test_description>\n"
        return ctx

    def _solve(self):
        instruction = (
            self._base_context()
            + f"\nYour task is to write a correct and efficient Python solution to the <problem_description> and save it in the {self.git_tempdir} directory. "
            "I have already taken care of the required dependencies. The solution will be judged on hidden tests (including large, worst-case inputs), "
            "so correctness on all edge cases and speed both matter.\n"
            + WORKFLOW_GUIDE.format(repo=self.git_tempdir)
        )
        try:
            chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        except Exception as e:
            safe_log(f"Error during solve phase: {e}")

    def _verify(self, diff):
        instruction = (
            self._base_context()
            + f"""
A previous attempt has already written a solution in {self.git_tempdir}. Here are the current changes relative to the original repository:

<current_changes>
{diff}
</current_changes>

Your task: act as a skeptical reviewer and make sure this solution is CORRECT and FAST ENOUGH for the hidden tests, fixing it if needed.

1. Re-read the problem statement carefully and check that the solution matches the required form (stdin/stdout program vs. exact `Solution` class/method signature) and the exact output format.
2. Independently think about the right algorithm and whether the implemented one is correct for all cases and within the time limits for the maximum constraints.
3. In /tmp (never inside {self.git_tempdir}), run the statement examples, write an independent brute-force solution and a random small-case generator, and run a bounded stress test comparing them. Also time a worst-case input.
4. If you find any bug, wrong output format, or performance issue, fix the solution file in {self.git_tempdir} and re-test everything. Only change the solution when you have evidence (a failing test or a clear complexity problem); do not rewrite a working solution needlessly.
5. Ensure no scratch/test files are left in {self.git_tempdir} and no debug prints remain in the solution.
"""
            + WORKFLOW_GUIDE.format(repo=self.git_tempdir)
        )
        try:
            chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        except Exception as e:
            safe_log(f"Error during verify phase: {e}")

    def forward(self):
        """
        The forward function for the AgenticSystem.
        """
        # Phase 1: solve (retry once if nothing was produced)
        for attempt in range(2):
            safe_log(f"\n===== Solve phase, attempt {attempt + 1} =====")
            self._solve()
            if self._current_diff().strip():
                break

        # Phase 2: independent verification with fresh context
        diff = self._current_diff()
        if diff.strip():
            safe_log("\n===== Verification phase =====")
            self._verify(diff)

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

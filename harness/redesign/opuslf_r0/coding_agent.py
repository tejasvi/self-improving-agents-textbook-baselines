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


WORKFLOW_GUIDE = """
## How to work (follow these steps carefully)

1. **Explore the repository first.** Use the `editor` tool (`view` on the directory) or `bash` (`ls -la`, `cat`) to find the file(s) where the solution must go. If the problem statement names a file, use exactly that file. If there is an existing stub (e.g. a `Solution` class skeleton), keep its class name, method name and signature EXACTLY.
2. **Determine the task form.**
   - *Standard I/O program*: read everything from standard input and write the answer to standard output. Never read from files, never print prompts or debug text. Follow the output format exactly.
   - *`Solution` class method*: implement the method of the given `Solution` class; do NOT read stdin or print. Include all needed imports at the top of the file (e.g. `from typing import List, Optional`, `import heapq`, `from collections import defaultdict`, ...). Keep any given helper classes (ListNode, TreeNode, ...) consistent with the statement.
3. **Analyze before coding.** Write down the constraints and derive an algorithm whose complexity fits them. Python does roughly 10^7 simple operations per second, so with n = 2*10^5 aim for O(n log n) or better; with n <= 20 exponential may be OK, and so on. Think about tricky cases: n = 0/1, all-equal values, negative numbers, overflow-free big numbers, duplicates, disconnected graphs, multiple test cases per input, etc. Re-read the statement to make sure you understood it — misreading is the most common cause of wrong answers. Verify your idea by hand on the provided examples before implementing.
4. **Implement efficiently in Python.**
   - Fast input: `data = sys.stdin.buffer.read().split()` and an index pointer; build output in a list and `sys.stdout.write("\\n".join(...))`.
   - Avoid deep recursion (Python default limit is 1000): prefer iterative DFS/BFS; if recursion is unavoidable, raise `sys.setrecursionlimit` and run inside `threading.Thread` with a larger `threading.stack_size`.
   - Prefer local variables inside a `main()` function, avoid repeated attribute lookups in hot loops, use built-ins / sorting / heapq / bisect / arrays smartly.
5. **Test against the examples.** Run your solution on every example in the statement and compare outputs exactly. The `run_solution` tool runs a Python program with given stdin and optional expected output and reports PASS/FAIL and run time. For `Solution` class tasks, write a small harness script in /tmp that imports/execs the solution file and calls the method on the examples.
6. **Stress test.** For non-trivial problems, write a simple brute-force solution and a random small-input generator in /tmp, and compare your solution against the brute force on hundreds of random cases (a short bash or Python loop). Fix any discrepancy and re-test.
7. **Test performance.** Generate a maximum-size input (in /tmp) and time your solution; optimize if it is too slow (target well under the limit, typically < 1-2 seconds).
8. **Clean up.** The final solution file must contain only the solution (no debug prints, no hardcoded test input). Put all scratch files (brute force, generators, harnesses, test inputs) in /tmp, NOT in the repository — any file left in the repository becomes part of the submission.
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

    def forward(self):
        """
        The forward function for the AgenticSystem.
        """
        test_info = ""
        if self.test_description:
            test_info = f"\n<test_description>\n{self.test_description}\n</test_description>\n"

        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following competitive programming problem (language: Python).

<problem_description>
{self.problem_statement}
</problem_description>
{test_info}
Your task is to make changes to the files in the {self.git_tempdir} directory so that they contain a correct and efficient solution to the <problem_description>. I have already taken care of the required dependencies. The solution will be judged on hidden tests (including large and tricky edge cases), so correctness on all cases and speed both matter.
"""
        instruction = f"{task}\n{WORKFLOW_GUIDE}\nStart by exploring {self.git_tempdir}, then analyze the problem carefully, implement, and test thoroughly. When you are confident the solution is correct and fast, give a short summary of the approach."

        try:
            chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        except Exception as e:
            safe_log(f"Error in solving phase: {e}")

        # Verification / refinement phase with a fresh context
        try:
            diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        except Exception as e:
            diff = f"(could not compute diff: {e})"
        if not diff.strip():
            diff = "(no edits have been made yet — the problem still needs to be solved from scratch)"
        if len(diff) > 40000:
            diff = diff[:40000] + "\n...(diff truncated; inspect the files directly)..."

        review = f"""{task}
A previous attempt has produced the following edits to the repository (git diff versus the original):

<current_edits>
{diff}
</current_edits>

Act as a meticulous reviewer and finisher. Your job:
1. Re-read the problem statement carefully and check that the solution solves exactly the stated problem (input/output format, multiple test cases, indexing, required output formatting, the exact class/method signature if a `Solution` class is required).
2. Run the solution on all examples from the statement and confirm the outputs match exactly.
3. Independently think about edge cases and worst-case complexity. Write a brute force in /tmp and stress test on many random small inputs; generate a maximum-size input and check the run time.
4. If anything is wrong, slow, or missing, fix it (or rewrite the solution with a better algorithm). If no solution exists yet, write one.
5. Make sure no scratch/test files are left inside {self.git_tempdir} (only the solution file(s) should be changed), and that the solution has no debug output.
{WORKFLOW_GUIDE}
Finish with a brief summary of what you verified or changed."""

        try:
            chat_with_agent(review, model=self.code_model, msg_history=[], logging=safe_log)
        except Exception as e:
            safe_log(f"Error in review phase: {e}")

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

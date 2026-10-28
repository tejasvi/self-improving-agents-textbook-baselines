import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import threading

from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
from utils.git_utils import diff_versus_commit, reset_to_commit, apply_patch

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
    return getattr(thread_local, 'logger', None)

def set_thread_logger(logger):
    thread_local.logger = logger

def setup_logger(log_file='./chat_history.md', level=logging.INFO):
    logger = logging.getLogger(f'AgenticSystem-{threading.get_ident()}')
    logger.setLevel(level)
    logger.handlers = []
    file_formatter = logging.Formatter('%(message)s')
    os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    set_thread_logger(logger)
    return logger

def safe_log(message, level=logging.INFO):
    logger = get_thread_logger()
    if logger:
        logger.log(level, message)
    else:
        print(f"Warning: No logger found for thread {threading.get_ident()}")


GUIDELINES = """
<guidelines>
## Workflow (follow these steps)
1. **Explore**: List the repository directory and view the existing files to find where the solution must go (e.g. an existing stub file, a `Solution` class, or a file that should contain a complete stdin/stdout program). Keep the existing file name, function/class names and signatures exactly.
2. **Understand**: Re-read the problem statement carefully. Note the exact input/output format, all constraints (sizes, value ranges), and corner cases (n = 1, empty, equal values, negative numbers, very large values, modulo requirements, multiple test cases, etc.). Work through the provided examples by hand to confirm your understanding.
3. **Design**: Derive an algorithm whose complexity fits the constraints (assume roughly 10^7 simple Python operations per second). Think about the correct approach before coding: greedy (prove it!), DP, binary search, graphs, number theory, data structures, etc. If unsure about a greedy, verify it against brute force.
4. **Implement**: Write the solution into the correct file in the repository using the editor tool.
5. **Test the examples**: Use the `run_python` tool (or bash) to run the solution on every sample from the statement and compare with the expected output. For a `Solution` class, write a small harness script in /tmp that imports/copies the class and calls the method on the examples.
6. **Stress test**: Write a simple, obviously-correct brute-force solution and a random small-test generator (taking a seed as argv[1]) in /tmp, then use the `stress_test` tool to compare them against your solution on hundreds of random tests. Fix every mismatch you find (the tool shows the failing input).
7. **Performance test**: Generate a maximum-size (worst-case) input and run your solution with a timeout to make sure it runs fast enough (ideally well under ~2 seconds). Optimize if it is too slow.
8. **Finalize**: Make sure the final solution in the repository is the tested version, and that it contains no debug prints.

## Python tips for competitive programming
- For stdin programs read input fast: `import sys; data = sys.stdin.buffer.read().split()` and parse tokens with an index; write output with `sys.stdout.write("\\n".join(...))`.
- Avoid deep recursion (Python's default limit is 1000). Prefer iterative DFS/BFS or explicit stacks. If recursion is unavoidable, raise the recursion limit and run in a thread with a large stack size.
- Prefer local variables inside a `main()` function, list comprehensions, built-ins (sorted, sum, min, max), `heapq`, `bisect`, `collections.deque/Counter/defaultdict`, `itertools`, `functools.lru_cache` (careful with depth).
- Watch out for answers requiring modulo (e.g. 10^9+7) and for exact output formatting (spaces, newlines, precision for floats, "YES"/"Yes" casing).
- For `Solution` class problems: do NOT read stdin or print; just implement the method. Include needed imports (e.g. `from typing import List, Optional`) at the top of the file, and keep any provided helper class definitions (e.g. ListNode, TreeNode) as the stub expects.

## Rules
- Put scratch files (brute force, generators, harnesses, test inputs) in /tmp, NOT in the repository. Only the solution file(s) in the repository should be changed.
- Use absolute paths. Each bash call runs in a fresh shell (cd does not persist).
- Do not stop until the solution passes the examples and the stress tests.
</guidelines>
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

        self.code_model = CLAUDE_MODEL if not self_improve else OPENAI_MODEL

        self.logger = setup_logger(chat_history_file)

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
            safe_log(f"Error getting diff: {e}")
            return ""

    def forward(self):
        """
        The forward function for the AgenticSystem.
        """
        test_info = ""
        if self.test_description:
            test_info = f"\n<test_description>\n{self.test_description}\n</test_description>\n"

        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. It contains a competitive programming task to be solved in Python.

<problem_description>
{self.problem_statement}
</problem_description>
{test_info}
Your task is to write a correct and efficient solution by making changes to the files in the {self.git_tempdir} directory. The solution is either a complete program reading standard input and writing standard output, or a method of a given `Solution` class (check the existing files and the problem statement to decide). Hidden tests will check correctness on many cases, including large worst-case inputs, so both correctness and speed matter.
"""
        instruction = f"{task}\n{GUIDELINES}\nStart by exploring {self.git_tempdir}, then follow the workflow step by step."

        try:
            chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        except Exception as e:
            safe_log(f"Main pass error: {e}")

        # If nothing was written, try once more.
        if not self._current_diff().strip():
            safe_log("No edits after first pass; retrying.")
            try:
                chat_with_agent(instruction + "\n\nIMPORTANT: A previous attempt ended without writing any solution to the repository. Make sure to write the solution file.",
                                model=self.code_model, msg_history=[], logging=safe_log)
            except Exception as e:
                safe_log(f"Retry pass error: {e}")

        # Review / verification pass with fresh context.
        diff = self._current_diff()
        if diff.strip():
            review = f"""{task}
A previous attempt produced the following changes to the repository (git diff versus the original):

<current_edits>
{diff[:30000]}
</current_edits>
{GUIDELINES}
Your job now is to act as a rigorous reviewer and fixer:
1. View the current solution file(s) in {self.git_tempdir}. Re-read the problem statement and check the solution logic against it, especially the input/output format, edge cases and constraints.
2. Run the solution on all examples from the statement.
3. Write an independent brute-force solution and random generator in /tmp and run the `stress_test` tool with many small random tests (include edge cases such as minimum sizes).
4. Run a worst-case maximum-size input to check the running time.
5. If anything fails or is too slow, fix the solution in the repository (or rewrite it with a better algorithm) and re-test. If everything passes, leave it as is.
Remove any scratch files you may have created inside the repository; keep only the solution."""
            try:
                chat_with_agent(review, model=self.code_model, msg_history=[], logging=safe_log)
            except Exception as e:
                safe_log(f"Review pass error: {e}")


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

    agentic_system = AgenticSystem(
        problem_statement=args.problem_statement,
        git_tempdir=args.git_dir,
        base_commit=args.base_commit,
        chat_history_file=args.chat_history_file,
        test_description=args.test_description,
        self_improve=args.self_improve,
        language=args.language,
    )

    agentic_system.forward()

    model_patch = diff_versus_commit(args.git_dir, args.base_commit)
    model_patch_outfile = os.path.join(args.outdir, 'model_patch.diff') if args.outdir else 'model_patch.diff'
    with open(model_patch_outfile, 'w') as f:
        f.write(model_patch)

if __name__ == "__main__":
    main()

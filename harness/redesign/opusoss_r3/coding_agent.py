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


WORKFLOW_GUIDE = """
## How to work (follow these steps)

1. **Inspect** the repository (the starter `solution.py`, any README). Note whether the task is a full stdin/stdout program or a `Solution` class method.
2. **Analyze** the problem: restate it precisely, check the samples by hand, and note the constraints. Choose an algorithm whose complexity fits the constraints *in Python* (roughly <= 10^7 simple operations). Be skeptical of greedy ideas: hard problems usually need DP, data structures (monotonic stacks/deques, Fenwick/segment trees, binary search), math, or careful case analysis. Keep this reasoning reasonably brief — your output per response is limited.
3. **Write the solution file EARLY** with the editor tool (a first correct-looking version is better than nothing; you can refine later). Never end your turn without having written code to the solution file.
   - For `Solution`-class tasks: keep the exact class and method signature, and add the needed imports at the top (e.g. `from typing import List, Optional`, `import heapq`, `from collections import ...`) — the starter code often lacks `from typing import List`, which would crash on import.
   - For stdin/stdout programs: read input fast (`sys.stdin.buffer.read().split()`), print exactly the required output, avoid deep recursion (use iterative code or raise the recursion limit + threading stack size).
4. **Test** using the bash tool. Put all scratch/test files in `/tmp` (NOT in the repository):
   - Run the samples from the statement and compare outputs exactly.
   - Write a simple **brute-force** solution (exhaustive search for tiny inputs) in /tmp and a **random stress test** script that compares the brute force against your solution on hundreds of small random inputs. Fix any mismatch — a mismatch means your algorithm is wrong, rethink it rather than patching special cases.
   - Generate a **maximum-size worst-case input** and time your solution (`time python3 ...`); it should run in well under ~2 seconds. Optimize if needed.
   - For class tasks, test by importing: `cd <repo> && python3 -c "from solution import Solution; print(Solution().method(...))"`.
5. **Finalize**: make sure the solution file contains only the final solution (no debug prints, no reading stdin for class tasks), and that it imports/runs without errors. Then give a short summary.

Notes on tools: each bash call runs in a fresh shell (use `cd` within the same command), commands time out after ~120 s. The editor supports `view`, `create`, `edit` (full overwrite) and `str_replace` (targeted replacement).
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
            safe_log(f"Error computing diff: {e}")
            return ""

    def _run(self, instruction):
        try:
            return chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        except Exception as e:
            safe_log(f"Error in chat_with_agent: {e}")
            return []

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
        instruction = f"{task}\n{WORKFLOW_GUIDE}"
        self._run(instruction)

        # Retry if nothing was written
        for _ in range(2):
            if self._current_diff().strip():
                break
            safe_log("No changes detected; re-prompting the agent.")
            retry_instruction = (
                f"{task}\n{WORKFLOW_GUIDE}\n\n"
                "IMPORTANT: A previous attempt ended WITHOUT writing any solution — the solution file in the "
                "repository is still unchanged. Look at the starter file, then write a complete solution to it with "
                "the editor tool as your very first step (keep reasoning short before writing), then test and refine it."
            )
            self._run(retry_instruction)

        # Verification / refinement round
        diff = self._current_diff()
        if diff.strip():
            review_instruction = f"""{task}
A solution has already been written. Here is the current diff of the repository against the original:

<current_diff>
{diff}
</current_diff>

Your job now is to **verify and, if necessary, fix** this solution. Do not trust it — previous solutions have often been wrong (e.g. an unjustified greedy) or too slow.
1. Re-read the problem and constraints. Check whether the algorithm is actually correct; think of tricky cases.
2. Using the bash tool with scratch files in /tmp only: run the samples, write an independent brute-force solution for tiny inputs, and run a random stress test (hundreds of cases) comparing it with the solution. Also time a maximum-size worst-case input.
3. If you find any mismatch, error, or timeout, fix the solution in the repository (rethink the algorithm if needed) and re-run all tests.
4. If everything passes, leave the solution as is. Make sure the final file imports/runs cleanly (needed imports such as `from typing import List` present, no debug output).
{WORKFLOW_GUIDE}"""
            self._run(review_instruction)


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

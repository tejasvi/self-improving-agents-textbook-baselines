
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
    MAX_ATTEMPTS = 5
    NUDGE_LIMIT = 2
    REPAIR_LIMIT = 2
    CHECK_TIMEOUT = 120  # seconds for running tests

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

    # Helper to determine if there is any git diff compared to base commit
    def _has_progress(self):
        diff = diff_versus_commit(self.git_tempdir, self.base_commit)
        return bool(diff.strip())

    # Helper to run the external test suite and capture result
    def _run_checks(self):
        test_path = '/tmp/agent_tests/run_tests.py'
        if not os.path.exists(test_path):
            return False, 'tests not written'
        try:
            result = subprocess.run(
                ['python', test_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=self.CHECK_TIMEOUT,
                text=True,
                cwd=self.git_tempdir  # ensure repo context if needed
            )
            output = result.stdout
            # Determine pass/fail by looking for a marker; assume the script prints 'ALL CHECKS PASSED' on success
            passed = 'ALL CHECKS PASSED' in output
            # Return only the tail (last 500 chars) to keep size reasonable
            tail = output[-500:]
            return passed, tail
        except subprocess.TimeoutExpired:
            return False, 'tests timed out'
        except Exception as e:
            return False, f'test execution error: {str(e)}'

    # Helper to snapshot current diff and store with result info
    def _snapshot_patch(self, attempts, passed, output_tail):
        diff = diff_versus_commit(self.git_tempdir, self.base_commit)
        attempts.append({
            'diff': diff,
            'passed': passed,
            'output_tail': output_tail,
        })

    # Helper to reset repository to base commit (clean state)
    def _reset(self):
        reset_to_commit(self.git_tempdir, self.base_commit)

    def forward(self):
        """Main orchestrator implementing bounded attempts, progress checks, and test verification."""
        attempts = []
        best_patch = None

        for attempt_idx in range(self.MAX_ATTEMPTS):
            safe_log(f"--- Attempt {attempt_idx + 1} ---")
            # Build the prompt for this attempt
            if attempt_idx == 0:
                instruction = (
                    "You have uploaded a code repository. Solve the problem described below. "
                    "Immediately edit `solution.py` (or the appropriate file) to implement the solution. "
                    "Also create the following test harness files under `/tmp/agent_tests/` with the exact paths: "
                    "`brute.py` (a correct but slow reference), `gen.py` (random test generator), and `run_tests.py` (which runs sample cases, 200 random comparisons, and a performance test). "
                    "After writing those files, run them to verify correctness."
                )
            else:
                # Include prior diff and failing output for context
                prev = attempts[-1]
                instruction = (
                    f"Previous attempt diff:\n{prev['diff']}\n\n"
                    f"Previous test output (first failure):\n{prev['output_tail']}\n\n"
                    "Fix the root cause of the failure instead of adding special‑case code."
                )
            task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

{instruction}
"""
            # Start fresh message history for each attempt
            msg_history = []
            # Initial call
            msg_history = chat_with_agent(task, model=self.code_model, msg_history=msg_history, logging=safe_log)

            # Ensure the assistant actually edited something
            nudges_sent = 0
            while nudges_sent < self.NUDGE_LIMIT and not self._has_progress():
                nudge = "You have not edited the solution file yet. Please use the editor tool now to write the implementation."
                msg_history = chat_with_agent(nudge, model=self.code_model, msg_history=msg_history, logging=safe_log)
                nudges_sent += 1

            # Run checks after initial edit (or after nudges)
            passed, output_tail = self._run_checks()
            self._snapshot_patch(attempts, passed, output_tail)

            # If checks failed, allow repair rounds
            repair_round = 0
            while not passed and repair_round < self.REPAIR_LIMIT:
                repair_prompt = f"The tests failed with the following output:\n{output_tail}\nPlease modify the code to fix the issue and then re‑run the tests."
                msg_history = chat_with_agent(repair_prompt, model=self.code_model, msg_history=msg_history, logging=safe_log)
                # After repair, ensure progress (in case the model still didn't edit)
                if not self._has_progress():
                    # send a single nudge without counting toward NUDGE_LIMIT (already used earlier)
                    msg_history = chat_with_agent("Please edit the solution file to address the failure.", model=self.code_model, msg_history=msg_history, logging=safe_log)
                passed, output_tail = self._run_checks()
                # Update latest attempt record
                attempts[-1]['passed'] = passed
                attempts[-1]['output_tail'] = output_tail
                attempts[-1]['diff'] = diff_versus_commit(self.git_tempdir, self.base_commit)
                repair_round += 1

            if passed:
                safe_log('All checks passed on this attempt.')
                best_patch = attempts[-1]['diff']
                break
            else:
                safe_log('Attempt failed; resetting repository for next attempt.')
                # Keep the latest diff as candidate if it's non‑empty
                if attempts[-1]['diff'].strip():
                    best_patch = attempts[-1]['diff']
                # Reset repo before next attempt
                self._reset()
                # Continue to next attempt loop
                continue

        # After attempts, apply the best patch (if any) on a clean base
        self._reset()
        if best_patch:
            safe_log('Applying best patch to repository.')
            apply_patch(self.git_tempdir, best_patch)
        else:
            safe_log('No patch to apply; repository remains unchanged.')

        return msg_history

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

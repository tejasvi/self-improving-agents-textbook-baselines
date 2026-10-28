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
            language='python',
            max_attempts=3,
        ):
        self.problem_statement = problem_statement
        self.git_tempdir = git_tempdir
        self.base_commit = base_commit
        self.chat_history_file = chat_history_file
        self.test_description = test_description
        self.self_improve = self_improve
        self.language = language
        self.max_attempts = max(1, int(max_attempts))

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

    def run_tests(self, timeout=300):
        """
        Run the language's test commands under git_tempdir.
        Returns (passed: bool, output: str). Bounded by a timeout per command.
        """
        commands = TEST_COMMANDS.get(self.language)
        if not commands:
            return True, f"No test commands configured for language '{self.language}'."
        outputs = []
        for cmd in commands:
            try:
                proc = subprocess.run(
                    cmd, cwd=self.git_tempdir, capture_output=True, text=True, timeout=timeout
                )
            except subprocess.TimeoutExpired:
                outputs.append(f"$ {' '.join(cmd)}\nTimed out after {timeout}s")
                return False, "\n".join(outputs)
            except Exception as e:
                outputs.append(f"$ {' '.join(cmd)}\nError: {e}")
                return False, "\n".join(outputs)
            text = (proc.stdout or "") + (proc.stderr or "")
            outputs.append(f"$ {' '.join(cmd)}\n(exit code {proc.returncode})\n{text[-4000:]}")
            # pytest exit code 5 = no tests collected; not a failure
            ok_codes = (0, 5) if self.language == 'python' else (0,)
            if proc.returncode not in ok_codes:
                return False, "\n".join(outputs)
        return True, "\n".join(outputs)

    def build_instruction(self, failed_attempts):
        """
        Build the task instruction. On retries, include previous failed attempts
        (their diffs and test outputs) so the agent can avoid repeating mistakes.
        """
        instruction = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Solve the following programming problem.

<problem_description>
{self.problem_statement}
</problem_description>

Deliverable: a single final solution file inside {self.git_tempdir}. Write the solution there and make it the final output of your work. Follow the interface the repository's existing files expect.
"""
        if failed_attempts:
            history_lines = []
            for i, attempt in enumerate(failed_attempts, 1):
                history_lines.append(
                    f"## Previous attempt {i}\n"
                    f"### Edits made\n{attempt['diff'] or '(no edits)'}\n"
                    f"### Test output\n{attempt['test_output']}\n"
                )
            instruction += f"""
# Retry context
Previous attempt(s) at this problem failed the tests. Their edits and test outputs are below.
Analyze why they failed, then fix the solution. Do not repeat the same mistakes.
Re-run the tests after your changes and make sure the solution passes before finishing.

{chr(10).join(history_lines)}"""
        return instruction

    def forward(self):
        """
        The forward function for the AgenticSystem.
        Runs up to max_attempts agent attempts; each failed attempt's edits and
        test output are passed to the next attempt as context.
        """
        failed_attempts = []
        for attempt_idx in range(self.max_attempts):
            safe_log(f"=== Attempt {attempt_idx + 1}/{self.max_attempts} ===")
            instruction = self.build_instruction(failed_attempts)
            chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)

            passed, test_output = self.run_tests()
            if passed:
                safe_log(f"Attempt {attempt_idx + 1} passed tests.")
                return
            safe_log(f"Attempt {attempt_idx + 1} failed tests.")
            diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
            failed_attempts.append({"diff": diff, "test_output": test_output})

def main():
    parser = argparse.ArgumentParser(description='Process repository with an agentic system.')
    parser.add_argument('--problem_statement', required=True, help='The problem statement to process')
    parser.add_argument('--git_dir', required=True, help='Path to git repository directory')
    parser.add_argument('--base_commit', required=True, help='Base commit hash to compare against')
    parser.add_argument('--chat_history_file', required=True, help='Path to chat history file')
    parser.add_argument('--outdir', required=False, default="/dgm/", help='Output directory')
    parser.add_argument('--test_description', default=None, required=False, help='Description of how to test the repository')
    parser.add_argument('--self_improve', default=False, action='store_true', help='Whether to self-improve the repository or solving swe')
    parser.add_argument('--max_attempts', required=False, type=int, default=3, help='Maximum number of attempts, with retry context from failed attempts')
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
        max_attempts=args.max_attempts,
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

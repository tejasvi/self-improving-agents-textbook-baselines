import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import shutil
import tempfile
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

    def run_attempt(self, msg_history=None):
        """
        Run the agent once on the task, then ask it to verify its solution against the examples
        in the problem statement, and finally to re-read the problem and check edge cases.
        Returns (msg_history, passed).
        """
        if msg_history is None:
            msg_history = []
        # Fresh scratch directory for this attempt. It lives outside git_tempdir so that
        # the agent's unit tests never show up in the repository diff.
        scratch_dir = tempfile.mkdtemp(prefix="scratch_tests_")
        try:
            return self._run_attempt_with_scratch(msg_history, scratch_dir)
        finally:
            shutil.rmtree(scratch_dir, ignore_errors=True)

    def _run_attempt_with_scratch(self, msg_history, scratch_dir):
        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        # Phase 1: analysis. Produce a plan without modifying any files.
        analysis_instruction = (
            f"{task}\n\nPlease analyze the problem description carefully. "
            "Do NOT modify any files in this step. Instead, produce a concrete plan covering: "
            "(1) the input/output format and what the expected answer is for each example, "
            "(2) the algorithm you will use and why it is correct and efficient enough for the stated constraints, "
            "(3) the edge cases to handle, "
            "(4) the files you will create or edit, and "
            "(5) how you will test the solution (example runs and any additional tests). "
            "You may inspect the repository with the available tools to gather information."
        )
        msg_history = chat_with_agent(analysis_instruction, model=self.code_model, msg_history=msg_history, logging=safe_log)

        # Phase 2: implementation. Follow the plan produced above.
        implement_instruction = (
            "Implementation step: follow the plan you just produced. Make the necessary edits to the code files "
            "to complete the task, then test the solution by running it on the examples from the problem statement. "
            "If you find a discrepancy with your plan, adjust the code and explain why.\n\n"
            f"Also write your own unit tests in the scratch directory {scratch_dir} (create it if needed; "
            "do NOT put test files inside the repository). Cover the examples from the problem statement plus "
            "edge cases (smallest/largest inputs, empty or single-element inputs, duplicates, format details). "
            "Run these tests against your solution, fix any failures, and re-run until they all pass "
            "before you finish this step."
        )
        msg_history = chat_with_agent(implement_instruction, model=self.code_model, msg_history=msg_history, logging=safe_log)

        verify_instruction = (
            f"Verification step: run the unit tests you wrote in {scratch_dir} again, then extract every example input/output pair from the problem statement, "
            "run your solution on each of them (for a complete program, feed the example input via stdin; "
            "for a Solution class method, call it with the example arguments), and compare the results with the expected outputs. "
            "Do not modify any files in this step unless a fix is strictly needed; if you do, re-run the examples."
        )
        msg_history = chat_with_agent(verify_instruction, model=self.code_model, msg_history=msg_history, logging=safe_log)

        review_instruction = (
            f"Final review step: re-read the problem statement carefully from start to finish (your unit tests are in {scratch_dir}; extend them if you find an uncovered edge case), "
            "and check your solution against it. Consider edge cases such as the smallest and largest allowed inputs, "
            "empty or single-element inputs, duplicates, zero or negative values (if allowed), input format details "
            "(whitespace, number of lines, multiple test cases), and the exact output format (spacing, newlines, casing). "
            "Verify that every requirement in the statement is satisfied. If you find a problem, fix the code and re-run the examples. "
            "Then reply with a short summary of the review and end your reply with exactly one line of the form "
            "'EXAMPLES_PASSED: yes' if all examples produce the expected output, or 'EXAMPLES_PASSED: no' otherwise."
        )
        msg_history = chat_with_agent(review_instruction, model=self.code_model, msg_history=msg_history, logging=safe_log)

        # Find the last assistant text containing the verdict
        verdict_text = ''
        for msg in reversed(msg_history):
            if msg.get('role') != 'assistant':
                continue
            content = msg.get('content')
            if isinstance(content, str):
                verdict_text = content
            else:
                verdict_text = ' '.join(
                    block.get('text', '') for block in content if isinstance(block, dict) and block.get('text')
                )
            if verdict_text:
                break
        passed = 'EXAMPLES_PASSED: yes' in verdict_text
        return msg_history, passed

    def forward(self, max_attempts=3):
        """
        The forward function for the AgenticSystem.
        Runs the agent up to `max_attempts` times, each from a clean base commit. The first attempt whose
        solution passes the problem statement's examples is kept; otherwise the last attempt is kept.
        The chosen attempt's diff is left applied in git_tempdir.
        """
        attempt_patches = []
        chosen_patch = None
        for attempt in range(max_attempts):
            safe_log(f"=== Attempt {attempt + 1}/{max_attempts} ===")
            reset_to_commit(self.git_tempdir, self.base_commit)
            _, passed = self.run_attempt()
            patch = str(diff_versus_commit(self.git_tempdir, self.base_commit))
            attempt_patches.append(patch)
            safe_log(f"=== Attempt {attempt + 1} examples passed: {passed} ===")
            if passed:
                chosen_patch = patch
                break

        if chosen_patch is None:
            chosen_patch = attempt_patches[-1]
        # Restore the chosen attempt's state in the repository
        reset_to_commit(self.git_tempdir, self.base_commit)
        if chosen_patch.strip():
            apply_patch(self.git_tempdir, chosen_patch)

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

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

    def forward(self, max_attempts=3):
        """
        The forward function for the AgenticSystem.

        Runs the agent up to `max_attempts` times. After each attempt the agent is asked
        to verify its solution against the examples in the problem statement. The first
        attempt whose solution passes the examples is kept; if none passes, the last
        attempt is kept.
        """
        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        analysis_msg = (
            f"{task}\n\n"
            "PHASE 1 (analysis only). Do NOT create or modify any files in this phase. "
            "Do the following and write the result as a clear plan:\n"
            "1. Read the problem. Restate the input format and the output format in your own words, "
            "and list every constraint the solution must handle (input sizes, value ranges, time/memory limits, edge cases).\n"
            "2. Plan an algorithm. Summarize the approach, justify why it fits the constraints, and work out by hand "
            "what it should output for each example in the problem statement.\n"
            "3. Write a numbered implementation plan: which files to write, the functions/classes involved, "
            "the test cases you will write in a scratch directory outside the repository, and the checks you will run.\n"
            "End this phase with the plan; do not implement yet."
        )

        instruction = (
            f"{task}\n\n"
            "PHASE 2 (implementation). Follow the plan you wrote in the previous step. "
            "Carry out the following steps explicitly, in order:\n"
            "1. Implement the algorithm from your plan in the code files of the repository "
            f"({self.git_tempdir}) so that it reads from stdin and writes to stdout (or implements the required Solution class method).\n"
            "2. Test the implementation on the examples given in the problem statement. Run it on each example input "
            "and compare the output with the expected output. If the outputs differ, go back to the plan, fix the issue, and test again.\n"
            "3. Additionally, write your own tests for the solution in a scratch directory OUTSIDE the repository "
            "(create it with `mktemp -d`, e.g. under /tmp), covering the examples, edge cases, and small brute-force "
            "comparisons where useful. Run these tests with the bash tool and fix the solution until they pass. "
            f"Do not put test files inside {self.git_tempdir}, so the repository diff contains only the solution."
        )

        verify_msg = (
            "Now verify your solution against every example input/output given in the problem statement. "
            "Run the solution on each example (for a complete program, pipe the example input via stdin; "
            "for a Solution class method, call it with the example arguments) and compare with the expected output. "
            "If the run_io_tests tool is available, you may use it to run the solution on all examples at once "
            "(pass each example's input and expected output as a test case). "
            "Do NOT modify any files in this verification step. "
            "When you are done, end your reply with exactly one of these lines on its own:\n"
            "EXAMPLES_PASS\n"
            "EXAMPLES_FAIL\n"
            "Use EXAMPLES_PASS only if the solution produces the expected output for all examples."
        )

        chosen_patch = None
        last_patch = None
        for attempt in range(1, max_attempts + 1):
            safe_log(f"=== Attempt {attempt}/{max_attempts} ===")
            if attempt > 1:
                reset_to_commit(self.git_tempdir, self.base_commit)

            plan_history = chat_with_agent(analysis_msg, model=self.code_model, msg_history=[], logging=safe_log)
            msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=plan_history, logging=safe_log)
            msg_history = chat_with_agent(verify_msg, model=self.code_model, msg_history=msg_history, logging=safe_log)
            passed = self._parse_verdict(msg_history)

            last_patch = diff_versus_commit(self.git_tempdir, self.base_commit)
            safe_log(f"=== Attempt {attempt} examples verdict: {'PASS' if passed else 'FAIL'} ===")
            if passed:
                chosen_patch = last_patch
                break

        if chosen_patch is None:
            chosen_patch = last_patch
            safe_log("No attempt passed the examples; keeping the last attempt.")
        else:
            safe_log("Keeping the attempt that passed the examples.")

        # Restore the chosen attempt's state in the repository
        reset_to_commit(self.git_tempdir, self.base_commit)
        if chosen_patch:
            apply_patch(self.git_tempdir, chosen_patch)

    @staticmethod
    def _parse_verdict(msg_history):
        """Return True if the last assistant text ends with EXAMPLES_PASS (and not EXAMPLES_FAIL)."""
        for msg in reversed(msg_history):
            if msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            texts = []
            if isinstance(content, str):
                texts.append(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        texts.append(block.get("text") or "")
                    elif getattr(block, "type", None) == "text":
                        texts.append(getattr(block, "text", ""))
            text = "\n".join(t for t in texts if t)
            if "EXAMPLES_FAIL" in text:
                return False
            return "EXAMPLES_PASS" in text
        return False

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

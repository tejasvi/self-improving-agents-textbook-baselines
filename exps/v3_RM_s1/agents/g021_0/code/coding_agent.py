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

    @staticmethod
    def _last_assistant_text(msg_history):
        """Return the text of the last assistant message in msg_history (or '')."""
        for msg in reversed(msg_history):
            if msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                texts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("text")]
                if texts:
                    return "\n".join(texts)
        return ""

    def _run_attempt(self, instruction):
        """
        Run one agent attempt from the base commit: solve, final review of the problem
        statement and edge cases, then verify the examples. Returns (passed, diff, report),
        where passed is True if the agent reports that the problem's examples pass and
        report is the agent's final verification output.
        """
        reset_to_commit(self.git_tempdir, self.base_commit)
        msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)

        review_msg = (
            "Final review step. Re-read the original problem statement in <problem_description> carefully, "
            "line by line, and compare it against your current solution. Check that:\n"
            "- every requirement and output format detail (spacing, newlines, ordering, case) is satisfied;\n"
            "- edge cases are handled (smallest and largest inputs, empty or minimal inputs, duplicates, "
            "zero or negative values, boundary conditions, and any constraints stated in the problem);\n"
            "- the solution does not rely on hardcoded answers and runs within reasonable time for the stated constraints.\n"
            "If you find any mismatch or unhandled edge case, fix the code in the repository. "
            "Otherwise, leave the code unchanged. Briefly summarize the review result."
        )
        msg_history = chat_with_agent(review_msg, model=self.code_model, msg_history=msg_history, logging=safe_log)

        verify_msg = (
            "Before finishing, run the example input/output pairs given in the problem statement "
            "against your final solution (for a complete program, feed the example input via stdin; "
            "for a Solution class method, call it with the example arguments). "
            "Compare the actual output with the expected output exactly. "
            "End your reply with exactly one final line: 'EXAMPLES: PASS' if every example matches, "
            "or 'EXAMPLES: FAIL' otherwise."
        )
        msg_history = chat_with_agent(verify_msg, model=self.code_model, msg_history=msg_history, logging=safe_log)
        verdict = self._last_assistant_text(msg_history)
        passed = "EXAMPLES: PASS" in verdict and "EXAMPLES: FAIL" not in verdict

        diff = diff_versus_commit(self.git_tempdir, self.base_commit)
        safe_log(f"Attempt finished: passed={passed}")
        return passed, diff, verdict

    @staticmethod
    def _format_failed_attempts(failed_attempts):
        """
        Build a context block describing previous failed attempts (their code changes and
        the agent's verification output) so that a retry can avoid repeating the same mistakes.
        Returns '' if there are no failed attempts.
        """
        if not failed_attempts:
            return ""
        parts = [
            "\n\nYou have already made previous attempts at this problem, and they FAILED to pass "
            "the examples in the problem statement. Their code changes and verification outputs are "
            "given below. Analyze why they failed, do not repeat the same mistake, and produce a "
            "correct solution. The repository has been reset to the original state, so write your "
            "solution from scratch."
        ]
        for i, (diff, report) in enumerate(failed_attempts, 1):
            parts.append(
                f"\n<previous_attempt_{i}>\n"
                f"Code changes made in attempt {i}:\n{diff if diff else '(no changes)'}\n\n"
                f"Verification output of attempt {i}:\n{report if report else '(none)'}\n"
                f"</previous_attempt_{i}>"
            )
        return "".join(parts)

    def forward(self, num_attempts=3):
        """
        The forward function for the AgenticSystem.
        Runs up to `num_attempts` independent attempts and keeps the attempt whose
        solution passes the examples in the problem statement. Falls back to the
        last attempt if none pass.
        """
        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        instruction = f"{task}\n\nPlease analyze the problem description carefully. Then make edits to the code files to complete the instruction."

        best_diff = None
        failed_attempts = []  # list of (diff, report) from previous failed attempts
        for attempt in range(num_attempts):
            safe_log(f"=== Attempt {attempt + 1}/{num_attempts} ===")
            attempt_instruction = instruction + self._format_failed_attempts(failed_attempts)
            passed, diff, report = self._run_attempt(attempt_instruction)
            best_diff = diff
            if passed:
                break
            failed_attempts.append((diff, report))

        # The loop stops at the first passing attempt, and otherwise ends on the last one,
        # so the repository already holds the chosen solution.
        return best_diff

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

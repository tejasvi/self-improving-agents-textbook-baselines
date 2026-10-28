import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import re
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

    def _get_changed_files(self):
        """
        Return the list of files changed relative to base_commit, including untracked files.
        """
        changed = set()
        commands = [
            ["git", "-C", self.git_tempdir, "diff", "--name-only", self.base_commit],
            ["git", "-C", self.git_tempdir, "ls-files", "--others", "--exclude-standard"],
        ]
        for cmd in commands:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            for line in result.stdout.decode(errors='replace').splitlines():
                line = line.strip()
                if line:
                    changed.add(line)
        return sorted(changed)

    def _is_test_file(self, path):
        """
        Heuristically decide whether a path refers to a test file.
        """
        test_tokens = {'test', 'tests', 'spec', 'specs', 'conftest'}
        normalized = path.replace('\\', '/')
        parts = [p for p in normalized.split('/') if p]
        if not parts:
            return False
        # Directory components must match exactly
        for part in parts[:-1]:
            if part.lower() in test_tokens:
                return True
        # Filename: split into words on non-alphanumeric characters
        filename = parts[-1].lower()
        words = re.split(r'[^a-z0-9]+', filename)
        return any(w in test_tokens for w in words)

    def _has_source_patch(self):
        """
        True if at least one changed file is not a test file.
        """
        return any(not self._is_test_file(f) for f in self._get_changed_files())

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
        workflow = """
Follow this workflow step by step:
1. Explore the repository: list the files and read the relevant code, tests, and any README or specification.
2. Identify the primary source file that must be changed. If the task names a file (e.g. solution.py) and it does not exist, create it.
3. Implement the solution by actually calling the editor tool (command=create or command=edit) on the source file. Do not only describe the code in text.
4. Test it: run the program via bash with the sample inputs from the problem statement and with your own edge cases. For interactive problems, write a small local judge/simulator and run your solution against it.
5. Finally verify with `git status` and `git diff` that the source file has actually changed. Fix any problems you find.

IMPORTANT RULES:
- You MUST make changes using the editor tool. Do not just answer in text.
- If the task names an output file such as solution.py, create it.
- Responding with text only and no file edits counts as failure.
- Modifying only test files does not solve the task; the primary source file must be changed.
"""
        instruction = f"{task}\n{workflow}"
        msg_history = []
        msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=msg_history, logging=safe_log)
        safe_log(f"Initial attempt finished. Changed files: {self._get_changed_files()}")

        for attempt in range(3):
            if self._has_source_patch():
                safe_log(f"Source patch detected before retry {attempt + 1}; stopping retries.")
                break
            changed = self._get_changed_files()
            if not changed:
                reason = "No file changes detected."
            else:
                reason = f"Only test files were modified: {', '.join(changed)}."
            feedback = (
                f"{reason} The task is not complete. Use the editor tool to create or edit the primary source file "
                f"in {self.git_tempdir} that solves the problem (not test files). Run it via bash to check it, "
                f"then verify with `git status` and `git diff`, and then finish."
            )
            safe_log(f"Retry attempt {attempt + 1}/3: {reason}")
            msg_history = chat_with_agent(feedback, model=self.code_model, msg_history=msg_history, logging=safe_log)
            safe_log(f"Retry attempt {attempt + 1}/3 finished. Changed files: {self._get_changed_files()}")

        if not self._has_source_patch():
            safe_log("Last-resort attempt: requesting the complete solution via the editor tool.")
            last_resort = (
                f"Write the complete solution now by calling the editor tool with command=create/edit on the target file "
                f"in {self.git_tempdir}. Do not reply with text only."
            )
            msg_history = chat_with_agent(last_resort, model=self.code_model, msg_history=msg_history, logging=safe_log)
            safe_log(f"Last-resort attempt finished. Changed files: {self._get_changed_files()}, "
                     f"source patch: {self._has_source_patch()}")

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

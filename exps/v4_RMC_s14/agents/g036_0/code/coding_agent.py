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
        analysis_instruction = f"""{task}

This is the ANALYSIS phase. Do NOT edit or create any files in this phase. Your goal is to produce a clear, step-by-step plan for solving the problem.

Before writing any plan, follow these steps:
1. Restate the input and output format in your own words: what is read from stdin (or what arguments the `Solution` method receives), what is written to stdout (or what is returned), and the exact format of each.
2. Identify the input constraints (e.g. n, m, value ranges) stated in the problem description, and list every constraint the solution must handle.
3. Design an algorithm that solves the problem.
4. State the time complexity (and space complexity) of your algorithm explicitly, as a function of the input size variables.
5. Compare this time complexity with the constraints. If the algorithm would be too slow for the maximum input sizes (e.g. more than roughly 10^8 simple operations in Python), revise the algorithm (e.g. use a better data structure, sorting, two pointers, binary search, DP, or math) and repeat this comparison until it fits.
6. Determine the expected input/output format and any edge cases.

Output the final plan as a numbered list of concrete steps, covering: the chosen algorithm and its complexity, the files to edit, the implementation details, and how to test the solution (e.g. writing and running tests against the sample inputs and edge cases). Do not implement the solution yet."""
        analysis_response, msg_history = self._run_phase(analysis_instruction, msg_history=[])

        implementation_instruction = f"""{task}

This is the IMPLEMENTATION phase. Follow the plan you produced in the analysis phase (it is in the conversation above). Carry out the steps in order:
1. Before writing any code, re-state the input and output format and the constraints from your analysis, so they are fixed before you start.
2. Implement the solution in the appropriate code file(s) under {self.git_tempdir}.
3. Write and run tests (e.g. sample inputs and edge cases) to verify the solution's correctness and performance.
4. If a test fails or the solution is too slow, refine the solution and re-test until it passes.
5. When finished, briefly summarize the changes you made.

Only make changes that address the problem described above."""
        implementation_response, msg_history = self._run_phase(implementation_instruction, msg_history=msg_history)

        review_instruction = f"""{task}

This is the FINAL REVIEW phase. Do NOT rewrite the solution from scratch. Carry out the following steps:
1. Re-read the <problem_description> above in full, word by word. Do not rely on memory of the plan.
2. List every requirement and output-format detail stated in the problem (input format, output format, exact strings and spacing, ordering, return types, and the required method name and signature if a `Solution` class is specified).
3. Check the current implementation (see the repo's edits and the code files under {self.git_tempdir}) against each requirement, one by one.
4. Enumerate the edge cases relevant to this problem: minimum and maximum input sizes, empty or single-element inputs, duplicates, zero and negative values, large values that may cause performance or overflow issues, and any special cases mentioned in the statement.
5. For each edge case or requirement that is not yet covered by a test, write a test (or run a sample input) and check the output. If anything is wrong, fix the code.
6. Re-run all tests and confirm they pass.
7. Finish with a short summary: which requirements and edge cases were checked, and any changes made during this review.

Only make changes that address the problem described above."""
        review_response, msg_history = self._run_phase(review_instruction, msg_history=msg_history)
        return review_response

    def _run_phase(self, instruction, msg_history):
        """
        Run one phase of the agent. Returns (response_text, updated_msg_history).
        """
        new_msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=msg_history, logging=safe_log)
        response_text = ''
        if new_msg_history:
            last = new_msg_history[-1]
            content = last.get('content', '')
            if isinstance(content, list):
                response_text = ' '.join(
                    block.get('text', '') for block in content
                    if isinstance(block, dict) and isinstance(block.get('text'), str)
                )
            elif isinstance(content, str):
                response_text = content
        return response_text, new_msg_history

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

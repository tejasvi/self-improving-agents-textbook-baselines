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
        Implements a multi-phase approach to solving competitive programming problems:
        1. Initial solution and testing against samples with complexity analysis
        2. Review and stress-testing with brute force, worst-case generator, and run_benchmark
        3. Iteration with optional review rounds
        """
        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""

        # Phase 1: Initial solution and sample testing with complexity budget
        instruction_phase1 = f"""{task}

Please solve this problem step by step:

1. **Understand and Analyze the Problem:**
   - Carefully read and summarize the problem statement, including:
     * Input format and constraints
     * Output format and expected behavior
     * All sample test cases provided
   - Identify the key algorithm or approach needed
   - Prove (or provide reasoning for) why your approach handles the entire solution space
   - Consider edge cases and how your solution addresses them
   - Verify that your approach respects the problem constraints

2. **Complexity Budget Analysis (REQUIRED BEFORE IMPLEMENTING):**
   - List all maximum constraint values (e.g., N ≤ 1e6, M ≤ 1e5, time limit 2s)
   - Estimate the worst-case operation count of your planned algorithm
   - Verify that your algorithm requires ≤ ~5e7 basic Python operations
   - If your algorithm exceeds 5e7 ops, you MUST find a better approach using:
     * Constraint-exploiting techniques (pigeonhole principle, bounded values)
     * Sorting with index retention for efficient grouping
     * Bitsets or FFT for special cases
     * Meet-in-the-middle or other optimization techniques
   - ALWAYS use fast IO: sys.stdin.buffer.read() for reading input instead of input()
   - Document your complexity analysis in a comment in solution.py

3. **Implement the Solution:**
   - Write a complete solution.py file that solves the problem
   - The solution should read from standard input and write to standard output
   - Use clear variable names and add brief comments
   - Ensure you use the fast IO method specified in step 2

4. **Extract and Test with Samples:**
   - Extract ALL sample test cases from the problem statement (input and expected output)
   - Write each sample as a JSON object with "input" and "expected_output" keys
   - Use the run_samples tool to test your solution against all samples
   - If there are mismatches, analyze whether:
     * Your solution is incorrect
     * The output is valid but formatted differently (e.g., multiple correct answers)
   - If outputs differ but are potentially valid, note this for later validation step

5. **Initial Verification:**
   - Ensure that the solution handles the provided samples correctly
   - If samples pass, you're ready to move to more comprehensive testing
   - If samples fail, debug and fix the solution before proceeding

After completing these steps, we'll move to comprehensive testing with brute force and stress testing.
"""

        init_edit = chat_with_agent(instruction_phase1, model=self.code_model, msg_history=[], logging=safe_log)

        # Phase 2: Brute force, comprehensive testing, and worst-case benchmarking
        # Get current edits to pass to the agent
        current_edits = self.get_current_edits()
        
        instruction_phase2 = """Now let's do comprehensive testing and validation:

6. **Create a Validity Checker (if needed):**
   - If you discovered that your solution can produce valid but different outputs than the samples (e.g., multiple correct answers), create a checker.py file
   - The checker should read from stdin with the format: test_input, then blank line, then solution_output, then blank line, then expected_output
   - The checker should exit with code 0 if the solution output is valid, or non-zero if invalid
   - Also try to align your solution's output with the sample where practical (e.g., picking canonical/smallest/largest valid answer)

7. **Create a Brute Force Solution:**
   - Write a brute.py file that solves the same problem using a simpler, clearly correct (but possibly slower) approach
   - This will be used as a reference for differential testing
   - The brute force solution should produce correct results on all inputs

8. **Create a Test Generator:**
   - Write a gen.py file that generates random valid test cases
   - The generator should produce diverse test cases covering:
     * Small and medium-sized inputs
     * Edge cases (minimum/maximum values, empty inputs, etc.)
     * Various patterns that exercise different code paths
   - Each invocation of gen.py should output one test case to stdout

9. **Run Comprehensive Differential Testing:**
   - Use the run_tests tool with your solution.py, brute.py, gen.py, and optionally checker.py
   - Run at least 100 random tests
   - This will catch logical errors that samples alone wouldn't find

10. **Create and Test Worst-Case Scenario:**
    - Create a max_input.txt file with the maximum size input allowed by the constraints
    - Make this input a worst-case for your algorithm (e.g., if you use sorting, make it reverse-sorted; if you use hashing, make all values equal)
    - Create a worst_case_gen.py that accepts an optional argument and generates:
      * 'max_n': input with maximum N and values designed to trigger worst-case behavior
      * 'no_answer': cases where no valid answer exists
      * 'all_equal': all elements with the same value
      * 'sorted': pre-sorted or reverse-sorted inputs
    - Use the run_benchmark tool to test the max-size input: run_benchmark(solution_path, max_input_path=max_input.txt)
    - If timing shows > ~2 seconds or any TIMEOUT, the algorithm is too slow and must be redesigned
    - If run_benchmark returns OK, provide max_input.txt to run_tests as well

11. **Test Maximum Input Size:**
    - Provide max_input.txt to run_tests to measure timing during differential testing
    - Ensure your solution doesn't timeout

12. **Fix Any Issues Found:**
    - If tests fail, analyze the failure and fix the solution
    - If run_benchmark shows TIMEOUT or time > ~2s, you MUST redesign the algorithm
    - NEVER rationalize or ignore a TLE - redesign is mandatory
    - Re-run tests after each fix

Once all tests pass (see "ALL PASSED" in test results) AND run_benchmark succeeds, your solution is ready.
"""

        # Use bounded loop for review rounds (max 3 iterations)
        max_review_rounds = 3
        benchmark_succeeded = False  # Track if we've seen a successful max-size benchmark
        
        for review_round in range(max_review_rounds):
            current_edits = self.get_current_edits()
            
            if review_round == 0:
                # First review: full comprehensive testing
                review_instruction = instruction_phase2
            else:
                # Subsequent reviews: focus on fixes and re-testing
                review_instruction = f"""You have {max_review_rounds - review_round} review rounds remaining.

Please continue improving the solution:
- Fix any issues found in the previous testing
- Re-run run_benchmark to verify worst-case performance
- Re-run run_tests to verify all tests pass
- If all tests now show "ALL PASSED" and run_benchmark shows "OK", you're done!
- Otherwise, continue debugging, redesigning, and testing

Remember to use bounded tools and avoid while loops."""

            review_result = chat_with_agent(
                review_instruction,
                model=self.code_model,
                msg_history=current_edits,
                logging=safe_log
            )
            
            # Check if all tests passed AND a successful benchmark was run
            # Only exit early if we see both "ALL PASSED" and "OK in" (successful benchmark)
            has_all_passed = "ALL PASSED" in review_result or "all tests passed" in review_result.lower()
            has_benchmark_ok = "OK in" in review_result  # run_benchmark success indicator
            
            if has_all_passed and has_benchmark_ok:
                benchmark_succeeded = True
                safe_log("All tests passed and worst-case benchmark succeeded! Solution is complete.")
                break
            elif has_all_passed and not has_benchmark_ok:
                safe_log("Random tests passed but benchmark not yet run or not yet succeeded. Continuing to next review round.")

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

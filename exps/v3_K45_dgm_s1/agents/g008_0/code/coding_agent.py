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
        Implements a multi-phase workflow:
        - Phase A: Analyze problem, determine complexity requirements, design algorithm, implement solution
        - Phase B: Write brute-force reference, generate random tests, stress test, optimize if needed (up to 3 rounds)
        - Phase C: Final review for correctness and cleanup
        """
        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        
        # ==================== PHASE A: ANALYZE AND IMPLEMENT ====================
        phase_a_instruction = f"""{task}

## PHASE A: Analysis and Initial Implementation

Please execute the following steps carefully:

1. **Extract Constraints**: From the problem statement, identify all input size constraints (e.g., n <= 1e5, m <= 1e6, time limit).
2. **Determine Required Complexity**: Based on the constraints, calculate what time complexity is acceptable (e.g., O(n log n) for n=1e5, O(n^2) for n=1e3).
3. **Algorithm Design**: Design an algorithm that meets or beats the required complexity. State the algorithm's time and space complexity before implementing.
4. **Implementation**: Implement the solution in the required file (solution.py for standalone programs, or a Solution class method for class-based tasks).
5. **Include Docstring**: Add a docstring to your solution explicitly stating the time and space complexity.

Be thorough in your analysis and precise in your stated complexity. Do not skip these steps.

Please analyze the problem description carefully. Then make edits to the code files to implement the solution.
"""
        
        phase_a_history = chat_with_agent(
            phase_a_instruction,
            model=self.code_model,
            msg_history=[],
            logging=safe_log
        )
        
        # ==================== PHASE B: VERIFICATION AND STRESS TESTING ====================
        phase_b_instruction = f"""Based on your implementation above, now execute PHASE B: Verification and Stress Testing.

## PHASE B: Brute-Force Testing and Optimization Loop

Your implementation is now in place. We need to verify its correctness and performance:

1. **Write Brute-Force Reference**: In a temporary directory (e.g., /tmp), write a simple, obviously correct brute-force solution. This solution does not need to be fast; it just needs to be clearly correct.

2. **Write Random Input Generator**: Create a generator script that produces random test cases with a seed parameter (arg 0 = seed). The generator should:
   - Use the seed to produce deterministic but varied inputs
   - Cover edge cases: empty input, single element, all equal elements, min/max values
   - For the first few seeds (0-5), generate small inputs
   - For larger seeds, generate inputs closer to the maximum constraints

3. **Run Stress Test**: Use the stress_test tool to run 100 random test cases:
   - Compare your solution against the brute-force reference
   - If any test fails, report the failing input and both outputs
   - If all pass, report pass rate and timing stats

4. **Benchmark Max-Size Input**: Create a worst-case input file at maximum constraint size:
   - For O(n^2) algorithms: use sorted ascending, sorted descending, or random order
   - For O(n log n) algorithms: the worst case is typically random or nearly-sorted data
   - Run the benchmark tool to measure wall-clock time with a timeout of 2-3 seconds
   - If it times out or exceeds 2 seconds, the algorithm is too slow for the constraints

5. **Redesign Loop** (if needed, up to 3 rounds):
   - If the stress test fails (wrong answer) OR the benchmark times out/is too slow:
     - Go back and redesign the algorithm from scratch (do not patch it)
     - State the new complexity before re-implementing
     - Repeat steps 3-4
   - If stress test passes AND benchmark runs in < 2 seconds, move to Phase C

Remember: test and generator files go in /tmp or other scratch directories, NOT in the main repo. Only solution.py (or the Solution class) should remain in the repo.

Execute these steps now. Report your findings clearly.
"""
        
        # Run Phase B with message history from Phase A to maintain context
        phase_b_history = chat_with_agent(
            phase_b_instruction,
            model=self.code_model,
            msg_history=phase_a_history,
            logging=safe_log
        )
        
        # ==================== PHASE C: FINAL REVIEW ====================
        phase_c_instruction = """## PHASE C: Final Review and Cleanup

Before finishing, perform a final review:

1. **Complexity Verification**: 
   - Look at your solution code and count the nested loops or recursion depth
   - Verify that the stated complexity matches the actual code structure
   - Example: if you claim O(n log n), the code should have at most O(log n) nested work, not nested loops

2. **Code Correctness for Class-Based Tasks**:
   - If this is a class-based task (Solution class method), ensure:
     - The code does NOT read from stdin
     - It only takes method parameters
     - Return type is correct

3. **Repository Cleanup**:
   - Verify that NO test files, brute-force references, or generators remain in the main repo
   - Only solution.py (or the Solution class) should be the modified deliverable
   - Check that all scratch files are in /tmp or other temporary locations

4. **Summary**: Report:
   - The final algorithm's time and space complexity
   - Whether stress tests passed
   - Whether max-constraint benchmark passed
   - Whether code is clean and ready for submission

If any issues are found, fix them now. Otherwise, confirm that the solution is ready.
"""
        
        # Run Phase C with combined history
        combined_history = phase_a_history + phase_b_history
        phase_c_history = chat_with_agent(
            phase_c_instruction,
            model=self.code_model,
            msg_history=combined_history,
            logging=safe_log
        )

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

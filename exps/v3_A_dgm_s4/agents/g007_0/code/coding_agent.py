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
        Return the list of files changed versus base_commit, including untracked files.
        """
        files = set()
        diff_cmd = ["git", "-C", self.git_tempdir, "diff", "--name-only", self.base_commit]
        result = subprocess.run(diff_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        files.update(line.strip() for line in result.stdout.decode().splitlines() if line.strip())

        untracked_cmd = ["git", "-C", self.git_tempdir, "ls-files", "--others", "--exclude-standard"]
        result = subprocess.run(untracked_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        files.update(line.strip() for line in result.stdout.decode().splitlines() if line.strip())
        return sorted(files)

    def _is_test_file(self, path):
        """
        Heuristically decide whether a path refers to a test file.
        """
        parts = path.replace('\\', '/').split('/')
        name = parts[-1]
        target = self._infer_target_file()
        if name == os.path.basename(target) or path.replace('\\', '/').endswith(os.path.relpath(target, self.git_tempdir).replace('\\', '/')):
            return False
        test_dirs = {'test', 'tests', 'spec', 'specs', '__tests__'}
        if any(p.lower() in test_dirs for p in parts[:-1]):
            return True
        if name.lower() in test_dirs:
            return True
        if name.startswith('test_') and name.endswith('.py'):
            return True
        if name.endswith('_test.py'):
            return True
        if name.endswith('.spec.js') or name.endswith('.test.js'):
            return True
        return False

    def _clean_history(self, msg_history):
        """
        Drop assistant messages that have no tool_use blocks and only empty/whitespace text.
        Returns [] if no meaningful content remains.
        """
        def _block_type(block):
            if isinstance(block, dict):
                return block.get('type')
            return getattr(block, 'type', None)

        def _block_text(block):
            if isinstance(block, dict):
                return block.get('text')
            return getattr(block, 'text', None)

        def _is_meaningful(msg):
            if not isinstance(msg, dict):
                return True  # non-dict message objects are kept as-is
            if msg.get('role') != 'assistant':
                return True
            content = msg.get('content')
            if isinstance(content, str):
                return bool(content.strip())
            if isinstance(content, list):
                for block in content:
                    btype = _block_type(block)
                    if btype in ('tool_use', 'function_call', 'tool_call'):
                        return True
                    text = _block_text(block)
                    if isinstance(text, str) and text.strip():
                        return True
                return False
            return content is not None

        cleaned = [m for m in (msg_history or []) if _is_meaningful(m)]
        if not cleaned:
            return []
        has_content = False
        for m in cleaned:
            if not isinstance(m, dict):
                has_content = True
                break
            content = m.get('content')
            if isinstance(content, str) and content.strip():
                has_content = True
                break
            if isinstance(content, list) and content:
                has_content = True
                break
        return cleaned if has_content else []

    def _infer_target_file(self):
        """
        Infer the primary solution file from the problem statement (first *.py name), default solution.py.
        Returns its absolute path under git_tempdir.
        """
        match = re.search(r'(?<![\w/.-])([A-Za-z_][\w-]*\.py)\b', self.problem_statement or '')
        name = match.group(1) if match else 'solution.py'
        return os.path.abspath(os.path.join(self.git_tempdir, name))

    def _has_source_edits(self):
        """
        True if at least one changed file is not a test file.
        """
        return any(not self._is_test_file(f) for f in self._get_changed_files())

    def _ends_with_empty_assistant(self, msg_history):
        """
        True if the last message in msg_history is an assistant message with no meaningful content.
        """
        if not msg_history:
            return False
        last = msg_history[-1]
        if not isinstance(last, dict) or last.get('role') != 'assistant':
            return False
        return len(self._clean_history([last])) == 0

    def _run_stress_test(self):
        """
        Run /tmp/stress_test.py. Returns (status, output) where status is one of
        'missing', 'ok', 'fail', 'timeout'. Output is the raw combined stdout/stderr (no parsing).
        """
        stress_path = '/tmp/stress_test.py'
        if not os.path.exists(stress_path):
            return 'missing', ''
        try:
            result = subprocess.run(
                ['python3', stress_path],
                capture_output=True,
                text=True,
                timeout=300,
            )
        except subprocess.TimeoutExpired as e:
            out = e.stdout if isinstance(e.stdout, str) else ''
            err = e.stderr if isinstance(e.stderr, str) else ''
            return 'timeout', (out + err)
        output = (result.stdout or '') + (result.stderr or '')
        if 'STRESS_OK' in output and result.returncode == 0:
            return 'ok', output
        return 'fail', output

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
        workflow = f"""

Follow these steps:
1. Explore the repository in {self.git_tempdir} with the bash and editor tools (list files, read any existing solution stub, README, or tests).
2. Identify the file that must be edited. If the task names a file (e.g. solution.py) and it does not exist, create it with the editor tool.
3. Implement the complete solution in that file early, even if it is not yet perfect. It must be a full program that reads from standard input and writes to standard output, or the required method of the given Solution class.
4. Write a few test inputs (including the sample inputs from the problem statement) and run them with the bash tool.
5. Write a randomized stress test at the fixed path /tmp/stress_test.py (outside the repository). It must:
   - Compare the solution against a simple brute-force reference on small random inputs (at least 1000 random cases), and include edge cases (empty/minimal inputs, duplicates, extreme values, boundary sizes).
   - Import or run the solution exactly as the judge would (stdin/stdout for programs, or call the Solution method).
   - On any mismatch, print 'STRESS_FAIL' followed by the counterexample (input, expected, got) and exit with a non-zero status.
   - Only when every case matches, print 'STRESS_OK' and exit 0.
   Run it with `python3 /tmp/stress_test.py`.
6. Fix any failures or mismatches, then re-run the sample tests and the stress test until the outputs are correct.
   - If the stress test fails, do not patch blindly: rederive the algorithm from the problem and check it against the brute-force reference.
   - Do not rely on a remembered formula or known solution without verifying it with the brute-force reference.
   - Never finish while a mismatch exists in the stress test.
7. Always finish with the solution file saved on disk. A text-only reply without file edits is a failure.
"""
        instruction = f"{task}{workflow}\nPlease analyze the problem description carefully. Then make edits to the code files to complete the instruction."
        target_path = self._infer_target_file()
        msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)

        def _log_state(label):
            changed = self._get_changed_files()
            has_src = self._has_source_edits()
            diff_nonempty = bool(str(diff_versus_commit(self.git_tempdir, self.base_commit)).strip())
            safe_log(f"[forward] {label}: changed={changed}, source_edits={has_src}, diff_nonempty={diff_nonempty}")
            return has_src

        _log_state("Initial call done")

        # Bounded verify-and-repair loop driven by the stress test
        for stress_round in range(4):
            status, output = self._run_stress_test()
            safe_log(f"[forward] Stress round {stress_round + 1}: status={status}")
            if status == 'ok':
                break
            if status == 'missing':
                prompt = (
                    f"{task}\n"
                    "The stress test file /tmp/stress_test.py does not exist. Create it now with the editor tool. "
                    "It must brute-force compare the solution against a reference on at least 1000 random small inputs "
                    "plus edge cases, print 'STRESS_FAIL' with the counterexample and exit non-zero on any mismatch, "
                    "and print 'STRESS_OK' and exit 0 only when every case matches. Then run `python3 /tmp/stress_test.py`."
                )
            else:
                reason = "timed out" if status == 'timeout' else "failed"
                prompt = (
                    f"Your stress test is failing (it {reason}). Here is the raw output (tail):\n"
                    f"<output>\n{output[-3000:]}\n</output>\n"
                    "Analyze the counterexample, find the flaw in the algorithm (rederive it rather than patching), "
                    "fix solution.py, and re-run until STRESS_OK."
                )
            cleaned = self._clean_history(msg_history)
            if self._ends_with_empty_assistant(msg_history) or not cleaned:
                safe_log(f"[forward] Stress round {stress_round + 1}: history ends empty; starting fresh context with failing output")
                fresh = f"{task}\n\nPrevious attempt left the solution in progress.\n{prompt}"
                msg_history = chat_with_agent(fresh, model=self.code_model, msg_history=[], logging=safe_log)
            else:
                msg_history = chat_with_agent(prompt, model=self.code_model, msg_history=cleaned, logging=safe_log)
            _log_state(f"After stress repair round {stress_round + 1}")
        recovery = (
            f"{task}\n"
            "Your previous attempt produced no file edits. Do NOT explore first. "
            f"Immediately call the editor tool with command=create (or edit if the file exists) on {target_path} "
            "to write a full working program that reads stdin and writes stdout. "
            "After it is saved, run the sample tests with bash and fix any errors."
        )
        simple = f"Create the file {target_path} now with a complete working program that reads stdin and writes stdout using the editor tool."

        for attempt in range(3):
            if _log_state(f"Attempt {attempt + 1} check"):
                break
            cleaned = self._clean_history(msg_history)
            safe_log(f"[forward] Retry {attempt + 1}: no source edits; history cleaned from {len(msg_history)} to {len(cleaned)} messages; starting fresh context")
            prompt = recovery if attempt < 2 else simple
            # Fresh context: never reuse a history that ends with an empty assistant message
            msg_history = chat_with_agent(prompt, model=self.code_model, msg_history=[], logging=safe_log)

        if not _log_state("Final check after retries"):
            if not os.path.exists(target_path):
                stub = "import sys\n\ndata = sys.stdin.read()\nprint(0)\n"
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, 'w') as f:
                    f.write(stub)
                safe_log(f"[forward] Wrote stub to {target_path}")
            _log_state("After stub written")
            final_prompt = (
                f"A stub exists at {target_path}. It is only a placeholder and must be replaced with a real implementation "
                "that reads stdin and writes stdout. Use the editor tool to overwrite it with a full solution, "
                "then test it with the sample inputs using bash and fix any errors."
            )
            msg_history = chat_with_agent(final_prompt, model=self.code_model, msg_history=[], logging=safe_log)
            _log_state("After final stub-replacement pass")

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

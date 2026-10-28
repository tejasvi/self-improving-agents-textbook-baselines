import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import threading

from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
from llm import create_client, get_response_from_llm
from utils.git_utils import diff_versus_commit, reset_to_commit, apply_patch
from tools.run_samples import tool_function as run_samples_tool

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

    def _changed_files(self):
        """
        Return the list of file paths changed versus base_commit (including untracked files),
        parsed from the 'diff --git a/X b/X' headers of the repository diff.
        """
        diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        files = []
        for line in diff.splitlines():
            match = re.match(r'^diff --git a/(\S+) b/(\S+)$', line)
            if match:
                path = match.group(2)
                if path not in files:
                    files.append(path)
        return files

    @staticmethod
    def _is_test_file(path):
        parts = path.replace('\\', '/').split('/')
        name = parts[-1]
        if any(p in ('test', 'tests') for p in parts[:-1]):
            return True
        if name.startswith('test_') or name.endswith('_test.py') or name in ('test.py', 'tests.py'):
            return True
        return False

    def _mentioned_deliverables(self):
        """
        Python file names mentioned in backticks in the problem statement, e.g. `solution.py`.
        """
        return re.findall(r'`([\w./-]+\.py)`', self.problem_statement or '')

    def _file_is_nonempty(self, rel_path, min_chars=20):
        """True if the file exists under git_tempdir and has more than a few characters of content."""
        full = os.path.join(self.git_tempdir, rel_path)
        if not os.path.isfile(full):
            return False
        try:
            with open(full, 'r', errors='ignore') as f:
                return len(f.read().strip()) >= min_chars
        except OSError:
            return False

    def _has_meaningful_edit(self):
        """
        True only if at least one changed file is a non-empty non-test file, and any deliverable
        file explicitly named in the problem statement appears among the changed files and is non-empty.
        """
        changed = self._changed_files()
        if not any(not self._is_test_file(f) and self._file_is_nonempty(f) for f in changed):
            return False
        for deliverable in self._mentioned_deliverables():
            deliverable = deliverable.lstrip('./')
            matches = [f for f in changed if f == deliverable or f.endswith('/' + deliverable)]
            if not matches or not any(self._file_is_nonempty(f) for f in matches):
                return False
        return True

    @staticmethod
    def _sanitize_history(msg_history):
        """
        Drop trailing assistant messages whose content blocks are all empty text (no tool_use).
        Returns [] if nothing meaningful is left.
        """
        if not isinstance(msg_history, list):
            return []
        history = list(msg_history)

        def is_empty_assistant(msg):
            if not isinstance(msg, dict) or msg.get('role') != 'assistant':
                return False
            content = msg.get('content', [])
            if isinstance(content, str):
                return content.strip() == ''
            if not isinstance(content, list):
                return True
            for block in content:
                if isinstance(block, dict):
                    if block.get('type') == 'tool_use':
                        return False
                    if block.get('type') == 'text' and str(block.get('text', '')).strip():
                        return False
                    if block.get('type') not in (None, 'text'):
                        return False
                elif block:
                    return False
            return True

        while history and is_empty_assistant(history[-1]):
            history.pop()
        return history if history else []

    def _fallback_target(self):
        """First mentioned non-test .py deliverable, else solution.py."""
        for deliverable in self._mentioned_deliverables():
            rel = deliverable.lstrip('./')
            if not self._is_test_file(rel):
                return rel
        return 'solution.py'

    def _fallback_write_solution(self):
        """
        Last resort: ask the model directly for only the Python program and write it to the target file.
        """
        if self._has_meaningful_edit():
            return
        target_rel = self._fallback_target()
        safe_log(f"[fallback] No meaningful edit; requesting complete program directly for {target_rel}.")
        prompt = (
            "Solve the following competitive programming problem in Python 3.\n\n"
            f"<problem_description>\n{self.problem_statement}\n</problem_description>\n\n"
            "Output ONLY the full Python 3 program in one ```python fenced block. "
            "The program must read standard input and write standard output. No explanation."
        )
        try:
            client, client_model = create_client(self.code_model)
            content, _ = get_response_from_llm(
                prompt,
                client=client,
                model=client_model,
                system_message="You are an expert competitive programmer.",
                msg_history=[],
            )
        except Exception as e:
            safe_log(f"[fallback] LLM request failed: {e}")
            return
        matches = re.findall(r'```python\s*\n(.*?)```', content or '', flags=re.DOTALL)
        if not matches:
            safe_log("[fallback] No ```python fenced block found in model response.")
            return
        code = matches[-1]
        target = os.path.join(self.git_tempdir, target_rel)
        try:
            os.makedirs(os.path.dirname(target) or '.', exist_ok=True)
            with open(target, 'w') as f:
                f.write(code)
            safe_log(f"[fallback] Wrote {len(code)} chars to {target}")
        except OSError as e:
            safe_log(f"[fallback] Could not write {target}: {e}")

    def _write_minimal_program(self):
        """Final safety net: write a minimal valid stdin-reading program to solution.py if it is missing."""
        target = os.path.join(self.git_tempdir, 'solution.py')
        if os.path.exists(target):
            return
        code = "import sys\n\n\ndef main():\n    data = sys.stdin.read()\n\n\nif __name__ == '__main__':\n    main()\n"
        try:
            with open(target, 'w') as f:
                f.write(code)
            safe_log(f"[safety] Wrote minimal program to {target}")
        except OSError as e:
            safe_log(f"[safety] Could not write {target}: {e}")

    def _diff_summary(self):
        changed = self._changed_files()
        if not changed:
            return "no changes"
        return "\n".join(f"- {f}" for f in changed)

    def _run_samples_check(self):
        """
        Run the sample runner programmatically on the deliverable solution.py.
        Returns (all_pass, report_text).
        """
        solution_path = os.path.join(self.git_tempdir, 'solution.py')
        if not os.path.exists(solution_path):
            return False, f"{solution_path} does not exist; no samples could be run."
        try:
            report = run_samples_tool(problem_text=self.problem_statement, solution_path=solution_path)
        except Exception as e:
            safe_log(f"[samples] run_samples failed: {e}")
            return False, f"run_samples could not be executed: {e}"
        all_pass = 'DIFFERS' not in report and 'No sample input/output pairs' not in report
        return all_pass, report

    @staticmethod
    def _is_empty_turn(history):
        """
        True if history is not a usable list, or its last assistant message has no tool_use
        and no non-whitespace text.
        """
        if not isinstance(history, list) or not history:
            return True
        last = history[-1]
        if not isinstance(last, dict) or last.get('role') != 'assistant':
            return False
        content = last.get('content', [])
        if isinstance(content, str):
            return content.strip() == ''
        if not isinstance(content, list):
            return True
        for block in content:
            if isinstance(block, dict):
                if block.get('type') == 'tool_use':
                    return False
                if block.get('type') == 'text' and str(block.get('text', '')).strip():
                    return False
            elif block:
                return False
        return True

    def forward(self):
        """
        The forward function for the AgenticSystem.
        """
        # Store the problem statement so the run_samples tool can read it
        try:
            with open('/tmp/problem.md', 'w') as f:
                f.write(self.problem_statement or '')
        except Exception as e:
            safe_log(f"Could not write /tmp/problem.md: {e}")

        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        workflow = """
If the problem is a standard input/output program, the deliverable is a Python file named solution.py in the repository root (create it with the editor tool if it does not exist). If the problem asks for a method of a given `Solution` class, edit the file that contains that class.

Follow these steps explicitly, calling the tools as you go:
1. Explore the repository with the editor tool (view directories and files) and bash (ls, cat, etc.) to understand the existing code and the expected interface.
2. Reason about the algorithm: restate the problem, derive a correct algorithm, and check its time and memory complexity against the input constraints.
3. Create or edit the deliverable source file (e.g. solution.py) with the editor tool. Write a complete implementation, not a partial sketch.
4. Run the program on the sample inputs from the problem statement with bash and check that the output matches the expected output.
5. Call the run_samples tool with the problem statement (the full text is also saved in /tmp/problem.md) and the path of your solution file. It reports PASS or DIFFERS for every sample, with the expected and actual outputs.
   - If any sample DIFFERS, treat it as a probable failure even if the statement says that any valid answer is accepted: the grader may compare outputs exactly. Do not stop at a valid-looking answer.
   - Study how the expected sample outputs are constructed (ordering, which values are chosen, tie-breaking such as smallest or largest, canonical choice, bit layout, output format) and revise the algorithm so that your output matches every sample byte for byte.
   - Only keep a differing output if no natural deterministic construction reproduces the samples. In that case, state explicitly in your final reply that you could not match the samples and why.
6. Where feasible, write a brute-force version and compare it against your solution on many small random inputs using bash. Fix any mismatches.
7. Fix and optimize the solution based on the test results, making sure it meets the constraints. Re-run run_samples after every change to the solution.

Important: Replying without calling tools, or ending your turn without having written or edited the source/deliverable file, counts as failure. Do not only modify test files; the actual source file must be implemented.
"""
        instruction = (f"{task}\n\n{workflow}\nPlease analyze the problem description carefully. Then make edits to the code files to complete the instruction.\n\n"
                f"HARD REQUIREMENT: Your FIRST action must be an editor tool call (command create) that writes a complete draft solution to {self.git_tempdir}/solution.py. Do not reply with text only.")

        msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        if self._is_empty_turn(msg_history):
            safe_log("[empty-turn] Initial turn returned no tool calls and no text; retrying on a fresh context.")
            msg_history = []
        elif not isinstance(msg_history, list):
            msg_history = []

        retry_prompt = (
            f"{self.problem_statement}\n\n"
            f"Your FIRST action must be an editor tool call (command create) that writes a complete draft solution to "
            f"{self.git_tempdir}/solution.py. Do not reply with text only. "
            f"FIRST ACTION: call the editor tool with command create, path {self.git_tempdir}/solution.py, and a complete draft."
        )
        for attempt in range(1, 4):
            if self._has_meaningful_edit():
                break
            reason = (
                f"no meaningful source edits detected (changed files: {self._diff_summary()}); "
                "the diff is empty, touches only test files, or is missing a deliverable file named in the problem"
            )
            safe_log(f"[retry {attempt}/3] Retrying: {reason}")
            # Always start from a fresh context so an empty assistant turn is never reused.
            new_history = chat_with_agent(retry_prompt, model=self.code_model, msg_history=[], logging=safe_log)
            if self._is_empty_turn(new_history):
                safe_log("[empty-turn] Model returned an empty turn with no tool calls; going to next retry.")
                msg_history = []
                continue
            msg_history = new_history

        if not self._has_meaningful_edit():
            safe_log("[retry] No meaningful source edit after retries; trying fallback.")
        self._fallback_write_solution()
        if not self._has_meaningful_edit():
            safe_log("[retry] Still no meaningful source edit after fallback.")

        # Bounded post-run sample check: feed any DIFFERS output back to the agent
        for attempt in range(1, 3):
            all_pass, report = self._run_samples_check()
            safe_log(f"[samples {attempt}/2] {'all samples PASS' if all_pass else 'some samples DIFFER'}")
            if all_pass:
                break
            follow_up = (
                "The sample runner (run_samples) reports that your solution does not reproduce the expected sample outputs:\n\n"
                f"{report}\n\n"
                "The grader may compare outputs exactly, so a DIFFERS result is a probable failure even if several answers "
                "are allowed. Analyse how the expected outputs were constructed (ordering, tie-breaking, canonical choice, "
                "bit layout, output format), adapt the algorithm with the editor tool so that every sample matches byte for byte, "
                "then re-run the samples. If no natural deterministic construction reproduces the samples, keep the best answer "
                "and explain in your reply why it cannot be matched."
            )
            sanitized = self._sanitize_history(msg_history)
            if not sanitized:
                # No usable history (e.g. after an empty turn or fallback): give full context in the turn.
                follow_up = f"{task}\n\n{follow_up}"
            msg_history = chat_with_agent(follow_up, model=self.code_model, msg_history=sanitized, logging=safe_log)
            if not isinstance(msg_history, list):
                break
        self._write_minimal_program()


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

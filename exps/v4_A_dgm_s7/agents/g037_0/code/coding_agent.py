import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import threading

from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
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
        Return the list of file paths changed in the repo versus base_commit,
        parsed from the 'diff --git a/... b/...' header lines.
        """
        diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        files = []
        for line in diff.splitlines():
            if line.startswith('diff --git'):
                parts = line.split(' b/')
                if len(parts) >= 2:
                    files.append(parts[-1].strip())
        return files

    @staticmethod
    def _is_test_path(path):
        p = path.lower()
        return any(s in p for s in ['/test', 'tests/', 'test_', '_test.', '.spec.', 'conftest'])

    @staticmethod
    def _block_text(block):
        if isinstance(block, dict):
            return block.get('type'), block.get('text')
        return getattr(block, 'type', None), getattr(block, 'text', None)

    @staticmethod
    def _sanitize_history(msg_history):
        """
        Drop trailing assistant messages whose content blocks are all empty text.
        Returns [] if no meaningful messages remain.
        """
        history = list(msg_history or [])
        while history:
            last = history[-1]
            if last.get('role') != 'assistant':
                break
            content = last.get('content')
            if isinstance(content, str):
                if content.strip():
                    break
                history.pop()
                continue
            blocks = content or []
            all_empty = True
            for block in blocks:
                btype, text = AgenticSystem._block_text(block)
                if btype != 'text' or (text or '').strip():
                    all_empty = False
                    break
            if all_empty:
                history.pop()
            else:
                break
        return history

    def _target_filename(self):
        """
        Extract the expected output file (a backticked *.py name) from the problem statement.
        Defaults to 'solution.py'.
        """
        match = re.search(r'`([\w./-]+\.py)`', self.problem_statement or '')
        return match.group(1) if match else 'solution.py'

    @staticmethod
    def _last_assistant_text(msg_history):
        for msg in reversed(msg_history or []):
            if msg.get('role') != 'assistant':
                continue
            content = msg.get('content')
            if isinstance(content, str):
                return content
            texts = []
            for block in content or []:
                btype, text = AgenticSystem._block_text(block)
                if btype == 'text' and text:
                    texts.append(text)
            if texts:
                return "\n".join(texts)
        return ""

    def _has_source_edit(self):
        """
        True if at least one changed file is not a test file.
        """
        return any(not self._is_test_path(f) for f in self._changed_files())

    @staticmethod
    def _last_assistant_is_empty(msg_history):
        """True if the last assistant message has no text and no tool use."""
        for msg in reversed(msg_history or []):
            if msg.get('role') != 'assistant':
                continue
            content = msg.get('content')
            if isinstance(content, str):
                return not content.strip()
            for block in content or []:
                btype, text = AgenticSystem._block_text(block)
                if btype == 'tool_use' or (btype == 'text' and (text or '').strip()):
                    return False
                if btype not in (None, 'text'):
                    return False
            return True
        return True

    def _run_sample_gate(self):
        """
        Objective check (no LLM): run the target file on the problem's samples.
        Returns (all_passed, report).
        """
        target_path = os.path.join(self.git_tempdir, self._target_filename())
        report = run_samples_tool(target_path, self.problem_statement or '')
        all_passed = (
            'ALL SAMPLES PASSED.' in report
            and 'SOME SAMPLES FAILED.' not in report
            and not report.startswith('Error:')
        )
        return all_passed, report

    @staticmethod
    def _ends_with_verified(text):
        lines = [l.strip() for l in (text or '').splitlines() if l.strip()]
        return bool(lines) and lines[-1] == 'VERIFIED'

    def _chat(self, prompt, msg_history, fresh_prefix, max_nudges=2):
        """
        Send prompt within the existing conversation (or a fresh one if the history is empty).
        If the assistant returns an empty turn, send a 'continue' nudge instead of
        treating it as a completed round.
        """
        sanitized = self._sanitize_history(msg_history)
        if sanitized:
            new_history = chat_with_agent(prompt, model=self.code_model, msg_history=sanitized, logging=safe_log)
        else:
            new_history = chat_with_agent(f"{fresh_prefix}\n\n{prompt}", model=self.code_model, msg_history=[], logging=safe_log)
        for nudge in range(1, max_nudges + 1):
            if not self._last_assistant_is_empty(new_history):
                break
            safe_log(f"Empty assistant turn; sending continue nudge {nudge}/{max_nudges}")
            new_history = chat_with_agent(
                "Your last reply was empty. Continue working on the task now, and use your tools.",
                model=self.code_model,
                msg_history=self._sanitize_history(new_history) or new_history,
                logging=safe_log,
            )
        return new_history

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

Please follow this workflow:
1. Explore the repository: list the files and find the target file named in the task (e.g. solution.py). If the task asks for a complete program reading stdin and writing stdout, write that program; if it asks for a method of a given `Solution` class, implement that method in the provided file.
2. Before coding, write a short complexity analysis: state the input constraints (maximum N, value ranges) and the time complexity your algorithm needs to meet them in Python. If a naive approach would be too slow, choose a better algorithm now.
3. Create or edit the target file with the editor tool (create/edit). Implement the full, complete solution, not a stub.
4. Run the solution via bash on all sample inputs in the problem statement and compare the output with the expected outputs. Fix any mismatch.
5. Consider edge cases (empty input, minimum/maximum values, duplicates, large inputs) and check that the time complexity is acceptable for the maximum constraints. Any brute-force reference you use for testing must be independent code written from scratch (do not import or copy from the solution under test). A solution that times out on the provided samples is NOT an acceptable final answer; keep analyzing brute-force output (print compact tables, hypothesize formulas, test them against brute force) until the efficient solution matches.
6. Only finish once the source file is written and verified. A reply without file edits counts as failure."""
        instruction = f"{task}\n\nPlease analyze the problem description carefully. Then make edits to the code files to complete the instruction.{workflow}"
        msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)

        target = self._target_filename()
        retry_templates = [
            (
                "No edits to non-test source files were detected in the repository. "
                f"Immediately call the editor tool to create {target} with an algorithm that meets the constraints: design it, state its complexity, and write it. "
                " Do not reply with text only. After writing, run it against the sample inputs."
            ),
            (
                "Still no edits to non-test source files. "
                f"Immediately call the editor tool to create {target} with an algorithm that meets the constraints: design it, state its complexity, and write it. "
                " Do not reply with text only."
            ),
            (
                "Final attempt: no source file has been written yet. "
                f"Immediately call the editor tool to create {target} with an algorithm that meets the constraints: design it, state its complexity, and write it. "
                " Do not reply with text only. "
                f"If {target} does not exist, you must create it now."
            ),
        ]

        max_attempts = 3
        for attempt in range(max_attempts):
            if self._has_source_edit():
                break
            safe_log(f"No source edits detected; retry attempt {attempt + 1}/{max_attempts}")
            retry_msg = retry_templates[attempt]
            try:
                sanitized = self._sanitize_history(msg_history)
                if sanitized:
                    safe_log(f"Retrying within existing conversation ({len(sanitized)} messages)")
                    msg_history = chat_with_agent(retry_msg, model=self.code_model, msg_history=sanitized, logging=safe_log)
                else:
                    safe_log("Conversation history empty after sanitizing; starting fresh conversation")
                    msg_history = chat_with_agent(
                        f"{instruction}\n\n{retry_msg}",
                        model=self.code_model,
                        msg_history=[],
                        logging=safe_log,
                    )
            except Exception as e:
                safe_log(f"Exception during retry attempt {attempt + 1}/{max_attempts}: {e}", level=logging.ERROR)
                msg_history = []

        if not self._has_source_edit():
            safe_log("Still no source edit after retries; running final code-block fallback")
            try:
                fallback_msg = (
                    "Output ONLY the complete Python 3 program for the task in a single ```python code block, nothing else. "
                    "Make it a simple correct solution that reads from standard input and writes to standard output."
                )
                fallback_history = chat_with_agent(
                    f"{instruction}\n\n{fallback_msg}",
                    model=self.code_model,
                    msg_history=[],
                    logging=safe_log,
                )
                text = self._last_assistant_text(fallback_history)
                match = re.search(r'```(?:python|py)?[ \t]*\n(.*?)```', text, re.DOTALL)
                if match and match.group(1).strip():
                    code = match.group(1)
                    out_path = os.path.join(self.git_tempdir, target)
                    out_dir = os.path.dirname(out_path)
                    if out_dir:
                        os.makedirs(out_dir, exist_ok=True)
                    if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
                        with open(out_path, 'w') as f:
                            f.write(code)
                        safe_log(f"Fallback wrote code block to {out_path}")
                    else:
                        safe_log(f"Fallback skipped: {out_path} already exists and is non-empty")
                else:
                    safe_log("Fallback failed: no fenced code block found in response", level=logging.WARNING)
            except Exception as e:
                safe_log(f"Exception during fallback: {e}", level=logging.ERROR)

        # Verify-and-harden phase: objective sample gate drives redesign; bounded rounds, no while loop.
        fresh_prefix = instruction
        stress_prompt = (
            "Samples pass. Now harden the solution: "
            "(a) state the worst-case time complexity against the maximum constraints; "
            "(b) write an independent brute.py (written from scratch, NOT imported from the solution) and gen.py "
            "(takes a seed argument, prints small random inputs, including edge cases like duplicates, minimum N, "
            "and answer-absent cases) in a scratch directory such as /tmp/verify, NOT inside the repository; "
            "(c) use the stress_test tool for at least 300 cases with brute_cmd and generator_cmd (checker_cmd if multiple answers are valid); "
            "(d) generate max-size worst-case inputs and time the solution with the time_run tool; it must run in under ~2s. "
            "Fix any failure and re-run the checks. "
            "When everything passes, end your final message with the line VERIFIED on its own as the last line."
        )
        verify_rounds = 4
        stress_done = False
        for verify_round in range(verify_rounds):
            if not self._has_source_edit():
                safe_log("Verification skipped: no source edit present")
                break
            try:
                passed, report = self._run_sample_gate()
            except Exception as e:
                safe_log(f"Sample gate exception: {e}", level=logging.ERROR)
                break
            safe_log(f"Sample gate round {verify_round + 1}/{verify_rounds}: {'PASS' if passed else 'FAIL'}\n{report}")

            try:
                if not passed:
                    prompt = (
                        "The solution fails these samples/time limits:\n\n"
                        f"{report}\n\n"
                        "The approach is likely algorithmically insufficient (especially if there is a TIMEOUT). "
                        "Do not just patch constants. Analyze the brute-force output for structure, find a closed form "
                        "or a faster algorithm that meets the maximum constraints, rewrite the solution file "
                        f"{target}, and re-run the samples with the run_samples tool. "
                        "Use an independent brute force only for checking small cases."
                    )
                    msg_history = self._chat(prompt, msg_history, fresh_prefix)
                    continue

                if not stress_done:
                    stress_done = True
                    msg_history = self._chat(stress_prompt, msg_history, fresh_prefix)
                    continue

                # Gate passed and the agent has hardened it: require final VERIFIED line AND gate pass.
                msg_history = self._chat(
                    "Re-check the solution. If everything passes, reply with the line VERIFIED as the last line of your message.",
                    msg_history, fresh_prefix,
                )
                break
            except Exception as e:
                safe_log(f"Exception during verification round {verify_round + 1}/{verify_rounds}: {e}", level=logging.ERROR)
                break

        passed, report = self._run_sample_gate()
        final_text = self._last_assistant_text(msg_history)
        if passed and self._ends_with_verified(final_text):
            safe_log("Verified: sample gate passed and final line is VERIFIED")
        else:
            safe_log(f"Not verified: gate passed={passed}, final VERIFIED line={self._ends_with_verified(final_text)}")

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

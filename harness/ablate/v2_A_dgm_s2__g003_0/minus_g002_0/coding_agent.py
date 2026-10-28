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

def _changed_files(diff: str) -> list[str]:
    """
    Extract changed file paths from 'diff --git a/X b/Y' header lines.
    """
    paths = []
    for match in re.finditer(r'^diff --git a/(.+?) b/(.+)$', diff or '', flags=re.MULTILINE):
        path = match.group(2).strip()
        if path not in paths:
            paths.append(path)
    return paths

def _is_test_path(path: str) -> bool:
    """
    Heuristically determine whether a path refers to a test file.
    """
    normalized = path.replace('\\', '/')
    parts = [p for p in normalized.split('/') if p]
    if not parts:
        return False
    name = parts[-1]
    lower_dirs = [p.lower() for p in parts[:-1]]
    if any(d in ('test', 'tests') for d in lower_dirs):
        return True
    lower_name = name.lower()
    if lower_name.startswith('test_') or lower_name == 'conftest.py':
        return True
    if (lower_name.endswith('_test.py') or lower_name.endswith('.spec.js')
            or lower_name.endswith('_test.go') or lower_name.endswith('_test.rs')
            or name.endswith('Test.java')):
        return True
    return False

def _needs_retry(diff):
    """
    Return a reason string if the diff is empty or only touches test files; otherwise None.
    """
    if diff is None or not str(diff).strip():
        return "no changes were made to the repository (the diff is empty)"
    files = _changed_files(str(diff))
    if files and all(_is_test_path(f) for f in files):
        return f"only test files were changed ({', '.join(files)}); no source/solution file was modified"
    if not files:
        return "no changed files could be identified in the diff"
    return None

def _gather_repo_context(git_tempdir, max_chars=8000):
    """
    Build a compact snapshot of the repository: tracked file list plus contents of
    small, non-test source files (solution/main files and files containing 'class Solution' first).
    """
    files = []
    try:
        result = subprocess.run(
            ["git", "-C", git_tempdir, "ls-files"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        files = [f for f in result.stdout.decode(errors='replace').splitlines() if f.strip()]
    except Exception:
        files = []
    if not files:
        for root, dirs, names in os.walk(git_tempdir):
            dirs[:] = [d for d in dirs if d != '.git']
            for name in names:
                files.append(os.path.relpath(os.path.join(root, name), git_tempdir))

    candidates = []
    for f in files:
        if _is_test_path(f) or f.startswith('.'):
            continue
        full = os.path.join(git_tempdir, f)
        if not os.path.isfile(full) or os.path.getsize(full) > 20000:
            continue
        try:
            with open(full, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except Exception:
            continue
        name = os.path.basename(f)
        if name == 'solution.py':
            rank = 0
        elif name == 'main.py':
            rank = 1
        elif 'class Solution' in content:
            rank = 2
        elif f.endswith('.py'):
            rank = 3
        else:
            continue
        candidates.append((rank, f, content))
    candidates.sort(key=lambda c: (c[0], c[1]))

    parts = [f"Tracked files:\n" + "\n".join(files[:200])]
    used = len(parts[0])
    for _, f, content in candidates:
        block = f"\n\n--- {f} ---\n{content}"
        if used + len(block) > max_chars:
            remaining = max_chars - used
            if remaining > 200:
                parts.append(block[:remaining])
            break
        parts.append(block)
        used += len(block)
    return "".join(parts)[:max_chars]

def _has_tool_use(msg_history):
    """
    Return True if the message history contains any tool call (Claude 'tool_use' blocks,
    OpenAI 'function_call' items, or manual '<tool_use>' text). Logs when none are found.
    """
    found = False
    for msg in msg_history or []:
        if isinstance(msg, dict):
            if msg.get('type') in ('function_call', 'function_call_output'):
                found = True
                break
            content = msg.get('content')
        else:
            if getattr(msg, 'type', None) == 'function_call' or getattr(msg, 'tool_calls', None):
                found = True
                break
            content = getattr(msg, 'content', None)
        if isinstance(content, str):
            if '<tool_use>' in content:
                found = True
                break
            continue
        for block in content or []:
            if isinstance(block, dict):
                btype = block.get('type')
                text = block.get('text') or ''
            else:
                btype = getattr(block, 'type', None)
                text = getattr(block, 'text', None) or ''
            if btype == 'tool_use' or (isinstance(text, str) and '<tool_use>' in text):
                found = True
                break
        if found:
            break
    if not found:
        safe_log("The model finished without using any tool (no tool calls in the response).")
    return found

def _last_assistant_text(msg_history):
    """
    Return the text of the last assistant message in msg_history, or '' if none.
    """
    for msg in reversed(msg_history or []):
        if isinstance(msg, dict):
            role, content = msg.get('role'), msg.get('content')
        else:
            role, content = getattr(msg, 'role', None), getattr(msg, 'content', None)
        if role != 'assistant':
            continue
        if isinstance(content, str):
            return content
        texts = []
        for block in content or []:
            if isinstance(block, dict):
                if block.get('type') == 'text' and block.get('text'):
                    texts.append(block['text'])
            elif getattr(block, 'type', None) == 'text' and getattr(block, 'text', None):
                texts.append(block.text)
        if texts:
            return "\n".join(texts)
    return ''

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
        instruction = f"""{task}

Please analyze the problem description carefully, then follow this workflow:
1. Explore the repository with the editor `view` command or bash (e.g. `ls`, `cat`) to find the target file. If the task names a file such as `solution.py` that does not exist yet, create it.
2. Implement the complete solution by actually calling the editor tool to write the code to disk. Do not only describe the solution in text.
3. Run the program on the sample inputs with bash and compare the output against the expected outputs. Fix any discrepancies.
4. Consider time complexity (e.g. N up to 10^6) and test with a large input to make sure the solution is fast enough.
5. Do not stop until the source file is saved on disk with the full solution.

IMPORTANT: The task is incomplete until a source file has been created or edited with the editor or bash tool. Ending your turn without writing code to disk is a failure. If the task says to write a program in a file such as `solution.py`, you must ensure that file exists with the full solution."""
        init_edit = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
        msg_history = init_edit if isinstance(init_edit, list) else []

        repo_context = _gather_repo_context(self.git_tempdir)
        retry_prompts = [
            "Your previous attempt made no changes to the repository. Your first action must be an editor tool call that creates or edits the solution file. Do not reply with text only.",
            "No solution file was written last time. Start now: use the editor tool to write the complete solution into the primary solution file (not a test file). Do not reply with text only.",
            "Still no code on disk. Immediately call the editor tool to create or overwrite solution.py with a full implementation, then test it with bash. Do not reply with text only.",
        ]
        for attempt in range(3):
            diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
            reason = _needs_retry(diff)
            if reason is None:
                safe_log(f"Patch validation passed on attempt {attempt}.")
                break
            safe_log(f"Patch validation failed on attempt {attempt}: {reason}. Retrying with fresh history.")
            retry_msg = f"""Original task:
{task}

Repository snapshot:
{repo_context}

{retry_prompts[attempt % len(retry_prompts)]}"""
            retry_result = chat_with_agent(retry_msg, model=self.code_model, msg_history=[], logging=safe_log)
            if not _has_tool_use(retry_result):
                safe_log("Retry finished without any tool call; the next attempt will start from a fresh history.")
        diff = str(diff_versus_commit(self.git_tempdir, self.base_commit))
        reason = _needs_retry(diff)
        if reason is None:
            return
        safe_log(f"Patch validation still failing after maximum retries: {reason}. Running deterministic fallback.")
        self._fallback_write_solution(task, repo_context)

    def _fallback_write_solution(self, task, repo_context):
        """
        Ask the model for only the full solution file contents and write them to the target file.
        """
        target_rel = None
        for f in re.findall(r'^--- (.+?) ---$', repo_context, flags=re.MULTILINE):
            if not _is_test_path(f) and f.endswith('.py') and os.path.basename(f) == 'solution.py':
                target_rel = f
                break
        if target_rel is None:
            target_rel = 'solution.py'
        target_path = os.path.join(self.git_tempdir, target_rel)
        fallback_msg = f"""{task}

Repository snapshot:
{repo_context}

Reply with ONLY the complete contents of `{target_rel}` (a full, working Python implementation including the starter class/method signature shown above) inside a single ```python fenced code block. No other text, no tool calls."""
        fallback_result = chat_with_agent(fallback_msg, model=self.code_model, msg_history=[], logging=safe_log)
        text = _last_assistant_text(fallback_result)
        match = re.search(r'```python\s*\n(.*?)```', text, flags=re.DOTALL)
        if not match:
            safe_log("Fallback failed: no ```python code block in the model reply.")
            return
        code = match.group(1)
        os.makedirs(os.path.dirname(target_path) or '.', exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(code)
        safe_log(f"Fallback wrote {len(code)} chars to {target_path}.")

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

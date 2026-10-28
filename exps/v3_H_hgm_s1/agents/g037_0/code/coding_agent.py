import argparse
import ast
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import threading

from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
from utils.git_utils import diff_versus_commit, reset_to_commit, apply_patch, has_source_edits, list_non_test_tracked_files, read_starter_files, is_test_file

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

def _block_field(block, name):
    if isinstance(block, dict):
        return block.get(name)
    return getattr(block, name, None)

def _last_assistant_is_empty(msg_history):
    """
    Return True if the last message is an assistant turn whose content blocks are all
    text with empty/whitespace-only strings (no tool_use blocks).
    """
    if not msg_history:
        return False
    last = msg_history[-1]
    if _block_field(last, 'role') != 'assistant':
        return False
    content = _block_field(last, 'content')
    if isinstance(content, str):
        empty = not content.strip()
        safe_log(f"[_last_assistant_is_empty] last assistant message is {'empty' if empty else 'non-empty'} (string content).")
        return empty
    if not content:
        safe_log("[_last_assistant_is_empty] last assistant message has no content blocks -> empty.")
        return True
    for block in content:
        if _block_field(block, 'type') == 'tool_use':
            safe_log("[_last_assistant_is_empty] last assistant message contains tool_use -> not empty.")
            return False
        if _block_field(block, 'type') != 'text':
            safe_log("[_last_assistant_is_empty] last assistant message has a non-text block -> not empty.")
            return False
        text = _block_field(block, 'text')
        if text is not None and str(text).strip():
            safe_log("[_last_assistant_is_empty] last assistant message has non-whitespace text -> not empty.")
            return False
    safe_log("[_last_assistant_is_empty] last assistant message is text-only and whitespace -> empty.")
    return True

def _last_assistant_text(msg_history):
    """Concatenate the text of the last assistant message (empty string if none)."""
    for msg in reversed(msg_history or []):
        if _block_field(msg, 'role') != 'assistant':
            continue
        content = _block_field(msg, 'content')
        if isinstance(content, str):
            return content
        parts = []
        for block in content or []:
            text = _block_field(block, 'text')
            if text:
                parts.append(str(text))
        return "\n".join(parts)
    return ""

def _guess_target_file(problem_statement, git_tempdir):
    """
    Guess the solution file: a backticked filename with a code extension in the statement,
    else the first non-test tracked file, else 'solution.py'.
    """
    for match in re.finditer(r'`([\w./-]+\.(py|cpp|java|go|rs|js))`', problem_statement or ''):
        if not is_test_file(match.group(1)):
            return match.group(1)
    files = list_non_test_tracked_files(git_tempdir)
    if files:
        return files[0]
    return 'solution.py'

def _last_tool_result_text(msg_history, limit=2000):
    """Return the text of the most recent tool result in the history ('' if none)."""
    for msg in reversed(msg_history or []):
        content = _block_field(msg, 'content')
        if isinstance(content, str):
            if content.startswith('Tool Result:'):
                return content[:limit]
            continue
        for block in content or []:
            if _block_field(block, 'type') == 'tool_result':
                result = _block_field(block, 'content')
                if isinstance(result, list):
                    result = "\n".join(str(_block_field(b, 'text') or b) for b in result)
                return str(result)[:limit]
            text = _block_field(block, 'text')
            if text and str(text).startswith('Tool Result:'):
                return str(text)[:limit]
    return ""

def _build_nudge(msg_history):
    """Build the nudge sent after an empty assistant turn, quoting the latest tool output."""
    last_output = _last_tool_result_text(msg_history)
    if not last_output:
        last_output = "(no tool output yet)"
    return ("Your last reply was empty. Continue by calling a tool now; "
            f"the previous tool output was: {last_output}")

def _as_content_list(content):
    if content is None:
        return []
    if isinstance(content, str):
        return [{'type': 'text', 'text': content}]
    return list(content)

def _is_empty_assistant_message(msg):
    """True if msg is an assistant turn with no tool_use and only empty/whitespace text."""
    if _block_field(msg, 'role') != 'assistant':
        return False
    content = _as_content_list(_block_field(msg, 'content'))
    if not content:
        return True
    for block in content:
        if isinstance(block, str):
            if block.strip():
                return False
            continue
        if _block_field(block, 'type') == 'tool_use':
            return False
        if _block_field(block, 'type') != 'text':
            return False
        text = _block_field(block, 'text')
        if text is not None and str(text).strip():
            return False
    return True

def _sanitize_history(msg_history):
    """
    Return a copy of msg_history with empty assistant turns removed and adjacent
    same-role messages merged (content lists concatenated). Input is not modified.
    """
    sanitized = []
    for msg in msg_history or []:
        if _is_empty_assistant_message(msg):
            safe_log("[_sanitize_history] dropped empty assistant message.")
            continue
        role = _block_field(msg, 'role')
        content = _as_content_list(_block_field(msg, 'content'))
        if sanitized and _block_field(sanitized[-1], 'role') == role:
            prev = _as_content_list(_block_field(sanitized[-1], 'content'))
            sanitized[-1] = {'role': role, 'content': prev + content}
        else:
            sanitized.append({'role': role, 'content': content})
    return sanitized

_DOC_EXTENSIONS = ('.md', '.txt', '.rst')

def _is_redundant_context(rel_path, text, problem_statement):
    """
    True if a starter file should be skipped in the prompt: documentation files,
    empty files, or files whose opening content already appears in the problem statement.
    """
    if os.path.splitext(rel_path)[1].lower() in _DOC_EXTENSIONS:
        return True
    stripped = (text or '').strip()
    if not stripped:
        return True
    if problem_statement:
        norm_stmt = ' '.join(problem_statement.split())
        norm_text = ' '.join(stripped[:200].split())
        if norm_text and norm_text in norm_stmt:
            return True
    return False

def _run_until_nonempty(prompt, model, history, max_nudges=3):
    """
    Call chat_with_agent with `prompt`. If the resulting last assistant turn is empty,
    re-call with the SAME history plus a nudge built from the latest tool result,
    up to `max_nudges` times. Returns the updated message history; if the turn stays
    empty, returns anyway so the caller can fall back (e.g. to the saved draft).
    """
    msg_history = chat_with_agent(prompt, model=model, msg_history=_sanitize_history(history), logging=safe_log)
    for nudge_idx in range(max_nudges):
        if not _last_assistant_is_empty(msg_history):
            break
        safe_log(f"[_run_until_nonempty] Empty assistant turn; nudge {nudge_idx + 1}/{max_nudges}.")
        msg_history = chat_with_agent(_build_nudge(msg_history), model=model, msg_history=_sanitize_history(msg_history), logging=safe_log)
        if _last_assistant_is_empty(msg_history):
            safe_log(f"[_run_until_nonempty] Nudge {nudge_idx + 1}/{max_nudges} also returned an empty turn.")
    else:
        if _last_assistant_is_empty(msg_history):
            safe_log(f"[_run_until_nonempty] Still empty after {max_nudges} nudges; returning to caller.")
    return msg_history

def _read_stub_context(git_tempdir, problem_statement=''):
    """Return the non-test tracked files and their contents as a prompt-ready string,
    skipping docs and files already contained in the problem statement."""
    parts = []
    for rel_path, text in read_starter_files(git_tempdir):
        if _is_redundant_context(rel_path, text, problem_statement):
            safe_log(f"[_read_stub_context] skipping redundant context file: {rel_path}")
            continue
        parts.append(f"### {rel_path}\n```\n{text}\n```")
    return "\n\n".join(parts) if parts else "(no starter files found)"

def _extract_code(text):
    """
    Extract solution code from a reply. Accepts fenced blocks with or without a language tag;
    falls back to the whole text if it parses as Python. Returns None if nothing usable.
    """
    text = text or ''
    blocks = re.findall(r'```[ \t]*[\w+-]*[ \t]*\n(.*?)```', text, re.DOTALL)
    blocks = [b for b in blocks if b.strip()]
    if blocks:
        return max(blocks, key=len)
    try:
        ast.parse(text)
        if text.strip():
            return text
    except SyntaxError:
        pass
    return None

SKELETON_CODE = """import sys


def main():
    data = sys.stdin.read().split()
    # TODO: implement the solution
    print(data)


if __name__ == "__main__":
    main()
"""

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

    def _draft_solution(self, target_file):
        """
        Tool-free draft stage: ask the model for the full target file, validate it, and write it.
        Each variant starts from a fresh history. Returns the draft code, or None if none was produced.
        """
        stub_context = _read_stub_context(self.git_tempdir, self.problem_statement)
        statement_block = f"""<problem_description>
{self.problem_statement}
</problem_description>"""
        stub_block = f"Starter files in the repository:\n{stub_context}"
        prompt_variants = [
            # Variant 1: statement + stub, code only
            f"{statement_block}\n\n{stub_block}\n\n"
            f"Reply with a single python code block only (```python ... ```) containing the full solution for {target_file}. No tools, no prose.",
            # Variant 2: brief reasoning, then code
            f"{statement_block}\n\n{stub_block}\n\n"
            f"No tools. First reason briefly in exactly 3 bullet points (approach, edge cases, complexity), "
            f"then give the complete {target_file} in one ```python fenced block.",
            # Variant 3: edit-only, editor tool allowed
            f"I have uploaded a code repository in the directory {self.git_tempdir}. "
            f"Solve the problem below by writing the full solution to {target_file} with the editor tool "
            f"(command=edit or create), then reply with one word: done.\n\n{statement_block}\n\n{stub_block}",
        ]
        is_python = target_file.endswith('.py')
        empty_count = 0
        for idx, prompt in enumerate(prompt_variants):
            history = chat_with_agent(prompt, model=self.code_model, msg_history=[], logging=safe_log)
            reply = _last_assistant_text(history)
            if not reply.strip():
                empty_count += 1
                safe_log(f"[_draft_solution] Variant {idx + 1}: empty reply (empty_count={empty_count}).")
                continue
            code = _extract_code(reply)
            if code is None or not code.strip():
                safe_log(f"[_draft_solution] Variant {idx + 1}: no code extracted.")
                continue
            if is_python:
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    safe_log(f"[_draft_solution] Variant {idx + 1}: syntax error: {e}.")
                    continue
            out_path = os.path.join(self.git_tempdir, target_file)
            os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
            with open(out_path, 'w') as f:
                f.write(code)
            safe_log(f"[_draft_solution] Wrote draft ({len(code)} chars) to {out_path} (variant {idx + 1}).")
            return code
        safe_log(f"[_draft_solution] All draft variants failed; empty_count={empty_count}.")
        return None

    def forward(self):
        """
        The forward function for the AgenticSystem.
        """
        target_file = _guess_target_file(self.problem_statement, self.git_tempdir)
        safe_log(f"[forward] Guessed target file: {target_file}")
        draft_code = self._draft_solution(target_file)
        safe_log(f"[forward] Draft stage produced draft: {draft_code is not None}.")

        task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
        instruction = f"""{task}

Follow these steps in order:
Step 1: ls and cat the stub. Read the starter file(s) (e.g. with bash `cat`, `ls`, `find`) to learn the required function/class signature and any existing tests.
Step 2: A draft solution already exists in {target_file}. Read it, run it on the examples and a brute-force comparison, and fix or improve it using the editor tool. Keep the required signature and make sure imports are correct.
Step 3: test and refine, re-editing the file as needed. Run the problem's examples and a brute-force comparison on small random inputs via bash, and fix any mismatches or errors in the source file with the editor tool. If the problem is interactive, use print(..., flush=True) and input(), and test with a small local judge script you write yourself.
Step 4: Final check: confirm via `git diff` (or equivalent) that the diff contains changes to the primary source file.

Rules:
- You MUST modify the source file using the editor tool; never finish your turn with an empty reply or only a plan.
- Do not only modify test files; the primary source file must contain the solution.
- Do not end your turn until the implementation is written to disk.
- Never end a turn with an empty message; end each turn with a short text summary.
"""
        msg_history = _run_until_nonempty(instruction, self.code_model, [])
        safe_log(f"[forward] Initial pass complete; {len(msg_history)} messages in history.")

        patch = diff_versus_commit(self.git_tempdir, self.base_commit)
        if _last_assistant_is_empty(msg_history) and not has_source_edits(patch):
            abs_target = os.path.abspath(os.path.join(self.git_tempdir, target_file))
            safe_log("[forward] Main pass ended on an empty turn with no source edits; compact editor-tool retry.")
            compact_msg = (f"Use the editor tool now: command=edit, path={abs_target}, "
                           f"file_text=<full solution>. Problem: {self.problem_statement}")
            msg_history = _run_until_nonempty(compact_msg, self.code_model, [])
            patch = diff_versus_commit(self.git_tempdir, self.base_commit)
        for attempt in range(3):
            if has_source_edits(patch):
                break
            # Keep history by default (nudge instead of restart); fresh only if history is tiny
            # or a previous nudge-retry already failed.
            use_fresh = len(msg_history) <= 2 or attempt >= 2
            safe_log(f"[forward] No source edits detected (attempt {attempt + 1}/3). "
                     f"fresh_history={use_fresh}. Re-prompting agent.")
            if use_fresh:
                retry_history = []
                retry_msg = f"""{task}
First run `ls -la` in the repo. Then you MUST call the editor tool: use `create` if the target file does not exist, otherwise `edit` to overwrite it with the full solution. Do not reply with text only."""
            else:
                retry_history = msg_history
                patch_display = patch.strip() if patch.strip() else "EMPTY (no changes at all)"
                retry_msg = f"""No source edits were detected in {self.git_tempdir}. The current diff against the base commit is:

{patch_display}

You have NOT yet modified the primary source file with a solution. Implement the solution NOW: use the editor tool to replace the stub if present, or create the file if missing, with a full implementation, adding any missing imports. Do not reply with only a plan or an empty message. After editing, reply with a short summary of the change."""
            msg_history = _run_until_nonempty(retry_msg, self.code_model, retry_history)
            safe_log(f"[forward] Retry attempt {attempt + 1} complete; {len(msg_history)} messages in history.")
            patch = diff_versus_commit(self.git_tempdir, self.base_commit)

        if not has_source_edits(patch):
            safe_log("[forward] Still no source edits after retries; running programmatic fallback.")
            fallback_prompts = [
                f"{task}\nOutput ONLY the full contents of the solution file in a single ```python code block. No tools.",
                f"{task}\nWithout using any tools, reply with the complete Python source code of the solution inside one fenced code block (```python ... ```). Nothing else.",
                f"{task}\nNo tools. Write the final, complete solution program as plain Python code. Put it in a single fenced code block.",
            ]
            code = None
            for idx, fallback_msg in enumerate(fallback_prompts):
                reply_history = chat_with_agent(fallback_msg, model=self.code_model, msg_history=[], logging=safe_log)
                code = _extract_code(_last_assistant_text(reply_history))
                safe_log(f"[forward] Fallback attempt {idx + 1}: extracted={code is not None}.")
                if code is not None:
                    break
            if code is None:
                compact_fallback = (f"<problem_description>\n{self.problem_statement}\n</problem_description>\n\n"
                                    "Respond only with a ```python block containing the complete solution program. No tools.")
                reply_history = chat_with_agent(compact_fallback, model=self.code_model, msg_history=[], logging=safe_log)
                code = _extract_code(_last_assistant_text(reply_history))
                safe_log(f"[forward] Compact code-only fallback: extracted={code is not None}.")
            out_path = os.path.join(self.git_tempdir, target_file)
            if code is None:
                safe_log(f"[forward] All fallback attempts failed; writing minimal skeleton to {out_path}.")
                code = SKELETON_CODE
            else:
                safe_log(f"[forward] Fallback writing {len(code)} chars to {out_path}.")
            os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
            with open(out_path, 'w') as f:
                f.write(code)
            patch = diff_versus_commit(self.git_tempdir, self.base_commit)
            safe_log(f"[forward] After fallback, has_source_edits={has_source_edits(patch)}.")

        # Optional verification pass once a source edit exists
        if has_source_edits(patch):
            verify_msg = """Verify your solution once more: run the problem's examples and a brute-force comparison on small random inputs via bash. If there are any mismatches, errors, or edge-case issues, fix them in the source file with the editor tool. Make sure the final source file is complete and imports are correct. End with a short text summary."""
            safe_log("[forward] Running verification pass.")
            msg_history = _run_until_nonempty(verify_msg, self.code_model, msg_history)

        # Restore last, so a broken edit made during verification is also reverted.
        if draft_code is not None:
            self._restore_draft_if_broken(target_file, draft_code)
            patch = diff_versus_commit(self.git_tempdir, self.base_commit)

        return msg_history

    def _restore_draft_if_broken(self, target_file, draft_code):
        """Rewrite the saved draft if the target is empty or no longer parses (Python only)."""
        out_path = os.path.join(self.git_tempdir, target_file)
        current = ''
        if os.path.exists(out_path):
            with open(out_path, 'r', errors='replace') as f:
                current = f.read()
        broken = not current.strip()
        if not broken and target_file.endswith('.py'):
            try:
                ast.parse(current)
            except SyntaxError:
                broken = True
        if broken:
            safe_log(f"[forward] Target {target_file} is empty or unparsable; restoring draft.")
            os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
            with open(out_path, 'w') as f:
                f.write(draft_code)
        return broken

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

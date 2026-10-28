import argparse
import subprocess
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import threading
import time

from llm_withtools import (CLAUDE_MODEL, OPENAI_MODEL, MAX_TOKENS_CAP, chat_with_agent, EmptyResponseError,
                           get_plain_code_response_claude)
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

def _message_blocks(msg):
    content = msg.get('content', [])
    if isinstance(content, str):
        return [{'type': 'text', 'text': content}]
    return [b if isinstance(b, dict) else {'type': 'text', 'text': str(b)} for b in content]

def _last_assistant_text(msg_history):
    """Return the concatenated text of the final assistant message ('' if none)."""
    for msg in reversed(msg_history or []):
        if msg.get('role') == 'assistant':
            return "\n".join(b.get('text', '') for b in _message_blocks(msg) if b.get('type') == 'text')
    return ''

def _last_assistant_empty(msg_history):
    """True if the final assistant message has only empty text and no tool_use blocks."""
    for msg in reversed(msg_history or []):
        if msg.get('role') == 'assistant':
            blocks = _message_blocks(msg)
            if any(b.get('type') == 'tool_use' for b in blocks):
                return False
            return all(not b.get('text', '').strip() for b in blocks if b.get('type') == 'text')
    return True

# Placeholder deliverable written before the first LLM call so the patch is never empty.
STUB_MARKER = '# STUB'
STUB_CODE = f"{STUB_MARKER} placeholder, to be replaced by the real solution\nimport sys\nprint(0)\n"

ESCALATION_SUFFIX = (
    "\n\nIMPORTANT: Be concise. Do not deliberate at length. Write the solution file NOW with the editor tool, "
    "then test it on the samples with bash."
)

def _extract_python_code(text):
    """Extract the longest

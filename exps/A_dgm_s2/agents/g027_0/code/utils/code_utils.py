import re

CODE_BLOCK_RE = re.compile(r"```[ \t]*(?:python|py|python3)?[ \t]*\n(.*?)```", re.DOTALL)


def _message_text(msg):
    """Return the concatenated text of an assistant/user message (str or list-of-blocks content)."""
    if not isinstance(msg, dict):
        return ''
    content = msg.get('content')
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and isinstance(block.get('text'), str):
                parts.append(block['text'])
            elif isinstance(block, str):
                parts.append(block)
        return '\n'.join(parts)
    return ''


def extract_last_code_block(msg_history):
    """
    Scan the message history from the end and return the body of the last fenced
    ```python block found in an assistant message, or None if there is none.
    """
    if not isinstance(msg_history, list):
        return None
    for msg in reversed(msg_history):
        if not isinstance(msg, dict) or msg.get('role') != 'assistant':
            continue
        matches = CODE_BLOCK_RE.findall(_message_text(msg))
        if matches:
            code = matches[-1]
            if code.strip():
                return code
    return None

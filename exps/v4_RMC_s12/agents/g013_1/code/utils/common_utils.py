import json


def read_file(file_path):
    """
    Read a file and return its contents as a string.
    """
    with open(file_path, 'r') as f:
        content = f.read().strip()
    return content

def load_json_file(file_path):
    """
    Load a JSON file and return its contents as a dictionary.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


CLIP_MARKER = "\n...<response clipped>...\n"

def truncate_text(text, max_chars=10000):
    """
    Truncate a string to at most `max_chars` characters, keeping the beginning
    and the end of the text (where errors and summaries usually are).
    The removed middle part is replaced with a clip marker.
    """
    if not isinstance(text, str):
        text = str(text)
    if max_chars is None or len(text) <= max_chars:
        return text
    keep = max(max_chars - len(CLIP_MARKER), 0)
    head_len = keep // 2
    tail_len = keep - head_len
    tail = text[-tail_len:] if tail_len > 0 else ""
    return text[:head_len] + CLIP_MARKER + tail

from pathlib import Path

def tool_info():
    return {
        "name": "editor",
        "description": """View, create and edit files.\n
* `view`: show a file with line numbers (optionally a `view_range` [start, end]) or list a directory.\n
* `create`: write `file_text` to `path` (creates or overwrites the file).\n
* `str_replace`: replace the exact text `old_str` (must occur exactly once in the file) with `new_str`.\n
* `insert`: insert `new_str` after line `insert_line` (0 = top of file).\n
* Paths must be absolute.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "enum": ["view", "create", "str_replace", "insert"],
                            "description": "The operation to perform."},
                "path": {"type": "string", "description": "Absolute path to the file or directory."},
                "file_text": {"type": "string", "description": "Full file content for `create`."},
                "old_str": {"type": "string", "description": "Exact text to replace for `str_replace`."},
                "new_str": {"type": "string", "description": "Replacement text for `str_replace`, or text to insert for `insert`."},
                "insert_line": {"type": "integer", "description": "Line number after which to insert for `insert`."},
                "view_range": {"type": "array", "items": {"type": "integer"}, "description": "Optional [start, end] lines for `view` (end -1 = end of file)."}
            },
            "required": ["command", "path"]
        }
    }

def _numbered(text, start=1):
    return "\n".join(f"{i:6}\t{line}" for i, line in enumerate(text.split("\n"), start))

def tool_function(command, path, file_text=None, old_str=None, new_str=None, insert_line=None, view_range=None):
    try:
        p = Path(path)
        if not p.is_absolute():
            return f"Error: {path} is not an absolute path."
        if command == "view":
            if p.is_dir():
                items = sorted(str(x) for x in p.rglob('*') if not any(part.startswith('.') for part in x.relative_to(p).parts))
                return "\n".join(items[:500]) or "(empty directory)"
            text = p.read_text()
            if view_range:
                lines = text.split("\n"); s = max(1, view_range[0]); e = len(lines) if view_range[1] == -1 else view_range[1]
                return _numbered("\n".join(lines[s - 1:e]), s)
            if len(text) > 30000:
                text = text[:30000] + "\n<file clipped; use view_range>"
            return _numbered(text)
        if command == "create":
            if file_text is None:
                return "Error: `file_text` is required for create."
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(file_text)
            return f"File written: {path}"
        if command == "str_replace":
            text = p.read_text()
            if old_str is None:
                return "Error: `old_str` is required for str_replace."
            n = text.count(old_str)
            if n != 1:
                return f"Error: old_str occurs {n} times in {path}; it must occur exactly once. No change made."
            p.write_text(text.replace(old_str, new_str or "", 1))
            return f"Edited {path}."
        if command == "insert":
            lines = p.read_text().split("\n")
            k = int(insert_line or 0)
            if k < 0 or k > len(lines):
                return f"Error: insert_line must be between 0 and {len(lines)}."
            lines[k:k] = (new_str or "").split("\n")
            p.write_text("\n".join(lines))
            return f"Inserted text after line {k} of {path}."
        return f"Error: unknown command {command}"
    except Exception as e:
        return f"Error: {e}"

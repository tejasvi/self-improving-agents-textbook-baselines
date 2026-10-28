from pathlib import Path
import subprocess

MAX_VIEW_CHARS = 30000


def tool_info():
    return {
        "name": "editor",
        "description": """Custom editing tool for viewing, creating, and editing files\n
* `view`: if `path` is a file, displays it with line numbers (optionally only `view_range` = [start, end], 1-indexed, end=-1 means to end of file). If `path` is a directory, lists non-hidden files and directories up to 2 levels deep.\n
* `create`: creates a new file with `file_text`. Cannot be used if `path` already exists (use `edit` to overwrite).\n
* `edit`: overwrites the entire existing file with `file_text`.\n
* `str_replace`: replaces the exact text `old_str` with `new_str` in the file. `old_str` must occur exactly once (include enough context lines to make it unique).\n
* `insert`: inserts `new_str` after line `insert_line` (0 means at the beginning of the file).\n
* Long outputs are truncated and marked with `<response clipped>`.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "enum": ["view", "create", "edit", "str_replace", "insert"],
                    "description": "The command to run: `view`, `create`, `edit`, `str_replace`, or `insert`."
                },
                "path": {
                    "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
                    "type": "string"
                },
                "file_text": {
                    "description": "Required for `create` and `edit`: the content of the entire file.",
                    "type": "string"
                },
                "view_range": {
                    "description": "Optional for `view` on a file: [start_line, end_line], 1-indexed, end_line=-1 means until end of file.",
                    "type": "array",
                    "items": {"type": "integer"}
                },
                "old_str": {
                    "description": "Required for `str_replace`: exact text to replace (must be unique in the file).",
                    "type": "string"
                },
                "new_str": {
                    "description": "For `str_replace`: replacement text (empty string to delete). For `insert`: text to insert.",
                    "type": "string"
                },
                "insert_line": {
                    "description": "Required for `insert`: line number after which `new_str` is inserted (0 = beginning).",
                    "type": "integer"
                }
            },
            "required": ["command", "path"]
        }
    }


def maybe_truncate(content: str, max_length: int = MAX_VIEW_CHARS) -> str:
    if len(content) > max_length:
        return content[:max_length] + "\n<response clipped>"
    return content


def validate_path(path: str, command: str) -> Path:
    if not isinstance(path, str) or not path:
        raise ValueError("A valid absolute `path` is required.")
    path_obj = Path(path)
    if not path_obj.is_absolute():
        raise ValueError(f"The path {path} is not an absolute path (must start with '/').")

    if command == "view":
        if not path_obj.exists():
            raise ValueError(f"The path {path} does not exist.")
    elif command == "create":
        if path_obj.exists():
            raise ValueError(f"Cannot create new file; {path} already exists. Use `edit` to overwrite it.")
    elif command in ("edit", "str_replace", "insert"):
        if not path_obj.exists():
            raise ValueError(f"The file {path} does not exist.")
        if path_obj.is_dir():
            raise ValueError(f"{path} is a directory and cannot be edited as a file.")
    else:
        raise ValueError(f"Unknown or unsupported command: {command}")
    return path_obj


def format_output(content: str, path: str, init_line: int = 1) -> str:
    content = maybe_truncate(content)
    content = content.expandtabs()
    numbered_lines = [
        f"{i + init_line:6}\t{line}"
        for i, line in enumerate(content.split("\n"))
    ]
    return f"Here's the result of running `cat -n` on {path}:\n" + "\n".join(numbered_lines) + "\n"


def read_file(path: Path) -> str:
    try:
        return path.read_text()
    except Exception as e:
        raise ValueError(f"Failed to read file: {e}")


def write_file(path: Path, content: str):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    except Exception as e:
        raise ValueError(f"Failed to write file: {e}")


def view_path(path_obj: Path, view_range=None) -> str:
    if path_obj.is_dir():
        try:
            result = subprocess.run(
                ['find', str(path_obj), '-maxdepth', '2', '-not', '-path', '*/\\.*'],
                capture_output=True,
                text=True
            )
            if result.stderr:
                return f"Error listing directory: {result.stderr}"
            return (
                f"Here's the files and directories up to 2 levels deep in {path_obj}, excluding hidden items:\n"
                + maybe_truncate(result.stdout)
            )
        except Exception as e:
            raise ValueError(f"Failed to list directory: {e}")

    content = read_file(path_obj)
    if view_range:
        if not isinstance(view_range, (list, tuple)) or len(view_range) != 2:
            raise ValueError("`view_range` must be a list of two integers [start, end].")
        lines = content.split("\n")
        start, end = int(view_range[0]), int(view_range[1])
        if start < 1:
            start = 1
        if end == -1 or end > len(lines):
            end = len(lines)
        if start > end:
            raise ValueError(f"Invalid view_range {view_range}; file has {len(lines)} lines.")
        return format_output("\n".join(lines[start - 1:end]), str(path_obj), init_line=start)
    return format_output(content, str(path_obj))


def _snippet(content: str, center_line: int, path: str, radius: int = 4) -> str:
    lines = content.split("\n")
    start = max(1, center_line - radius)
    end = min(len(lines), center_line + radius)
    return format_output("\n".join(lines[start - 1:end]), path, init_line=start)


def tool_function(command: str, path: str, file_text: str = None, view_range=None,
                  old_str: str = None, new_str: str = None, insert_line: int = None) -> str:
    try:
        path_obj = validate_path(path, command)

        if command == "view":
            return view_path(path_obj, view_range)

        elif command == "create":
            if file_text is None:
                raise ValueError("Missing required `file_text` for 'create' command.")
            write_file(path_obj, file_text)
            return f"File created successfully at: {path}"

        elif command == "edit":
            if file_text is None:
                raise ValueError("Missing required `file_text` for 'edit' command.")
            write_file(path_obj, file_text)
            return f"File at {path} has been overwritten with new content."

        elif command == "str_replace":
            if old_str is None or old_str == "":
                raise ValueError("Missing required non-empty `old_str` for 'str_replace' command.")
            if new_str is None:
                new_str = ""
            content = read_file(path_obj)
            count = content.count(old_str)
            if count == 0:
                raise ValueError(f"`old_str` was not found verbatim in {path}. View the file and copy the exact text (whitespace matters).")
            if count > 1:
                raise ValueError(f"`old_str` occurs {count} times in {path}; include more context to make it unique.")
            idx = content.index(old_str)
            new_content = content.replace(old_str, new_str, 1)
            write_file(path_obj, new_content)
            line_no = content[:idx].count("\n") + 1
            return f"The file {path} has been edited. " + _snippet(new_content, line_no, path)

        elif command == "insert":
            if new_str is None:
                raise ValueError("Missing required `new_str` for 'insert' command.")
            if insert_line is None:
                raise ValueError("Missing required `insert_line` for 'insert' command.")
            content = read_file(path_obj)
            lines = content.split("\n")
            n = int(insert_line)
            if n < 0 or n > len(lines):
                raise ValueError(f"`insert_line` {n} out of range [0, {len(lines)}].")
            new_lines = lines[:n] + new_str.split("\n") + lines[n:]
            new_content = "\n".join(new_lines)
            write_file(path_obj, new_content)
            return f"The file {path} has been edited. " + _snippet(new_content, n + 1, path)

        else:
            raise ValueError(f"Unknown command: {command}")

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print(tool_function("view", str(Path("./coding_agent.py").resolve()), view_range=[1, 10]))

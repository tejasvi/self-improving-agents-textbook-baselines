from pathlib import Path
import subprocess


def tool_info():
    return {
        "name": "editor",
        "description": """Custom editing tool for viewing, creating, and editing files\n
* If `path` is a file, `view` displays the file with line numbers (optionally only `view_range`). If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep.\n
* `create` creates a new file (fails if the file exists).\n
* `edit` overwrites the entire file with the provided `file_text` (file must exist).\n
* `str_replace` replaces the single exact occurrence of `old_str` with `new_str` in the file (fails if `old_str` occurs 0 or more than 1 times).""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "enum": ["view", "create", "edit", "str_replace"],
                    "description": "The command to run: `view`, `create`, `edit`, or `str_replace`."
                },
                "path": {
                    "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
                    "type": "string"
                },
                "file_text": {
                    "description": "Required for `create` and `edit`: the content for the entire file.",
                    "type": "string"
                },
                "old_str": {
                    "description": "Required for `str_replace`: exact text to replace (must occur exactly once).",
                    "type": "string"
                },
                "new_str": {
                    "description": "Used by `str_replace`: replacement text (empty string if omitted).",
                    "type": "string"
                },
                "view_range": {
                    "description": "Optional for `view` on a file: [start_line, end_line] (1-based, inclusive; end -1 means end of file).",
                    "type": "array",
                    "items": {"type": "integer"}
                }
            },
            "required": ["command", "path"]
        }
    }


def maybe_truncate(content: str, max_length: int = 30000) -> str:
    if len(content) > max_length:
        return content[:max_length] + "\n<response clipped>"
    return content


def validate_path(path: str, command: str) -> Path:
    if not isinstance(path, str) or not path:
        raise ValueError("A path must be provided.")
    path_obj = Path(path)
    if not path_obj.is_absolute():
        raise ValueError(f"The path {path} is not an absolute path (must start with '/').")

    if command == "view":
        if not path_obj.exists():
            raise ValueError(f"The path {path} does not exist.")
    elif command == "create":
        if path_obj.exists():
            raise ValueError(f"Cannot create new file; {path} already exists.")
    elif command in ("edit", "str_replace"):
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
                capture_output=True, text=True, timeout=30
            )
            if result.stderr:
                return f"Error listing directory: {result.stderr}"
            return (
                f"Here's the files and directories up to 2 levels deep in {path_obj}, excluding hidden items:\n"
                + result.stdout
            )
        except Exception as e:
            raise ValueError(f"Failed to list directory: {e}")

    content = read_file(path_obj)
    if view_range:
        lines = content.split("\n")
        start = int(view_range[0]) if len(view_range) > 0 else 1
        end = int(view_range[1]) if len(view_range) > 1 else -1
        start = max(1, start)
        if end == -1 or end > len(lines):
            end = len(lines)
        return format_output("\n".join(lines[start - 1:end]), str(path_obj), init_line=start)
    return format_output(content, str(path_obj))


def tool_function(command: str, path: str, file_text: str = None, old_str: str = None,
                  new_str: str = None, view_range=None) -> str:
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
                raise ValueError("Missing required `old_str` for 'str_replace' command.")
            content = read_file(path_obj)
            count = content.count(old_str)
            if count == 0:
                raise ValueError("`old_str` was not found in the file. View the file and copy the exact text.")
            if count > 1:
                raise ValueError(f"`old_str` occurs {count} times; include more context to make it unique.")
            write_file(path_obj, content.replace(old_str, new_str if new_str is not None else "", 1))
            return f"Replaced text in {path} successfully."

        else:
            raise ValueError(f"Unknown command: {command}")

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print(tool_function("view", str(Path("./coding_agent.py").resolve()), view_range=[1, 10]))

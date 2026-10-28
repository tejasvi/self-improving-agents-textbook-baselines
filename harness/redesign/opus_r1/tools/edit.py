from pathlib import Path
import subprocess


def tool_info():
    return {
        "name": "editor",
        "description": """Custom editing tool for viewing, creating, and editing files\n
* If `path` is a file, `view` displays the entire file with line numbers. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep.\n
* The `create` command cannot be used if the specified `path` already exists as a file.\n
* The `edit` command overwrites the entire existing file with the provided `file_text`.\n
* The `str_replace` command replaces exactly one occurrence of `old_str` with `new_str` in an existing file (`old_str` must appear exactly once).\n
* If a `command` generates a long output, it will be truncated and marked with `<response clipped>`.""",
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
                    "description": "Required parameter of `create` or `edit` command, containing the content for the entire file.",
                    "type": "string"
                },
                "old_str": {
                    "description": "Required parameter of `str_replace`: the exact text to replace (must occur exactly once).",
                    "type": "string"
                },
                "new_str": {
                    "description": "Required parameter of `str_replace`: the replacement text.",
                    "type": "string"
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
    if not path:
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
    numbered_lines = [f"{i + init_line:6}\t{line}" for i, line in enumerate(content.split("\n"))]
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


def view_path(path_obj: Path) -> str:
    if path_obj.is_dir():
        try:
            result = subprocess.run(
                ['find', str(path_obj), '-maxdepth', '2', '-not', '-path', '*/\\.*'],
                capture_output=True, text=True, timeout=60
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
    return format_output(content, str(path_obj))


def tool_function(command: str, path: str, file_text: str = None, old_str: str = None, new_str: str = None) -> str:
    try:
        path_obj = validate_path(path, command)

        if command == "view":
            return view_path(path_obj)

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
            if old_str is None or new_str is None:
                raise ValueError("`old_str` and `new_str` are required for 'str_replace' command.")
            content = read_file(path_obj)
            count = content.count(old_str)
            if count == 0:
                raise ValueError("`old_str` was not found in the file.")
            if count > 1:
                raise ValueError(f"`old_str` occurs {count} times; it must be unique. Add more context.")
            write_file(path_obj, content.replace(old_str, new_str, 1))
            return f"File at {path} has been edited (1 replacement)."

        else:
            raise ValueError(f"Unknown command: {command}")

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    print(tool_function("view", str(Path("./coding_agent.py").resolve())))

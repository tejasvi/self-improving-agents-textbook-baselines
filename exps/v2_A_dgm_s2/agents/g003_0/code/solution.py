import re
import sys


def extract_python_code(text):
    """
    Return the contents of the first ```python (or ```py / bare ```) fenced block in text.
    Returns None if no non-empty fenced block is present.
    """
    if not text:
        return None
    match = re.search(r'```(?:python|py)?[ \t]*\n(.*?)```', text, flags=re.DOTALL)
    if match and match.group(1).strip():
        return match.group(1)
    return None


def main():
    data = sys.stdin.read()
    code = extract_python_code(data)
    if code is None:
        sys.stdout.write("")
    else:
        sys.stdout.write(code)


if __name__ == "__main__":
    main()

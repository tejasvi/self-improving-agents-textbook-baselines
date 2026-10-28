import ast
import builtins
import os
import sys

TYPING_NAMES = {
    "List", "Dict", "Set", "FrozenSet", "Tuple", "Optional", "Union", "Any",
    "Callable", "Iterable", "Iterator", "Sequence", "Mapping", "MutableMapping",
    "Deque", "DefaultDict", "Generator", "Type", "TypeVar", "Literal",
}

BUILTIN_NAMES = set(dir(builtins))


def tool_info():
    return {
        "name": "solution_lint",
        "description": """Lint a Python solution file for portability problems that commonly crash in the grader.\n
* Reports calls to three-argument pow(a, b, m) (not supported by the grader's pow).\n
* Reports imports of modules outside the Python standard library (e.g. numpy).\n
* Reports definitions, assignments, or parameters that shadow Python builtins (e.g. list, sum, input).\n
* Reports typing names (List, Dict, Optional, ...) used without importing them from typing.\n
* Returns 'No issues found' when clean; otherwise one line per finding as 'file:line: message: source line'.\n
* Reports a syntax error with its line number if the file does not parse.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to lint."
                }
            },
            "required": ["file_path"]
        }
    }


def _source_line(lines, lineno):
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1].strip()
    return ""


def _add_name_targets(target, out):
    """Collect plain names bound by an assignment target (handles tuple/list unpacking)."""
    if isinstance(target, ast.Name):
        out.append(target)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            _add_name_targets(elt, out)
    elif isinstance(target, ast.Starred):
        _add_name_targets(target.value, out)


def tool_function(file_path):
    if not os.path.isfile(file_path):
        return f"Error: file not found: {file_path}"
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()
    except OSError as e:
        return f"Error: could not read {file_path}: {e}"

    lines = source.splitlines()
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError as e:
        lineno = e.lineno or 0
        return f"{file_path}:{lineno}: syntax error: {e.msg}: {_source_line(lines, lineno)}"

    findings = []  # (lineno, message)
    stdlib = set(sys.stdlib_module_names)

    def report(lineno, message):
        findings.append((lineno, message))

    def check_builtin_name(name, lineno, what):
        if name in BUILTIN_NAMES and not name.startswith("_"):
            report(lineno, f"{what} '{name}' shadows a Python builtin")

    # Names bound by any import, and whether a `from typing import *` exists.
    imported_names = set()
    star_typing = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    if node.module == "typing":
                        star_typing = True
                else:
                    imported_names.add(alias.asname or alias.name)

    # Names that appear inside annotations (parameter, return, and variable annotations).
    annotation_roots = []
    for node in ast.walk(tree):
        if isinstance(node, ast.arg) and node.annotation is not None:
            annotation_roots.append(node.annotation)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.returns is not None:
            annotation_roots.append(node.returns)
        elif isinstance(node, ast.AnnAssign):
            annotation_roots.append(node.annotation)

    for node in ast.walk(tree):
        # (a) three-argument pow
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "pow" and len(node.args) == 3:
            report(node.lineno, "three-argument pow(a, b, m) is not supported by the grader; "
                                "use a hand-written square-and-multiply modpow helper")

        # (b) non-stdlib imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top not in stdlib:
                    report(node.lineno, f"import of non-standard-library module '{top}' is not allowed; "
                                        f"use pure-Python code instead")
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                top = node.module.split(".")[0]
                if top not in stdlib:
                    report(node.lineno, f"import from non-standard-library module '{top}' is not allowed; "
                                        f"use pure-Python code instead")

        # (c) shadowed builtins
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            check_builtin_name(node.name, node.lineno, "function/class name" if not isinstance(node, ast.ClassDef) else "class name")
        elif isinstance(node, ast.arg):
            check_builtin_name(node.arg, node.lineno, "parameter")
        elif isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.For, ast.AsyncFor,
                               ast.With, ast.AsyncWith, ast.comprehension, ast.NamedExpr)):
            targets = []
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    _add_name_targets(t, targets)
            elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
                _add_name_targets(node.target, targets)
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
                _add_name_targets(node.target, targets)
            elif isinstance(node, ast.NamedExpr):
                _add_name_targets(node.target, targets)
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                for item in node.items:
                    if item.optional_vars is not None:
                        _add_name_targets(item.optional_vars, targets)
            for t in targets:
                check_builtin_name(t.id, t.lineno, "variable")
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.asname:
                    check_builtin_name(alias.asname, node.lineno, "import alias")

    # (d) typing names used in annotations without being imported
    if not star_typing:
        for root in annotation_roots:
            for sub in ast.walk(root):
                if isinstance(sub, ast.Name) and sub.id in TYPING_NAMES and sub.id not in imported_names:
                    report(sub.lineno, f"typing name '{sub.id}' used without 'from typing import {sub.id}'")

    if not findings:
        return "No issues found"

    findings = sorted(set(findings), key=lambda x: (x[0], x[1]))
    out = []
    for lineno, message in findings:
        out.append(f"{file_path}:{lineno}: {message}: {_source_line(lines, lineno)}")
    return "\n".join(out)

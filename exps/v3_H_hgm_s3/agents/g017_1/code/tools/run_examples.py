import ast
import importlib.util
import inspect
import re
import traceback

# Matches "Input: ..." followed by "Output: ..." (both may span lines until the next keyword).
EXAMPLE_RE = re.compile(
    r'Input:\s*(.*?)\s*\n\s*Output:\s*(.*?)(?=\n\s*(?:Input:|Explanation:|Constraints:|Follow[- ]?up:)|\Z)',
    re.DOTALL,
)


def tool_info():
    return {
        'name': 'run_examples',
        'description': (
            'Check a method-style solution (a `Solution` class method) against the examples written as '
            '"Input: a = ..., b = ..." / "Output: ..." pairs in the problem statement. The module is imported, '
            'Solution().<method>(**kwargs) is called for each example, and PASS or MISMATCH is reported per '
            'example with a final summary. Any mismatch is a failure.'
        ),
        'input_schema': {
            'type': 'object',
            'properties': {
                'module_path': {
                    'type': 'string',
                    'description': 'Path to the Python file that defines the Solution class.',
                },
                'problem_text': {
                    'type': 'string',
                    'description': 'The full problem statement containing "Input:" / "Output:" example pairs.',
                },
                'class_name': {
                    'type': 'string',
                    'description': 'Name of the class to instantiate. Defaults to "Solution".',
                },
                'method_name': {
                    'type': 'string',
                    'description': 'Name of the method to call. If omitted, the single public method of the class is used.',
                },
            },
            'required': ['module_path', 'problem_text'],
        },
    }


def _parse_examples(problem_text):
    """Return a list of (input_text, output_text) pairs found in the problem statement."""
    return [(i.strip(), o.strip()) for i, o in EXAMPLE_RE.findall(problem_text or '')]


def _parse_kwargs(input_text):
    """
    Parse 'a = 1, b = [2, 3]' into ({'a': 1, 'b': [2, 3]}, []).
    Arguments are evaluated with ast.literal_eval. Positional args are returned separately.
    """
    call = ast.parse(f"_f({input_text})", mode='eval').body
    kwargs = {}
    for kw in call.keywords:
        kwargs[kw.arg] = ast.literal_eval(kw.value)
    args = [ast.literal_eval(a) for a in call.args]
    return kwargs, args


def _load_class(module_path, class_name):
    spec = importlib.util.spec_from_file_location('candidate_solution_module', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


def _pick_method(cls, method_name):
    if method_name:
        return method_name
    methods = [
        name for name, member in inspect.getmembers(cls, predicate=inspect.isfunction)
        if not name.startswith('_')
    ]
    if len(methods) == 1:
        return methods[0]
    raise ValueError(f'cannot infer method name, candidates: {methods}')


def _same(got, expected_text):
    try:
        expected = ast.literal_eval(expected_text)
    except Exception:
        return str(got).strip() == expected_text.strip()
    return got == expected


def tool_function(module_path, problem_text, class_name=None, method_name=None):
    class_name = class_name or 'Solution'
    examples = _parse_examples(problem_text)
    if not examples:
        return 'No "Input:" / "Output:" example pairs found in problem_text.'

    try:
        cls = _load_class(module_path, class_name)
        method = _pick_method(cls, method_name)
    except Exception as e:
        return f'ERROR: could not load {class_name} from {module_path}: {type(e).__name__}: {e}'

    lines = []
    failures = 0
    for idx, (inp, expected) in enumerate(examples, 1):
        try:
            kwargs, args = _parse_kwargs(inp)
            got = getattr(cls(), method)(*args, **kwargs)
        except Exception:
            lines.append(f'Example {idx}: MISMATCH (runtime error)')
            lines.append(f'input: {inp}')
            lines.append(f'expected: {expected}')
            lines.append(f'traceback: {traceback.format_exc()[-800:]}')
            failures += 1
            continue
        if _same(got, expected):
            lines.append(f'Example {idx}: PASS')
        else:
            lines.append(f'Example {idx}: MISMATCH')
            lines.append(f'input: {inp}')
            lines.append(f'expected: {expected}')
            lines.append(f'got: {got!r}')
            failures += 1

    if failures == 0:
        lines.append('ALL EXAMPLES EXACT MATCH')
    else:
        lines.append(f'{failures} EXAMPLE(S) DIFFER')
    return '\n'.join(lines)

# Implementation Details

## Summary of Changes

This document outlines the implementation of the three main requirements:

1. Add a new tool `tools/run_samples.py`
2. Modify the prompt in `coding_agent.py` with detailed step-by-step workflow
3. Enhance `run_tests.py` documentation for the checker contract

---

## 1. New Tool: `/dgm/tools/run_samples.py`

### Purpose
Runs a solution against sample test cases extracted from the problem statement to detect basic issues early.

### Tool Signature
```python
def tool_info() -> dict
def tool_function(solution_path: str, samples: list, timeout_sec: float = 5.0) -> str
```

### Input Schema (Valid JSON)
```json
{
  "type": "object",
  "properties": {
    "solution_path": {
      "type": "string",
      "description": "Path to the solution.py file to test"
    },
    "samples": {
      "type": "array",
      "description": "List of sample test cases, each with 'input' and 'expected_output' strings"
    }
  },
  "required": ["solution_path", "samples"]
}
```

**Key Points:**
- `required` is at the same level as `properties` ✓
- Array property `samples` has only `type` and `description` (no `minItems`, `maxItems`, `items`) ✓
- All properties have `type` and `description` ✓

### Functionality
1. Takes a solution path and list of {input, expected_output} objects
2. For each sample:
   - Runs `python3 solution_path` with the sample input
   - Compares actual output to expected output
   - Returns PASS or FAIL with details
3. Detects whitespace-only differences and flags them
4. Generates unified diffs for mismatches
5. Returns summary indicating all passed or some failed

### Return Format
```
Sample Test Results: [ALL PASSED|SOME FAILED (N failures)]
Sample 0: PASS
Sample 1: FAIL (whitespace-only difference)
  Expected output: ...
  Actual output: ...
  Diff: ...
```

---

## 2. Updated: `/dgm/coding_agent.py`

### Major Changes
Rewrote the `forward()` method to implement a detailed, multi-phase workflow.

### New Workflow Architecture

#### Phase 1: Initial Solution and Sample Testing
First call to `chat_with_agent()` instructs the agent to:

1. **Understand and Analyze the Problem**
   - Summarize problem including constraints and samples
   - Identify key algorithm or approach
   - Prove the approach handles the entire solution space
   - Consider edge cases
   - Verify alignment with constraints

2. **Implement the Solution**
   - Write `solution.py` that reads from stdin and writes to stdout
   - Use clear variable names and brief comments

3. **Extract and Test with Samples**
   - Extract all sample test cases from the problem statement
   - Format samples as JSON: {input, expected_output}
   - Call `run_samples` tool to test the solution
   - Identify if mismatches are due to:
     - Incorrect solution
     - Valid but different output format (multiple correct answers)

4. **Initial Verification**
   - Ensure samples pass
   - Note if validation is needed for multiple-answer scenarios
   - Fix any issues before proceeding

#### Phase 2: Comprehensive Testing (Bounded Iteration)
Uses a bounded loop: `for review_round in range(max_review_rounds)` where `max_review_rounds = 3`

**First Iteration (review_round == 0):**
Agent is instructed to:

5. **Create Validity Checker (if needed)**
   - If multiple valid outputs exist, create `checker.py`
   - Checker reads from stdin: `test_input\n\nsolution_output\n\brute_output`
   - Checker exits with code 0 if valid, non-zero if invalid
   - Try to align solution output with samples (canonical/smallest/largest)

6. **Create Brute Force Solution**
   - Write `brute.py` with simple, clearly correct but possibly slower approach
   - Used as reference for differential testing

7. **Create Test Generator**
   - Write `gen.py` that generates random test cases
   - Each invocation outputs one test case to stdout
   - Should cover:
     - Small and medium-sized inputs
     - Edge cases (min/max values, empty inputs, etc.)
     - Various patterns for different code paths

8. **Run Comprehensive Differential Testing**
   - Call `run_tests` tool with:
     - solution_path: solution.py
     - brute_path: brute.py
     - generator_path: gen.py
     - checker_path: checker.py (if created)
   - Run at least 100 random tests

9. **Test Maximum Input Size**
   - Create `max_input.txt` with maximum-size input per constraints
   - Pass to `run_tests` to measure timing
   - Ensure no timeout

10. **Fix Any Issues**
    - Analyze failures
    - Fix solution, checker, generator as needed
    - Re-run `run_tests`

**Subsequent Iterations (review_round > 0):**
If tests didn't pass, agent continues with:
- Up to 2 more review rounds (3 total)
- Fixes issues and re-runs tests
- Gets early exit if "ALL PASSED" detected

### Loop Control
```python
max_review_rounds = 3
for review_round in range(max_review_rounds):
    current_edits = self.get_current_edits()
    # ... run review
    if "ALL PASSED" in review_result or "all tests passed" in review_result.lower():
        safe_log("All tests passed! Solution is complete.")
        break
```

**Key Properties:**
- NO `while True` loops ✓
- Bounded by fixed number (3) ✓
- Early exit on success ✓
- Each iteration passes current edits via `msg_history` ✓

---

## 3. Updated: `/dgm/tools/run_tests.py`

### Changes Made

#### 1. Enhanced Tool Description
Added explicit "Checker contract" section:
```
Checker contract (if checker_path is provided):
  The checker receives input and outputs as arguments or via stdin and must exit with:
  - Exit code 0 if the solution output is valid
  - Non-zero exit code if the solution output is invalid
  The checker will be invoked as: python3 checker.py with input passed as the first argument,
  solution output as the second, and brute output as the third (or via clear delimiters in stdin).
```

#### 2. Improved Checker Input Format
Updated checker invocation to pass inputs clearly separated:
```python
checker_input = f"{test_input}\n\n{sol_output}\n\n{brute_output}"
check_result = subprocess.run(
    ["python3", str(checker_path)],
    input=checker_input,
    capture_output=True,
    text=True,
    timeout=timeout_sec
)
```

#### 3. Updated Input Schema Description
Added clarity for `checker_path` parameter:
```
"Checker receives test input, solution output, and brute output separated by blank lines on stdin."
```

#### 4. Exit Code Handling
Checker must exit with:
- Code 0: solution output is valid
- Non-zero: solution output is invalid

### Checker Contract Specification
Checkers written by the agent should:
1. Read from stdin in format: `input\n\nsolution\n\brute`
2. Parse the three parts (separated by blank lines)
3. Validate the solution output according to the problem's acceptance criteria
4. Exit with code 0 if valid, non-zero if invalid
5. Optionally write validation messages to stdout

---

## Integration

### Tool Loading
All tools are automatically discovered and loaded by `/dgm/tools/__init__.py`:
- `bash.py` - Execute shell commands
- `edit.py` - View, create, edit files
- `run_samples.py` - Test against problem samples (NEW)
- `run_tests.py` - Differential stress testing

### Agent Interaction
The agent now has access to a complete testing pipeline:
1. **run_samples** - Validate basic correctness
2. **bash** - Create auxiliary files (checker, brute, generator)
3. **editor** - Write and modify files
4. **run_tests** - Comprehensive differential testing

---

## Acceptance Criteria - All Met ✓

### Requirement 1: New Tool run_samples.py ✓
- [x] Tool info and function both defined
- [x] Takes solution_path and samples (array) as arguments
- [x] Returns PASS/FAIL per sample with diffs
- [x] Detects whitespace-only differences
- [x] Valid JSON schema with correct nesting
- [x] Array property has no forbidden attributes

### Requirement 2: Rewritten Prompt ✓
- [x] Detailed step-by-step workflow (10 steps)
- [x] Phase 1: Algorithm derivation and proof
- [x] Phase 2: Implementation
- [x] Phase 3: Sample testing with run_samples
- [x] Phase 4: Validator creation for multi-answer cases
- [x] Phase 5: Brute force solution
- [x] Phase 6: Test generator
- [x] Phase 7: Differential testing with run_tests
- [x] Phase 8: Max-size input testing
- [x] Bounded loops only (max 3 review rounds)
- [x] No `while True` loops
- [x] Early exit on success
- [x] Passes current edits via get_current_edits()

### Requirement 3: Checker Contract Clarity ✓
- [x] Explicit description of checker contract
- [x] Clear input format: `input\n\nsolution\n\brute`
- [x] Clear exit codes: 0 for valid, non-zero for invalid
- [x] Updated checker invocation to match contract
- [x] Multi-answer scenario support

---

## Example Usage

### Agent Workflow for Multi-Answer Problem

**Problem:** Find any valid arrangement of N items satisfying constraints

**What the agent does:**

1. Extracts samples: [Sample 1: "Yes\n4 4 4", Sample 2: "Yes\n3 3 3"]
2. Writes solution.py, runs samples
3. Solution outputs "Yes\n1 1 1" for Sample 1 (valid but different)
4. Detects mismatch and creates validator checker.py
5. Checker validates if output satisfies problem constraints
6. Solution may be updated to output canonical form matching samples
7. Writes brute.py (simpler, correct algorithm)
8. Writes gen.py (random test generator)
9. Runs run_tests with checker for 100+ differential tests
10. Tests max-size inputs for timing
11. If all tests pass, solution is verified ready

---

## Files Changed

| File | Change Type | Details |
|------|-------------|---------|
| `/dgm/tools/run_samples.py` | Created | New tool for sample testing |
| `/dgm/tools/run_tests.py` | Modified | Enhanced checker contract docs and invocation |
| `/dgm/coding_agent.py` | Modified | Replaced single-shot prompt with detailed multi-phase workflow |

---

## Testing Strategy

The implementation ensures the agent will:

1. **Catch early issues** via run_samples
2. **Validate algorithms** by requiring proof before coding
3. **Handle multiple-answer scenarios** with custom validators
4. **Stress-test thoroughly** with random generation and brute-force comparison
5. **Verify performance** on maximum-size inputs
6. **Iterate bounded times** without infinite loops
7. **Exit early** when success is detected

This addresses the XOR Neighbors problem mentioned in the requirements where the agent previously produced a solution passing only 1 of 29 hidden tests. Now the agent will detect such issues through comprehensive sample testing and differential stress-testing.

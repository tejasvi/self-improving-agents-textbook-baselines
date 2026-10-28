# Verification Checklist

## File Creation and Modification

### ✅ Created Files
- [x] `/dgm/tools/run_samples.py` - New tool for sample testing
  - File size: 5.5K
  - Contains `tool_info()` function
  - Contains `tool_function()` function

### ✅ Modified Files
- [x] `/dgm/tools/run_tests.py` - Enhanced existing tool
  - File size: 9.3K
  - Updated tool description with checker contract
  - Updated checker invocation
  - Improved schema documentation

- [x] `/dgm/coding_agent.py` - Rewrote workflow
  - File size: 13K
  - Complete rewrite of `forward()` method
  - Added detailed multi-phase instructions
  - Implemented bounded iteration with early exit

## Requirement 1: run_samples Tool ✅

### Tool Structure
- [x] `tool_info()` function exists
- [x] `tool_function()` function exists
- [x] Both functions are in `/dgm/tools/run_samples.py`

### Tool Functionality
- [x] Takes `solution_path` parameter (string)
- [x] Takes `samples` parameter (array of objects)
- [x] Runs solution on each sample with subprocess
- [x] Compares actual output to expected output
- [x] Returns PASS/FAIL status per sample
- [x] Generates unified diffs for mismatches
- [x] Detects whitespace-only differences
- [x] Returns summary with ALL PASSED or failure count

### JSON Schema Validation
- [x] Root type is "object"
- [x] Has "type" field at root level
- [x] Has "properties" field
- [x] Has "required" field at same level as "properties"
- [x] Solution_path property:
  - [x] Has "type": "string"
  - [x] Has "description"
- [x] Samples property:
  - [x] Has "type": "array"
  - [x] Has "description"
  - [x] Does NOT have "minItems" ✓
  - [x] Does NOT have "maxItems" ✓
  - [x] Does NOT have "items" ✓
- [x] Required list includes both parameters
- [x] Schema is valid JSON

### Code Quality
- [x] Python syntax is valid
- [x] File compiles without errors
- [x] Imports are correct
- [x] Error handling is present
- [x] Timeout handling is implemented
- [x] Return value is string as specified

## Requirement 2: Enhanced Prompt ✅

### Workflow Architecture
- [x] Divided into clear phases (Phase 1, Phase 2)
- [x] Phase 1: Initial solution and sample testing
- [x] Phase 2: Comprehensive testing with iteration

### Phase 1 Instructions (10 steps detailed)
- [x] Step 1: Understand and analyze problem
  - [x] Summarize problem statement
  - [x] Identify key algorithm
  - [x] Prove algorithm handles solution space
  - [x] Consider edge cases
  - [x] Verify constraint compliance

- [x] Step 2: Implement solution
  - [x] Write complete solution.py
  - [x] Read from stdin
  - [x] Write to stdout
  - [x] Use clear variable names

- [x] Step 3: Extract and test samples
  - [x] Extract ALL samples
  - [x] Format as JSON
  - [x] Use run_samples tool
  - [x] Identify valid-but-different outputs
  - [x] Note validation needs

- [x] Step 4: Verify samples
  - [x] Ensure samples pass
  - [x] Debug if needed
  - [x] Note before proceeding

### Phase 2 Instructions (with bounded iteration)
- [x] Step 5: Create validity checker
  - [x] For multiple-answer scenarios
  - [x] Correct input format: test_input\n\nsolution\n\brute
  - [x] Correct exit codes: 0 for valid, non-zero for invalid
  - [x] Alignment with samples where practical

- [x] Step 6: Create brute force solution
  - [x] Simple, clearly correct approach
  - [x] Used as reference
  - [x] Correct results on all inputs

- [x] Step 7: Create test generator
  - [x] Random test case generation
  - [x] Coverage of edge cases
  - [x] Coverage of diverse patterns
  - [x] One test per invocation to stdout

- [x] Step 8: Run differential testing
  - [x] Use run_tests tool
  - [x] Solution, brute, generator
  - [x] Optional checker
  - [x] 100+ tests

- [x] Step 9: Test max input size
  - [x] Create max_input.txt
  - [x] Maximum size per constraints
  - [x] Timing measurement
  - [x] Timeout verification

- [x] Step 10: Fix and iterate
  - [x] Analyze failures
  - [x] Fix solution
  - [x] Re-run tests

### Bounded Iteration
- [x] Uses `for review_round in range(max_review_rounds)`
- [x] NOT using `while True`
- [x] max_review_rounds = 3
- [x] First iteration (review_round == 0) gets full instruction
- [x] Subsequent iterations get updated instructions
- [x] Early exit on "ALL PASSED" detection
- [x] Bounded to maximum 3 iterations

### Message History Handling
- [x] First call uses empty msg_history
- [x] Subsequent calls use `self.get_current_edits()`
- [x] Current edits formatted as user message with diff
- [x] Proper message history format

### Tool Integration
- [x] Mentions run_samples tool explicitly
- [x] Mentions run_tests tool explicitly
- [x] Instructions compatible with tool usage
- [x] Agent can automatically invoke tools

### Code Quality
- [x] Python syntax is valid
- [x] File compiles without errors
- [x] No infinite loops
- [x] Proper indentation
- [x] Proper string formatting
- [x] Bounded loops only

## Requirement 3: Checker Contract ✅

### Tool Documentation
- [x] Explicit "Checker contract" section in description
- [x] Clear statement of what checker receives
- [x] Clear statement of exit code semantics
- [x] Detailed format specification

### Checker Input Format
- [x] Three components separated by blank lines
- [x] Format: `input\n\nsolution_output\n\brute_output`
- [x] Passed via stdin (not command arguments)
- [x] Clear in tool description

### Checker Exit Codes
- [x] Exit code 0: solution output is valid
- [x] Non-zero exit code: solution output is invalid
- [x] Clearly specified in description
- [x] Implemented in tool

### Implementation
- [x] Checker invocation passes inputs correctly
- [x] Code: `f"{test_input}\n\n{sol_output}\n\n{brute_output}"`
- [x] Subprocess call passes via stdin
- [x] Exit code is checked
- [x] Return code checked properly

### Multi-Answer Support
- [x] Prompt instructs checker creation for multi-answer cases
- [x] Checker can validate various correct outputs
- [x] Integration with run_tests
- [x] Support for aligning output with samples

### Code Quality
- [x] Python syntax is valid
- [x] File compiles without errors
- [x] Consistent with existing code style
- [x] Backward compatible

## Integration Tests

### Tool Loading
- [x] run_samples.py is discoverable
- [x] run_tests.py is discoverable
- [x] Both load via `/dgm/tools/__init__.py`
- [x] tool_info() returns correct structure
- [x] tool_function() is callable

### Tool Functions
- [x] run_samples.tool_info() has valid schema
- [x] run_samples.tool_function() has correct signature
- [x] run_tests.tool_info() has valid schema
- [x] run_tests.tool_function() has correct signature

### Backward Compatibility
- [x] Existing tools (bash, editor) still work
- [x] run_tests is backward compatible (checker optional)
- [x] AgenticSystem interface unchanged
- [x] forward() method signature unchanged
- [x] No breaking changes to existing code

## All Acceptance Criteria Met ✅

### Requirement 1: run_samples.py Tool
- [x] Tool info() function defined
- [x] Tool function() defined
- [x] Takes solution_path and samples parameters
- [x] Returns PASS/FAIL per sample with diffs
- [x] Detects whitespace-only differences
- [x] Valid JSON schema with correct nesting
- [x] Array property follows schema rules (no minItems, maxItems, items)

### Requirement 2: Detailed Step-by-Step Prompt
- [x] 10-step detailed workflow
- [x] Phase 1: Analysis and implementation
- [x] Phase 2: Testing and iteration
- [x] Bounded loops (for...range, not while True)
- [x] Maximum 3 review iterations
- [x] Early exit on success
- [x] Uses run_samples for sample testing
- [x] Handles multi-answer scenarios with checker
- [x] Differential testing with brute force
- [x] Maximum-size input testing
- [x] Current edits passed between iterations

### Requirement 3: Checker Contract Clarity
- [x] Explicit checker contract in description
- [x] Clear input format specification
- [x] Clear exit code semantics
- [x] Updated checker invocation to match contract
- [x] Support for multi-answer validation

## Files Verified

```
✓ /dgm/tools/run_samples.py - NEW TOOL
  - Size: 5.5K
  - Functions: tool_info(), tool_function()
  - Schema: Valid
  - Syntax: Valid

✓ /dgm/tools/run_tests.py - ENHANCED TOOL
  - Size: 9.3K
  - Functions: tool_info(), tool_function()
  - Schema: Valid
  - Syntax: Valid
  - Enhancements: Checker contract documented

✓ /dgm/coding_agent.py - REWRITTEN PROMPT
  - Size: 13K
  - Method: forward()
  - Workflow: Multi-phase, detailed
  - Loops: Bounded (no while True)
  - Iterations: Maximum 3
  - Syntax: Valid

✓ /dgm/IMPLEMENTATION_DETAILS.md - DOCUMENTATION
✓ /dgm/CHANGES_SUMMARY.md - SUMMARY
```

## Summary

All three requirements have been fully implemented:

1. ✅ **New Tool: run_samples.py**
   - Enables early sample testing
   - Detects mismatches quickly
   - Provides detailed diagnostics

2. ✅ **Rewritten Prompt in coding_agent.py**
   - 10-step detailed workflow
   - Multi-phase approach
   - Bounded iteration (max 3 rounds)
   - No infinite loops
   - Early exit on success

3. ✅ **Enhanced Checker Contract in run_tests.py**
   - Explicit documentation
   - Clear input/output format
   - Proper exit code semantics
   - Support for custom validators

**Impact:** The coding agent will now properly test solutions before submission, catching algorithmic errors, edge cases, and performance issues that would otherwise result in hidden test failures.

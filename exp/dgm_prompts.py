"""DGM polyglot self-improvement prompts, ported to the LCB domain with minimal edits.

Source: jennyzzt/dgm prompts/self_improvement_prompt.py and prompts/testrepo_prompt.py (polyglot variants).
Edits: the domain sentence (C++/Go/.../Rust -> Python competitive programming), "GitHub issue" wording kept as in
DGM, and the private test section now carries the failing hidden test case. A log-free variant is added for
the prior-only ladder arms (marked NEW).
"""

coding_agent_summary_lcb = """# Coding Agent Summary

- **Main File**: `coding_agent.py`
  - Primary Class: `AgenticSystem`
  - The `forward()` function is the central entry point.
  - Prompts are located either within the `forward()` function or in the `prompts/` directory.
- **Tools**: `tools/`
  - The `tools/` directory contains various tools that LLMs can use to perform specific tasks.
  - Each tool must have a `tool_info()` function that returns a JSON object containing 'name', 'description', and 'input_schema'. The 'input_schema' should be a JSON object containing 'type', 'properties', and 'required'.
  - Each tool must have a `tool_function()` function that takes the arguments defined in input_schema, performs the tool's task, and returns a string.
  - See other tools for reference.
- **Utilities**: `utils/`
  - The `utils/` directory contains utility functions used across the codebase.

- **Additional Details**:
  - The coding agent is trying to solve a programming task. A task is a competitive programming problem in Python: either a complete program that reads standard input and writes standard output, or a method of a given `Solution` class.
  - The agent is very good at automatically utilizing the right available tools at the right time. So do not have an agentic flow that explicitly forces a tool's usage.
  - Be detailed in the prompt about what steps (e.g. implementing tests, refining solutions, etc.) you would like the agent to execute.
  - Common tools, such as file editing and bash commands, are easy for the agent to recognize and use appropriately. However, more complex and niche tools may require explicit instructions in the prompt.
  - Tools should be designed to be as general as possible, ensuring they work across any task. Avoid hardcoding task-specific details or behaviors (e.g., paths or solutions).
  - DO NOT use 'while True' loops in the agent's code IN ANY CASE!! This can cause the agent to get stuck and not respond.
  - Verify the implementation details of helper functions prior to usage to ensure proper integration and expected behavior.
  - **DO NOT create parsing errors tools or functions, collecting raw error messages and letting the agent analyze them will be more efficient.**
\n\n
""" + """
### DOC: tool function schema

Carefully consider whether to add/enhance the current tool or edit the workflow in forward()

Pay special attention to making sure that "required" and "type" are always at the correct level of nesting. For example, "required" should be at the same level as "properties", not inside it.
Make sure that every property, no matter how short, has a type and description correctly nested inside it.
Other arguments than you have seen are not permitted. For example, in "edit_line_ranges" with "type": "array", arguments like "minItems" and "maxItems" are not permitted.
\n\n
"""

diagnose_system_message = """Here is the implementation of the coding agent.

# Coding Agent Implementation
----- Coding Agent Implementation Start -----
{code}
----- Coding Agent Implementation End -----

Your task is to identify ONE detailed plan that would improve the agent's coding ability. The improvement should not be specific to any particular GitHub issue or repository.
"""

lcb_issue_prompt = "Here is the log for the coding agent trying to solve a programming task. A task is a competitive programming problem in Python."

diagnose_prompt = """
# Agent Running Log
----- Agent Running Log Start -----
{md_log}
----- Agent Running Log End -----

# GitHub Issue
The GitHub issue that the agent is trying to solve.
----- GitHub Issue Start -----
{github_issue}
----- GitHub Issue End -----

# Predicted Patch
The agent's predicted patch to solve the issue.
----- Predicted Patch Start -----
{predicted_patch}
----- Predicted Patch End -----

# Private Test Patch
SWE-bench's official private tests to detect whether the issue is solved. This is not available to the agent during evaluation. The agent should try to implement its own tests.
----- Private Test Patch Start -----
{test_patch}
----- Private Test Patch End -----

# Issue Test Results
The test results from SWE-bench using the above official private tests.
----- Issue Test Results Start -----
{eval_log}
----- Issue Test Results End -----

Respond precisely in the following format including the JSON start and end markers:

```json
<JSON>
```

In <JSON>, provide a JSON response with the following fields:
- "log_summarization": Analyze the above logs and summarize how the agent tried to solve the GitHub issue. Note which tools and how they are used, the agent's problem-solving approach, and any issues encountered.
- "potential_improvements": Identify potential improvements to the coding agent that could enhance its coding capabilities. Focus on the agent's general coding abilities (e.g., better or new tools usable across any repository) rather than issue-specific fixes (e.g., tools only usable in one framework). All necessary dependencies and environment setup have already been handled, so do not focus on these aspects.
- "improvement_proposal": Choose ONE high-impact improvement from the identified potential improvements and describe it in detail. This should be a focused and comprehensive plan to enhance the agent's overall coding ability.
- "implementation_suggestion": Referring to the coding agent's summary and implementation, think critically about what feature or tool could be added or improved to best implement the proposed improvement. If the proposed feature can be implemented by modifying the existing tools, describe the modifications needed, instead of suggesting a new tool.
- "problem_description": Phrase the improvement proposal and implementation suggestion as a GitHub issue description. It should clearly describe the feature so that a software engineer viewing the issue and the repository can implement it.

Your response will be automatically parsed, so ensure that the string response is precisely in the correct format. Do NOT include the `<JSON>` tag in your output."""

_json_tail = """
Respond precisely in the following format including the JSON start and end markers:

```json
<JSON>
```

In <JSON>, provide a JSON response with the following fields:
- "potential_improvements": Identify potential improvements to the coding agent's system. All necessary dependencies and environment setup have already been handled, so do not focus on these aspects.
- "improvement_proposal": Choose ONE high-impact improvement from the identified potential improvements and describe it in detail. This should be a focused and comprehensive plan to enhance the agent's overall coding ability.
- "implementation_suggestion": Referring to the coding agent's summary and implementation, think critically about what feature could be added or improved to best implement the proposed improvement.
- "problem_description": Phrase the improvement proposal and implementation suggestion as a GitHub issue description. It should clearly describe the feature so that a software engineer viewing the issue and the repository can implement it.

Your response will be automatically parsed, so ensure that the string response is precisely in the correct format. Do NOT include the `<JSON>` tag in your output."""

diagnose_prompt_emptypatches = """There are some empty patches when attempting to solve GitHub issues. Since the coding agent is stochastic, it may not always produce a patch. Handle cases where the coding agent fails to generate a patch or generates one that only modifies the test cases without editing the primary source code. For example, the simplest solution is to change the prompt to specifically make sure it called the edit tool.

Please analyze the log below to identify why no code edits were made.

# Agent Running Log
----- Agent Running Log Start -----
{md_log}
----- Agent Running Log End -----
""" + _json_tail

diagnose_prompt_stochasticity = """Since the coding agent is stochastic, it may not produce the correct patch for the given problem statement on the first try.
Take into account the agent's stochastic nature and provide a solution to handle such cases.
For example, one solution could be to ask the agent to try multiple times and select the best patch according to the test results. Scale the reflection times is also a good idea.
Giving previous attempts and test results as context to the agent may also help.
The tests for tasks are not provided in the repo, and the agent needs workflow design to implement them.
Agent's own tests that validate the solution may not cover all the cases that will be checked by the private tests during official scoring. So the quality of implemented tests are crucial.

Please analyze the log below to identify how we can improve the testing process and multiple solution attempts.

# Agent Running Log
----- Agent Running Log Start -----
{md_log}
----- Agent Running Log End -----
""" + _json_tail

# NEW (prior-only ladder arms): same system message and JSON contract, no task data at all.
diagnose_prompt_nolog = """The coding agent above solves programming tasks. A task is a competitive programming problem in Python: either a complete program that reads standard input and writes standard output, or a method of a given `Solution` class. Its solution is checked by hidden test cases that the agent never sees.

Based only on the implementation above (no execution logs are available), identify how the agent could be improved.
""" + _json_tail

problem_description_prompt = """# To Implement\n\n{implementation_suggestion}\n\n{problem_description}"""

test_description_dgm_repo = 'The tests in the repository can be run with the bash command `cd /dgm/ && pytest -rA <specific test files>`. If no specific test files are provided, all tests will be run. The given command-line options must be used EXACTLY as specified. Do not use any other command-line options. ONLY test tools and utils. NEVER try to test or run agentic_system.forward().'

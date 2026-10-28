"""Fixed list of 20 generic harness-improvement requests for the clean random-diagnosis arm (PREREG_v3 E2).

The list of exp/random_moves.py (PREREG_v2 B2) with three requests removed because they target the failure that the
first round had found (model responses with neither text nor a tool call, which end runs without a solution): the
request to recover from such responses, the request to rerun the agent when the solution file is unchanged, and the
request to log each response's stop reason and usage. Three generic requests unrelated to output limits or empty
responses replace them. No request mentions empty responses, output or token limits, stop reasons, or reruns after a
missing solution. Each loop step draws one request uniformly at random and hands it to the self-modifying agent in place
of the model-written diagnosis.
"""
MOVES = [
    "Replace the file editing tool with one that supports viewing line ranges, exact string replacement and insertion, instead of rewriting whole files.",
    "Make the bash tool non-interactive: close standard input, add a per-command timeout, and truncate very long outputs.",
    "Before writing code, have the agent restate the input and output format and list the constraints it must handle.",
    "Add an explicit workflow to the prompt: read the problem, plan an algorithm, implement it, then test it on the examples given in the problem.",
    "Add a step that writes a brute-force reference solution and compares it with the main solution on random small inputs.",
    "Add a step that generates a maximum-size input and checks the running time against the limits.",
    "Ask the agent to keep its solution in small functions with clear names and to test each function on a small case.",
    "Run the agent up to three times and keep the attempt whose solution passes the examples in the problem statement.",
    "Give the agent its previous failed attempts and their test outputs as context when it retries.",
    "Add a tool that runs the solution on given inputs and compares its outputs with expected outputs.",
    "Summarize or truncate long tool outputs and old conversation turns to keep the context small.",
    "Add a final review step in which the agent re-reads the problem statement and checks edge cases.",
    "Ask the agent to state the time complexity of its algorithm and compare it with the constraints before coding.",
    "Add error handling around model API calls, with retries and backoff on transient failures.",
    "Add a checklist of common mistakes to the prompt: off-by-one errors, wrong handling of the smallest and largest inputs, and integer division.",
    "Split the work into two phases: an analysis call that produces a plan, then an implementation call that follows it.",
    "Add instructions for reading input efficiently and for avoiding recursion-depth limits.",
    "Let the agent write and run its own unit tests in a scratch directory before finishing.",
    "Simplify the prompt: remove ambiguous instructions and state the exact deliverable, the final solution file.",
    "When a run ends with an exception, catch it and retry the conversation once from the last good state.",
]
assert len(MOVES) == 20

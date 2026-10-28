"""Fixed list of 20 generic harness-improvement requests for the random-diagnosis arm (PREREG_v2 B2).

Written before any v2 run. Each loop step draws one uniformly at random and hands it to the self-modifying agent in
place of the model-written diagnosis. None mentions the output cap or token limits by name.
"""
MOVES = [
    "Replace the file editing tool with one that supports viewing line ranges, exact string replacement and insertion, instead of rewriting whole files.",
    "Make the bash tool non-interactive: close standard input, add a per-command timeout, and truncate very long outputs.",
    "Make the agent loop robust: answer every tool call in a response, and recover from model responses that contain neither text nor a tool call.",
    "Add an explicit workflow to the prompt: read the problem, plan an algorithm, implement it, then test it on the examples given in the problem.",
    "Add a step that writes a brute-force reference solution and compares it with the main solution on random small inputs.",
    "Add a step that generates a maximum-size input and checks the running time against the limits.",
    "After the agent finishes, check that the solution file was actually changed; if it was not, run the agent again.",
    "Run the agent up to three times and keep the attempt whose solution passes the examples in the problem statement.",
    "Give the agent its previous failed attempts and their test outputs as context when it retries.",
    "Add a tool that runs the solution on given inputs and compares its outputs with expected outputs.",
    "Summarize or truncate long tool outputs and old conversation turns to keep the context small.",
    "Add a final review step in which the agent re-reads the problem statement and checks edge cases.",
    "Ask the agent to state the time complexity of its algorithm and compare it with the constraints before coding.",
    "Add error handling around model API calls, with retries and backoff on transient failures.",
    "Log the metadata of each model response (stop reason and usage) to the chat history.",
    "Split the work into two phases: an analysis call that produces a plan, then an implementation call that follows it.",
    "Add instructions for reading input efficiently and for avoiding recursion-depth limits.",
    "Let the agent write and run its own unit tests in a scratch directory before finishing.",
    "Simplify the prompt: remove ambiguous instructions and state the exact deliverable, the final solution file.",
    "When a run ends with an exception, catch it and retry the conversation once from the last good state.",
]
assert len(MOVES) == 20

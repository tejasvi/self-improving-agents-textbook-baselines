def forward(self, taskInfo):
    # Initial reasoning instruction
    initial_instruction = "Please think step by step and then solve the task. Provide a confidence score (0-1) along with your answer."

    # Knowledge retrieval instruction
    knowledge_retrieval_instruction = "Retrieve relevant information from an external knowledge base to support solving the task."

    # Iterative refinement instruction
    refinement_instruction = "Based on the retrieved knowledge, refine your solution and provide an updated answer with a confidence score (0-1)."

    # Final synthesis instruction
    synthesis_instruction = "Combine the refined outputs from all agents to provide a final answer."

    # Initialize agents
    initial_agent = LLMAgentBase(['thinking', 'answer', 'confidence'], 'Initial Reasoning Agent')
    knowledge_retrieval_agent = LLMAgentBase(['knowledge'], 'Knowledge Retrieval Agent')
    refinement_agent = LLMAgentBase(['thinking', 'answer', 'confidence'], 'Refinement Agent')
    synthesis_agent = LLMAgentBase(['thinking', 'answer'], 'Synthesis Agent', temperature=0.1)

    # Number of maximum iterations
    N_max = 5

    # Initial reasoning
    initial_results = initial_agent([taskInfo], initial_instruction)
    intermediate_results = initial_results

    for i in range(N_max):
        # Retrieve relevant knowledge
        knowledge_results = knowledge_retrieval_agent([taskInfo], knowledge_retrieval_instruction)

        # Refine the answer based on retrieved knowledge
        refinement_results = refinement_agent([taskInfo] + knowledge_results, refinement_instruction)
        intermediate_results.extend(refinement_results)

        # Check confidence of refined answers
        valid_confidences = [result for result in refinement_results if result.name == 'confidence' and result.content.strip()]
        try:
            if any(0 <= float(result.content) <= 1 for result in valid_confidences):
                break
        except ValueError:
            continue

    # Integrate the results to get the final answer
    final_results = synthesis_agent([taskInfo] + intermediate_results, synthesis_instruction)
    final_answer = next(info for info in final_results if info.name == 'answer')

    return final_answer
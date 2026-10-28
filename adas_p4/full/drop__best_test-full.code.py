def forward(self, taskInfo):
    # Initialize specialized agents
    numerical_agent = LLMAgentBase(['thinking', 'numerical_insight'], 'Numerical Reasoning Agent')
    linguistic_agent = LLMAgentBase(['thinking', 'linguistic_insight'], 'Linguistic Analysis Agent')
    contextual_agent = LLMAgentBase(['thinking', 'contextual_insight'], 'Contextual Understanding Agent')
    consensus_coordinator = LLMAgentBase(['consensus_insight', 'final_answer'], 'Consensus Coordinator', temperature=0.3)
    synthesis_agent = LLMAgentBase(['thinking', 'final_answer'], 'Synthesis Agent', temperature=0.1)

    # Instructions for each specialized agent
    numerical_instruction = "Analyze the passage and question for any numerical reasoning required and provide your insights."
    linguistic_instruction = "Analyze the passage and question for linguistic patterns and provide your insights."
    contextual_instruction = "Analyze the passage and question for contextual understanding and provide your insights."
    consensus_instruction = "Integrate the insights from each agent and build a consensus on the final answer."
    synthesis_instruction = "Combine the consensus-based insights from other agents to form a thorough understanding and provide your synthesis."

    # Step 1: Collect initial insights from specialized agents
    numerical_results = numerical_agent([taskInfo], numerical_instruction)
    linguistic_results = linguistic_agent([taskInfo], linguistic_instruction)
    contextual_results = contextual_agent([taskInfo], contextual_instruction)

    # Step 2: Use Consensus Coordinator to build consensus among agents
    combined_results = [taskInfo] + numerical_results + linguistic_results + contextual_results
    consensus_results = consensus_coordinator(combined_results, consensus_instruction)

    # Step 3: Iteratively refine insights based on consensus
    for _ in range(3):  # Limit the number of refinement iterations
        combined_results = combined_results[:1] + consensus_results  # Keep taskInfo at the start
        consensus_results = consensus_coordinator(combined_results, consensus_instruction)
        if any('satisfactory' in insight.content.lower() for insight in consensus_results):
            break

    # Step 4: Synthesize final answer using Synthesis Agent
    final_result = synthesis_agent([taskInfo] + consensus_results, synthesis_instruction)

    return final_result[1]  # Return the final answer

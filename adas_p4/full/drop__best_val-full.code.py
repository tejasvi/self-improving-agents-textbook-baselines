def forward(self, taskInfo):
    # Initialize specialized agents
    numerical_agent = LLMAgentBase(['thinking', 'numerical_insight'], 'Numerical Reasoning Agent')
    linguistic_agent = LLMAgentBase(['thinking', 'linguistic_insight'], 'Linguistic Analysis Agent')
    contextual_agent = LLMAgentBase(['thinking', 'contextual_insight'], 'Contextual Understanding Agent')
    synthesis_agent = LLMAgentBase(['thinking', 'synthesis_insight'], 'Synthesis Agent')
    adaptive_agent = LLMAgentBase(['priority', 'updated_insight'], 'Real-Time Adaptive Agent', temperature=0.3)
    coordinator_agent = LLMAgentBase(['thinking', 'final_answer'], 'Coordinator Agent', temperature=0.3)

    # Instructions for each specialized agent
    numerical_instruction = "Analyze the passage and question for any numerical reasoning required and provide your insights."
    linguistic_instruction = "Analyze the passage and question for linguistic patterns and provide your insights."
    contextual_instruction = "Analyze the passage and question for contextual understanding and provide your insights."
    synthesis_instruction = "Combine the insights from other agents to form a thorough understanding and provide your synthesis."
    adaptive_instruction = "Evaluate the importance of each component's insights and dynamically adjust the focus and assignments for further refinement."
    coordinator_instruction = "Given the refined insights, determine the final answer. If necessary, reassign tasks for further refinement."

    # Step 1: Collect initial insights from specialized agents
    numerical_results = numerical_agent([taskInfo], numerical_instruction)
    linguistic_results = linguistic_agent([taskInfo], linguistic_instruction)
    contextual_results = contextual_agent([taskInfo], contextual_instruction)

    # Step 2: Use Real-Time Adaptive Agent to evaluate and adjust focus
    adaptive_inputs = [taskInfo] + numerical_results + linguistic_results + contextual_results
    adaptive_results = adaptive_agent(adaptive_inputs, adaptive_instruction)
    priority = [result for result in adaptive_results if result.name == 'priority']
    updated_insights = [result for result in adaptive_results if result.name == 'updated_insight']

    # Step 3: Refine insights based on real-time adjustments
    for _ in range(3):  # Limit the number of refinement iterations to 3
        new_refinement_results = []  # Collect new refinements in each iteration
        for priority_insight in priority:
            if 'numerical' in priority_insight.content.lower():
                new_refinement_results.extend(numerical_agent([taskInfo] + updated_insights, numerical_instruction))
            elif 'linguistic' in priority_insight.content.lower():
                new_refinement_results.extend(linguistic_agent([taskInfo] + updated_insights, linguistic_instruction))
            elif 'contextual' in priority_insight.content.lower():
                new_refinement_results.extend(contextual_agent([taskInfo] + updated_insights, contextual_instruction))
        adaptive_inputs = [taskInfo] + new_refinement_results
        adaptive_results = adaptive_agent(adaptive_inputs, adaptive_instruction)
        priority = [result for result in adaptive_results if result.name == 'priority']
        updated_insights = [result for result in adaptive_results if result.name == 'updated_insight']
        if any('satisfactory' in insight.content.lower() for insight in updated_insights):
            break

    # Step 4: Synthesize final answer
    synthesis_inputs = [taskInfo] + updated_insights
    synthesis_results = synthesis_agent(synthesis_inputs, synthesis_instruction)

    # Step 5: Coordinator Agent to determine final refined answer
    final_result = coordinator_agent([taskInfo] + synthesis_results, coordinator_instruction)

    return final_result[1]  # Return the final answer

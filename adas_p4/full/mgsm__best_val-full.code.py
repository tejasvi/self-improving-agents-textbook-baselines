def forward(self, taskInfo):
    # Instruction for the Teacher agent to explain the task and provide feedback
    teacher_instruction = "Please explain the task in detail and provide any necessary hints or steps to solve it."

    # Instruction for the Student agent to solve the task based on the Teacher's explanation
    student_instruction = "Using the Teacher's explanation and feedback, please solve the task step by step."

    # Instruction for the Verifier agent to review the Student's answer and provide a final decision
    verifier_instruction = "Please review the Student's answer, verify its correctness, and provide a final decision. Also, give feedback on the Teacher's explanation and the Student's approach."

    # Initialize the Teacher, Student, and Verifier agents
    teacher_agent = LLMAgentBase(['explanation'], 'Teacher Agent')
    student_agent = LLMAgentBase(['thinking', 'answer'], 'Student Agent')
    verifier_agent = LLMAgentBase(['final_verdict', 'teacher_feedback', 'student_feedback'], 'Verifier Agent')

    # Teacher agent provides explanation and hints
    teacher_output = teacher_agent([taskInfo], teacher_instruction)
    explanation = teacher_output[0]

    # Student agent attempts to solve the task based on Teacher's explanation
    student_output = student_agent([taskInfo, explanation], student_instruction)
    thinking, answer = student_output

    # Verifier agent reviews the Student's answer and provides feedback
    verifier_output = verifier_agent([taskInfo, thinking, answer], verifier_instruction)
    final_verdict, teacher_feedback, student_feedback = verifier_output

    # Teacher agent refines the explanation based on Verifier's feedback
    refined_teacher_output = teacher_agent([taskInfo, teacher_feedback], teacher_instruction)
    refined_explanation = refined_teacher_output[0]

    # Student agent refines the solution based on refined Teacher's explanation and Verifier's feedback
    refined_student_output = student_agent([taskInfo, refined_explanation, student_feedback], student_instruction)
    refined_thinking, refined_answer = refined_student_output

    # Return the final answer
    return refined_answer

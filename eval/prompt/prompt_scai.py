sys="""
For the given scientific problem in the Chemistry, Physics, or Mathematics category, please provide a concise and step-by-step solution. Ensure that your final answer is placed within \\box{}. If the final answer contains \\pi or \\sqrt{2}, convert it to a decimal approximation and calculate the final numerical value, using approximately 3.14159265359 for \\pi and 1.41421356237 for \\sqrt{2}.  If the answer is in scientific notation, such as 1.8 * 10^4, the base value (10^4) will be provided in the problem, and the final answer should be expressed as 1.8. The unit will be provided in the problem and should not be included in the answer. The final answer should be expressed solely as a decimal number.
"""

# sys_new="""
# For the given scientific problem in the Chemistry, Physics, or Mathematics category, please provide a concise and step-by-step solution. Ensure that your final answer is placed within \\box{}. If the final answer contains \\pi or \\sqrt{2}, convert it to a decimal approximation and calculate the final numerical value. If the answer is in scientific notation, such as 1.8 * 10^4, the base value (10^4) will be provided in the problem, and the final answer should be expressed as 1.8. The unit will be provided in the problem and should not be included in the answer. The final answer should be expressed solely as a decimal number (2 digits).
# """

sys_cal="""
Please provide a clear and step-by-step solution for a scientific problem in the categories of Chemistry, Physics, or Mathematics. The problem will specify the unit of measurement, which should not be included in the answer. Express the final answer as a decimal number with three digits after the decimal point. Conclude the answer by stating "The answer is therefore [ANSWER]."
"""

sys_cal_box="""
Please provide a clear and step-by-step solution for a scientific problem within the fields of Chemistry, Physics, or Mathematics. The problem will specify the unit of measurement. In your conclusion, state "The answer is therefore \\box{[ANSWER]}" where [ANSWER] refers to a decimal number with three digits after the decimal point.
"""

sys_cal_box2="""
Please provide a clear and step-by-step solution for a scientific problem in the categories of Chemistry, Physics, or Mathematics. The problem will specify the unit of measurement, which should not be included in the answer. Express the final answer as a decimal number with three digits after the decimal point. Conclude the answer by stating "The answer is therefore \\boxed{[ANSWER]}."
"""

sys_cal_box3="""
Please provide a clear and step-by-step solution for a scientific problem in the categories of Calculus. The problem will specify the unit of measurement, which should not be included in the answer. Express the final answer as a decimal number with three digits after the decimal point. Conclude the answer by stating "The answer is therefore \\boxed{[ANSWER]}."
"""

sys_cal_box4="""
Given a scientific problem in the categories of Chemistry, Physics, or Mathematics, your task is to provide a clear and step-by-step solution for the problem. Conclude your solution by explicitly stating the final answer in the following format: "The answer is therefore \\boxed{[ANSWER]}." The problem will specify the unit of measurement, which should not be included in the answer. Please express the final answer as a decimal number with three digits after the decimal point.
"""

sys_cal_box5="""
Given a scientific problem in the categories of Chemistry, Physics, or Mathematics, your task is to provide a clear and step-by-step solution for the problem. Conclude your solution by explicitly stating the final answer in the following format: "The answer is \\boxed{[ANSWER]}." The problem will specify the unit of measurement, which should not be included in the answer. Please express the final answer as a decimal number with three digits after the decimal point.
"""

sys_cal_box6="""
Given a scientific problem, please provide a step-by-step solution with concise and clear details. The problem will provide the unit of measurement.
"""

sys_tool_python="""
Please provide a clear and step-by-step solution for a scientific problem in the categories of Chemistry, Physics, or Mathematics. The problem will specify the unit of measurement. Please translate the solution steps into Python code and encase the Python code within triple backticks for clarity.
"""


sys_tool_wolfram="""
Please provide a clear and step-by-step solution for a scientific problem in the categories of Chemistry, Physics, or Mathematics. The problem will specify the unit of measurement. Please translate the solution steps into Wolfram code and encase the Wolfram Language code within triple backticks for clarity.
"""

sys_ana="""
Examine the given problem, the correct solution, and the model's solution. Identify the reason for the error in the model's solution based on the following 10 categories:
1. Logical Decomposition and Analysis Skills: This ability involves decomposing the problem into smaller, manageable parts, and understanding the relationships between these parts.
2. Identification of Assumptions: This skill involves the AI's ability to recognize relevant and necessary assumptions in the problem. 
3. Spatial Perception: This is important for understanding problems in areas such as physics and chemistry, where you need to visualize molecules, forces, fields, etc.
4. Causal Reasoning: This is the ability to understand cause and effect relationships.
5. Problem Deduction Skills: This pertains to the ability to infer and deduce potential solutions or underlying principles from the given information in a problem.
6. Abstract Reasoning: This skill involves the ability to understand complex concepts that can't be perceived physically, and to recognize patterns or relationships beyond concrete examples.
7. Scientific Literacy:  This skill involves a comprehensive understanding of key scientific principles, terminology, and methodologies across a range of disciplines.
8. Code Conversion Skills: This denotes the ability to accurately translate solution steps into different programming languages, like Python or Wolfram, without syntax errors.
9. Logical Reasoning: This is the ability to make a reasoned argument and to identify fallacies or inconsistencies in an argument or set of data.
10. Calculation Skills: This involves the ability to accurately carry out mathematical operations and computations. 
Conclude your final error reason category number within \\boxed{}.
"""
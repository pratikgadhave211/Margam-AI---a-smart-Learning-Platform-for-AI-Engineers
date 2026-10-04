from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from app.agents.llm_service import solver_llm

class FailureSummary(BaseModel):
    improvements: list[str] = Field(description="List of areas where the code failed and why the retrieved chunks didn't match the expected claims.")
    approach_hints: list[str] = Field(description="General advice on how to approach chunking, embedding, or retrieval for this type of problem.")
    specific_hints: list[str] = Field(description="Specific, actionable hints comparing their code logic to the ideal logic without giving away the exact answer.")

class SuccessSummary(BaseModel):
    praise: str = Field(description="A short congratulatory message celebrating their success.")
    further_improvements: list[str] = Field(description="Suggestions on how the code could be further optimized (e.g., performance, memory, edge cases).")
    next_steps: list[str] = Field(description="Recommendations on what advanced concepts they should explore next.")

def solver_agent_summary(test_results: list, user_code: str, ideal_code: str, is_success: bool):
    """
    Analyzes the user's RAG sandbox performance and generates a structured summary.
    If they failed, gives hints and improvements.
    If they succeeded, gives praise and further optimizations.
    """
    
    # Format the test results into a readable string for the LLM
    results_str = ""
    for i, res in enumerate(test_results):
        results_str += f"\nTest Case {i+1}:\n"
        results_str += f"- Passed: {res.get('passed')}\n"
        results_str += f"- Score: {res.get('avg_score')}\n"
        # If retrieved chunks were passed back from the runner, show them
        if "retrieved_chunks" in res:
            results_str += f"- Retrieved Chunks: {res.get('retrieved_chunks')}\n"
            
    system_prompt = (
        "You are an expert AI mentor grading a student's RAG (Retrieval-Augmented Generation) code submission.\n"
        "Your job is to compare the User's Code with the Ideal Code and analyze their Sandbox Test Results.\n"
        "Do not write code for them, but explain the concepts they are missing or what they did perfectly.\n"
    )
    
    user_prompt = (
        "User Code:\n{user_code}\n\n"
        "Ideal Code:\n{ideal_code}\n\n"
        "Sandbox Execution Results:\n{test_results}\n\n"
        "Generate the structured summary based on these results."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])
    
    # Dynamically choose the structured output schema based on whether they passed or failed
    if is_success:
        structured_llm = solver_llm.with_structured_output(SuccessSummary)
    else:
        structured_llm = solver_llm.with_structured_output(FailureSummary)
        
    chain = prompt | structured_llm
    
    result = chain.invoke({
        "user_code": user_code,
        "ideal_code": ideal_code,
        "test_results": results_str
    })
    
    # Convert Pydantic object to dict for the API response
    return result.dict()

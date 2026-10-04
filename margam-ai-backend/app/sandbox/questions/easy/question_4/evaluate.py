from llm_client import llm
from langchain_core.prompts import PromptTemplate

def evaluate_output(actual: str, expected: str) -> dict:
    if not isinstance(actual, str) or len(actual.strip()) == 0:
         return {"passed": False, "score": 0.0, "mismatches": ["Output must be a non-empty string."]}
         
    eval_prompt = PromptTemplate.from_template(
        "You are a strict grader. The user was tasked with rewriting an angry message into polite corporate-speak.\n\n"
        "User's Output: {message}\n\n"
        "Did the user successfully neutralize the anger and adopt a highly professional, polite tone? "
        "Reply ONLY with the exact word YES or NO."
    )
    
    try:
        result = (eval_prompt | llm).invoke({"message": actual}).content.strip().upper()
        if "YES" in result:
            return {"passed": True, "score": 1.0, "mismatches": []}
        else:
            return {"passed": False, "score": 0.0, "mismatches": [f"The LLM failed to adopt the corporate tone. Output was: {actual}"][:200]}
    except Exception as e:
         return {"passed": False, "score": 0.0, "mismatches": [f"Evaluator LLM error: {str(e)}"]}

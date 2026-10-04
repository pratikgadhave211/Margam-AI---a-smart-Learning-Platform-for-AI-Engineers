def evaluate_output(actual: str, expected: str) -> dict:
    if not isinstance(actual, str):
        return {"passed": False, "score": 0.0, "mismatches": [f"Expected a string, got {type(actual).__name__}"]}
        
    if expected == "error":
        if actual != "ERROR: Payload too large":
            return {"passed": False, "score": 0.0, "mismatches": [f"Expected 'ERROR: Payload too large' for text > 100 tokens, but got: '{actual[:50]}...'"]}
        return {"passed": True, "score": 1.0, "mismatches": []}
        
    if expected == "summary":
        if actual == "ERROR: Payload too large":
            return {"passed": False, "score": 0.0, "mismatches": ["Returned 'Payload too large' for a text that is under 100 tokens."]}
        
        # Check if they successfully used max_tokens (approximate check based on words)
        # 50 tokens is usually ~35 words. If they return 100 words, they failed to bind max_tokens.
        if len(actual.split()) > 75:
             return {"passed": False, "score": 0.0, "mismatches": ["Response is too long! Did you forget to bind max_tokens=50?"]}
             
        return {"passed": True, "score": 1.0, "mismatches": []}

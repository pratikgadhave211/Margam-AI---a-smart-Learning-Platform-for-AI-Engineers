import re

def evaluate_output(actual: str, expected: str) -> dict:
    mismatches = []
    
    if not isinstance(actual, str):
        return {
            "passed": False,
            "score": 0.0,
            "mismatches": [f"Expected a string, but got {type(actual).__name__}"]
        }
        
    actual_clean = re.sub(r'[^\w\s]', '', actual.lower()).strip()
    expected_clean = re.sub(r'[^\w\s]', '', expected.lower()).strip()
    
    # Check if the LLM successfully recalled the expected fact from the history
    if expected_clean not in actual_clean:
        mismatches.append(f"AI failed to remember the context. Expected answer containing: '{expected}', but AI responded with '{actual}'")
        return {
            "passed": False,
            "score": 0.0,
            "mismatches": mismatches
        }
        
    return {
        "passed": True,
        "score": 1.0,
        "mismatches": []
    }

def evaluate_output(actual: dict, expected: dict) -> dict:
    mismatches = []
    
    for key, expected_val in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key: '{key}'")
            continue
        actual_val = actual[key]
        if type(actual_val) != type(expected_val):
            mismatches.append(f"Type mismatch for '{key}': expected {type(expected_val).__name__}, got {type(actual_val).__name__}")
        elif actual_val != expected_val:
            mismatches.append(f"Value mismatch for '{key}': expected '{expected_val}', got '{actual_val}'")
            
    passed = len(mismatches) == 0
    score = 1.0 if passed else 0.0
    return {"passed": passed, "score": score, "mismatches": mismatches}

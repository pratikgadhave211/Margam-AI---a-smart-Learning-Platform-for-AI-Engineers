import asyncio
import importlib.util
import sys
import os
from .test_cases import TEST_CASES
from .evaluate import evaluate_output
from .rules import MAX_POINTS

async def evaluate_submission(injected_filepath: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    spec = importlib.util.spec_from_file_location("user_submission", injected_filepath)
    user_module = importlib.util.module_from_spec(spec)
    sys.modules["user_submission"] = user_module
    
    try:
        spec.loader.exec_module(user_module)
    except Exception as e:
        return {"status": "FAILURE", "final_score": 0.0, "error": f"Compilation error: {str(e)}"}
        
    if not hasattr(user_module, 'chat'):
        return {"status": "FAILURE", "final_score": 0.0, "error": "Missing function: chat"}

    results = []
    total_weight = 0
    total_points = 0
    warnings = []
    
    for i, tc in enumerate(TEST_CASES):
        weight = tc.get("weight", 1.0)
        total_weight += weight
        
        try:
            actual = user_module.chat(**tc["input"])
        except Exception as e:
            actual = ""
            warnings.append(f"Test case {i+1} runtime error: {str(e)}")
            
        eval_res = evaluate_output(actual, tc["expected"])
        
        test_points = round((weight / len(TEST_CASES)) * MAX_POINTS, 2) if total_weight > 0 else 0
        points_earned = test_points if eval_res["passed"] else 0.0
        total_points += points_earned
        
        if not eval_res["passed"]:
            warnings.append(f"Test case {i+1} failed: {', '.join(eval_res['mismatches'])}")
            
        results.append({
            "passed": eval_res["passed"],
            "score": eval_res["score"],
            "weight": weight,
            "points_earned": points_earned,
            "max_points": test_points,
            "mismatches": eval_res["mismatches"]
        })

    is_success = all(r["passed"] for r in results)
    
    return {
        "status": "SUCCESS" if is_success else "FAILURE",
        "final_score": 1.0 if is_success else 0.0,
        "points_earned": round(total_points, 2),
        "max_points": MAX_POINTS,
        "warnings": warnings,
        "test_results": results,
        "summary": {"feedback": "Excellent! Your AI successfully remembered the conversation history." if is_success else "Check how you are mapping the dictionaries to HumanMessage and AIMessage objects."},
    }

import asyncio
import importlib.util
import sys
import os
import typing
from .test_cases import TEST_CASES
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
        
    if not hasattr(user_module, 'generate_blog'):
        return {"status": "FAILURE", "final_score": 0.0, "error": "Missing function: generate_blog"}

    results = []
    total_weight = 0
    total_points = 0
    warnings = []
    
    for i, tc in enumerate(TEST_CASES):
        weight = tc.get("weight", 1.0)
        total_weight += weight
        
        passed = False
        score = 0.0
        mismatches = []
        
        try:
            generator = user_module.generate_blog(**tc["input"])
            
            if not isinstance(generator, typing.AsyncGenerator):
                mismatches.append("You must return an AsyncGenerator using yield, not a standard string or list.")
            else:
                chunks = []
                async for chunk in generator:
                    chunks.append(chunk)
                    
                if len(chunks) < 5:
                    mismatches.append(f"Response yielded too few chunks ({len(chunks)}). Did you yield chunk by chunk using llm.astream?")
                else:
                    passed = True
                    score = 1.0
        except Exception as e:
            mismatches.append(f"Test case runtime error: {str(e)}")
            
        test_points = round((weight / len(TEST_CASES)) * MAX_POINTS, 2) if total_weight > 0 else 0
        points_earned = test_points if passed else 0.0
        total_points += points_earned
        
        if not passed:
            warnings.append(f"Test case {i+1} failed: {', '.join(mismatches)}")
            
        results.append({
            "passed": passed,
            "score": score,
            "weight": weight,
            "points_earned": points_earned,
            "max_points": test_points,
            "mismatches": mismatches
        })

    is_success = all(r["passed"] for r in results)
    
    return {
        "status": "SUCCESS" if is_success else "FAILURE",
        "final_score": 1.0 if is_success else 0.0,
        "points_earned": round(total_points, 2),
        "max_points": MAX_POINTS,
        "warnings": warnings,
        "test_results": results,
        "summary": {"feedback": "Excellent! You successfully yielded tokens from the LLM asynchronously!" if is_success else "Review your async generator syntax."},
    }

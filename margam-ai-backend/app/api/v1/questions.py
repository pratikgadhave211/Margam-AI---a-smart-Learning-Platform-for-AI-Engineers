import importlib
import os
import uuid
import asyncio
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.submission import CodeSubmission, SubmissionResponse
from app.api.v1.auth import verify_token

# Removed auth dependency temporarily
router = APIRouter()

@router.get("/{difficulty}/{question_id}")
async def get_question(difficulty: str, question_id: str):
    question_dir = os.path.join("app", "sandbox", "questions", difficulty, question_id)
    if not os.path.exists(question_dir):
        raise HTTPException(status_code=404, detail="Question not found.")
        
    try:
        rules_module = importlib.import_module(f"app.sandbox.questions.{difficulty}.{question_id}.rules")
        editor_module = importlib.import_module(f"app.sandbox.questions.{difficulty}.{question_id}.editor")
        
        return {
            "title": rules_module.TITLE,
            "difficulty": rules_module.DIFFICULTY,
            "description": rules_module.DESCRIPTION,
            "examples": getattr(rules_module, "EXAMPLES", []),
            "hints": getattr(rules_module, "HINTS", []),
            "max_points": rules_module.MAX_POINTS,
            "starter_code": editor_module.STARTER_CODE.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load question data: {str(e)}")

@router.post("/{difficulty}/{question_id}/evaluate", response_model=SubmissionResponse)
async def evaluate_code(difficulty: str, question_id: str, request: CodeSubmission):
    run_id = str(uuid.uuid4())
    question_dir = os.path.join("app", "sandbox", "questions", difficulty, question_id)
    
    if not os.path.exists(question_dir):
        raise HTTPException(status_code=404, detail="Question not found.")
        
    runs_dir = os.path.join("app", "sandbox", "runs")
    os.makedirs(runs_dir, exist_ok=True)
    output_path = os.path.join(runs_dir, f"sandbox_run_{run_id}.py")
    
    try:
        # 1. Run static analysis checker (Common)
        from app.sandbox.utils import check_errors
        check_result = check_errors.check_code_validity(request.code)
        if not check_result["valid"]:
            return SubmissionResponse(status="FAILURE", final_score=0.0, error=check_result["error"])
            
        # 2. Inject and evaluate
        from app.sandbox.utils import injector
        runner_module = importlib.import_module(f"app.sandbox.questions.{difficulty}.{question_id}.runner")
        
        injected_file = injector.inject_user_code(request.code, output_path)
        result = await asyncio.wait_for(runner_module.evaluate_submission(injected_file), timeout=15.0)
        
        return SubmissionResponse(**result)
        
    except asyncio.TimeoutError:
        return SubmissionResponse(status="FAILURE", final_score=0.0, error="Execution timed out.")
    except Exception as e:
        return SubmissionResponse(status="FAILURE", final_score=0.0, error=f"Execution error: {str(e)}")
    finally:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except OSError:
                pass

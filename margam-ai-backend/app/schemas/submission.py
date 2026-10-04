from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CodeSubmission(BaseModel):
    code: str

class TestCaseResult(BaseModel):
    passed: bool
    score: float
    weight: float
    points_earned: float
    max_points: float
    mismatches: List[str] = []

class SubmissionResponse(BaseModel):
    status: str
    final_score: float
    points_earned: float = 0.0
    max_points: float = 0.0
    warnings: List[str] = []
    test_results: List[TestCaseResult] = []
    summary: Dict[str, Any] = {}
    error: Optional[str] = None

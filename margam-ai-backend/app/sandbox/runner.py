import asyncio
import importlib.util
import sys

from app.sandbox.templates.vectorstore import FAISSVectorStore
from app.sandbox.document import DOCUMENT_TEXT, GOLDEN_DATASET
from app.sandbox.evaluate import calculate_metrics

async def run_single_test(rag_instance, test_case):
    """Runs a single query against the user's RAG class."""
    try:
        # Call the user's injected retrieve method (letting them use their own top_k!)
        retrieved_chunks = rag_instance.retrieve(test_case["query"])
        
        # Fallback if user code returns None
        if not isinstance(retrieved_chunks, list):
            retrieved_chunks = []
            
    except Exception as e:
        print(f"User code crashed on query '{test_case['query']}': {e}")
        retrieved_chunks = []
        
    all_chunks = rag_instance.vector_store.chunks if rag_instance.vector_store else []
    return calculate_metrics(retrieved_chunks, test_case["expected_claims"], all_chunks, test_case.get("weight", 1.0))

async def evaluate_submission(injected_filepath: str):
    """
    Loads the user's injected script dynamically, instantiates their class,
    runs the setup phase (chunk -> embed -> index), and then tests retrieval.
    """
    # 1. Dynamically load the user's python file (produced by injector.py)
    module_name = "user_submission"
    spec = importlib.util.spec_from_file_location(module_name, injected_filepath)
    user_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = user_module
    spec.loader.exec_module(user_module)
    
    # 2. Instantiate the user's RAG class
    # We pass the realistic dense document for the user to chunk
    RAG = user_module.RAG
    rag_instance = RAG(documents=DOCUMENT_TEXT)
    
    # 3. Setup Phase: The user's code builds the pipeline
    print("Running User's chunk() and embed() methods...")
    
    # Give the RAG class access to the FAISS model early so their embed() can use it
    v_store = FAISSVectorStore()
    rag_instance.vector_store = v_store
    
    try:
        # A. User chunks the document
        user_chunks = rag_instance.chunk(DOCUMENT_TEXT)
        
        # B. User embeds each chunk
        user_embeddings = []
        for c in user_chunks:
            emb = rag_instance.embed(c)
            user_embeddings.append(emb)
            
        # C. We take their chunks and their embeddings and load them into FAISS
        v_store.build_index_with_embeddings(user_chunks, user_embeddings)
        
    except Exception as e:
        print(f"Pipeline Setup Failed: {e}")
        return {"status": "FAILURE", "final_score": 0.0, "error": str(e)}
        
    # 4. Testing Phase: Run all test cases in PARALLEL using asyncio
    print("Running Retrieval Test Cases...")
    tasks = [run_single_test(rag_instance, test_case) for test_case in GOLDEN_DATASET]
    results = await asyncio.gather(*tasks) 
    
    # 5. Calculate Final Weighted Average Score across all test cases
    total_weight = sum(res["weight"] for res in results)
    if total_weight > 0:
        total_avg_score = sum(res["avg_score"] * res["weight"] for res in results) / total_weight
    else:
        total_avg_score = 0.0
    
    # 6. Check against Threshold & Calculate Points (Total 25 points)
    THRESHOLD = 0.6
    MAX_POINTS = 25
    
    warnings = []
    total_points_earned = 0.0
    
    for i, res in enumerate(results):
        res["passed"] = res["avg_score"] >= THRESHOLD
        
        # Distribute the 25 points proportionally based on the test case's weight
        test_max_points = (res["weight"] / total_weight) * MAX_POINTS if total_weight > 0 else 0
        res["max_points"] = round(test_max_points, 2)
        
        if res["passed"]:
            res["points_earned"] = round(test_max_points, 2)
            total_points_earned += test_max_points
        else:
            res["points_earned"] = 0.0
            warnings.append(f"Test case {i+1} failed (Score: {round(res['avg_score'], 2)}). Lost {round(test_max_points, 2)} points out of {MAX_POINTS}.")
            
    # Success is determined by the global weighted average, not individual tests
    is_success = total_avg_score >= THRESHOLD
    
    # Generate the structured AI summary based on the results
    with open(injected_filepath, "r", encoding="utf-8") as f:
        user_code = f.read()
        
    from app.sandbox.seed.ideal_code import IDEAL_CODE
    from app.agents.solving_time_agent import solver_agent_summary
    
    agent_summary = solver_agent_summary(results, user_code, IDEAL_CODE, is_success)
    
    return {
        "status": "SUCCESS" if is_success else "FAILURE",
        "final_score": round(total_avg_score, 2),
        "points_earned": round(total_points_earned, 2),
        "max_points": MAX_POINTS,
        "warnings": warnings,
        "test_results": results,
        "summary": agent_summary
    }     


   
 

# --- Example of how the pipeline runs ---
if __name__ == "__main__":
    # asyncio.run(evaluate_submission("sandbox_run_123.py"))
    pass

STARTER_CODE = """
import tiktoken
from llm_client import llm

def summarize(text: str) -> str:
    # 1. Initialize the tiktoken encoder (use "cl100k_base")
    
    # 2. Encode the text and get the exact token count
    
    # 3. If tokens > 100, return "ERROR: Payload too large"
    
    # 4. Bind the llm to limit output to max_tokens=50
    
    # 5. Invoke the restricted llm and return the string content
    pass
"""

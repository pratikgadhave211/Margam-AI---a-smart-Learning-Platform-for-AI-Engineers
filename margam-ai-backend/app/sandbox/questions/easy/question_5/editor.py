STARTER_CODE = """
from typing import AsyncGenerator
from llm_client import llm

async def generate_blog(topic: str) -> AsyncGenerator[str, None]:
    prompt = f"Write a 3 paragraph blog post about {topic}"
    
    # 1. Asynchronously iterate over llm.astream(prompt)
    
    # 2. yield the .content of each chunk
    pass
"""

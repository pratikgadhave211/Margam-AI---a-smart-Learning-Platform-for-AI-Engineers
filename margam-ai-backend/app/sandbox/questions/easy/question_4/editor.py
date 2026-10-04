STARTER_CODE = """
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from llm_client import llm

def translate_message(message: str) -> str:
    # You are given a messy list of tuples. 
    # You must format these into a list of dictionaries so they work with FewShotPromptTemplate!
    messy_examples = [
        ("I am not doing this pointless project.", "I would like to better understand the strategic alignment of this project before proceeding."),
        ("Tell marketing their new design looks like a child drew it.", "Please provide constructive feedback to the marketing team regarding the new design aesthetics."),
        ("Stop messaging me after 5 PM.", "I will review this first thing tomorrow morning during working hours.")
    ]
    
    # 1. Clean the messy_examples into a list of dicts [{"input": ..., "output": ...}]
    
    # 2. Create example_prompt
    
    # 3. Create FewShotPromptTemplate using the cleaned examples
    
    # 4. Create chain and invoke
    pass
"""

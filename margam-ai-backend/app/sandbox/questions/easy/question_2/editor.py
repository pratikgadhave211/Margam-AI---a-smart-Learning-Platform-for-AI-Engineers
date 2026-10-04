STARTER_CODE = """
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_client import llm 

def chat(message: str, history: list[dict]) -> str:
    # history looks like this: [{"role": "user", "content": "hi"}, {"role": "ai", "content": "hello!"}]
    
    # 1. Create a ChatPromptTemplate using from_messages
    # Make sure to include the MessagesPlaceholder for the history!
    
    # 2. Chain it to the llm
    
    # 3. Invoke the chain passing in both the history and the new message
    
    # 4. Return the string content of the AI's response
    pass
"""

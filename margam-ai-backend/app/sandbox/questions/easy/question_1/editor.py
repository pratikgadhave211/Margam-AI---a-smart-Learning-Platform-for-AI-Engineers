STARTER_CODE = """
from typing import Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from llm_client import llm 

class SupportTicket(BaseModel):
    pass

def analyze_support_ticket(email_text: str) -> SupportTicket:
    pass
"""

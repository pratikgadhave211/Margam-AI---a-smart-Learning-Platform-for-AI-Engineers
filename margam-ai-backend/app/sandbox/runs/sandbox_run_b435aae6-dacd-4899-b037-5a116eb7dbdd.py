from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from llm_client import llm 

class SupportTicket(BaseModel):
    intent: str
    urgency: int
    customer_sentiment: str
def analyze_support_ticket(email_text: str) -> SupportTicket:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI customer support triage bot for SwiftCart. Categorize the user's email."),
        ("user", "{email}")
    ])
    
    # 2. Bind the Pydantic schema to the LLM to force structured output
    structured_llm = llm.with_structured_output(SupportTicket)
    
    # 3. Chain the prompt and the structured LLM together
    chain = prompt | structured_llm
    
    # 4. Invoke the chain with the user's email text
    result = chain.invoke({"email": email_text})
    
    return result
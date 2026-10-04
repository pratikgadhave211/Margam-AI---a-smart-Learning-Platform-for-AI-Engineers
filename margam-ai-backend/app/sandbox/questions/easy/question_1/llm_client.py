import os
from langchain_openai import ChatOpenAI

# Provide a real Langchain ChatOpenAI client pointing to OpenRouter
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    max_retries=2
)

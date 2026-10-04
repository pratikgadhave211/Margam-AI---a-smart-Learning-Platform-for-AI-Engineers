import os
from langchain_openai import ChatOpenAI

def get_solver_llm(temperature=0.7):
    """
    Initializes the Langchain ChatOpenAI wrapper configured to use
    OpenRouter's endpoint and the GPT-4o-mini model.
    """
    # Grab the API key from the environment
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing from environment variables.")

    return ChatOpenAI(
        model="openai/gpt-4o-mini",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=temperature
    )

# Export a default instance for easy importing
solver_llm = get_solver_llm()

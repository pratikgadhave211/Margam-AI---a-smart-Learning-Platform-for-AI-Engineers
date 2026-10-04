import os
from langchain_openai import ChatOpenAI

# This file exists purely to provide Jedi with type hints for the frontend autocomplete.
# During actual execution, the sandbox injects its own version of llm_client which matches this.
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    max_retries=2
)

 
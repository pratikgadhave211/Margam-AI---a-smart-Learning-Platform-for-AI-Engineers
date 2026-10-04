TITLE = "The Tokenizer — Measuring & Restricting Tokens"
DIFFICULTY = "easy"
DESCRIPTION = {
    "scenario": "Your AI startup is burning money because users are pasting massive 50-page PDFs into the chat, and the LLM is responding with expensive 3-page essays. You need to implement strict token controls!",
    "tasks": [
        "Complete the `summarize` function.",
        "Use `tiktoken.get_encoding(\"cl100k_base\")` to count the exact number of tokens in the `text` parameter.",
        "If the token count is strictly greater than 100, return the exact string: `\"ERROR: Payload too large\"`.",
        "If it's safe (<= 100 tokens), you must restrict the LLM's output to a maximum of 50 tokens to save money using `llm.bind(max_tokens=50)`.",
        "Invoke the restricted LLM with the text and return the raw string content of the AI's response."
    ]
}
MAX_POINTS = 25
THRESHOLD = 0.8
FORBIDDEN_EDITS = ["summarize"] 
ALLOWED_IMPORTS = ["tiktoken"]

EXAMPLES = [
    {
        "input": "text = 'This is a short text'",
        "output": "'This text is short.'",
        "explanation": "The text was under 100 tokens, so the LLM successfully summarized it within the 50-token strict limit."
    },
    {
        "input": "text = 'word ' * 500",
        "output": "'ERROR: Payload too large'",
        "explanation": "The token count vastly exceeded 100 tokens, triggering your exact error string."
    }
]

HINTS = [
    "tiktoken is the official library OpenAI uses for token counting. Initialize it with get_encoding('cl100k_base').",
    "Don't just measure string length! You must call `.encode(text)` and measure the length of the resulting array.",
    "Use llm.bind(max_tokens=50) to strictly cap the API's generation length on the backend."
]

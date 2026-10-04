TITLE = "The Streamer — Real-Time UX"
DIFFICULTY = "easy"
DESCRIPTION = {
    "scenario": "Users are giving your app 1-star reviews because they have to stare at a blank loading screen for 15 seconds while the LLM generates a massive blog post. You need to implement real-time streaming to create a ChatGPT-like typing effect on the frontend.",
    "tasks": [
        "Complete the `generate_blog` function.",
        "Notice that the function signature returns an `AsyncGenerator[str, None]`.",
        "Use `llm.astream(prompt)` to asynchronously stream chunks from the OpenAI API.",
        "Use an `async for` loop to iterate over the chunks, and `yield` the `.content` of each chunk one by one."
    ]
}
MAX_POINTS = 25
THRESHOLD = 0.8
FORBIDDEN_EDITS = ["generate_blog"] 
ALLOWED_IMPORTS = ["langchain_core", "typing"]

EXAMPLES = []

HINTS = [
    "You cannot use `return` in a generator! You must use `yield`.",
    "Make sure to yield `chunk.content`, not the raw chunk object!"
]

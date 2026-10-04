TITLE = "The Conversationalist — Chat History"
DIFFICULTY = "easy"
DESCRIPTION = {
    "scenario": "You are building an AI Movie Recommendation Bot. A user types: 'I just watched Inception and absolutely loved the mind-bending plot.' In their second message, they simply type: 'Can you recommend another movie like it?' The LLM has absolutely no idea what 'it' refers to because LLMs are inherently stateless!",
    "tasks": [
        "Complete the `chat` function.",
        "The function receives a new `message` (str) and a `history` (a list of dictionaries).",
        "Use a `ChatPromptTemplate` with a `MessagesPlaceholder(variable_name=\"history\")`.",
        "Append the new incoming user message to the template.",
        "Create an LCEL chain (`prompt | llm`) and invoke it with the `history` and `message` variables.",
        "Return the raw string content of the AI's response."
    ]
}
MAX_POINTS = 25
THRESHOLD = 0.8
FORBIDDEN_EDITS = ["chat"] 
ALLOWED_IMPORTS = ["langchain_core"]

EXAMPLES = [
    {
        "input": "message = 'Can you recommend another movie like it?', history = [{'role': 'user', 'content': 'I loved Inception.'}]",
        "output": "'If you loved Inception, you should definitely check out Interstellar or The Matrix!'",
        "explanation": "Because the history was successfully passed in the chain, the LLM knew that 'it' referred to 'Inception'."
    }
]

HINTS = [
    "You do NOT need to write a for-loop. Use ChatPromptTemplate.from_messages().",
    "MessagesPlaceholder(variable_name='history') will dynamically inject your list of dictionaries and automatically coerce them into native LangChain Message objects."
]

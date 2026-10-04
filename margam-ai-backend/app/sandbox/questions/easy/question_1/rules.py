TITLE = "The Support Bot — Structured JSON Output"
DIFFICULTY = "easy"
MAX_POINTS = 25
THRESHOLD = 0.8
FORBIDDEN_EDITS = ["analyze_support_ticket"]
ALLOWED_IMPORTS = ["pydantic", "langchain_core", "llm_client", "typing"]

DESCRIPTION = {
    "scenario": "You are building an AI customer support triage bot for SwiftCart. When a customer sends an email, the LLM categorizes the email so it can be automatically routed to the right dashboard.",
    "tasks": [
        "Create a Pydantic schema named `SupportTicket` with the fields: `intent` (str), `urgency` (int), and `customer_sentiment` (str).",
        "Complete the `analyze_support_ticket` function.",
        "Create a `ChatPromptTemplate` instructing the AI on its role and injecting the user's `email_text`.",
        "Use the provided `llm` client and bind your schema using `.with_structured_output()`.",
        "Chain them together, invoke the chain, and return the parsed `SupportTicket` object."
    ]
}

EXAMPLES = [
    {
        "input": "email_text = 'Where is my package? It is 3 days late and I am furious!'",
        "output": '{"intent": "shipping", "urgency": 4, "customer_sentiment": "angry"}',
        "explanation": "The customer is asking about shipping, expressing extreme anger, and the delay warrants high urgency."
    }
]

HINTS = [
    "Make sure to use typing.Literal inside your Pydantic fields. This restricts the LLM from hallucinating output types.",
    "The .with_structured_output() method automatically binds your Pydantic schema to the underlying LLM's function-calling API."
]

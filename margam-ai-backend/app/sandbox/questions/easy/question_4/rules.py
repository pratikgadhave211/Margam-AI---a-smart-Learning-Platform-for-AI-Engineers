TITLE = "The Few-Shot Learner — Tone & Persona"
DIFFICULTY = "easy"
DESCRIPTION = {
    "scenario": "Your company wants a Slack bot that translates angry, unprofessional messages into polite, ultra-professional 'corporate-speak'. Since you are guiding tone and style rather than extracting data, `with_structured_output` won't work here. You must teach the LLM how to sound 'corporate' by providing a few examples in the prompt.",
    "tasks": [
        "Complete the `translate_message` function.",
        "Create an `example_prompt` using `PromptTemplate.from_template(\"Angry: {input}\\nCorporate: {output}\")`.",
        "Clean the `messy_examples` tuples into a list of dictionaries.",
        "Create a `FewShotPromptTemplate` using your cleaned examples list and your `example_prompt`.",
        "Set the prefix to `\"Translate the following angry messages into polite corporate communication.\"` and suffix to `\"Angry: {message}\\nCorporate:\"`.",
        "Chain the prompt to the `llm` and return the invoked string."
    ]
}
MAX_POINTS = 25
THRESHOLD = 0.8
FORBIDDEN_EDITS = ["translate_message"] 
ALLOWED_IMPORTS = ["langchain_core"]

EXAMPLES = [
    {
        "input": "message = 'This code is absolute garbage and Dave is an idiot for merging it.'",
        "output": "'I have some concerns regarding the recent code merge and would like to suggest a few improvements.'",
        "explanation": "The LLM adopts the exact polite tone and structure shown in the FewShotPromptTemplate examples."
    }
]

HINTS = [
    "A FewShotPromptTemplate strictly expects a list of dictionaries. You can use a Python list comprehension to clean the messy list of tuples: `cleaned = [{'input': t[0], 'output': t[1]} for t in messy_examples]`",
    "Don't forget to include `input_variables=['message']` in your FewShotPromptTemplate."
]

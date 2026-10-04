TEST_CASES = [
    {
        "input": {"text": "This is a very short text about artificial intelligence. Please summarize it."},
        "expected": "summary", 
        "weight": 1.0,
    },
    {
        "input": {"text": "word " * 150}, # 150 words guarantees > 100 tokens
        "expected": "error",
        "weight": 1.0,
    },
]

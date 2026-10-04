TEST_CASES = [
    {
        "input": {
            "message": "What is my favorite color?", 
            "history": [
                {"role": "user", "content": "Hi, my favorite color is blue!"},
                {"role": "ai", "content": "Nice to meet you! Blue is a great color."}
            ]
        },
        "expected": "blue",
        "weight": 1.0,
    },
    {
        "input": {
            "message": "How many dogs do I have?", 
            "history": [
                {"role": "user", "content": "I have 3 dogs named Max, Bella, and Charlie."},
                {"role": "ai", "content": "Wow, 3 dogs must be a lot of fun!"}
            ]
        },
        "expected": "3",
        "weight": 1.0,
    },
]

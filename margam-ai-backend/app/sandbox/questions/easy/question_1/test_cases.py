TEST_CASES = [
    {
        "input": "I ordered a laptop 3 weeks ago and it still hasn't arrived. This is unacceptable!",
        "expected": {"intent": "shipping", "urgency": 4, "customer_sentiment": "angry"},
        "weight": 1.0,
    },
    {
        "input": "Hi, I'd like a refund for order #12345. The product was damaged.",
        "expected": {"intent": "refund", "urgency": 3, "customer_sentiment": "neutral"},
        "weight": 1.0,
    },
    {
        "input": "My app keeps crashing when I try to checkout. Can someone help?",
        "expected": {"intent": "technical", "urgency": 3, "customer_sentiment": "neutral"},
        "weight": 1.0,
    },
]

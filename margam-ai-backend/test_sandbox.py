import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from app.sandbox.runner import evaluate_submission

async def main():
    # Run the sandbox evaluation, which now synchronously calls the LLM internally
    result = await evaluate_submission("app/sandbox/seed/test_ideal.py")
    
    import json
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

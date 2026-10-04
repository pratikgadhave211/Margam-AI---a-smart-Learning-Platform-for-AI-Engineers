import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv

load_dotenv()

import asyncio
import json
import os

from app.sandbox.injector import inject_user_code
from app.sandbox.runner import evaluate_submission
from app.submission.user_code import USER_CODE


async def run_pipeline():

    template_path = os.path.join("app", "sandbox", "templates", "rag_class_template.py")

    output_path = os.path.join("app", "sandbox", "sandbox_run_123.py")

    injected_file = inject_user_code(template_path, USER_CODE, output_path)

    result = await evaluate_submission(injected_file)

    print("\n" + "=" * 50)
    print("           SANDBOX EVALUATION REPORT           ")
    print("=" * 50 + "\n")

    print(f"Status        : {result.get('status')}")
    print(f"Final Score   : {result.get('final_score')}")
    print(f"Points Earned : {result.get('points_earned')} / {result.get('max_points')}\n")

    if result.get("warnings"):
        print("Warnings:")
        for warning in result["warnings"]:
            print(f"  - {warning}")
        print()

    print("Test Results:")
    for idx, test in enumerate(result.get("test_results", []), 1):
        print(f"  Test {idx}: Passed={test.get('passed')} | Score={test.get('avg_score'):.2f} | "
              f"Precision={test.get('precision'):.2f} | Recall={test.get('recall'):.2f} | F1={test.get('f1'):.2f}")
    print()

    print("AI Mentor Summary:")
    print(json.dumps(result.get("summary", {}), indent=2))
    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":

    asyncio.run(run_pipeline())

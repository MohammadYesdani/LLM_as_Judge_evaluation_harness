import json
import time
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

JUDGE_MODEL = "gemini-3.1-flash-lite"

# The judge's instructions. We ask for a clear verdict AND its reasoning.
JUDGE_TEMPLATE = """You are an impartial judge evaluating two answers to the same question.

Question: {question}

Answer A:
{answer_a}

Answer B:
{answer_b}

Decide which answer is better based on accuracy, completeness, and clarity.
Respond in exactly this format:

REASONING: <one or two sentences explaining your choice>
VERDICT: <write only "A" or "B">
"""

def judge_one(question, answer_a, answer_b):
    """Ask the judge to compare two answers. Returns (verdict, reasoning)."""
    prompt = JUDGE_TEMPLATE.format(
        question=question,
        answer_a=answer_a,
        answer_b=answer_b,
    )
    response = client.models.generate_content(
        model=JUDGE_MODEL,
        contents=prompt,
    )
    text = response.text

    # Pull the verdict and reasoning out of the response.
    verdict = ""
    reasoning = ""
    for line in text.splitlines():
        if line.strip().startswith("VERDICT:"):
            verdict = line.split("VERDICT:")[1].strip()
        if line.strip().startswith("REASONING:"):
            reasoning = line.split("REASONING:")[1].strip()

    return verdict, reasoning

# Load the answers we generated in Step 2.
with open("answers.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

results = []

for item in answers:
    print(f"[{item['id']+1}/{len(answers)}] judging: {item['question'][:45]}...")

    verdict, reasoning = judge_one(
        item["question"],
        item["answer_a"],
        item["answer_b"],
    )

    results.append({
        "id": item["id"],
        "question": item["question"],
        "judge_verdict": verdict,       # "A" or "B"
        "judge_reasoning": reasoning,
    })

    time.sleep(4)   # stay under the rate limit

with open("judge_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nDone. Saved {len(results)} judgments to judge_results.json")
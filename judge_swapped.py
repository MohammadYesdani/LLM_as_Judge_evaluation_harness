import json
import time
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

JUDGE_MODEL = "gemini-3.1-flash-lite"

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
    prompt = JUDGE_TEMPLATE.format(question=question, answer_a=answer_a, answer_b=answer_b)
    response = client.models.generate_content(model=JUDGE_MODEL, contents=prompt)
    text = response.text
    verdict = ""
    reasoning = ""
    for line in text.splitlines():
        if line.strip().startswith("VERDICT:"):
            verdict = line.split("VERDICT:")[1].strip()
        if line.strip().startswith("REASONING:"):
            reasoning = line.split("REASONING:")[1].strip()
    return verdict, reasoning

with open("answers.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

results = []

for item in answers:
    print(f"[{item['id']+1}/{len(answers)}] judging (swapped): {item['question'][:40]}...")

    # THE KEY DIFFERENCE: we swap the positions.
    # The weak answer (answer_b) goes into slot A.
    # The strong answer (answer_a) goes into slot B.
    verdict, reasoning = judge_one(
        item["question"],
        item["answer_b"],   # <-- weak answer now in position A
        item["answer_a"],   # <-- strong answer now in position B
    )

    results.append({
        "id": item["id"],
        "question": item["question"],
        "judge_verdict_swapped": verdict,   # "A" now means the WEAK answer
        "judge_reasoning": reasoning,
    })

    time.sleep(4)

with open("judge_results_swapped.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nDone. Saved {len(results)} swapped judgments.")
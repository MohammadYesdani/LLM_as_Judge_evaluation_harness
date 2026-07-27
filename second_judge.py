import json
import os
import time
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# A different model from your Flash-Lite judge = independent second opinion.
SECOND_JUDGE_MODEL = "gemini-3.5-flash"

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
    response = client.models.generate_content(model=SECOND_JUDGE_MODEL, contents=prompt)
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

# Resume support: load whatever we already saved.
out_path = "second_judge_results.json"
if os.path.exists(out_path):
    with open(out_path, "r", encoding="utf-8") as f:
        results = json.load(f)
else:
    results = []

done_ids = {str(r["id"]) for r in results}

for item in answers:
    if str(item["id"]) in done_ids:
        continue   # already judged this one on a previous run

    print(f"[{item['id']+1}/{len(answers)}] second judge: {item['question'][:40]}...")

    # Try up to 4 times, waiting longer each time, before giving up.
    verdict, reasoning = None, None
    for attempt in range(4):
        try:
            verdict, reasoning = judge_one(item["question"], item["answer_a"], item["answer_b"])
            break   # success, stop retrying
        except Exception as e:
            wait = 10 * (attempt + 1)   # 10s, 20s, 30s, 40s
            print(f"   error ({e}) — retrying in {wait}s (attempt {attempt+1}/4)")
            time.sleep(wait)

    if verdict is None:
        # Still failing after 4 tries — save and stop cleanly.
        print("\nStill failing after retries. Progress saved. Run again later.")
        break

    results.append({
        "id": item["id"],
        "question": item["question"],
        "second_verdict": verdict,
        "second_reasoning": reasoning,
    })

    # Save after EVERY call, so a crash never loses progress.
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    time.sleep(4)

print(f"\nHave {len(results)} of {len(answers)} second-judge verdicts saved.")
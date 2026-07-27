import json
import time
from google import genai
from prompts import PROMPTS   # pulls in your 40 questions
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# The two models we're comparing.
MODEL = "gemini-3.1-flash-lite"   # same model for both, higher daily limit

# We create a quality gap using instructions, not different models.
STRONG_INSTRUCTION = "Answer carefully and accurately. Think step by step and check your work before giving a clear, complete answer."
WEAK_INSTRUCTION = "Answer as quickly and briefly as possible. Give a short answer without showing any working."

def ask(instruction, question):
    """Send one question with a given style instruction, return the text answer."""
    response = client.models.generate_content(
        model=MODEL,
        contents=f"{instruction}\n\nQuestion: {question}",
    )
    return response.text

results = []

for i, question in enumerate(PROMPTS):
    print(f"[{i+1}/{len(PROMPTS)}] {question[:50]}...")

    answer_a = ask(STRONG_INSTRUCTION, question)
    time.sleep(4)          # pause so we don't hit the free-tier rate limit

    answer_b = ask(WEAK_INSTRUCTION, question)
    time.sleep(4)

    results.append({
        "id": i,
        "question": question,
        "answer_a": answer_a,
        "answer_b": answer_b,
    })

# Save everything to a file so we never have to re-run these calls.
with open("answers.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nDone. Saved {len(results)} answer pairs to answers.json")
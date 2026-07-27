import json

# Load the judge's verdicts and your human labels.
with open("judge_results.json", "r", encoding="utf-8") as f:
    judge_results = json.load(f)

with open("human_labels.json", "r", encoding="utf-8") as f:
    human_labels = json.load(f)

# Compare them, question by question.
agree = 0
disagree = 0
skipped = 0
disagreements = []   # remember which ones they differed on

for item in judge_results:
    item_id = str(item["id"])
    judge = item["judge_verdict"].strip().upper()   # "A" or "B"
    human = human_labels.get(item_id, "").strip().upper()

    # Skip anything we can't cleanly compare (blank verdict, or you marked TIE).
    if judge not in ("A", "B") or human not in ("A", "B"):
        skipped += 1
        continue

    if judge == human:
        agree += 1
    else:
        disagree += 1
        disagreements.append({
            "id": item["id"],
            "question": item["question"],
            "judge_said": judge,
            "you_said": human,
            "judge_reasoning": item["judge_reasoning"],
        })

compared = agree + disagree
agreement_rate = (agree / compared * 100) if compared else 0

print("=" * 60)
print("RESULTS: Judge vs Human")
print("=" * 60)
print(f"Total questions:        {len(judge_results)}")
print(f"Compared:               {compared}")
print(f"Skipped (tie/blank):    {skipped}")
print(f"Agreements:             {agree}")
print(f"Disagreements:          {disagree}")
print(f"AGREEMENT RATE:         {agreement_rate:.1f}%")
print("=" * 60)

if disagreements:
    print("\nWHERE THE JUDGE DISAGREED WITH YOU:")
    for d in disagreements:
        print(f"\n[id {d['id']}] {d['question']}")
        print(f"   You picked: {d['you_said']}   Judge picked: {d['judge_said']}")
        print(f"   Judge's reasoning: {d['judge_reasoning']}")
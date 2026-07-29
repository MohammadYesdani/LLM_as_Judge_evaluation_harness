import json

# Load the second judge's verdicts and your human labels.
with open("second_judge_results.json", "r", encoding="utf-8") as f:
    second_judge = json.load(f)

with open("human_labels.json", "r", encoding="utf-8") as f:
    human_labels = json.load(f)

agree = 0
disagree = 0
skipped = 0
disagreements = []

for item in second_judge:
    item_id = str(item["id"])
    judge = item["second_verdict"].strip().upper()      # "A" or "B"
    human = human_labels.get(item_id, "").strip().upper()

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
            "second_judge_said": judge,
            "you_said": human,
        })

compared = agree + disagree
agreement_rate = (agree / compared * 100) if compared else 0

print("=" * 60)
print("SECOND JUDGE vs MY HAND-LABELS (ground-truth validation)")
print("=" * 60)
print(f"Total second-judge verdicts: {len(second_judge)}")
print(f"Compared:                    {compared}")
print(f"Skipped (tie/blank):         {skipped}")
print(f"Agreements:                  {agree}")
print(f"Disagreements:               {disagree}")
print(f"AGREEMENT RATE:              {agreement_rate:.1f}%")
print("=" * 60)

if disagreements:
    print("\nWHERE THE SECOND JUDGE DISAGREED WITH ME:")
    for d in disagreements:
        print(f"  [id {d['id']}] {d['question'][:55]}")
        print(f"     I said {d['you_said']}, second judge said {d['second_judge_said']}")
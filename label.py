import json
import os

with open("answers.json", "r", encoding="utf-8") as f:
    answers = json.load(f)

labels_path = "human_labels.json"
if os.path.exists(labels_path):
    with open(labels_path, "r", encoding="utf-8") as f:
        labels = json.load(f)
else:
    labels = {}

print("=" * 70)
print("HAND-LABELING: read both answers and pick the better one.")
print("Type A, B, or tie, then Enter. Type quit to stop and save.")
print("=" * 70)

for item in answers:
    item_id = str(item["id"])

    if item_id in labels:
        continue

    print("\n" + "=" * 70)
    print(f"QUESTION {item['id']+1} of {len(answers)}")
    print("=" * 70)
    print(f"\nQUESTION: {item['question']}\n")
    print("-" * 70)
    print("ANSWER A:")
    print(item["answer_a"])
    print("-" * 70)
    print("ANSWER B:")
    print(item["answer_b"])
    print("-" * 70)

    choice = input("\nWhich is better? (A / B / tie / quit): ").strip().lower()

    if choice == "quit":
        print("Stopping. Progress saved.")
        break

    if choice not in ("a", "b", "tie"):
        print("Not understood, skipping. Run again to revisit.")
        continue

    labels[item_id] = choice.upper()

    with open(labels_path, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(labels)} labels to human_labels.json")
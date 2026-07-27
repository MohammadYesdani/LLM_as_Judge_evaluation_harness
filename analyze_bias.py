import json

with open("judge_results.json", "r", encoding="utf-8") as f:
    original = json.load(f)

with open("judge_results_swapped.json", "r", encoding="utf-8") as f:
    swapped = json.load(f)

# Turn the swapped list into a lookup by id for easy pairing.
swapped_by_id = {str(item["id"]): item for item in swapped}

consistent_strong = 0
consistent_weak = 0
flipped = 0
skipped = 0
flip_details = []

for item in original:
    item_id = str(item["id"])
    if item_id not in swapped_by_id:
        skipped += 1
        continue

    orig_verdict = item["judge_verdict"].strip().upper()
    swap_verdict = swapped_by_id[item_id]["judge_verdict_swapped"].strip().upper()

    if orig_verdict not in ("A", "B") or swap_verdict not in ("A", "B"):
        skipped += 1
        continue

    # In the ORIGINAL run, A = strong.
    orig_picked_strong = (orig_verdict == "A")
    # In the SWAPPED run, B = strong.
    swap_picked_strong = (swap_verdict == "B")

    if orig_picked_strong and swap_picked_strong:
        consistent_strong += 1
    elif (not orig_picked_strong) and (not swap_picked_strong):
        consistent_weak += 1
    else:
        flipped += 1
        flip_details.append({
            "id": item["id"],
            "question": item["question"],
            "original_verdict": orig_verdict,
            "swapped_verdict": swap_verdict,
        })

total = consistent_strong + consistent_weak + flipped
flip_rate = (flipped / total * 100) if total else 0
position_bias_note = ""

print("=" * 60)
print("POSITION-BIAS ANALYSIS")
print("=" * 60)
print(f"Comparable questions:       {total}")
print(f"Skipped (blank verdicts):   {skipped}")
print(f"Consistent (picked strong): {consistent_strong}")
print(f"Consistent (picked weak):   {consistent_weak}")
print(f"FLIPPED (position bias):    {flipped}")
print(f"FLIP RATE:                  {flip_rate:.1f}%")
print("=" * 60)

# A simple read on which position the judge favors overall.
# Count how often it picked position A across both runs.
a_picks = sum(1 for i in original if i["judge_verdict"].strip().upper() == "A")
a_picks_swapped = sum(1 for i in swapped if i["judge_verdict_swapped"].strip().upper() == "A")
total_a = a_picks + a_picks_swapped
print(f"\nHow often judge picked position A (both runs): {total_a} out of {len(original)+len(swapped)}")
print("If this is well above half, the judge leans toward whatever is in slot A.")

if flip_details:
    print("\nQUESTIONS WHERE THE VERDICT FLIPPED ON SWAP:")
    for d in flip_details:
        print(f"  [id {d['id']}] {d['question'][:55]}")
        print(f"     original said {d['original_verdict']}, swapped said {d['swapped_verdict']}")
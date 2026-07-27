# LLM-as-Judge Reliability Harness

**Can you trust one AI to grade another AI's answers? This project measures it — and finds a bias that a naive first metric completely hides.**

Modern ML teams increasingly use one language model to evaluate the outputs of another ("LLM-as-judge") because hand-grading thousands of responses doesn't scale. But that shortcut is only as good as the judge is trustworthy. This harness measures that trustworthiness on a controlled set of question-answer pairs, validates the ground truth against an independent model, and runs a swap experiment to detect **position bias** — the judge preferring an answer based on *where* it appears rather than *how good it is*.

## Key findings

- **A naive agreement metric said the judge was "perfect" (100%).** The judge agreed with my own hand-labels on all comparable questions. This looked like a great result — and was a warning sign, not a success.
- **A controlled swap experiment exposed real position bias.** Re-running every judgment with the two answers swapped, the verdict flipped on **10% of questions**, and the judge preferred the first-shown answer on **55%** of all judgments.
- **The bias concentrated entirely in subjective tasks.** All four flipped verdicts were open-ended writing prompts (a poem, a haiku, a product description, a summary). On questions with an objectively correct answer (math, logic), the judge was consistent and position-independent. Position bias appeared precisely where quality is ambiguous and there is no factual anchor.
- **Independent validation of the ground truth:** a second, different model was used as an independent labeler to check my own hand-labels. `[Second-judge agreement with my labels: TO BE ADDED once all 40 verdicts are collected.]`

**The takeaway:** the 100% agreement was partly an artifact of the experiment's setup — the stronger answer always sat in the position the judge happened to favor. Only a controlled swap test revealed the truth. This mirrors how model evaluation is actually done in practice: a flattering metric is a reason to dig deeper, not to stop.

## How it works

The pipeline is deliberately split into independent stages so that expensive API calls are never repeated and every stage's output is saved to disk.

1. **Generate answers** (`generate_answers.py`) — one model answers 40 varied questions (factual, math, reasoning, and open-ended writing) in two styles: a careful "strong" style and a terse "weak" style, creating a controlled quality gap. Output: `answers.json`.
2. **Judge** (`judge.py`) — a separate model reads each question with both answers and picks the better one, with reasoning, in a strict parseable format. Output: `judge_results.json`.
3. **Hand-label** (`label.py`) — I label all 40 comparisons myself, blind to the judge's verdicts, to build an uncontaminated ground truth. Output: `human_labels.json`.
4. **Agreement analysis** (`analyze.py`) — compares the judge against my labels and lists every disagreement with the judge's reasoning.
5. **Swap experiment** (`judge_swapped.py`) — re-judges every pair with answer positions reversed. Output: `judge_results_swapped.json`.
6. **Position-bias analysis** (`analyze_bias.py`) — combines both runs to compute the flip rate and directional position preference.
7. **Independent validation** (`second_judge.py`) — a different model independently judges all 40, as a second opinion on the ground truth. Includes resume support and retry-with-backoff to survive free-tier rate limits and transient server errors. Output: `second_judge_results.json`.

## Methodology notes (and honest limitations)

- **Labels were made blind** to the judge's verdicts, so ground truth wasn't biased toward agreeing with the judge.
- **The quality gap was created by instruction, not by two different models** (both answers come from the same underlying model with different prompts), because the free API tier restricts access to stronger models. This keeps costs at zero.
- **The independent second labeler is a different model, not a stronger one** (the free tier no longer offers Pro-class models). It therefore validates *consistency* of the labels, not their absolute *correctness*. This is stated plainly rather than overclaimed.
- **Sample size is 40 questions.** Findings are directional and illustrative, not statistically definitive — appropriate for a focused portfolio project rather than a research claim.

## Tech stack

- Python
- Google Gemini API (free tier) via the `google-genai` library
- Models: `gemini-3.1-flash-lite` (answer generation + primary judge), `gemini-3.5-flash` (independent second labeler)

## Setup

```bash
# 1. Install the dependency
pip install google-genai

# 2. Add your free Gemini API key
#    Get one at https://aistudio.google.com  (no credit card required)
#    Paste it into the client = genai.Client(api_key="...") line in each script
```

## Running the pipeline

Run the scripts in order:

```bash
python generate_answers.py     # -> answers.json
python judge.py                # -> judge_results.json
python label.py                # -> human_labels.json (interactive)
python analyze.py              # prints agreement + disagreements
python judge_swapped.py        # -> judge_results_swapped.json
python analyze_bias.py         # prints the position-bias results
python second_judge.py         # -> second_judge_results.json (resumable)
```

`second_judge.py` is safe to re-run: it skips already-saved verdicts and continues where it stopped, which matters because the free tier caps daily requests.

## What I learned

- How LLM-as-judge evaluation works, and why raw agreement is a misleading metric on its own.
- How to design a controlled experiment (position swapping) to isolate a specific bias.
- Practical engineering for unreliable external APIs: checkpointing results to disk, resume-on-restart, and retry-with-exponential-backoff for transient (503) and rate-limit (429) errors.
- The value of distrusting a result that looks too clean.

## Repository structure

```
prompts.py                    # the 40 test questions
generate_answers.py           # stage 1
judge.py                      # stage 2
label.py                      # stage 3 (interactive)
analyze.py                    # stage 4
judge_swapped.py              # stage 5
analyze_bias.py               # stage 6
second_judge.py               # stage 7 (resumable, with retry/backoff)
answers.json                  # generated data
judge_results.json            # generated data
human_labels.json             # generated data
judge_results_swapped.json    # generated data
second_judge_results.json     # generated data
```
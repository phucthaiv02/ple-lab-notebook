---
name: ple-writeup
description: Use when drafting, revising or checking the Kaggle Writeup and final submission for the PLE competition, built from the ple-lab-notebook evidence and the official rubric.
---

# PLE Kaggle Writeup and submission

Reply to the user in the language they write in. Write the writeup itself in English.

Drafts live in `ple-lab-notebook/writeup/` (private). Final figures and their scripts are copied into `ple-harness/writeup/` on `main`.

## 0. Requirements come only from the official pages

Before drafting, and again before submitting, re-read the competition's Overview (Submission Requirements, Evaluation, Timeline), the Rules, and host or Kaggle-staff replies in Discussion. Use Claude in Chrome or WebFetch. Update the checklist below if anything changed, and tell the user what changed.

Past hackathon writeups (for example the Gemma 4 Developer Agent paper track) may be skimmed **for style and structure ideas only**. Never take requirements, limits or rubric items from them.

## 1. Rubric (as published; verify it is unchanged)

| Criterion | Pts | Evidence source in notebook |
|---|---|---|
| Insight & Failure Analysis | 25 | `failures.csv`, `ablations.md`, `ideas_failed.md` |
| Engineering Reasoning | 25 | `casebook/` |
| Cross-Model Generalizability | 15 | `models.md`, `runs.csv` (≥2 models, ideally across families; which changes help all vs one; accuracy and token cost) |
| Efficiency & Scaling | 20 | `runs.csv` budget sweep (calls, tokens, runtime, or parallel attempts); plateau; headroom estimate |
| Clarity & Visuals | 15 | ≤2,000 words, headline finding near the top, written for an ML researcher with no civil/mechanical/electrical background, 3 required figures |

Stage 1 is a qualification gate (Top 100 go to Stage 2), and ties in Stage 2 break on the Stage 1 score. Write it well even though prizes are decided by Stage 2.

## 2. Hard requirements checklist

- [ ] Writeup ≤ 2,000 words; check with a word count of the final text.
- [ ] Covers all 5 criteria.
- [ ] **Media Gallery cover image.**
- [ ] **3 figures:**
  - (1) architecture diagram
  - (2) score-vs-cost plot
  - (3) failure breakdown on the 29 dev tasks
- [ ] **Commit SHA:** the 40-character SHA of `ple-harness` `main` (`git rev-parse HEAD`) is at the **top** of the writeup, and https://github.com/phucthaiv02/ple-harness is under **Project Links**.
- [ ] **That commit contains:**
  - `submission.yaml` with `model_api` set to one of the 8 `google-cloud/<id>` models
  - `serve.py` / `harness.py`
  - an Apache-2.0 or MIT `LICENSE`
  - unpacked `artifacts/` produced by `eval/run.py`
- [ ] **`artifacts/` limits:** ≤ 512 MiB, ≤ 10,000 files, no Git LFS, no symlinks.
- [ ] **Repo size:** the repo including history is ≤ 1 GiB. Squash it if `artifacts/` was committed many times.
- [ ] **Checks pass on that commit (run from `ple/`):**
  - `uv run python -m kit check ../ple-harness` ends with `ready to submit`
  - `uv run python -m kit artifacts ../ple-harness` passes
  - optional regrade: `uv run python eval/run.py --artifacts ../ple-harness`
- [ ] **Disclosed in the writeup:**
  - which model generated `artifacts/`, if it was not the declared model (a `manifest.json` warning about this is OK per Kaggle staff)
  - the local judge model, if it was not the official one
  - the target Stage 2 model
- [ ] Harness code supports the target model's API format (tested on a few tasks).
- [ ] **Public-repo safety:** the repo contains no notebook files, dev task files, run folders or keys.
- [ ] **Private repo:** the `ple-submission` GitHub App is installed on `ple-harness` only, and there is a plan to make it public at close.
- [ ] One submission per team. Clicking Submit is the final step; un-submitted drafts are not judged. The writeup can be un-submitted, edited and re-submitted until the deadline.
- [ ] **Deadline:** submitted before the deadline on the Timeline (2027-01-05 23:59 UTC when this skill was written; re-check).

## 3. Suggested structure and word budget (~2,000)

1. **Header:** commit SHA line, repo link, then a 2–3 sentence TL;DR with the headline finding and dev score/cost (~100 words).
2. **System:** the architecture figure. Describe the loop, tools, verification and context strategy in plain words (~250 words).
3. **What fails and what fixed it:** the failure-breakdown figure, an ablation table (A→B, cost delta), and 1–2 ideas that failed (~500 words).
4. **Engineering reasoning case study:** one task walked through against a licensed engineer's workflow. Define every engineering term in one clause (~450 words).
5. **Cross-model results:** a table with rows = models and columns = dev score, checks/rubric split, tokens, cost. Say which changes generalize (~250 words).
6. **Efficiency and scaling:** the score-vs-cost figure, where it plateaus, and estimated headroom (~300 words).
7. **Reproducibility and disclosures:** models, judge, how `artifacts/` were produced, LLM-assistance note (~100 words).

## 4. Writing rules

- Every number must trace to a row in `runs.csv`, `task_scores.csv` or `ablations.md`. Before finalizing, list each number with its source row and fix any without one.
- State noise honestly: LLM-judged scores shift a few points between calls. Report the number of runs and the spread when the claim is small.
- Prefer concrete failure examples, such as "read grid line C as D on sheet M-201", over generic ones.
- Use the figure scripts in `ple-lab-notebook/figures/`. Commit the final PNGs/SVGs and scripts under `ple-harness/writeup/`, not inside `artifacts/` or any harness folder.
- **LLM assistance:** the Rules do not forbid it, but the entry must be the team's original work, and deception can lead to disqualification. Use LLMs for editing, structure and clarity. Never use them to invent results, failures or analysis. Recommend a one-line disclosure.
- Do not include hidden test content. Keep dev-task excerpts short.

## 5. Figures

- **Architecture:** boxes for the evaluator, serve container (harness stages), model endpoint and task container (files + MCP), with arrows for the protocol messages and the verification loop.
- **Score vs. cost:** x = mean cost per task in USD (or total tokens if prices are unknown; label which), y = dev mean score. One series per model, points = budget settings. Annotate the plateau.
- **Failure breakdown:** a stacked bar of failure categories over the 29 dev tasks, grouped by discipline or grading type, for the final configuration. Optionally show baseline vs. final.

## 6. Final pass

1. Re-read the official pages for changes.
2. Run the checklist.
3. Get the word count.
4. Confirm the SHA in the writeup equals the pushed commit (`git -C ../ple-harness ls-remote origin HEAD`).
5. Have the user click Submit themselves. Do not submit on their behalf.

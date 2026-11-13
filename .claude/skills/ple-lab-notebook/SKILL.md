---
name: ple-lab-notebook
description: Use after every PLE dev run, ablation, model comparison or notable failure, to record the evidence the Kaggle writeup needs: runs, scores, tokens, costs, failures, ablations, case studies.
---

# PLE lab notebook (evidence for the writeup)

The Stage 1 writeup is scored on evidence: real failures, controlled ablations ("added X, score went from A to B"), cross-model tables, score vs. cost, and a walkthrough of a concrete task. None of this can be reconstructed at the end. **Log as you go**, and never write a number into the writeup that has no row here.

Reply to the user in the language they write in.

## Where

The notebook is the private repo **github.com/phucthaiv02/ple-lab-notebook**, cloned beside the other two repos:

```
workspace/
  ple/                official repo clone (runs/ live here)
  ple-harness/        the entry (public at close): never put notebook files there
  ple-lab-notebook/   this notebook (always private)
```

Why it is separate:
- run data and transcripts contain dev-task content, which is for competition use only;
- the harness must never be able to read it;
- the build bundles every tracked file of the entry.

Only final figures and their plotting scripts get copied to `ple-harness/writeup/`.

```
ple-lab-notebook/
  log_run.py          appends a run to runs.csv and task_scores.csv
  runs.csv            one row per eval run
  task_scores.csv     one row per (run, task)
  ablations.md        hypothesis -> change -> A vs B -> verdict
  failures.csv        categorized failures with evidence paths
  casebook/           2-4 detailed trajectory case studies (markdown)
  ideas_failed.md     things tried that did not help, and why
  models.md           cross-model setup: provider, endpoint, context, effort, vision support
  decisions.md        setup and provenance: judge, artifact model, rule conflicts, LLM-assistance note
  prices.md           price per 1M tokens per model, with the source URL and the date checked
  figures/            plotting scripts + outputs (architecture, score-vs-cost, failure breakdown)
  archive/<run>/      copied results.json + cited transcripts (never whole run folders)
  writeup/            writeup drafts (see the ple-writeup skill)
```

## After every run (mandatory)

1. **Record provenance.** Note:
   - the `ple-harness` commit and tag (`git -C ../ple-harness rev-parse HEAD`, plus `dirty` if there are uncommitted changes)
   - the branch
   - the `model_api` actually called, how it was served (proxy, API provider, Ollama or vLLM), and its reasoning effort
   - for DeepSeek, whether the run was in peak or off-peak hours
   - the judge model and endpoint
   - the task subset and the machine
2. **Extract scores and tokens** with `log_run.py`, run from the `ple/` folder:
   ```bash
   uv run --with pyyaml python ../ple-lab-notebook/log_run.py runs/<run> ../ple-lab-notebook "<variant>" "<served_via>" "<notes incl. SHA>"
   ```
   - Top-level fields in `results.json`: `submission`, `model`, `score`, `complete`, `unmeasured`, `judge_model`, `date`.
   - Each entry in `tasks[]` has `id`, `score`, `reward`, `measured`, `status`, `kind`, `seconds`, `tokens{input,cache,output}` and `trial`.
3. **Estimate cost** only from prices recorded in `prices.md`: the official provider pricing pages, or for sponsored models the cost links on the Kaggle Evaluation page. Never invent prices; if one is unknown, leave cost blank and mark it TODO. Fill `cost_usd` in the new `runs.csv` row.
4. **Triage each task below 1.0.** Open `trial/agent/<name>.txt` (protocol transcript), `trajectory.json`, `serve.log`, and `verifier/test-stdout.txt` or `grade.json`. Add one row to `failures.csv`.
5. **If the run was an ablation,** append an entry to `ablations.md`.
6. **Archive before deleting.** Copy `results.json` and any transcript cited in the casebook into `archive/<run>/`, then commit and push the notebook. Never commit whole run folders.

## failures.csv columns and taxonomy

Columns: `run, task, domain, grading, score, category, sub_cause, evidence_path, one_line, engineer_would_have`.

Start with these categories and keep them stable so the failure-breakdown figure stays comparable across runs:

- `misread_drawing`: wrong callout, dimension, grid or layer
- `wrong_code_clause`: wrong standard, table, or edition
- `unit_error`: unit or conversion mistake
- `hard_constraint_violated`: G=0, so the item is capped at 0.4
- `objective_not_optimized`: compliant but costly, so O' is low
- `missing_or_misnamed_deliverable`: wrong path or format
- `rubric_section_missing`: the judge wanted X
- `hallucinated_input`: used a value that is not in the project files
- `stopped_early_or_timeout`
- `tool_or_mcp_failure`
- `context_overflow`
- `harness_crash_or_protocol`
- `model_api_error_400`
- `other`

Add a category only when a new failure clearly fits none of these, and record why in `decisions.md`.

## ablations.md entry template

```
## A<n>: <short name>   (date)
- Hypothesis:
- Change: <tag/SHA before> -> <tag/SHA after> (one change only; branch exp/<idea>)
- Model(s) / judge:
- Tasks: <subset or all 29>; same subset for A and B
- Result: A=<run id, score> -> B=<run id, score>; tokens/cost A -> B; per-grading-type deltas
- Noise note: LLM-judged scores vary a few points between calls; repeat or use the checks-only subset before claiming small gains
- Verdict: kept (merged to main) / reverted / inconclusive
- Helps which models? (fill after cross-model run)
```

Failed ideas go in `ideas_failed.md` too. The rubric explicitly rewards reporting them.

## casebook/ (for "Engineering Reasoning", 25 pts)

For 2–4 dev tasks (aim for at least one pass and one fail, in different disciplines), write:

1. The task in plain words for an ML reader.
2. The agent's trajectory as numbered key steps, with transcript line references.
3. How a licensed engineer would approach it. Mark what you are unsure of as an assumption to verify, and check public references.
4. Where the agent's reasoning held up, where it took shortcuts, and which domain skill decided pass or fail: reading CAD or PDF drawings, checking code tables, or running solvers.

Keep excerpts from task files short (dev data is for competition use only). Never record hidden test task content.

## Cross-model and efficiency data

- Run the same harness commit on at least 2 models, ideally from different families. A local or personal-API model counts. Record each in `models.md`.
- For score vs. cost, sweep one budget knob, such as max turns, reasoning effort, verifier rounds or parallel attempts, and log each point as a run. Mark where accuracy plateaus.

## Weekly check (remind the user)

Compare `runs.csv` against the writeup needs:

- an architecture description that is up to date
- at least 3 ablations with A→B numbers
- at least 2 models compared
- at least 4 budget points for the score-vs-cost curve
- a failure breakdown covering all 29 tasks
- at least 2 casebook entries
- decisions logged: which model generated `artifacts/`, judge used, target `google-cloud/<id>`

Report gaps to the user while there is still time to fill them before 2027-01-05.

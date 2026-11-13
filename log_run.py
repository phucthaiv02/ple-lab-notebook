"""Append one PLE eval run to the lab notebook.

Run from the official `ple/` repo root (it reads eval/dev_set.yaml):

    uv run --with pyyaml python ../ple-lab-notebook/log_run.py runs/<run> ../ple-lab-notebook \
        "<variant>" "<served_via>" "<notes incl. ple-harness SHA/tag>"

Appends per-task rows to task_scores.csv and one summary row to runs.csv.
Fill cost_usd in runs.csv afterwards from prices.md.
"""

import csv
import json
import pathlib
import sys

import yaml

GRADING_TYPES = ("checks", "checks-judge", "rubric")


def append(path, header, rows):
  new = not path.exists()
  with path.open("a", newline="") as f:
    w = csv.writer(f)
    if new:
      w.writerow(header)
    w.writerows(rows)


def main():
  if len(sys.argv) < 3:
    sys.exit(__doc__)
  run, nb = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
  variant, served, notes = (sys.argv[3:] + ["", "", ""])[:3]
  r = json.loads((run / "results.json").read_text())
  meta = {t["id"]: t for t in yaml.safe_load(open("eval/dev_set.yaml"))["tasks"]}

  rows, tot = [], {"input": 0, "cache": 0, "output": 0}
  for t in r["tasks"]:
    tok = t.get("tokens") or {}
    for k in tot:
      tot[k] += tok.get(k, 0)
    m = meta.get(t["id"], {})
    rows.append([
        run.name, t["id"], m.get("domain", ""), m.get("grading", ""),
        t["score"], t["measured"], t["kind"], t["status"], t.get("seconds"),
        tok.get("input", 0), tok.get("cache", 0), tok.get("output", 0),
    ])
  append(nb / "task_scores.csv",
         ["run", "task", "domain", "grading", "score", "measured", "kind", "status",
          "seconds", "in_tok", "cache_tok", "out_tok"], rows)

  by = {}
  for x in rows:
    by.setdefault(x[3], []).append(x[4])
  means = [round(sum(by[g]) / len(by[g]), 4) if by.get(g) else "" for g in GRADING_TYPES]
  append(nb / "runs.csv",
         ["run", "date", "model", "judge", "variant", "served_via", "n_tasks", "mean",
          "checks", "checks_judge", "rubric", "complete", "in_tok", "cache_tok", "out_tok",
          "harness_sec", "cost_usd", "notes"],
         [[run.name, r["date"], r["model"], r["judge_model"], variant, served, len(rows),
           r["score"], *means, r["complete"], tot["input"], tot["cache"], tot["output"],
           round(sum(x[8] or 0 for x in rows)), "", notes]])
  print(f"logged {run.name}: mean={r['score']} n={len(rows)} unmeasured={r['unmeasured']}")


if __name__ == "__main__":
  main()

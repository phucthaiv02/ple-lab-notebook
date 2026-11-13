# ple-lab-notebook (PRIVATE)

Evidence log and writeup drafts for the Kaggle PLE competition entry
(https://github.com/phucthaiv02/ple-harness). This repo must stay **private**: it holds dev-task excerpts and
transcripts, and dev data is for competition use only.

## Workspace

```
workspace/
  ple/                official repo (google-research/ple): runs/ are written here
  ple-harness/        the entry (public at close)
  ple-lab-notebook/   this repo
```

## Skills in this repo

- `ple-lab-notebook` (canonical copy; mirrored in `ple-harness`): what to log after every run, and how.
- `ple-writeup`: drafting the Kaggle Writeup and the final submission checklist.

## Usage

- Log a run from the `ple/` folder: `uv run --with pyyaml python ../ple-lab-notebook/log_run.py runs/<run> ../ple-lab-notebook "<variant>" "<served_via>" "<notes incl. SHA>"`
- **Never commit whole run folders.** Copy only `results.json` and cited transcripts into `archive/<run>/`.
- **Never record hidden test task content.**
- Every number in the writeup must trace to a row here.

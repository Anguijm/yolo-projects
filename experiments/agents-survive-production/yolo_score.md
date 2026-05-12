# Yolo-loop score against the survival checklist

Scored 2026-05-11. Subject: `.github/workflows/tick_tock.yml` and the
scripts it invokes (`scripts/process_experiments.py`,
`fetch_youtube_rss.py`, `.harness/scripts/council.py`).

Scoring leans toward FAIL/PARTIAL where ambiguity exists.

| # | Criterion                       | Score    | Evidence |
|---|---------------------------------|----------|----------|
| 1 | Silent-failure detection        | PARTIAL  | `scripts/process_experiments.py:159-173` now logs `json.JSONDecodeError` with raw-doc snippets after PR #8; `stop_reason` logged at line 112-114. But there's no shape gate on the cards array itself — a syntactically-valid but semantically-empty `[]` from the LLM would still commit silently. `experiments/deterministic-script-verification/` proposes the shape gate. |
| 2 | Drift detection                 | FAIL     | Model ID `claude-sonnet-4-6` is hard-coded at `scripts/process_experiments.py:94` but no assertion that the model still exists. RSS feed schemas not validated (we trust YouTube's RSS format). No input-distribution canary (e.g., "if the prompt produces 0 cards 3 days running, alert"). |
| 3 | Cost ceilings                   | PARTIAL  | `max_tokens=16000` set per call (`scripts/process_experiments.py:101`); supadata daily quota indirectly caps transcript spend. No daily Anthropic-budget alert. |
| 4 | Observability — logs            | PARTIAL  | `phase4_run.json` records `last_run_utc`, `new_videos_found`, `new_experiments_added`, `backlog_count`. `.harness/yolo_log.json` records build history. But raw model responses are not persisted, so silent-truncation events can't be reconstructed after the fact. |
| 5 | Observability — metrics         | FAIL     | No time-series store. `phase4_run.json` overwrites each run, so trend analysis requires git log spelunking. |
| 6 | Alerting                        | FAIL     | GitHub Actions default email-on-failure is the only notification path, and the May 2026 silent-truncation incident demonstrated that "workflow green + 0 outputs" doesn't fire it. |
| 7 | Idempotency                     | PASS     | `scripts/process_experiments.py:175-181` dedupes by `card.id`; `fetch_youtube_rss.py` dedupes videos by `video_id`. Re-running produces no duplicate records. |
| 8 | Rollback path                   | PASS     | Every cron commit is reversible via `git revert`. No side effects outside git (no external API mutations). |
| 9 | Dependency pinning              | PARTIAL  | GHA actions pinned to SHA in `ci.yml` (e.g., `actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5`). But Python packages in `.harness/scripts/requirements.txt` are not pinned to exact versions (verified by reading the file), and `process_experiments.py` floats `anthropic` SDK version. |
| 10 | Secret rotation                | FAIL     | `SUPADATA_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN` all exist; no runbook for rotating any of them, no rotation has been performed in this repo's history. |
| 11 | Runbook coverage               | FAIL     | The card-generator incident response (PR #8) is documented in commit messages but not in a runbook file. There's no `runbooks/` directory. CLAUDE.md captures conventions but not failure-response procedures. |
| 12 | Test coverage of agent logic   | FAIL     | No `tests/` directory at repo root. The CI `validate` job runs `pytest` conditionally but pytest is not installed in the workflow (verified at `.github/workflows/ci.yml:74-80`). `experiments/deterministic-script-verification/` proposes the first shape tests. |
| 13 | Security — secret scanning     | PASS     | gitleaks runs on every PR and push to main as the first CI job (`.github/workflows/ci.yml:19-30`), with `.gitleaks.toml` config. |
| 14 | Security — input validation    | PARTIAL  | `fetch_youtube_rss.py` filters `/shorts/` URLs and `video_id` extracted via regex. Transcript fetches go through supadata's API with size caps. But the LLM prompt assembles transcript text without schema validation — a maliciously-crafted YouTube description could be in the input. |

## Tally

| Score    | Count |
|----------|-------|
| PASS     | 3     |
| PARTIAL  | 5     |
| FAIL     | 6     |

**3 of 14 PASS** is the headline. Six outright failures.

The strongest area is hygiene (idempotency, rollback, secret scanning).
The weakest is operational maturity (alerting, runbooks, metrics, tests,
secret rotation, drift detection) — exactly the cluster the MLOps talk
warned would kill prototypes in production.

## What "production" means here

This score is *for the tick_tock cron specifically*. It's not a verdict
on the yolo-projects repo overall, the council pipeline's design, or
the individual project subdirectories. Those are different systems with
different risk profiles. The cron pipeline is the one running unattended
on a schedule with commit authority on `main`, so it's the one that
needs to survive production.

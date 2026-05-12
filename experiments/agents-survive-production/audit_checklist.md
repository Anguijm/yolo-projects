# Audit checklist — agents in production

14 criteria, drawn from the MLOps "agents survive production" talk and
extended with criteria specific to autonomous cron pipelines. Each
criterion has a rubric for PASS / PARTIAL / FAIL so scores are defensible.

## 1. Silent-failure detection

**Rubric.** Does the agent fail loudly when its output is wrong-shaped,
empty when it shouldn't be, or otherwise diverges from expected?

- **PASS** — shape checks, count thresholds, or schema validation gate
  output before commit.
- **PARTIAL** — some checks exist but coverage is incomplete.
- **FAIL** — broad `except Exception: pass` patterns; no shape gates.

## 2. Drift detection

**Rubric.** When upstream dependencies, model versions, or input
distributions change, does the agent notice?

- **PASS** — pinned dependencies, model-version assertion in code,
  input-shape canary.
- **PARTIAL** — pinned dependencies but no input-distribution monitoring.
- **FAIL** — floating dependency versions, no canary.

## 3. Cost ceilings

**Rubric.** Does each LLM call have a per-call max_tokens / max_cost
bound? Is there a total-budget alert?

- **PASS** — every API call has explicit max_tokens; daily budget alert
  fires before overrun.
- **PARTIAL** — max_tokens set per call but no daily ceiling.
- **FAIL** — unbounded calls or relying on provider's default cap.

## 4. Observability — logs

**Rubric.** Can you reconstruct what the agent did on a given day from
logs alone?

- **PASS** — structured logs, raw model outputs persisted, every cron
  run produces an auditable artifact.
- **PARTIAL** — workflow logs exist but raw API responses are not
  persisted.
- **FAIL** — only GitHub Actions stdout, ephemeral, no JSON artifact.

## 5. Observability — metrics

**Rubric.** Are there numeric time-series for "things that should hold
roughly steady"? (run count, items processed, parse-success rate.)

- **PASS** — metrics emitted to a time-series store + dashboard.
- **PARTIAL** — metrics computed per-run but only in workflow logs.
- **FAIL** — no quantitative tracking.

## 6. Alerting

**Rubric.** When something goes wrong, does a human get notified within
24h without manually checking?

- **PASS** — Slack/email/PagerDuty integration triggers on failure
  criteria.
- **PARTIAL** — GitHub Actions email-on-failure only (which can
  reasonably be ignored).
- **FAIL** — no notification path; user discovers issues by manual
  spot-check.

## 7. Idempotency

**Rubric.** Can the same input run twice produce the same effect (or no
duplicate effect)?

- **PASS** — dedup by content hash or stable ID; re-running a workflow
  is safe.
- **PARTIAL** — dedup exists for the primary path but not for retries.
- **FAIL** — re-running produces duplicate records.

## 8. Rollback path

**Rubric.** If the agent commits something wrong, how do you revert?

- **PASS** — every commit is a discrete artifact reversible via `git
  revert`; no irreversible side effects (deletions, external API mutations).
- **PARTIAL** — git is the system of record but some mutations are
  outside git (e.g., issues posted).
- **FAIL** — mutations to shared state with no rollback.

## 9. Dependency pinning

**Rubric.** Are model IDs, action SHAs, and package versions pinned?

- **PASS** — model IDs hard-coded, GHA actions pinned to SHA, package
  versions in a lockfile.
- **PARTIAL** — actions pinned to SHA, but Python packages float.
- **FAIL** — `@v1`-style action pins, floating package versions.

## 10. Secret rotation

**Rubric.** Is there a documented procedure for rotating each secret,
and has it been tested in the last 12 months?

- **PASS** — runbook exists, rotation drill happened recently.
- **PARTIAL** — runbook exists but never tested.
- **FAIL** — no runbook, would have to invent the procedure during an
  incident.

## 11. Runbook coverage

**Rubric.** For each known failure mode, is there a written procedure to
diagnose and remediate?

- **PASS** — runbook covers each top-3 failure mode.
- **PARTIAL** — some runbooks exist for past incidents but no systematic
  coverage.
- **FAIL** — no runbooks; tribal knowledge only.

## 12. Test coverage of agent logic

**Rubric.** Is the agent's logic (parsing, dispatch, decision rules)
exercised by tests that run in CI?

- **PASS** — unit tests for parsing + integration tests with stubbed
  LLM, both in CI.
- **PARTIAL** — some unit tests exist locally but don't run in CI.
- **FAIL** — no automated tests.

## 13. Security — secret scanning

**Rubric.** Is the repo continuously scanned for committed secrets?

- **PASS** — gitleaks or equivalent runs on every PR and on push to
  main, blocks merge on detection.
- **PARTIAL** — periodic scans but not blocking.
- **FAIL** — no secret scanning.

## 14. Security — input validation

**Rubric.** Are untrusted inputs (RSS feeds, transcript APIs, etc.)
validated before being passed to the LLM or written to artifacts?

- **PASS** — every external input has explicit schema validation and
  size caps.
- **PARTIAL** — some validation but inconsistent.
- **FAIL** — external inputs flow into prompts unvalidated.

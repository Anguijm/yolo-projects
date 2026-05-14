# Top 3 gaps — proposed follow-on tick cards

Each gap below is reformulated as a tick-ready card. Pick any to promote
at the next backlog triage. Ordered by impact-per-effort.

---

## Gap 1: Output-shape alerting (criterion #1 + #6, PARTIAL + FAIL)

**Effort:** low

**Hypothesis.** If the cron writes `phase4_run.json` with `new_experiments_added=0` two runs in a row, then a workflow step opens a GitHub issue titled "Phase 4 ingestion produced 0 cards" — because the May 2026 silent-truncation incident proved a zero-output streak is the canonical alarm shape and a GitHub issue is the lowest-friction notification that integrates with the existing repo.

**What this gives us.** The single-incident pattern from PR #8 — silent zero-output runs for days — becomes a Day-1 alarm. The fix is small (a `jq` step at the end of `tick_tock.yml` plus a `gh issue create` call) and uses no new infrastructure.

**Out of scope.** General-purpose alerting infrastructure. Issue-creation
is a stop-gap; if we ever have ≥3 alert types, graduate to Slack or a
dedicated channel.

**Proposed deliverables:**
- New step in `.github/workflows/tick_tock.yml` that reads
  `phase4_run.json`, counts consecutive zero-output runs by looking
  at the last N commits, and opens an issue when the streak hits 2.
- Issue template at `.github/ISSUE_TEMPLATE/phase4-zero-output.md` with
  the diagnosis runbook inline.
- README addition under `.harness/` explaining the alarm shape.

**Why this beats fancier observability.** The criterion #5 "metrics +
dashboard" gap is real, but the marginal value of metrics is much
lower than the marginal value of one specific alarm wired up. Build the
alarm first; build metrics when we have a second alarm to share
infrastructure with.

---

## Gap 2: Runbook directory + card-generator incident writeup (criterion #11, FAIL)

**Effort:** low

**Hypothesis.** If we create `runbooks/` with the May 2026 card-generator silent-truncation incident written up as the seed entry, then future incidents have a template and an obvious place to land — because the value of runbooks is in their cumulative density, and one runbook is the cheap way to start a discipline.

**What this gives us.** A standing convention. The PR #8 commit message
has all the diagnosis steps already; copying them into a structured
runbook costs an hour and provides a template for the next 20 incidents.

**Out of scope.** Full runbook coverage. The first runbook seeds the
practice; the next incident produces the second; coverage grows
organically.

**Proposed deliverables:**
- `runbooks/README.md` — what a runbook is in this repo, the structure
  (Symptom → Diagnosis → Remediation → Prevention).
- `runbooks/2026-05-card-generator-zero-output.md` — the PR #8 incident
  in the structured format.
- `CLAUDE.md` update — point at `runbooks/` from the existing "responding
  to status" section.

---

## Gap 3: Pin Python deps + add anthropic SDK version assertion (criterion #2 + #9, FAIL + PARTIAL)

**Effort:** medium

**Hypothesis.** If `.harness/scripts/requirements.txt` pins every package to an exact version AND `scripts/process_experiments.py` asserts the `anthropic` SDK version at startup, then a silent SDK behavior change (response shape, retry semantics, deprecated model) fails loud at startup instead of producing subtle wrong output mid-run.

**What this gives us.** Closes the drift-detection criterion #2 partially
and the dependency-pinning criterion #9 fully. The SDK assertion
specifically catches the "model alias renamed and our hard-coded
`claude-sonnet-4-6` 404s" failure mode.

**Out of scope.** Renovate/Dependabot integration (would be a third
ticket); a TUI for managing pin updates; anything beyond exact-pinning
+ a single version assertion line.

**Proposed deliverables:**
- `.harness/scripts/requirements.txt` — every package pinned to exact
  version (`==X.Y.Z`).
- `scripts/process_experiments.py` — `assert
  anthropic.__version__.startswith("0.")` (or whatever the canonical
  major is) at module load with a clear error message.
- `.github/workflows/ci.yml` — verify the pin file parses by running
  `pip install -r .harness/scripts/requirements.txt --dry-run` (validate
  job already has setup-python; add 3 lines).
- CLAUDE.md note: how to bump pins safely (run model-upgrade-audit
  before changing the SDK).

---

## Gaps deliberately NOT in the top 3

- **Criterion #12 (test coverage).** Important but high-cost; the
  pydantic-agents-production-optimisation tick already proposes the
  starting infrastructure (Pydantic schemas), and the
  deterministic-script-verification tick proposes the shape-test
  pattern. Bundle a real test suite once both ship.
- **Criterion #5 (metrics + dashboard).** Marginal value low until we
  have multiple alarms. Wait for Gap 1 + a second alarm.
- **Criterion #10 (secret rotation).** Important but no current incident
  pressure; the secrets are user-owned. Defer until at least one
  rotation drill is on the calendar.

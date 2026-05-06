# Council Rules

Canonical reference for `council.py` behavior — how the 7-angle review works, what an OBJECT does, and which auto-downgrade rules can convert an OBJECT into an APPROVE-advisory.

This file is the single source of truth for human users and AI agents working with the council. The module docstring at the top of `council.py` summarizes the same rules; this file contains the full rationale, history, and edge cases.

## How a gate runs

Each project gate (`plan` → `implementation` → `tests` → `outcome`) invokes `council.py` with the deliverable. All seven angles run **in parallel** via the configured backend (Gemini by default, Claude Haiku as fallback):

| Angle | Lens |
|---|---|
| `bugs` | Correctness, edge cases, runtime errors |
| `security` | Injection, ReDoS, path traversal, untrusted input |
| `ui` | Accessibility, affordances, mobile usability |
| `guide` | Discoverability, in-app docs, agent-readability |
| `usefulness` | Real-user value, frequency of need |
| `cool` | Project identity, signature moves, differentiation |
| `lessons` | Documented patterns from `learnings.md` |

Each angle returns a JSON `Verdict` with `verdict` (`APPROVE`/`OBJECT`), `severity` (`low`/`medium`/`high`/`critical`/`advisory`), `reason`, `required_fix`, and `evidence`.

**LESSONS has veto power**: a LESSONS OBJECT halts the build immediately (subject to the precondition rule below). Other angles' OBJECTs trigger a fix-and-retry loop; if the same angle objects with conflicting fixes after two attempts, the build escalates and writes `<project>/COUNCIL_ESCALATION.md`.

## Auto-downgrade enforcement rules

Four enforcement passes run after each gate. Each one converts a matching OBJECT verdict to APPROVE-advisory and prefixes the `reason` with `[AUTO-DOWNGRADED: …]` so the trigger is self-evident in cron logs and JSON artifacts.

### 1. Parse-failure retry

**Where:** `call_angle` (council.py)

**Trigger:** the model returns unparseable JSON (e.g. malformed code fence, trailing prose).

**Action:** retry once with stricter JSON instructions before falling back to a phantom OBJECT (`Verdict.parse_failed=True` so the detection is structural rather than string-based).

**Why:** transient JSON-mode glitches were the root cause of `infra-yolo-evals` escalation 4 and the PLAN-gate BUGS phantom in `fix-council-enforcement` escalation 5.

### 2. LESSONS VETO precondition_evidence

**Where:** `enforce_lessons_precondition` (council.py)

**Trigger:** a LESSONS verdict has `verdict=OBJECT` and `veto=True`, but the `evidence` field lacks both:
- a `file.ext:NN` citation (matched by `EVIDENCE_CITATION_RE`), AND
- the literal string `precondition_evidence`.

**Action:** auto-downgrade to APPROVE-advisory; the build proceeds.

**Why:** four false-positive LESSONS vetoes between 2026-04-21 and 2026-04-22 each cited a learnings.md rule but provided no concrete evidence the rule's *precondition* was met for this project. Requiring grep-verifiable evidence keeps the veto power intact while filtering the cargo-culted invocations.

### 3. Goalpost-move auto-downgrade

**Where:** `check_goalpost_moves` (council.py)

**Trigger:** a new OBJECT from angle X on project P has `keyword_overlap >= 0.35` with any prior reason for the same `(project, angle)` tuple, computed across all gates (not just the current one).

**Action:** auto-downgrade with the prior overlap score in the prefix.

**Threshold rationale:** empirical recalibration — same-concern/opposite-framing pairs in real escalations land at 0.35-0.43 using count-shared-tokens / max-token-count, while genuinely distinct concerns land at 0.00. The 0.35 boundary cleanly separates observed cases. The original learnings.md prose suggested 0.6 as a guess; 0.35 is the data-derived value.

**Why:** angles that get overruled on a feature have historically rephrased the same objection at later gates ("PLAN: this is unsanitized AI output" → "IMPLEMENTATION: the generated code wasn't sanitized"). The cross-gate keyword check stops that loop.

### 4. BUGS hallucination auto-downgrade

**Where:** `detect_bugs_hallucination` (council.py)

**Trigger:** a BUGS verdict satisfies *all* of:
- `angle == "bugs"` AND `verdict == "OBJECT"`
- `reason` contains `undefined`, `undeclared`, `not defined`, `does not exist`, or `missing` (case-insensitive)
- backtick-quoted identifiers of 3-80 chars appear in the prose **before** each claim keyword (the proximity filter prevents matching scope hints like "not defined IN `getFullState`" or replacement suggestions like "use `setDraftStatus`")
- at least one cited file (`file.ext:NN` from `evidence`, or fall-back project files) actually contains a definition for one of the cited symbols

**Definition-pattern check** (after a cited-line window check):

| Language | Patterns |
|---|---|
| `.html` / `.js` / `.ts` | `function NAME`, `(?:const|let|var) NAME =`, line-anchored method shorthand `NAME(args) {` |
| `.py` | `def NAME` / `class NAME`, line-anchored `NAME =` (module/class-level assignment) |
| Other | skipped (return False) |

The method-shorthand pattern is line-anchored and requires `{` after `)` so call sites (`foo()`, `obj.foo()`) don't match — only definitions like `foo() {` do.

**Action:** auto-downgrade to APPROVE-advisory with `[AUTO-DOWNGRADED: hallucinated symbol claim, symbols present in cited files] …` prefix.

**Why:** naval-scribe Letter Status Tracker rounds 7-9 and Template Letter Library rounds 1-3 each had three identical hallucinated BUGS objections claiming functions/properties were undefined while grep showed them defined at the very lines the council cited. Both tocks ultimately shipped via retroactive 4-gate stamps; preventing the hallucination at the enforcement layer saves those stamp cycles.

## Configuration constants (council.py)

| Constant | Value | Where used |
|---|---|---|
| `GOALPOST_OVERLAP_THRESHOLD` | `0.35` | rule 3 |
| `EVIDENCE_CITATION_RE` | `r"\w+\.\w+:\d+"` | rule 2 |
| `_HALLUCINATION_CLAIM_RE` | `r"\b(undefined\|undeclared\|not\s{1,4}defined\|does\s{1,4}not\s{1,4}exist\|missing)\b"` | rule 4 |
| `_SYMBOL_FROM_FIX_RE` | `r"\`([a-zA-Z_][a-zA-Z0-9_]{2,80})\`"` | rule 4 |
| `_FILE_REF_RE` | `r"([\w\-/.]{1,200}\.\w{1,12}):(\d{1,8})(?:[-,]\d{1,8})?"` | rule 4 |
| `MAX_FILE_BYTES` (implicit) | 2,000,000 | rule 4 size cap |

All quantifiers are explicitly bounded — worst-case backtracking is linear in input length even on adversarial 2 MB inputs.

## When a downgrade fires

- `[council] BUGS auto-downgraded (hallucinated symbol) — verified definition exists in cited files` → rule 4
- `[council] {angle} auto-downgraded (goalpost move, {score:.2f} overlap)` → rule 3
- `[council] LESSONS auto-downgraded (precondition_evidence missing)` → rule 2
- `[council] {angle}: parse-failure retry` → rule 1 (logged on retry; success or failure)

The downgraded verdict still appears in the `council_<gate>.json` artifact with the `[AUTO-DOWNGRADED: …]` prefix on `reason` for full traceability.

## Authoring new rules

1. Add the helper to `council.py` next to the existing enforcement functions.
2. Wire it into `main()` after the existing rule pass that's most adjacent.
3. Add unit tests + at least one historical fixture replay to `experiments/fix-council-enforcement/test_enforcement.py`.
4. Document the rule here, in the `council.py` module docstring, in `learnings.md` under "Council enforcement rules are now LIVE in code", and in `CLAUDE.md`.
5. Ship through the same 4-gate cron pipeline.

## See also

- **`council.py`** — the orchestrator (module docstring is the API summary)
- **`council/angles/*.md`** — per-angle prompts
- **`learnings.md`** "Council enforcement rules are now LIVE in code" — full per-rule history
- **`CLAUDE.md`** "Council enforcement rules (auto-downgrade behavior)" — quick reference for AI agents
- **`experiments/fix-council-enforcement/`** — tick that shipped rules 1-3
- **`experiments/fix-council-bugs-hallucination/`** — tick that shipped rule 4

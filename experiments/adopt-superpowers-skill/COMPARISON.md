# Superpowers vs. this repo's council gates — a one-page comparison

**TL;DR verdict:** The two systems enforce *plan-first* the same way and reach
the same goal (no slop ships) by opposite routes. Superpowers is **soft,
in-context, test-FIRST discipline** delivered as composable Markdown skills;
our council is **hard(ish), out-of-process, multi-angle adversarial review**
delivered as a Python gate runner. They are complementary, not redundant. The
one genuinely missing idea worth grafting in is **test-FIRST** (write the
failing check before the code), which our pipeline does *not* enforce — it runs
tests as a post-build pre-filter. Recommended as a follow-up tick, not changed
here.

---

## What Superpowers enforces

Superpowers (the Claude Code plugin by obra / Jesse Vincent) packages a software
engineering *discipline* as a library of reusable **skills** — Markdown files
with YAML frontmatter that Claude loads on demand. The methodology it encodes:

1. **Brainstorm before planning.** Don't jump to a plan; widen the option space
   first, interrogate assumptions, then converge.
2. **Write the plan to a file.** The plan is an artifact, reviewable and
   referenceable — not ephemeral chat.
3. **Test-Driven Development — RED / GREEN / REFACTOR.** Write a *failing* test
   first, make it pass with the minimum code, then refactor. Tests precede
   implementation, not follow it.
4. **Dispatch subagents** for isolated/parallel work and to keep the main
   context clean.
5. **Verify before claiming done.** Run the thing; observe the behavior; don't
   assert success from the diff alone.
6. **Skills are composable + self-authoring.** A "how to write a skill" meta-skill
   means the system extends itself in its own format.

Enforcement mechanism: **prompting discipline loaded as skills.** It works
*inside* the model's context — strong when the skills are loaded, but ultimately
advisory (the model can still deviate). It is designed for **interactive** Claude
Code sessions.

## What this repo's council enforces

This repo wraps every autonomous build in **4 sequential gates**, each running
**7 advocate angles** in parallel via an out-of-process Python runner
(`.harness/scripts/council.py` → Gemini):

1. **PLAN gate** — a *structured* `plan.md` (Goal / Scope / Approach / File
   Layout / Function Map / Security / UI / Guide / Edge Cases / Test Strategy) is
   reviewed by all 7 angles before any code is written.
2. **IMPLEMENTATION gate** — the built artifact is reviewed against the plan.
3. **PRE-FILTER (mechanical)** — `test_project.py`, `eval_bugs.py`,
   `security_scan.py` must pass. This is where tests run.
4. **TESTS gate** — council reviews the test results + test plan.
5. **OUTCOME gate** — final ship check (`verify_build.py`, dashboard, docs).

Plus pipeline-level enforcement: **lessons-veto**, and four **auto-downgrade
passes** (parse-failure retry, LESSONS-veto precondition-evidence,
goalpost-move, BUGS-hallucination). Currently **advisory** under the drain
directive — gates run and log but never block.

Enforcement mechanism: **out-of-process adversarial review.** Verdicts come from
a *separate* process with its own persona prompts, so they are independent of the
builder's context. Designed for **headless cron** (`claude -p` in GitHub
Actions), fully non-interactive.

## Point-by-point mapping

| Dimension | Superpowers | This repo's council |
|---|---|---|
| Plan-first | ✅ write plan to file | ✅ structured `plan.md` + PLAN gate |
| Brainstorm-before-plan | ✅ explicit step | ⚠️ partial (tick brainstorm queue, not per-build) |
| Test discipline | ✅ **test-FIRST** (RED/GREEN/REFACTOR) | ⚠️ test-**after** (post-build pre-filter) |
| Review | self + subagent dispatch | **7 independent advocate angles** |
| Review independence | in-context (same model) | **out-of-process** (separate runner) |
| Enforcement strength | advisory (prompt discipline) | gate runner (now advisory in drain) |
| Self-extension | ✅ skills author skills | ✅ `skills/50-skill-creator.md` (adopted) |
| Verify-before-done | ✅ run it, observe | ✅ OUTCOME gate + `verify_build.py` |
| Runtime model | interactive Claude Code | **headless cron** |
| Delivery format | Markdown skills + YAML frontmatter | Python runner + persona `.md` files |

## Verdict — what to graft, what to keep, what to skip

**What overlaps (already covered, no action):** plan-first, plan-as-artifact,
verify-before-done, and self-authoring skills. Our PLAN gate + `skills/` system
already match Superpowers here. The `adopt-skill-creator` tick already gave us
the self-authoring half.

**What Superpowers adds that we lack — worth grafting:**
- **Test-FIRST.** Our pipeline runs `test_project.py` *after* the build as a
  pre-filter. Superpowers writes the failing assertion *first*. For our HTML
  YOLO tools test-first is awkward (no unit harness), but for **infrastructure
  ticks that touch `council.py` or other Python**, a "write the failing test in
  the same commit, demonstrate RED→GREEN" rule would be a real upgrade. → File
  as a follow-up infra tick; do NOT change the pipeline in this doc-only tick.
- **Brainstorm-before-plan** as an explicit per-build step (we have it only at
  the tick-queue level, not inside a single build).

**What we have that Superpowers lacks — keep:**
- **Out-of-process, multi-angle adversarial review.** Seven advocates in a
  separate process catch what an in-context self-review cannot — this is our
  core differentiator and the reason the council survives even as advisory.
- **Headless-cron operation.** Superpowers is interactive-first; our whole
  pipeline is built to run unattended in CI. We cannot adopt the plugin as-is.
- **Auto-downgrade enforcement + lessons-veto** — codified anti-goalpost and
  anti-hallucination rules with no equivalent in Superpowers.

**What to skip:** installing the plugin itself. It is interactive and cannot run
in `claude -p` headless cron (see README honest-scope). We adopt the
*methodology*, not the binary.

**Net recommendation:** No pipeline change in this tick. Open one follow-up infra
tick — *"test-first for Python-touching infra ticks"* — to graft the single
highest-value idea (RED→GREEN in the same commit) into the IMPLEMENTATION/TESTS
gates. Everything else Superpowers offers, the council already covers.

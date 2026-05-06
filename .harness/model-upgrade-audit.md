# Model Upgrade Audit Checklist

Run this audit BEFORE switching to a new Claude model version. The goal is to strip workarounds that patched old model weaknesses — stronger models don't need them and old hacks confuse them.

## When to Run
- New Claude model family release (e.g. 4.x → 5.x)
- New model tier available for cron (e.g. sonnet → opus)
- After any model behavioral change notice from Anthropic

## Layer 1: System Prompts (Cron + Session)

**Files to audit:**
- Hourly cron prompt (RemoteTrigger `trig_0111YcE8ZJBhX2xkBKfGP8qd`)
- Phase 4 cron prompt (RemoteTrigger `trig_01ABkrVvExqfkAQMKTNSjXmS`)
- `program.md`
- `~/.claude/CLAUDE.md`

**Check for:**
- [ ] Overly prescriptive step-by-step instructions that the new model can infer
- [ ] Explicit "DO NOT" lists that address old model failure modes (does the new model still fail this way?)
- [ ] Redundant examples/formatting guidance the new model handles natively
- [ ] Hardcoded tool call syntax that may have changed
- [ ] Token-heavy context that could be compressed without quality loss

**Action:** Remove dead guardrails. Test by running 3 builds on new model WITHOUT removed rules — if quality holds, the rules were cruft.

## Layer 2: Retrieval (What the Agent Reads)

**Files to audit:**
- `learnings.md` — are old learnings still relevant?
- `design.md` — does the new model follow design systems better natively?
- `eval_bugs.json` — are any patterns now caught by the model itself?
- `session_state.json` structure — any fields the new model handles differently?

**Check for:**
- [ ] Learnings about model-specific quirks (e.g. "Gemini does X wrong") — retest
- [ ] Bug patterns in eval_bugs.json that the new model no longer produces
- [ ] Retrieval order assumptions — does the new model need the same priming?

**Action:** Retest 5 eval_bugs patterns. If the new model avoids them natively, mark as "model-resolved" but keep in suite for regression.

## Layer 3: Verification (Testing + Council)

**Files to audit:**
- `test_project.py` — any workarounds for model-generated code patterns?
- `eval_bugs.py` — patterns specific to old model output style?
- Council review prompts — do they need recalibration for new model quality?

**Check for:**
- [ ] Test brace checker workarounds (// in strings) — does new model avoid this?
- [ ] Council review prompts tuned for old model quality level — raise the bar?
- [ ] False positive rates in eval_bugs.py — rerun `--all` and compare

**Action:** Run eval_bugs.py --all before and after upgrade. Compare match counts. Patterns with 0 matches on new model can be flagged.

## Layer 4: Orchestration (How Agents Coordinate)

**Files to audit:**
- Cron tick/tock alternation logic
- Flagship roadmap structure
- session_state.json update flow
- Agent spawning patterns (worktree isolation, parallel builds)

**Check for:**
- [ ] Serialization workarounds the new model doesn't need (e.g. explicit "verify it flipped")
- [ ] Agent coordination hacks that stronger models handle implicitly
- [ ] Context window assumptions — does the new model have a larger window?
- [ ] Tool calling changes — any new MCP capabilities to adopt?

**Action:** Run one full tick-tock cycle on new model with current prompts. Note friction points. Simplify after.

## Layer 5: MCP Spec Changes

**Check before every upgrade:**
- [ ] Review Anthropic MCP changelog for breaking changes or new capabilities
- [ ] Check if new tool types are available (streaming, multi-modal, etc.)
- [ ] Verify Gemini MCP connector still works with new spec version
- [ ] Check for new auth patterns or connector requirements
- [ ] Review https://claude.ai/settings/connectors for any connector updates needed

**Action:** If spec changed, update tool calls in cron prompts. If new capabilities available, evaluate for adoption.

## Post-Audit

1. Create a git branch `model-upgrade/<version>`
2. Apply all changes
3. Run 3 tick builds + 1 tock on new model
4. Compare council scores against last 3 builds on old model
5. If scores hold or improve: merge and update cron
6. If scores drop: identify which removed guardrail was load-bearing, restore it

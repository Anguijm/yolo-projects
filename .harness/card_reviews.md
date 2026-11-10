# Card reviews

One line per card: date reviewed | card id | verdict | project it bears on | why.
Verdicts: **propose** (worth John's time; told him), **note** (useful idea, small, fold into existing work when
touching that project), **pass** (noise or already covered). Rule: CLAUDE.md "Operating mode".

## 2026-10-19 (first review: backlog cards ingested 2026-10-13 to 2026-10-18)

- 2026-10-19 | aie-2026-10-15-rag-table-csv-chunking | propose | pdf-to-csv | tables to CSV with row/column context is the v0.8 "table section", and record-text.jsonl is already meant for his gen.ai.mil RAG (retrieval-augmented generation) use
- 2026-10-19 | aie-2026-10-15-rag-agentic-retrieval-zoom-levels | propose | pdf-to-csv | chunk/section/document levels for record-text.jsonl: the tool already knows form, field and page boundaries, so it can emit all three
- 2026-10-19 | dc-2026-10-18-dwarfstar-deepseek-strix-halo | propose | MS-S1 local LLM (tools/serve_llm.sh, editor-train) | the MS-S1 is a Strix Halo; a faster local engine helps every local model job. Heavy: ops check-in first
- 2026-10-19 | dc-2026-10-16-specialized-inference-engine-per-gpu-model | note | MS-S1 local LLM | same benchmark as DwarfStar; run together if that goes ahead
- 2026-10-19 | dc-2026-10-18-terminal-bench-mini-token-efficiency | note | MS-S1 local LLM | a yardstick for the same benchmark
- 2026-10-19 | pa-2026-10-15-ai-image-to-3d-print-local | pass | mini-forge | mini-forge already runs prompt to Trellis/Hunyuan/Pixal3D to watertight STL locally
- 2026-10-19 | aie-2026-10-13-artifact-verified-agent-returns | note | all sessions | already the standing "verify before presenting" rule; worth applying to subagent reports
- 2026-10-19 | aie-2026-10-13-cold-persona-adversarial-review | note | pdf-to-csv, flagships | already used (cold second review, A/B design contest on 2026-10-19)
- 2026-10-19 | eh-2026-10-15-external-judge-for-model-output | note | all | same idea as cold review
- 2026-10-19 | nh-2026-10-15-roast-room-multi-persona-decision-council | pass | | the gauntlet-loop skill and the council already cover it
- 2026-10-19 | mk-2026-10-17-audit-claude-codex-config-logs | pass | ops | ~/bin/session-digest already does this
- 2026-10-19 | mk-2026-10-17-unified-agents-md-hierarchy | pass | ops | CLAUDE.md hierarchy already nests machine > project
- 2026-10-19 | nb-2026-10-18-agent-permission-boundaries | pass | ops | permissions and hooks (forbidden-commands, heavy-work check-in) already layered
- 2026-10-19 | aie-2026-10-15-agent-infrastructure-controls-lethal-trifecta | note | polymarket, squishybot | sessions that read untrusted web content and can act outward; worth a one-off audit if either grows new powers
- 2026-10-19 | ail-2026-10-15-rea-five-use-cases | pass | | REA not installed; the security scans already run on yolo builds
- 2026-10-19 | aie-2026-10-15-mcp-gateway-with-pii-blocking-and-context-opt | pass | | no MCP (Model Context Protocol) fleet that needs a gateway
- 2026-10-19 | az-2026-10-15-kv-cache-agents-lmcache | pass | | vLLM-specific; the MS-S1 runs llama.cpp and Vulkan engines
- 2026-10-19 | az-2026-10-16-rtx-spark-laptop-120b-local-inference | pass | | hardware news; the laptop is an RTX 3070 8 GB
- 2026-10-19 | lc-2026-10-16-agent-harness-explainer | pass | | descriptive
- 2026-10-19 | lc-2026-10-16-continual-learning-sft-rl-tradeoff | note | editor-train | only if the editor training is revisited
- 2026-10-19 | cm-2026-10-16-immutable-mission-md-factory-context | pass | | "durable rules are his" already covers it
- 2026-10-19 | cm-2026-10-16-software-factory-human-in-staging | pass | | the PR-and-review flow already is this
- 2026-10-19 | cm-2026-10-16-token-efficient-model-routing-per-node | pass | | daily_cards already routes to sonnet
- 2026-10-19 | aie-2026-10-16-dependency-graph-preloaded-into-agent-session | pass | | repos are small
- 2026-10-19 | aie-2026-10-16-linux-kernel-trust-hierarchy-for-agents | pass | | no large agent fleet
- 2026-10-19 | aie-2026-10-16-highest-loop-loopcraft-abstraction | pass | | descriptive
- 2026-10-19 | ls-2026-10-16-world-action-model-visual-chain-of-thought | pass | | research
- 2026-10-19 | eh-2026-10-16-neural-network-interpretability-clean-hypothes | pass | | research
- 2026-10-19 | nh-2026-10-16-agent-environment-quality | pass | | general advice
- 2026-10-19 | nh-2026-10-16-unknown-unknowns-communication-skill | pass | | the intent.md interview already does this
- 2026-10-19 | do-2026-10-16-open-source-tagline-positioning | pass | |
- 2026-10-19 | do-2026-10-16-headless-api-first-no-dashboard | pass | |
- 2026-10-19 | do-2026-10-15-isolated-sandbox-per-agent | pass | |
- 2026-10-19 | do-2026-10-15-agent-feedback-tool-to-founder | pass | |
- 2026-10-19 | mlops-2026-10-15-domain-expert-agent-authoring | pass | | PDF to CSV's typed-names template is already this for one domain
- 2026-10-19 | mlops-2026-10-15-webmcp-agent-safe-actions | pass | |
- 2026-10-19 | aie-2026-10-15-ceiling-test-for-prompt-optimization | pass | |
- 2026-10-19 | aie-2026-10-15-accessibility-skill-reduces-agent-cost | pass | |
- 2026-10-19 | aie-2026-10-15-ai-automation-due-diligence-checks | pass | |
- 2026-10-19 | aie-2026-10-15-agent-trust-autonomy-scorecard | pass | |
- 2026-10-19 | aie-2026-10-15-gnn-graph-fraud-detection | pass | |
- 2026-10-19 | aie-2026-10-15-ai-engineer-nyc-day3 | pass | |
- 2026-10-19 | aie-2026-10-15-median-novelty-above-median | pass | |
- 2026-10-19 | nb-2026-10-15-narrow-superintelligence-skill-framing | pass | |
- 2026-10-19 | idd-2026-10-15-pi-durable-proactive-agents | pass | |
- 2026-10-19 | ls-2026-10-15-leash-bio-dell-ml-pipeline | pass | |

## 2026-10-20 (John: "2 - both things in a sensible sequence")
- 2026-10-20 | aie-2026-10-15-rag-table-csv-chunking + aie-2026-10-15-rag-agentic-retrieval-zoom-levels | built (zoom levels) | pdf-to-csv | v0.7.1 record-chunks.jsonl, PR #40; tables wait for v0.8 table sections
- 2026-10-20 | dc-2026-10-18-dwarfstar-deepseek-strix-halo | does not fit | MS-S1 | Q2 is a 340.6 GiB download, 151.8 GiB main weights > 128 GB; DwarfStar needs ROCm, not installed. Substitute plan: experiments/local-engine-bench/plan.md (ops approved schedule; waiting on John)

## To do (parked, not dropped)
- (done: un-parked the same day, John "ok for the model test") Local engine benchmark: experiments/local-engine-bench/plan.md.
- Local engine benchmark GPU runs: ops said WAIT on 2026-10-21 (the 22:00-03:45 window went to editor training); waiting for ops to name the first free night.
- 2026-10-22: ops relayed John's approval to run right after writer v2 training finishes today, on ops' GO. run.sh and chat_bench.py ready in experiments/local-engine-bench/; both models on disk, no downloads.
- 2026-10-22: benchmark RAN on ops GO, 08:56-09:11 JST, exit 0. Verdict: no switch, the new build reads long prompts faster (+38% at 16k on the ptt model) but generates at the same speed. experiments/local-engine-bench/results.md.

## 2026-10-22 (PRs #45 and #47)
- 2026-10-22 | nh-2026-10-19-claude-code-deterministic-jobs | pass | brain vault | scripts on cron already do this; Trigger.dev would add a paid outside service for no gain
- 2026-10-22 | idd-2026-10-19-cheap-gate-vault-capture | maybe | brain vault | hash dedupe plus a cheap classifier before verification; worth it only if the laptop's capture step has no dedupe yet (unchecked, laptop side)
- 2026-10-22 | idd-2026-10-19-local-classifier-strix-halo | fold in | MS-S1 / ptt | a small-model latency row could ride on the engine benchmark later; not added tonight, the approved scope is fixed
- 2026-10-22 | az-2026-10-20-local-pii-redaction-gate | pass | ptt | dictation is already local; John ruled out privacy hoops for his own data (2026-10-19)
- 2026-10-22 | pl-2026-10-18-architecture-review-gate-for-agents | pass | | no method, only a caution

## 2026-10-22 catch-up (found by the BAR.md critic: seven backlog cards had no line)
- 2026-10-22 | aie-2026-10-15-mcp-gateway-with-pii-blocking-and-context-optimizer | pass | | an enterprise gateway; one operator, and no privacy hoops for his own data (2026-10-19)
- 2026-10-22 | eh-2026-10-16-neural-network-interpretability-clean-hypothesis | pass | | a research framing, no project use
- 2026-10-22 | pl-2026-10-21-pr-comprehension-quiz-gate | pass | | a quiz gate puts work on John; he does not review PRs line by line
- 2026-10-22 | ail-2026-10-21-independent-cli-reviewer-and-altitude-prompts | folded in | yolo | the independent reviewer is now the fresh-critic step in BAR.md section 5
- 2026-10-22 | nb-2026-10-20-agent-memory-hygiene-audit | pass | MS-S1 | ops already runs preflight, memguard and job-guard; a Mac-focused video
- 2026-10-22 | do-2026-10-20-local-inference-sandboxing-strix-halo | maybe, ops-gated | ptt / MS-S1 | MXFP4 serving reported at 72 t/s on a larger model; our 2026-10-22 bench gives the ptt 30B 80 t/s at 4k, so a gain is unproven; needs a download, so ops first
- 2026-10-22 | aie-2026-10-19-harness-shim-registry | pass | | durable rules are John's (global CLAUDE.md); pruning them is not ours to automate
- 2026-10-22 | 21 cards dated 2026-10-15 with status discarded in experiments.json | covered | | discarded by the 2026-10-16/17 sweeps (git 33ab6a0, 731e47c) before this log began; verdicts live in experiments.json
- 2026-10-24 | do-2026-10-23-two-model-adversarial-verification | covered | yolo / all | a separate reviewer already checks findings here: the gauntlet's fresh blind critic, the code-review verify pass, and this session reviewing next-big-thing's PRs
- 2026-10-24 | do-2026-10-23-module-chunked-scheduled-sweeps | pass | | scheduled cloud agent loops every hour or every 10 minutes cost money (ops-gated) to sweep small single-file projects; nothing here has the attack surface the video's codebases do
- 2026-10-25 | ls-2026-10-22-corroboration-confidence-scoring | pass | brain vault | the vault already labels every claim FACT, Assessment, Speculation or Unverified, and FACT requires a source that was read; counting sources adds little for a one-author newsletter
- 2026-10-27 | aie-2026-10-25-trace-sweep-fix-agent | covered | ops / all | failures are already swept: job-guard alerts, `~/bin/session-digest`, the weekly docs-stale check; an agent opening its own fix PRs on a timer runs against "durable rules are his" and is ops-gated spend
- 2026-10-27 | ail-2026-10-25-egm-goldfish-spec-review | covered | mini-forge / yolo | zero-context reviewers already run here: the gauntlet's fresh blind critic per round, and this session reviewing next-big-thing's PRs cold
- 2026-10-27 | aie-2026-10-24-multi-model-review-council | covered | yolo | the council (`.harness/scripts/council.py`, seven personas) plus Codex and human review on PRs; the video's finding (reviewers rarely overlap) is the case for it, not a new build
- 2026-10-27 | mk-2026-10-23-skills-audit-prune | pass | all | about 30 skills load per session, under the video's 50-skill bloat line; the 23 dangling symlinks in `~/.claude/skills` load nothing (mini-forge CLAUDE.md) and are already pending John's call
- 2026-10-27 | joem-2026-10-26-spec-kit-assess-gate | covered | mini-forge / all | mini-forge's intent interview (five questions, accept or reject) and "build nothing until John says go" are the same go/kill gate
- 2026-10-27 | eh-2026-10-26-option-grid-before-3d | useful, parked (John 2026-10-27: not now) | mini-forge | its design pass picks from 2-3 generated candidates; a 24-48 image grid from the local Chroma server (`tools/genq.sh`, `tools/contact_sheet.py`, the phone gallery on 1235) would let John tap picks before any mesh run; GPU work, so ops first
- 2026-10-31 | ls-2026-10-27-evals-as-code | covered | all | requirements as checks already run here: prepare_mini exits 2, dfm_gate, the Python twins next-big-thing tests every prompt page against
- 2026-10-31 | ail-2026-10-28-token-economizer-pruning | pass | all | Claude Code already defers unused tool schemas (loaded on demand), which is the saving the plugin buys; a third-party hook plugin is new supply-chain surface
- 2026-10-31 | ail-2026-10-28-micro-skills-failure-memory | pass | all | `~/bin/session-digest` already finds repeated failures; a plugin writing its own rules from logs breaks "durable rules are his" and carries the injection risk the video names
- 2026-10-31 | idd-2026-10-26-near-the-loop-approval-agent | covered | ops / all | already how the jobs work: a scheduled job does the work, opens a PR or a phone-sized item, John taps
- 2026-10-31 | idd-2026-10-26-recursive-ui-hill-climb-loop | pass | flagships | heavy token spend to match a mockup; the flagships are not built from mockups, and mini-forge's blind-pair gauntlet is the same idea where it fits
- 2026-10-31 | aie-2026-10-29-strix-halo-quantized-coding-model | maybe, ops-gated | ptt / MS-S1 | B200 and vLLM scale does not transfer; the one lever that might is speculative decoding (a draft model) in llama.cpp for the local writer model; same lane as the 2026-10-22 card
- 2026-10-31 | cm-2026-10-29-model-switch-regression-suite | covered | yolo / editor | `.harness/model-upgrade-audit.md` is yolo's model-bump checklist; editor training has its own evals
- 2026-10-31 | cm-2026-10-29-draft-only-heartbeat-triage | pass | | an inbox-triage heartbeat is not a project here, and every 30 minutes is ops-gated spend
- 2026-10-31 | aie-2026-10-28-layered-verification-evidence | covered | yolo / prompt-built-tools | next-big-thing's PRs carry headless test records and sample pages; reviews here check them
- 2026-10-31 | do-2026-10-30-cross-model-review-filter | covered | yolo | same as the 2026-10-24 two-model card: the council uses Gemini, findings are verified before they are reported
- 2026-10-31 | do-2026-10-30-one-task-thread-minimal-tests | pass | all | a style policy; regression-only tests already match practice here (twins and gates, not unit-test bloat)
- 2026-10-31 | nh-2026-10-30-cap-improvement-loops | covered | mini-forge | the gauntlet stops on a blind win plus a dfm_gate pass, not round count; tick-tock, the open-ended loop here, is retired
- 2026-10-31 | ail-2026-10-30-evals-first-stop-hook | covered | mini-forge / all | prepare_mini's exit 2 and dfm_gate are the completion gate; "never trust a success log" is the standing rule
- 2026-10-31 | ail-2026-10-30-fresh-reviewer-capped-loop | covered | yolo / mini-forge | same as the 2026-10-27 goldfish card: fresh blind critic per round, cold review of every PR
- 2026-10-31 | (no card) Joe Maddalone "Software Factories Are Dumb" (sheet row 2026-10-31) | no card made | | the card writer dropped it (opinion talk, no experiment); its argument that design taste and verification beat assembly lines matches how John already works
- 2026-11-01 | nh-2026-10-30-effort-level-cost-ladder | note | ops cost lanes / scheduled jobs | one anecdote (one task, one run per level); cheap to repeat on a fixed PDF to CSV fix if John ever wants per-job effort defaults, but cost settings are his and ops' call, so not proposed
- 2026-11-02 | cm-2026-10-31-counterfactual-advice-probe | propose | how John and the sessions decide (CLAUDE.md "Give pros and cons", AskUserQuestion Recommended-first) | John picked the Recommended option on most menus this week; a one-line "what would make the other option right" per choice is a cheap check on deference; rule change is his, told him; John 2026-11-02: try it on big choices, added to ~/.claude/CLAUDE.md "Give pros and cons"
- 2026-11-05 | aie-2026-11-03-compile-skill-to-step-graph | note | rabbit-holes (daily researched stories) | the only paid part is the Ask research run, 1 run logged at $0.07; the stories come from the session and the local writer model, so a step graph plus a smaller model saves little and risks the fact checks; revisit if Rabbit Holes moves story research onto the API
- 2026-11-06 | az-2026-11-05-agent-concurrency-cliff-strix-halo | pass | MS-S1 local inference | the sessions run on Claude, not on local llama.cpp, and the local servers (dictation, writer, narrator test) each serve one caller; the benchmark itself is heavy load on a box that froze from memory before (2026-10-19), so no use running it
- 2026-11-08 | aie-2026-11-04-hermes-agent-local-provider-swap | pass | home ops | ops triage already runs in a Claude session on the subscription; a second agent framework on a local model adds a thing to maintain with no failure it would fix, and the video gives no quality evidence
- 2026-11-08 | ls-2026-11-04-vault-mcp-endpoint | pass | brain vault / rabbit-holes | sessions already search the vault and the Rabbit Holes topic ledger with plain file reads and grep, which is the same on-demand lookup; the brain session is disabled (2026-10-21) and Rabbit Holes is kept out of the brain by design
- 2026-11-09 | ail-2026-11-05-router-worker-watchdog | covered | home ops | ops already coordinates and checks in heavy work, per-project sessions do the building, each session has a supervisor unit that restarts it, and job-guard reports failed jobs; parallel workers in worktrees are what the Workflow tool and subagents already give on request, and the video concedes the token cost is much higher
- 2026-11-10 | do-2026-11-07-agent-hardens-calendar-backend-host | pass | family-calendar / MS-S1 | the calendar has no VPS to clone: it runs on the MS-S1 (port 1239, published as cal.edgerush.org), and that host's firewall (ufw already limits RDP to tailscale0 and the LAN) belongs to ops; the card's premise does not match the setup
- 2026-11-11 | az-2026-11-10-comfyui-contiguous-patch-strix-halo | note | mini-forge | real fit for the same chip, but ComfyUI here only runs Hunyuan3D (about 55 s; images run on stable-diffusion.cpp over Vulkan), so the gain is seconds per mesh; Pixal3D (about 6 min, sdpa attention) is where it could pay. The mini-forge session is closed (2026-11-10); worth a timed before and after through the ops GPU gate when 3D work resumes, patch kept reversible since the ROCm venvs must not be reinstalled

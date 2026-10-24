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

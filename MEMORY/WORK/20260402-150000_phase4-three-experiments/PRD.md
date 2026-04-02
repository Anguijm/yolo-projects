---
task: Run three Phase 4 experiments in sequence
slug: 20260402-150000_phase4-three-experiments
effort: deep
phase: observe
progress: 0/18
mode: interactive
started: 2026-04-02T15:00:00+09:00
updated: 2026-04-02T15:00:00+09:00
---

## Context

Running three Phase 4 experiments from the backlog in order: Parallel Agent Sessions, Vertical Planning, Autoresearch Loop. Each experiment tests a hypothesis about improving the YOLO build loop.

## Criteria

### Experiment 1: Parallel Agent Sessions (mlops-2026-04-01)
- [ ] ISC-1: 3 agents spawn in parallel, each in isolated worktree
- [ ] ISC-2: Each agent builds a complete YOLO project independently
- [ ] ISC-3: All 3 projects pass test_project.py
- [ ] ISC-4: Total wall-clock time measured vs sequential estimate
- [ ] ISC-5: Experiment status updated in experiments.json with outcome
- [ ] ISC-6: All 3 projects committed and pushed

### Experiment 2: Vertical Planning (mlops-2026-03-25)
- [ ] ISC-7: Structure outline written before code for one build
- [ ] ISC-8: Outline defines function signatures and data flow
- [ ] ISC-9: Build follows outline without major rework
- [ ] ISC-10: Compare rework rate vs typical non-outlined build
- [ ] ISC-11: Experiment status updated in experiments.json

### Experiment 3: Autoresearch Loop (do-2026-03-31)
- [ ] ISC-12: Single metric defined for optimization
- [ ] ISC-13: Automated eval runs after each iteration
- [ ] ISC-14: Agent iterates autonomously (commit on pass, reset on fail)
- [ ] ISC-15: At least 5 iterations completed
- [ ] ISC-16: Quality improvement measured across iterations
- [ ] ISC-17: Experiment status updated in experiments.json

### Meta
- [ ] ISC-18: All three experiments logged with verdicts

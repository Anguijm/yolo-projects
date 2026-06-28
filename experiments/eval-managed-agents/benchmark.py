#!/usr/bin/env python3
"""
benchmark.py — Claude Managed Agents vs. manual tick-tock orchestration.

Premise (verified against the first-party Claude API, managed-agents-2026-04-01):
Anthropic's Managed Agents surface lets you create a persisted, versioned Agent
(`POST /v1/agents`) and then start stateful Sessions (`POST /v1/sessions`) that
reference it. Anthropic runs the agent loop on its orchestration layer and hosts
a per-session container where the agent's tools (bash/read/write/edit/...) execute.
The session streams events back; you send user messages and tool results in.

That is a genuine alternative to this repo's *manual* orchestration, where the
tick-tock driver owns the whole loop: it resends full conversation history every
turn, hosts tool execution itself, and hand-rolls retry / pause_turn / context
compaction. This benchmark asks: would adopting managed agents simplify the
tick-tock dispatch logic, and at what wall-clock / token cost?

Two modes:
  * static (default) — deterministic, offline. Scores manual vs managed across
    fixed dimensions grounded in documented API behavior, computes an
    "orchestration-ownership delta" (the loop/retry/context surface the repo
    would STOP maintaining), and emits a reproducible verdict + results.md.
  * --live          — a real wall-clock / token benchmark via the Managed Agents
    SDK. Gated behind ANTHROPIC_API_KEY. NEVER auto-run from cron: managed
    sessions run for minutes and bill real tokens, which violates the
    synchronous-finish rule the autonomous builder runs under.

Run:
  python3 benchmark.py                 # static comparison -> results.md + summary
  python3 benchmark.py --json          # machine-readable summary on stdout
  python3 benchmark.py --live          # live benchmark (needs ANTHROPIC_API_KEY)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

MODEL = "claude-opus-4-8"

# A canonical multi-step dev task: one historical YOLO build, replayed as a fixed
# ordered work-list. Deterministic — no dependency on live repo state.
CANONICAL_TASK: dict = {
    "name": "ship-one-yolo-tool",
    "summary": "Build a single-file HTML tool through the 4-gate council pipeline.",
    "steps": [
        "PLAN: write plan.md, run council plan gate",
        "BUILD: write index.html",
        "IMPLEMENTATION: run council implementation gate",
        "PRE-FILTER: test_project.py + eval_bugs.py + security_scan.py",
        "TESTS: run council tests gate",
        "OUTCOME: run council outcome gate",
        "SHIP: update logs, commit, git push origin main",
    ],
    # The manual driver re-sends the growing transcript on every model turn; a
    # managed session keeps it server-side. This count is illustrative of loop
    # ownership, not a billed figure.
    "model_turns_estimate": len(  # one model turn per step that needs the model
        ["PLAN", "BUILD", "IMPL", "TESTS", "OUTCOME"]
    ),
}

# Each dimension contrasts what the *repo* owns under each model. `winner` is the
# orchestration model that requires less bespoke code / fewer failure modes for
# that dimension; rationale is grounded in documented managed-agents behavior.
DIMENSIONS: list[dict] = [
    {
        "key": "agent_loop",
        "manual": "tick-tock driver owns the loop: call model, detect tool/stop, "
                  "feed results back, repeat until done.",
        "managed": "Anthropic runs the loop server-side; you create a session and "
                   "stream events.",
        "winner": "managed",
        "rationale": "The loop is the bulk of dispatch code; managed removes it.",
    },
    {
        "key": "context_passing",
        "manual": "stateless Messages API — resend full history every turn; "
                  "hand-roll compaction near the context limit.",
        "managed": "stateful session; built-in context compaction + prompt caching.",
        "winner": "managed",
        "rationale": "Statefulness eliminates resend + bespoke compaction logic.",
    },
    {
        "key": "tool_execution",
        "manual": "the runner hosts and executes every tool (bash/file ops) itself.",
        "managed": "per-session container hosts tool execution on Anthropic infra "
                   "(cloud env); or self-hosted worker if you want your own infra.",
        "winner": "managed",
        "rationale": "Offloads sandboxing for the cloud path.",
        "caveat": "Cloud container = code runs off-box; a self_hosted env keeps it "
                  "on your infra but reintroduces worker plumbing.",
    },
    {
        "key": "error_recovery",
        "manual": "hand-rolled retry/backoff, pause_turn handling, rebase-and-retry.",
        "managed": "automatic session rescheduling on retryable errors; errors "
                   "surface as session.error events.",
        "winner": "managed",
        "rationale": "Built-in rescheduling replaces bespoke retry plumbing.",
    },
    {
        "key": "determinism_control",
        "manual": "full control of every gate boundary, council injection, and the "
                  "advisory-not-blocking rule — exactly as tick-tock requires.",
        "managed": "the model drives its own trajectory inside the session; gate "
                   "boundaries must be reconstructed via outcomes/custom tools.",
        "winner": "manual",
        "rationale": "Tick-tock's 4-gate discipline + council injection is explicit "
                     "code today; managed would need re-expressing it as outcomes / "
                     "always_ask tool gates.",
    },
    {
        "key": "observability_audit",
        "manual": "every step is a local artifact (council_*.json, logs) committed "
                  "to git — the audit trail IS the repo.",
        "managed": "session event stream + Console; artifacts land in "
                   "/mnt/session/outputs and must be pulled back via files.list.",
        "winner": "manual",
        "rationale": "The repo's git-as-audit-trail is simpler than reconstructing "
                     "state from an event stream for this autonomous use case.",
    },
    {
        "key": "cost_latency",
        "manual": "pay per Messages API call; latency is per-turn round trips you "
                  "control and can short-circuit.",
        "managed": "session inference draws standard ITPM/OTPM; long autonomous "
                   "sessions run minutes — incompatible with a synchronous cron tick.",
        "winner": "manual",
        "rationale": "The synchronous one-shot cron needs bounded, controllable "
                     "turns; a minutes-long managed session can't finish in-process.",
    },
]


def run_static() -> dict:
    """Score the dimensions and produce a structured result + verdict. Pure/offline."""
    tally: dict[str, int] = {"manual": 0, "managed": 0}
    for d in DIMENSIONS:
        tally[d["winner"]] += 1

    # Orchestration-ownership delta: dimensions where managed would let the repo
    # STOP maintaining bespoke code (signature metric of this benchmark).
    sheddable = [d["key"] for d in DIMENSIONS if d["winner"] == "managed"]
    retained = [d["key"] for d in DIMENSIONS if d["winner"] == "manual"]

    # Verdict logic: managed clearly wins on loop/context/tooling/recovery, but the
    # synchronous one-shot cron + explicit 4-gate council discipline are exactly the
    # dimensions managed loses. Net: promising but not a drop-in for tick-tock today.
    verdict = "iterate"
    recommendation = (
        "ITERATE / DEFER adoption. Managed Agents removes the agent-loop, "
        "context-passing, tool-hosting, and error-recovery code that dominates "
        "manual orchestration ({} of {} dimensions). But the tick-tock pipeline's "
        "value is its explicit, synchronous, git-audited 4-gate discipline — the "
        "exact dimensions ({}) where a server-run, minutes-long managed session is "
        "a worse fit for a one-shot cron. Recommend: prototype the COUNCIL-GATE "
        "sub-step (not the whole tick) as a managed session with always_ask tool "
        "gates, measured live with a real key, before committing dispatch changes."
    ).format(len(sheddable), len(DIMENSIONS), ", ".join(retained))

    return {
        "mode": "static",
        "task": CANONICAL_TASK,
        "model": MODEL,
        "dimensions": DIMENSIONS,
        "tally": tally,
        "orchestration_ownership_delta": {
            "sheddable_if_managed": sheddable,
            "retained_under_manual": retained,
            "sheddable_count": len(sheddable),
            "total": len(DIMENSIONS),
        },
        "verdict": verdict,
        "recommendation": recommendation,
        "note": "Static comparison is deterministic and reproducible. Live wall-clock "
                "and token figures require --live with ANTHROPIC_API_KEY.",
    }


def run_live(task: dict, model: str, deadline_s: float = 240.0) -> dict:
    """Live wall-clock / token benchmark via the Managed Agents SDK.

    Gated: requires ANTHROPIC_API_KEY and the `anthropic` SDK. Never auto-run from
    cron. Uses the documented surface: create the agent ONCE, create a session,
    stream events, accumulate token usage, break on a terminal idle/terminated.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("--live needs ANTHROPIC_API_KEY in the environment.")
    try:
        import anthropic  # imported lazily so static mode has zero dependency
    except ImportError:
        raise SystemExit("--live needs the `anthropic` SDK: pip install anthropic")

    client = anthropic.Anthropic()
    prompt = "Task: {}\nSteps:\n{}".format(
        task["summary"], "\n".join(f"- {s}" for s in task["steps"])
    )

    # Resources are created inside the try so a partial-creation failure (e.g.
    # environments.create raises after agents.create succeeds) still hits the
    # finally and cleans up whatever was created. Each handle starts as None and
    # cleanup skips the ones that never got built.
    agent = env = session = None
    started = time.monotonic()
    tokens = {"input": 0, "output": 0, "cache_read": 0, "cache_creation": 0}
    try:
        # Agent is a persisted resource — create once, reference by id. (In a real
        # adoption this id would be stored, not minted per run.)
        agent = client.beta.agents.create(
            name="yolo-bench-agent",
            model=model,
            system="You are a benchmark agent. Complete the task, then stop.",
            tools=[{"type": "agent_toolset_20260401"}],
        )
        env = client.beta.environments.create(
            name=f"yolo-bench-{int(time.time())}",
            # Deny-by-default egress: the benchmark task needs no network access, so
            # we don't grant the container unrestricted egress. Add allowed_hosts
            # only if a future task requires it.
            config={"type": "cloud", "networking": {"type": "limited"}},
        )
        session = client.beta.sessions.create(
            agent=agent.id, environment_id=env.id, title="managed-agents benchmark"
        )
        print(f"[bench] live session {session.id} started; streaming "
              f"(deadline {deadline_s:.0f}s)…", file=sys.stderr, flush=True)
        # Stream-first, then send (events only deliver after the stream opens).
        with client.beta.sessions.events.stream(session_id=session.id) as stream:
            client.beta.sessions.events.send(
                session_id=session.id,
                events=[{"type": "user.message",
                         "content": [{"type": "text", "text": prompt}]}],
            )
            for event in stream:
                if time.monotonic() - started > deadline_s:
                    print("[bench] live deadline reached; stopping stream.",
                          file=sys.stderr, flush=True)
                    break
                etype = getattr(event, "type", None)
                if etype == "span.model_request_end":
                    u = getattr(event, "model_usage", None) or {}
                    tokens["input"] += u.get("input_tokens", 0)
                    tokens["output"] += u.get("output_tokens", 0)
                    tokens["cache_read"] += u.get("cache_read_input_tokens", 0)
                    tokens["cache_creation"] += u.get("cache_creation_input_tokens", 0)
                    print(f"[bench] turn done — in={tokens['input']} out={tokens['output']}",
                          file=sys.stderr, flush=True)
                elif etype == "session.status_terminated":
                    break
                elif etype == "session.status_idle":
                    stop = getattr(event, "stop_reason", None)
                    if getattr(stop, "type", None) != "requires_action":
                        break
    finally:
        # Best-effort cleanup of whatever was created — guarded so a partial-create
        # failure doesn't orphan resources or raise a NameError. Sessions and
        # environments support delete; agents are persisted (archive only).
        cleanup = [
            ("session", session, lambda h: client.beta.sessions.delete(h.id)),
            ("environment", env, lambda h: client.beta.environments.delete(h.id)),
            ("agent", agent, lambda h: client.beta.agents.archive(h.id)),
        ]
        for label, handle, fn in cleanup:
            if handle is None:
                continue
            try:
                fn(handle)
            except Exception as exc:  # never mask the benchmark result/error
                print(f"[bench] cleanup of {label} failed: {exc}",
                      file=sys.stderr, flush=True)

    elapsed = time.monotonic() - started
    return {
        "mode": "live",
        "model": model,
        "agent_id": agent.id,
        "session_id": session.id,
        "wall_clock_s": round(elapsed, 2),
        "tokens": tokens,
        "note": "Single managed session; compare against manual per-turn metrics "
                "captured by the tick-tock driver to complete the benchmark.",
    }


def _dimension_table(result: dict) -> str:
    rows = ["| Dimension | Manual owns | Managed owns | Less code |",
            "|---|---|---|---|"]
    for d in result["dimensions"]:
        rows.append("| `{}` | {} | {} | **{}** |".format(
            d["key"], d["manual"], d["managed"], d["winner"]))
    return "\n".join(rows)


def write_results_md(result: dict, path: str) -> None:
    t = result["tally"]
    delta = result["orchestration_ownership_delta"]
    md = f"""# Results — Managed Agents vs. manual tick-tock orchestration

*Generated by `benchmark.py` in static (deterministic) mode. Re-run to reproduce.*

## Premise

Claude **Managed Agents** (first-party, `managed-agents-2026-04-01`) provides
server-run orchestration: a persisted Agent (`POST /v1/agents`) plus stateful
Sessions (`POST /v1/sessions`). Anthropic runs the agent loop and hosts a
per-session container for tool execution. This repo's tick-tock builder instead
does **manual** orchestration — it owns the loop, resends full history each turn,
hosts tool execution, and hand-rolls retry/compaction.

Task benchmarked: **{result['task']['name']}** — {result['task']['summary']}

## Dimension-by-dimension

{_dimension_table(result)}

## Score

- Dimensions where **managed** needs less bespoke code: **{t['managed']}**
- Dimensions where **manual** is the better fit: **{t['manual']}**

## Orchestration-ownership delta

Adopting managed agents would let the repo **stop maintaining** code for:
{os.linesep.join('- `' + k + '`' for k in delta['sheddable_if_managed'])}

…but it would have to **re-express** these, which manual handles natively today:
{os.linesep.join('- `' + k + '`' for k in delta['retained_under_manual'])}

## Verdict: **{result['verdict'].upper()}**

{result['recommendation']}

## How to extend

Run a live benchmark to get real wall-clock + token numbers (needs a key):

```bash
ANTHROPIC_API_KEY=... python3 benchmark.py --live
```

The live path is deliberately **not** run by the autonomous cron — managed
sessions run for minutes and bill real tokens, which is incompatible with the
synchronous one-shot tick. {result['note']}
"""
    with open(path, "w") as f:
        f.write(md)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Managed Agents vs manual orchestration benchmark.")
    ap.add_argument("--live", action="store_true",
                    help="Run the live SDK benchmark (needs ANTHROPIC_API_KEY). "
                         "Never run this from cron.")
    ap.add_argument("--json", action="store_true", help="Print machine-readable JSON only.")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "results.md"),
                    help="Path for the generated results.md (static mode).")
    args = ap.parse_args(argv)

    if args.live:
        result = run_live(CANONICAL_TASK, MODEL)
        print(json.dumps(result, indent=2))
        return 0

    result = run_static()
    write_results_md(result, args.out)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        t = result["tally"]
        print(f"[bench] static comparison complete — verdict: {result['verdict'].upper()}")
        print(f"[bench] managed-wins={t['managed']}  manual-wins={t['manual']}  "
              f"sheddable={result['orchestration_ownership_delta']['sheddable_count']}"
              f"/{result['orchestration_ownership_delta']['total']}")
        print(f"[bench] results written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

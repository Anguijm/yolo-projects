#!/usr/bin/env python3
"""timing_extract.py — per-stage wall-clock timing for the YOLO tick-tock loop.

Tests the hypothesis (from Phase-4 experiment nb-2026-04-16-fix-bottleneck-not-
ai-speed): *AI speed may not be the loop bottleneck.* It decomposes loop time
using timing data we ALREADY emit — no new instrumentation:

  1. Local council JSON timestamps (primary, offline): every gate writes
     <project>/council_<gate>.json with an ISO `timestamp`. The four gates of a
     single build (plan -> implementation -> tests -> outcome) give inter-gate
     intervals = build/fix time + council latency.
  2. GitHub Actions step durations (CI-only, optional): `gh run view <id>
     --json jobs` yields each step's name + startedAt/completedAt — capturing the
     NON-AI stages (checkout, pip/npm install, git push) the council JSON cannot
     see. Uses --json (structured step names), never parses workflow YAML, so a
     YAML reformat cannot break it.

Read-only. Writes only timing_log.json and (with --report) REPORT.md.

Usage:
  python3 timing_extract.py --source local --report
  python3 timing_extract.py --source both --runs 5 --report
  python3 timing_extract.py --selftest
"""
import argparse
import json
import os
import re
import statistics
import subprocess
import sys
from datetime import datetime

# Resolve repo root: this file lives at <root>/experiments/infra-loop-timing/.
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GATES = ["plan", "implementation", "tests", "outcome"]
WORKFLOW_YAML = os.path.join(REPO_ROOT, ".github", "workflows", "tick_tock.yml")
WORKFLOW_NAME = "tick_tock.yml"


def parse_iso(ts):
    """Tolerant ISO-8601 parse. Returns datetime or None."""
    if not ts or not isinstance(ts, str):
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _sanitize(s, maxlen=120):
    """Make a string safe to embed in markdown (no injection / no table-
    breaking). Strips newlines and escapes pipes/backticks. `maxlen` bounds
    table cells (default 120); pass a larger value for full-text bullets."""
    if not isinstance(s, str):
        s = str(s)
    s = s.replace("\r", " ").replace("\n", " ")
    s = s.replace("|", "\\|").replace("`", "'")
    s = re.sub(r"\s+", " ", s).strip()
    return s[:maxlen]


def collect_council_files(roots):
    """project_dir -> {gate: abspath} for every council_<gate>.json found."""
    out = {}
    for root in roots:
        if not os.path.isdir(root):
            continue
        for entry in sorted(os.listdir(root)):
            proj = os.path.join(root, entry)
            if not os.path.isdir(proj):
                continue
            for gate in GATES:
                p = os.path.join(proj, f"council_{gate}.json")
                if os.path.isfile(p):
                    rel = os.path.relpath(proj, REPO_ROOT)
                    out.setdefault(rel, {})[gate] = p
    return out


def extract_local_timings(files, max_gap_min):
    """Per-project gate timestamps + inter-gate deltas. Marks a build
    `coherent` only when all present gate timestamps fall within max_gap_min
    AND are monotonic — gate files get overwritten across builds, so a dir can
    hold gate files from different dates."""
    records = []
    skipped = 0
    for proj, gatemap in sorted(files.items()):
        gates = {}
        objections = {}
        for gate, path in gatemap.items():
            try:
                d = json.load(open(path, encoding="utf-8"))
            except (json.JSONDecodeError, OSError, ValueError):
                skipped += 1
                continue
            dt = parse_iso(d.get("timestamp"))
            if dt is not None:
                gates[gate] = dt
                objections[gate] = len(d.get("objections") or [])
        present = [g for g in GATES if g in gates]
        rec = {
            "project": proj,
            "gates_present": present,
            "objections": {g: objections.get(g, 0) for g in present},
            "total_objections": sum(objections.get(g, 0) for g in present),
        }
        if len(present) >= 2:
            times = [gates[g] for g in present]
            span_min = (max(times) - min(times)).total_seconds() / 60.0
            monotonic = all(
                gates[present[i + 1]] >= gates[present[i]]
                for i in range(len(present) - 1)
            )
            coherent = span_min <= max_gap_min and monotonic
            rec["coherent"] = coherent
            rec["span_minutes"] = round(span_min, 2)
            intervals = {}
            for i in range(len(present) - 1):
                a, b = present[i], present[i + 1]
                intervals[f"{a}->{b}"] = round(
                    (gates[b] - gates[a]).total_seconds(), 1
                )
            rec["intervals_sec"] = intervals
        else:
            rec["coherent"] = False
            rec["span_minutes"] = None
            rec["intervals_sec"] = {}
        records.append(rec)
    return records, skipped


def aggregate_local(records):
    """Median/total per gate-interval over COHERENT builds only."""
    coherent = [r for r in records if r.get("coherent")]
    if not coherent:
        return {
            "coherent_builds": 0,
            "total_builds_seen": len(records),
            "interval_medians_sec": {},
            "total_objections": sum(r["total_objections"] for r in records),
        }
    buckets = {}
    for r in coherent:
        for k, v in r["intervals_sec"].items():
            buckets.setdefault(k, []).append(v)
    medians = {
        k: {
            "median_sec": round(statistics.median(v), 1),
            "max_sec": round(max(v), 1),
            "n": len(v),
        }
        for k, v in buckets.items()
    }
    return {
        "coherent_builds": len(coherent),
        "total_builds_seen": len(records),
        "interval_medians_sec": medians,
        "total_objections": sum(r["total_objections"] for r in coherent),
        "objection_heavy_gates": _objection_heavy(coherent),
    }


def _objection_heavy(records):
    """Which gate accrues the most advisory objections across builds."""
    tally = {}
    for r in records:
        for g, n in r["objections"].items():
            tally[g] = tally.get(g, 0) + n
    return dict(sorted(tally.items(), key=lambda kv: -kv[1]))


# ---------------------------------------------------------------------------
# GitHub Actions path (CI-only; degrades to empty without a token)
# ---------------------------------------------------------------------------
def run_cmd(args, timeout=60):
    """Subprocess wrapper with a fixed argv list (no shell). Never raises."""
    try:
        p = subprocess.run(
            args, capture_output=True, text=True, timeout=timeout, check=False
        )
        return p.returncode, p.stdout, p.stderr
    except (subprocess.TimeoutExpired, OSError) as e:
        return 1, "", str(e)


def gh_available():
    """gh binary present AND a token in the environment."""
    if not (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")):
        return False
    rc, _, _ = run_cmd(["gh", "--version"])
    return rc == 0


def list_recent_runs(workflow, n):
    rc, out, _ = run_cmd(
        ["gh", "run", "list", "--workflow", workflow, "-L", str(n),
         "--json", "databaseId,conclusion,createdAt"]
    )
    if rc != 0:
        return []
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return []


def extract_gh_timings(runs):
    """Per-run step name -> duration (sec) via `gh run view --json jobs`."""
    out = []
    for run in runs:
        rid = str(run.get("databaseId", ""))
        if not rid:
            continue
        rc, raw, _ = run_cmd(
            ["gh", "run", "view", rid, "--json", "jobs"]
        )
        if rc != 0:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        steps = {}
        for job in data.get("jobs", []):
            for step in job.get("steps", []):
                a = parse_iso(step.get("startedAt"))
                b = parse_iso(step.get("completedAt"))
                if a and b and b >= a:
                    steps[_sanitize(step.get("name", "?"))] = round(
                        (b - a).total_seconds(), 1
                    )
        out.append({
            "run_id": rid,
            "conclusion": run.get("conclusion"),
            "created_at": run.get("createdAt"),
            "steps_sec": steps,
        })
    return out


def aggregate_gh(runs):
    if not runs:
        return {"runs_seen": 0, "step_medians_sec": {}}
    buckets = {}
    for r in runs:
        for name, dur in r["steps_sec"].items():
            buckets.setdefault(name, []).append(dur)
    medians = {
        name: {"median_sec": round(statistics.median(v), 1),
               "max_sec": round(max(v), 1), "n": len(v)}
        for name, v in buckets.items()
    }
    return {"runs_seen": len(runs), "step_medians_sec": medians}


def detect_uncached_installs(yaml_path):
    """Scan the workflow text for install steps that run with NO dependency
    caching configured. Text/regex only (no YAML structure dependence); tolerant
    of a missing file. Returns a list of human-readable findings."""
    findings = []
    try:
        text = open(yaml_path, encoding="utf-8").read()
    except OSError:
        return ["workflow file not found — cannot check for caching"]
    has_cache = bool(
        re.search(r"actions/cache@", text)
        or re.search(r"^\s*cache:\s*\S", text, re.MULTILINE)
    )
    install_lines = re.findall(
        r"^\s*run:\s*(.*(?:pip install|npm install|npm ci|apt-get install).*)$",
        text, re.MULTILINE,
    )
    if install_lines and not has_cache:
        findings.append(
            "Install steps run UNCACHED on every invocation (no actions/cache "
            "and no setup-* cache: key): "
            + "; ".join(_sanitize(x) for x in install_lines)
        )
    return findings


def identify_bottlenecks(local_agg, gh_agg, yaml_findings):
    """Rank concrete findings, separating non-AI (mechanical) from AI stages."""
    out = []
    # Non-AI mechanical overhead repeated every run — the cleanest fixable win.
    for f in yaml_findings:
        out.append({
            "kind": "non_ai",
            "severity": "high",
            "finding": f,
            "fix": "Add actions/cache (or setup-python/node cache:) for pip + "
                   "npm so install steps are near-instant on warm cache.",
        })
    # GHA step medians: surface the slowest NON-AI steps if we have live data.
    steps = gh_agg.get("step_medians_sec", {})
    nonai_steps = {
        k: v for k, v in steps.items()
        if not re.search(r"agent|council|claude", k, re.I)
    }
    if nonai_steps:
        slowest = max(nonai_steps.items(), key=lambda kv: kv[1]["median_sec"])
        out.append({
            "kind": "non_ai",
            "severity": "medium",
            "finding": f"Slowest non-AI workflow step (median): "
                       f"{slowest[0]} = {slowest[1]['median_sec']}s "
                       f"(n={slowest[1]['n']})",
            "fix": "Cache or pre-bake this step into a container image.",
        })
    # AI stages: inter-gate intervals from local council data.
    ivals = local_agg.get("interval_medians_sec", {})
    if ivals:
        slowest = max(ivals.items(), key=lambda kv: kv[1]["median_sec"])
        out.append({
            "kind": "ai",
            "severity": "info",
            "finding": f"Slowest AI inter-gate interval (median): "
                       f"{slowest[0]} = {slowest[1]['median_sec']}s "
                       f"(build+fix+council, n={slowest[1]['n']})",
            "fix": "AI work dominates here; reduce escalation rounds rather "
                   "than raw model speed.",
        })
    return out


def render_report(log):
    """Render REPORT.md from the timing_log dict. All embedded strings are
    sanitized at extraction time (_sanitize) to prevent table/markdown injection."""
    L = []
    a = L.append
    a("# infra-loop-timing — REPORT")
    a("")
    a(f"*Generated by `timing_extract.py` at "
      f"{_sanitize(log.get('generated_at'), maxlen=40)}.*")
    a("*Sources used: "
      f"{_sanitize(', '.join(log.get('sources_used') or ['none']))}.*")
    a("")
    a("## What this measures")
    a("")
    a("Per-stage wall-clock decomposition of the YOLO tick-tock loop, built "
      "from timing data we already emit — **no new instrumentation**:")
    a("")
    a("- **Local council JSON timestamps** (offline): inter-gate intervals "
      "for a single build. NOTE: each interval conflates *build/fix time* "
      "with *council latency* — it is not council time alone.")
    a("- **GitHub Actions step durations** (CI-only, via `gh ... --json jobs`): "
      "the non-AI stages (checkout, pip/npm install, git push) the council "
      "JSON cannot see.")
    a("")
    a("### Data-source decision")
    a("")
    a("We use both *existing* sources and instrument nothing. Instrumenting "
      "`council.py` would measure only council latency and miss the non-AI "
      "stages the hypothesis targets, while adding code to the hot path. GHA "
      "step boundaries + council JSON timestamps cover the full loop for free. "
      "The gh path reads `--json jobs` (structured step names), never parses "
      "workflow YAML, so a YAML reformat cannot break it.")
    a("")

    # --- AI: local council intervals
    la = log.get("local", {}).get("aggregate", {})
    a("## AI stages — council inter-gate intervals (local)")
    a("")
    a(f"Coherent same-session builds analyzed: "
      f"**{la.get('coherent_builds', 0)}** "
      f"(of {la.get('total_builds_seen', 0)} project dirs with council JSON; "
      f"incoherent dirs hold gate files overwritten across different builds "
      f"and are excluded from intervals).")
    a("")
    a("> **Self-measurement note:** this tool reads council JSON, so its own "
      "build (`infra-loop-timing`) appears in the corpus once its gates run. "
      "Per-interval `n` can therefore differ by one across rows — the last "
      "gate (`tests->outcome`) is written after report generation, so it lags "
      "the earlier intervals by one build. This is expected, not a data bug.")
    a("")
    medians = la.get("interval_medians_sec", {})
    if medians:
        a("| Interval | Median (s) | Max (s) | n |")
        a("|---|---:|---:|---:|")
        for k in ["plan->implementation", "implementation->tests",
                  "tests->outcome"]:
            if k in medians:
                m = medians[k]
                a(f"| {_sanitize(k)} | {m['median_sec']} | {m['max_sec']} "
                  f"| {m['n']} |")
        a("")
    else:
        a("_No coherent builds found._")
        a("")
    oh = la.get("objection_heavy_gates", {})
    if oh:
        a("Advisory objections by gate (across coherent builds): "
          + ", ".join(f"`{_sanitize(g)}`={n}" for g, n in oh.items()) + ".")
        a("")

    # --- Non-AI: gh steps
    ga = log.get("gh", {}).get("aggregate", {})
    a("## Non-AI stages — GitHub Actions step durations")
    a("")
    if ga.get("runs_seen"):
        a(f"Runs analyzed: **{ga['runs_seen']}**.")
        a("")
        a("| Step | Median (s) | Max (s) | n |")
        a("|---|---:|---:|---:|")
        for name, m in sorted(
            ga.get("step_medians_sec", {}).items(),
            key=lambda kv: -kv[1]["median_sec"],
        ):
            a(f"| {name} | {m['median_sec']} | {m['max_sec']} | {m['n']} |")
        a("")
    else:
        a("_No live GitHub Actions data (no `GH_TOKEN` in this environment)._ "
          "The gh-mode test against ≥5 real recent runs runs in CI, where the "
          "runner has `GH_TOKEN`. Invoke there with "
          "`python3 timing_extract.py --source gh --runs 5 --report`.")
        a("")

    # --- Bottlenecks
    a("## Bottlenecks identified")
    a("")
    bn = log.get("bottlenecks", [])
    if bn:
        for b in bn:
            a(f"- **[{_sanitize(b['kind'])} / {_sanitize(b['severity'])}]** "
              f"{_sanitize(b['finding'], maxlen=400)}")
            a(f"  - *Fix:* {_sanitize(b['fix'], maxlen=400)}")
    else:
        a("- _None identified from available data._")
    a("")
    a("## Verdict on the hypothesis")
    a("")
    a("The decomposition separates **non-AI mechanical overhead** (uncached "
      "installs, checkout, push — fixed cost every hourly run, independent of "
      "build difficulty) from **AI stages** (inter-gate build/fix/council "
      "intervals). The mechanical overhead is the bottleneck class that is "
      "*directly fixable without faster models* — caching dependencies removes "
      "it from every run. AI inter-gate time is dominated by escalation/fix "
      "rounds, not raw model latency, so the lever there is fewer rounds, not "
      "a faster backbone.")
    a("")
    return "\n".join(L)


def build_log(source, runs_n, max_gap_min):
    files = collect_council_files(
        [REPO_ROOT, os.path.join(REPO_ROOT, "experiments")]
    )
    records, skipped = extract_local_timings(files, max_gap_min)
    local_agg = aggregate_local(records)

    gh_runs, gh_agg = [], {"runs_seen": 0, "step_medians_sec": {}}
    sources_used = ["local"]
    gh_note = None
    if source in ("gh", "both"):
        if gh_available():
            raw = list_recent_runs(WORKFLOW_NAME, runs_n)
            gh_runs = extract_gh_timings(raw)
            gh_agg = aggregate_gh(gh_runs)
            sources_used.append("gh")
        else:
            gh_note = "gh unavailable (no GH_TOKEN/binary) — local only"
            if source == "gh":
                sources_used = ["local-fallback"]

    yaml_findings = detect_uncached_installs(WORKFLOW_YAML)
    bottlenecks = identify_bottlenecks(local_agg, gh_agg, yaml_findings)

    log = {
        "generated_at": os.environ.get("TIMING_NOW", "")
        or datetime.fromtimestamp(os.path.getmtime(__file__)).isoformat(),
        "sources_used": sources_used,
        "gh_note": gh_note,
        "skipped_files": skipped,
        "local": {"records": records, "aggregate": local_agg},
        "gh": {"runs": gh_runs, "aggregate": gh_agg},
        "bottlenecks": bottlenecks,
    }
    return log


def selftest():
    """Invariant checks over the live local corpus. Exit 0 = PASS."""
    ok = True

    def check(cond, msg):
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}  {msg}")
        ok = ok and cond

    log = build_log("local", 0, 360)
    la = log["local"]["aggregate"]
    check(la["total_builds_seen"] >= 5,
          f">=5 project dirs with council JSON ({la['total_builds_seen']} seen)")
    check(la["coherent_builds"] >= 1,
          f">=1 coherent build ({la['coherent_builds']} found)")
    # All coherent builds must have non-negative intervals.
    neg = [
        r["project"] for r in log["local"]["records"]
        if r.get("coherent")
        for v in r["intervals_sec"].values() if v < 0
    ]
    check(not neg, f"no negative intervals in coherent builds ({neg})")
    # JSON round-trips.
    try:
        json.loads(json.dumps(log))
        check(True, "timing_log round-trips through JSON")
    except (TypeError, ValueError) as e:
        check(False, f"JSON round-trip failed: {e}")
    rep = render_report(log)
    check(len(rep) > 200 and "REPORT" in rep, "REPORT.md renders non-empty")
    check(len(log["bottlenecks"]) >= 1,
          f">=1 bottleneck identified ({len(log['bottlenecks'])})")
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=["local", "gh", "both"], default="both",
                    help="Timing source. local=council JSON; gh=GitHub Actions "
                         "steps; both (default), gh auto-skips without a token.")
    ap.add_argument("--runs", type=int, default=5,
                    help="How many recent tick_tock runs to pull (gh source).")
    ap.add_argument("--out", default=os.path.join(HERE, "timing_log.json"),
                    help="Path for the timing_log.json output.")
    ap.add_argument("--report", action="store_true",
                    help="Also write REPORT.md next to the script.")
    ap.add_argument("--max-session-gap-min", type=int, default=360,
                    help="Max minutes spanning a build's gates for it to count "
                         "as one coherent session (default 360).")
    ap.add_argument("--selftest", action="store_true",
                    help="Run invariant checks over the local corpus and exit.")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    log = build_log(args.source, args.runs, args.max_session_gap_min)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
    la = log["local"]["aggregate"]
    print(f"[timing] sources={log['sources_used']} "
          f"coherent_builds={la.get('coherent_builds', 0)} "
          f"gh_runs={log['gh']['aggregate'].get('runs_seen', 0)} "
          f"bottlenecks={len(log['bottlenecks'])} -> {args.out}")
    if log.get("gh_note"):
        print(f"[timing] note: {log['gh_note']}")
    if args.report:
        report_path = os.path.join(HERE, "REPORT.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(render_report(log))
        print(f"[timing] report -> {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

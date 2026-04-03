#!/usr/bin/env python3
"""
run_eval.py -- Golden-Prompt Eval Suite Runner

Regression test framework for verifying YOLO build quality across model upgrades.
Does NOT call Claude or build anything. Provides scaffolding for manual or
cron-triggered eval runs: loads prompts, runs test_project.py on built outputs,
and generates structured JSON reports for comparison.

Usage:
    python3 run_eval.py --model "opus-4" --run         # Run eval on built projects
    python3 run_eval.py --model "opus-4" --list        # List prompts without running
    python3 run_eval.py --compare old.json new.json    # Diff two reports
    python3 run_eval.py --model "opus-4" --run --ids eval-1-devtool,eval-3-creative
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
YOLO_ROOT = SCRIPT_DIR.parent
PROMPTS_FILE = SCRIPT_DIR / "prompts.json"
REPORTS_DIR = SCRIPT_DIR / "reports"
TEST_RUNNER = YOLO_ROOT / "test_project.py"


def load_prompts(filter_ids=None):
    """Load eval prompts from prompts.json, optionally filtering by ID."""
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)
    if filter_ids:
        id_set = set(filter_ids)
        prompts = [p for p in prompts if p["id"] in id_set]
    return prompts


def list_prompts(prompts):
    """Print a summary table of all eval prompts."""
    print(f"{'ID':<24} {'Category':<22} {'Criteria':<6} Prompt (first 60 chars)")
    print("-" * 120)
    for p in prompts:
        snippet = p["prompt"][:60].replace("\n", " ")
        print(f"{p['id']:<24} {p['category']:<22} {len(p['success_criteria']):<6} {snippet}...")
    print(f"\nTotal: {len(prompts)} prompts")


def derive_project_name(eval_id):
    """Derive expected project directory name from eval ID.

    Convention: eval-N-slug -> model-eval-N-slug
    The builder should create projects in YOLO_ROOT with this naming.
    Falls back to checking if a directory matching the eval ID exists.
    """
    # Try exact match first
    candidate = YOLO_ROOT / eval_id
    if candidate.is_dir():
        return eval_id

    # Try with model-eval- prefix stripped to just the slug
    slug = eval_id.replace("eval-", "", 1)
    for pattern in [f"eval-{slug}", slug]:
        candidate = YOLO_ROOT / pattern
        if candidate.is_dir():
            return pattern

    return eval_id


def run_test_project(project_name):
    """Run test_project.py on a built project and return results.

    Returns dict with keys: passed, checks, error
    """
    project_dir = YOLO_ROOT / project_name

    if not project_dir.is_dir():
        return {
            "passed": False,
            "checks": {},
            "error": f"Project directory not found: {project_dir}"
        }

    html_file = project_dir / "index.html"
    if not html_file.exists():
        html_files = list(project_dir.glob("*.html"))
        if not html_files:
            return {
                "passed": False,
                "checks": {},
                "error": "No HTML file found in project directory"
            }

    try:
        result = subprocess.run(
            [sys.executable, str(TEST_RUNNER), project_name],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(YOLO_ROOT)
        )
        # Parse the output for pass/fail info
        output = result.stdout + result.stderr
        passed = result.returncode == 0

        # Extract individual check results from output
        checks = {}
        for line in output.split("\n"):
            line = line.strip()
            if line.startswith(("✓", "✗")):
                # Parse "✓ check_name: detail" or "✗ check_name: detail"
                is_pass = line.startswith("✓")
                rest = line[1:].strip()
                if ":" in rest:
                    name, detail = rest.split(":", 1)
                    checks[name.strip()] = {
                        "passed": is_pass,
                        "detail": detail.strip()
                    }

        return {
            "passed": passed,
            "checks": checks,
            "error": None,
            "raw_output": output[:2000]
        }
    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "checks": {},
            "error": "test_project.py timed out after 60s"
        }
    except Exception as e:
        return {
            "passed": False,
            "checks": {},
            "error": str(e)
        }


def run_eval(model_name, prompts):
    """Run the full eval suite and return a report dict."""
    report = {
        "model": model_name,
        "date": datetime.now(timezone.utc).isoformat(),
        "total_prompts": len(prompts),
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "results": []
    }

    for prompt_def in prompts:
        eval_id = prompt_def["id"]
        category = prompt_def["category"]
        print(f"\n{'='*60}")
        print(f"  [{eval_id}] {category}")
        print(f"{'='*60}")

        project_name = derive_project_name(eval_id)
        start_time = time.time()
        test_result = run_test_project(project_name)
        elapsed = round(time.time() - start_time, 2)

        if test_result.get("error") and "not found" in test_result["error"]:
            status = "skipped"
            report["skipped"] += 1
            print(f"  SKIPPED: {test_result['error']}")
        elif test_result["passed"]:
            status = "passed"
            report["passed"] += 1
            print(f"  PASSED ({elapsed}s)")
        else:
            status = "failed"
            report["failed"] += 1
            print(f"  FAILED ({elapsed}s)")
            if test_result.get("error"):
                print(f"  Error: {test_result['error']}")

        # Print individual checks
        for check_name, check_data in test_result.get("checks", {}).items():
            icon = "+" if check_data["passed"] else "-"
            print(f"    [{icon}] {check_name}: {check_data['detail']}")

        entry = {
            "id": eval_id,
            "category": category,
            "project_name": project_name,
            "status": status,
            "time_seconds": elapsed,
            "test_checks": test_result.get("checks", {}),
            "error": test_result.get("error"),
            "success_criteria": prompt_def["success_criteria"],
            "min_council_scores": prompt_def["min_council_scores"]
        }
        report["results"].append(entry)

    # Summary
    print(f"\n{'='*60}")
    print(f"  EVAL COMPLETE: {model_name}")
    print(f"  Passed: {report['passed']}/{report['total_prompts']}")
    print(f"  Failed: {report['failed']}/{report['total_prompts']}")
    print(f"  Skipped: {report['skipped']}/{report['total_prompts']}")
    print(f"{'='*60}")

    return report


def save_report(report):
    """Save report to reports/ directory with timestamped filename."""
    REPORTS_DIR.mkdir(exist_ok=True)
    model_slug = report["model"].replace(" ", "-").replace("/", "-").lower()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"eval-{model_slug}-{timestamp}.json"
    filepath = REPORTS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved: {filepath}")
    return filepath


def compare_reports(old_path, new_path):
    """Compare two eval reports and print a diff summary."""
    with open(old_path, "r", encoding="utf-8") as f:
        old = json.load(f)
    with open(new_path, "r", encoding="utf-8") as f:
        new = json.load(f)

    print(f"\n{'='*70}")
    print(f"  EVAL COMPARISON")
    print(f"  Old: {old['model']} ({old['date']})")
    print(f"  New: {new['model']} ({new['date']})")
    print(f"{'='*70}")

    # Build lookup by ID
    old_by_id = {r["id"]: r for r in old["results"]}
    new_by_id = {r["id"]: r for r in new["results"]}

    all_ids = sorted(set(list(old_by_id.keys()) + list(new_by_id.keys())))

    regressions = []
    improvements = []
    unchanged = []

    for eid in all_ids:
        o = old_by_id.get(eid)
        n = new_by_id.get(eid)

        if not o:
            print(f"  [NEW]  {eid}: {n['status']}")
            continue
        if not n:
            print(f"  [GONE] {eid}: was {o['status']}")
            continue

        old_status = o["status"]
        new_status = n["status"]

        if old_status == new_status:
            unchanged.append(eid)
            symbol = "="
        elif new_status == "passed" and old_status != "passed":
            improvements.append(eid)
            symbol = "+"
        elif new_status != "passed" and old_status == "passed":
            regressions.append(eid)
            symbol = "!"
        else:
            unchanged.append(eid)
            symbol = "~"

        time_delta = ""
        if o.get("time_seconds") and n.get("time_seconds"):
            delta = n["time_seconds"] - o["time_seconds"]
            time_delta = f" ({delta:+.1f}s)"

        print(f"  [{symbol}] {eid:<24} {old_status:<10} -> {new_status:<10}{time_delta}")

        # Show check-level diffs for regressions
        if eid in regressions:
            old_checks = set(
                k for k, v in o.get("test_checks", {}).items() if v.get("passed")
            )
            new_checks = set(
                k for k, v in n.get("test_checks", {}).items() if v.get("passed")
            )
            lost = old_checks - new_checks
            if lost:
                for check in sorted(lost):
                    print(f"         REGRESSION: {check} was passing, now failing")

    # Summary
    print(f"\n  Summary:")
    print(f"    Improvements: {len(improvements)}")
    print(f"    Regressions:  {len(regressions)}")
    print(f"    Unchanged:    {len(unchanged)}")

    old_pass_rate = old["passed"] / max(old["total_prompts"], 1) * 100
    new_pass_rate = new["passed"] / max(new["total_prompts"], 1) * 100
    print(f"    Pass rate:    {old_pass_rate:.0f}% -> {new_pass_rate:.0f}%")

    if regressions:
        print(f"\n  WARNING: {len(regressions)} regression(s) detected!")
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Golden-Prompt Eval Suite for YOLO builds"
    )
    parser.add_argument(
        "--model", type=str, help="Model name/version label for this run"
    )
    parser.add_argument(
        "--run", action="store_true", help="Run the eval suite"
    )
    parser.add_argument(
        "--list", action="store_true", help="List all eval prompts"
    )
    parser.add_argument(
        "--ids", type=str, help="Comma-separated eval IDs to run (default: all)"
    )
    parser.add_argument(
        "--compare", nargs=2, metavar=("OLD", "NEW"),
        help="Compare two report JSON files"
    )
    parser.add_argument(
        "--json", action="store_true", help="Print report as JSON to stdout"
    )

    args = parser.parse_args()

    if args.compare:
        sys.exit(compare_reports(args.compare[0], args.compare[1]))

    filter_ids = args.ids.split(",") if args.ids else None
    prompts = load_prompts(filter_ids)

    if args.list:
        list_prompts(prompts)
        return

    if args.run:
        if not args.model:
            print("Error: --model is required with --run")
            sys.exit(1)
        report = run_eval(args.model, prompts)
        save_report(report)
        if args.json:
            print(json.dumps(report, indent=2))
        sys.exit(1 if report["failed"] > 0 else 0)

    parser.print_help()


if __name__ == "__main__":
    main()

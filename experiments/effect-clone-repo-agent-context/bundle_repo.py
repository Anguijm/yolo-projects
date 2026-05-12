#!/usr/bin/env python3
"""Pre-compute a repo context bundle for a given diff.

Produces a markdown blob suitable for prepending to an LLM reviewer prompt:
  1. One-paragraph repo overview (from CLAUDE.md or a fallback)
  2. List of changed files
  3. Full contents of each changed file (post-diff state)
  4. Top-N most-related files inlined
  5. Token-budget summary

Soft token cap (default 8000, approximated as chars/4). Truncation order:
related files first (least essential), then trim each changed file from
the middle if any single one exceeds 25% of the budget on its own.

Usage:
    python3 bundle_repo.py [--diff PATH | --demo] [--max-tokens N]
                           [--repo-root PATH]

Output goes to stdout.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_MAX_TOKENS = 8000
CHARS_PER_TOKEN = 4
TOP_RELATED = 5


def approx_tokens(text: str) -> int:
    return len(text) // CHARS_PER_TOKEN


def parse_diff_paths(diff_text: str) -> list[str]:
    """Extract changed file paths from a unified diff. Post-rename targets win."""
    paths: list[str] = []
    seen: set[str] = set()
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            path = line[len("+++ b/"):].strip()
            if path != "/dev/null" and path not in seen:
                paths.append(path)
                seen.add(path)
    return paths


def find_related(repo_root: Path, changed: list[str], k: int) -> list[Path]:
    """Heuristic 'related files': directory-siblings + name-prefix matches.

    Not an import graph — we deliberately keep this dumb so it can't lie.
    """
    related: list[tuple[int, Path]] = []
    changed_paths = [Path(p) for p in changed]
    changed_dirs = {p.parent for p in changed_paths}
    changed_stems = {p.stem for p in changed_paths}

    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.relative_to(repo_root).parts):
            continue
        rel = path.relative_to(repo_root)
        if str(rel) in changed:
            continue
        if path.suffix not in {".py", ".md", ".yml", ".yaml", ".toml", ".json"}:
            continue
        if path.stat().st_size > 50_000:
            continue
        score = 0
        if rel.parent in changed_dirs:
            score += 3
        if any(rel.stem.startswith(s) or s.startswith(rel.stem) for s in changed_stems):
            score += 2
        if score > 0:
            related.append((score, path))

    related.sort(key=lambda t: (-t[0], str(t[1])))
    return [p for _, p in related[:k]]


def repo_overview(repo_root: Path) -> str:
    """First H1+paragraph of CLAUDE.md, or a fallback."""
    claude = repo_root / "CLAUDE.md"
    if claude.exists():
        text = claude.read_text()
        match = re.match(r"^#\s+(.+?)\n\n(.+?)(?:\n\n|\Z)", text, re.DOTALL)
        if match:
            return f"**{match.group(1).strip()}.** {match.group(2).strip()}"
        return text.split("\n\n", 1)[0].strip()[:500]
    return "(no CLAUDE.md found — repo overview unavailable)"


def truncate_middle(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    head = max_chars // 2 - 20
    tail = max_chars - head - 40
    return (
        text[:head]
        + f"\n\n... [TRUNCATED {len(text) - head - tail} chars] ...\n\n"
        + text[-tail:]
    )


def render_file_section(repo_root: Path, rel_path: str,
                        char_budget: int) -> tuple[str, int]:
    """Return (markdown_block, chars_used)."""
    full = repo_root / rel_path
    header = f"\n### `{rel_path}`\n\n"
    if not full.exists():
        body = "_(file does not exist in working tree — deleted by this diff)_\n"
        out = header + body
        return out, len(out)
    try:
        text = full.read_text()
    except UnicodeDecodeError:
        body = "_(binary file — contents omitted)_\n"
        out = header + body
        return out, len(out)

    fenced_overhead = 20
    body_budget = max(200, char_budget - len(header) - fenced_overhead)
    body = truncate_middle(text, body_budget)
    lang = full.suffix.lstrip(".") or ""
    out = f"{header}```{lang}\n{body}\n```\n"
    return out, len(out)


def build_bundle(repo_root: Path, diff_text: str, max_tokens: int) -> str:
    char_budget = max_tokens * CHARS_PER_TOKEN

    changed = parse_diff_paths(diff_text)
    related = find_related(repo_root, changed, TOP_RELATED)

    sections: list[str] = []
    sections.append("# Repo context bundle\n")
    sections.append("\n## Overview\n\n" + repo_overview(repo_root) + "\n")

    sections.append("\n## Changed files\n\n"
                    + ("\n".join(f"- `{p}`" for p in changed) if changed
                       else "_(no changed files parsed from diff)_") + "\n")

    used = sum(len(s) for s in sections)

    if changed:
        sections.append("\n## Changed files — full post-diff contents\n")
        used += len(sections[-1])
        per_file_budget = max(500, (char_budget - used) // max(1, len(changed) + len(related)))
        for path in changed:
            block, n = render_file_section(repo_root, path, per_file_budget)
            sections.append(block)
            used += n
            if used >= char_budget * 0.85:
                sections.append("\n_(remaining changed files omitted — token budget)_\n")
                used += 60
                break

    if related and used < char_budget * 0.9:
        sections.append("\n## Related files (heuristic — directory-siblings + name-prefix)\n")
        used += len(sections[-1])
        remaining = max(500, char_budget - used)
        per_related = max(300, remaining // max(1, len(related)))
        for path in related:
            rel = str(path.relative_to(repo_root))
            block, n = render_file_section(repo_root, rel, per_related)
            sections.append(block)
            used += n
            if used >= char_budget * 0.95:
                sections.append("\n_(remaining related files omitted — token budget)_\n")
                used += 60
                break

    bundle = "".join(sections)
    tokens_used = approx_tokens(bundle)
    footer = (
        f"\n---\n_Bundle stats: ~{tokens_used} tokens "
        f"(budget {max_tokens}); {len(changed)} changed file(s), "
        f"{len(related)} related file(s)._\n"
    )
    return bundle + footer


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diff", default=None,
                        help="Path to a unified diff file. Default: read stdin.")
    parser.add_argument("--demo", action="store_true",
                        help="Run against fixture_diff.patch + write to "
                             "sample_bundle.md")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument("--repo-root", default=None,
                        help="Path to repo root (default: two parents up)")
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    repo_root = (Path(args.repo_root).resolve() if args.repo_root
                 else here.parent.parent)

    if args.demo:
        fixture = here / "fixture_diff.patch"
        if not fixture.exists():
            print(f"ERROR: {fixture} not found", file=sys.stderr)
            return 2
        diff_text = fixture.read_text()
        bundle = build_bundle(repo_root, diff_text, args.max_tokens)
        out = here / "sample_bundle.md"
        out.write_text(bundle)
        print(f"Wrote {out} ({len(bundle)} chars, ~{approx_tokens(bundle)} tokens)")
        return 0

    diff_text = (Path(args.diff).read_text() if args.diff
                 else sys.stdin.read())
    if not diff_text.strip():
        print("ERROR: no diff input", file=sys.stderr)
        return 2

    sys.stdout.write(build_bundle(repo_root, diff_text, args.max_tokens))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Council

Each `*.md` file in this directory (other than this README and `lead-architect.md`) defines a reviewer persona. The Gemini runner (`../scripts/council.py`) dispatches them in parallel and then runs the Lead Architect synthesis.

## Active angles (template defaults)

| File | Role |
|------|------|
| `architecture.md` | Architecture Reviewer |
| `security.md` | Security Reviewer |
| `bugs.md` | Bug Hunter |
| `cost.md` | Cost Reviewer |
| `product.md` | Product Reviewer |
| `accessibility.md` | Accessibility Reviewer |
| `maintainability.md` | Maintainability Reviewer |
| `lead-architect.md` | Resolver — synthesizes the above into one verdict |

## Specializing for this repo

Each persona file is a generic skeleton with a `yolo-projects` token (substituted at `harness init` time). After init, **edit each persona's `## Scope` section** to describe the actual surface of this repo: what modules exist, what contracts matter, what the threat model is, what the cost drivers are. Generic personas produce generic critiques. Specialized personas catch real bugs.

## Adding a new angle

1. Create `<angle>.md` in this directory following the persona shape in any existing file:
   - One-sentence role statement.
   - Scope list.
   - Review checklist (numbered questions).
   - Output format (fenced block with `Score:` on its own line).
2. The runner auto-picks it up — no code change.
3. Append the entry to the table above.

## Removing an angle

Delete the file. The runner skips it on the next invocation.

## Disabling an angle temporarily

Rename to `<angle>.md.disabled`. The runner only loads files ending in `.md`.

## Cost cap

The runner enforces 15 Gemini calls per run (hard). Adding a new angle eats one of those slots.

## Style invariants for new personas

- No emojis.
- Always include non-negotiables that grant veto power (so the Lead Architect knows when to reject).
- Keep the checklist actionable — questions, not lectures.
- Output format must be machine-parseable (fenced block with `Score:` on its own line so the log can extract it).
- For axes that don't apply to a particular diff type, score **10** with "No impact for this diff type" — never 1–2.

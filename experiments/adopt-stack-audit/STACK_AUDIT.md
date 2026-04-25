# YOLO-Projects Pipeline — Stack Audit
**Snapshot date:** 2026-04-25  
**Re-derive with:** the grep commands in each row. If a cited grep returns zero matches, the row is stale.

---

## 1. Installable Python Packages

Locate: `grep -nE "pip install" .github/workflows/*.yml`

| Package | Installed in | Current "version" | Deprecation horizon | Coupling depth | Replacement plan |
|---|---|---|---|---|---|
| `anthropic` | `tick_tock.yml:37`, `daily_research.yml:59` | latest-at-install (no pin) | **stable** | medium — SDK construction in `council.py:553`; fallback path to Claude Haiku | Pin a version; N/A for deprecation |
| `google-generativeai` | `tick_tock.yml:37` | latest-at-install (no pin) | **3mo** — actively deprecated; FutureWarning fires on every import (`council.py:77`) | medium — SDK used in `council.py:77,232,540,542` across `genai.configure`, `genai.GenerativeModel` call | Migrate to `google-genai` (`pip install google-genai`); requires rewriting the 4 call sites in `council.py` |
| `requests` | `tick_tock.yml:37` | latest-at-install (no pin) | **stable** | **zero** — `grep -rn "^import requests\|^from requests" --include="*.py" .` returns empty; package is installed but never imported | Remove from `pip install` line in `tick_tock.yml` — no code change needed |

### Pip version-pinning gap + supply chain risk
None of the three packages are pinned to a version in the workflow. A breaking release (e.g., `anthropic` v2, `google-generativeai` final EOL) would silently upgrade and potentially break the next cron run. More critically, **unpinned packages are a supply chain risk**: a compromised or typosquatted release could be installed automatically on the next cron run without any diff to review.  
**Action:** Pin with `==` or `~=` for all three packages in both workflow files. For `google-generativeai`, pin while migrating to `google-genai`.

Verify current latest versions with `pip index versions <package>` before pinning.

---

## 2. npm Package

Locate: `grep -nE "npm install" .github/workflows/*.yml`

| Package | Installed in | Current version | Deprecation horizon | Coupling depth | Replacement plan |
|---|---|---|---|---|---|
| `@anthropic-ai/claude-code` | `tick_tock.yml:40` (`npm install -g`) | latest-at-install (no pin) | **stable** — core Anthropic product, actively developed | **deep** — the entire tick-tock agent (Claude Code CLI) is the backbone of the YOLO build loop; every gate invocation goes through it | No replacement; pin a version for stability |

---

## 3. GitHub Actions Marketplace Actions

Locate: `grep -nE "uses: [^@]+@" .github/workflows/*.yml`

| Action | Used in | Pinned version | Deprecation horizon | Coupling depth | Replacement plan |
|---|---|---|---|---|---|
| `actions/checkout@v4` | `tick_tock.yml:22`, `daily_research.yml:19` | v4 | **stable** — maintained by GitHub | shallow — standard checkout step | Bump to v5 when released |
| `actions/setup-node@v4` | `tick_tock.yml:27` | v4 | **stable** — maintained by GitHub | shallow — one step, configure node version | Bump to v5 when released |
| `actions/setup-python@v5` | `tick_tock.yml:32`, `daily_research.yml:22` | v5 | **stable** — maintained by GitHub | shallow — one step, configure python version | N/A — already v5 |
| `stefanzweifel/git-auto-commit-action@v5` | `daily_research.yml:108` | v5 | **stable** — widely used community action | shallow — only in `daily_research.yml`; `tick_tock.yml` uses raw `git` commands instead | N/A — already v5; or replace with raw `git` (like tick_tock does) |

---

## 4. Runtime Versions

Locate: `grep -nE "(node|python)-version:" .github/workflows/*.yml`

| Runtime | Pinned version | Used in | Deprecation horizon | Coupling depth | Replacement plan |
|---|---|---|---|---|---|
| Python 3.12 | `3.12` | `tick_tock.yml:34`, `daily_research.yml:24` | **stable** — LTS until Oct 2028 | medium — all pipeline Python scripts run under 3.12 | Bump to 3.13+ when EOL approaches |
| Node.js 20 | `20` | `tick_tock.yml:29` | **3mo / critical** — Node 20 entered maintenance Apr 2024; End of Life **2026-04-30** (5 days from snapshot date). Node 22 is current LTS. | shallow — used only to install `@anthropic-ai/claude-code` globally | **Upgrade to `node-version: '22'`** in `tick_tock.yml:29` before 2026-04-30 |

> **Urgent:** Node 20 goes EOL on 2026-04-30, five days after this audit. The change is one line: `node-version: '20'` → `node-version: '22'` in `.github/workflows/tick_tock.yml`.

---

## 5. Hardcoded Model Names

Locate: `grep -nE "^(MODEL_NAME|CLAUDE_MODEL)\s*=" council.py`

| Constant | Model string | File | Deprecation horizon | Coupling depth | Replacement plan |
|---|---|---|---|---|---|
| `MODEL_NAME` | `"gemini-2.5-flash"` | `council.py:90` | **12mo** — Gemini model generations rotate; flash models typically have 1-2 year availability windows | **deep** — primary council backend; retry logic, prompt formatting, and fallback paths all assume this model's behavior | Monitor Google AI model deprecation notices; bump to `gemini-2.5-flash-latest` or next generation |
| `CLAUDE_MODEL` | `"claude-haiku-4-5-20251001"` | `council.py:91` | **12mo** — Anthropic model IDs with date stamps are versioned releases; typically 12-24mo support | medium — fallback path only, triggered when Gemini is unavailable; fewer call sites than primary | Bump to latest Claude Haiku model when this one is sunset; check `console.anthropic.com` for deprecation schedule |

> **Note:** Model names are pipeline dependencies even though they aren't installable packages. A model deprecation forces a code edit to `council.py`. The `google-generativeai` SDK deprecation (§1 above) and the `gemini-2.5-flash` model deprecation are separate risks that may arrive on different timelines.

---

## 6. External API Services (Runtime Dependencies)

These are not installable packages but are live dependencies — if unavailable, the pipeline halts.

| Service | Purpose | How it's used | Deprecation/availability risk | Coupling depth | Mitigation |
|---|---|---|---|---|---|
| **Anthropic API** | Powers Claude Code CLI (build agent) and fallback Haiku council calls | SDK construction: `grep -n "anthropic_sdk.Anthropic\|Anthropic(api_key" council.py`; secret: `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}` in both workflows | **stable** — Anthropic's core API product; no deprecation signal | **deep** — the build agent is Claude Code; without Anthropic API, no builds | Budget/quota monitoring; keep fallback model current |
| **Google Gemini API** | Primary council backend (7 angles × 4 gates per build) | SDK: `grep -n "genai\.configure\|genai\.GenerativeModel" council.py`; secret: `GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}` in `tick_tock.yml` only | **12mo** — underlying `google-generativeai` SDK is deprecated (3mo risk); Gemini API itself is stable but SDK migration is needed | **deep** — every council gate runs through Gemini; fallback to Haiku only | Migrate SDK to `google-genai` to resolve the FutureWarning and ensure continued support |
| **GitHub Actions platform** | Hosts cron scheduling, runner provisioning, `git push` integration | Entire `.github/workflows/tick_tock.yml` and `.github/workflows/daily_research.yml` are the dependency surface | **stable** — no credible risk; GitHub Actions is GitHub's core CI/CD offering | **deep** — all builds run on GitHub-hosted runners; git push back to main requires GitHub | Self-hosted runners as fallback (significant effort); no urgent action needed |
| **YouTube RSS** | Ingests new video metadata for Phase 4 experiment discovery | Network call: `grep -n "youtube\.com/feeds\|urllib\.request" fetch_youtube_rss.py`; invocation: `grep -n "fetch_youtube_rss" .github/workflows/daily_research.yml` | **stable** — YouTube RSS feeds are unauthenticated and have been stable for years; no auth token means no credential rotation risk | shallow — isolated to `fetch_youtube_rss.py` and `daily_research.yml`; failure only affects ingestion, not builds | **Security note (LLM prompt injection):** `fetch_youtube_rss.py` parses RSS XML with regex and writes title/video_id values directly into `experiments.json`, which is subsequently read into LLM prompts by `council.py`. YouTube controls this data — a crafted video title could inject instructions into the LLM's context window ("ignore previous instructions…"). Risk is low (YouTube moderation, no auth), but titles are not HTML/XML-escaped or stripped before storage. Mitigation: `parse_entries()` in `fetch_youtube_rss.py` should apply `html.unescape()` to extracted text fields and verify `video_id` matches `[a-zA-Z0-9_-]{11}` before storing; see `infra-rss-sanitize` follow-up tick. |

---

## 7. What We Do NOT Depend On

The 231 single-file HTML YOLO tools in the portfolio are the **lowest-coupling pattern** in the entire stack:

- **Zero npm/pip dependencies** — every tool is a standalone HTML file with inline CSS and vanilla JS
- **Zero build step** — no bundler, no transpiler, no framework lock-in
- **Zero server** — runs from `file://` in any browser; no hosting dependency
- **Zero API calls** — tools are computation-only; no external services
- **Deployment surface** — a file copy; `git push` to GitHub Pages suffices

This is the anti-fragile core of the portfolio. A tool built today in 2026 will open in a browser in 2036 without modification. The entire pipeline stack above exists to *produce* these tools, but the tools themselves carry none of the pipeline's coupling risk.

---

## Summary: Risk Register

| Item | Risk level | Urgency | Action |
|---|---|---|---|
| Node.js 20 EOL (2026-04-30) | **CRITICAL** | **Immediate (5 days)** | Change `node-version: '22'` in `tick_tock.yml:29` — running EOL runtimes means no security patches |
| `google-generativeai` SDK deprecated | **HIGH** | Within 3mo | Migrate `council.py` to `google-genai` package; FutureWarning fires every run |
| No pip version pins (supply chain risk) | **HIGH** | Next maintenance window | Pin all packages with `==` in both workflow files to prevent silent upgrades |
| No npm version pin (`@anthropic-ai/claude-code`) | **HIGH** | Next maintenance window | Pin `@anthropic-ai/claude-code` to a specific version in `tick_tock.yml` npm install; unpinned global installs carry the same silent-upgrade supply chain risk as pip packages |
| YouTube RSS → LLM prompt injection | **medium** | Low | Add `html.unescape()` + video_id regex validation in `fetch_youtube_rss.py:parse_entries()` to prevent crafted titles from injecting instructions into council LLM context |
| `requests` installed but unused | low | Low | Remove from `tick_tock.yml:37` pip install |
| `CLAUDE_MODEL` haiku date-stamp | low | 12mo | Monitor Anthropic model deprecation notices |
| `MODEL_NAME` gemini-2.5-flash | low | 12mo | Monitor Google AI model lifecycle |
| All other entries | — | No action | Stable, no foreseeable risk |

---

## Recommended Follow-Up Ticks

This audit is a **snapshot document**, not a remediation. Each high-risk row above is proposed as its own follow-up tick so production-affecting changes go through their own approval gate (per `feedback_approval_gate.md`):

| Proposed tick name | Risk addressed | Scope (one-line) |
|---|---|---|
| `infra-node-22-upgrade` | Node.js 20 EOL | Change `node-version: '20'` → `'22'` in both workflow YAMLs; verify `@anthropic-ai/claude-code` installs cleanly on Node 22 |
| `infra-genai-migration` | `google-generativeai` deprecation | Replace `import google.generativeai as genai` with `from google import genai`; rewrite the four `genai.*` call sites in `council.py` |
| `infra-pip-pinning` | unpinned pip-package supply chain risk | Add `==` version pins for `anthropic`, `google-generativeai` (or successor), and any other pip packages; document the pinning convention in `learnings.md` |
| `infra-npm-pinning` | unpinned npm-package supply chain risk | Add `@<version>` pin for `@anthropic-ai/claude-code` in the `npm install -g` step in `tick_tock.yml`; prevents silent major-version upgrades |
| `infra-rss-sanitize` | YouTube RSS → LLM prompt injection | Apply `html.unescape()` to extracted titles in `fetch_youtube_rss.py:parse_entries()`; assert `video_id` matches `^[a-zA-Z0-9_-]{11}$` before storing |
| `infra-prune-unused-deps` | unused `requests` package | Remove `requests` from the `pip install` line in `tick_tock.yml`; smoke-test the next cron run for any latent import |

Each follow-up should be its own queue entry with its own PLAN/IMPL/TESTS/OUTCOME gates. Bundling them into this audit would conflate "identify" with "remediate" and obscure the audit's role as a dated reference snapshot.

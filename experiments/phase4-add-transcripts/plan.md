# Plan: phase4-add-transcripts

## Goal
Improve Phase 4 card quality by feeding video transcripts (not just titles)
into the LLM card-generator. Today every experiment description is the
LLM's guess from the title alone; this tick gives it the actual content.

## Scope

**In:**
- Modify `fetch_youtube_rss.py` to optionally pull auto-generated YouTube
  captions via `yt-dlp --write-auto-sub --sub-format vtt --skip-download`.
- Add `transcript` field to the per-video JSON output (string or null).
- Modify `scripts/process_experiments.py` to inject `transcript` into the
  card-generation prompt when present.
- On-disk transcript cache at `phase4_cache/transcripts/<video_id>.vtt` so
  re-runs don't re-fetch.
- Truncate transcripts to 10,000 characters (head + tail) before sending
  to the LLM. Captions for an hour-long video are ~12K-15K chars; keeping
  the first 6K + last 4K keeps the intro hook + the "what we built / what
  to do next" tail that's where actionable content tends to live.
- Update `.github/workflows/daily_research.yml` to install yt-dlp.

**Out:**
- Whisper / speech-to-text fallback for captionless videos. Documented as
  a follow-on (`phase4-add-whisper-fallback`). Most tracked channels have
  auto-captions; the few that don't are an acceptable miss for v1.
- Re-processing of historical videos. Forward-only.
- Transcript-based smarter classification (skip rules currently key off
  title; could key off transcript). Out of scope; let the LLM use the
  transcript through the existing prompt.

## Approach

### Why captions, not whisper, for v1
Captions are free, fast (single yt-dlp call, ~2s per video), and YouTube
auto-generates them for ~95% of channels we track. Whisper adds API cost
($0.006/min × ~22 hr/month = $8/month), latency, and a binary dependency.
The captions-only baseline lets us measure whether transcripts even matter
before we pay for the harder cases.

### Why head+tail truncation
Captions for a 60-minute video are ~12K-15K chars at ~200 chars/min.
Sending all of that to the card generator inflates token cost ~10x and
mostly fills the prompt with mid-roll filler. Head (first 6K) captures the
hook / problem statement; tail (last 4K) captures conclusions / "try this
yourself" callouts. Validate empirically — first cycle's data tells us
whether the truncation strategy throws away signal.

### Failure modes
- yt-dlp unavailable / wrong version → log warning, set `transcript: null`,
  card generator falls back to title-only behavior. **Backwards-compatible
  by default.**
- Caption file missing for a video → same null fallback.
- yt-dlp times out (default 30s) → log, fallback.
- Cached vtt corrupt / truncated → log, re-fetch once, then fallback.

## File Layout
- `experiments/phase4-add-transcripts/plan.md` — this file.
- `experiments/phase4-add-transcripts/README.md` — written after build.
- `fetch_youtube_rss.py` — add `--with-transcripts` flag and the
  yt-dlp invocation. ~40 LOC added.
- `scripts/process_experiments.py` — add transcript section to the
  prompt; preserve title-only path when transcript is null. ~20 LOC added.
- `phase4_cache/transcripts/.gitkeep` — directory for vtt cache (add
  `phase4_cache/transcripts/*.vtt` to `.gitignore`).
- `.github/workflows/daily_research.yml` — install yt-dlp step.
- `experiments/phase4-add-transcripts/baseline_vs_transcript_diff.md`
  — written after the first cron run with transcripts enabled. Shows
  card-quality delta on the same N videos.

## Function Map
- `fetch_youtube_rss.py::fetch_transcript(video_id) -> str | None` — new.
- `fetch_youtube_rss.py::truncate_transcript(text, head=6000, tail=4000) -> str`
  — new.
- `fetch_youtube_rss.py::main()` — gate transcript fetch behind a CLI flag.
- `scripts/process_experiments.py::generate_cards_via_api()` — extend
  the user prompt to include the transcript section when present.

## Security
- yt-dlp is a third-party binary. Pin to a specific version in the workflow
  (`pip install yt-dlp==<latest-stable>`) to avoid supply-chain drift.
- Transcripts are public YouTube captions — no auth, no PII concerns.
- Cache directory is gitignored; transcripts never enter the repo.
- The new prompt content is treated as untrusted user input by the
  card-generator (already enforced — Claude treats user-message content
  as data, not instructions).

## UI / Guide
Not applicable: ingestion infrastructure.

## Edge Cases
- **Captions disabled on the channel** → null transcript, fallback to
  title-only. Logged.
- **Multi-language captions** → prefer `en`, then `en-auto`, then any.
  Document the priority in code comment.
- **Live-stream archive** → captions can be incomplete or arrive late;
  retry once on next cron rather than treating as permanent miss.
- **Very short videos (< 60s)** → transcript will be tiny; truncation
  is a no-op; should still help (Shorts often have surprisingly dense
  hooks).

## Test Strategy
- Unit: `truncate_transcript` with a synthetic 20K-char input → check
  head+tail composition and total length.
- Integration: run `fetch_youtube_rss.py --with-transcripts` against the
  10 most recent videos in the cache → confirm transcripts populated
  for ≥7 of them (auto-captions coverage).
- End-to-end: run the modified `process_experiments.py` against 5
  historical videos with their transcripts → manually inspect the
  resulting cards. Look for:
  - Hypothesis/what_they_did fields drawing from transcript content
    rather than guessing from title.
  - No regression in card structure or required fields.
  - Reasonable behavior on a captionless video (graceful degrade).
- Cost: budget ~$1 for the validation runs.

## Estimated effort
~3-4 hours of build + validation. Single tick.

## Council focus
- **PLAN**: is the head+tail truncation the right shape, or should we
  use chunked summarization? (Chunked summarization is a much bigger
  scope; head+tail is the cheaper first cut.)
- **IMPLEMENTATION**: does the yt-dlp call timeout cleanly when
  captions are unavailable? Is the cache invalidation correct?
- **TESTS**: end-to-end test produces visibly better cards on at least
  3 of 5 sample videos, judged by a quick manual eyeballing.
- **OUTCOME**: written `baseline_vs_transcript_diff.md` showing
  side-by-side cards (title-only vs title+transcript) for the first 5
  videos after rollout. Shipped if the diff is meaningfully better;
  iterate if mixed; rollback to title-only if worse.

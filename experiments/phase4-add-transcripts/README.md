# phase4-add-transcripts

**Status:** Implemented 2026-04-30 on branch `claude/phase4-ingest-scopes`.
Built directly without going through the tick queue (per explicit user
instruction).

Source plan at `experiments/phase4-add-transcripts/plan.md`.

## What changed

### `fetch_youtube_rss.py`
- Added `--with-transcripts` CLI flag (off by default — backwards-compatible).
- New `fetch_transcript(video_id)` calls `yt-dlp --write-auto-sub --skip-download --sub-lang en,en-US,en-auto`.
- New `_strip_vtt(text)` removes VTT headers, timestamps, and inline cue tags; collapses *consecutive* duplicate lines (handles rolling-karaoke captions without losing legitimate repeats).
- New `truncate_transcript(text, head=6000, tail=4000)` keeps the first 6K + last 4K chars when content exceeds the budget. Hook + conclusion preserved; mid-roll filler dropped.
- VTT cache at `phase4_cache/transcripts/<video_id>.vtt` (gitignored). Re-runs are free.

### `scripts/process_experiments.py`
- The card-generator prompt now embeds a `TRANSCRIPT` block per video when present, with a directive: "When a transcript is present, base hypothesis and what_they_did on the transcript content, NOT on the title alone."
- When transcripts are absent for all videos, the prompt explicitly says so and falls back to title-only inference.
- Channel shortcode list extended with `@AndrejKarpathy=ak` and `@Mark_Kashef=mk`.

### `.github/workflows/daily_research.yml`
- Installs `yt-dlp>=2026.03.17` alongside `anthropic`.
- Cron now invokes `fetch_youtube_rss.py --with-transcripts`.
- `phase4_run.json` gains three fields: `with_transcripts`, `transcripts_fetched`, `transcripts_missing`.

### `.gitignore`
- Adds `phase4_cache/transcripts/*.vtt` so cached caption files don't pollute the repo.

## Failure modes (all degrade to title-only)

- yt-dlp not installed → caught at subprocess.FileNotFoundError → null transcript.
- Captions disabled on the channel → yt-dlp exits non-zero with no .vtt → null transcript, warning logged.
- Network/timeout → null transcript, warning logged.
- Cached VTT corrupt → re-fetched once, then null on second failure.

The card generator handles `transcript: null` identically to today's behavior, so no regression risk.

## Tests run

- Unit: `truncate_transcript` (short text unchanged, long text head+tail composition).
- Unit: `_strip_vtt` (rolling-karaoke dedup, non-consecutive duplicate preservation, header / timestamp / cue-tag removal).
- Integration (cache hit): pre-seeded a VTT, called `fetch_transcript`, got the expected stripped plain text.
- Integration (no transcript flag, all 12 channels): 12 feeds successful, 0 failed, `with_transcripts=False` plumbed through correctly.
- Live `yt-dlp` fetch: blocked in this sandbox (TLS-inspection proxy), but CI has no such proxy. The graceful-degrade path was exercised by the failure.

## Verification in CI

The next scheduled cron run should produce:
- `phase4_run.json.transcripts_fetched > 0` (most channels have auto-captions).
- Resulting cards' `hypothesis` and `what_they_did` fields visibly drawing from transcript content.

If `transcripts_fetched == 0` after one cron cycle, that's the signal to investigate (most likely cause: yt-dlp version mismatch in the runner).

## Cost estimate

- yt-dlp transcript fetch: free.
- Larger Anthropic prompt: head+tail truncation caps each transcript at ~10KB. With ~5 new videos per cron run × 10KB extra per video × $3/MTok input = ~$0.0002/run. Negligible.

## Whisper fallback (deferred)

For captionless channels (rare), a follow-on tick `phase4-add-whisper-fallback` is documented in the plan. Whisper would call `yt-dlp` to grab audio + an STT API. Scope: ~$8/month at full coverage.

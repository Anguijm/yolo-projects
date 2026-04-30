# Lessons — model-routing-bench

## Cycle 1 (baseline + classifier inspection)
**Tried:** Baseline benchmark (single vs routed), per-task classifier
inspection, edge cases (empty, super-short, mixed-keyword prompts).

**Learned:**
- Routed beat single 0.853 vs 0.733 — but the score function is
  literally a stub that rewards class-match, so this is a self-fulfilling
  result. *Real model APIs are needed to know if routing actually wins.*
- **The long-context classifier is broken.** Both `long-1` and `long-2`
  (each containing ~3KB of placeholder text — under the 8000-char gate)
  fall through to the *reasoning* fallback rather than `long_context`.
  The 8000-char threshold is too high for the test data; either lower
  it or add a different signal (e.g., presence of "summarize" /
  "extract" keywords).
- **Edge case: empty prompt** classifies as `simple` (length-based).
  That's probably wrong — empty prompts should error, not route.
- **Mixed code+reasoning** ("Implement a function that explains why")
  classifies as `code` because CODE_HINTS are checked before
  REASONING_HINTS. The order is arbitrary; either model might be a
  better choice depending on which aspect dominates.

**Change for cycle 2:**
- Lower the long-context threshold to 4000 chars OR add keyword
  signals ("summarize", "extract", "from this document").
- Reject empty prompts in `classify` (raise ValueError) so routing
  never silently picks haiku for an empty input.
- Score the classifier separately from the routing benchmark: a
  per-task expected_class field in tasks.json so accuracy of the
  classifier is its own metric.

## Cycle 2 (long-context fix + empty raises)
**Tried:** classify() on every task + edge cases; long-context detection with new keyword path.
**Learned:** long-2 (which says "Extract the key entities") now correctly routes to long_context. long-1 (which says "Summarize this document" — also a keyword) DOES match and routes correctly too. Wait, looking at log: long-1 says "Summarize this document in one sentence" and was classified as `reasoning (default fallback)` — so the keyword regex isn't matching "Summarize". Issue: regex is `\b(summarize|...)\b` — should match. Probably the prompt length test fires first (>500 chars but <4000): "matched long-context keywords + length>500" requires len > 500. long-1 length: ~3060 chars including the placeholder. So it should match. Investigation: the keyword regex uses `` word boundaries; "Summarize" capitalized — re.IGNORECASE handles that. Still broken. Will debug in cycle 3.
**Change for cycle 3:** Debug why long-1 ("Summarize this document...") falls through. Suspect: the prompt has trailing text including "Summarize this document in one sentence." but the placeholder text comes BEFORE. Maybe the length>500 check fires before the keyword check is reached because the placeholder pushes len > 4000 — wait, length is 3060, that's <4000. Oh the prompt was "PLACEHOLDER_LONG_DOCUMENT___..." x N. Let me look. Actually: long-1's prompt > 4000 chars. So it hits "prompt is X chars (>4000)" — that route exists. Why didn't it? Re-check.

## Cycle 3 (long-1 fall-through diagnosed)
**Tried:** Inspected long-1's prompt structure and length.
**Learned:** **Real bug found.** long-1's prompt length is 1054, not 4000+. The keyword regex `\bsummarize\b` doesn't match because the prompt is `..._UVWXYZ___Summarize this document...` — there's no word boundary between `_` (which IS a word character in regex) and `S`. The `\b` only fires between word and non-word chars. Underscore-bounded keywords are silently invisible to the classifier.
**Change for cycle 4:** Replace `\b` with explicit `(?:^|[^a-zA-Z0-9])` boundary, OR strip non-letter chars before applying the regex. Real-world prompts will have markdown punctuation around keywords, so this matters beyond the synthetic test data.

## Cycle 4 (regex boundary fix verified)
**Tried:** Re-classified all 12 tasks after replacing `\b` with explicit non-letter boundaries.
**Learned:** **Real fix landed.** long-1 (which was falling through to 'reasoning' default) now correctly classifies as 'long_context'. long-2 still works. The underscore-boundary regex bug is gone. This is the cycle that produced an actual production-quality bug fix, not just instrumentation.

## Cycle 5 (final smoke)
**Result:** Classifier accuracy 11/11 on the labeled task subset. The underscore-boundary regex fix landed clean. Verdict: **iterate** — orchestration and classifier are production-quality; benchmark numbers need real model API keys to be meaningful.

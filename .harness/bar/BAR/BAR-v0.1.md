# Bar: what perfect looks like for yolo-projects

Written 2026-10-22 (JST) at John's standing order, relayed by ops: "I need you to know exactly what perfect looks like.
And I don't want to have to explain it every time... go find out what perfect would look like for that session, and
make them keep trying till [they] meet that bar." Template: `~/ops/BAR.md`. Nothing from this project reaches John
until it passes sections 4 and 5. Labels: FACT (read in a named source), Assessment (my judgment), Unverified.

This project delivers five things:
1. **PDF to CSV**: the built page, its guide and its prompt series, published from `~/projects/pdf-to-csv`.
2. **Markdown Deck**: a single-file markdown-to-slides tool.
3. **Naval Scribe**: a single-file formatter for Navy letters (SECNAV M-5216.5) that exports .docx.
4. **Card reviews**: the daily verdicts on new cards in `.harness/card_reviews.md`, plus the proposals sent to John.
5. **Repo upkeep**: merges of other sessions' pull requests, the daily card script, and README, CLAUDE.md and status.md.

## 1. What perfect looks like (checkable by a stranger)

**Every flagship page**
- One HTML file that works when opened from disk (`file://`) with the network unplugged. It makes zero network
  requests, which a headless browser run counts, and it shows no console errors on load or in its main flow.
- It says what it could not do, in words, never silently. PDF to CSV writes problems.csv; the other two give
  visible warnings.
- It has a guide that a first-time user can follow, linked from the page or the README.
- The live copy is byte-identical to the build it came from.
- Every claim the README makes about it is true of the live page. No feature is listed that is not there.

**PDF to CSV**: each record is one row with named fields. Every guess is named in problems.csv with its reason.
Zero silent wrong values on every fixture set. The page states its limits, such as needing a text layer, and
says plainly that nothing leaves the computer. Nothing from John's real records appears anywhere in the public repo.

**Markdown Deck**: `---` splits slides the way Marp does, so a Marp deck pastes in and breaks in the same places.
It has a presenter view with notes, a timer and the next slide; an overview; keyboard navigation listed on the
page; and PDF export through print.

**Naval Scribe**: a letter it exports matches the manual's rules for margins, font, date, SSIC (Standard Subject
Identification Code) block, From/To/Via/Subj/Ref/Encl layout, paragraph numbering (1. a. (1) (a)), signature
block and second-page header. Each rule is checked in the .docx itself, not in the preview.

**Card reviews**: every new card gets one line within a day: date, id, verdict, the project it bears on and a
reason. Noise is said in one line. A proposal to John names the project, what would be built, the cost in time
and money, and whether ops has to say yes. He never has to ask "what does this mean for me".

**Repo upkeep**: one fact matches in every place it appears, changed in the same commit. Merged branches are
deleted. Nothing is pushed without his ask or a standing rule. Job-guard shows no false failures from this repo.

## 2. His words

John has given no explicit praise of the flagships in the October sources. What follows is everything found,
newest first. "Paraphrase" means the source records his ruling but not his exact words.

- 2026-10-22: one question, one channel: anything ops gates goes through ops only. [`~/.claude/CLAUDE.md`; `~/ops/log.md`]
- 2026-10-22: "It was supposed to be a dictation off night. Last night, too. That was the plan." A lost night delayed
  this project's benchmark. [`~/ops/log.md:199`]
- 2026-10-22: "I need you to know exactly what perfect looks like..." (this file). [ops relay]
- 2026-10-22: "Have yolo review and merge them" (the next-big-thing prompt PRs). [relay from next-big-thing]
- 2026-10-21: cost lanes. Scripted model calls use the home-jobs key per command; no model loops without ops.
  Paraphrase. [memory `claude-cost-lanes.md`]
- 2026-10-20: "free inference is free inference". [`~/ops/RUNBOOK.md:171`]
- 2026-10-20: "ok for the model test"; earlier the same day he parked it. [`.harness/card_reviews.md`]
- 2026-10-20: "2 - both things in a sensible sequence". [`.harness/card_reviews.md`]
- 2026-10-20: "direct the adversarial agents to actually be adversarial... Finish the 10 rounds". This was a
  correction after the critique loop stopped at 5 of 10 rounds. [`~/projects/pdf-to-csv/status.md:16`]
- 2026-10-20: "ask haiku, then Sonnet, then fable... repeat 10x". [`~/projects/pdf-to-csv/status.md:36`]
- 2026-10-20: "Go for v0.8.1, keep testing and improving"; "also ok" (v0.8 packets). [`~/projects/pdf-to-csv/status.md:51,60`]
- 2026-10-19: "We're not doing ticks and tocks any longer." Keep up the flagships and judge cards against his
  whole ecosystem; build nothing until he says go. [`CLAUDE.md`]
- 2026-10-19: he caught the README listing two flagships when there were three. That led to the rule "one fact,
  every place it appears, same commit". [`~/ops/log.md:113`; `~/.claude/CLAUDE.md`]
- 2026-10-19: "information flowing the wrong direction, so it's not gonna happen". No work data, not even field
  names, comes to this machine. [memory `no-work-data-inbound.md`]
- 2026-10-19: "I do want a usage guide written up in the github". [`~/projects/pdf-to-csv/status.md:9`]
- 2026-10-19: "Build 7 then publish". [`~/projects/pdf-to-csv/status.md:98`]
- 2026-10-19: his real-record report on v0.5.2 named six faults: label and value glued together, labels cut,
  headers merged across drawn lines, headers and footers inside values, sub-headings ending a box early, and
  repeated signature labels that could not be reached. Paraphrase. [`~/projects/pdf-to-csv/PLAN-v0.6.md:3-19`]
- 2026-10-19: "give field names, not clicks, so the tool works on any form". Paraphrase. [`~/projects/pdf-to-csv/status.md:255`]
- 2026-10-15: "also 3": widen card judging to his other projects. [git ef5d2f2]
- 2026-10-16: discard cards that are only someone selling a product. Paraphrase. [git 33ab6a0]
- 2026-06-11: "don't care about tick-tock". [git a2e2d4b]
- 2026-05-28: he overrode the Naval Scribe UI council objection as a false positive. Paraphrase.
  [`naval-scribe/COUNCIL_ESCALATION.md`]
- 2026-05-06: "kill the cron and just work when I want work done." [git 59fea25]
- About 2026-04: builds were "too simple and formulaic"; he wants ambition. He likes synthesizers, drum machines,
  developer tools and naval-scribe, and does not want visual toys. Paraphrase. [old memory `feedback_quality_bar.md`,
  `feedback_utility_focus.md`]
- About 2026-04: "shipped and ugly" over "planned and pretty". [old memory `user_profile.md`]
- 2026-03-30: Markdown Deck presentation features are "lowest priority per user". [`markdown-deck/deck_roadmap.md:67`]

Assessment: the October corrections share one theme. He wants the loop run in full ("finish the 10 rounds"), the
docs consistent ("two flagships when there were three"), and never to be asked twice.

## 3. Outside references (fetched and read 2026-10-22)

- **Camelot** (https://camelot-py.readthedocs.io/en/latest/), the bar for PDF to CSV.
  FACT: every table carries a `parsing_report` with accuracy, whitespace, order and page. FACT: it lets you "discard
  bad tables based on metrics like accuracy and whitespace". FACT: it states its limit up front: "only works with
  text-based PDFs and not scanned documents". Assessment: the bar is a quality figure per record, problems you can
  sort by severity, and limits stated before the user finds them.
- **Tabula** (https://tabula.technology/, https://github.com/tabulapdf/tabula). FACT: "Your PDF and the
  extracted data _never_ touch the net", with a way for the user to verify it. FACT: a command-line twin for
  batch jobs. Assessment: the offline claim should be one the user can test, not just one we make.
- **reveal.js** (https://revealjs.com/ and its speaker-view, pdf-export and markdown pages) and **Marp**
  (https://marp.app/), the bar for Markdown Deck. FACT: reveal.js has a speaker view (S key) with a timer, the
  next slide and notes; `Note:` lines in markdown; PDF export with notes; an ESC overview; stepped code
  highlighting. FACT: reveal.js needs a local web server to load an external .md file. FACT: Marp splits slides
  on `---`, exports to HTML, PDF and PowerPoint, and ships three themes. Assessment: reveal.js is the bar for
  presenting, Marp for syntax and export. Working from `file://` is an edge we can claim over reveal.js.
- **Simon Willison, "Useful patterns for building HTML tools"** (https://simonwillison.net/2025/Dec/10/html-tools/)
  and **tools.simonwillison.net/colophon**, the bar for single-file tools. FACT: a single file with inline JS and
  CSS, no build step, copy buttons, state in the URL. FACT: the colophon lists, for every tool, its source, its
  commit history and often the prompt that made it. Assessment: he loads libraries from a CDN, a content delivery
  network, which our offline rule forbids. Our version of the bar is "vendored, works unplugged" plus his provenance.
- **SECNAV M-5216.5**, the Navy correspondence manual and the bar for Naval Scribe. Unverified today: marines.mil,
  DTIC (Defense Technical Information Center) and secnav.navy.mil all refused a scripted fetch on 2026-10-22, with
  403 or an HTML wall. Gap: the rule list in section 1 comes from the tool's own README, not the manual. Next
  step: open the manual in the signed-in Chrome and write the rules out with paragraph numbers.

## 4. Measurable checks (pass or fail, run before anything reaches John)

| deliverable | check | how |
|---|---|---|
| any flagship page | 0 network requests, 0 console errors, loads from `file://` | headless Chromium (the pdf-to-csv `dev/` node setup), page opened from disk |
| PDF to CSV | full battery green: every packet set, 0 silent wrong values or cuts, old suites byte-identical, edge cases all pass | `bash dev/battery.sh dist/pdf-to-csv-vX.html OUT BASE` in `~/projects/pdf-to-csv` |
| PDF to CSV | live copy is byte-identical to `dist/` | `cmp` |
| PDF to CSV | no real record content in the public repo | `status.md` and `research/` never copied; grep of the published files for hull, job and name patterns |
| docs | no em dashes, acronyms expanded | `grep -c '—'` on every changed .md (0) |
| docs | one fact everywhere | `grep -n -i "<keyword>"` across README.md, CLAUDE.md and status.md for each changed fact |
| Naval Scribe | each manual rule checked in an exported .docx | unpack the .docx and check margins, font, sizes and numbering in `word/document.xml` (to build: see section 6) |
| Markdown Deck | the features listed in the README work in a headless run | scripted keypresses and screenshots (to build) |
| card reviews | every card id added since the last review has a line | script comparing `experiments.json` ids with `card_reviews.md` |
| merges | checks pass (council-script-check excepted by his ruling), branch deleted, local main matches origin | `gh pr checks`, `git ls-remote`, `git status -sb` |

## 5. The loop

Before anything goes to John (a new flagship version, a proposal from a card, a merged PR he will look at):
1. Run section 4. Any fail goes back to the builder; it is not reported as done.
2. A **fresh critic**, a subagent that did not make the work, gets only the output (renders, the built file or
   the text), the relevant reference from section 3, and section 1 of this file. It returns PASS or FAIL with the
   gap named. It is never shown the builder's reasoning or an earlier critic's verdict. For visual comparisons,
   use `~/mini-forge/tools/blind_pair.py` and keep the key from the critic, as in the mini-forge gauntlet-loop.
3. Fail means another round, with no fixed limit and no self-graded score. Each critic's verdict is saved in
   `.harness/bar/<deliverable>/round-N.md`, with a `~/bin/session-digest ... -o round-N-digest.md` at the end of each round.
4. If honest rounds cannot reach the bar, John gets the gap named ("presenter view missing; needs about 2 hours")
   instead of the weak version.
5. Model calls inside the loop follow the cost lanes. An interactive subagent is fine; any `claude -p` loop
   checks in with ops first.

## 6. Current gap (honest, 2026-10-22)

- **PDF to CSV: closest to the bar.** v0.8.11 is live after ten adversarial rounds; the battery is green with 0
  silent wrong values and 0 problems.csv rows on the normal set. Gaps against Camelot: no quality figure per
  record, and problems cannot be sorted by severity. The source checkout is 23 commits ahead of its private
  remote, with unpublished v0.8.10 and v0.8.11 builds in `dist/`, and `pdf-to-csv/README.md` does not yet link
  the five newer prompt files. No fresh-critic pass has been run on the live page against Camelot or Tabula.
- **Markdown Deck: unverified, and its README is wrong.** Last changed 2026-06-27 (Slide Sorter View). The code
  has presenter, notes, timer, overview and print paths (a grep of index.html finds presenter 36 times, notes 95,
  timer 68, `window.print` once). Its README still lists "Add speaker notes" and "Add PDF export" as wishes,
  which breaks "every README claim true". None of the features has been run headless against reveal.js's list.
  He ranked presentation features "lowest priority", so new features wait for his go. The README fix and the
  headless check do not need to wait.
- **Naval Scribe: unknown against the bar.** Last changed 2026-06-22. It has never been checked against the
  manual, and the manual could not be fetched today. Its README claims (margins, Times New Roman 12 pt, numbering)
  are untested in an exported .docx.
- **Card reviews: process, not quality, is the gap.** Every card since 2026-10-19 has a line. Verdicts have not
  had a fresh critic, and there is no script yet checking that every card has a line.
- **Repo upkeep: meets the bar today.** PRs #50 to #55 were merged with checks passing, branches deleted and
  README links added; main matches origin. One miss: `pdf-to-csv/README.md` lags (see above). Before today, the
  job-guard false failure (fixed in #50) reached John's alert list.
- **Not yet built from this file:** the Naval Scribe .docx checker, the Markdown Deck headless feature run, the
  card-coverage script and the `.harness/bar/` record folder. Each is small, CPU only, and none is started
  without his go.

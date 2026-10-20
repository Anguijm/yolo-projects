# Prompts for GenAI.mil: build the JCN analog estimator inside the enclave

Version 0.2, 2026-10-20. Tested against Gemini with no code execution before publishing: the v0.1 prompts
produced four mismatches between the pieces; v0.2 closes each of them by stating the contract more exactly.
In that test the assembled file opened with one error, fixed by one round of the Debug prompt, then ran.
A companion to GENAI-PROMPTS.md (the packet-structure prompts); this series builds a different tool, a
history-based estimator for new jobs.

Scope of this series: load exports, enter a new JCN, list the ten closest same-class past jobs with
reasons, build the phase-hours and material estimate from the ones you tick, write it out as CSV.
(Timing within the availability, the shop-by-week load grid and the emergent reserve are a second series.)

## How to use

1. Start ONE new chat. Pick a model (the series is written for Gemini, GPT or Grok). Run the prompts in
   order in that same chat; each later prompt refers to the file written earlier in it.
2. Each answer ends with one code block. Copy that block into Notepad (or any plain text editor).
   Prompt 1 gives the whole file; Prompts 2, 3 and 4 each give one `<script>` block that you paste over
   the matching placeholder line in the file. Prompt 5 checks the assembled file.
3. Save as `estimator.html` (plain text, UTF-8). Open it in the browser. Use the file picker on the page
   to choose your three exports. Nothing leaves the computer: the page has no network access by design.
4. If something fails, press F12, copy the red error text from the Console tab, and use the Debug prompt
   at the end. In the test here, one such round fixed the only error.

The prompts contain no record content. Your exports never go into the chat; they only go into the
browser page on your own computer.

---

## The contract (repeated inside every prompt so the pieces fit together)

Three CSV exports, identified by their columns, not their file names. After column mapping the page uses
these field names:

- `jcn_history`: jcn, job_summary, hull, ship_class, swlin, space, equipment_id, equipment_nomenclature, received_date
- `phases`: job_summary, phase_no, phase_title, shop, est_hours, charged_hours
- `material`: job_summary, phase_no (the end-use phase), item, qty

One global object `DB`: `DB.jcns` (array of jcn_history rows), `DB.phasesByJS` (plain object, job_summary
to array of phase rows), `DB.matByJS` (plain object, job_summary to array of material rows), `DB.jsCount`
(plain object, job_summary to the number of JCNs that share it, read as `DB.jsCount[job_summary]`),
`DB.hulls` (an array of [hull, ship_class] pairs, unique).

`readNewJCN()` returns exactly {hull, cls, swlin, space, eid, nom}. `findAnalogs(nj)` returns an array of
exactly {j, score, raw, reasons, note?} where j is a jcn_history row. Every function is a plain global
function declaration (no IIFE, no module, no `window.x =`); events are wired through arrow functions so a
later script block can replace a stub by declaring the same name again.

Functions: `parseCSV(text)`, `loadFiles(fileList)`, `buildDB(tables)`, `readNewJCN()`, `scoreJCN(nj, j)`,
`findAnalogs(nj)`, `renderAnalogs()`, `buildEstimate()`, `estimateCSV()`, `run()`, `setDownload()`.
Helpers: `$(id)`, `esc(s)`, `toDate(s)`, `fmtDate(d)`, `num(s)`, `csvCell(v)`.

Element ids: `files`, `datastatus`, `mapping`, `f-hull`, `f-swlin`, `f-space`, `f-eid`, `f-nom`, `btn-run`,
`weights`, `analogs`, `estnotes`, `estimate`, `material`, `csvout`, `btn-copy`, `btn-download`.

---

## Prompt 1: the page skeleton

```
I am building a small offline tool for a ship repair planning department. It is ONE self-contained HTML
file that runs in a browser on a work computer with no network access, no installation and no libraries.
You will build it with me in five steps. In this step, write only the skeleton: the page, its styling,
shared helper functions, and empty stub functions with exact names. Later steps fill the stubs in.

What the tool does: a planner loads three CSV exports from the maintenance system, types in a new job
(a JCN, job control number), and the tool lists the ten most similar past jobs with the reason each one
matched. The planner ticks the ones that are really the same kind of work, and the tool builds an
estimate from them: the phases of work, the hours by shop as low-to-high ranges (both what was estimated
and what was actually charged), and the material by the phase that uses it. The estimate can be copied
or downloaded as CSV.

Hard rules for the file:
- Plain HTML, CSS and vanilla JavaScript only. No frameworks, no CDN links, no fonts from the web, no
  fetch or XMLHttpRequest, no eval.
- Put this in the head so the browser enforces it:
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline';
  style-src 'unsafe-inline'; img-src data:; connect-src 'none'; form-action 'none'">
- Works in Edge and Chrome. Readable on a narrow window: sections stack in one column; tables scroll
  sideways inside their own container; a 16px side gutter; system font stack.
- Light and dark color schemes via prefers-color-scheme, using CSS variables for every color.
- No em dashes anywhere in text or comments.
- Reads files only through <input type="file" multiple>. Writes only through a download link and a
  textarea the user can copy from.
- Every function is a plain global function declaration at the top level of a script block. A later
  step replaces a stub by declaring a function of the same name in a later script block, so never wrap
  code in an IIFE or a module, and never assign functions to window.

The contract that every later step relies on (keep these names exactly):
- Three CSV exports, identified by their columns, not file names. After column mapping the page uses:
  jcn_history: jcn, job_summary, hull, ship_class, swlin, space, equipment_id, equipment_nomenclature,
  received_date; phases: job_summary, phase_no, phase_title, shop, est_hours, charged_hours;
  material: job_summary, phase_no (end-use phase), item, qty.
- One global object DB: DB.jcns (array of jcn_history rows), DB.phasesByJS (plain object, job_summary to
  array of phase rows), DB.matByJS (plain object, job_summary to array of material rows), DB.jsCount
  (plain object, job_summary to the number of JCNs sharing it, read as DB.jsCount[job_summary]),
  DB.hulls (an array of [hull, ship_class] pairs, unique).
- Global functions: parseCSV(text), loadFiles(fileList), buildDB(tables), readNewJCN(), scoreJCN(nj, j),
  findAnalogs(nj), renderAnalogs(), buildEstimate(), estimateCSV(), run().
- readNewJCN() returns an object with exactly these keys: hull, cls, swlin, space, eid, nom.
- findAnalogs(nj) returns an array of objects with exactly these keys: j (a jcn_history row), score,
  raw, reasons (array of strings).
- Element ids: files, datastatus, mapping, f-hull, f-swlin, f-space, f-eid, f-nom, btn-run, weights,
  analogs, estnotes, estimate, material, csvout, btn-copy, btn-download.

Write the skeleton now:
1. The page with these sections in order, each with a short heading: "1. Load exports" (file input id
   files, a status line id datastatus, an empty div id mapping), "2. New JCN" (a select id f-hull and text
   inputs f-swlin, f-space, f-eid, f-nom with labels, and a button id btn-run "Find similar jobs"),
   "3. Similar past jobs" (an empty div id weights, then an empty table id analogs), "4. Estimate" (an
   empty div id estnotes, an empty table id estimate, then a sub-heading "Material by end-use phase" and an
   empty table id material), "5. Export" (a textarea id csvout, a button id btn-copy "Copy CSV", a link
   id btn-download "Download estimate.csv"). Add one sentence under the title saying the page works
   offline and nothing leaves the computer.
2. Helper functions, fully written: $(id) returning the element; esc(s) for HTML escaping; toDate(s)
   that accepts YYYY-MM-DD, MM/DD/YYYY and DD-MON-YYYY and returns a Date or null; fmtDate(d) that
   returns YYYY-MM-DD or an empty string for null; num(s) that strips commas and returns a number or 0;
   csvCell(v) that quotes values containing commas, quotes or line breaks and prefixes a cell starting
   with = + - @ with an apostrophe unless it is a plain number.
3. The globals: let DB = null, let W = {} (weights, filled in step 3), let ANALOGS = [], let TICK = new
   Set(), let EST = null.
4. Stubs for every contract function that is not a helper, each one line, for example
   function loadFiles(fileList) { /* step 2 */ }.
5. Event wiring at the bottom, always through arrow functions that look the function up by name when
   the event fires, for example $('btn-run').addEventListener('click', () => run()), never
   addEventListener('click', run), because later steps replace the stubs. files change calls
   loadFiles(the file list); btn-run click calls run(); btn-copy copies csvout to the clipboard; and a
   global function setDownload() sets btn-download's href from csvout as a data: URL (later steps call
   it after filling csvout).
6. Mark where later steps go with three placeholder lines inside the body, after the main script:
   <!-- MODULE 2: data loading -->, <!-- MODULE 3: matching -->, <!-- MODULE 4: estimate -->.

Answer with the complete file in one code block and nothing after the block.
```

## Prompt 2: loading the exports and mapping columns

```
Continue the same file. Write MODULE 2: a single <script> block that I will paste over the line
<!-- MODULE 2: data loading -->. It replaces the stubs parseCSV, loadFiles and buildDB by declaring
plain global functions of the same names (no IIFE, no module, no assignment to window). Keep every name
in the contract from step 1 exactly.

Contract reminder: jcn_history: jcn, job_summary, hull, ship_class, swlin, space, equipment_id,
equipment_nomenclature, received_date; phases: job_summary, phase_no, phase_title, shop, est_hours,
charged_hours; material: job_summary, phase_no, item, qty. DB.jcns (array), DB.phasesByJS (plain
object), DB.matByJS (plain object), DB.jsCount (plain object, DB.jsCount[job_summary] = count),
DB.hulls (array of [hull, ship_class] pairs). Elements: files, datastatus, mapping, f-hull.

Requirements:
1. parseCSV(text): a real CSV parser, not split on commas: handles quoted fields, doubled quotes inside
   quotes, line breaks inside quotes, CRLF, and a leading byte-order mark. Returns an array of objects
   keyed by the header row, with header names trimmed.
2. loadFiles(fileList): reads each chosen file with FileReader as UTF-8, parses it, and decides which
   export it is from its columns: a file is jcn_history if it has a jcn column and an equipment column;
   phases if it has a phase title column and an estimated hours column; material if it has an item or
   part column and a quantity column. Matching is case-insensitive, ignores spaces, underscores and
   punctuation, and accepts these aliases for each field (extend them sensibly): jcn: jcn, job control
   number; job_summary: job summary, js, job summary number; hull: hull, ship, ship name; ship_class:
   class, ship class; swlin: swlin, swlin number; space: space, compartment, space number; equipment_id:
   equipment id, equipment, eqpt, eid, component; equipment_nomenclature: nomenclature, equipment
   nomenclature, description, noun name; received_date: received, received date, date received, jcn
   date; phase_no: phase, phase no, phase number, key op, keyop; phase_title: phase title, title, phase
   name, task; shop: shop, trade, work center; est_hours: estimated hours, est hours, planned hours,
   estimate; charged_hours: charged hours, actual hours, charged, expended hours; item: item, part,
   material, nsn, description; qty: qty, quantity.
3. For any required field that no column matches, do not fail: draw a small mapping row in div mapping
   with the file name, the field name, and a <select> of that file's columns; when the user picks one,
   use it and rebuild. Also list in datastatus which of the three exports are loaded and how many rows
   each has, and name any export still missing.
4. buildDB(tables): takes {jcn_history, phases, material} as arrays of mapped rows and builds DB.
   Normalize: trim strings; uppercase jcn, job_summary, hull, swlin, space, equipment_id, shop; phase_no
   and hours and qty through num(); received_date through toDate() kept as a Date (null if unreadable).
   DB.jsCount counts jcn rows per job_summary. DB.hulls is unique [hull, ship_class] sorted by hull.
   Then fill the f-hull select with one option per hull showing "hull (class)".
5. When all three exports are loaded and mapped, call buildDB, then enable btn-run. Before that,
   btn-run is disabled.
6. No em dashes. No network access.

Answer with the one <script> block only, starting with <script> and ending with </script>, and nothing
after it.
```

## Prompt 3: finding similar past jobs

```
Continue the same file. Write MODULE 3: a single <script> block that I will paste over the line
<!-- MODULE 3: matching -->. It replaces the stubs readNewJCN, scoreJCN, findAnalogs, renderAnalogs and
run by declaring plain global functions of the same names (no IIFE, no module, no assignment to window),
and it fills the global W. Keep every contract name exactly.

Contract reminder: DB.jcns rows have jcn, job_summary, hull, ship_class, swlin, space, equipment_id,
equipment_nomenclature, received_date (a Date or null). DB.hulls is an ARRAY of [hull, ship_class] pairs:
to find the class of a hull, find the pair whose first element equals the hull and take its second
element. DB.jsCount is a PLAIN OBJECT, read as DB.jsCount[job_summary] (not a Map, so never .get()).
Globals W, ANALOGS, TICK. Elements: f-hull, f-swlin, f-space, f-eid, f-nom, weights, analogs. Helpers
$(id), esc(s), fmtDate(d).
readNewJCN() returns an object with exactly these keys: hull, cls, swlin, space, eid, nom.
findAnalogs(nj) returns an array of objects with exactly these keys: j (the jcn_history row), score,
raw, reasons (array of strings), and optionally note (a string, for rows from another class).

How matching works (this is the planner's judgment, written as rules):
1. Ship class is a FILTER, not points. Only past jobs on the same class as the chosen hull are
   candidates. Other classes are shown only when the same class has fewer than W.minSame (default 5)
   candidates with a score above zero, and each such row gets note = "Other class (X): shown because
   <class> has only N".
2. Points within the class, all editable: same equipment ID 40 (W.eqId); else same equipment type 20
   (W.eqType), where the type is the text before the first hyphen of equipment_id, uppercased; else same
   system 5 (W.eqSys), where the system is the first character of swlin. Same hull as the new JCN adds 5
   (W.hull), so the ship's own history ranks first among equals. Space: same space 15 (W.space); else
   same deck and frame 8 (W.spaceDF), comparing the first two hyphen-separated parts of the space number;
   else same deck 2 (W.spaceDeck), the first part. SWLIN: same swlin 10 (W.swlin); else same first three
   characters 6 (W.swlinGrp); else same first character 2 (W.swlinSys).
3. Recency: multiply the points by 0.5 + 0.5 * exp(-age / W.recency), with age in years from
   received_date to today and W.recency = 3 (years). A job with no readable date gets age 10.
4. scoreJCN(nj, j) returns {score, raw, reasons} where reasons is an array of short plain-English
   strings such as "Same equipment ID", "Same equipment type (FMV)", "Same hull", "Same space", "Same
   SWLIN group 521", "2.3 years ago". Do not include a reason for things that did not match.
5. findAnalogs(nj) scores every DB.jcns row, drops raw == 0, applies the class filter and fallback above,
   and returns the top ten by score as {j, score, raw, reasons, note}.
6. readNewJCN() reads the form into {hull, cls, swlin, space, eid, nom}: hull from f-hull and cls looked
   up in DB.hulls as described; the text fields trimmed and uppercased.
7. renderAnalogs() draws table analogs with columns: Use (a checkbox, checked when TICK has the row's
   jcn; ticking or unticking updates TICK and calls buildEstimate()), JCN, Hull and class, Received
   (fmtDate), Score (one decimal), Equipment (id and nomenclature), Space, SWLIN, Why it matched (the
   reasons joined with "; "), and Job summary (with "covers N JCNs" when DB.jsCount[job_summary] is
   above 1, and the note when present). Rows with a note get a muted style.
8. The weights div shows one small number input per W key with a plain label (for example "Same
   equipment ID", "Same class fallback: fewest same-class matches before other classes are shown",
   "Recency half-life, years"), plus a "Reset weights" button. Changing any value re-runs run().
   Remember the weights in localStorage, wrapped in try/catch, and load them when the module runs.
   Build the weights panel by calling a function directly at the end of the module (the elements already
   exist because the script is at the end of the body); do not use a DOMContentLoaded listener.
9. run() = readNewJCN, findAnalogs into ANALOGS, reset TICK to the jcn values of the top five,
   renderAnalogs, buildEstimate.
10. No em dashes.

Answer with the one <script> block only, and nothing after it.
```

## Prompt 4: the estimate and the CSV

```
Continue the same file. Write MODULE 4: a single <script> block that I will paste over the line
<!-- MODULE 4: estimate -->. It replaces the stubs buildEstimate and estimateCSV by declaring plain
global functions of the same names (no IIFE, no module, no assignment to window). Keep every contract
name exactly.

Contract reminder: ANALOGS is the array returned by findAnalogs, each element {j, score, raw, reasons}
where j is a jcn_history row with jcn, job_summary, hull, ship_class, swlin, space, equipment_id,
equipment_nomenclature, received_date (a Date or null). TICK is the Set of ticked jcn values.
DB.phasesByJS[job_summary] is an array of phase rows (phase_no, phase_title, shop, est_hours,
charged_hours). DB.matByJS[job_summary] is an array of material rows (phase_no, item, qty).
DB.jsCount[job_summary] (a plain object, not a Map) is how many JCNs share that summary. readNewJCN()
returns {hull, cls, swlin, space, eid, nom}. Elements: estnotes, estimate, material, csvout. Helpers
esc, csvCell, fmtDate, setDownload. Global EST.

How the estimate is built:
1. Take the ticked analogs that have phase data. Use each job_summary once even if two ticked JCNs share
   it. If none, write a note in estnotes asking the user to tick at least one job with phase data, clear
   the tables and csvout, call setDownload(), and return.
2. Sort the used job summaries newest first by received_date. The phase breakdown (the list of phases
   and their order) comes from the NEWEST one. Note in estnotes which JCN it came from, its date
   (fmtDate), how many phases, and how many job summaries are behind the numbers.
3. Method change check: for each other used summary, compare its set of phase titles with the newest
   one's; if fewer than 80% of the combined titles are shared, add a visible note "Possible method
   change" naming that JCN, its date and its phase count, and saying to check how the work is done today
   before trusting older hours.
4. If fewer than three summaries are used, add a note that the ranges are a starting point for the
   planner, not a forecast.
5. For each phase of the newest breakdown, find the phase with the same title in every used summary.
   Collect est_hours and charged_hours, each divided by that summary's DB.jsCount (a summary that covered
   several JCNs is shared out). Show low to high of each as "a to b" (one decimal), the shop from the
   newest breakdown, and "k of n" for how many summaries had that phase.
6. Totals: sum the low and high of est and of charged across phases, state both ranges in estnotes, and
   if charged ran higher than estimated say by about what percent, and end with "Plan to the charged
   range."
7. Material: for every used summary, map each material row's phase_no to that summary's phase title,
   then group by title and item. Show a table: end-use phase, item, qty as low to high (divided by
   jsCount), and "seen on k of n". Items whose phase title is not in the newest breakdown are listed last
   and marked "older breakdown only".
8. Set EST = {nj: readNewJCN(), rows, used} and then fill csvout with estimateCSV() and call
   setDownload().
9. estimateCSV(): header new_equipment_id, new_space, new_swlin, new_hull, phase_no, phase_title, shop,
   est_hours_low, est_hours_high, charged_hours_low, charged_hours_high, summaries_with_phase,
   summaries_used, analog_jcns; one line per phase; CRLF line ends; every cell through csvCell; the new
   job's values come from EST.nj.eid, EST.nj.space, EST.nj.swlin, EST.nj.hull.
10. No em dashes. Tables are plain HTML with a header row; numbers right-aligned.

Answer with the one <script> block only, and nothing after it.
```

## Prompt 5: check the assembled file

```
I have assembled the file from your four answers. Without rewriting it, check it for the mistakes that
usually break a file built in pieces, and list each one with the exact fix:
1. Every function called anywhere but not defined, and every function defined twice (a stub left in
   place next to the real one is fine only if the real one comes later in the file).
2. Every element id used in JavaScript that does not exist in the HTML, and the reverse.
3. Values used across modules under different shapes: DB.jsCount read with .get() although it is a
   plain object; analogs read as a.jcn in one place and a.j.jcn in another; the new JCN read as
   equipment_id in one place and eid in another.
4. Any <script> block left unclosed, any placeholder comment left in, and any character outside plain
   ASCII inside the JavaScript that could be a smart quote.
5. Anything that would be blocked by the Content-Security-Policy in the head.
Then give me a short test checklist: five things to do in the opened page, in order, and what I should
see after each.
```

## Debug prompt (use as many times as needed)

```
I opened the assembled file and did this: <what you clicked>. The browser console (F12) shows this error:

<paste the red text here, exactly>

Find the cause in the file you wrote and answer with only the corrected function or block, named so I
can paste it over the old one. Do not change anything else.
```

## Column-name prompt (optional, for the real exports)

```
My three exports have these header rows (names only, no data):
jcn_history: <paste the header row>
phases: <paste the header row>
material: <paste the header row>
Update the alias lists in loadFiles so each of these headers maps to the right contract field, and tell
me which contract fields, if any, have no matching column so I know what to add in the export.
```

## Test checklist (what the test here saw, for comparison)

1. Open the file: five numbered sections, "Find similar jobs" greyed out.
2. Choose the three exports: the status line names all three with their row counts; no mapping rows if
   the columns matched; btn-run turns on.
3. Pick a hull, type an equipment ID, space and SWLIN, click: ten rows, the exact-match job first,
   then same-type jobs on the same class, each with its reasons and a tick box.
4. Untick a row: the estimate recomputes; the note says which JCN the breakdown came from.
5. The CSV box fills with one line per phase; Download saves estimate.csv.

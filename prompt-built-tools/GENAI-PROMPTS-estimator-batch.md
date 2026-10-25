# Prompts C: add batch mode to the estimator (big files in, one big CSV out)

Version 0.9, 2026-10-25 (v0.1 to v0.8 kept in the private source). v0.9 follows the estimator series v0.7 to the
task-based history of the owner's pulls: the history's `tasks` table (one record per task, the phase-level fields
repeated on each) already carries the four dates, so C1 no longer adds them to a phases table; the estimate rows are
one per phase AND shop with a `tasks` text (Prompt 4 v0.7), so the consumption file is one line per item, phase and
shop and gains a last column, tasks (20 cells); placePhases reads a phase's dates from DB.phasesByJS by phase title
and gives every shop row of the phase the same weeks, and the sequence rule starts the rows of one phase together.
C1, C2 and C2b regenerated from this text on the v0.7 estimator and tested against the twin on the fourth made-up
data set (the private test record). v0.8 (2026-10-24) built on the estimator series v0.5: the new JCN
carries its discrepancy text, so `proposed` gains an optional discrepancy column and nj gains `text` (the owner's ruling
R4, 2026-10-24); the weights panel is drawn by renderWeights() and the saved weights are merged again through
loadSavedWeights() after this series adds its keys; the EST shape the batch loop reads is pinned in Prompt 4 of the
estimator series; all from the review of PR 69; v0.8 was regenerated from this text on the v0.5 estimator and checked
line by line against an independent calculation of the auto-select and the estimate, test record kept in the private source). v0.7 only moved the pointer to Prompts D v0.4, which stops dividing material by the JCN count and adds group_size; v0.6 corrected the order: Prompts D in `GENAI-PROMPTS-estimator-planned.md` run after C2b and BEFORE Prompts X, and add planned jobs, the contractor and the material list; v0.4 added the pointer to Prompts X, which let both file pickers take .xlsx workbooks, see `GENAI-PROMPTS-xlsx.md`; C1 to C3 are unchanged from v0.3, which says how rule 2 chains after a phase placed by rule 1, from the review of PR 52). Tested against Gemini with no code execution, the same
handicap as the chat inside: the v0.1 prompts produced one syntax error on load and four mismatches in
the batch loader, and the model shortened the placement logic on its own. v0.2 states the pieces that
drifted and moves placement into its own prompt (C2b), which then worked first time. The test build ran
28 proposed items to 135 phase lines with every week inside its availability window. Details in the private test record.

Three prompts that extend the estimator built from `GENAI-PROMPTS-estimator.md` (Prompts 1 to 5, and Prompt T of the
tune series if you ran it). Run them in the same chat after Prompt 5 (and after T). Each answer is pasted into the file as the prompt says. To feed Excel files
directly (the history export as one workbook with a sheet per table, the proposed list as a workbook), run
Prompts X from `GENAI-PROMPTS-xlsx.md` after C2b; tested with both pickers. Prompts D (`GENAI-PROMPTS-estimator-planned.md`: planned job summaries bypass the guess, a performing column for the
contractor, a material list output) run after C2b and BEFORE Prompts X; if X is already in the file, run X2 again after D so
its hook wraps D's loader.

What batch mode does: load a CSV of proposed work items (many new JCNs at once) and, for each one, find
analogs, build the estimate and place its phases in weeks without anyone ticking boxes, then write one big
CSV (one line per item per phase and shop) in the shape the Resource Map app imports. It also makes the history
import survive big files: streamed reading and a local store (IndexedDB) so the history loads once.

Contracts added here (the single-JCN contract from Prompts 1 to 5 stays as it is):

- `tasks` (the history's task table, estimator series v0.7) already carries the optional planned_start,
  planned_finish, actual_start, actual_finish on every task record, and DB.phasesByJS holds them per phase;
  nothing is added to it here.
- `jcn_history` gains one optional column: project (the availability or project the JCN belongs to;
  aliases: project, availability, avail, avail id, availability name, period).
- `availabilities` (optional table): project, hull, start, end.
- `proposed` (input): proposed_id, hull, project, swlin, space, equipment_id, nomenclature,
  planned_start (optional), discrepancy (optional: the free text as written on the new JCN; aliases
  discrepancy, discrepancytext, narrative, problem, deficiency, remarks, text).
- `consumption` (output): proposed_id, hull, project, phase_no, phase_title, shop, est_hours_low,
  est_hours_high, charged_hours_low, charged_hours_high, load_hours, week_start, week_end, placement,
  summaries_used, same_class, top_score, analog_jcns, notes, tasks (the newest analog's task texts for
  that phase and shop, "; " separated). 20 cells, one line per item, phase and shop; the Resource Map reads
  the first 19 by name and ignores the rest.
- New element ids: p-files, btn-batch, batch-status, batch-summary, batch-preview, batch-download,
  hist-store.
- New weights: W.autoMin (default 0.6, a share of the top score), W.autoMax (default 5).
- New functions: streamCSV(file, onProgress), storeDB(tables), loadStoredDB(), checkStoredDB(),
  loadBatchFiles(files), estimateBatch(), finishBatch(rows, stats, ms), getMonday(d),
  placePhases(item, estRows, usedJcns).

---

## Prompt C1: big history files and a local store

```
Continue the same file (the offline JCN estimator). Write MODULE 5: a single <script> block that I will
paste just BEFORE the MODULE 3 script block (the block that begins with const DEFAULT_W), so it runs after
MODULE 2, plus one small HTML block. Keep every contract name exactly; declare plain global functions (no
IIFE, no module, no window assignment). Where this module redefines a function from MODULE 2, declare it
again with the same name: the later declaration wins.

Two rules about MODULE 2's variables: it declared SCHEMA and OPTIONAL_FIELDS with const and RAW_DATA and
MAPPINGS with let.
A second declaration of any of those names in another script block is a syntax error that kills the
whole block, so never write const SCHEMA, const OPTIONAL_FIELDS, let RAW_DATA or let MAPPINGS again. Extend SCHEMA in
place (Object.assign(SCHEMA.jcn_history, {project: [...]}); SCHEMA.availabilities = {...}), push the new
optional field name onto OPTIONAL_FIELDS, and use RAW_DATA and MAPPINGS as they are. MODULE 2 checks that
list by field name across every table, so push only the names that are optional wherever they appear
(here only project; the task table's dates and text fields are already on it); the availabilities
table's own fields (project, hull, start, end) are required for it and are never pushed, because hull
is required in the history.

Contract reminder: DB.jcns (array of rows: jcn, job_summary, hull, ship_class, swlin, space,
equipment_id, equipment_nomenclature, discrepancy (a string, as typed, possibly empty), received_date as
a Date or null), DB.tasksByJS (plain object, job_summary to array of task rows {phase_no, phase_title,
description, task_no, task, shop, crew_size, est_hours, charged_hours, performing, planned_start,
planned_finish, actual_start, actual_finish}, dates as Date or null, one row per task of a phase),
DB.phasesByJS (job_summary to the phases {phase_no, phase_title, description, planned_start,
planned_finish, actual_start, actual_finish}, derived from the tasks by buildDB, or from an optional
phases file), DB.matByJS, DB.jsCount (plain object), DB.hulls (array of [hull, ship_class]). Helpers $(id), esc, toDate, fmtDate,
num, csvCell. MODULE 2 has parseCSV(text), loadFiles(fileList), buildDB(tables), a SCHEMA of aliases
(written without spaces, compared through cleanCol(s) = lower case with everything but letters and
digits removed), OPTIONAL_FIELDS, a detectType(headers), an updateStatus() and a mapping panel; its code
is above in this chat, so reuse its mapping panel and autoMap as they are rather than guessing at them.

Changes:
1. Streamed reading. Write streamCSV(file, onProgress): reads the file in 4 MB slices (file.slice, read
   as text), carries the incomplete last record from one slice to the next (quoted fields with line
   breaks inside must still work, so carry the partial record, not just the partial line), parses
   complete records as it goes, calls onProgress(percent) with a number after each slice when a function
   was given (a caller may omit it, so guard the call), and resolves to {headers, data} where headers is
   the array of trimmed header strings and data is the array of row objects keyed by header. loadFiles uses it instead of reading the whole file, and shows progress in
   datastatus ("reading tasks.csv: 37%").
2. More columns. Extend SCHEMA in place: jcn_history gains optional project (aliases: project,
   availability, avail, avail id, availability name, period). A fourth optional table availabilities: project, hull,
   start, end (aliases: start, start date, avail start; end, end date, finish, completion), detected by a
   project or availability column together with start and end columns. Optional columns never block the
   mapping panel or btn-run; they are blank when absent. buildDB keeps every column and every table the first
   buildDB built (the task rows with their dates, DB.phasesByJS derived from them, the optional
   discrepancy text on each jcn row, trimmed, as typed), plus project (uppercased) on each jcn row, and
   stores availabilities in DB.availByProject (plain object, uppercased project to {project, hull, start, end} with Dates).
3. Local store. Add storeDB(tables) that writes the mapped tables and the mapping to IndexedDB (database
   "estimator", one object store "tables", one record keyed "history" holding {savedAt, rowCounts,
   tables, mappings}; the tables are jcn_history, tasks, material and, when one was loaded, phases), and
   loadStoredDB() that reads it back and calls buildDB. Dates must survive the
   round trip: store them as YYYY-MM-DD strings and rebuild them. Every IndexedDB call is wrapped so a
   failure (a private window, storage blocked) only shows a message and never breaks the page. After a
   successful import, call storeDB(tables) and tell the user in datastatus that the history is saved in
   this browser.
4. On page load (a DOMContentLoaded listener is fine), if a stored history exists, fill the element
   hist-store with a line "Stored history: saved <date>, N JCNs, M tasks" and two buttons "Use stored"
   (calls loadStoredDB) and "Forget" (deletes the record). The file picker still works as before to
   replace it.
5. Memory: keep rows as plain objects but do not keep the raw CSV text or the unmapped rows after
   buildDB has run (clear RAW_DATA).
6. After buildDB, btn-run and btn-tune are enabled, as MODULE 2 did; buildDB keeps the material rows as
   MODULE 2 built them ({job_summary, phase_no, item, qty}) and the task, phase and jcn rows with every
   field MODULE 2 gave them, in the same case (nomenclature, phase titles, descriptions, task texts,
   performing and discrepancy as typed; codes uppercased). Nothing in the file reads a field MODULE 2 did not define.
7. No em dashes. No network access. No alert, confirm or prompt dialogs.

Also give me this HTML block to paste just before the "2. New JCN" section:
<div id="hist-store"></div>

Answer with the HTML block first, then the one <script> block, and nothing after it.
```

## Prompt C2: batch load, auto-select, output

```
Continue the same file. Write MODULE 6: a single <script> block that I will paste as the LAST script in
the file, after the MODULE 4 block, plus one HTML block. Declare plain global functions (no IIFE, no
module, no window assignment). Keep every contract name exactly.

Contract reminder: findAnalogs(nj) returns [{j, score, raw, reasons, note?}] for a new JCN nj = {hull,
cls, swlin, space, eid, nom, text}, where text is the discrepancy as typed (an empty string when the item
has none; the matcher scores a missing text as 0); rows from another class carry note. DB.hulls holds [HULL, class] pairs with
the hull uppercased and trimmed, so uppercase and trim the hull before looking it up; uppercase and trim
project the same way. The single-JCN estimate logic is in buildEstimate() and reads ANALOGS and TICK; do
not change it; it sets EST = {nj, rows, used, usedJcns, notes} where rows are {phase_no, phase_title,
shop, tasks, est_low, est_high, charged_low, charged_high, k, n}, one row per phase AND shop of the
newest analog (so consecutive rows share a phase), tasks a string, and usedJcns is a space-separated
string of the JCNs used, newest first (Prompt 4 of the estimator series v0.7 pins that shape; if your
file came from an older series, run its Prompt 4 again first). streamCSV(file, onProgress) from MODULE 5 calls onProgress with a percent number and
resolves to {headers, data}, where headers is the array of trimmed header strings and data is an array
of row objects keyed by those header strings (a cell is row[headers[i]] or row["Hull"], never row[i]);
cleanCol(s) lower-cases a header and strips everything but letters and digits, and every alias list is
written in that form ("proposedid", "equipmentid", "plannedstart").
DB.availByProject maps an uppercased project to {project, hull, start, end}. W holds the weights: add
W.autoMin (default 0.6) and W.autoMax (default 5) to BOTH DEFAULT_W and W, add their labels to W_LABELS,
then call loadSavedWeights() (so values of the new keys saved in an earlier session survive a reload) and
then renderWeights() so they show. Helpers $(id), esc, toDate, fmtDate, num, csvCell,
setDownload. Declare getMonday(d) in this module (the Monday on or before d, as a Date at midnight; null
for null or an invalid date), because the placement step and later series call it. Placement of phases
in weeks is written in the NEXT step as placePhases(item, estRows,
usedJcns), which returns an array parallel to estRows of {week_start, week_end, placement, note}; in
this step declare it as a one-line stub that returns, for every row, {week_start: '', week_end: '',
placement: '', note: 'no dates'}, and call it from the loop as described below.

New HTML (paste just before the "5. Export" section):
<div class="section" id="sec-batch">
  <h2>6. Batch: estimate a list of proposed work</h2>
  <p>Choose proposed.csv (columns: proposed_id, hull, project, swlin, space, equipment_id, nomenclature,
  planned_start optional, discrepancy optional) and, if you have it, availabilities.csv (project, hull,
  start, end).</p>
  <input type="file" id="p-files" multiple>
  <div><button id="btn-batch" disabled>Estimate all</button></div>
  <div id="batch-status"></div>
  <div id="batch-summary"></div>
  <textarea id="batch-preview" readonly></textarea>
  <div><a id="batch-download" download="consumption.csv">Download consumption.csv</a></div>
</div>

Behavior:
1. p-files: its change listener calls a plain global function loadBatchFiles(Array.from(this.files)),
   so the function receives a plain array (a later series wraps that function by name, so it must exist
   under that name and accept an array). loadBatchFiles reads the files with streamCSV. Detect proposed.csv by a proposed id
   column (aliases proposedid, id, line, item, jcn) together with a hull or equipment column, and
   availabilities.csv by a project column (aliases project, availability, avail, availid,
   availabilityname, period: the list MODULE 5 gave SCHEMA.availabilities.project, so reuse
   SCHEMA.availabilities for its four fields) together with start and end columns, comparing
   cleanCol(header) with the alias lists; map columns the same way (proposed_id, hull, project, swlin, space, equipment_id
   (aliases equipmentid, equipment, eid), nomenclature (nomenclature, nom, description), planned_start
   (plannedstart, plannedstartdate, start), discrepancy (optional: discrepancy, discrepancytext,
   narrative, problem, deficiency, remarks, text; blank when the column is absent)); show a mapping panel
   when any of the seven required columns (proposed_id, hull, project, swlin, space, equipment_id,
   nomenclature) found no column: one <select> of the file's headers per missing field and an Apply
   button, drawn in batch-status (never an alert, confirm or prompt dialog: every message goes to
   batch-status); then enable btn-batch and say in batch-status how many items and how many
   availabilities were read. Availabilities read here go into BATCH_AVAIL (same shape as
   DB.availByProject: uppercased project to {project, hull, start, end}, start and end through toDate, so
   Dates or null, never strings). Keep the items in a global BATCH_ITEMS.
2. btn-batch runs estimateBatch(): for each proposed item, in chunks of 20 items per setTimeout(0) so
   the page stays responsive and batch-status shows "item 140 of 800":
   a. Build nj from the item: hull, swlin, space, eid and nom trimmed and uppercased; text = the item's
      discrepancy trimmed and otherwise as typed ("" when absent); cls from DB.hulls by the uppercased
      hull; if the hull is not found, cls is blank and the item note "hull not in history" is
      recorded. Item notes are fixed before the phase loop; each output line gets a copy of them plus its
      own.
   b. analogs = findAnalogs(nj). Auto-select: same-class rows (no note) with score >= W.autoMin times
      the top same-class score, at most W.autoMax, at least one if any exist. If there is no same-class
      analog, use the top other-class analog alone and set same_class = no. If there are no analogs at
      all, write one output line with blank hours and the note "no analog".
   c. Set ANALOGS to the analog list and TICK to a new Set of the selected analogs' jcn values (each
      analog a is {j, score, raw, reasons}, so the value is a.j.jcn), call buildEstimate(), and read
      EST.rows, EST.usedJcns and EST.notes. It is acceptable that the single-JCN tables show the last
      item's estimate when the batch ends.
   d. load_hours for a row (one phase and shop) = the midpoint of its charged range (if the charged
      range is blank, the midpoint of the estimated range).
   e. const placed = placePhases(item, EST.rows, EST.usedJcns); the line for row i takes week_start,
      week_end and placement from placed[i], and adds placed[i].note to the line's notes when present.
   f. Collect one output line per estimate row (phase and shop): proposed_id, hull, project, phase_no,
      phase_title, shop, est_hours_low, est_hours_high, charged_hours_low, charged_hours_high, load_hours,
      week_start, week_end, placement, summaries_used (EST.usedJcns.split(' ').length: the JCNs the
      estimate used, not the count of ticked analogs), same_class, top_score (one decimal), analog_jcns
      (EST.usedJcns), notes (semicolon separated, from this fixed list only: "possible method change"
      when any string in EST.notes begins "Possible method change", "thin history" when n < 3, "no
      analog", "hull not in history", "no dates"; never copy EST.notes themselves into the line), tasks
      (EST.rows[i].tasks, "" for a no-analog line). 20 cells.
3. When done: batch-summary shows items estimated, items with no analog, lines by placement rule
   (relative, sequence, start_week, blank), total load_hours by shop (a small table), and the elapsed
   time. batch-preview shows the header and the first 50 lines. batch-download gets a Blob URL (or a
   data: URL) of the whole CSV, UTF-8 with no byte-order mark (the Resource Map reads the header by
   name), CRLF, every cell through csvCell. Build the CSV in an array of lines and join once.
4. Wire btn-batch through an arrow function: $('btn-batch').addEventListener('click', () =>
   estimateBatch()), never by passing the function itself, because a later series declares estimateBatch
   again. finishBatch(rows, stats, ms) is a plain global function with that signature.
5. No em dashes. No alert, confirm or prompt dialogs anywhere.

Answer with the one <script> block only, and nothing after it (the HTML block is given above; I will
paste it myself).
```

## Prompt C2b: placing phases in weeks

```
Continue the same file. Replace the one-line stub placePhases with the real function: ONE global
function placePhases(item, estRows, usedJcns), a plain function declaration (no IIFE, no window
assignment), pasted over the stub. It returns an array parallel to estRows, each element {week_start,
week_end, placement, note}, where week_start and week_end are 'YYYY-MM-DD' Monday strings or '' and
placement is one of "relative", "sequence", "start_week", or "" when nothing applies. Implement ALL
THREE rules in full; do not simplify or leave any as a placeholder; if the answer would be too long, say
so instead of shortening the logic.

What the file provides: $(id), toDate(s) (Date or null), fmtDate(d) ('YYYY-MM-DD' or ''), getMonday(d)
(the Monday on or before d, as a Date; null for null; declare it here if MODULE 6 did not). DB.jcns rows
{jcn, job_summary, hull, ship_class, swlin, space, equipment_id, equipment_nomenclature, received_date,
project (uppercased string or '')}. DB.phasesByJS[job_summary]: the summary's phases {phase_no, phase_title,
description, planned_start, planned_finish, actual_start, actual_finish} (each date a Date or null), one
row per phase, derived from the task records (the dates sit on the phase; every shop of a phase shares
them). DB.availByProject[PROJECT] and BATCH_AVAIL[PROJECT] = {project, hull, start, end} (Dates or
null). estRows elements {phase_no, phase_title, shop, tasks, est_low, est_high, charged_low, charged_high, k,
n} in the newest analog's phase order, ONE PER PHASE AND SHOP, so consecutive rows share a phase (same
phase_no and phase_title); all rows of one phase get the same weeks and placement. usedJcns: a space-separated string of the JCNs used, newest first.
item: {proposed_id, hull, project, swlin, space, equipment_id, nomenclature, planned_start} as strings.

Definitions:
- Target window: the item's project (uppercased) looked up in BATCH_AVAIL first, then DB.availByProject;
  usable only if both start and end are Dates and end is after start.
- An analog's own window: for each JCN in usedJcns, find its row in DB.jcns, take its project, look it up
  in DB.availByProject; usable under the same condition.
- For a given estimate row, an analog's phase is the row in DB.phasesByJS[that JCN's job_summary] whose
  phase_title, trimmed and uppercased, equals the estimate row's phase_title trimmed and uppercased
  (use phaseKey from MODULE 4 when it exists, else compare inline).

Rules, in order; the first rule whose conditions hold for the phase is used:
1. "relative": the target window is usable, AND at least one used analog has a usable window AND a phase
   with this title whose actual_start is a Date. For each such analog, fraction = (actual_start -
   window.start) / (window.end - window.start), clamped to 0..1, and duration in days = (actual_finish -
   actual_start) if actual_finish is a Date and after actual_start, else 7; take the mean fraction and
   the mean duration (at least 7 days). start = target.start + fraction * (target.end - target.start);
   finish = start + duration days.
2. "sequence": else, if toDate(item.planned_start) is a Date: phases run one after another from
   planned_start in estRows order, where all rows of one phase (same phase_no) share one start and one
   duration; a phase's duration comes from the NEWEST analog (the first JCN in usedJcns): its phase with
   this title, actual_finish - actual_start when both are Dates and finish is after start, else
   planned_finish - planned_start under the same test, else 7 days; at least 1 day. A rule-2 phase starts
   at the latest finish among the item's already placed rows of EARLIER phases (in estRows order,
   whichever rule placed them); if no earlier phase of the item has been placed, it starts at
   planned_start.
3. "start_week": else, if toDate(item.planned_start) is a Date: every phase gets week_start = week_end =
   the Monday of planned_start.
4. Otherwise week_start = week_end = '', placement = '', note = "no dates".
week_start = fmtDate(getMonday(start)); week_end = fmtDate(getMonday(finish)); note = '' unless rule 4.
Rules 1 and 2 are decided per phase (all its shop rows together), so one item may mix them when only
some phases have actual dates in the analogs; the rows of one phase always carry the same week_start,
week_end and placement. Guard every date arithmetic against null and NaN. No em dashes.

Answer with the one function only, in one code block, and nothing after it.
```

## Prompt C3: check the batch build (run in the same chat as the build; it needs the whole file)

```
I have added MODULE 5, MODULE 6 and placePhases. Without rewriting the file, check:
1. That MODULE 5 declares no const or let name that MODULE 2 already declared, that its redefinitions of
   loadFiles and buildDB keep every name MODULE 3 and 4 rely on, and that nothing in MODULE 5 runs before
   the elements it touches exist.
2. That estimateBatch never calls a function that does not exist (renderWeights, not buildWeightsPanel,
   draws the weights), calls placePhases once per item, uppercases the hull before the DB.hulls lookup,
   builds nj with a text key (the item's discrepancy, or ""), counts summaries_used from EST.usedJcns,
   writes only the fixed phrases into notes (never the sentences in EST.notes), writes one line per
   EST row (phase and shop) with that row's tasks as the last cell, and gives the rows of one phase the
   same week_start and week_end; that MODULE 6 declares
   getMonday; and that a proposed file missing one of the seven required columns draws the mapping panel
   in batch-status instead of reading blanks.
3. That week_start is always a Monday string or blank, and that every output line has exactly 20 cells.
4. Any Date object that would reach csvCell unformatted.
Then give me a five-step test for batch mode with a proposed.csv of three made-up lines: one with a known
hull and equipment, one with an unknown hull, one with no planned_start.
```

## Debug prompts (use as many times as needed)

For an error in the console:

```
I opened the assembled file and did this: <what you clicked>. The browser console (F12) shows this error:

<paste the red text here, exactly>

Find the cause in the file you wrote and answer with only the corrected function or block, named so I
can paste it over the old one. Do not change anything else.
```

For a wrong result with no error (this form fixed two of the three loader faults in the test):

```
I opened the assembled file and did this: <what you clicked, and the header row of the file you chose>.
There was no error in the console, but <what the status line or the output showed> where I expected
<what should have happened>.

Find the cause in the file you wrote and answer with only the corrected function or block, named so I
can paste it over the old one. Do not change anything else.
```

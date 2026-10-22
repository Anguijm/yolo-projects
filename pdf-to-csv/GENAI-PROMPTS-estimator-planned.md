# Prompts D: planned jobs, the contractor, and the material list

Version 0.4, 2026-10-23. v0.4 applies the project owner's rule for JCNs grouped on one job summary
(2026-10-23): the hours of a grouped summary are divided by its JCN count, as they have been since the first
estimator prompts, but the material is NOT. A new JCN that matches a grouped summary gets the complete material list
at full quantity, and a new column, group_size, says how many JCNs the bundle held (1 = not grouped), so a planner
knows the list may carry sibling jobs' parts and can trim it. v0.3 divided material by the JCN count (an inference
from the hours rule, tightened by the review of PR 57); that is reversed here on that rule. The owner also answered the
pull shape: the material export lists each order line once per phase of a job summary, and it is the JCN history
that repeats a grouped summary once per JCN, so the tool takes material rows as they are and never collapses or
divides them. v0.3 answered the review of PR 57: D runs BEFORE Prompts X, one material value per summary with
every used JCN listed, and performing is matched on whole words so "control" is not a contractor. Earlier, tested
against Gemini with no code execution, the same handicap as the chat inside: v0.1 recursed on the first history
load (the wrapper captures shared a block with the new declarations), the rewritten batch loop never ran from the
button (MODULE 6 had bound the old function), the material quantities were summed, and unscheduled planned phases
piled into one week; v0.2 fixed all of that in the prompt text and built working code first time. The test records
stay in the private source.

Three prompts that extend the batch estimator built from Prompts C (`GENAI-PROMPTS-estimator-batch.md`,
C1, C2, C2b). Run them in the same chat after C2b and BEFORE Prompts X (workbook input): X2's hook must wrap
D's loader, not the other way round, because D captures whatever loadBatchFiles is at the time as its Core, and
after X that is the workbook expander, so a planned workbook would be read as raw text and never recognized. If
Prompts X are already in the file, run X2 again after D. D adds no file picker. Each answer is pasted into the
file as the prompt says.

What they add:

1. **Planned jobs bypass the guess.** Planning gives some job summaries a real estimate (man-hours or man-days
   by shop, per phase) and, later, scheduled dates. A new optional table `planned` carries those. A proposed
   item whose job summary is in it is written out from the planner's numbers, not from history, and its weeks
   come from the schedule when there is one.
2. **The contractor.** About a third of the work is farmed out. The history phases gain `performing` (organic
   shop or contractor), so each estimate line says who did the similar work; a proposed item screened as
   in-house or farm-out carries that mark through; a planned phase carries planning's answer.
3. **The material list.** A second output, `material_estimate.csv`: for every phase of every item, the stock
   numbers the similar jobs ordered, with nomenclature and quantity range, which analogs carried them, and how
   many JCNs the source summary bundled. Hours from a grouped summary are shared out over its JCNs; material is
   not: each JCN gets the whole list, marked with the group size.

Contracts added here (everything from Prompts 1 to 5 and C1 to C2b stays as it is):

- `phases` gains one optional column: performing (aliases: performing, performingactivity, activity,
  performer, workby, inhouse, farmout, contractor, org, organic). Values are normalized to "farm-out",
  "in-house" or "".
- `material`: item becomes optional; two optional columns are added, stock_number (aliases: stocknumber,
  niin, nsn, stock, partnumber, partno, nationalstocknumber) and nomenclature (aliases: nomenclature, noun,
  nounname, description, itemdescription, itemname). A material file is recognized by a quantity column
  together with an item, part, stock number, NIIN or NSN column. A row with a blank item takes its
  stock_number as item; a blank stock_number takes item; a blank nomenclature takes item.
- The material export lists each order line once per phase of a job summary (the JCN history is what repeats a
  grouped summary once per JCN). Quantities are taken as they are: never divided by DB.jsCount, never collapsed.
  Two rows with the same stock number on one phase are two orders and add up.
- `proposed` gains two optional columns: job_summary (aliases: jobsummary, js, jobsummarynumber) and
  performing (same aliases and normalization as phases).
- `planned` (new optional input through the batch picker p-files): job_summary, phase_no, phase_title,
  shop, planned_hours OR planned_mandays (one of them), scheduled_start, scheduled_finish, performing
  (all but job_summary, phase_no and the hours column optional). Kept in the global PLANNED (a plain object,
  uppercased job_summary to an array of phase rows with planned_hours always in hours).
- `consumption` (output) gains three columns at the end, after notes: source ("history" or "planned"),
  performing ("in-house", "farm-out" or ""), performing_basis ("screening", "planning", "analogs" or "").
  22 cells per line. The Resource Map reads the first 19 by name and ignores the rest.
- `material_estimate` (new output): proposed_id, hull, project, job_summary, phase_no, phase_title,
  stock_number, nomenclature, qty_low, qty_high, seen_on, summaries_used, group_size, source, analog_jcns.
  15 cells per line.
- New weight: W.hoursPerDay (default 8), used to turn planned_mandays into hours.
- New globals: PLANNED, PROPOSED_EXTRA (plain object, uppercased proposed_id to {job_summary, performing}).
- New element ids: mat-summary, mat-download.
- New functions: normPerforming(s), augmentDB(tables), loadPlanned(file), materialLines(item, usedJcns),
  plus wrappers that keep the earlier functions: buildDB, detectType, loadBatchFiles.

The lesson from Prompts C and X applies: a wrapper keeps a tested function and adds to it (`var
buildDBCore = buildDB;` in one script block, then a new declaration of buildDB in the NEXT block that calls
buildDBCore first; in the same block the hoisted new declaration would be captured instead). Only
estimateBatch and finishBatch are rewritten in full, because the new rules live inside their loop.

---

## Prompt D1: the new columns and the planned table

```
Continue the same file (the offline JCN estimator with batch mode). Write MODULE 7: two <script>
blocks that I will paste as the LAST scripts in the file, after MODULE 6, plus one HTML block. Declare
plain global functions (no IIFE, no module, no window assignment). Keep every contract name exactly.
Never declare again with const or let a name an earlier block declared (SCHEMA, RAW_DATA, MAPPINGS, DB,
W, DEFAULT_W, W_LABELS, OPTIONAL_FIELDS, BATCH_ITEMS, BATCH_AVAIL, EST, ANALOGS, TICK); extend objects
in place.

Keep the earlier functions by wrapping them, not by rewriting them, and mind hoisting: a function
declaration is hoisted to the top of its own script block, so a `var buildDBCore = buildDB;` written in
the same block as a new `function buildDB` would capture the new one and recurse forever. So MODULE 7
is TWO script blocks, pasted in this order: block 7a holds only the three captures
`var buildDBCore = buildDB; var detectTypeCore = detectType; var loadBatchFilesCore = loadBatchFiles;`
and nothing else; block 7b holds everything below, including the new declarations of buildDB,
detectType and loadBatchFiles, each of which calls its Core version and adds what is described. The
later declaration wins; the Core variable keeps the earlier one.

Contract reminder: SCHEMA holds, per table, the field names and their alias lists; aliases are written
without spaces and compared through cleanCol(s) (lower case, everything but letters and digits
removed). MODULE 5 extended SCHEMA in place with Object.assign; do the same. detectType(headers) names
the table a header row belongs to. loadFiles reads the history files through streamCSV(file, onProgress),
which resolves to {headers, data} (data: row objects keyed by header). buildDB(tables) builds
DB.jcns, DB.phasesByJS (job_summary to phase rows {phase_no, phase_title, shop, est_hours,
charged_hours, planned_start, planned_finish, actual_start, actual_finish}), DB.matByJS (job_summary to
material rows {phase_no, item, qty}), DB.jsCount, DB.hulls, DB.availByProject; it uppercases
job_summary keys. loadBatchFiles(files) reads the batch picker's files with streamCSV, recognizes
proposed.csv and availabilities.csv by their headers, and enables btn-batch. Helpers $(id), esc, toDate
(Date or null), fmtDate, num, csvCell, getMonday. W and DEFAULT_W hold the weights, W_LABELS their
labels, buildWeightsPanel() redraws them.

1. normPerforming(s): trim, lower case; "" stays "". Split the text into words on anything that is not a
   letter or digit; it is "farm-out" when any word is one of contr, contractor, contract, contracted, ctr,
   cms, vendor, sub, subcontractor, subcontract, subk, farm, farmout, outsource, outsourced (whole words, so
   "control" and "subassembly" do not match); anything else non-blank is "in-house".
2. SCHEMA, extended in place at the top of this block, before any function runs:
   - phases gains optional performing with aliases performing, performingactivity, activity,
     performer, workby, inhouse, farmout, contractor, org, organic.
   - material: item becomes optional. Add optional stock_number (aliases stocknumber, niin, nsn, stock,
     partnumber, partno, nationalstocknumber) and optional nomenclature (aliases nomenclature, noun,
     nounname, description, itemdescription, itemname). Remove nsn and description from item's aliases
     if they are there, so a NIIN column maps to stock_number and a description column to nomenclature.
   - If an earlier block keeps a list of optional fields (MODULE 5 may have declared one with const,
     such as OPTIONAL_FIELDS), add item, stock_number, nomenclature and performing to it in place with
     push; never declare it again. The point: a material file with stock_number and qty but no item
     column needs no mapping panel.
3. detectType(headers): call detectTypeCore(headers); if it returns a table name, return it. Otherwise
   return "material" when the cleaned headers contain a quantity column (qty, quantity) together with any
   of item, part, material, stocknumber, niin, nsn; else return what Core returned.
4. buildDB(tables): call buildDBCore(tables), then augmentDB(tables):
   - For every row of tables.phases: find DB.phasesByJS[uppercased job_summary] and in it the phase row
     with the same phase_no (through num()); set that row's performing = normPerforming(row.performing).
     Rows with no match are skipped. A phase row that gets no value has performing "".
   - Rebuild DB.matByJS from tables.material: one row per input row, {phase_no: num(phase_no), item,
     stock_number, nomenclature, qty: num(qty)} with the blank-fill rules: blank item takes stock_number,
     blank stock_number takes item, blank nomenclature takes item; all three trimmed; keyed by the
     uppercased job_summary, in file order.
5. loadPlanned(file): streamCSV, then map columns by cleanCol against these alias lists: job_summary
   (jobsummary, js, jobsummarynumber), phase_no (phaseno, phase, phasenumber, keyop), phase_title
   (phasetitle, title, phasename, task), shop (shop, trade, workcenter), planned_hours (plannedhours,
   planhours, hours, manhours, mh, esthours, estimatedhours), planned_mandays (plannedmandays, mandays,
   manday, md, days), scheduled_start (scheduledstart, schedstart, start, startdate, plannedstart),
   scheduled_finish (scheduledfinish, schedfinish, finish, finishdate, end, enddate, plannedfinish),
   performing (as in SCHEMA). Required: job_summary, phase_no and one of planned_hours or
   planned_mandays. Build PLANNED: for each row, hours = planned_hours if that column exists, else
   planned_mandays times W.hoursPerDay; push {phase_no: num, phase_title (trimmed; if blank, "Phase " +
   phase_no), shop (uppercased, trimmed), planned_hours: hours, scheduled_start: toDate or null,
   scheduled_finish: toDate or null, performing: normPerforming} under the uppercased job_summary.
   Return the number of rows read. A required column missing: write which in batch-status and read
   nothing from that file.
6. loadBatchFiles(files): for each file in files, read its headers with streamCSV and decide: a planned
   file has a job summary column and a planned hours or man-days column and NO hull, equipment or
   proposed id column; a proposed file is what Core recognizes. Planned files go to loadPlanned and are
   NOT passed to Core; write the line "planned: N phase rows for M job summaries" into batch-summary
   (Core overwrites batch-status when it finishes, so the line would be lost there). For a
   proposed file, also record PROPOSED_EXTRA[uppercased proposed_id] = {job_summary: uppercased or "",
   performing: normPerforming(value or "")} from its rows, mapping the two columns by the aliases above,
   then pass the file on. Finally call loadBatchFilesCore with an array of the remaining files (it must
   accept an array; if Core indexes a FileList, an array works the same way). If no files remain (only
   a planned file was chosen), do not call Core; just report.
7. Weights: W.hoursPerDay = 8 in both DEFAULT_W and W (only if not already set), W_LABELS.hoursPerDay =
   "Hours per man-day (planned_mandays)", then buildWeightsPanel().
8. PLANNED and PROPOSED_EXTRA are declared with var at the top of this block as empty objects.
9. No em dashes. No network access.

Also give me this HTML block to paste just after the batch-download line inside the batch section:
<div id="mat-summary"></div>
<div><a id="mat-download" download="material_estimate.csv">Download material_estimate.csv</a></div>

Answer with the HTML block first, then the two <script> blocks in order (7a, then 7b), and nothing
after it.
```

## Prompt D2: planned bypass, performing, and the material lines

```
Continue the same file. Write MODULE 8: a single <script> block that I will paste as the LAST script in
the file, after MODULE 7. It declares estimateBatch and finishBatch again, in full, with the same names
and the same signatures as MODULE 6 (finishBatch(rows, stats, ms)); the later declarations win. Also
declare materialLines(item, usedJcns). Plain global function declarations only; no IIFE, no module, no
window assignment; never redeclare with const or let a name an earlier block declared. One thing a new
declaration cannot reach: MODULE 6 wired the button by passing the function itself
(addEventListener('click', estimateBatch)), which bound MODULE 6's estimateBatch for good. So at the END
of this block, after the declarations, replace the button with a clone of itself to drop every old
listener (var b = $('btn-batch'); var b2 = b.cloneNode(true); b.parentNode.replaceChild(b2, b);) and
wire the click again through an arrow function: $('btn-batch').addEventListener('click', () =>
estimateBatch()). Everything
MODULE 6's estimateBatch did stays exactly as it was; this prompt lists it again so nothing is lost, and
adds the planned bypass, the performing columns and the material lines. If the answer would be too long,
say so instead of shortening the logic.

Contract reminder: findAnalogs(nj) returns [{j, score, raw, reasons, note?}] for nj = {hull, cls, swlin,
space, eid, nom}; rows from another class carry note. buildEstimate() reads ANALOGS and TICK and sets
EST = {nj, rows, usedJcns} where rows are {phase_no, phase_title, shop, est_low, est_high, charged_low,
charged_high, k, n} and usedJcns is a space-separated string of the JCNs used, newest first.
placePhases(item, estRows, usedJcns) returns an array parallel to estRows of {week_start, week_end,
placement, note}. DB.jcns rows {jcn, job_summary, hull, ship_class, ..., received_date, project};
DB.phasesByJS[JS] phase rows now carry performing ("in-house", "farm-out" or ""); DB.matByJS[JS] rows
{phase_no, item, stock_number, nomenclature, qty}, one row per order line of that summary (the material export
does not repeat rows per JCN; only the JCN history does); DB.jsCount[JS] = how many JCNs share that summary. DB.hulls holds [HULL, class] with
the hull uppercased and trimmed. BATCH_AVAIL and DB.availByProject map an uppercased project to
{project, hull, start, end}. PLANNED maps an uppercased job_summary to rows {phase_no, phase_title,
shop, planned_hours, scheduled_start, scheduled_finish, performing}. PROPOSED_EXTRA maps an uppercased
proposed_id to {job_summary, performing}. Helpers $(id), esc, toDate, fmtDate, getMonday, num, csvCell,
setDownload. Elements batch-status, batch-summary, batch-preview, batch-download, mat-summary,
mat-download. W.autoMin, W.autoMax, W.hoursPerDay.

estimateBatch(), for each proposed item, in chunks of 20 items per setTimeout(0) with batch-status
showing "item 140 of 800":
a. Build nj from the item with every text field trimmed and uppercased; cls from DB.hulls by the
   uppercased hull; if the hull is not found, cls is blank and the item note "hull not in history" is
   recorded. Item notes are fixed before the phase loop; each output line gets a copy plus its own.
   extra = PROPOSED_EXTRA[uppercased proposed_id] or {job_summary: "", performing: ""}.
b. PLANNED BYPASS. If extra.job_summary is non-blank and PLANNED[extra.job_summary] exists: do not
   call findAnalogs or buildEstimate. estRows = one row per planned phase row, in file order:
   {phase_no, phase_title, shop, est_low: planned_hours, est_high: planned_hours, charged_low:
   planned_hours, charged_high: planned_hours, k: 1, n: 1}. Do not call placePhases for a planned
   item; place its rows here: a row whose scheduled_start is a Date gets week_start = fmtDate(getMonday(
   scheduled_start)), week_end = fmtDate(getMonday(scheduled_finish)) if scheduled_finish is a Date on
   or after scheduled_start else week_start, placement "scheduled"; otherwise, if toDate(
   item.planned_start) is a Date, the unscheduled rows run one after another from planned_start, 7
   days each (the first unscheduled row starts at planned_start, each next one at the previous
   finish), week_start = fmtDate(getMonday(start)), week_end = fmtDate(getMonday(finish)), placement
   "sequence"; otherwise week_start = week_end = "", placement "", note "no dates". load_hours =
   planned_hours. Line fields: summaries_used 0, same_class "", top_score "", analog_jcns "", notes
   "planned" plus any item notes, source "planned", performing = the planned row's performing if
   non-blank (basis "planning"), else extra.performing if non-blank (basis "screening"), else "" with
   basis "". Go to step g.
c. analogs = findAnalogs(nj). Auto-select: same-class rows (no note) with score >= W.autoMin times the
   top same-class score, at most W.autoMax, at least one if any exist. If there is no same-class analog,
   use the top other-class analog alone and set same_class = no. If there are no analogs at all, write
   one output line with blank hours, the note "no analog", source "history", performing =
   extra.performing with basis "screening" if non-blank else "" and "", and go to the next item.
d. Set ANALOGS to the analog list and TICK to the selected jcn values, call buildEstimate(), read
   EST.rows and EST.usedJcns. It is acceptable that the single-JCN tables show the last item's estimate.
e. load_hours for a phase = the midpoint of its charged range (if blank, the midpoint of the estimated
   range).
f. placed = placePhases(item, EST.rows, EST.usedJcns); the line for phase i takes week_start, week_end
   and placement from placed[i] and adds placed[i].note to its notes when present.
   PERFORMING for a history line: if extra.performing is non-blank, every line of the item gets it
   with basis "screening". Otherwise, per phase: walk the used summaries (the job_summary of each JCN
   in EST.usedJcns, newest first, each summary once) and take the performing of the phase with the same
   phase_title; count "farm-out" against "in-house"; the majority wins; a tie goes to the newest
   summary that had a non-blank value; if every value was blank, "" with basis "". A non-blank result
   gets basis "analogs" and the line note "performing guessed from analogs".
g. Collect one output line per phase, in this order: proposed_id, hull, project, phase_no,
   phase_title, shop, est_hours_low, est_hours_high, charged_hours_low, charged_hours_high,
   load_hours, week_start, week_end, placement, summaries_used (number of JCNs in EST.usedJcns),
   same_class, top_score (one decimal), analog_jcns (EST.usedJcns), notes (semicolon separated:
   "possible method change" when EST noted one, "thin history" when n < 3, "no analog", "hull not in
   history", "no dates", "planned", "performing guessed from analogs"), source, performing,
   performing_basis. 22 cells.
h. MATERIAL LINES. For a history item after step d: matLines.push(...materialLines(item,
   EST.usedJcns)). For a planned item: if DB.matByJS[extra.job_summary] exists, group its rows by
   phase_no and stock_number, qty = the group's sum of qty (two rows with the same stock number on a phase
   are two orders; never divide by DB.jsCount: hours are shared out over a grouped summary's JCNs, material
   is not), one line per group with phase_title from the planned row with that phase_no (or "Phase " +
   phase_no), qty_low = qty_high = qty, nomenclature from the group's first row, seen_on "1 of 1",
   summaries_used 1, group_size = DB.jsCount[extra.job_summary] or 1, source "planned", analog_jcns "".

materialLines(item, usedJcns): the batch form of the single-JCN material table. Used summaries = the
job_summary of each JCN in usedJcns, each once, newest first; n = their count. For each used summary,
map each of its material rows' phase_no to that summary's phase_title (through DB.phasesByJS; a
material row whose phase_no has no phase row in that summary gets phase_title ""), and group by
phase_title and stock_number. For each summary that has the line, ONE value = the sum of that summary's
qty for the group (its rows with that phase_title and stock_number; two rows are two orders). Never
divide by DB.jsCount: a summary that bundled four JCNs gives each new JCN its whole list, because the
tool cannot tell which parts belonged to which job, and the planner trims a marked list (hours are the
other way round: buildEstimate shares a grouped summary's hours out over its JCNs, and that stays).
qty_low and qty_high are the smallest and the largest of those per-summary values (a line seen on one
summary has qty_low = qty_high). group_size = the largest DB.jsCount among the summaries that carried the
line (1 when none was grouped). nomenclature from the newest summary that had the line. One line per
group: proposed_id, hull, project, job_summary (extra.job_summary or ""), phase_no (look the phase_title
up in DB.phasesByJS[newest used summary] and take that row's phase_no; "" if no row there has that title;
never from the material row), phase_title, stock_number, nomenclature, qty_low, qty_high (one decimal),
seen_on ("k of n"), summaries_used (n), group_size, source "history", analog_jcns (walk usedJcns in order
and keep every JCN whose summary carried the line, so two JCNs of one summary both appear; never a JCN
that is not in usedJcns). 15 cells. Order: by phase_no (blank last), then stock_number.

finishBatch(rows, stats, ms): as before (batch-summary shows items estimated, items with no analog,
lines by placement rule, now including "scheduled", total load_hours by shop as a small table, the
elapsed time; batch-preview
shows the header and the first 50 lines; batch-download gets a Blob or data: URL of the whole CSV,
UTF-8, CRLF, every cell through csvCell, built in an array of lines and joined once), with the header
now the 22 names above, plus: batch-summary also shows items from planning (source planned) and lines
by performing (in-house, farm-out, blank); mat-summary shows "material estimate: N lines for M items";
mat-download gets the material_estimate.csv the same way (header: proposed_id, hull, project,
job_summary, phase_no, phase_title, stock_number, nomenclature, qty_low, qty_high, seen_on,
summaries_used, group_size, source, analog_jcns; 15 names). Keep the material lines in a variable that estimateBatch fills
and finishBatch reads (declare it with var in this block).

No em dashes. Answer with the one <script> block only, and nothing after it.
```

## Prompt D3: check the planned build (same chat as the build; it needs the whole file)

```
I have added MODULE 7 and MODULE 8. Without rewriting the file, check:
1. That MODULE 7's three Core captures sit in their own script block before the block that declares
   buildDB, detectType and loadBatchFiles again (a capture in the same block would take the hoisted new
   function and recurse), and that no const or let name from an earlier block is declared again.
2. That a material file whose columns are NIIN, Nomenclature, Qty (no item column) is detected as
   material and needs no mapping panel, and that DB.matByJS rows then carry stock_number, nomenclature
   and item all filled.
3. That a planned file whose job summaries match proposed items takes those items past findAnalogs
   entirely, that their lines carry source "planned", that a scheduled phase's week_start is the
   Monday of scheduled_start, and that an unscheduled planned phase runs seven days after the previous
   one from planned_start with placement "sequence".
4. That every consumption line has exactly 22 cells and every material line exactly 15, and that no
   Date object reaches csvCell unformatted.
5. That the performing majority rule counts each used summary once and that a tie goes to the newest
   summary with a non-blank value.
6. That MODULE 7a and 7b sit BEFORE the Prompts X hook block in the file if Prompts X are present, so the
   hook wraps D's loader; if they sit after it, say so and tell me to run X2 again.
7. That no material quantity is divided by DB.jsCount anywhere (buildEstimate shares a grouped summary's
   hours out over its JCNs; material lines never do), and that a line from a summary whose DB.jsCount is
   4 carries group_size 4.
Then give me a five-step test with a planned.csv of three made-up rows (two phases scheduled, one not)
and a proposed.csv of four made-up lines: one planned, one screened farm-out with history, one plain
history item, one unknown hull.
```

## Debug prompts

Use the two Debug prompts at the end of `GENAI-PROMPTS-estimator-batch.md` (console error; wrong
result with no error) unchanged.

## What the Resource Map does with the new columns (for series B2, not here)

The map still reads the 19 columns it knows and ignores source, performing and performing_basis. The
leveler work will use performing: a farm-out line should load the contractor's capacity line on the
workforce map, not the organic shop, and the farm-out list should show the lines whose basis is "analogs" as
guesses. That is a series B2 change and is written there, not in these prompts.

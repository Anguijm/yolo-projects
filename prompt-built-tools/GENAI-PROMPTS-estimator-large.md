# Prompts L: the large tasks export (roll it up while it streams)

Version 0.1, 2026-10-27. Built on the owner's report from work the same day: his tasks export comes out of the converter at
1.2 GB (the workbook is 65 MB), and he has already built the estimator, so the fix has to paste into the build he
has. The loader already streams a CSV in 4 MB slices (MODULE 5, Prompt C1); what breaks is holding one object per task
row. Prompt L1 writes one script block, pasted last, that declares the streaming reader again: a history tasks file is
rolled up as it streams to one row per job summary, phase and shop (hours summed, task texts joined, the performing
mark decided, the phase fields kept once), and that is what the mapping panel, buildDB, the browser store, the
estimate and the weight test then see. Every other file passes through unchanged, planning's task-level table
included (it has no charged hours, which is the test). The page never holds the file's text or its task rows, so
memory scales with phases and shops, not tasks. Works on any build that has MODULE 2 and MODULE 5, with or without
Prompts D; nothing else in the file changes. Tested headless: the single-JCN build and the planned stack with L
pasted last give the same estimates, placements and material lines as before on the made-up history, and made-up
tasks files load whole: 300 MB (302,000 task rows) in 8 seconds, 1.2 GB (1.2 million task rows) in 29 seconds, the
page's heap in the hundreds of megabytes, every row read and every hour summed. Test record kept in the private source.

How to run it (the estimator's own chat, or a new chat: the prompt stands alone):
1. Paste Prompt L1. Save the answer (one script block) and paste it into estimator.html as the LAST script, just
   before </body>, after every other module.
2. Paste Prompt L2 and run the five-step test it gives.
3. Load the history as before. A line of its own under the status says how many task rows were rolled up into how
   many rows. The stored history ("Use stored") holds the rolled rows, so the next start is quick.

One grain to know: the roll-up keys on the phase number. The estimate keys a phase on its title, as it always did; a
summary with two phases of the same title and different numbers gives two rolled rows of that title, which the
estimate sums together as before, and their task texts join as two strings instead of one list.

Contracts:

- Input: the same files as before. A file whose columns make it a history tasks table (a job summary column, a shop
  column, an hours column) AND that has a charged hours column is rolled up; every other file is returned row by row
  as before.
- Output of the roll-up: rows keyed by the file's own header names, one per job summary, phase number and shop, in
  order of first appearance: est_hours and charged_hours summed; task the distinct non-blank task texts in file
  order joined with "; "; task_no the first row's; crew_size the first non-blank; performing "farm-out" when any row
  of the group names a contractor, "in-house" when any row has a non-blank performing otherwise, else ""; phase_title,
  description and the four dates the first non-blank; every other column the first row's value.
- Names: streamCSV(file, onProgress) declared again (the later declaration wins), tasksColumns(headers),
  isHistoryTasks(headers), rollUpTasks(headers) (returns the accumulator with add(row) and rows()),
  performingOf(values), internText(s, table) (a flat copy of a field's text, shared when the same text recurs),
  var LAST_ROLLUP. Each phase's description is kept on the first rolled row of its job summary and phase only; the
  other shop rows of that phase carry "" (the loader takes a phase's description from the first non-blank). The line "<file>: N task rows rolled up to M rows (one per job summary,
  phase and shop)" goes into a div with id l-status that the block creates once, right after datastatus (the loader
  rewrites datastatus itself after every load, so a line appended there would be lost).

---

## Prompt L1: the streaming reader that rolls a tasks file up

```
Continue the same file (the offline JCN estimator). Write MODULE L: a single <script> block that I will
paste as the LAST script in the file, just before </body>, after every other module. Its job: the
history's tasks export can be very large (a gigabyte or more, one row per task with the phase fields
repeated on every row), and the page must load it without ever holding one object per task. Plain
global function declarations only (no IIFE, no module, no class, no window assignment); never redeclare
with const or let a name an earlier block declared (declare your own state with var); no em dashes; no
alert, confirm or prompt; no network.

What the file holds (the contract this block relies on; rely on it, not on guesses about the code):
MODULE 2 declared const SCHEMA (one entry per table; SCHEMA.tasks is a plain object of field name to an
array of aliases written without spaces), cleanCol(s) (lower case, everything but letters and digits
removed: a header matches a field when cleanCol(header) equals one of the field's aliases or the field
name with its underscores removed), detectType(headers) (returns "jcn_history", "tasks", "phases",
"material" or null), num(s) (a number from text, 0 when blank), and the element datastatus, which the loader rewrites whole after every
load (so nothing appended to it survives). MODULE 5
declared streamCSV(file, onProgress): it reads a file in slices, parses records as it goes, calls
onProgress(percent) with a number after each slice when a function was given, and resolves to {headers,
data} where headers is the array of trimmed header strings and data an array of row objects keyed by
header. Every loader in the file, the history picker's and the batch picker's, reads through streamCSV,
and the column mapping, buildDB and the browser store run afterwards on what it returns; so a new
streamCSV that returns the same shape changes nothing else. The tasks table's fields: job_summary,
phase_no, shop, est_hours, charged_hours (required) and phase_title, description, task, task_no,
crew_size, performing, planned_start, planned_finish, actual_start, actual_finish (optional). A later
module may have declared normPerforming(s), which maps a performing value to "farm-out", "in-house" or
"".

Write, in this order:
1. var LAST_ROLLUP = null; (the last file's counts, for the status line).
1a. internText(s, table): table is a plain object used as a map from text to its stored copy, one per file.
   If table has s, return the stored copy; otherwise store and return a FLAT copy of s, made as (" " + s).slice(1)
   (a string built by adding characters one at a time is a chain of pieces inside the engine, many times its
   own length; adding one character and slicing it off forces one flat copy). Every field value of every record
   goes through internText before it is used or stored, in the rolled path and in the pass-through path alike,
   so repeated values (shop codes, phase titles, task texts, the standard block of a description, dates) share
   one string and nothing stored is a chain.
2. tasksColumns(headers): a plain object, field name to the matching header or null, for every field
   of SCHEMA.tasks: the first header whose cleanCol equals one of that field's aliases or the field name
   without underscores.
3. isHistoryTasks(headers): true when detectType(headers) === "tasks" AND tasksColumns(headers) finds
   job_summary, phase_no, shop and charged_hours. Planning's task-level table has no charged hours
   column, so it is never rolled up; neither is any other file.
4. performingOf(values): values is an array of the group's performing strings. If normPerforming is
   declared (typeof normPerforming === "function"), map each value through it; otherwise map each value
   yourself: "" stays ""; split the lower-cased text into words on anything that is not a letter or a
   digit; "farm-out" when any word is one of contr, contractor, contract, contracted, ctr, cms, vendor,
   sub, subcontractor, subcontract, subk, farm, farmout, outsource, outsourced; else "in-house". Return
   "farm-out" when any mapped value is "farm-out", else "in-house" when any is "in-house", else "".
5. rollUpTasks(headers): returns an accumulator {add(row), rows(), count} for one file. cols =
   tasksColumns(headers). It keeps a plain object of groups keyed by the trimmed uppercased job_summary,
   "|", num(phase_no), "|", the trimmed uppercased shop, and an array of the keys in order of first
   appearance. add(row): count increments; find or create the group's output row, a plain object keyed
   by the SAME header names as the file, built from the first row of the group (every column copied as
   typed); then fold the row in: est_hours and charged_hours are kept as running numbers (num() of each
   row's value added; write the sums into the output row's hours columns as numbers); the task column
   collects the distinct non-blank trimmed task texts in file order (joined with "; " when rows() is
   called); task_no stays the first row's; crew_size, phase_title, description, planned_start,
   planned_finish, actual_start and actual_finish each take the first non-blank value seen in ITS OWN
   column (write the seven as one loop over their names, never one line per column, so no column reads
   another's); the performing
   column collects every value and is replaced by performingOf(the values) when rows() is called. The
   description is kept ONCE per job summary and phase: the accumulator remembers which job summary and
   phase (the key without the shop) already has a rolled row, and a group that is the second or later
   shop of that phase gets "" in its description column and never takes one (the loader derives a
   phase's description from the first non-blank among the phase's rows, so one copy is enough). rows()
   returns the output rows in order of first appearance, finishes the task and performing columns, and
   must be callable once. Nothing from a row is kept except what the output rows hold.
6. streamCSV(file, onProgress): declared again in full (the later declaration wins). Read the file in
   4 MB slices with await file.slice(start, end).arrayBuffer(), and decode every slice with ONE
   TextDecoder("utf-8") created for the file and called with {stream: true}, so a character split across
   two slices decodes whole (never readAsText on a slice); drop a leading byte-order mark. Parse records
   with a real CSV parser whose state (inside quotes or not, the current field, the current record) is
   carried from one slice to the next: quoted fields, doubled quotes inside quotes, line breaks inside
   quotes, CRLF or LF, and a last record without a line break (flush it at the end). The first record is
   the header row: trim the headers. Create one plain object as the interning table for this file, and
   pass every field of every record through internText(field, table) as the record is completed. Then,
   if isHistoryTasks(headers), create roll = rollUpTasks(headers) and pass every following record, as a
   row object keyed by header, to roll.add and drop it; otherwise push every row object into data as
   before. The table is dropped with the function's locals when the file is done. Call onProgress(Math.round(percent)) after each slice when
   a function was given (guard the call), and let the page breathe between slices (await a resolved
   promise or a zero setTimeout) so the status repaints. At the end: for a rolled file set LAST_ROLLUP =
   {name: file.name, taskRows: roll.count, rows: the output length}, and write the line "<file name>: N
   task rows rolled up to M rows (one per job summary, phase and shop)" into a div with id l-status: create
   that div once if it does not exist yet (document.createElement, inserted right after the datastatus
   element with insertAdjacentElement("afterend")), and set its textContent, because the loader rewrites
   datastatus itself after every load and a line appended there would be lost; then resolve {headers,
   data: roll.rows()}; for any other file resolve {headers, data} and leave l-status as it is.
   Never keep the file's text or the dropped records; never read the whole file at once. Build each
   field by appending to a string as the characters come, but store only what internText returns.
7. Nothing else: do not touch parseCSV, loadFiles, buildDB, the mapping panel, the store or any
   element but the l-status div it creates; this block only declares what is listed above.

Answer with the one <script> block only, starting with <script> and ending with </script>, and nothing
after it.
```

## Prompt L2: check the large-file block (run in the same chat as L1; it needs the block)

```
I have pasted MODULE L as the last script in the file. Without rewriting it, check:
1. That it declares nothing with const or let that an earlier block declared (LAST_ROLLUP is a var), that
   no function is assigned through window, nothing calls alert, confirm or prompt, and that the block
   touches no element but the l-status div it creates next to datastatus.
2. That a file is rolled up only when detectType says tasks AND a charged hours column is found, so
   planning's task table and the jcn history, material, phases, proposed and availabilities files pass
   through unchanged, row by row, keyed by header.
3. That the parser carries its state across slices (a quoted field with a line break that straddles two
   slices still comes out as one field), decodes with one streaming TextDecoder per file, drops a leading
   byte-order mark, and flushes a last record without a line break.
4. That a group's hours are num() sums, its task text the distinct non-blank texts in file order joined
   with "; ", its performing "farm-out" when any row named a contractor, "in-house" when any row had a
   non-blank performing otherwise, else "", and its phase fields the first non-blank, with the description
   on the first rolled row of each job summary and phase only; that the output rows keep the file's header
   names so the mapping panel and buildDB see nothing new; and that every stored field value went through
   internText (a flat copy, shared when the text recurs).
5. That no array of the dropped records or copy of the file's text survives the call.
Then give me a five-step test with a made-up tasks CSV of eight rows: two job summaries, one of them with
two phases, one shop tasked twice in one phase (the two rows must add up to one row), one row whose
performing says CMS and another in the same group that says ORG (the group must come out farm-out), and
the expected three output rows with their sums and texts.
```

## Debug prompts

Use the two Debug prompts at the end of `GENAI-PROMPTS-estimator-batch.md` (console error; wrong result
with no error) unchanged.

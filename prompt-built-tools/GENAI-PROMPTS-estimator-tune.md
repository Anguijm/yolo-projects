# Prompts for GenAI.mil: the weight test for the JCN analog estimator

Version 0.3, 2026-10-25 (v0.1 and v0.2 kept in the private source). v0.3 follows the estimator series v0.7 to the
task-based history: the charged hours of a finished job are summed over its task records (DB.tasksByJS) instead of
phase rows; nothing else in the test changes, because the test compares whole-job hours. Regenerated from this text
on the v0.7 estimator and checked against the Python twin (test record kept in the private source). v0.2 (2026-10-24) read the feature keys from DEFAULT_W instead of
naming fifteen, so the two features the estimator series v0.5 added (class family, hull nearness) are tuned too, and
a weight whose default is 0 gets a ladder of its own. v0.2 also takes the review of PR 69 (the reviewer, 2026-10-24): a
question sees only history received before its own date, with age measured from that date, as a planner at the
time could; the candidate cap is ranked by a neutral weight set rather than the starting weights; the Suggested
column is described as the blend it is. Regenerated from this text with the estimator v0.5 and tested against a Python
twin of every rule (test record kept in the private source). One prompt (T) that adds a weight test to the estimator built by the estimator series
v0.7 (`GENAI-PROMPTS-estimator.md`), plus a check prompt (T2). Run it in the same chat, after Prompt 5 of that
series and before the batch series (prompts C), because the batch tool is built on top of this file and keeps
the test.

What the test does, in plain words. Every finished past job in the loaded history is a question with a known
answer: hide it, let the tool find its closest past jobs among the ones received before it, build its estimate the way the tool
does, and compare with the hours actually charged. The test does that for a few hundred jobs under your weights,
then tries other weights one at a time and keeps what lowers the error, learning on one half of the history and
judging on the other half so a weight set cannot just memorize. It ends in a table: your weights beside the
fitted weights, with the error under each, and a button that adopts the fitted set. You stay the one who
decides.

What it cannot do: tell the right weights from made-up data. On a made-up history it only proves the test runs
and the arithmetic holds. The numbers mean something only on the real exports at work, and they stay there.

Limits, stated in the page: the test judges same-class matching only (other-class fallback rows are not
scored); it needs charged hours on the tasks; a half with fewer than 20 finished jobs stops the test; each
tested job keeps its 500 closest past rows under the starting weights (measured here on a 200,000-row made-up
history with 300 questions per half: about 90 seconds and 330 MB with the cap; without it the browser passed 2.8 GB
and an hour).

---

## Prompt T: the weight test

```
Continue the same file. Write MODULE T: a single <script> block that I will paste over the line
<!-- MODULE T: tune -->. It replaces the stubs tuneRun, adoptWeights and tuneCSV by declaring plain
global functions of the same names (no IIFE, no module, no assignment to window), and it may add more
plain global functions whose names start with tune. Keep every contract name exactly.

Contract reminder: DB.jcns rows have jcn, job_summary, hull, ship_class, swlin, space, equipment_id,
equipment_nomenclature, discrepancy, received_date (a Date or null). DB.tasksByJS[job_summary] is an
array of task rows (one per task of a phase; several shops work one phase) with charged_hours (numbers).
DB.jsCount[job_summary] is a plain object (never .get()). Globals W (the weights, a plain object with the same keys as DEFAULT_W: the feature keys, then
noEquip, recency, minSame),
DICT, FAMILY, TUNE, all declared with let and read by name, never through window. const DEFAULT_W exists.
Functions already in the file: features(nj, j) returning the feature keys, each 0 to 1: the feature keys
are every key of DEFAULT_W except noEquip, recency and minSame, in DEFAULT_W's key order (declare that list
in THIS block as const FEATURE_KEYS = Object.keys(DEFAULT_W).filter(...), once, at the top; no earlier block
declares it; never write the names out); scoreFrom(F, W, age) returning pts * recency * gate exactly as the
matching module does; renderWeights() which redraws the weights panel from W; run(); $(id); esc(s);
csvCell(v); setTuneDownload(); const W_LABELS (plain label per weight key). Elements: tune-n,
tune-band, btn-tune, tune-status, tune-table, btn-adopt, tune-csv, btn-tune-download, f-eid, f-text.

The test, as rules. Every rule is deterministic: no Math.random anywhere, so two runs on the same files
give the same table.
1. First group DB.jcns by job_summary in ONE pass into a plain object (job_summary to array of rows);
   never loop over all of DB.jcns once per summary, because the real history has 200,000 rows.
   Finished summaries: every job_summary in DB.tasksByJS whose tasks have charged_hours summing above
   0 and that has at least one row in that grouping. actualHours(js) = the sum of charged_hours over its
   tasks (every shop, every phase) divided by DB.jsCount[js] (a summary that covered several JCNs is shared out, the same rule the
   estimate uses). The question row of a summary is its row with the smallest jcn string.
2. Halves: sort the finished summaries by job_summary string; the ones at even positions (0, 2, 4, ...)
   are half 1, the odd positions half 2.
3. Questions: for a half, let N = the value of tune-n (at least 1). If the half has at most N
   summaries, every summary is a question; otherwise take every k-th summary starting at position 0,
   where k = floor(count / N), until N are taken. A half with fewer than 20 finished summaries stops the
   test with a message in tune-status.
4. A run is (questions from one half, history = the other half). Run A: questions from half 1, history
   half 2. Run B: questions from half 2, history half 1. The history of a run is the set of DB.jcns rows
   whose job_summary is in that half: build a Set of the half's job summaries and test each row against
   the Set (one pass over DB.jcns per half). A question row with no received_date is dropped from the
   questions (a planner at the time cannot be placed in time); the count of dropped questions goes into
   the final status line. For each question build nj = {hull, cls: ship_class, swlin, space,
   eid: equipment_id, nom: equipment_nomenclature, text: discrepancy} from the question row (the same
   uppercasing the form applies: swlin, space, eid and nom uppercased, text as is).
5. Featurize once per question: for every history row j with j.ship_class equal to nj.cls AND a
   received_date that is a Date strictly before the question's received_date (a job being estimated
   could only see jobs received before it; rows with no date are skipped), F = features(nj, j) and age =
   years from j.received_date to the QUESTION's received_date (never to today). Keep the row when at
   least one feature is above 0. Then cap the kept rows at 500 per question: score each kept row with
   scoreFrom(F, WCAP, age), where WCAP is a copy of DEFAULT_W in which every feature key whose default is
   0 is set to 5 and noEquip is 1 (a neutral set, so a feature the defaults ignore still lifts its rows
   into the cap); sort by that score descending with ties kept in history order (a stable sort), and keep
   only the first 500 (a real history has tens of thousands of same-class rows that share only a digit
   or a deck with the question, and keeping them all costs gigabytes and an hour). Store per kept row: the
   job_summary, the age, and the feature values (a plain object or a typed array, your choice). Store per question: its
   job_summary, its actual hours, and the kept rows. Only same-class rows are used.
6. Evaluate a weight set Wt on a run: for each question, score every kept row with scoreFrom(F, Wt,
   age), keep rows with score above 0, sort by score descending, take the top five rows, and let used =
   their distinct job summaries. If used is empty the question is "no analog" and is excluded from the
   error numbers but counted. Otherwise est = the median of actualHours(js) over used (for an even
   count, the mean of the two middle values), and rel = (est - actual) / actual. The run's result is
   {medianAbs: the median of |rel| over the questions with an estimate, optimistic: the share with rel
   below -band, exact: the share with |rel| at most band, conservative: the share with rel above band,
   n: the count with an estimate, noAnalog: the count without}, where band = tune-band / 100. medianAbs
   and the three shares are FRACTIONS between 0 and 1 (0.257, not 25.7); only the table multiplies them
   by 100 for display, and the 0.001 threshold of the sweep is on those fractions.
7. The sweep, which fits weights on one run: start from W0 (a copy of W). Visit the keys in this exact
   order: FEATURE_KEYS in DEFAULT_W's order, then noEquip, then recency. For a points key with current
   value v, the ladder is [0, v / 2, v * 2] when v is above 0, and [d / 2, d] when v is 0, where d =
   DEFAULT_W[key] when that is above 0, else 5 (so a feature whose default is 0 still gets tried). For noEquip
   the ladder is [1, 0.5, 0.25]. For recency the ladder is [1, 3, 10]. Round each ladder value before
   trying it (points and recency to one decimal, noEquip to two). Try each ladder value in order that
   differs from the current value; evaluate the run; a candidate is better when its medianAbs is lower
   than the best so far by at least 0.001, or equal within 0.001 and its optimistic share is lower. Keep
   the best value for the key before moving to the next key. One pass is one visit of every key; run up
   to three passes, and stop early after a pass that changed nothing. Return the fitted copy.
8. tuneRun(): reads tune-n and tune-band, builds both runs (steps 1 to 5), then: yours = W evaluated on
   run A and on run B; fitA = sweep on run A, evaluated on run A (fitted) and on run B (held out); fitB
   = sweep on run B, evaluated on run B (fitted) and on run A (held out); suggested = for each key the
   mean of fitA[key] and fitB[key] (every FEATURE_KEYS key, noEquip and recency), points rounded to one decimal, noEquip to two decimals, recency to
   one decimal, minSame = W.minSame; evaluated on both runs. Do the work in chunks with setTimeout so the
   page stays responsive: featurize 20 questions per chunk, then one sweep step per chunk; write progress
   to tune-status ("Preparing 140 of 300 jobs, half 1", "Fitting on run A, pass 2, key swlin3 ...").
   When done set TUNE = {suggested, fitA, fitB, results, items}, where suggested, fitA and fitB are
   weight objects (plain copies of W with the fitted values, nothing else inside them; the skeleton's
   Adopt button passes TUNE.suggested straight to adoptWeights), results = {yours: {A, B}, fitA: {A, B},
   fitB: {A, B}, suggested: {A, B}} holds the evaluation results, and items holds the per-item rows for
   the CSV. In results, the key A ALWAYS means "evaluated on run A (the questions of half 1)" and B
   ALWAYS means "evaluated on run B (the questions of half 2)", for every weight set: results.fitB.A is
   fitB judged on run A, which is its held-out result, and results.fitB.B is fitB judged on run B, where
   it was fitted. Write one small function evalBoth(Wt) that returns {A: evaluate on run A, B: evaluate
   on run B} and use it for all four weight sets, so the halves cannot be swapped. Then write "Done (same-class matching only; N questions dropped for a missing date)" to tune-status, enable btn-adopt, draw the
   table, fill tune-csv with tuneCSV() and call setTuneDownload(). Any thrown error goes to tune-status
   as text.
9. The table: set the innerHTML of table tune-table to a thead and a tbody (never a second table inside
   it): columns Weight, Yours, Fitted on A, Fitted on B, Suggested. One row per key of DEFAULT_W except
   minSame, in DEFAULT_W's order,
   labeled W_LABELS[key] when that constant exists, else the key. Then the result rows, one per measure
   and run: "Median error %, run A", "Median error %, run
   B", "Optimistic %, run A", "Optimistic %, run B", "Exact %, run A", "Exact %, run B", "Conservative
   %, run A", "Conservative %, run B", "Jobs with an estimate, run A", "Jobs with an estimate, run B",
   "Jobs with no analog, run A", "Jobs with no analog, run B". Percentages as whole numbers. In the
   Fitted on A column mark the run B cells "(held out)" and in the Fitted on B column mark the run A
   cells "(held out)". Below the table one sentence: "Optimistic means the estimate came in more than
   <band>% under the charged hours, the error that lets work overrun its window."
10. adoptWeights(newW): when newW is null do nothing; otherwise copy into W only the keys that
    DEFAULT_W has, taking each value from newW when newW has it, save W to localStorage under
    "estimator.weights" (try/catch), call renderWeights(), and if f-eid or f-text has a value call
    run().
11. tuneCSV(): header run, job_summary, jcn, hull, ship_class, actual_hours, est_yours, est_suggested,
    analogs_yours, analogs_suggested; one line per question of both runs; CRLF line ends; every cell
    through csvCell; est as one decimal or empty when no analog.
12. No em dashes. No Math.random. No network access.

Answer with the one <script> block only, and nothing after it.
```

## Prompt T2: check the tune module

```
I have pasted MODULE T into the file. Without rewriting it, check these and list each problem with the
exact fix:
1. A question's own job_summary can never be among its candidates (the history is the other half, and
   the halves come from one sorted list split by position).
2. The sweep visits the keys in the stated order with the stated ladders (a key whose default is 0 gets
   [2.5, 5]), keeps a change only when the median error falls by at least 0.001 (or ties and the
   optimistic share falls), and never changes minSame.
3. The suggested weights are evaluated on both runs, and the "held out" marks are on the right cells.
4. adoptWeights writes W, saves it, and redraws the weights panel through renderWeights().
5. Nothing in the module uses Math.random, fetch, eval or window.<global>.
6. After an error written to tune-status, pressing "Run the weight test" again starts a fresh run.
Then tell me what I should see in the table after a run on a small history where most jobs have charged
hours, and what a "no analog" count above zero means.
```

## How to read the result

- The Suggested column is the test's advice: the mean of the two fits. Its error on each run is half in-sample
  (half of the blend was fitted on that run), so read it beside the two held-out cells, which are the honest
  numbers; when all three agree, the weights are a property of the history rather than of one half.
- "Fitted on A" judged on run B is the honest error of those weights; the same column judged on run A is the
  best case, not the expected case.
- A large optimistic share is worse than a large conservative share: optimistic estimates are the ones that
  let work overrun its window.
- If the suggested weights barely beat yours, your idea of the weights was already close. If they differ a
  lot on one key (for example the text weights climb and the space weights fall), that is the test telling
  you which field carries the signal in your history.
- Run it again after the history export grows; the weights are a property of the history, not of the tool.

## Debug prompt

```
I ran the weight test and the status line shows this error, or the console (F12) shows this red text:

<paste it here, exactly>

Find the cause in MODULE T and answer with only the corrected function, named so I can paste it over the
old one. Do not change anything else.
```

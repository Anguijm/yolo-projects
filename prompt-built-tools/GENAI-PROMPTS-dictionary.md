# Prompts K: the dictionary page (harvest the yard's shorthand, decide it once, hand it to the estimator)

Version 0.2, 2026-10-25 (v0.1 kept in the private source). v0.2 adds the boilerplate cutoff the owner chose on 2026-10-25
after describing the real text's shape: a port engineer's standard block (field labels, codes, slashes) opens nearly
every record, and a frequency list would put those tokens first. A token that appears on more than a set share of the
jobs (h-max, 60 percent by default) is boilerplate: it is dropped from the candidates and the phrase pairs at drawing
time, whatever its type, and listed under the summary line so the planner sees what went and can raise the cutoff.
Nothing else in the rules changed. K1 and K2 regenerated from this text; test record kept in the private source. Version 0.1, 2026-10-24, built on the owner's ruling of 2026-10-24 ("Ask me": the dictionary development file is its own
standalone page, separate from the estimator and the weight test) and on his question to Gemini the same day ("Is it
possible to have JavaScript kind of read through a bunch of these long text forms and pull out the things that need to
be expanded on or clarified and added to the dictionary, and then I could go make the dictionary correction"). Gemini's
answer had the three heuristics this page uses (shorthand with slashes or in capitals, frequent tokens that are not
stop words, words seen together) and a review table that writes a portable dictionary file; the page here is that idea
written as a tested prompt series, with the same tokenizer the estimator uses, so what the page decides is what the
matcher sees. Tested: every prompt regenerated from this text by Gemini with no earlier answers in the chat, the page
driven in a headless browser against a Python copy of its rules on a 1,121-row made-up history (34 checks, 0 bad on
the final build) and the estimator's picker on the v0.6 estimator (15 checks); five rounds of K1 and four of K2 to get
there, each failure a sentence here. Test record kept in the private source.

What the page is for. The estimator matches the discrepancy text of a new JCN against the text of past JCNs by shared
words, after an abbreviation dictionary turns the yard's shorthand into words ("lks" to "leaks", "o/h" to "overhaul",
"fmv" to "fire main valve"). Nobody can type that dictionary from memory, and the estimator's own textarea is the
wrong place to build it. This page reads the whole JCN history once, counts every token in the free text, puts the
ones that look like shorthand at the top with three example sentences each, and lets a planner type the long form or
mark the token as a plain word. It writes `dictionary.json` (a plain map, short to long), the same entries as the
`short=long` text the estimator's box takes, and a review file so the work can be resumed and shared. Prompt K4 gives
the estimator a file picker for `dictionary.json`.

The rule that makes the page and the estimator agree: the page splits text exactly the way the estimator's `words()`
does before expansion (lowercase; split on every character that is not a letter, a digit or a slash; drop empty
tokens), uses the same stop list, and never drops the word "depot". A token the page shows is a token the matcher
will compare.

Contracts:

- Input: the JCN history export (CSV; one row per JCN) with a free-text column (aliases discrepancy, discrepancytext,
  narrative, problem, problemdescription, deficiency, remarks, csmpnarrative, description) and, when present, a jcn
  column (aliases jcn, jobcontrolnumber). Column names are compared through cleanCol (lower case, everything but
  letters and digits removed). Nothing else from the file is kept.
- Input, optional: an existing `dictionary.json` (a plain object, token to long form), a `dictionary-review.json`
  written by this page, or a `.txt` of `short=long` lines.
- Output `dictionary.json`: a JSON object, keys the tokens (lowercased, trimmed), values the long forms (trimmed),
  only the tokens with status mapped, keys sorted, two-space indent. This is the file Prompt K4 reads.
- Output, the text: the same entries as `short=long` lines, one per line, sorted, for the estimator's textarea.
- Output `dictionary-review.json`: {savedAt, history (the file name), rows: {token: {long, status, count}}} for every
  token with a status other than pending.
- Element ids: h-file, h-status, h-mapping, d-file, d-status, d-text, btn-harvest, h-top, h-min, h-max, h-search, h-summary,
  h-boiler, h-table, h-pairs, t-text, btn-try, t-out, x-text, btn-copy, dl-json, dl-review.
- Globals (declared with let in the skeleton): TEXTS (array of {jcn, text} after a load), HARVEST (null until a
  harvest; then {tokens: an array of token records, byToken: a plain object token to its jobs count, pairs: an
  array, total: a number}; the h-min threshold is applied when drawing), REVIEW (plain object, token to {long, status, count}), and the const STOP (the stop list).
- Functions: $(id), esc(s), cleanCol(s), tokenize(s), streamCSV(file, onProgress), loadHistory(file),
  loadDictionaryFile(file), applyDText(), harvest(), renderHarvest(), setRow(token, long, status), tryText(),
  exportJSON(), exportText(), exportReview(), saveReview(), restoreReview().

---

## Prompt K1: the page and the two loaders

```
Write a single, self-contained HTML file: a dictionary page for a ship repair planning department. It reads a
JCN history export (CSV) offline, finds the shorthand in the free text, and lets a planner decide what each term
means. Plain HTML, CSS and vanilla JavaScript: no library, no framework, no network call, no CDN, no web font,
no eval, no inline event attributes (onclick=""); add a Content-Security-Policy meta tag with default-src 'none',
script-src 'unsafe-inline', style-src 'unsafe-inline', img-src data:, connect-src 'none', form-action 'none'.
Every function is a plain global function declaration (no IIFE, no module, no class, never assigned through
window); every global is declared with let at the top of the one script block, read and written by name. Light
and dark follow the system (prefers-color-scheme) with system fonts. No em dashes anywhere in the file. Never
use alert, confirm or prompt.

Page sections, in order, with these exact element ids:
1. "1. Load the JCN history": one sentence saying the file never leaves the computer; <input type="file"
   id="h-file" accept=".csv,.txt">; div id h-status; div id h-mapping (empty until needed).
2. "2. Your dictionary so far": <input type="file" id="d-file" accept=".json,.txt"> labeled "dictionary.json,
   dictionary-review.json or a short=long text file (optional)"; div id d-status; a textarea id d-text labeled
   "Decided entries, one per line as short=long (you can type here too)".
3. "3. Harvest the shorthand": a number input id h-top (label "Rows to show", value 200), a number input id
   h-min (label "Least jobs a term must appear on", value 3), a number input id h-max (label "Most jobs a term may appear on, percent", value 60, min 1,
   max 100), a text input id h-search (label "Find a term"),
   a button id btn-harvest "Harvest" that starts disabled, div id h-summary, div id h-boiler, table id h-table, then a small
   heading "Words seen together (for your understanding; the matcher compares single words)" and table id
   h-pairs.
4. "4. Try a sentence": textarea id t-text, button id btn-try "Show the words", div id t-out.
5. "5. Export": textarea id x-text readonly (the short=long text), button id btn-copy "Copy the text",
   <a id="dl-json" download="dictionary.json">Download dictionary.json</a>, <a id="dl-review"
   download="dictionary-review.json">Download dictionary-review.json</a>.

Script block, in this order:
- Globals: let TEXTS = []; let HARVEST = null (the next step sets it to {tokens, byToken, pairs, total}: tokens
  an array of candidate records, byToken a plain object token to its jobs count, pairs an array, total a
  number); let REVIEW = {}; let HISTORY_NAME = ''; and const STOP = new Set of exactly these words: the, a, an, of, to, and, or, is, are, was, were, be, been, in, on, at, for,
  with, by, it, its, this, that, these, those, as, from, request, requested, req, please, properly, ships,
  ship's, force, sf, unable, able, not, no, does, do, did, during, found, per, iaw.
- Helpers: $(id); esc(s) (HTML-escapes &, <, >, " and '); cleanCol(s) (lower case, everything but letters and
  digits removed); tokenize(s): an empty, null or undefined input returns []; otherwise lowercase, split on
  every character that is not a letter, a digit or a slash, drop empty tokens, return the array in order with
  repeats kept (the caller decides about distinctness). This is the estimator's own split rule and must not be
  improved.
- streamCSV(file, onProgress): reads the file in 4 MB slices (file.slice, FileReader.readAsText as UTF-8),
  carries the incomplete last record from one slice to the next (quoted fields with line breaks inside must
  still work, so carry the parser state, not just the partial line), handles quoted fields, doubled quotes,
  CRLF and a leading byte-order mark, calls onProgress(percent) after each slice when a function was given,
  and resolves to {headers, data} where headers is the array of trimmed header strings and data is an array
  of row objects keyed by those header strings. When the file ends without a line break, the characters after
  the last line break are still one record: parse them before resolving.
- loadHistory(file): streamCSV with progress in h-status ("reading <the file's own name>: 37%"); find the text column
  by cleanCol against the aliases discrepancy, discrepancytext, narrative, problem, problemdescription,
  deficiency, remarks, csmpnarrative, description, and the jcn column against jcn, jobcontrolnumber. When no
  text column matches, draw in h-mapping one <select> of the file's headers with the label "Which column
  holds the discrepancy text?" and a button "Use it"; on that click, continue with the chosen column. Fill
  TEXTS with {jcn, text} for every row whose text is not blank (jcn "" when there is no jcn column), set
  HISTORY_NAME to the file name, write "N rows read, M with text" into h-status, enable btn-harvest, and
  drop the parsed rows (keep only TEXTS).
- loadDictionaryFile(file): read the whole file as text. If it parses as JSON and has a "rows" key, it is a
  review file: for each token in rows, setRow(token, rows[token].long, rows[token].status). If it parses as
  JSON and is a plain object of strings, each key is a token: setRow(lowercased trimmed key, trimmed value,
  "mapped"). Otherwise treat it as text: each line with "=" is setRow(left lowercased trimmed, right trimmed,
  "mapped"); lines without "=" are ignored. The file wins over what the page had for the same token. Then
  write "N entries loaded from <name>" into d-status, N being the number of entries read from that file (not
  the size of REVIEW), and call renderHarvest() (which does nothing until a harvest has run).
- setRow(token, long, status): REVIEW[token] = {long: long or "", status: status, count: HARVEST.byToken[token]
  when HARVEST is not null and has the token, else the count already stored, else 0}; a status of "pending" with an empty
  long form deletes the entry instead; then saveReview(), refresh d-text and x-text from REVIEW (the
  mapped entries as short=long, sorted by token), and call exportJSON() and exportReview() (empty stubs until
  the next step; once it is in, the download links stay current after every decision).
- applyDText(): parse every line of d-text with "=" as a mapped entry (left lowercased trimmed, right trimmed)
  through setRow; tokens that were mapped before and are no longer in the textarea go back to pending (setRow
  with "" and "pending"); then renderHarvest(). It is wired on d-text's change event.
- saveReview(): localStorage "dictionary.review" = JSON of REVIEW (try/catch); restoreReview(): the reverse,
  called when the script runs, followed by the d-text and x-text refresh.
- Stubs to be replaced in the next step: harvest(), renderHarvest(), tryText(), exportJSON(), exportText(),
  exportReview() (each an empty function for now).
- Events, each wired through an arrow function that calls the function by name (() => harvest()), never by
  passing the function itself, because the next step replaces the stubs: h-file change calls loadHistory(the
  first file); d-file change calls loadDictionaryFile(the first file); d-text change calls applyDText();
  btn-harvest click calls harvest(); btn-try click calls tryText(); btn-copy click selects x-text and copies
  it (navigator.clipboard.writeText inside the click handler, with a try/catch fallback to select() and
  document.execCommand('copy')); h-search input and h-top change and h-min change and h-max change call renderHarvest(). Wire
  them at the end of the script (the elements exist because the script is at the end of the body); no
  DOMContentLoaded listener.

Answer with the complete HTML file in one code block, and nothing after it.
```

## Prompt K2: the harvest, the review table, the trial sentence, the exports

```
Continue the same file. Replace the six stubs harvest, renderHarvest, tryText, exportJSON, exportText and
exportReview by plain global function declarations of the same names, pasted over the stubs (answer with
those six functions, plus any small helper they need, in one <script>-free code block of JavaScript). Keep
every contract name exactly. Never assign through window; never use alert, confirm or prompt; no em dashes.

Contract reminder: TEXTS is an array of {jcn, text}; HARVEST is null until this step fills it with {tokens,
byToken, pairs, total}; tokenize(s) is the estimator's split (lowercase; split on
every character that is not a letter, a digit or a slash; drop empty tokens; repeats kept); STOP is a Set of
stop words; REVIEW is a plain object token to {long, status, count} with status "mapped", "ignore" or
"pending" (a pending token with no long form is not stored at all); setRow(token, long, status) stores one
decision and refreshes d-text and x-text; HARVEST starts null. Elements h-top, h-min, h-max, h-search, h-summary,
h-boiler, h-table, h-pairs, h-status, t-text, t-out, x-text, dl-json, dl-review. Helpers $(id), esc(s).

1. harvest(): walk TEXTS in chunks of 5000 rows per setTimeout(0) (h-status shows "harvesting: row 40000 of
   183000"), building, per token: jobs (how many TEXTS rows contain the token at least once), caps (true when
   the token appeared in capital letters in the raw text of at least one row: test the original text with a
   case-sensitive search for the token's letters in upper case, only when the token has at least one
   letter), and up to three examples (a snippet of the row's text around the first occurrence, about 90
   characters, each from a different row). Also count adjacent token pairs per row (both tokens kept, see 2),
   once per row (keep a Set of the row's phrases, so a phrase repeated inside one row counts once); a pair is two consecutive tokens of the row AFTER the stop words, the digit-only tokens and the
   one-character tokens are removed (the same tokens that never become candidates; so "fmv 3-100-10 stk"
   gives the pair "fmv stk", and "n / deferred" gives no pair holding "n" or "/"), and the row's first kept
   token pairs with nothing before it (never with null or an empty string). When done: HARVEST = {tokens, byToken, pairs, total}, where tokens is the array of records
   {token, jobs, type, examples} for every token that is not in STOP, not digits only and longer than one
   character (h-min is applied when drawing, not here, so a change of h-min needs no new harvest), byToken a
   plain object from every such token to its jobs count (setRow reads it), pairs the array of {phrase, jobs}
   (top 200 by jobs descending, ties by phrase A to Z; the draw shows at most 50 of them), and total the number of TEXTS rows; then renderHarvest(). The run is deterministic (no random numbers) and never blocks the page
   for more than one chunk.
2. A token is a candidate when it is in HARVEST.tokens, its jobs count is at least the value of h-min at
   drawing time, and its share of the jobs (jobs divided by HARVEST.total, times 100) is not above the value
   of h-max at drawing time. A token above h-max is BOILERPLATE: the fixed text of a form that opens nearly
   every record (field labels, codes repeated on every job). It is never a candidate and never a row of the
   table, whatever its type, and a pair that contains a boilerplate token is not shown. Both thresholds are
   read when drawing, so a change of h-min or h-max needs no new harvest. A token's type is "shorthand" when it contains a slash, or
   has no vowel (a, e, i, o, u, y) and is at most 6 characters long, or appeared in capitals and is at most 5
   characters long; otherwise "word". A pair never contains a stop word, a digit-only token or a one-character token (they are
   removed before the pairs are read off). The word "depot" is never dropped and never a stop word.
3. renderHarvest(): if HARVEST is null, return. Take the candidates (rule 2: jobs at least h-min and not
   boilerplate), order them shorthand
   first, then words, each group by jobs descending then token ascending. Apply h-search (a token contains the typed text, lowercased) and
   show the first h-top rows. h-summary says: "N candidate terms on M jobs; D decided (K mapped, I ignored),
   covering P% of candidate occurrences" where M is HARVEST.total (the jobs read), occurrences are the sum of jobs over candidates and the
   covered share is the sum over decided ones. h-boiler shows one line: "Boilerplate (on more than H% of jobs,
   not listed): token (P%), token (P%), ..." for every token above h-max, by jobs descending, the percents
   without decimals, or "Boilerplate: none" when no token is above h-max. The table h-table (set its innerHTML to a thead and a tbody,
   never a table inside a table): columns Term, Jobs, Type, Examples (the three snippets joined with " | ",
   escaped), Long form (a text input, value REVIEW[token].long or ""), Status (a select with pending, mapped,
   ignore; value from REVIEW or pending). Typing in the long form input (on change) calls setRow(token, the
   value, the value is non-empty ? "mapped" : "pending"); choosing a status calls setRow(token, the current
   long form, the chosen status), and choosing ignore clears the long form. After either, refresh the summary
   line (h-summary) without redrawing the table, so the focus stays where the planner is typing. Wire these
   listeners once per draw, by querying the inputs after the innerHTML is set, with the token in a data-token attribute; never
   with inline event attributes. The pairs table h-pairs shows phrase and jobs for the first 50 entries of HARVEST.pairs in which neither
   token is boilerplate at drawing time. Keep the
   draw fast: build one HTML string and set it once.
4. tryText(): tokens = tokenize(t-text's value); before = those tokens; after = for each token, if REVIEW has
   it with status mapped, the words of its long form (split on spaces), else the token itself; then drop
   STOP words (never "depot"), then distinct in order of first appearance; undecided = the tokens of before
   that are candidates in HARVEST (when HARVEST exists) with no entry in REVIEW. t-out shows three lines:
   "Before: ..." (the tokens exactly as split, stop words included), "After: ..." (what the estimator will
   compare), "Undecided: ..." (or "none").
5. exportText(): returns the short=long lines for every REVIEW token with status mapped, sorted by token,
   joined with "\n"; it is what x-text shows. exportJSON(): builds a plain JSON object of the same entries, each key the token and each
   value the long form as a STRING (never the {long, status, count} record: dictionary.json is what the
   estimator reads as short to long), keys sorted, two-space indent, and sets dl-json's href to a Blob URL of it (type application/json);
   exportReview(): {savedAt: ISO date-time, history: HISTORY_NAME, rows: every REVIEW entry whose status is
   not pending} as JSON to dl-review the same way. setRow() already calls exportJSON() and exportReview()
   after every decision; call both at the end of harvest() too, and once at the end of this code block, so the
   links work even with nothing decided (an empty object).
6. Performance: 200,000 rows with 15 tokens each must harvest in a few seconds; use plain objects as maps,
   count once per row with a Set of the row's distinct tokens, and never search the whole TEXTS array per
   token.

Answer with the code block only, and nothing after it.
```

## Prompt K3: check the dictionary page (run in the same chat; it needs the whole file)

```
I have pasted K2 over the stubs. Without rewriting the file, check:
1. That no function is assigned through window, no element carries an inline event attribute, nothing calls
   alert, confirm or prompt, and the CSP meta tag is present.
2. That tokenize() lowercases, splits on every character that is not a letter, a digit or a slash, and drops
   empty tokens, and nothing else (no stemming, no stop words inside it); that STOP has exactly the listed
   words and never contains depot.
3. That harvest() counts a token once per row, keeps at most three examples per token from different rows,
   counts pairs once per row, and yields to the page between chunks.
4. That a token with status ignore is excluded from dictionary.json and from the short=long text, and that a
   pending token with an empty long form is not stored in REVIEW at all.
5. That loading dictionary.json and then dictionary-review.json merges (the later file wins per token), and
   that typing in d-text and removing a line sends that token back to pending.
6. That the Blob URLs behind dl-json and dl-review are refreshed after every decision.
7. That a token above h-max is absent from the table and from the pairs, listed in h-boiler with its percent,
   and comes back as a candidate when h-max is set to 100, without a new harvest.
Then give me a five-step test with a made-up history of six rows whose text uses three abbreviations, one of
them in capitals, one with a slash, and a fixed label that opens every row.
```

## Prompt K4: the estimator's dictionary picker (run in the ESTIMATOR chat, any time after its Prompt 5)

```
Continue the estimator file. Add a small HTML block and a small <script> block. HTML, pasted right after the
textarea id dict: <div><input type="file" id="dict-file" accept=".json,.txt"> <span id="dict-status"></span></div>
with a label "Load dictionary.json from the dictionary page". Script, pasted as the LAST script in the file:
one plain global function loadDictFile(file) and the change listener $('dict-file').addEventListener('change',
function() { if (this.files[0]) loadDictFile(this.files[0]); }). loadDictFile reads the file as text; if it
parses as JSON and has a "rows" key (a review file from the dictionary page: rows is a plain object keyed by
the token, each value {long, status, count}), take the tokens whose status is "mapped" with their long form;
if it parses as a plain JSON object of strings, take every entry; otherwise read it as text and take every line with "=".
Merge into the lines already in the textarea dict: parse those lines the same way (left lowercased and
trimmed, right trimmed), let the file win for the same key, and write the merged entries back as short=long
lines, sorted, one per line. Then dispatch on the textarea a new Event('input', {bubbles: true}) and a new
Event('change', {bubbles: true}), so the estimator's own listener parses the dictionary, saves it and re-runs
the match; do not call the estimator's internal functions by name. Write "N entries from <file name>, M in
the box now" into dict-status. No new globals, no em dashes, no alert.

Answer with the HTML block and the script block, and nothing after it.
```

## Debug prompts

Use the two Debug prompts at the end of `GENAI-PROMPTS-estimator-batch.md` (console error; wrong result
with no error) unchanged.

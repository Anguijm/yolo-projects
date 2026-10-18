# PDF to CSV

A scanned-document-library to CSV converter that runs as one HTML file, offline. Type the names of the fields you want, choose a folder, and it reads every PDF in it (subfolders included) into one CSV row per record, with a separate list of the files it could not read and why.

What you get:

- `records.csv`: one row per record, one column per mapped field (UTF-8 with BOM so Excel shows non-Latin text)
- `problems.csv`: every file it could not open, that has no text layer, that lacks the main form, or that is
  missing a required field, with the reason
- `needs-ocr.txt`: files with no text layer, to batch through Acrobat Pro's Recognize Text and read again
- `record-text.jsonl`: optional, the main form's text per record, for a retrieval index

Progress is saved in the browser (IndexedDB) as it runs, so a closed tab or a sleeping computer loses nothing:
choose the same folder and press Start, finished files are skipped.

## Safety properties
- No network: the page's Content-Security-Policy sets `connect-src 'none'` and `default-src 'none'`. The
  test harness also blocks and records any request the page attempts (expected: none).
- Reads only files you choose through the browser's folder picker; writes only through normal downloads.
- No `eval`; pdf.js runs with `isEvalSupported: false`.
- CSV cells that start with `= + - @` are prefixed with `'` so Excel cannot run them as formulas (plain numbers such as `-12.5` are left alone).
- Values with commas, quote marks or line breaks are quoted the standard way (RFC 4180, as Excel expects); `dev/check_csv.py` verifies this with Python's own CSV reader.
- The template (field map) holds labels and box positions only, never record content.

## How it reads a record
It reads the PDF's existing text layer with pdf.js (Mozilla's PDF reader, embedded). It does not do OCR
(optical character recognition) itself: a file with no text layer is listed in `needs-ocr.txt`.

**Fields are defined by name.** Type one field per line, the way its label appears on the form. Matching
ignores case, spacing and punctuation; `A | B` gives alternate spellings; a trailing `*` marks a field
required. Each label is searched for on every page of the form, and the value is read beside it or on the
line(s) below. A value ends at the next label (listed or not, when it follows a wide gap or a colon), at a
paragraph gap, or where the type size changes.

**Form styles it reads** (each tested on invented forms): label and value in table cells; two-column grids
(label, value, label, value) with or without colons, including labels that wrap inside their cell; "Label:
value" running text, two or more fields to a line; label above value; labels in capitals; numbered labels
("12. Date Completed:", "(3)", "b)"); dot or underscore leaders ("Title ........ value"); checkboxes
("☒ Yes ☐ No" or "[X] Yes [ ] No" become "Yes"). Dates are copied exactly as written, in whatever format.
A value also ends at labels you did not list when they have a clear label shape (after a wide gap, numbered
with a colon, or with leaders); a line inside a narrative such as "Note: seal replaced" is kept as text.

**Long text.** A value can be as long as the form allows: it carries on across page breaks (skipping a
repeated page header) and keeps its paragraph breaks, which Excel shows inside the cell. Excel cuts any
one cell off at 32,767 characters; the CSV always holds the full text, and any record with a longer field
is listed in `problems.csv` so nothing is silently cut.

**Forms.** The main form needs no anchor: without one, the whole record is searched. Extra form types (for
example a supplementary request form that may appear anywhere, zero or more times) need anchor text, such as
their form number, so each copy can be told apart.

**A sample PDF is optional.** Open one to see what every field reads before running a folder, to click
labels instead of typing them, or to drag a box around a value that has no label at all.

## Moving it to another computer
Copy the file, or open it as text, copy all of it, paste it into a plain text editor such as Notepad and save
it with a name ending in `.html`. The built file is pure ASCII (every non-English character is written as an
escape code), so any encoding works: Notepad's UTF-8, UTF-8 with BOM, UTF-16 and "ANSI", a strict ASCII-only
transfer, and Windows line endings were all tested. The page checks itself when it opens: if the copy is incomplete or
altered, a red notice at the top says so instead of the tool half-working. The file must end with `</html>`.

## For a code reviewer
`src/app.html` is the whole program (the built file adds only the embedded pdf.js). Its script opens with a
reading guide, the security properties to verify, and the known limitations, then runs in eleven numbered
sections: start-up and reader verification; the tuning constants (every threshold, named and explained);
text geometry; label matching; value extraction; one-PDF processing and statuses; storage; the three tabs;
start-up wiring. Things worth checking by hand: the Content-Security-Policy in `<head>`; that the only
`innerHTML` uses set `""`; that every `download()` is of text the page built; and what IndexedDB holds
(extracted field values, until erased from the Results tab).

## Build and test (developer machine only)
    cd dev && npm install                       # pdfjs-dist 4.10.38, puppeteer-core (tests only)
    python3 dev/make_fixtures.py dev/fixtures   # SYNTHETIC records with an answer key
    python3 dev/build.py --version v0.1         # -> dist/pdf-to-csv-v0.1.html
    node dev/test_run.js dist/pdf-to-csv-v0.5.html dev/fixtures dev/test-template.json             # template file
    RH_MODE=names node dev/test_run.js ...                     # field names typed into the page
    RH_MODE=names RH_PARTIAL=1 node dev/test_run.js ...        # only two thirds of the names listed
    RH_DUMP=out.csv RH_DUMP_PROB=problems.csv ...              # also save the CSVs the page produced
    python3 dev/check_csv.py out.csv dev/fixtures/truth.json  # independent check with Python's csv module
    node dev/edge_cases.js dist/pdf-to-csv-v0.5.2.html          # 16 targeted cases from the code review
    python3 dev/make_fixtures.py dev/fixtures-huge --n 8 --seed 11 --huge   # multi-page narrative fields

Only synthetic records are ever used here. Real records stay in the environment they belong to.

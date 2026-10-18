# Record Harvest

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
- CSV cells that start with `= + - @` are prefixed with `'` so Excel cannot run them as formulas.
- The template (field map) holds labels and box positions only, never record content.

## How it reads a record
It reads the PDF's existing text layer with pdf.js (Mozilla's PDF reader, embedded). It does not do OCR
(optical character recognition) itself: a file with no text layer is listed in `needs-ocr.txt`.

**Fields are defined by name.** Type one field per line, the way its label appears on the form. Matching
ignores case, spacing and punctuation; `A | B` gives alternate spellings; a trailing `*` marks a field
required. Each label is searched for on every page of the form, and the value is read beside it or on the
line(s) below. A value ends at the next label (listed or not, when it follows a wide gap or a colon), at a
paragraph gap, or where the type size changes.

**Forms.** The main form needs no anchor: without one, the whole record is searched. Extra form types (for
example a supplementary request form that may appear anywhere, zero or more times) need anchor text, such as
their form number, so each copy can be told apart.

**A sample PDF is optional.** Open one to see what every field reads before running a folder, to click
labels instead of typing them, or to drag a box around a value that has no label at all.

## Build and test (developer machine only)
    cd dev && npm install                       # pdfjs-dist 4.10.38, puppeteer-core (tests only)
    python3 dev/make_fixtures.py dev/fixtures   # SYNTHETIC records with an answer key
    python3 dev/build.py --version v0.1         # -> dist/record-harvest-v0.1.html
    node dev/test_run.js dist/record-harvest-v0.2.html dev/fixtures dev/test-template.json             # template file
    RH_MODE=names node dev/test_run.js ...                     # field names typed into the page
    RH_MODE=names RH_PARTIAL=1 node dev/test_run.js ...        # only two thirds of the names listed

Only synthetic records are ever used here. Real records stay in the environment they belong to.

# References fetched 2026-10-22 (JST) for BAR.md

Fetched with WebFetch on 2026-10-22, between about 17:05 and 17:12 JST, by a research subagent of the yolo session.
Quotes below are short excerpts from the fetched pages. Anything not on this list was not read.

## Set the bar
1. **Camelot**, https://camelot-py.readthedocs.io/en/latest/ (the /en/master/ URL returned 404)
   - Each table has a `parsing_report`: accuracy, whitespace, order, page (example: accuracy 99.02, whitespace 12.24).
   - "discard bad tables based on metrics like accuracy and whitespace"
   - "only works with text-based PDFs and not scanned documents"; an `[ocr]` extra for scans.
   - Links a "comparison with similar libraries and tools" (page itself not read).
2. **reveal.js**, https://revealjs.com/, /speaker-view/, /pdf-export/, /markdown/
   - Speaker view (S key) "includes a timer, preview of the upcoming slide as well as your speaker notes";
     pacing via `defaultTiming` or `totalTime`.
   - Markdown notes after a `Note:` line (separator `notes?:`).
   - PDF export via `?print-pdf` and the browser print dialog; notes can print, including "separate-page";
     "only confirmed to work in" Chrome or Chromium.
   - ESC overview; configurable keyboard; stepped code highlighting such as `[1-2|3|4]`.
   - An external .md file "requires that reveal.js runs from a local web server".
3. **Simon Willison, "Useful patterns for building HTML tools"**, https://simonwillison.net/2025/Dec/10/html-tools/,
   and https://tools.simonwillison.net/colophon (first 100,000 of about 574,000 characters read)
   - "inline JavaScript and CSS in a single HTML file"; "Avoid React, or anything with a build step"; "Keep them small".
   - Copy-to-clipboard buttons; "store a lot of state directly in the URL"; localStorage for larger state.
   - Loads dependencies "from a CDN" (opposite of our offline rule).
   - Colophon: per tool, live link, code link, "AI generated" label, description, every commit with hash, date and
     message, often the prompt and sometimes the LLM transcript.

## Supporting
- **Tabula**, https://tabula.technology/ and https://github.com/tabulapdf/tabula: "Your PDF and the extracted data
  _never_ touch the net" (verifiable through the localhost address); "only works on text-based PDFs, not scanned
  documents"; exports CSV and Excel (JSON mentioned); tabula-java command-line tool for automation.
- **Marp**, https://marp.app/: CommonMark plus "Split pages by horizontal ruler (`---`)"; exports "HTML, PDF and
  PowerPoint files directly"; "3 built-in themes called `default`, `gaia`, and `uncover`"; no presenter view mentioned
  on the homepage.

## Not read (fetch failed)
- SECNAV M-5216.5 (Department of the Navy Correspondence Manual): marines.mil and apps.dtic.mil returned 403 to
  WebFetch and to curl; secnav.navy.mil returned an HTML page, not the PDF.
- sli.dev (Slidev): the page loaded but was mostly navigation; nothing cited.

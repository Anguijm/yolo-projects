# naval-scribe

Browser-based Naval Correspondence formatter per SECNAV M-5216.5. Paste or type correspondence content, get a properly formatted .docx file. Zero dependencies, single HTML file, works offline.

## What it does

Fill in the structured form (From, To, Via, Subject, References, Enclosures, body, signature block) and naval-scribe formats it according to the Department of the Navy Correspondence Manual. Live preview shows the formatted letter. Download generates a valid .docx file with correct margins, fonts, and spacing.

## Features

- Standard Naval Letter and Memorandum formats
- Auto-paragraph numbering (1. a. (1) (a) hierarchy)
- Times New Roman 12pt, 1-inch margins in exported .docx
- SSIC field, DD Mon YYYY date format
- Multi-entry Via/Ref/Encl fields with add/remove
- Live preview with proper spacing
- .docx generated entirely in-browser (hand-rolled OOXML + ZIP)
- localStorage auto-save (survives page refresh)
- CRC32 checksums for ZIP integrity

## How to run

Open `index.html` in any modern browser. No server needed.

## What to change

- Add endorsement format
- Add SSIC code lookup/search
- Add letterhead presets per command
- Add second-page header continuation
- Add classification marking toggle (UNCLASSIFIED/CUI)

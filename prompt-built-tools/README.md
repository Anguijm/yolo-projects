# Prompt-built tools

Planning tools for a ship repair yard, built inside GenAI.mil from prompt series. Each series makes a chat model
(Gemini, GPT or Grok) write one self-contained HTML file that runs offline in a browser on a work computer: no
network, no installation, no libraries. Nothing here carries a real record; every example and every test used
made-up data. Moved from `pdf-to-csv/` on 2026-10-24, where the series had grown up beside the PDF converter.

Start with the build guide: [GENAI-BUILD-GUIDE.md](GENAI-BUILD-GUIDE.md). It says what the tools are, which files
they need, which prompt file to run in which order, how to paste the answers, how to test with made-up data, and
what to do when something breaks.

## The prompt files, in the order the guide runs them

Tool 1, the estimator (one chat):

1. [GENAI-PROMPTS-estimator.md](GENAI-PROMPTS-estimator.md): the page, the history import (one record per task of a
   phase, the way the yard's pulls come), the matching of a new JCN against the past with the reasons and a match
   strength, the estimate per phase and shop and its CSV, the check prompt.
2. [GENAI-PROMPTS-estimator-tune.md](GENAI-PROMPTS-estimator-tune.md): the weight test (hide each finished past
   job, estimate it from the others, fit the weights on one half and judge on the other).
3. [GENAI-PROMPTS-estimator-batch.md](GENAI-PROMPTS-estimator-batch.md): the whole work package at once, one
   consumption CSV out.
4. [GENAI-PROMPTS-estimator-planned.md](GENAI-PROMPTS-estimator-planned.md): planned job summaries (a shop row
   planning left undated takes its phase's window), the contractor mark, the material list.
5. [GENAI-PROMPTS-xlsx.md](GENAI-PROMPTS-xlsx.md): read Excel workbooks directly (optional; superseded by the
   converter page below for new builds).
6. [GENAI-PROMPTS-style.md](GENAI-PROMPTS-style.md): the look, last.
7. [GENAI-PROMPTS-dictionary.md](GENAI-PROMPTS-dictionary.md), Prompt K4 only: a file picker that loads the
   dictionary page's dictionary.json into the estimator's abbreviation box (any time after Prompt 5).
8. [GENAI-PROMPTS-estimator-large.md](GENAI-PROMPTS-estimator-large.md): Prompt L1, pasted last, only when the
   tasks export is huge: it rolls the file up while it streams to one row per job summary, phase and shop, so the
   page never holds one object per task; the numbers downstream do not change. Needs Prompt C1 in the build.

Tool 3, the dictionary page (one chat, short):

1. [GENAI-PROMPTS-dictionary.md](GENAI-PROMPTS-dictionary.md): Prompts K1 to K3. The page reads the JCN history
   once, lists the shorthand in the free text with counts and example sentences, lets a planner type each long
   form or mark a plain word as ignore, drops the form's own boilerplate (a token on more than a set share of the
   jobs, 60 percent by default, listed under the summary instead of ranked), and writes dictionary.json for the
   estimator and a review file to resume.

Tool 4, the workbook converter (one chat, three prompts; the file opens with a how-to-run block):

1. [GENAI-PROMPTS-converter.md](GENAI-PROMPTS-converter.md): Prompts W1 to W3. Excel workbooks in, one CSV per
   sheet out (a workbook with a single sheet is named "<workbook>.csv", several sheets "<workbook> - <sheet>.csv");
   tick the sheets you want and download them as one zip; the same cell rules the tools' reader always applied; the
   tools keep reading CSV.

Tool 5, the resource burn forecast page (one chat, two prompts):

1. [GENAI-PROMPTS-forecast.md](GENAI-PROMPTS-forecast.md): Prompts F1 and F2. One page that forecasts how a job or an
   availability burns a resource week by week from the weeks already charged, with a p10, p50, p90 band from its own
   past errors, the schedule's planned hours as a known future, and an honesty check against "same as last week" on
   weeks it hides from itself. [GENAI-FORECAST-sample.html](GENAI-FORECAST-sample.html) is the page Gemini built from
   F1, tested on [forecast-sample.csv](forecast-sample.csv) (made-up weekly hours for twelve series).

Tool 2, the Resource Map (one chat):

1. [GENAI-PROMPTS-resource-map-analysis.md](GENAI-PROMPTS-resource-map-analysis.md): describe the workforce
   workbooks, structure only.
2. [GENAI-PROMPTS-resource-map.md](GENAI-PROMPTS-resource-map.md): the Resource Map app.
3. [GENAI-PROMPTS-resource-map-leveling.md](GENAI-PROMPTS-resource-map-leveling.md): the leveler (moves, the
   contractor line, zoom, snapshot, automatic level and farm-out).
4. [GENAI-PROMPTS-xlsx.md](GENAI-PROMPTS-xlsx.md) (optional, superseded by the converter page) and
   [GENAI-PROMPTS-style.md](GENAI-PROMPTS-style.md), as above.

## Two design pages

Made-up data; open them in a browser: [the process flow](GENAI-PROCESS-FLOW.html) and
[its loops and graphs](GENAI-LOOPS-AND-GRAPHS.html).

## Rules every file here follows

No real data, names or system names; the series are written so the real column names are learned by a prompt, not
typed into one; every series was tested with made-up data in a headless browser before it was committed; no em
dashes.

Since 2026-10-31 every series is also run against a set of made-up nasty inputs (byte-order marks, CRLF, quoted line
breaks, a two-byte character astride a 4 MB slice, headers and values named constructor or __proto__, merged cells,
every date shape, header-only and empty files, names that differ only by case), and the eight faults that set found
were pinned in the texts and regenerated. On bad data a tool finishes the rest and lists the misses ([TASTE.md](TASTE.md)).

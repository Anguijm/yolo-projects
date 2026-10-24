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

1. [GENAI-PROMPTS-estimator.md](GENAI-PROMPTS-estimator.md): the page, the history import, the matching of a new
   JCN against the past with the reasons and a match strength, the estimate and its CSV, the check prompt.
2. [GENAI-PROMPTS-estimator-tune.md](GENAI-PROMPTS-estimator-tune.md): the weight test (hide each finished past
   job, estimate it from the others, fit the weights on one half and judge on the other).
3. [GENAI-PROMPTS-estimator-batch.md](GENAI-PROMPTS-estimator-batch.md): the whole work package at once, one
   consumption CSV out.
4. [GENAI-PROMPTS-estimator-planned.md](GENAI-PROMPTS-estimator-planned.md): planned job summaries, the
   contractor mark, the material list.
5. [GENAI-PROMPTS-xlsx.md](GENAI-PROMPTS-xlsx.md): read Excel workbooks directly (optional).
6. [GENAI-PROMPTS-style.md](GENAI-PROMPTS-style.md): the look, last.
7. [GENAI-PROMPTS-dictionary.md](GENAI-PROMPTS-dictionary.md), Prompt K4 only: a file picker that loads the
   dictionary page's dictionary.json into the estimator's abbreviation box (any time after Prompt 5).

Tool 3, the dictionary page (one chat, short):

1. [GENAI-PROMPTS-dictionary.md](GENAI-PROMPTS-dictionary.md): Prompts K1 to K3. The page reads the JCN history
   once, lists the shorthand in the free text with counts and example sentences, lets a planner type each long
   form or mark a plain word as ignore, and writes dictionary.json for the estimator and a review file to resume.

Tool 2, the Resource Map (one chat):

1. [GENAI-PROMPTS-resource-map-analysis.md](GENAI-PROMPTS-resource-map-analysis.md): describe the workforce
   workbooks, structure only.
2. [GENAI-PROMPTS-resource-map.md](GENAI-PROMPTS-resource-map.md): the Resource Map app.
3. [GENAI-PROMPTS-resource-map-leveling.md](GENAI-PROMPTS-resource-map-leveling.md): the leveler (moves, the
   contractor line, zoom, snapshot, automatic level and farm-out).
4. [GENAI-PROMPTS-xlsx.md](GENAI-PROMPTS-xlsx.md) and [GENAI-PROMPTS-style.md](GENAI-PROMPTS-style.md), as above.

## Two design pages

Made-up data; open them in a browser: [the process flow](GENAI-PROCESS-FLOW.html) and
[its loops and graphs](GENAI-LOOPS-AND-GRAPHS.html).

## Rules every file here follows

No real data, names or system names; the series are written so the real column names are learned by a prompt, not
typed into one; every series was tested with made-up data in a headless browser before it was committed; no em
dashes.

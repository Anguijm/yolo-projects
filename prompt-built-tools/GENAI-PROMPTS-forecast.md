# Prompts for GenAI.mil: a resource burn forecast page, one offline HTML file

Version 0.1, 2026-10-25. One prompt (F1) that makes the model write a single HTML file, plus a check prompt (F2) and a
debug prompt. The page forecasts how a job or an availability will burn a resource week by week (hours charged by a shop,
material drawn) from the weeks already seen, gives a low, middle and high band (p10, p50, p90), takes the schedule's
planned hours as a known future, and checks itself against "same as last week" on weeks it has hidden from itself. It
was shaped by the ideas in Mistral's Timestral time-series models (quantile forecasts, known-future inputs, honest
baselines); none of their code or weights is used, because the work tool must be one HTML file with no dependencies and
no network. A page built from this prompt by Gemini and tested on made-up data (`GENAI-FORECAST-sample.html`) and the data it
ships with (`forecast-sample.csv`) sit beside this file; the work version is built from this prompt inside the enclave,
with the real column names learned by the column-name prompt at the end.

Rules the prompts carry (the owner's constraints, 2026-10-25): plain HTML, CSS and JavaScript in ONE file; no library,
no CDN, no web font, no fetch, no eval, no model weights, no minified blob; readable source; nothing leaves the
computer; no real record ever goes into the chat.

## How to use

1. Start one new chat (Gemini, GPT or Grok). Paste F1. Copy the answer's code block into Notepad, save as
   `burn-forecast.html` (plain text, UTF-8), open it in the browser.
2. Paste F2 in the same chat and apply any fix it lists. Open the page again.
3. Paste a few weeks of a made-up series first (the prompt's own sample is built in) and read the honesty check before
   trusting anything. Then the real pull: the real column names go through the column-name prompt at the end, never
   the rows.

---

## Prompt F1: the page

```
Write ONE self-contained HTML file for a ship repair planning department: a resource burn forecast page. It
runs offline in Edge or Chrome on a work computer: plain HTML, CSS and vanilla JavaScript in one file, no
library, no CDN, no web font, no fetch or XMLHttpRequest, no eval, no model weights, no minified code;
every function a plain global function declaration with a readable name, so a planner can read the
arithmetic. Put this in the head: <meta http-equiv="Content-Security-Policy" content="default-src 'none';
script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; form-action
'none'">. Light and dark colors through prefers-color-scheme with CSS variables; readable on a phone-width
window; no em dashes anywhere; only plain ASCII inside the JavaScript. The page reads files only through
a textarea and an <input type="file">, and writes only through a textarea and a download link.

What it does: a planner pastes a CSV with one row per week (a date column, a value column such as hours
charged, an optional plan column such as hours the schedule planned for that week, and optional series
columns such as project and shop). Rows that have a plan but no value yet are the future weeks: the page
forecasts them, and the plan is the known future it leans on. The page draws the history, the forecast
and its band, writes a forecast table and a CSV, and runs an honesty check.

Sections, in order, each with a numbered heading:
1. Data: textarea id csvin; button id btn-sample "Load the made-up sample" that fills the textarea with the
   built-in sample (below) and loads it; file input id file; selects id c-date (period column), c-value
   (value column), c-plan (plan column, with a "(none)" option), c-series and c-series2 (series columns,
   each with "(none)"), and id series (the series to forecast: the distinct values of the series columns
   joined with " / ", and nothing else in that select, no "(none)" entry); a status line id datastatus. Guess the columns from their names, keyword by keyword
   in this order so that the first keyword that matches any column wins (week, date, period for the period
   column; charged, actual, hours, value for the value column; planned, plan, scheduled for the plan
   column; project, availability, job for the first series column; shop, trade for the second), and let
   the planner change them.
2. Settings: number inputs id horizon (weeks to forecast when the plan has no future rows, default 8),
   season (season length in weeks, 0 = none, default 0), holdout (weeks hidden for the honesty check,
   default 6); select id useplan (yes / no); button id btn-run "Forecast", disabled until data is loaded;
   status line id runstatus.
3. The forecast: a canvas id chart drawn with the 2D context (no library): the actuals as a solid line,
   the p50 forecast as a line in the accent color, the p10 to p90 band as a filled shape, the plan as a
   dotted line in its own color, the hidden weeks' "same as last week" forecast as a dashed grey line, a
   vertical dotted line where the forecast starts, axes with a few date labels; a legend; a notes line id
   fcnotes; a table id fctable with one row per forecast week: week, plan, p10, p50, p90, where the band
   came from.
4. Honesty check: a verdict box id verdict and a table id checktable (see below).
5. Export: textarea id csvout, button id btn-copy, link id btn-download (download="burn_forecast.csv").
6. How it works, and what it is not: six short bullets in plain words (given below).

The CSV reader: a real parser (quoted fields, doubled quotes, line breaks inside quotes, CRLF, a leading
byte-order mark); header names trimmed; rows keyed by header. Dates: YYYY-MM-DD, MM/DD/YYYY and
DD-MON-YYYY, built with Date.UTC and read with UTC getters, so the week does not shift on a computer in
another time zone; rows sorted by date when every row has one, else kept in file order. The series:
the rows whose series key equals the chosen one; actual weeks are the rows whose value is a number
(their plan held with them, NaN when blank); future weeks are the rows with a plan and no value, in
order; the horizon is the number of future weeks when there are any, else the horizon input; future
week labels are the future rows' dates, else the last actual date plus 7 days per week.

The model, written as functions with these names and exactly these rules:
- hwFit(y, m, a, b, g, phi): Holt-Winters additive with a damped trend. seasonal = m > 1 and y.length >=
  2 * m. Initial state when seasonal: level = mean of the first m values, trend = (mean of the second m
  values minus the first mean) / m, season[i] = y[i] minus the first mean for i < m; otherwise level =
  y[0], trend = y[1] - y[0] (0 with one value), no season. For each t: s = season[t mod m] (0 when not
  seasonal); fitted = level + phi * trend + s; error = y[t] - fitted; newLevel = a * (y[t] - s) + (1 - a)
  * (level + phi * trend); newTrend = b * (newLevel - level) + (1 - b) * phi * trend; when seasonal,
  season[t mod m] = g * (y[t] - newLevel) + (1 - g) * s; then level = newLevel, trend = newTrend, and the
  state {level, trend, season, t} is kept for every t, where season is a copy taken AFTER that step's
  seasonal update (a copy taken before it makes every later forecast one update stale). Returns {fitted,
  errors, states, m, seasonal, a, b, g, phi}.
- hwForecast(state, fit, h): for k = 1..h, damped sum ph = phi + phi^2 + ... + phi^k, forecast = level +
  ph * trend + season[(t + k) mod m] (0 when not seasonal).
- gridSearch(y, m): try alpha in 0.1 to 0.9 by 0.1, beta in 0 to 0.5 by 0.1, gamma in 0 to 0.5 by 0.1
  when seasonal else 0 only, phi in 1 and 0.9, in that nesting order; keep the set with the smallest sum
  of squared one-step errors over t >= m (t >= 1 when not seasonal); a later set replaces an earlier one
  only when its sum is smaller by more than 1e-9.
- ols(y, x): y = a + b * x by least squares over the weeks whose x is a number; null when fewer than 4
  such weeks or x does not vary.
- backtestErrors(y, fit, H): for every origin t from max(2 * m when seasonal, 3) to y.length - 2,
  forecast 1..min(H, y.length - 1 - t) from fit.states[t] and collect y[t + h] - forecast by horizon.
- bands(point, byH, oneStepErrors): per horizon h = 1..H, when at least 10 backtest errors exist, p10 =
  point + the 10th percentile of them, p90 = point + the 90th (percentile with linear interpolation on
  the sorted errors), p50 = point, basis "errors"; otherwise p10/p90 = point minus or plus 1.2816 * sd *
  sqrt(h), basis "normal", where sd = sqrt(sum of the squared one-step errors passed in / (n - 1)), the
  errors squared as they are with no mean subtracted, and the caller passes fit.errors from index m on
  when seasonal, from index 1 on otherwise (the warm-up errors are left out). No p10, p50 or p90 below
  0.
- forecastSeries(y, plan, planFuture, m, H, usePlan): when usePlan and the plan column is chosen, reg =
  ols(y, plan); when reg exists the model is fitted to the residuals y - (a + b * plan) (y - a where plan
  is blank), and the forecast for week h is a + b * planFuture[h] plus the Holt-Winters forecast of the
  residual, with the last known plan carried forward (and a note) when planFuture runs out. Otherwise the
  model is fitted to y itself. Bands come from backtestErrors on the fitted series. The point values are
  returned as computed, a negative one included: the clamp at 0 belongs to bands (p10, p50, p90) and to
  the table and the CSV, which show p50, never to point or to the holdout's misses.
- The honesty check, holdoutCheck: hide the last Ht actual weeks; refit everything on the rest (the plan's
  future for the check is the hidden weeks' plan); forecast Ht weeks with bands; compare with "same as
  last week" (the last unhidden value repeated) and, when a season is set, "same as last season"; report
  the average absolute miss of each in hours a week, the model's miss divided by the naive miss, the
  share of hidden weeks inside p10 to p90 (coverage, target 80 percent), and the average bias (forecast
  minus actual), the misses and the bias computed from the model's point forecasts as forecastSeries
  returns them (not the table's clamped values). "Same as last season" runs only
  when m > 1 and the unhidden weeks hold at least m values. Refuse with {ok: false, reason} when fewer
  than six weeks would remain to fit. The verdict box says in plain words
  whether the model beats "same as last week" (a ratio under 0.9), ties (0.9 to 1.1) or loses, whether
  the band is honest (coverage 70 to 90 percent), too narrow or too wide, and whether the forecast ran
  high or low. The table has one row each for the model's miss, the "same as last week" miss, the "same
  as last season" miss (the word none without a season), the ratio and the coverage, then one row per
  hidden week with actual, forecast, and inside or outside the band (two columns: the label and the
  value).
- run(): builds the series, refuses a series under six actual weeks by writing exactly "This series has N
  weeks of actuals; six is the least the model can work with." to runstatus and returning, forecasts,
  runs the check, writes runstatus (weeks fitted, the chosen weights, the regression line as "charged = a
  + b x planned" when used, the horizon), draws the table, the check, the chart and the CSV, and sets a
  global FC (declared with var at the top as null) with exactly these keys, because a test reads them:
  series (the key), m, usePlan (true only when the regression was used), H, fit: {a, b, g, phi, seasonal},
  reg ({a, b, n} or null), point (array of H numbers), bands (array of H objects {p10, p50, p90, basis,
  n}), futureLabels (array of H strings), planUsed (array of H numbers, NaN when no plan), check (the
  holdout result: {ok, reason} when it could not run, else {ok: true, Ht, fitLen, yHold (the hidden
  actuals), naive (the array of Ht "same as last week" values), maeModel, maeNaive, maeSnaive (NaN
  without a season), coverage (a fraction 0 to 1), bias, model: {point, bands}}),
  notes (array of strings). The verdict text begins with one of these three: "The model beats \"same as
  last week\" on the hidden N weeks", "The model and \"same as last week\" miss the hidden N weeks by
  about the same", "\"Same as last week\" beats the model on the hidden N weeks", and goes on with "...
  percent of the hidden weeks fell inside p10 to p90 (80 is the target)".
- The CSV: header series, week, plan, p10, p50, p90, band_basis, model; one line per forecast week, the
  model cell a short description of the fit ("holt" or "holt-winters m=N", the weights, "with plan" when
  the regression was used); CRLF;
  cells quoted when they hold a comma, a quote or a line break; a cell starting with = + - @ prefixed with
  an apostrophe unless it is a number; the download link's href a data: URL of the same text.

The six "How it works" bullets, in plain words: the model (level and trend smoothing, a season when
asked, a damped trend, weights chosen by a grid on the one-week-ahead error, about a hundred lines of
arithmetic); the plan as a known future (regress the actuals on the plan, smooth the leftover, forecast
the line on the future plan plus the leftover's forecast; the idea behind known-future inputs in
time-series models); the band (from the model's own past errors by horizon, a normal fallback with few
errors); the honesty check (a holdout against "same as last week"; a model that loses is not worth using);
what the page is not (a learned model, several series learning from each other, growth the schedule never
planned, judgment about why a week ran high); and that the real columns are learned by the column-name
prompt, never typed into a chat.

The built-in sample: a JavaScript string named SAMPLE_CSV with this made-up CSV (invent about 30 rows per
series for two series in this shape; no real project, shop or hours):
project,shop,week_start,planned_hours,charged_hours
with weekly rows from 2026-08-03, a plan that ramps over the first fifth, holds, and ramps down over the
last quarter, actuals that follow the plan a week or two late with noise and one dip, and the last 8 rows
of each series with a plan and an empty charged_hours.

Wire events through arrow functions. Answer with the complete file in one code block and nothing after
it.
```

## Prompt F2: check the file

```
Without rewriting the file, check it and list each problem with the exact fix:
1. Every function called but not defined; every element id used in the script that the page does not
   have, and the reverse.
2. hwFit: the season index is t mod m on both the fitted value and the update; the trend update uses the
   new level minus the old; the damped forecast sums phi^k, not k * phi.
3. gridSearch nests alpha, beta, gamma, phi in that order and keeps a candidate only when its sum of
   squares is smaller by more than 1e-9; gamma is tried only when the series is long enough for a season.
4. backtestErrors forecasts from the state after the origin, never from a state that has seen the
   target week; bands use at least 10 errors or fall back to the normal width; no band goes below 0.
5. The holdout refits on the unhidden weeks only (the regression too) and the hidden weeks' plan is the
   known future for the check; "same as last week" is the last unhidden value; coverage counts a hidden
   week inside when p10 <= actual <= p90.
6. Dates built with Date.UTC and read with UTC getters; a textarea's value is read as text; the CSV uses
   CRLF; nothing uses fetch, eval, a library or a web font; no em dashes.
Then give me a five-step test with a ten-week made-up series: what the status line, the table, the
verdict and the chart should show after each step.
```

## Column-name prompt (for the real pull; names only, never rows)

```
My export has these header names: <paste the header row>. Which should be the period column, the value
column, the plan column and the series columns in the page, and do any need a different date format than
YYYY-MM-DD, MM/DD/YYYY or DD-MON-YYYY? Answer with the five choices and, if a format is missing, the one
function to change (toDate) and its new text.
```

## Debug prompt

```
I opened the file and did this: <what you clicked>. The console (F12) shows this error:

<paste the red text here, exactly>

Find the cause and answer with only the corrected function, named so I can paste it over the old one.
```

## What the made-up test showed (2026-10-25)

Two pages were tested against a Python twin of every rule on the same made-up series (20 weeks of actuals, 8 planned
weeks ahead, three settings: history only; with the plan; a season of 4 with the plan): a copy built by hand to this
text, and the page Gemini wrote from Prompt F1 with no code execution (the one beside this file). On that series the
honesty check did its job: history-only smoothing lost to "same as last week" on the six hidden weeks (17.1 against 9.5
hours a week), the plan did not help it there, and a season of 4 beat it (6.7). The band covered all six hidden weeks,
which the verdict called wider than needed. That is what the check is for: a page that reports its own losses. The
test record is kept with the private source.

Gemini needed four runs of Prompt F1 before a fresh run passed all 43 checks, and every miss was a place the text had
left open rather than a rule it broke, so the text above is the fourth: it now says that the season copy in each
state is taken after that step's update, that the normal fallback's spread is the root of the mean square of the
one-step errors after the warm-up with n - 1 and no mean subtracted, that the column guess runs keyword by keyword,
that the series select holds the series and nothing else, that the check table has one row per figure, what the CSV's
model cell holds, and that the clamp at 0 belongs to the bands and the table and never to the point values. If a
model's page misses the twin on a run of your own, the first place to look is a sentence of F1 that can be read two
ways; pin it and run F1 again rather than patching the page.

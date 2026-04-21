# infra-yolo-evals

Advisory pre-filter lenses for YOLO HTML builds. Three scripts added to the repo root; each checks one dimension of quality and prints warnings (never blocks).

## Scripts

### ux_completeness.py
Checks whether a single-file HTML tool handles the states users inevitably encounter.

```
python3 ux_completeness.py <project>/index.html
```

Checks: error-state · empty-state · loading-state · focus-ring · primary-cta

### mobile_usability.py
Checks whether a single-file HTML tool is usable on a phone.

```
python3 mobile_usability.py <project>/index.html
```

Checks: viewport · responsive · tap-target · table-overflow · touch-events

### cult_status.py
Heuristic check for signature-move signals that make a tool memorable.

```
python3 cult_status.py <project>/index.html
```

Checks: animation · canvas-svg · keyboard-shortcuts · realtime · memorable-hook

## Output format

```
[WARN] <check>: <description>
WARNINGS: N
```

Or `PASS` if no issues. Exit code is always 0 (advisory). Exit code 1 = invalid input.

## Usage in the tick prompt pre-filter

Run all three before the council TESTS gate:

```bash
python3 ux_completeness.py <project>/index.html
python3 mobile_usability.py <project>/index.html
python3 cult_status.py <project>/index.html
```

Include warning counts in the `--inline` payload to the TESTS gate so council angles can see the results. These are advisory — the build is not blocked by warnings.

## Known limitations

All checks are file-level regex heuristics. They are intentionally approximate:

- `table-overflow` checks for `overflow-x:auto` anywhere in the file; a precise check would require DOM traversal
- `focus-ring` checks for `outline:none` without `:focus-visible` — inline style exceptions may not be caught
- `cult_status` checks are subjective and expected to evolve over the first 5 builds

Promote checks to hard-fail only after observing false-positive rates across ≥5 real builds.

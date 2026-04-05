# semver-range

Semver range calculator. Paste any npm-compatible range expression and a list of versions — instantly see which match with PASS/FAIL colors and a per-line explanation.

## What it does

- **Range expression**: `^1.2.3`, `~2.4.1`, `>=1.0.0 <2.0.0`, `1.x || >=3.0.0`, `2.0.0 - 3.0.0`, etc.
- **Version list**: one per line, auto-detects leading `v` (e.g. `v1.2.3`)
- **Per-version result**: PASS or FAIL badge + plain-English explanation
- **Range breakdown panel**: shows the expanded comparator form for any range expression
- **6 presets**: caret, tilde, explicit range, union, hyphen, 0.x caret

## Spec coverage

- Caret (`^`): `^1.2.3`, `^0.2.3`, `^0.0.3` with all 0.x edge cases
- Tilde (`~`): `~1.2.3`, `~1.2`, `~1`
- Comparators: `>=`, `>`, `<=`, `<`, `=`
- Wildcards: `1.x`, `1.*`, `1.2.x`
- Hyphen ranges: `1.2.3 - 2.3.4`
- Union (`||`): `1.x || >=3.0.0`
- Pre-release versions: `1.2.3-alpha.1`, `2.0.0-rc.1`
- Build metadata stripped: `1.2.3+build` treated as `1.2.3`

## How to run

Open `index.html` in any browser. No server required.

## What to change

- Add more presets in the `PRESETS` array in the JS
- The `expandCaret` / `expandTilde` functions follow npm semver v7 semantics; adjust edge-case branching if targeting a different registry

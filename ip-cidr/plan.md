# Plan: ip-cidr — IP/CIDR Calculator & Subnet Analyzer

## Goal
Single-file HTML tool for network/devops engineers to dissect IPv4 CIDR blocks instantly. Zero dependencies, pure browser JS.

## Signature Move
**Live binary bitmask race** — as you type each character of a CIDR, the 32-bit binary display updates in real time, with a sliding cyan prefix boundary that animates to the new position. The network bits glow cyan, the host bits fade to dim — you literally see the subnet boundary move. Every subnet splitter row also shows a compressed binary swatch so you can visually spot overlap at a glance. This is the one interaction subnet tools never show you.

## Scope
1. **CIDR Dissector** — enter IP/CIDR (e.g., `192.168.1.0/24`), immediately show:
   - Network address, broadcast address, subnet mask, wildcard mask
   - Usable host count (2^(32-prefix) − 2, handles /31 = 2, /32 = 1)
   - First & last usable host
   - Binary bitmask — 4 octets separated by dots, prefix bits cyan / host bits dim, prefix boundary marker `|`
2. **In-Range Checker** — type any IP; immediately shows INSIDE / OUTSIDE with host index within the subnet
3. **Subnet Splitter** — choose new prefix (must be > current via validated select); show all resulting subnets in a compact scrollable table: network, broadcast, binary swatch, host count
4. **Bulk CIDR Annotator** — paste newline-separated CIDRs; each row shows parsed fields; overlapping pairs highlighted in amber

## JS Safety — 32-bit Unsigned
- All bitwise ops follow with `>>> 0` to force unsigned 32-bit: `(ip32 & mask32) >>> 0`
- `toBin32(n)` uses `(n >>> 0).toString(2).padStart(32, '0')` — no signed surprises
- Division for host count uses `Math.pow(2, 32 - prefix)` rather than bit-shift to avoid sign issues for /0

## Input Validation & Security
- Strict regex before any parsing: `/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?:\/(\d{1,2}))?$/`
- Each octet checked `0–255`; prefix checked `0–32`
- Bulk paste hard-capped at 256 lines to prevent DoS on main thread
- All output inserted via `textContent` / safe DOM APIs — no `innerHTML` with user input

## UX & Empty States
- **Pre-filled default**: page loads with `10.0.0.0/8` already analyzed — user sees the full UI immediately, no blank state
- Input box has placeholder `e.g. 192.168.1.0/24`; validation error shown inline below the input in amber on any invalid input
- Three sub-sections (In-Range, Splitter, Bulk) start collapsed; expand via chevron buttons — reduces overwhelm on first visit
- A subtle inline guide line under each section header explains what to do ("Enter an IP to check if it falls in this subnet")
- Error states: red border + amber inline message; success states: no change (clean)

## Approach
- `parseCIDR(s)` → `{ ip32, net32, mask32, prefix, broadcast32 }` using `>>> 0` throughout
- Live `input` event on CIDR field drives all dissector updates
- Separate `analyzeInRange()`, `analyzeSplit()`, `analyzeBulk()` functions called on their respective inputs
- Sections shown/hidden via `classList.toggle('open')` — CSS handles display

## File Layout
```
ip-cidr/
  index.html   # all HTML + CSS + JS inline, single file
  plan.md      # this file
```

## Design
- Monospace font stack (data/utility tool)
- Accent: `--accent-cyan: #0ff`
- Max-width 480px, centered, scrollable body
- Ghost buttons throughout; one solid cyan "Analyze" button as the only CTA (keyboard users)
- Binary display: prefix bits `color: #0ff`, host bits `color: #333`, pipe `|` separator in `#555`

## Test Strategy
- `test_project.py ip-cidr` — syntax, ID refs, event listeners, brace balance, HTML validity, HTTP 200
- Manual: type `10.0.0.0/8` → verify all 7 fields; type `10.255.255.255` in-range checker → INSIDE; split /8 → /9 gives 2 subnets; bulk paste 3 CIDRs including one overlap
- Edge cases: /0 (whole internet), /32 (single host), /31 (2-host link), bare IP without prefix (show error asking for CIDR), `999.0.0.0/24` (invalid octet)
- XSS check: paste `<script>alert(1)</script>` in bulk — verify no execution

## What "working" means
- Load page → see `10.0.0.0/8` pre-analyzed with binary display, 16M hosts
- Edit to `192.168.1.0/24` → all 7 fields update live, 24 cyan prefix bits visible
- In-range: type `192.168.1.100` → INSIDE (#100 host index); type `10.0.0.1` → OUTSIDE
- Splitter: select /25 → 2 rows; select /26 → 4 rows; all rows show binary swatches
- Bulk: paste 3 valid CIDRs + 1 bad line → 3 parsed rows + 1 error row, overlaps highlighted

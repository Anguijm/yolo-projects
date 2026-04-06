# Plan: ip-cidr — IP/CIDR Calculator & Subnet Analyzer

**Plan revision:** v2 (2026-04-07) — addresses council PLAN gate v1 objections from bugs, security, ui, and guide angles.

## Goal
Single-file HTML tool for network/devops engineers to dissect IPv4 CIDR blocks instantly. Zero dependencies, pure browser JS.

## Signature Move
**Live binary bitmask race** — as you type each character of a CIDR, the 32-bit binary display updates in real time, with a sliding cyan prefix boundary that animates to the new position. The network bits glow cyan, the host bits fade to dim — you literally see the subnet boundary move. Every subnet splitter row also shows a compressed binary swatch so you can visually spot overlap at a glance.

## Scope
1. **CIDR Dissector** — enter IP/CIDR (e.g., `192.168.1.0/24`), immediately show:
   - Network address, broadcast address, subnet mask, wildcard mask
   - Usable host count (edge-case-safe — see §Edge Cases)
   - First & last usable host (or `N/A` for /31, /32, /0)
   - Binary bitmask — 4 octets separated by dots, prefix bits cyan / host bits dim, prefix boundary marker `|`
2. **In-Range Checker** — type any IP; immediately shows INSIDE / OUTSIDE with host index within the subnet
3. **Subnet Splitter** — choose new prefix (must be strictly `>` current); show all resulting subnets in a compact scrollable table: network, broadcast, binary swatch, host count
4. **Bulk CIDR Annotator** — paste newline-separated CIDRs; each row shows parsed fields; overlapping pairs highlighted in amber

---

## §Edge Cases (bugs angle — explicit guards)

Host count formula MUST handle all prefix values without overflow or undefined behavior:

```js
function usableHostCount(prefix) {
  if (prefix === 0)  return { total: 'N/A (entire IPv4 space)', usable: 'N/A' };
  if (prefix === 31) return { total: 2, usable: 2 }; // RFC 3021 point-to-point — both addresses usable
  if (prefix === 32) return { total: 1, usable: 1 }; // single host
  const total = Math.pow(2, 32 - prefix);            // safe up to /0 → 2^32 = 4294967296, within Number precision
  return { total, usable: total - 2 };
}
```

Additional guards:
- `parseCIDR` rejects any prefix outside `0..32` with a specific inline error
- `analyzeSplit()` rejects `newPrefix <= currentPrefix` with a specific inline error: `"Split prefix must be greater than current (/${current})"`
- `analyzeSplit()` caps total generated subnets at 1024 to prevent main-thread freeze (e.g., /8 → /24 would be 65K rows)
- `toBin32(n)`: forced unsigned via `(n >>> 0).toString(2).padStart(32, '0')` — round-trip tested in `testBin32Roundtrip()` for `0`, `1`, `4294967295`, `2147483648`
- First-host / last-host display returns `N/A` for /31, /32, and /0 rather than computing garbage

**Unit assertions baked into load:**
```js
console.assert(usableHostCount(0).total === 'N/A (entire IPv4 space)');
console.assert(usableHostCount(31).total === 2);
console.assert(usableHostCount(32).total === 1);
console.assert(usableHostCount(24).usable === 254);
console.assert(toBin32(4294967295).length === 32);
console.assert(toBin32(4294967295) === '11111111111111111111111111111111');
```
Any failed assertion logs to console and shows a red banner at the top of the page so broken builds are obvious.

---

## §Security (security angle — explicit XSS defense)

**Threat model:** untrusted input from paste handlers, URL fragments, and direct typed input. No network calls, no localStorage of pasted data, no `eval`, no `new Function`.

**Controls:**
1. **`<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'none'; connect-src 'none'; frame-src 'none'; base-uri 'none'; form-action 'none'">`** — inline CSP blocks external loads, image exfil, and form submission
2. **`textContent` only** — every rendering function writes to `el.textContent`, never `el.innerHTML`. One place to audit: a single `render(el, text)` helper used everywhere.
3. **Bulk paste handler** pipeline:
   - Read via `textareaEl.value` (plain string)
   - `.split('\n')` → cap at 256 lines
   - Each line passed to `parseCIDR` which uses strict regex before any parsing
   - Each row built via `document.createElement` + `textContent` assignment
   - **No `innerHTML` anywhere in the bulk path**
4. **Binary swatch rendering** — each bit is a `<span>` created via `createElement('span')` with `textContent = '0' | '1'` and `className = 'bit-net' | 'bit-host'`. No string concatenation into HTML.
5. **Validation-first** — regex match must succeed before any DOM insertion; failed parses render the literal line text via `textContent` inside a muted `<div class="err">` row.

**XSS test matrix (baked into manual test & Test Strategy):**
- `<script>alert(1)</script>` in bulk paste → appears as literal text, no script execution
- `<img src=x onerror=alert(1)>` in bulk paste → literal text, no script execution
- `" onload="alert(1)` in bulk paste → literal text
- `javascript:alert(1)` in CIDR input → rejected by regex, error shown
- Long payload (10k chars in one line) in bulk paste → rejected by line length cap (1024 chars per line)

**No third-party resources:** no CDN fonts, no analytics, no external CSS — everything inlined. The CSP above is self-enforcing for this.

---

## §UI (ui angle — first-use experience)

**All sections expanded by default.** No collapsed sections on first visit. A first-time user sees the full feature set immediately.

**Hero header (always visible, top of page):**
```
ip-cidr — IP/CIDR Calculator & Subnet Analyzer

Dissect a subnet → Check if an IP is inside → Split into smaller subnets → Compare multiple CIDRs
All four tools are visible below. Edit the CIDR to see everything update live.
```

**Section layout (all expanded on load):**
1. **Dissector** — at top, the primary CIDR input with pre-filled `10.0.0.0/8`. The binary bitmask display and all fields visible immediately.
2. **In-Range Checker** — below dissector, always visible. Header: `In-Range Checker — Is an IP inside this subnet?` with a single input prefilled with `10.0.0.1`.
3. **Subnet Splitter** — always visible. Header: `Subnet Splitter — divide this subnet into smaller ones`. Prefix select prefilled one step finer than the current prefix so you see a 2-row result immediately.
4. **Bulk Annotator** — always visible. Header: `Bulk Annotator — paste a list of CIDRs, get overlap detection`. Textarea prefilled with 3 example CIDRs (one overlapping) so the feature's value is obvious.

**Optional collapse for power users** — each section header has a small `[−]` button that collapses just that section. State persists in localStorage so returning users get their preferred layout.

**Affordances:**
- Primary CTA: cyan solid "Analyze" button next to CIDR input (keyboard users hit Enter)
- All interactive elements have visible focus rings (`outline: 2px solid #0ff; outline-offset: 2px`)
- Error states: red border + amber inline message below the offending field
- Success states: clean (no change), results appear live
- Empty state: the pre-filled example means there is no blank state — the page is useful the instant it loads

**Keyboard shortcuts (visible in the shortcut legend, see §Guide):**
- `Enter` in any input → re-analyze that section
- `?` → toggle shortcut legend modal
- `Esc` → close any open modal

**Mobile:** flex-column layout under 600px, tap targets ≥ 44px, binary display wraps at octet boundaries so it stays readable.

---

## §Guide (guide angle — discoverability & self-documentation)

**Visible labels — explicit inventory:**
- Page title: `ip-cidr — IP/CIDR Calculator & Subnet Analyzer`
- Hero text (3 lines, always visible): purpose + tool list (see §UI)
- Section 1: `Dissector — enter a CIDR block to see its components` (visible under section header)
- Section 2: `In-Range Checker — is an IP inside this subnet?` (visible under section header)
- Section 3: `Subnet Splitter — divide this subnet into smaller ones` (visible under section header)
- Section 4: `Bulk Annotator — paste a list of CIDRs, get overlap detection` (visible under section header)
- Every input has an inline placeholder (e.g., `e.g. 192.168.1.0/24`)
- Every input has a one-line help text below it (e.g., `Format: ipv4/prefix, prefix 0–32`)

**Tooltips on the binary display:**
- Hover a cyan bit → tooltip `Network bit (prefix)`
- Hover a dim bit → tooltip `Host bit`
- Hover the `|` separator → tooltip `Prefix boundary — bits to the left identify the network`

**Visible shortcut legend:**
- Persistent bottom-right badge: `[?]  shortcuts`
- Clicking or pressing `?` opens a modal listing: `Enter → analyze`, `?  → this legend`, `Esc → close`, `Ctrl+Click bit → copy binary`
- The legend is also printable via `Ctrl+P` for one-page desk reference

**Specific error messages:**
- `"Invalid CIDR: prefix must be 0–32, got 33"` (not `"Invalid input"`)
- `"Invalid CIDR: octet out of range 0–255, got 999"` in octet 1
- `"Split prefix /24 must be greater than current /24"` (not `"Invalid split"`)
- `"Bulk line 12: missing prefix — did you mean /32?"` (actionable)
- `"Bulk input too large: 512 lines (max 256) — please split"` (specific cap)

**README.md for repeat discovery:**
- First 3 lines: what it does, who it's for, the signature move
- Example: paste `10.0.0.0/8` and see what happens
- Link to `plan.md` for the architecture

**Self-documenting console output** — on load, the console logs:
```
ip-cidr v1 — IP/CIDR Calculator
Try: 10.0.0.0/8, 192.168.1.0/24, 2001:db8::/32 (ipv6 not supported)
Shortcuts: Enter → analyze, ? → legend
```
so power users driving via DevTools console see the tool without reading the page.

---

## Approach
- `parseCIDR(s)` → `{ ip32, net32, mask32, prefix, broadcast32 }` using `>>> 0` throughout
- Live `input` event on CIDR field drives all dissector updates + in-range + splitter (so everything updates together when the base CIDR changes)
- Separate `analyzeInRange()`, `analyzeSplit()`, `analyzeBulk()` functions for their respective inputs
- Single `render(el, text)` helper for all text insertion — one audit point for XSS
- DOM cache pattern: grab all element refs once on `DOMContentLoaded`, reuse
- Sections default-open; `classList.toggle('open')` only on explicit user collapse

## File Layout
```
ip-cidr/
  index.html   # all HTML + CSS + JS inline, single file
  plan.md      # this file (v2)
  README.md    # 3-line hero + example
```

## Design
- Monospace font stack (data/utility tool)
- Accent: `--accent-cyan: #0ff`
- Max-width 720px (wider than v1 so all four sections fit comfortably at default zoom), centered, scrollable body
- Ghost buttons throughout; one solid cyan "Analyze" button as the CTA
- Binary display: prefix bits `color: #0ff`, host bits `color: #333`, pipe `|` separator in `#555`
- Focus rings: `2px solid #0ff` with `2px` offset on all interactive elements

## Test Strategy
- `test_project.py ip-cidr` — syntax, ID refs, event listeners, brace balance, HTML validity, HTTP 200
- `eval_bugs.py ip-cidr` — check for known bug patterns
- `security_scan.py ip-cidr` — verify no innerHTML on user input, no eval, CSP present
- **Console assertions** baked into page load (see §Edge Cases)
- **Manual test matrix:**
  - Dissector: `10.0.0.0/8` → 7 fields populated, 8 cyan bits, 16,777,214 usable hosts
  - Dissector: `192.168.1.0/24` → live update, 24 cyan bits, 254 usable hosts
  - Edge: `0.0.0.0/0` → total N/A, first/last N/A, all 32 bits dim
  - Edge: `10.0.0.1/31` → 2 usable, both addresses
  - Edge: `10.0.0.1/32` → 1 usable, first=last=10.0.0.1
  - Edge: `999.0.0.0/24` → inline error "octet out of range 0–255, got 999"
  - Edge: `10.0.0.0/33` → inline error "prefix must be 0–32, got 33"
  - In-Range: `192.168.1.100` in `192.168.1.0/24` → INSIDE, host index 100
  - In-Range: `10.0.0.1` in `192.168.1.0/24` → OUTSIDE
  - Splitter: /24 → /25 gives 2 rows; /24 → /26 gives 4 rows; /24 → /24 gives inline error; /8 → /24 gives "capped at 1024 rows" notice
  - Bulk: 3 CIDRs including `10.0.0.0/16` and `10.0.5.0/24` → both highlighted as overlapping
  - XSS matrix (see §Security) — all 5 payloads pasted, zero execution, all rendered as literal text
- **Accessibility check:** Tab order flows Dissector → In-Range → Splitter → Bulk → `?` badge; all interactive elements reachable by keyboard; focus rings visible

## What "working" means
- Load page → all four sections visible, `10.0.0.0/8` pre-analyzed, binary display showing 8 cyan + 24 dim bits
- Edit CIDR → all 7 fields + binary + in-range + splitter update live in the same frame
- Edge cases (/0, /31, /32) render correctly without Infinity, NaN, or crash
- XSS test matrix: all 5 payloads render as literal text, zero script execution
- First-time user sees all 4 tools on first render without clicking anything
- Console shows `ip-cidr v1` banner and zero failed assertions
- Keyboard-only user can drive every feature without touching the mouse
- `?` key opens the shortcut legend; `Esc` closes it

## Council gate expectations
- **bugs**: approves — explicit /0, /31, /32 guards; split validation; assertion tests on load
- **security**: approves — CSP meta tag, textContent-only pipeline, XSS test matrix, no innerHTML anywhere
- **ui**: approves — all sections visible on first load, hero text, visible help, focus rings, mobile layout
- **guide**: approves — explicit label inventory, tooltips, shortcut legend, specific error messages, README
- **usefulness**: approved in v1
- **cool**: approved in v1 (live binary bitmask)
- **lessons**: approved in v1

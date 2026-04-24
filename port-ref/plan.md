# port-ref Plan

## Goal
Static single-file PWA port quick-reference tool — type a port number or service name to get IANA service, protocol, privilege boundary warning (<1024), and security flags. Paste docker-compose / k8s YAML for bulk port annotation.

## Scope
**In scope:**
- Embedded port database (~250 well-known ports, IANA + commonly-needed DevOps ports)
- Live search by port number or service name with instant filtering
- Privilege boundary badge for ports < 1024 (root/admin required on Linux)
- Security flags: CLEARTEXT (unencrypted protocol), HIGH RISK (common exploitation target), COMMON CVE (historically exploited services)
- Bulk annotation mode: paste docker-compose or k8s YAML/text, extract port mentions, annotate each
- PWA: manifest + service worker for offline use
- Mobile-first layout with 44px+ touch targets

**Out of scope:**
- Real-time IANA sync or network requests
- User-defined custom port entries
- Network scanning or connection testing
- Port range queries (e.g., "80-90")

## Approach
**Subtask 1 (Port DB):** Build a JS const array PORT_DB with ~250 entries. Each entry: `{p: number, name: string, proto: "TCP"|"UDP"|"TCP/UDP", desc: string, sec: 0|1|2}` where sec=0=none, 1=cleartext/warn, 2=high-risk/danger. Also tag `root: true` for ports < 1024 (auto-computed at runtime from p < 1024).

**Subtask 2 (Search index):** `buildIndex()` creates a Map from lowercase name fragments → port records for O(1) prefix lookup. Also direct numeric lookup by port number.

**Subtask 3 (Search UI):** Single input at top (autofocus). `handleInput()` debounced to 80ms. `search(query)` checks numeric vs. text, returns up to 20 matches. `renderResults(matches)` renders port cards.

**Subtask 4 (Port card):** `renderCard(rec)` returns an HTML string with port number, service name, protocol badge, description, privilege badge (if port < 1024 **AND port !== 0** — port 0 is reserved and exempt from the privilege rule per Edge Cases, resolving the BUGS PLAN-escalation 2026-04-24 contradiction with Subtask 1), security badge (if sec > 0), and security note.

**Subtask 5 (Bulk mode):** Toggle button shows/hides a textarea. `annotateManifest(text)` uses **7 regex patterns** (broadened per BUGS PLAN-escalation 2026-04-24 to cover docker-compose forms the original 5 missed) to extract port numbers from common docker-compose and k8s formats. Patterns are tried in order; first match on a line wins:
  1. `^\s*-\s*"?(\d{1,5}):(\d{1,5})(?:/\w+)?"?` — docker-compose `host:container` mapping with optional `/tcp` `/udp` suffix (extracts host port; container port captured for reference). Covers `- "80:80"`, `- 80:80`, `- "80:80/tcp"`.
  2. `^\s*-\s*"?(\d{1,3}(?:\.\d{1,3}){3}):(\d{1,5}):(\d{1,5})(?:/\w+)?"?` — **NEW**: IP-bound docker-compose (`- "127.0.0.1:80:80"`, `- "0.0.0.0:8080:80/tcp"`). Extracts middle (host) port.
  3. `^\s*-\s*"?(\d{1,5})(?:/\w+)?"?\s*$` — **NEW**: single container port with optional protocol (`- "80"`, `- 80`, `- "80/tcp"`). Anchored to end-of-line so it doesn't accidentally match the leading half of a `host:container` mapping.
  4. `\bport(?:s)?:\s*(\d{1,5})\b` — k8s `port:` / `ports:` scalar values
  5. `\bcontainerPort:\s*(\d{1,5})\b` — k8s containerPort field
  6. `\bhostPort:\s*(\d{1,5})\b` — k8s hostPort field
  7. `\btargetPort:\s*(\d{1,5})\b` — **NEW**: k8s targetPort field (service → endpoint mapping)
  The function deduplicates found port numbers, looks each up in PORT_DB, and renders TWO outputs: (a) the original pasted text line by line, with any line containing a recognized port annotated with `# → SERVICE DESCRIPTION [badge]` appended inline, and (b) a compact summary table of unique ports found. If no ports are recognized, show "NO PORTS FOUND IN RECOGNIZED PATTERNS." Input capped at 50000 chars with a truncation warning.

**Subtask 6 (PWA):** Manifest embedded as `<link rel="manifest" href="data:application/json,...">` for home-screen install. **No service worker** — a single-file HTML with all assets inline is inherently offline-capable (every asset is in the file itself). Service worker via blob URL would create a scope mismatch (blob: origin ≠ file: origin) and is an unnecessary risk. PWA offline capability is achieved by the zero-external-request architecture itself.

**Sequencing:** Port DB → Index → Search → Card → Bulk → PWA (each depends on previous).

## File Layout
- `port-ref/index.html` — entire app, ~650 lines

## Function Map
**File: port-ref/index.html**
- `buildIndex(db)` — builds Map(name → record[]) and Map(port → record) from PORT_DB
- `search(query, idx)` — returns matching records for a query string (numeric or name)
- `renderCard(rec)` — returns HTML string for a single port record card
- `renderResults(matches)` — renders result list into #results
- `annotateManifest(text)` — extracts port numbers from pasted YAML/compose text using **7 regex patterns** (docker-compose host:container, IP-bound host:container, single container port, k8s port/ports/containerPort/hostPort/targetPort), annotates each line and generates summary table
- `handleInput()` — debounced input handler wired to #query
- (No service worker — single-file HTML is inherently offline-capable; blob URL SW removed per security review)

## Security
- No external requests; CSP `default-src 'self' 'unsafe-inline'` per design system
- `annotateManifest()` output rendered via textContent (not innerHTML) to prevent injection from pasted content
- Port cards use innerHTML only with data sourced from PORT_DB (static author-controlled strings); no user input injected
- No localStorage usage; no sensitive data stored
- No service worker (blob URL SW removed — scope mismatch risk and unnecessary for zero-external-dep single file); manifest only for installability
- Bulk annotate output: original text lines with inline annotations rendered as `<pre>` content set via `textContent`, never innerHTML; summary table also uses textContent for all user-input-derived values

## UI
- Top: app title "PORT REF" + subtitle; search input (autofocus, full-width)
- Results area: instant-update card list below input
- Each card: port number (accent color, large), service name, protocol badge, description, privilege badge if <1024, security badge if flagged
- Bulk toggle button shows/hides a secondary panel with textarea + annotate button + two-section output: (1) annotated manifest view — original text with `# → SERVICE [badge]` appended on lines where a port was recognized, rendered in a monospace block; (2) compact summary table of unique ports found
- Empty state: dim "TYPE A PORT NUMBER OR SERVICE NAME"
- No-results state: "NO MATCH — NOT IN WELL-KNOWN RANGE"
- Privilege badge: "ROOT REQUIRED" (amber)
- Security badges: "CLEARTEXT" (amber), "HIGH RISK" (red)

## Guide
- Search placeholder: "Port or service name…"
- Bulk panel header: "BULK ANNOTATE — PASTE DOCKER-COMPOSE OR K8S YAML"
- Annotate button label: "ANNOTATE"
- PWA name: "Port Ref"
- App subtitle: "WELL-KNOWN PORT REFERENCE"

## Edge Cases
- Port 0 (reserved): in database, no privilege badge — **explicit exception in Subtask 4's `renderCard` logic**: `if (port < 1024 && port !== 0) show root-required badge`. This is the authoritative rule; Subtask 4 must honor it.
- Non-numeric partial: "htt" matches "http", "https"
- Numeric exact: "443" returns HTTPS record instantly
- Bulk paste with no recognizable port patterns: "NO PORTS FOUND" message
- Bulk paste >50000 chars: truncate with a warning note
- Multiple protocols same port (e.g., 53 TCP/UDP): single entry with proto=TCP/UDP
- Query cleared: show empty state, not empty results list

## Test Strategy
- `test_project.py port-ref` — syntax check, ID consistency, event listener validation
- Manual: type "80" → HTTP shows with no privilege badge; type "22" → SSH shows with ROOT REQUIRED badge; type "23" → Telnet shows with CLEARTEXT + HIGH RISK badges; type "9999" → NO MATCH
- Bulk: paste "ports:\n  - 22:22\n  - 80:80\n  - 443:443" → annotated table with all three
- Mobile: 375px viewport, touch on cards, input triggers keyboard without overflow

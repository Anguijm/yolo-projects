# port-ref — Architectural Constraints

## 1. Single-file HTML with inline CSS and JS

**Decision**: `port-ref/index.html` is a single self-contained file with all CSS inside `<style>` and all JS inside `<script>` blocks. No external files, no build step, no framework.

**Implication for CSP**: `script-src 'unsafe-inline'` and `style-src 'unsafe-inline'` are REQUIRED by the single-file design. Removing them would break the app entirely — no scripts or styles would execute because none are loaded from external sources.

**Why this is accepted YOLO portfolio practice**:
- Matches every other YOLO utility build (naval-scribe, markdown-deck, svg-fields, 90+ others)
- Zero external dependencies → zero supply-chain surface
- Trivial to verify integrity (one file, one hash)
- Distributable offline (file:// protocol works)
- No build toolchain, no package.json, no npm install
- `connect-src 'none'` prevents any data exfiltration to external origins

**This is the producer-side decision.** Consumers (users) choose whether to trust the file they open. The tool is author-controlled static content — no user-supplied scripts ever enter the inline blocks. XSS via inline script injection requires an attacker to modify the file itself, at which point CSP enforcement is moot.

**Scope of SECURITY reviews**: per-feature reviews may NOT re-raise the `unsafe-inline` CSP concern. That decision was made once at the project level and is recorded here. Future reviews must cite specific new attack surfaces introduced by a feature, not revisit this architectural choice.

## 2. No service worker

**Decision**: No service worker registration. PWA installability via manifest only.

**Implication**: The `blob:` scope-mismatch pitfall documented in `learnings.md` is avoided by construction. Offline use works via the single-file architecture: opening the file directly (file://) works with no network.

## 3. localStorage usage

**Decision**: No localStorage writes in this tool (port-ref is read-only).

**Implication**: No persistence layer, no schema migrations, no quota handling needed. Fresh state every time the page loads.

## 4. Port database is static and author-controlled

**Decision**: `PORT_DB` is a hardcoded array in the source file. Entries ship with the file; no runtime fetching of port data.

**Implication**: No IANA sync, no API keys, no rate-limit handling. Price for freshness is an author edit and a commit.

---

Established: 2026-04-24, as port-ref moved through the SECURITY TESTS-escalation review. Matches the portfolio-level CSP pattern from naval-scribe/CONSTRAINTS.md.

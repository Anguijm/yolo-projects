# ssl-check

X.509 Certificate Inspector — browser-based, zero dependencies.

## What it does

Decode and inspect SSL/TLS certificates entirely in the browser. Two modes:

**PEM Paste (primary — offline/IL2-safe):** Paste one or more PEM-encoded certificates. The tool decodes the X.509 DER structure client-side using a pure-JS ASN.1 parser. Zero network requests.

**Domain Lookup (secondary — network required):** Enter a domain to query the crt.sh certificate transparency log. Returns recent cert issuances with expiry status.

## Fields decoded

- Subject CN / full DN
- Issuer
- Valid From / Valid To
- Expiry countdown with color-coded status (green >30d, amber 7-30d, red <7d or expired)
- Subject Alternative Names (SANs) including wildcard highlighting
- Key algorithm (RSA with key size, EC with curve name, Ed25519)
- Signature algorithm
- Serial number (hex)
- Version

## Chain of Trust visualization

Paste multiple PEM blocks (leaf + intermediates + root) and the tool renders a vertical chain visualization showing cert type (leaf → intermediate CA → root CA) with issuer relationships.

## Presets

Three sample certs built in: Valid (ISRG Root X1), Expired (self-signed localhost 2020), Self-signed (localhost 2024-25).

## Copy JSON

Exports all decoded fields as formatted JSON to clipboard.

---

## COUNCIL PILOT — Dual Gemini Review Results

This project was built with the Council pilot: two sequential Gemini code reviews using `mcp__gemini__gemini-analyze-code`.

### Review 1: Bug Focus

Gemini found 6 real bugs:

| Bug | Fix Applied |
|-----|-------------|
| `parseDateASN1` NaN fallthrough — invalid date showed as VALID | Added `isNaN(d.getTime())` check in `daysUntil()` |
| OID bitwise overflow — `val << 7` overflows 32-bit signed int on large OID components | Changed to `val * 128 + (b & 0x7f)` |
| BMPString (tag 0x1E) read as single bytes instead of UTF-16BE pairs | Added proper UTF-16BE decode (2 bytes per char) |
| `atob()` throws uncaught `DOMException` on invalid Base64 | Wrapped in try/catch, throws human-readable error |
| `parseCertificate` could throw `TypeError` on malformed certs (undefined children) | Added explicit null checks with descriptive errors |
| IPv6 SAN parsing — `b[i+1]` could be undefined on odd-length arrays | Added `!== undefined ? b[i+1] : 0` fallback |

### Review 2: Security Focus

Gemini found 5 security issues that Review 1 **missed entirely**:

| Issue | Fix Applied |
|-------|-------------|
| `esc()` didn't escape single quotes or backticks — latent XSS vector | Added `&#39;` and `&#x60;` replacements |
| No Content Security Policy — inline scripts could exfiltrate data if XSS found | Added CSP meta tag: `connect-src https://crt.sh`, blocks all other external connections |
| Domain input not validated — any string passed to URL construction | Added `/^[a-zA-Z0-9.\-]+$/` regex + 253-char length check |
| `Array.isArray()` not checked on crt.sh response — unexpected format would crash | Changed `!data` check to `!Array.isArray(data)` |
| `c.issuer_name.split()` could throw if value is non-string | Added `typeof c.issuer_name === 'string'` guard |

### What Review 2 caught that Review 1 missed

The security review caught **defense-in-depth issues** that the bug review didn't flag:
- CSP meta tag (bug review doesn't think about browser security policies)
- Single-quote/backtick XSS escape gap (bug review checked functionality, not attack vectors)
- Input format validation (bug review checked runtime errors, not malformed input injection)
- API response type checking for security (bug review noted it as a crash risk but not as an injection vector)

**Council pilot verdict:** Running two focused reviews (bugs → security) caught meaningfully different issue classes. The security review added ~4-5 fixes the bug review would never have surfaced. Worth the extra pass for any tool that handles external data or renders user-provided content.

---

## Tech notes

- Pure JS ASN.1 DER parser — no WebAssembly, no `forge`, no `node-forge`
- Handles: SEQUENCE, SET, INTEGER, OID, UTF8String, PrintableString, IA5String, BMPString, UTCTime, GeneralizedTime, BitString, OctetString, ContextSpecific tags
- OID table covers all common X.509 DN attributes, key algorithms, signature algorithms, and extensions
- Self-signed detection via DN comparison (not AKID/SKID — noted limitation)

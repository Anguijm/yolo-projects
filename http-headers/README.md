# HTTP Header Analyzer

Paste raw HTTP response headers and get an instant security grade (A+ to F), per-header analysis, and a list of missing security headers.

## How to run

Open `index.html` in any browser. No server required, no internet connection needed.

## What it does

- **Security scoring** — 100-point rubric across 12 header categories
- **Letter grade** — A+ (≥95) through F (<40), color-coded
- **Per-header breakdown** — badge (GOOD/WARN/MISS), score chip, click to expand detail
- **Missing headers list** — shows which scored headers are absent and points at stake
- **CORS misconfiguration warning** — detects `*` + `credentials: true` combination
- **Copy Report** — exports a plain-text summary for security audits
- **Load Sample** — fills with a realistic mixed-quality example to demonstrate the tool

## Scored headers

| Header | Max pts | What it checks |
|--------|---------|----------------|
| Content-Security-Policy | 20 | Presence + no unsafe-inline/eval |
| Strict-Transport-Security | 15 | max-age ≥ 31536000, includeSubDomains |
| Set-Cookie | 10 | Secure, HttpOnly, SameSite flags |
| X-Frame-Options | 8 | DENY or SAMEORIGIN |
| X-Content-Type-Options | 8 | nosniff |
| Server (absent = good) | 8 | No version leakage |
| X-Powered-By (absent = good) | 6 | Absence = full points |
| Referrer-Policy | 5 | strict-origin or no-referrer |
| Permissions-Policy | 5 | Any presence |
| Cross-Origin-Opener-Policy | 5 | same-origin |
| Content-Type | 5 | charset specified |
| Cache-Control | 5 | no-store or private |

## Input format

Accepts headers from:
- `curl -I https://example.com`
- Browser DevTools → Network → select request → Headers tab → copy response headers
- Any raw HTTP response header block (HTTP/1.1 and HTTP/2 status lines are auto-skipped)

## What to change

- Add more header rules in the `scoreHeader()` function
- Adjust grade thresholds in `getGrade()`
- Add HPKP or Expect-CT analysis for legacy coverage

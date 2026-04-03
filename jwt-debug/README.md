# jwt-debug

Offline JWT decoder and security auditor. Paste any JWT, instantly see the decoded header, payload, and signature with syntax highlighting and security warnings.

## Run

Open `index.html` in a browser. No server needed.

## What it does

- **Three-color JWT visualization** — header (red), payload (amber), signature (blue)
- **Instant decode** — parses on every keystroke, no submit button
- **Security warnings:**
  - `alg: "none"` → unsigned token, critical alert
  - Expired tokens (exp < now)
  - Tokens not yet valid (nbf > now)
  - No expiry claim (never-expiring token)
  - Long-lived tokens (> 24h)
  - Algorithm info (symmetric vs asymmetric)
- **Standard claims table** — iss, sub, aud, exp, iat, nbf, jti explained in plain English with human-readable timestamps
- **Copy buttons** — copy header or payload JSON
- **Offline-first** — token never leaves your browser (unlike jwt.io)

## What to change

- Add signature verification (requires server-side or WASM for HMAC/RSA)
- Add JWKS endpoint fetching for public key lookup
- Add support for JWE (encrypted tokens)

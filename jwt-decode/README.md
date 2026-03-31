# jwt-decode

Browser-based JWT (JSON Web Token) inspector. Paste any JWT and instantly see the decoded header, payload, and signature — with expiration countdown, claim validation, and timeline visualization. Works fully offline with zero dependencies.

## Features

- **Auto-decode** — paste or type, results appear instantly
- **Header / Payload JSON** — syntax-highlighted, pretty-printed, copyable
- **Signature** — hex dump with note that client-side verification is not performed
- **Expiration countdown** — live timer, turns amber < 5 min, red when expired
- **Timeline visualization** — iat → now → exp progress bar
- **Key claims** — highlights sub, iss, aud, iat, nbf, exp, jti, roles, scope, email, name
- **Validation badges** — EXPIRED, NOT YET VALID, NO SUB, NO ISS
- **Presets** — Valid Sample, Expired, Minimal, Malformed for quick testing
- **IL2-safe** — zero network requests, all processing in-browser

## Usage

Open `index.html` in any modern browser. Paste a JWT into the input field.

## Security note

This tool decodes and inspects JWT structure only. It does not verify cryptographic signatures — a valid-looking decoded token does not mean the signature is authentic. Use server-side libraries for signature verification.

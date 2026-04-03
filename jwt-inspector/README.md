# JWT Inspector

A privacy-first, offline JWT decoder and inspector. No data ever leaves your browser.

## What it does

- **Decodes any JWT** — splits the token into Header, Payload, and Signature parts with color coding (cyan / amber / red)
- **Explains standard claims** — `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti`, `kid`, `alg` get inline descriptions
- **Shows timestamps as dates** — `exp`, `nbf`, `iat` display both raw Unix time and ISO 8601 date
- **Expiration badge** — prominent status: Valid (with time remaining), Expired (with how long ago), Not Yet Valid, or No Expiration
- **HS256/384/512 signature verification** — paste your HMAC secret to verify the signature using the browser's native WebCrypto API
- **URL sharing** — paste a token, the URL hash auto-updates for easy sharing (paste `#<jwt>` in the hash to pre-load)
- **Copy buttons** — copy raw decoded JSON for header or payload

## How to run

Open `index.html` directly in a browser. No server needed.

```
open jwt-inspector/index.html
```

## What I'd change next

- Public key (RSA/EC) upload for RS256/ES256 signature verification
- Base64url encode/decode tool for manually crafting tokens
- Token diff view for comparing two JWTs side by side
- Warning badges for insecure algorithms (none, HS256 with weak secret)

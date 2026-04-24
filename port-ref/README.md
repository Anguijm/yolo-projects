# port-ref

Well-Known Port Quick-Reference — type a port number or service name to get IANA service info, protocol, privilege boundary warning, and security flags. Paste a docker-compose or Kubernetes YAML manifest for bulk port annotation.

## Features

- **Port lookup** — search by number (e.g. `443`) or service name (e.g. `https`, `redis`) with instant fuzzy matching
- **Security badges** — color-coded risk levels: green (safe), amber (caution), red (high risk / never expose)
- **Privilege boundary** — ROOT REQUIRED badge for ports below 1024 (except port 0)
- **Protocol label** — TCP, UDP, or TCP/UDP shown per service
- **Bulk YAML annotation** — paste docker-compose / k8s YAML; each exposed port gets annotated inline with service name, protocol, and risk level
- **Try Example button** — loads a realistic multi-service compose snippet to demo the bulk feature
- **Offline ready** — single file, no network required after opening

## How to run

Open `index.html` directly in any browser. No server required.

## Tech

Single HTML file, zero dependencies. Static port database with 80+ well-known ports. Pure JS lookup and YAML line annotation.

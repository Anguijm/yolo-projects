# ip-cidr — IP/CIDR Calculator & Subnet Analyzer

Single-file HTML tool for network/devops/cloud engineers. Paste any CIDR block and instantly see every subnet field, a live binary bitmask with an animated prefix boundary, an in-range checker, subnet splitter, and bulk overlap detector.

**Signature move:** as you type each character of a CIDR, the 32-bit binary display updates live — cyan prefix bits / dim host bits / `|` prefix boundary marker.

## Quick start

1. Open `index.html` in any browser — no server, no deps.
2. Try `10.0.0.0/8` in the Dissector → see 8 cyan + 24 dim bits, 16,777,214 usable hosts.
3. Paste into Bulk Annotator: `10.0.0.0/8` + `10.0.5.0/24` → overlap highlighted in amber.

See `plan.md` for architecture, edge-case coverage, and security model.

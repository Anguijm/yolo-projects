# Naval Scribe — Structural Constraints

This file declares the architectural constraints that the cron council reviewer
MUST honor when evaluating any naval-scribe feature. Cron workers and council
angles are required to read this file before voting on a plan or implementation
gate for naval-scribe.

These constraints are NOT subject to per-feature renegotiation. They were
decided once, by the project owner, with full understanding of their tradeoffs.

---

## Constraint 1: Zero-dep single-file HTML is irreversible

**Decision:** Naval Scribe is, and will remain, a single `index.html` file with
all scripts and styles inline. No external `.js`, no external `.css`, no build
step, no bundler, no npm dependencies.

**Why:**
- **Portability:** Users email the file, save it to thumb drives, run it
  air-gapped, drop it in SharePoint. A single file works everywhere a browser
  exists.
- **Auditability:** "Right-click → View Source" shows the entire tool. Users
  in restricted environments (which is the entire target audience) need to
  verify what the tool does without trusting external resources.
- **Zero install friction:** Anyone with a browser can use it immediately.
  No node, no python, no permission to install software.

**Implication for Content Security Policy:**
- The CSP MUST use `script-src 'unsafe-inline'` and `style-src 'unsafe-inline'`
  because the constraint above forbids external script/style files.
- The CSP also uses `connect-src 'none'`, `default-src 'none'`, `object-src 'none'`,
  `form-action 'none'` — meaning no remote loads, no XHR, no form posts. The
  practical XSS attack surface is therefore extremely narrow.
- All user input is escaped via `esc()` before rendering with `innerHTML`.

**Council instruction (SECURITY angle):** SECURITY may NOT object to
`unsafe-inline` as a per-feature issue. SECURITY's job for naval-scribe is to
evaluate whether a proposed feature introduces a NEW attack surface — not to
re-litigate the host architecture. Objections of the form "the entire app is
vulnerable because of unsafe-inline" must be treated as out-of-scope and
downgraded to a low-severity advisory. If SECURITY believes a NEW feature
adds a NEW injection point, it must cite the specific code location and the
specific input vector — not the host CSP.

---

## Constraint 2: Naval Scribe is a utility-flagship, exempt from novelty requirements

**Decision:** Naval Scribe is a utility flagship. Its target user is a working
naval officer or civilian DON employee drafting formal correspondence under
deadline. Speed, reliability, and conformance to naval correspondence standards
are the entire product.

**Why:**
- Per `feedback_utility_focus.md` in user memory:
  *"UTILITY is king — no visual toys, build things people bookmark and use."*
- Users do not stumble onto naval-scribe and need to be wowed. They come to
  it intentionally because they have a letter to write. The signature move
  IS reliability + speed + correctness.
- Animated card flips, gamified saving, novel interaction models, distinctive
  visual identities — all of these add cognitive load and time-to-completion
  for a serious tool used under deadline pressure.

**Council instruction (COOL angle):** COOL may NOT require a "signature move"
or "unique interaction model" or "wow moment" for naval-scribe features.
COOL's job for naval-scribe is to evaluate fit-with-identity: does this
feature reinforce or compromise the project's distinctive identity as
*the only zero-dep single-file naval correspondence tool that handles 9 doc
types with proper formatting?* That is the right question. "Is it novel?"
is the wrong question. Objections of the form "needs signature move" or
"too generic" must be treated as out-of-scope and downgraded to a low-
severity advisory.

---

## Constraint 3: Storage is localStorage, not server-side

**Decision:** All user data (drafts, presets, address book, etc.) lives in
`localStorage`. There is no server. There is no sync. There is no account.

**Why:**
- Server-side storage requires hosting, auth, network access, and ongoing
  maintenance — directly contradicting the zero-dep single-file constraint.
- The target audience often works in environments with restricted network
  access. Local-only storage is a feature, not a bug.

**Council instruction (SECURITY angle):** SECURITY may evaluate whether a
specific data class is sensitive enough to warrant a user-facing storage
warning, but may NOT demand server-side storage as a fix. The acceptable
remedy for any "sensitive local storage" concern is an inline warning to
the user (e.g., "Stored locally on this device. Not synced. Not encrypted.").

---

## How to use this file

Cron tick/tock workers MUST read this file before invoking `council.py` for
any naval-scribe gate, and pass its contents via the `--inline` flag along
with the council_focus text. Council angle reviewers see the constraints in
their "Additional context" section and must apply them when scoring.

If you (the council reviewer) believe a constraint here is wrong, do NOT
override it. Instead, raise an APPROVE verdict on the current build and
add an `escalation_request` field to your verdict explaining why the
constraint should be revisited. The project owner will review.

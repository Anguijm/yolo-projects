# Naval Scribe Formatting Guide

Use this guide when drafting naval correspondence with an AI model. Following this format exactly allows Naval Scribe to parse and render your document correctly.

## Standard Naval Letter

```
SSIC: 5216
Date: 2 Apr 2026

From: Commanding Officer, USS EXAMPLE (DDG 00)
To:   Commander, Naval Surface Force, U.S. Pacific Fleet
Via:  (1) Commander, Destroyer Squadron FIFTEEN
      (2) Commander, Naval Surface Group Western Pacific

Subj: REQUEST FOR EXTENSION OF DEPLOYMENT

Ref:  (a) COMNAVSURFPAC ltr 3000 Ser N3/0123 of 15 Mar 2026
      (b) OPNAVINST 3120.32D

Encl: (1) Proposed deployment schedule
      (2) Maintenance status report

1.  Per reference (a), this command requests a 30-day extension of the current deployment period.

2.  The following factors support this request:

    a.  Current operational tasking requires continued presence in the AOR.

    b.  Maintenance status per enclosure (2) supports extended operations.

        (1) All critical systems are fully mission capable.

        (2) Fuel and stores are sufficient for 45 additional days.

3.  Request approval by 15 Apr 2026 to allow adequate planning time.

J. A. SMITH
Captain, U.S. Navy
Commanding Officer

Enclosure (1)

PROPOSED DEPLOYMENT SCHEDULE

[Content of enclosure 1 here — maintains its own internal numbering if any]

Enclosure (2)

MAINTENANCE STATUS REPORT

1.  Hull and mechanical systems: FMC
2.  Combat systems: PMC — radar calibration scheduled for 10 Apr
3.  Communications: FMC

[Enclosures maintain their original numbering — do not renumber]

Copy to:
COMDESRON FIFTEEN
USS EXAMPLE (DDG 00) Operations Department
```

## Key Formatting Rules

### Header Fields
- **SSIC**: 4-5 digit number, right-aligned. Example: `5216`
- **Date**: DD Mon YYYY format. Example: `2 Apr 2026`
- **From/To**: Full formal command name. Example: `Commanding Officer, USS ENTERPRISE (CVN 65)`
- **Via**: Numbered sequentially `(1)`, `(2)`, etc. One per line.
- **Subj**: ALL CAPS. Brief description of the letter's purpose.
- **Ref**: Lettered sequentially `(a)`, `(b)`, etc. Include originator, SSIC, serial, and date.
- **Encl**: Numbered sequentially `(1)`, `(2)`, etc.

### Enclosures
- Listed in the header as `Encl: (1) Title, (2) Title`
- **Enclosure content goes BELOW the signature block**, before Copy To
- Each enclosure starts with `Enclosure (N)` on its own line, followed by the title in ALL CAPS
- Enclosures are NOT numbered by the auto-numbering system — they maintain their own internal structure
- If an enclosure has its own numbered paragraphs, **preserve those numbers exactly as provided** — do not renumber them
- Order: Body → Signature Block → Enclosures → Copy To

### Body Paragraphs
Numbered hierarchically:
```
1.  First-level paragraph.

    a.  Second-level sub-paragraph.

        (1) Third-level sub-paragraph.

            (a) Fourth-level sub-paragraph.
```

Rules:
- **Blank line between paragraphs** at the same level.
- **4 spaces** of additional indent per level.
- If you create sub-paragraphs, you must have **at least two** at each level.
- Single-paragraph letters do NOT get a number.

### Signature Block
```
J. A. SMITH
Captain, U.S. Navy
Commanding Officer
```
- Name in ALL CAPS (first initial, middle initial, last name).
- Rank/rate on second line using full title.
- Billet title on third line (optional).
- For civilian signers: use GS grade or SES/SL/ST title instead of military rank.

### Copy To
```
Copy to:
COMDESRON FIFTEEN
USS EXAMPLE Operations Department
```
One recipient per line.

## Memorandum

Same as standard letter but:
- Add `MEMORANDUM` centered at top
- No Via line needed (optional)
- No Ref/Encl needed (add only if relevant)

## Endorsement

```
FIRST ENDORSEMENT

From: Commander, Destroyer Squadron FIFTEEN
To:   Commander, Naval Surface Force, U.S. Pacific Fleet

Subj: REQUEST FOR EXTENSION OF DEPLOYMENT

1.  Forwarded, recommending approval.

R. B. JONES
Captain, U.S. Navy
Commander, Destroyer Squadron FIFTEEN
```

- Endorsement number: `FIRST`, `SECOND`, `THIRD`, etc.
- Subject MUST match the original letter's subject exactly.
- "Forwarded" is sufficient if no comment needed.

## Memorandum of Agreement (MOA)

```
MEMORANDUM OF AGREEMENT

BETWEEN
COMMANDING OFFICER, NAVAL STATION NORFOLK
AND
COMMANDING OFFICER, USS ENTERPRISE (CVN 65)

Serial Numbers:
NAVSTA Norfolk: N00024-26-MOA-0001
USS Enterprise: N00065-26-MOA-0042

Subj: SHARED USE OF PIER 12 FACILITIES

Ref:  (a) OPNAVINST 11010.20G

Effective Date: Upon signature
Duration: 5 years from effective date

1.  Purpose. This memorandum establishes the terms for shared use of Pier 12 facilities.

2.  Scope. This agreement applies to all tenant commands assigned berthing at Pier 12.

    a.  Scheduling shall be coordinated through the Port Operations Center.

    b.  Priority shall be given to deploying units.

3.  Responsibilities.

    a.  NAVSTA Norfolk shall:

        (1) Maintain pier infrastructure.

        (2) Provide shore power connections.

    b.  USS Enterprise shall:

        (1) Coordinate arrival/departure schedules 72 hours in advance.

        (2) Comply with all environmental protection requirements.


_______________________________
J. A. SMITH
Captain, U.S. Navy
Commanding Officer, Naval Station Norfolk
N00024-26-MOA-0001

_______________________________
R. B. JONES  
Captain, U.S. Navy
Commanding Officer, USS Enterprise (CVN 65)
N00065-26-MOA-0042
```

- List all parties with `BETWEEN` / `AND`
- Each party gets a serial number
- Each party gets a separate signature block with their serial number
- References and enclosures follow standard lettering/numbering

## Point Paper

```
Date: 2 Apr 2026

POINT PAPER
PIER 12 FACILITY SHARING ARRANGEMENT

- Current berthing capacity at Pier 12 supports 3 surface combatants simultaneously
- Demand exceeds capacity by 40% during deployment surge periods (Mar-Sep)
- Proposed scheduling system reduces conflicts by routing requests through Port Ops
- Cost: $0 — uses existing infrastructure and personnel
- Risk: Low — no structural modifications required
- Recommendation: Approve the MOA and implement scheduling by 1 May 2026
```

- Bulletized format, one point per line
- Centered title (ALL CAPS after `POINT PAPER`)
- No From/To/Via structure
- Should fit on one page
- No signature block

## Action Memo

```
SSIC: 5216
Date: 2 Apr 2026

ACTION MEMO

From: N3 Operations Officer
To:   Commanding Officer

Subj: PIER 12 SCHEDULING CONFLICT RESOLUTION

BLUF: Three commands are requesting simultaneous berth at Pier 12 during the March surge. A shared-use MOA resolves this without additional infrastructure costs.

- Recommend executing MOA between NAVSTA Norfolk and affected commands
- Port Operations Center to manage scheduling via existing INPORT system
- No additional manning or budget required
- TAB A: Draft MOA for review
- TAB B: Current berth utilization data

RECOMMENDATION: Sign the attached MOA (TAB A) and direct Port Ops to implement scheduling by 1 May 2026.

J. A. SMITH
Commander, U.S. Navy
N3 Operations Officer
```

- `ACTION MEMO` centered at top
- BLUF (Bottom Line Up Front) immediately after subject
- Bulletized action items
- Label supporting documents as TAB A, TAB B, etc.
- Recommendation statement at end
- Concise — should fit on one page

## Classification Markings

If the document requires classification, add the marking as the first line:

```
SECRET

SSIC: 5216
Date: 2 Apr 2026
...
```

Valid markings: `UNCLASSIFIED`, `CUI`, `FOUO`, `SECRET`, `TOP SECRET`

Omit the marking line entirely for unclassified documents with no marking requirement.

## Tables in Body Text

Use markdown table syntax within body paragraphs:

```
3.  Current readiness status:

| System | Status | Last Inspection |
| ------ | ------ | --------------- |
| Propulsion | FMC | 15 Mar 2026 |
| Combat Systems | PMC | 10 Mar 2026 |
| Communications | FMC | 12 Mar 2026 |
```

## References Format

References should follow this format:
```
Ref:  (a) COMNAVSURFPAC ltr 5216 Ser N3/0123 of 15 Mar 2026
      (b) OPNAVINST 3120.32D
      (c) SECNAVINST 5216.5E
      (d) USS EXAMPLE ltr 1000 Ser CO/0456 of 1 Feb 2026
```

Pattern: `[Originator] [type] [SSIC] Ser [office/serial] of [date]`
- For instructions/directives: just the instruction number (e.g., `OPNAVINST 3120.32D`)
- For letters: include originator, SSIC, serial number, and date

## Tips for AI Models

1. **Always use DD Mon YYYY** for dates (e.g., `2 Apr 2026`, not `April 2, 2026`)
2. **Subject lines are ALL CAPS** — no exceptions
3. **4 spaces per indent level** in body paragraphs
4. **Blank line between paragraphs** at the same level
5. **References use lowercase letters** in parentheses: `(a)`, `(b)`, `(c)`
6. **Enclosures use numbers** in parentheses: `(1)`, `(2)`, `(3)`
7. **Via uses numbers** in parentheses: `(1)`, `(2)` — chain of command order
8. **Names in signature blocks are ALL CAPS**: `J. A. SMITH`
9. **Rank uses full title**: `Captain, U.S. Navy` not `CAPT, USN`
10. **One blank line** between header sections (From→To→Via, then gap, Subj, then gap, Ref, then gap, Encl, then gap, Body)
11. **Enclosure CONTENT goes AFTER the signature block** — not inline in the body. The body REFERENCES enclosures (e.g., "per enclosure (1)"), the actual enclosure content appears below the signature.
12. **Never renumber enclosure content** — if an enclosure has its own numbered list (1, 2, 3), preserve those numbers exactly. The auto-numbering system only applies to the letter body, not to enclosures.
13. **Document order**: Header → Body → Signature Block → Enclosures → Copy To

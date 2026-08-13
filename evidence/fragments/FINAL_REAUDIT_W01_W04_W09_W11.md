# Final independent semantic re-audit: W01--W04 and W09--W11

Audit date: 2026-08-13. Scope was read-only except for this report. The current
English W01, W02, W03, W04, W09, W10, W11, and master were compared line by
line with the frozen files of the same names under
`source/french_diplomatic/`. The current records in `source/critical_baseline/`
and the earlier audit fragments `AUDIT_W01_W04_W10.md` and
`AUDIT_W09_W11.md` were reconciled. No remote, DOI, source, translation,
master, ledger, or metadata action was taken.

## Verdict

**FAIL -- PASS withheld.** No substantive translation, mathematical-display,
quantifier, negation, name/date/reference, or source-page-topology error remains
in the seven audited English components. All findings from the two earlier
audits have been substantively repaired. Three publication-apparatus/evidence
defects remain: two medium-severity reader-facing contradictions and one
low-severity alignment-ledger omission.

Severity:

- **High:** changes or seriously obscures historical or mathematical meaning.
- **Medium:** gives a materially false critical classification or reader-facing
  account of the apparatus.
- **Low:** traceability/evidence defect without loss of translated content.

## Findings

### F01 -- Medium -- W09 renders a dagger on a non-source control defect but supplies no promised critical note

**Anchors:**

- `source/english/GAL1897_EN_MODERN_READER.tex:50` and `:92`
- `source/english/tex/wrappers/W09.tex:16`
- `source/english/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:50`

The master tells readers that every dagger marks a proved or suspected defect
and that a nearby boxed GPT Critical Note supplies the stable ID, correction or
qualification, evidence, transmission status, and disposition. W09 instead
renders `\GalControlDefect{this}{W09-CD001}` as `this` plus a dagger. The
English word “this” is the correct translation of the frozen French `cette`;
`W09-CD001` records a control-text defect, not an error in the 1897 witness or
the English translation. There is no `\GalCriticalNote{W09-CD001}{...}` anywhere
in the component. The mark therefore falsely suggests a source/translation
defect and violates the master’s explanation of its own apparatus.

Required resolution: either render `\GalControlDefect` without the critical
dagger in this reader, or add an expressly labelled control-only note and revise
the master’s marker claim so that it no longer says every marked item is a
historical/translated defect with a nearby correction box.

### F02 -- Medium -- W10-SE002 is incorrectly labelled a “counting error”

**Anchors:**

- `source/english/tex/works/GAL1897_W10_PRIMITIVE_EQUATIONS.tex:453-461`
- `source/critical_baseline/PRINTED_AND_SOURCE_ERRORS.csv:36`

The note heading says **“proved identity exception and counting error.”** The
frozen baseline classifies the defect only as
`identity_exception_in_universal_fixed_point_claim` and expressly says that the
scalar subgroup order remains `p^2-1` and the later affine-group count remains
intact. The note body itself agrees: exactly `p^2-2` nonidentity scalars move
every nonzero letter, while the subgroup still has `p^2-1` elements. Calling
this a counting error contradicts both the authoritative classification and
the body and can lead a reader to think the printed group count is wrong.

Required resolution: change the heading to “proved identity exception” (or an
equally precise formulation) without altering the faithful main translation or
the correct body.

### F03 -- Low -- W01's new PDF021 segment is absent from the alignment and coverage counts

**Anchors:**

- `source/english/tex/works/GAL1897_W01_PRELIMS.tex:122`
- `evidence/ENGLISH_COVERAGE.tsv:2`
- `evidence/EN_FR_ALIGNMENT.tsv` (no row for
  `ENSEG:W01:PDF021:0005`)

W01 now contains five unique ENSEG markers, ending with
`ENSEG:W01:PDF021:0005`, but `ENGLISH_COVERAGE.tsv` still records a segment
count of four and the master alignment ledger contains only the first four W01
records. The underlying PDF021 unresolved-page topology and witness note are
present and correct, so this is not a content or topology loss; it is a stale
traceability record inconsistent with the coverage row’s passed status.

Required resolution: add the PDF021 segment to `EN_FR_ALIGNMENT.tsv` and update
W01's coverage count to five.

## Prior-finding reconciliation

Every earlier audit finding was substantively resolved:

- W10 now defines historical support-size “order” in `W10-TERM001` before the
  first affected classification.
- W10 now exposes `W10-NA001`, `W10-WV001`--`W10-WV006`, and
  `W10-DA001`--`W10-DA004`; proved-error notes include source, downstream,
  witness/prior-notice, and evidence information.
- W03's display now says `\text{or}`; the W01/W03 English title order and the
  W04 title are corrected; W01's three unresolved notes carry `W01-U001`--
  `W01-U003`.
- W09's ambiguity, temporal wording, primitive-root terminology, and W11's W07
  contents title are corrected.
- W09 retains all `W09-PE001`--`W09-PE002`, `W09-SE001`--`W09-SE006`, and
  `W09-WV001`--`W09-WV006` records with the historical main text kept separate
  from repair/witness apparatus. The bounded deferred tasks POST-P13-A009--A014
  remain explicitly identified as pending in the relevant notes.
- W11 preserves printed `1` under `W11-PE001`, retains the unresolved job-number
  crop under `W11-U001`, and states the pending `W11-DA001`/`W11-DA002` work.

## Negative and mechanical findings

- No sentence, paragraph, footnote, theorem hypothesis, explicit quantifier,
  negation, name, date, bibliographic reference, or substantive French residue
  was omitted or mistranslated in the audited components.
- After masking English-only critical-note bodies, mathematical display-token
  sequences are exact: W03 25/25, W04 8/8, W09 37/37, W10 45/45; W01, W02, and
  W11 contain no mathematical display group. Translated `\text{...}` payloads
  were ignored, while every operand, sign, index, exponent, tag, congruence,
  delimiter, and equation was compared.
- Begin/end environment sequences are exact in every pair. Source/topology-call
  sequences are exact: W01 27, W02 6, W03 8, W04 2, W09 18, W10 12, W11 5.
  This includes all blank, excluded, unresolved, in-word boundary, image, and
  terminal-page records.
- All master reader-content hyperlinks have exactly one corresponding source
  anchor (`007`, `024`, `030`, `038`, `040`, `042`, `044`, `054`, `062`, `080`,
  `092`). Wrapper input order is W01--W11, and bookmark destination names are
  unique. The current QA7 PDF outline contains Reader contents plus all eleven
  work bookmarks in that order.
- The master’s completeness and no-silent-correction claims are supported for
  these components. Its universal dagger/nearby-note claim is not supported,
  as recorded in F01.

## Audited English snapshots

| File | Lines | SHA-256 |
|---|---:|---|
| `GAL1897_W01_PRELIMS.tex` | 139 | `1F7C8F54BFE5CFEDD41E58C07EAF14CF8ECF1DBDC11EB7A6FC1E46FEEC87581C` |
| `GAL1897_W02_INTRODUCTION.tex` | 185 | `DB459562F5C7FEDE1CFCB5D84BA00CDAA2E983CE1D355CE58C0B2C6629C0431B` |
| `GAL1897_W03_CONTINUED_FRACTIONS.tex` | 438 | `7280BB8C4EFCAB1C99FC94841ADBF0ECACB891628F2A827D2B1B031A8AB1EB6F` |
| `GAL1897_W04_NOTES_ANALYSIS.tex` | 159 | `A8EDC0751E0C6CFB55537C7C980A5AE7862D91F3BB0EEE1158CBDF0C6C5D3C65` |
| `GAL1897_W09_RADICALS_MEMOIR.tex` | 1259 | `77BEB15F0FEFFE9C793D489790E8110B762651B897EA0D21E904904905119E07` |
| `GAL1897_W10_PRIMITIVE_EQUATIONS.tex` | 648 | `25DD392730C74377E7DA450580F597591E770C4F9A854DAFD2D90873E1ABAC34` |
| `GAL1897_W11_BACKMATTER.tex` | 122 | `49F574205E027263280CF2EEF050534DA409A2040FBD150F59BC39D5DF878748` |
| `GAL1897_EN_MODERN_READER.tex` | 133 | `68289E60BDD5ACBE58B4513406627C04AAFA247A7C05D570A55F46695903811F` |

Current integrated QA7 PDF snapshot: SHA-256
`EA58D93D87B859682D8077F4DC2A0E2CD46765A70CF1C703345B1900CAD1FA35`.

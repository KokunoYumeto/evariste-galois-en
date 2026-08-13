# Independent English audit: W05--W08

Date: 2026-08-13  
Scope: read-only comparison of the current English W05--W08 TeX components against the frozen French diplomatic components, the frozen source-error ledger, witness-variant ledger, and deferred-audit register. Line numbers below refer to the current files at audit time.

## Verdict

No substantive paragraph, historical footnote, display, source-page boundary, image/topology record, name, date, or bibliographic reference is missing. No negation, quantifier, hypothesis, or mathematical formula has been silently reversed or repaired. The source/error/variant macros already present in both layers preserve the same stable issue IDs and printed forms.

The validator's reported math mismatch clusters for W05 (about 28), W06 (about 10), and W07 (about 26) are overwhelmingly parser effects rather than mathematical loss. After removing English-only `\GalCriticalNote` bodies and allowing only translation of prose inside `\text{...}` plus ordinary grammar-driven moves between math and prose, the display inventories are:

| Work | French displays | English displays | Genuine formula loss/change |
|---|---:|---:|---|
| W05 | 2 | 2 | none |
| W06 | 8 | 8 | none |
| W07 | 39 | 39 | none; one terminal comma was dropped |
| W08 | 24 | 24 | none |

The issues that should be fixed or explicitly dispositioned are below.

## Findings

### M1 — W07: misleading mathematical translation of root-count statement

- French anchor: `source/french_diplomatic/tex/works/GAL1897_W07_NUMBER_THEORY.tex`, lines 363--366 (`d'admettre précisément autant de racines qu'il y a d'unités dans l'ordre de leur degré`).
- English anchor: `source/english/tex/works/GAL1897_W07_NUMBER_THEORY.tex`, lines 466--470; `% ENSEG:W07:PDF050:0099`.
- Current English: “admitting precisely as many roots as there are units in the order of their degree.”
- Severity: **medium** (the wording introduces the modern algebraic senses of “units” and “order” and obscures the asserted root-count equality).
- Proposed fix: translate the numerical idiom directly, for example: “of admitting exactly as many roots as their degree.” Do not alter any surrounding historical claim or attach a new mathematical diagnosis solely for this translation repair.

### M2 — W06-PE001: critical note does not state the complete reconstruction it invokes

- Frozen authority: `source/critical_baseline/PRINTED_AND_SOURCE_ERRORS.csv`, record `W06-PE001`.
- English anchor: `source/english/tex/works/GAL1897_W06_NUMERICAL_EQUATIONS.tex`, lines 70--80; `% ENSEG:W06:PDF042:0010`.
- Severity: **medium** (apparatus completeness; the main translated formula is correctly preserved).
- Problem: the note says only that a “symmetric candidate with numerator $Y$” is an editorial reconstruction. The frozen ledger gives the complete candidate
  `x=\psi x=\sqrt[n]{Y/(X/x^n)}`; both the numerator and denominator differ from the printed formula. The note also omits the ledger's explicit witness qualification that the 1846 repetition is not a correcting variant.
- Proposed fix: state the entire reconstructed expression in the note and add that the 1846 repetition does not attest it as a source reading. Continue to preserve the printed `X/(x^n/Y)` expression in the main translation.

### M3 — W08: two frozen witness-variant records are absent from the English apparatus

- Frozen authority: `source/critical_baseline/WITNESS_VARIANTS.csv` and `.md`, records `W08-WV002` and `W08-WV003`.
- `W08-WV003` anchor: `source/english/tex/works/GAL1897_W08_CHEVALIER_LETTER.tex`, lines 149--152; `% ENSEG:W08:PDF056:0028`, at `\emph{Bulletin de Férussac}`.
- `W08-WV002` anchor: the same file, lines 161--177 (and the related order display at 179--185); `% ENSEG:W08:PDF056:0030`--`0035`, at the printed `$p,\nu$` notation.
- Severity: **medium** (stable textual provenance is missing; the English main text itself correctly preserves the 1897 forms).
- Proposed fix: add adjacent apparatus notes with the existing IDs:
  - `W08-WV003`: status `not_error/policy_noop`; retain the 1897 `Bulletin de Férussac`; report only in apparatus that the 1908 collation gives manuscript `bulletin ferussac`.
  - `W08-WV002`: status `not_error/policy_noop`; retain the 1897 `$p,\nu$`; report only in apparatus that the 1908 collation attributes manuscript `$p,n$` and the change to `$p,\nu$` to Liouville.
- Do not add either variant to the diplomatic French layer or normalize the English main text.

### M4 — W07: two local deferred-audit records are not exposed in the reader apparatus

- Frozen authority: `source/critical_baseline/DEFERRED_AUDIT_REGISTER.csv`, records `POST-P13-A004` and `POST-P13-A005`.
- `POST-P13-A004` anchor: `source/english/tex/works/GAL1897_W07_NUMBER_THEORY.tex`, lines 243--270; `% ENSEG:W07:PDF047:0042`--`0050`, after the printed $\mu>\nu$ argument.
- `POST-P13-A005` anchor: the same file, lines 576--590; `% ENSEG:W07:PDF051:0115`--`0117`, after the converse solvability statement and ninth-/twenty-fifth-degree exceptions.
- Severity: **medium** for issue traceability, **none** for translation accuracy.
- Proposed fix: if the English reader is intended to expose every frozen local issue record, add concise `\GalCriticalNote` callouts under these IDs stating `unresolved/defer`, preserving the printed argument, explicitly making no diagnosis, and naming the required proof/classification audit. If deferred-register entries are intentionally external-only, record that policy explicitly in the English coverage evidence rather than silently omitting these two local records.
- The cumulative `POST-P13-A001`--`A003` records are global and should not be duplicated after every work.

### L1 — W07: terminal display punctuation dropped

- French anchor: `source/french_diplomatic/tex/works/GAL1897_W07_NUMBER_THEORY.tex`, lines 357--361; the display ends `a+a_1i+a_2i^2,`.
- English anchor: `source/english/tex/works/GAL1897_W07_NUMBER_THEORY.tex`, lines 456--464; `% ENSEG:W07:PDF050:0097`--`0098`; the comma is absent.
- Severity: **low** (punctuation only; formula unchanged).
- Proposed fix: restore the comma, preferably as prose punctuation immediately after `\]`, or retain it within the display to mirror the witness.

### L2 — W07/W08: permanent ENSEG IDs are unique but not in source order

- W07 anchors: line 213 has `ENSEG:W07:PDF046:0122` before line 224's `...:0037`; line 617 has `...:0123`.
- W08 anchors: line 156 has `ENSEG:W08:PDF056:0125` before line 161's `...:0030`; the final ordinary segment at line 566 is `...:0124`.
- Severity: **low** (no content loss; alignment rows exist for all IDs), but this conflicts with a naive reading of “sequential-id” and can trigger order-sensitive validators.
- Proposed fix: do **not** silently renumber permanent IDs. Either document that later-added permanent IDs may be nonmonotone, and make validators compare uniqueness/page coordinates rather than numeric order, or perform an explicit ID migration with an old-to-new alias table.

### L3 — W05: one sentence is needlessly difficult to parse

- French anchor: `source/french_diplomatic/tex/works/GAL1897_W05_ALGEBRAIC_RESOLUTION_ANALYSIS.tex`, lines 72--79.
- English anchor: `source/english/tex/works/GAL1897_W05_ALGEBRAIC_RESOLUTION_ANALYSIS.tex`, lines 94--103; `% ENSEG:W05:PDF041:0014`--`0015`.
- Current English: “by means of a number of radicals of degree $p$ equal to the number of divisors ...”.
- Severity: **low** (meaning is recoverable; no quantifier is lost).
- Proposed fix: “by means of as many radicals of degree $p$ as there are divisors $a^{\alpha}$ of ... satisfying ...”. Preserve the displayed congruence unchanged.

## Validator-mismatch disposition

The major mismatch sources are mechanical:

- W05: English-only mathematics inside the two critical notes; English math styling of the prose number `5`; and translation of `a\text{ premier}` to `a\text{ prime}`.
- W06: English-only critical-note mathematics; French `$=a$` rendered grammatically as “equal to `$a$`”; French `$n^{\text{ième}}$` rendered as English `$n$th`; two adjacent French math runs (`$x$ ... `$>1$`) combined as `$x>1$`; and `\text{ou bien}` / `\text{pour}` translated inside displays.
- W07: English-only critical-note mathematics; ordinal tokens `$2^{\mathrm e}$`, `$3^{\mathrm e}$`, and `$(\nu-1)^{\text{ième}}$` rendered as English prose; `$>\nu$` rendered as “greater than `$\nu$`”; translated words inside `\text{...}`; and the one dropped comma recorded as L1.

These are not evidence of 28/10/26 lost formulas. A structural checker should parse balanced TeX, remove or separately inventory `\GalCriticalNote` arguments, normalize language-bearing `\text{...}` nodes, and compare mathematical ASTs rather than raw `$...$` token strings.

## Passed checks

- Complete prose and historical-footnote translation: pass for W05--W08.
- Source topology: exact page-start/boundary sequences match; W07's PDF 053 blank leaf and PDF 052 image/ornament calls are retained.
- Issue-bearing source macros: printed/source error IDs and `W08-WV001` match the frozen French calls and preserve their printed payloads.
- Names/dates/references: Férussac, Liouville, Gauss, Legendre, Libri, Abel, Poisson, Chevalier, Jacobi; April/June 1830, 1832, and 29 May 1832; volume/page/issue references all survive.
- Residual-French scan: no substantive French prose remains. The surviving French strings are intentional titles/proper bibliographic forms (`Bulletin des Sciences mathématiques`, `Bulletin de Férussac`, `Revue encyclopédique`) or ledger/evidence filenames.
- Existing critical-note diagnoses: apart from M2 and the missing callouts in M3--M4, the notes preserve the historical claim, separate correction from translation, state downstream limits, and retain unresolved/prior-notice-pending status.


# Independent semantic and formula audit: W09 and W11

Audit date: 2026-08-13. This is a read-only, sentence-by-sentence comparison of the English W09 and W11 work files against the frozen French files with the same names under `source/french_diplomatic/tex/works/`. No TeX, shared ledger, metadata, repository state, or publication surface was edited.

## Result

No sentence, footnote, mathematical claim, hypothesis, negation, explicit quantifier, display, name, date, or reference is missing from either English component. No high- or medium-severity semantic defect was found. Four low-severity wording/title issues should be tightened for clear modern mathematical English. The W09 structural-validator mismatch near old math-sequence index 42 is not a mathematical mismatch: English grammar merely reverses the order of two intact inline math spans within one sentence.

Severity used below:

- **High**: changes or seriously obscures mathematical meaning.
- **Medium**: loses a hypothesis, quantifier, critical record, source topology item, or materially required provenance.
- **Low**: localized ambiguity, anachronistic wording, or title inconsistency without mathematical drift.

Audited snapshots:

| Layer | Component | Lines | SHA-256 |
|---|---|---:|---|
| French frozen source | W09 | 906 | `9D15B6CEF971EB7B36B1168444B1FC731A2FE38E45FE3DA34B687C7CDFCA8013` |
| English | W09 | 1259 | `26A0C65D61501D687623ADCB73AA84913EF789BB05C8DBEAB1EA231DF46313BF` |
| French frozen source | W11 | 86 | `337F1B3279B68F67BD516563BEA5A664F6FD44765D89A8C793BD086297C47380` |
| English | W11 | 122 | `119ED004904B6E443A56871E8CA3795ABEA30F655BBB7ED00038C9404557E852` |

## Findings

### F01 — Low — W09's “its solvability” has an ambiguous antecedent

**French anchor:** `source/french_diplomatic/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:37-39`.

**English anchor:** `source/english/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:40-42`, segment `ENSEG:W09:PDF062:0003`.

French says that every equation solvable by radicals satisfies the condition and that, conversely, the condition assures `leur résolubilité` (the solvability of the equations). In “which conversely ensures its solvability,” English `its` can grammatically point to the condition rather than the equation and also loses the French plural reference. The intended necessary-and-sufficient claim remains recoverable, but the sentence is needlessly ambiguous.

**Proposed fix:**

```tex
Here one will find a general \emph{condition satisfied by every equation solvable
by radicals}, and which, conversely, guarantees solvability. It is applied only to
```

### F02 — Low — W09's “currently known” is temporally misleading

**French anchor:** `source/french_diplomatic/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:595-603`.

**English anchor:** `source/english/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:813-836`, especially `:835-836`, segment `ENSEG:W09:PDF073:0138`.

In this deduction, `sera actuellement connue` means that the displayed invariant will at that stage/thereby be known. Modern English “will be currently known” normally means “will be known at the present time,” which obscures the logical consequence even though it does not change the formula.

**Proposed fix:** replace `will be currently known` with `will thereby be known` (or `will then be known`).

### F03 — Low — W09 should state “primitive root modulo n”

**French anchor:** `source/french_diplomatic/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:800-813`, especially `:808`.

**English anchor:** `source/english/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:1111-1127`, especially `:1120-1122`, segment `ENSEG:W09:PDF077:0190`.

The English “$a$ is a primitive root of $n$” is recognizable historical terminology, but clear modern number-theoretic English is “a primitive root modulo $n$.” The surrounding subscripts use successive powers of the residue class of $a$ modulo the prime $n$, so the clarification introduces no new hypothesis.

**Proposed fix:**

```tex
where $\alpha$ is an $n$th root of unity and $a$ is a primitive root modulo $n$.
```

### F04 — Low — W11's W07 title is inconsistent with the translated work title

**French anchor:** `source/french_diplomatic/tex/works/GAL1897_W11_BACKMATTER.tex:47` (`Sur la théorie des nombres.`).

**English anchor:** `source/english/tex/works/GAL1897_W11_BACKMATTER.tex:66`, segment `ENSEG:W11:PDF092:0010`.

The contents entry “On Number Theory” is understandable, but it drops the definite article in `la théorie des nombres` and does not match the W07 title at `source/english/tex/works/GAL1897_W07_NUMBER_THEORY.tex:21-24` (“ON / THE THEORY OF NUMBERS”).

**Proposed fix:**

```tex
\GalTocEntry{On the Theory of Numbers.}{15}
```

## W09 validator mismatch near math-sequence index 42

**Verdict: parser/alignment false positive; no mathematical repair is required.**

The relevant source sentence is at `source/french_diplomatic/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:285-287`:

```tex
... dont $a,b,c,\ldots$ sont les $m$ racines. ...
des lettres $a,b,c,\ldots$ ...
```

Its math-span sequence at local indexes 42–44 is therefore:

```text
a,b,c,\ldots  |  m  |  a,b,c,\ldots
```

The English sentence at `source/english/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:376-378`, segment `ENSEG:W09:PDF067:0059`, reads:

```tex
... whose $m$ roots are $a,b,c,\ldots$. ...
the letters $a,b,c,\ldots$ ...
```

Its sequence is:

```text
m  |  a,b,c,\ldots  |  a,b,c,\ldots
```

Both mathematical spans occur unchanged and with the same meaning; only their order is reversed to produce idiomatic English. A validator should compare math spans within the aligned sentence/`ENSEG` as a multiset before reporting a loss, or explicitly permit local reordering. If strict global sequence identity is nevertheless required, the English could be rephrased without semantic change as `Let an equation be given whose roots $a,b,c,\ldots$ are $m$ in number.`

## Formula, macro, and topology checks

- After masking the fourteen English W09 critical-note bodies, both W09 files contain 193 math spans. All variables, indices, exponents, signs, equalities, inequalities, products, arrays, and ellipses are preserved.
- The only non-byte-identical W09 math spans are the harmless local reorder above; two translated `\text{...}` clauses inside displays (`une fonction divisible par` → `a function divisible by`); and six French ordinal constructions such as `$p^{\text{ième}}$`/`$n^{\text{ième}}$` rendered idiomatically as `$p$th`/`$n$th` in prose. No mathematical operand is lost in any of these cases.
- W11 contains no substantive mathematical display or inline formula to drift.
- W09's one `\GalSourcePageStart` and seventeen `\GalSourcePageBoundary` calls match the French four-argument tuples exactly and in order, covering PDF062/L0061 through PDF079/L0078.
- W11's page start, page boundary, three blank-page records, and unresolved-image call match exactly, including PDF/leaf coordinates, topology descriptions, crop path, and unresolved-reading text.
- W09 preserves the exact control-ID sequence: `W09-WV001`; `W09-PE001`–`W09-PE002`; `W09-SE001`–`W09-SE006`; `W09-CD001`–`W09-CD007` as present in the source. Mathematical control payloads are exact; prose payloads are translated. The six historical-note containers and terminal article rule are also preserved.
- W11 preserves `W11-PE001` with printed value `1` and the complete four arguments of the unresolved-image record.
- A read-only brace/environment scan found balanced braces and properly nested `\begin`/`\end` pairs in all four audited files.
- W09 has 215 unique, sequential `ENSEG` markers (`0001`–`0215`); W11 has 18 (`0001`–`0018`). The alignment fragment contains all 233 records.

## Critical-note fidelity

All critical-note IDs and bodies were checked against the frozen records under `source/critical_baseline/`.

- W09 contains all eight source-error notes (`W09-PE001`, `W09-PE002`, and `W09-SE001`–`W09-SE006`) and all six witness-history notes (`W09-WV001`–`W09-WV006`). Each preserves the printed claim in the main translation, keeps the repair or witness history in the separate note, cites the correct evidence IDs, states the relevant downstream effect, and honestly marks pending prior-notice/propagation research.
- The mathematical repairs in `W09-SE001`–`W09-SE006` agree with the frozen ledgers: the gcd/Bézout completion; field-intersection index formula; normal-intersection proof; nonzero Fourier-coefficient selection; missing Kummer/normality context; and missing nonidentity qualifier.
- W11's `W11-PE001` preserves the printed Arabic `1`, identifies logical folio `v` only in apparatus, and does not treat generated control text as independent evidence. `W11-U001` retains the fused job number as an unresolved image and makes no digit guess.

No critical-note overclaim, silent source correction, unsupported witness fusion, or missing frozen W09/W11 record was found.

## Names, dates, references, and residual-language scan

The dated and bibliographic content is complete: 16 January 1831, 1846, 1832, Liouville, Auguste Chevalier, Abel, Poisson, Gauss, Descartes, Euler, Cauchy, the *Revue encyclopédique*, and the *Journal de l'École Polytechnique*, XVIIe/17th issue all remain associated with the correct statements.

No unintentional substantive French remains in either English file. The scan hits are limited to proper titles and addresses, exact French witness forms quoted inside critical notes (`celle fonction`, `cette fonction`, `proprieté`, `propriété`), and the manuscript citation `Journal de l'École, XVII`; these must remain untranslated or quoted as written.

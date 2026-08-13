# Galois 1897 English style guide

Translate the printed French into readable modern mathematical English without altering the mathematical claim. A false, incomplete, or typographically defective claim remains faithfully translated and receives an adjacent `\GalCriticalNote{ID}{...}`. Never fuse the French witness with a manuscript, 1846 printing, 1908 collation, or modern theorem.

- Preserve all LaTeX mathematics unless English grammar requires punctuation outside math mode.
- Preserve source macros; page-boundary, error, variant, historical-note, image, and topology calls; theorem numbering; displays; footnotes; names; dates; titles; and citations.
- Add `% ENSEG:<component>:<source-PDF>:<sequential-id>` before each substantive English paragraph, heading, display group, note, or caption. IDs are permanent identifiers, not mutable counters: after assignment they are never renumbered merely to restore numeric order. Validators require component/source identity and global uniqueness, while the alignment ledger records reading order explicitly.
- Do not add explanations or modern notation to the main translation. Put them only in stable-ID critical boxes.
- Prefer direct modern prose. Translate `on` contextually as “we,” a passive, or “one.”
- Use “given equation,” “adjoin,” “solvable by radicals,” “irreducible,” “primitive equation,” “auxiliary equation,” “rational function,” “group,” “order,” and “index” consistently.
- Retain “substitution” for Galois's historical permutation operation. Retain “conjugate” for `conjugué`; defer the exact W10 force to `W10-DA003`.

Every critical note states: stable ID/status; printed claim; corrected/qualified statement; proof/counterexample and hypotheses; downstream effect; witness transmission/prior notice; evidence pointer. If research is incomplete, say so and never claim novelty.

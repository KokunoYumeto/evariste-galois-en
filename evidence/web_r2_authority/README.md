# Galois 1897 GPT Critical Edition — R2 rebuilt cumulative handoff

This directory is the self-contained successor to the previously announced cumulative post-P13 ZIP whose byte stream was unavailable in the active runtime. The surviving predecessor sidecar and receipt are preserved under `provenance/missing_predecessor_archive/`; this R2 package does not claim byte identity with that absent archive.

R2 contains:

- the exact immutable P00-P13R repaired cumulative handoff, SHA-256 `05C2247E2127BF816B838DA668EB9EF05AC6981D09862FB819470D79DFE3E74B`;
- the complete 36-file original source packet, including its 35-payload SHA-256 manifest;
- the frozen 78-page diplomatic PDF, unchanged, SHA-256 `8E6071A2E4A0D38CC89232553CE0CC0314C7EF4BD0A084240C41D60B0AEBBFC5`;
- a revised 24-page GPT critical appendix and a 102-page diplomatic-plus-critical reader;
- all 21 task certificates and completed structured ledgers;
- source replay, images, retrieval receipts, web/literature provenance, mathematical checks, deterministic build scripts, and independent cold-audit materials.

## R2 task disposition

The 21 post-P13 tasks are now closed as follows:

- 10 `repaired`;
- 9 `proved`;
- 2 `rejected`;
- 0 unresolved task rows.

The two records formerly unresolved after bounded search are closed in the critical layer:

- `POST-P13-A008 / W08-WV001`: direct 600 ppi replay reads Tannery's formula as `E′F″−E″F′=(π/2)√−1`, not the former apparatus reading beginning `F′F″`; the determinant and printed complete-integral forms are proved equivalent under an explicit admissible period normalization.
- `W11-DA002 / W11-U001`: the independent ETH-Bibliothek 1897 copy and its OCR resolve the printer job number as the five-digit `24572`.

Three inherited W01 image/provenance readings remain open outside the 21-task scope: `W01-U001`, `W01-U002`, and `W01-U003`. They are retained in `ledgers/OPEN_AFTER_21_TASKS.csv` and are not blocking defects.

## Active PDFs

- `critical_edition/GAL1897_GPT_CRITICAL_EDITION.pdf`: 24 pages, SHA-256 `BC152B109F592C159FB5267C69D01AF82B0F8152B7315D88CCC343953CDCE34E`.
- `critical_edition/GAL1897_ONE_CLICK_READER_DIPLOMATIC_PLUS_GPT_CRITICAL.pdf`: 102 pages, SHA-256 `38A474F0ED516EBCC5A797E0178D34E4BD3168131B6A14870DD0E50C3AB55112`.

The reader preserves the frozen diplomatic PDF as pages 1-78 and appends the separately titled critical layer as pages 79-102. Poppler and PDFium replay both pass 78/78 diplomatic-prefix pages and 24/24 appended critical pages.

## Verification

The independent R2 cold audit passes 242/242 checks. Deterministic two-run builds are byte-identical. PDF preflight, embedded-font checks, Ghostscript validation, mathematical checks, renderer parity, source-packet hashes, ZIP CRC checks, and source-replay hashes all pass.

Use `RETURN_TO_CODEX.md` for integration instructions. No DOI, Zenodo, GitHub, or publication mutation was performed.

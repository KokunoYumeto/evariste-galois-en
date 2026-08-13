# English release QA report

Prepared: 2026-08-14. Release: `2026-08-14 en-r1`.

## Current verdict

The post-P13-integrated reader is substantively and visually closed for packaging. Publication remains pending until the final public-safe archives are built twice with byte-identical results and then retrieved and verified from GitHub and Zenodo. Reciprocal French r2 remains a later external step in the same controlled workflow.

## Translation and critical apparatus

- 11/11 ordered components translated.
- 587 unique aligned English segments.
- 96/96 physical source pages accounted for.
- 36/36 frozen source-error records have rendered adjacent notes.
- 15/15 witness/editorial variant records are preserved in the apparatus and evidence.
- All 21 post-P13 tasks are dispositioned: 9 repaired, 8 proved, 2 rejected, and 2 unresolved after bounded search.
- The exact cumulative open set is `W01-U001`, `W01-U002`, `W01-U003`, `W08-WV001`, and `W11-U001`.
- The missing 313,572,719-byte cumulative web-return ZIP is not claimed as independently replayed. The 16 individual returned files and their receipt were hash-validated and parsed; their machine-readable cold audit reports 242/242 checks passing.

`TRANSLATION_LEDGER_BUILD.json` passes fail-closed checks for the exact task universe, exact 36-error plus 15-variant priority universe, exact five-record open universe, source references to all 21 task IDs, and all rendered baseline error/variant notes.

## Source and formula structure

`STRUCTURAL_VALIDATION_POST_P13.json` passes over all eleven French/English component pairs with zero errors. It pins complete ordered issue-call payloads for every component, preserves every stable source ID, detects lost calls and arguments, and retains seven separately audited formula-delta pins. Deliberate in-memory mutation tests detected argument edits, stable-ID loss, and call-count loss.

## Reader build

- Exact PDF: `reader/00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf`.
- Pages: 85.
- Bytes: 3,826,541.
- SHA-256: `8A3702F37031199F3AD4904C36297F439DE4E265A2D10C203F6A6B8F2D2AACF3`.
- Two independent uniquely named builds are byte-identical.
- LaTeX warnings: zero. Undefined references: zero.

`READER_STRUCTURAL_QA_POST_P13.json` passes: exact metadata; 12 ordered bookmarks; 14 valid link annotations; all page content streams parse; uniform valid page boxes; no encryption; all required DOI strings recover through independent extractors; every font embedded; and exact blank topology at pages 42, 80, and 83-85.

`READER_MECHANICAL_RENDER_QA_POST_P13.json` passes over all 85 PNG pages at 120 DPI with no mechanically black page, no dark-pixel edge contact, exact declared blanks, and one consistent render geometry. It explicitly does not claim visual inspection.

`READER_VISUAL_INSPECTION_POST_P13.json` separately records actual model viewing of every page through ten original-detail contact sheets and full-resolution review of representative dense pages 3, 29, 71, 73, and 82. No clipping, overlap, broken glyph, unreadable mathematics, image/seam defect, unexpected blank/black page, or hierarchy defect was observed. The English historical translation remains visually primary; concise blue critical notes remain adjacent and navigable.

## Metadata and rights

- Reserved English exact DOI: `10.5281/zenodo.21924302`; concept DOI: `10.5281/zenodo.21924301`.
- English concept `IsTranslationOf` French concept `10.5281/zenodo.21923856`; French reciprocally `HasTranslation` English. Zenodo fallback uses `isDerivedFrom` / `isSourceOf` while preserving exact DataCite intent in visible metadata and the sidecar.
- Galois is the historical author. Manuscript Typesetting Project is the edition identity and maintainer. GPT-5.6 Sol Pro is credited for the returned post-P13 web research and mathematical certificates; GPT-5.6 Sol Ultra is credited for modern-English translation, integration, DOI engineering, and independent QA. No human translator is asserted.
- Public-domain historical material is distinguished from CC0 project-owned contributions. Third-party scans, cataloguing, and witness artifacts are not relicensed.

## Remaining release gates

1. Build the source, evidence, manifest, and French sibling-language archives from explicit public allowlists.
2. Require safe member paths, CRC success, no duplicate names, no credentials or absolute local paths, full French-public-release hash verification, and byte-identical repeat builds.
3. Push and tag the standalone English GitHub repository, publish the reserved Zenodo record, retrieve every public file, and compare checksums.
4. Create French r2 with reciprocal metadata and the final English sibling ZIP, then retrieve and verify it while preserving French r1.

No human review, sign-off, certification, community acceptance, or waiting period is a release gate.

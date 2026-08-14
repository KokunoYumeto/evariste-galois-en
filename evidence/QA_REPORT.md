# English R2 release QA report

Prepared: 2026-08-14. Release: `2026-08-14 en-r2`.

## Verdict

The human-facing English reader and its R2 research layer pass the local semantic, structural, deterministic-PDF, visual, archive-safety, and repeat-package gates. Two retained package builds produced byte-identical five-file surfaces. External publication and outside-in retrieval verification remain pending.

## Translation and editorial apparatus

- 11/11 ordered components translated.
- 587 unique aligned English segments.
- 96/96 physical source pages accounted for.
- 36/36 source-error records have adjacent editorial notes.
- 15/15 witness/editorial variants are preserved in the apparatus and evidence.
- All 21 bounded research tasks are concluded: 10 repaired, 9 proved, 2 rejected, 0 unresolved.
- The only open records are three preliminary-image questions outside that task set: `W01-U001`, `W01-U002`, and `W01-U003`.
- R2 evidence contains 48 dependency edges, 52 prior-notice rows, 22 search rows, a 242/242 cold audit, and a verified 164/164 split-source replay.

The source tree preserves 65 unique `GalCriticalNote` anchors and three unique W01 `GalWitnessNote` anchors. Reader-facing headings and prose are descriptive and human-readable. Stable IDs appear only as small editorial references. The main historical translation is not silently corrected.

Two R2 resolutions supersede the R1 state: the Tannery manuscript relation at `W08-WV001` is read and normalized, and the printer job number at `W11-U001` is resolved as `24572` from an independent ETH copy and OCR.

## Source and formula structure

`STRUCTURAL_VALIDATION_POST_P13.json` passes over all eleven French/English component pairs with zero errors. It preserves source coordinates, stable issue IDs, ordered issue-call payloads, and the separately audited formula-delta pins. The translation ledger passes for all 11 components, 587 aligned segments, and 96 physical pages.

`R2_AUTHORITY_VALIDATION.json` passes the R2 package replay and all controlling counts. It also records the received package's one known documentation defect: two ledger rows cite an absent `qa/OPEN_TASK_RESOLUTION_CHECKS.json`. The present certificates, comparison figures, source replay, mathematical checks, and cold audit supply the actual evidence; the absent path is not presented as available.

## Reader build and inspection

- Exact local PDF: `build/en-r2-reader-a-20260814T022000/GAL1897_EN_MODERN_READER.pdf`.
- Pages: 84.
- Bytes: 3,734,236.
- SHA-256: `2AF04298A1184307C2F94B82FAE55E6AA0BDA4560C2E95461537924AB814E6D5`.
- Two clean builds are byte-identical.
- LaTeX warnings and undefined references: zero.
- PDF metadata title: *Modern English Reader with Editorial Notes*.
- 12 ordered bookmarks and 14 valid link annotations.
- Five intentional blank-topology pages: 41, 79, 82, 83, and 84.

`READER_STRUCTURAL_QA_POST_P13.json` passes metadata, outlines, links, content streams, page boxes, encryption, fonts, DOI extraction, build logs, and blank topology. `READER_MECHANICAL_RENDER_QA_POST_P13.json` passes all 84 rendered pages and explicitly makes no visual claim. `READER_VISUAL_INSPECTION_POST_P13.json` separately records actual viewing of every page through ten contact sheets plus full-resolution inspection of representative pages. No clipping, overlap, broken glyph, unreadable mathematics, image/seam defect, unexpected blank/black page, or hierarchy defect was observed.

## Metadata, rights, and next gate

- Exact English R2 DOI: `10.5281/zenodo.21926209`; concept DOI: `10.5281/zenodo.21924301`.
- English concept `IsTranslationOf` French concept `10.5281/zenodo.21923856`; French reciprocally `HasTranslation` English. Zenodo fallback uses `isDerivedFrom` / `isSourceOf` while preserving the exact DataCite intent in public metadata and the sidecar.
- Galois is the historical author. Manuscript Typesetting Project is the edition identity and maintainer. Model production roles are identified without inventing a human translator.
- Public-domain historical material is distinguished from CC0 project-owned contributions. Third-party scans, catalogue data, and witness artifacts are not relicensed.

The next gate is to publish this exact five-file set to GitHub and the unsubmitted Zenodo R2 draft, retrieve it from both public surfaces, and compare every checksum. No human review, sign-off, certification, community acceptance, or waiting period is a release gate.

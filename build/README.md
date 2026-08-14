# Galois English R3 two-reader builder

This isolated R3 tooling has no Git, network, publication, deletion, cleanup,
or credential code path. It refuses reused build/output directories.

## Frozen and public contracts

`GALOIS_R3_FROZEN_AUTHORITY.json` pins the exact eleven annotated R2 work
bodies, nine source-era figures, annotated predecessor identity, and all five
French R2 public files. Both reader recorder graphs must resolve their eleven
work inputs to that one pinned authority set.

A publication-authoritative output contains exactly:

1. `00_GALOIS_1897_EN_SOURCE_FAITHFUL_READER.pdf`
2. `01_GALOIS_1897_EN_GPT_ANNOTATED_READER.pdf`
3. `02_GALOIS_1897_EN_EDITABLE_SOURCES.zip`
4. `03_GALOIS_1897_EN_EVIDENCE_AND_PROVENANCE.zip`
5. `04_GALOIS_1897_EN_SHA256_MANIFEST.txt`
6. `OTHER_TRANSLATIONS.zip`

The editable-source archive contains the one active English corpus under
`source/english/tex/works`, the direct driver/wrappers, exact rendered release
metadata, licensing metadata, and build tooling. Inactive French
`source/english/tex/pages` files and inactive `source/english_direct/tex/works`
snapshots are never staged or packaged.

## Strict visual receipts

The two receipt paths must be distinct. Each receipt must implement
`GALOIS_R3_VISUAL_QA_RECEIPT_SCHEMA.json` and bind, at top level, the exact
reader role, exact DOI, PDF SHA-256, page count, ordered complete page list,
`all_pages_visually_inspected: true`, `visual_result: "PASS"`, and an empty
`blocking_findings` list. The builder preserves both original receipts in the
evidence archive.

## Required sequence

Build the exact-DOI readers first:

```text
python build_galois_english_r3_two_reader_release.py <publication-root> \
  --exact-doi <reserved exact DOI> \
  --version "2026-08-14 en-r3" \
  --tag "v2026.08.14-en-r3" \
  --publication-date 2026-08-14 \
  --build-directory <fresh-reader-preflight-name> \
  --reader-preflight
```

After all-page inspection, render the seven publication metadata artifacts
plus `METADATA_RENDER_RECEIPT.json`, and retain the same-concept Zenodo
reservation identity receipt. Establish a quarantined baseline:

```text
python build_galois_english_r3_two_reader_release.py <publication-root> \
  --exact-doi <same exact DOI> \
  --version "2026-08-14 en-r3" \
  --tag "v2026.08.14-en-r3" \
  --publication-date 2026-08-14 \
  --build-directory <fresh-baseline-build-name> \
  --direct-qa-receipt <direct receipt> \
  --annotated-qa-receipt <annotated receipt> \
  --reservation-identity-receipt <reservation receipt> \
  --rendered-metadata-directory <fresh metadata directory> \
  --establish-comparison-baseline
```

The baseline is written only to
`build/<fresh-baseline-build-name>/comparison-baseline`; it is explicitly
non-authoritative. It cannot accept an output-directory argument.

Create the public output only through a verified second build:

```text
python build_galois_english_r3_two_reader_release.py <publication-root> \
  --exact-doi <same exact DOI> \
  --version "2026-08-14 en-r3" \
  --tag "v2026.08.14-en-r3" \
  --publication-date 2026-08-14 \
  --build-directory <fresh-verified-build-name> \
  --output-directory <fresh-public-output-name> \
  --direct-qa-receipt <same direct receipt> \
  --annotated-qa-receipt <same annotated receipt> \
  --reservation-identity-receipt <same reservation receipt> \
  --rendered-metadata-directory <same metadata directory> \
  --compare-to-baseline-build-directory <baseline-build-name>
```

The public directory is created only after all six candidate files match the
receipt-gated quarantined baseline byte-for-byte. The PASS build receipt stays
outside the exact six-file directory under the verified build directory.

## Projection validator

The validator pins 11 components, 587 ENSEG anchors, work/figure hashes,
historical apparatus counts, topology, destinations, bookmarks, and rendered
modern-apparatus exclusions. In compiled mode the direct PDF and `.fls` must
share a stem, the recorder must name that PDF output and staged master, and all
eleven inputs must resolve to the frozen annotated authority. The builder runs
the corresponding exact proof independently against the annotated `.fls` and
requires the two authority-set hashes to match.

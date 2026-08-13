# Proposed English release surface and metadata crosswalk

## Zenodo file surface

The record must expose exactly these five top-level files, with the English-native artifacts first and the sibling-language bundle last:

| Order | Filename | Required content |
|---:|---|---|
| 00 | `00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf` | Linked/bookmarked complete English reader for the exact declared source coverage; opening pages state scope, language, roles, rights, source authority, repository, concept DOI, and exact DOI. |
| 01 | `01_GALOIS_1897_EN_EDITABLE_SOURCES.zip` | Reproducible English LaTeX, figures, root metadata/license, source-authority/relation records, and build instructions; no caches or credentials. |
| 02 | `02_GALOIS_1897_EN_EVIDENCE_AND_PROVENANCE.zip` | Coverage, EN–FR alignment, critical-callout and unresolved ledgers, semantic/formula audits, source hashes, build receipt, structural PDF QA, rendered inspection, archive QA, and manifests. |
| 03 | `03_GALOIS_1897_EN_SHA256_MANIFEST.txt` | Exact DOI header and byte/SHA-256 rows for 00, 01, 02, and `OTHER_TRANSLATIONS.zip`; it does not hash itself. |
| last | `OTHER_TRANSLATIONS.zip` | One DOI-labelled French directory containing the four byte-exact public files from French release `10.5281/zenodo.21923857` plus its public README, license, citation metadata, and Zenodo metadata. |

`CURRENT` is intentional: later evidence-backed corrections remain versions in the same English concept lineage. Do not name the artifact `COMPLETE` as a claim of finality, even though the exact source coverage of this release is all PDF001–PDF096.

## Public identity

| Field | Exact value |
|---|---|
| Record title | `Évariste Galois — Mathematical Works (1897): Modern English Reader with GPT Critical Notes / Œuvres mathématiques (1897) : lecteur anglais moderne et notes critiques GPT` |
| Resource | One fixed book-like English translation family with maintainable critical apparatus |
| DataCite general type | `Book` |
| Zenodo type | `upload_type=publication`; `publication_type=book` |
| Version | `2026-08-14 en-r1` |
| Publication date | `2026-08-14` |
| Language identity | BCP 47 `en`; Zenodo legacy/CFF-compatible code `eng` (CFF may use `en`) |
| Stable English concept DOI | `10.5281/zenodo.21924301` |
| Exact English release DOI | `10.5281/zenodo.21924302` |
| French source concept DOI | `10.5281/zenodo.21923856` |
| Frozen French exact release | `10.5281/zenodo.21923857` |
| Global project | `10.5281/zenodo.20393488` |
| Repository | `https://github.com/KokunoYumeto/evariste-galois-en` |
| Release tag | `v2026.08.14-en-r1` |
| Zenodo record | `https://zenodo.org/records/21924302` |
| Reader preview | `https://zenodo.org/records/21924302/preview/00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf` |
| Reader download | `https://zenodo.org/records/21924302/files/00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf?download=1` |
| Direct GitHub reader | `https://raw.githubusercontent.com/KokunoYumeto/evariste-galois-en/main/reader/00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf` |
| Zenodo license selector | `cc-zero` |
| CFF/SPDX license | `CC0-1.0` |

The Zenodo license selector covers project-owned contributions only to the extent stated in `LICENSE`; it does not convert public-domain historical material into newly licensed material or relicense third-party scans and metadata.

## Roles

| Role | Identity | Metadata treatment |
|---|---|---|
| Historical author | Évariste Galois | Zenodo creator; CFF preferred-citation author |
| Historical Introduction | Émile Picard | Disclosed in scope/source authority; not mislabelled as modern translator |
| Maintainer/editorial identity | Manuscript Typesetting Project | Zenodo creator; CFF repository author and preferred-citation editor |
| Post-P13 web research and mathematical certificates | OpenAI GPT-5.6 Sol, Pro mode | Zenodo contributor `Other` because the live vocabulary lacks the exact research role; precise role in prose |
| Modern-English translation, critical integration, DOI release engineering, independent QA | OpenAI GPT-5.6 Sol, Ultra mode | CFF translator; Zenodo contributor `Other`; precise role in prose |

No human translator or unverified affiliation is asserted.

## Relation implementation

| Semantic direction | Canonical DataCite 4.7 | Current Zenodo expression | Where applied |
|---|---|---|---|
| English → French | `IsTranslationOf` | `isDerivedFrom` | English record now; exact relation also in README/description/sidecar |
| French → English | `HasTranslation` | `isSourceOf` | French metadata update after English publication |
| English → global | `IsPartOf` | `isPartOf` | English record |
| Global → English | `HasPart` | `hasPart` | Global metadata update after English publication |
| English exact → English concept | `IsVersionOf` | Zenodo version lineage | Supplied by Zenodo |
| English concept → English exact | `HasVersion` | Zenodo version lineage | Supplied by Zenodo |

The presence of French files in `OTHER_TRANSLATIONS.zip` is a convenience mirror. It does not turn the English record into a multilingual work, make English part of French, or make one language a version of the other.

## Frozen local reader and preflight values

- English reader: 85 pages; 3,826,541 bytes; SHA-256 `8A3702F37031199F3AD4904C36297F439DE4E265A2D10C203F6A6B8F2D2AACF3`.
- Complete translation ledger: 11 components; 587 segments; 96 physical source pages; 36 proved errors; 15 witness variants; 21/21 post-P13 tasks dispositioned as 9 repaired, 8 proved, 2 rejected, and 2 unresolved after bounded search; exact cumulative open set of five records.
- Structural PDF preflight: PASS; 12 ordered bookmarks, 14 link annotations, exact five intentional blanks (42, 80, 83--85), no encryption, all fonts embedded/subset/Unicode-mapped, required DOI strings extractable, zero compile warnings, and two byte-identical builds.
- Render inspection: PASS at 120 DPI over all 85 pages plus full-page checks of representative dense critical-note pages; no clipping, overlap, broken glyphs, edge contacts, black surprises, or unexpected blanks.
- Archive hashes and repeat-build closure are supplied by the final package receipt and `03_GALOIS_1897_EN_SHA256_MANIFEST.txt`.

Final exact archive hashes are supplied by `03_GALOIS_1897_EN_SHA256_MANIFEST.txt`. The Git commit/tag and public retrieval checks are frozen only after their respective external operations; no human approval is required.

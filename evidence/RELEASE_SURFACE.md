# English two-reader release surface

## Identity

| Field | Value |
|---|---|
| Title | Évariste Galois — Mathematical Works (1897): Source-Faithful English Translation and GPT-Annotated Edition |
| Stable concept DOI | `10.5281/zenodo.21924301` |
| Exact version DOI | `10.5281/zenodo.21935485` |
| Zenodo record | `https://zenodo.org/records/21935485` |
| Version | `2026-08-14 en-r3` |
| Git tag | `v2026.08.14-en-r3` |
| Publication date | `2026-08-14` |
| Repository | `https://github.com/KokunoYumeto/evariste-galois-en` |
| French concept DOI | `10.5281/zenodo.21923856` |
| Global project DOI | `10.5281/zenodo.20393488` |
| Preserved predecessor | `10.5281/zenodo.21926209` |

The two reader PDFs are files in this single exact English version. They share one DOI and one version history.

## Exact public file set

| Order | Filename | Role |
|---:|---|---|
| 00 | `00_GALOIS_1897_EN_SOURCE_FAITHFUL_READER.pdf` | One-click direct translation without modern GPT annotations. |
| 01 | `01_GALOIS_1897_EN_GPT_ANNOTATED_READER.pdf` | One-click modern reader with human-readable GPT critical annotations. |
| 02 | `02_GALOIS_1897_EN_EDITABLE_SOURCES.zip` | Both reader sources, shared translated corpus, figures, metadata, and reproducible build inputs. |
| 03 | `03_GALOIS_1897_EN_EVIDENCE_AND_PROVENANCE.zip` | Source authority, alignment, apparatus evidence, semantic and mathematical QA, render inspection, and provenance. |
| 04 | `04_GALOIS_1897_EN_SHA256_MANIFEST.txt` | Exact DOI/concept headers and hashes for the other five public payloads. |
| 05 | `OTHER_TRANSLATIONS.zip` | Current complete public French release as a convenience sibling bundle. |

## Manifest contract

The manifest begins with these three lines:

```text
Exact DOI: 10.5281/zenodo.21935485
Concept DOI: 10.5281/zenodo.21924301
SHA256  BYTES  FILENAME
```

It then contains five rows, in order: source-faithful reader, annotated reader, sources ZIP, evidence ZIP, and `OTHER_TRANSLATIONS.zip`. The manifest does not hash itself.

## Relations

- Canonical DataCite: English concept `IsTranslationOf` French concept.
- Canonical reciprocal: French concept `HasTranslation` English concept.
- Zenodo fallback on English: `isDerivedFrom` French concept.
- Project membership: English concept `IsPartOf` global project.
- Repository: English record `isSupplementedBy` the GitHub repository.
- Exact version/concept and predecessor/successor relations: supplied by Zenodo's version lineage.

## Rights

The record is open access but mixed-rights and therefore uses Zenodo `other-open`, not an unconditional license over every archived byte. `RIGHTS_AND_LICENSING.md` gives the per-file rules; third-party evidence and the French sibling package are not relicensed by the English release.

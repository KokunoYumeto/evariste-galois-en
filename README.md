# Évariste Galois — Mathematical Works (1897): Modern English Reader with GPT Critical Notes

[Open the current linked English reader](reader/00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf) · [Zenodo preview](https://zenodo.org/records/21924302/preview/00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf) · [direct download](https://zenodo.org/records/21924302/files/00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf?download=1)

- Stable English concept DOI: [`10.5281/zenodo.21924301`](https://doi.org/10.5281/zenodo.21924301)
- Exact English release DOI: [`10.5281/zenodo.21924302`](https://doi.org/10.5281/zenodo.21924302)
- French source-language concept DOI: [`10.5281/zenodo.21923856`](https://doi.org/10.5281/zenodo.21923856)
- Exact frozen French release used: [`10.5281/zenodo.21923857`](https://doi.org/10.5281/zenodo.21923857)
- Global project record: [`10.5281/zenodo.20393488`](https://doi.org/10.5281/zenodo.20393488)
- Language: English (`en`; Zenodo/CFF `eng`)
- Family mode: fixed English translation of one fixed historical work, with maintainable critical apparatus
- Exact source coverage: all physical pages PDF001–PDF096 / leaves L0000–L0095 of the 1897 Gauthier-Villars edition, organized as W01–W11; substantive text is translated and figures, excluded scan matter, blank leaves, and page topology are accounted for
- Release: `2026-08-14 en-r1`; Git tag `v2026.08.14-en-r1`
- Publication repository: [`KokunoYumeto/evariste-galois-en`](https://github.com/KokunoYumeto/evariste-galois-en)

This repository is the standalone English publication home. English is on the default `main` branch, and the linked reader above is the primary product. A reader does not need to inspect a multilingual hub, a branch list, or an internal evidence tree to obtain the edition.

## Edition scope and method

The reader translates the complete substantive content of the audited French diplomatic transcription of Évariste Galois's *Œuvres mathématiques* (Paris: Gauthier-Villars et fils, 1897), including the front matter, Émile Picard's Introduction, all collected Galois works and fragments, historical/editorial notes, formulas, contents, and colophon. Source-page anchors map every English segment to the frozen French witness.

The main English text translates the printed historical claim, including claims known to be false, incomplete, or typographically defective. Such material is not silently repaired. A concise, visibly separate `GPT Critical Note` gives the stable identifier, correction or qualification, consequence, and research status beside the relevant passage; exhaustive proofs, propagation records, searches, and provenance remain in the evidence archive. The completed post-P13 program closed all 21 bounded tasks except two explicitly unresolved after search, leaving exactly five cumulative open readings when the three inherited W01 image records are included.

## Roles and attribution

- Historical author: **Évariste Galois**.
- Historical Introduction: **Émile Picard**.
- Edition identity and maintenance: **Manuscript Typesetting Project**.
- Post-P13 web research and mathematical certificates: **OpenAI GPT-5.6 Sol, Pro mode**, where identified by the evidence ledgers.
- Modern-English translation, critical integration, DOI release engineering, and independent QA: **OpenAI GPT-5.6 Sol, Ultra mode**, where identified by the evidence ledgers.

No human translator is invented. Model names describe production roles; they are not presented as natural-person authors or rightsholders.

## DOI relation graph

The authoritative DataCite 4.7 intent is:

- English concept `10.5281/zenodo.21924301` **IsTranslationOf** French concept `10.5281/zenodo.21923856`.
- French concept `10.5281/zenodo.21923856` **HasTranslation** English concept `10.5281/zenodo.21924301`.
- English concept `10.5281/zenodo.21924301` **IsPartOf** global project `10.5281/zenodo.20393488`; the global record reciprocally **HasPart** the English concept.
- Exact English release `10.5281/zenodo.21924302` **IsVersionOf** English concept `10.5281/zenodo.21924301`; Zenodo manages this same-language lineage.

Zenodo does not currently expose `IsTranslationOf`/`HasTranslation`. Until it does, the English record uses the honest machine-readable fallback `isDerivedFrom` the French concept, and the French record should reciprocally use `isSourceOf` the English concept. Translation is not represented as containment or as a cross-language version relation. The exact DataCite directions remain visible here and in `evidence/DATACITE_RELATIONS.json`.

## Public release files

The Zenodo record has a deliberately small, native-first surface in this exact order:

1. `00_GALOIS_1897_EN_CURRENT_LINKED_READER.pdf` — immediately previewable English reader.
2. `01_GALOIS_1897_EN_EDITABLE_SOURCES.zip` — English LaTeX, figures, metadata, and deterministic build inputs.
3. `02_GALOIS_1897_EN_EVIDENCE_AND_PROVENANCE.zip` — source authority, alignment, coverage, critical, unresolved, build, structural, rendered, and hash evidence.
4. `03_GALOIS_1897_EN_SHA256_MANIFEST.txt` — byte counts and SHA-256 values for the other public files.
5. `OTHER_TRANSLATIONS.zip` — one final convenience archive containing the complete current French public release package; it does not change the English DOI's language identity or relation semantics.

The repository exposes the unpacked English sources and evidence. Generated caches, transient render directories, credentials, private custody archives, and unrelated language workspaces are excluded.

## Building and checking

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md). A release closes through source replay, model/agent semantic and formula checks, deterministic non-destructive builds, structural PDF checks, rendered inspection, archive validation, hashes, and honest disclosure of unresolved items. Human review, sign-off, community acceptance, outside certification, and waiting periods are never release gates.

## Rights

The 1897 historical work is public-domain source material. The modern English translation, critical apparatus, typesetting, metadata, scripts, and evidence produced for this edition are dedicated to the public domain under CC0 1.0 to the extent the Manuscript Typesetting Project owns the relevant rights. This does not relicense third-party scans, catalogue metadata, or witness artifacts. See [LICENSE](LICENSE) and `evidence/SOURCE_AUTHORITY.json`.

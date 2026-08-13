# Post-P13 semantic audit closure

Audit date: 2026-08-14 (Europe/Berlin). Release: `2026-08-14 en-r1`.

## Verdict

**PASS after the recorded post-P13 repairs.** The changed critical-note content and current semantic-closure claims in the English reader agree with the validated 16-file post-P13 return, the frozen critical baseline, and the frozen French authority. The task universe is exactly 21 records, the source-error universe is exactly 36 records, the witness/editorial-variant universe is exactly 15 records, and the cumulative open universe is exactly five records. No high- or medium-severity semantic defect remains in the changed post-P13 layer.

This verdict does not re-audit the frozen historical English prose; that prose had already received independent sentence/formula audit and was outside this closure pass. It also does not convert the five disclosed open readings into solved readings. The two bounded-search failures are valid final task dispositions, not failed audit work.

No human review, sign-off, certification, community acceptance, or waiting period is a semantic or release gate. Packaging, repository publication, Zenodo publication, retrieval verification, and the reciprocal French release remain mechanical/external workflow states, not semantic blockers.

## Authorities and custody checked

- The frozen French diplomatic PDF at `source/french_diplomatic/GAL1897_1897_SOURCE_FAITHFUL_CANDIDATE_P13R_AUDIT_BUILD.pdf` is 3,510,046 bytes and independently hashes to `8E6071A2E4A0D38CC89232553CE0CC0314C7EF4BD0A084240C41D60B0AEBBFC5`. That is the exact hash stated in `evidence/SOURCE_AUTHORITY.json` and the returned handoff.
- The 16 returned files, excluding the subsequently written individual-validation receipt, are all present, nonzero, and readable. Their total is 4,108,834 bytes. Every filename, byte count, and SHA-256 matches `evidence/web_post_p13_return/INDIVIDUAL_DOWNLOAD_VALIDATION_RECEIPT.json` (receipt SHA-256 `810E162C076465099310C105A711DDBB6E7C28DAE4420F21EFEA2251983C796A`). The two cold-audit JSON copies are byte-identical and contain 242 unique `PASS` rows out of 242.
- The 36 returned errata IDs exactly equal the 36 frozen IDs in `source/critical_baseline/PRINTED_AND_SOURCE_ERRORS.csv`; worker, PDF page, JP2 leaf, and baseline classification all match. The active `evidence/GPT_CRITICAL_CALLOUTS.tsv` is an exact join for the baseline worker/page/leaf/classification/disposition/proof/evidence/instruction fields and for the returned adjudication, repair, hypotheses, propagation, prior-notice outcome, diplomatic-mutation state, and critical-layer state.
- The 15 returned priority-matrix variant IDs exactly equal the 15 frozen IDs in `source/critical_baseline/WITNESS_VARIANTS.csv`. Worker, page/leaf scope, classification, baseline disposition, evidence IDs, and editorial instruction all survive unchanged into `evidence/GPT_CRITICAL_CALLOUTS.tsv`.

## Twenty-one task dispositions and active references

`evidence/web_post_p13_return/MASTER_21_TASK_LEDGER.csv` and `evidence/POST_P13_TASK_DISPOSITIONS.tsv` are row-for-row equal: 21 unique IDs, no omissions, additions, or status drift. The task table and all 21 certificate headings in the returned `GAL1897_GPT_CRITICAL_EDITION.md` reproduce the same IDs and statuses. `POST_P13_INTEGRATION_SUMMARY.json` lists the same exact set, with `task_ids_without_source_reference: []`. All 21 exact IDs also occur in active English TeX.

| Status | Count | Exact task IDs |
|---|---:|---|
| repaired | 9 | `POST-P13-A001`, `POST-P13-A006`, `POST-P13-A010`, `POST-P13-A011`, `POST-P13-A012`, `POST-P13-A013`, `W10-DA001`, `W10-DA002`, `W10-DA004` |
| proved | 8 | `POST-P13-A002`, `POST-P13-A003`, `POST-P13-A004`, `POST-P13-A007`, `POST-P13-A009`, `POST-P13-A014`, `W11-DA001`, `W11-DA003` |
| rejected | 2 | `POST-P13-A005`, `W10-DA003` |
| unresolved after bounded search | 2 | `POST-P13-A008`, `W11-DA002` |

The active-reference replay found these task anchors or citations (line numbers are the audited snapshot):

| Task(s) | Active English source evidence |
|---|---|
| `POST-P13-A001`--`A003` | `source/english/GAL1897_EN_MODERN_READER.tex:101-107`; exact 9/8/2/2 count, closed error layer, dependency graph, and 51-row prior-notice scope |
| `POST-P13-A004` | `source/english/tex/works/GAL1897_W07_NUMBER_THEORY.tex:273-278`; proved finite-field divisibility argument |
| `POST-P13-A005` | `source/english/tex/works/GAL1897_W07_NUMBER_THEORY.tex:590-598`; rejected degree-9/25-only classification and degree-16 counterexample |
| `POST-P13-A006`--`A008` | `source/english/tex/works/GAL1897_W08_CHEVALIER_LETTER.tex:353-381,462-470`; repaired p=11 row, proved equation/reduction transmission, and unresolved double-prime witness |
| `POST-P13-A009`--`A014` | `source/english/tex/works/GAL1897_W09_RADICALS_MEMOIR.tex:131-144,250-257,327-343,532-551,650-697,830-838,966-998,1200-1207`; lexical findings, Bezout/field-intersection/normality/Fourier/Kummer repairs, and bounded provenance |
| `W10-DA001`--`DA004` | `source/english/tex/works/GAL1897_W10_PRIMITIVE_EQUATIONS.tex:161-167,341-346,616-647`; repaired affine proofs, rejected commutativity premise, and propagation |
| `W11-DA001`--`DA003` | `source/english/tex/works/GAL1897_W11_BACKMATTER.tex:41-50,113-130`; proved contents correction, unresolved printer number, and proved terminal topology |

The wording preserves the meaning of the four status classes. In particular, `rejected` is used only for a disproved historical premise or proposed inference (`POST-P13-A005`, `W10-DA003`), never as an audit-failure label. Repaired claims state the needed replacement, qualification, or proof; proved claims state what survives; the two unresolved tasks do not guess a result.

## Thirty-six errors and fifteen variants

The 36 unique error IDs are distributed W02 1, W03 3, W04 4, W05 2, W06 2, W07 5, W08 2, W09 8, W10 8, W11 1:

`W02-PE001`; `W03-PE001`--`PE003`; `W04-SE001`--`SE004`; `W05-SE001`--`SE002`; `W06-PE001`, `W06-SE001`; `W07-SE001`--`SE005`; `W08-PE001`--`PE002`; `W09-PE001`--`PE002`, `W09-SE001`--`SE006`; `W10-PE001`--`PE006`, `W10-SE001`--`SE002`; `W11-PE001`.

For all 36 rows:

- `critical_layer_state` is `closed` and `diplomatic_layer_mutated` is `no`;
- adjudication, critical repair, minimal hypotheses, proof certificate, propagation outcome, prior-notice outcome, and source pointers are nonempty;
- the returned critical Markdown contains exactly 36 error blocks, and all eight labelled fields in every block reproduce the catalogue exactly;
- the integrated callout ledger reproduces the returned final fields exactly; and
- active English TeX has one unique `GalCriticalNote` for every error ID. No error ID is missing, duplicated, renumbered, or silently applied to the historical layer.

The 15 variant IDs are exactly `W08-WV001`--`W08-WV003`, `W09-WV001`--`W09-WV006`, and `W10-WV001`--`W10-WV006`. Each has one unique row in the frozen baseline, the 51-row prior-notice matrix, the integrated callout ledger, and active English TeX. Fourteen have `critical_layer_state=closed`; only `W08-WV001` remains `open`, consistently with its task and cumulative-open disposition. Variants remain witness/editorial evidence rather than being inflated into additional 1897 errors.

The active TeX contains all 51 baseline error/variant notes exactly once. Its additional task, terminology, topology, and unresolved-reading notes are separately identified; they do not change the 36+15 baseline universe.

## Prior-notice and propagation claims

The returned `BIBLIOGRAPHIC_PRIOR_NOTICE_MATRIX.csv` has 51 unique rows: 36 `proved_source_error` and 15 `witness_or_editorial_variant`. All rows carry the 2026-08-13 cutoff. The active callout ledger exactly preserves each row's `notice_class`, `earliest_secure_notice_or_attestation`, and `search_cutoff`; the item-level historical wording in active TeX agrees with those fields.

The notice classes comprise 23 bounded `no_prior_notice_found_in_searched_corpus` findings and 28 affirmative/qualified transmission findings. The latter correctly distinguish, rather than merge: a correct earlier witness without explicit notice; explicit 1846 or 1908 notice/collation; the same error already attested in 1846; later silent correction; later reconstruction; and a documented but still semantically unresolved manuscript formula. The 1976 Bourgne--Azra errata list is described only as a proven but item-level-inaccessible candidate; no error is attributed to that list without evidence. Negative searches are bounded findings, not novelty claims.

Specific high-risk priority statements agree across matrix, returned catalogue/Markdown, and active notes: Liouville's 1846 notice for `W05-SE002`; the correct 1846 row without explicit erratum for `W08-PE001`; correct 1846 reading plus Tannery's 1908 collation for `W08-PE002`; the 1846 `cette fonction` witness without itemized notice for `W09-PE001`; Tannery's insufficiency/revision evidence for `W09-SE001`--`SE003`; explicit 1908 corrections for `W10-PE001`--`PE003` and `PE005`; 1846 attestation of the same uncorrected error for `W10-PE006`/`W10-WV006`; and the dated 2018 silent `v` correction for `W11-PE001`, with no unsupported claim from the inaccessible 1976 list or ETH metadata.

The dependency ledger has 46 rows. All source IDs resolve to a frozen error or audited task, all certificate fields are populated in the returned evidence, and the active notes preserve the decisive outcomes: local closure, survival under added hypotheses, or a blocked downstream claim. In particular, the degree-9/25 claim and PDF089 p=3 inference remain rejected/blocked rather than being mislabeled as repaired.

## Exact cumulative open set

The returned `OPEN_AFTER_21_TASKS.csv`, active `UNRESOLVED_ITEMS.tsv`, integration summary, reader front matter, and active notes agree on exactly five IDs:

| ID | Current disposition |
|---|---|
| `W01-U001` | carried forward unresolved outside the 21-task scope; faint portrait signature |
| `W01-U002` | carried forward unresolved outside the 21-task scope; relation of the degraded portrait page to PDF019 |
| `W01-U003` | carried forward unresolved outside the 21-task scope; publisher-device ribbon legend |
| `W08-WV001` | unresolved after bounded search; manuscript double-prime formula lacks a secure notation key |
| `W11-U001` | unresolved after bounded search under task `W11-DA002`; fused four-digit printer job number |

For each ID, returned status and missing-evidence text exactly equal the active status and required-action text, and `rendered_note=true`. The active TeX renders all five disclosures. No sixth item is open, and none of the five is represented as solved.

## Stale-state scan

No stale `pending` or `deferred` semantic claim remains in the active English TeX or in the current post-P13 critical ledgers (`GPT_CRITICAL_CALLOUTS.tsv`, `POST_P13_TASK_DISPOSITIONS.tsv`, `UNRESOLVED_ITEMS.tsv`, `POST_P13_INTEGRATION_SUMMARY.json`, and `TRANSLATION_LEDGER_BUILD.json`). The translation-build receipt explicitly distinguishes `baseline_deferred_research_records: 21` from `post_p13_remaining_deferred_research_records: 0`. `ENGLISH_COVERAGE.tsv` records semantic and rendered QA as passed for all eleven components and describes only publication as pending.

Current `QA_STATE.json` and `QA_REPORT.md` likewise record semantic closure and the exact 9/8/2/2 and five-open counts. Their pending archive, GitHub, Zenodo, and reciprocal-French states are accurate outstanding packaging/publication operations and do not contradict semantic closure.

Historical wording remains, intentionally and outside the active-current set, in the frozen critical baseline, the returned handoff's description of the formerly deferred program, `evidence/coverage_fragments/`, and the predecessor `evidence/SEMANTIC_AUDIT_CLOSURE.md`. Those files are immutable provenance, not current closure claims; this report supersedes the predecessor only for post-P13 state and does not rewrite it. A phrase `not yet` in W08 is translated historical prose, not workflow status.

## Remaining limitation and release effect

The 313,572,719-byte cumulative ZIP `GAL1897_CUMULATIVE_P00-P13R_POST_P13_GPT_CRITICAL_EDITION_21_TASKS.zip` is absent. Its sidecar and package receipt agree on expected SHA-256 `C3D91146F5772861E614EF8C2FA42749D163274773D786051F6E9E499E417E44`, 182 payload files, 180 manifest records, and output-set fingerprint `0C78078E584DD96612A5BFAA3E1AA3609C96B76D334C9F8644D95E88327FB5B6`, but this audit cannot independently verify the absent ZIP's bytes, CRC, deterministic packaging, or internal 180-record hash replay. Those remain returned claims.

This limitation is fully disclosed and does not block semantic closure because the complete 16-file individual return was independently hash-validated and parsed, including the maintained critical source, task/error/open ledgers, prior-notice and web-evidence ledgers, both PDFs, and both identical 242-check cold-audit JSON copies. It does remain a custody limitation on the missing cumulative archive itself.

**Final semantic state: `PASS_POST_P13_AFTER_REPAIRS`; semantic blockers: none; human gate: none.**

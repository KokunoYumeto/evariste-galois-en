# R2 semantic audit closure after the post-P13 deep replay

Audit date: 2026-08-14 (Europe/Berlin). Release: `2026-08-14 en-r2`.

## Verdict

**PASS_R2_AFTER_DEEP_REPLAY_AND_READER_HUMANIZATION.** The English translation remains aligned to the frozen French diplomatic source, the 21-task research program is fully dispositioned, both R2 witness resolutions are integrated, and the reader-facing apparatus has been rewritten in ordinary editorial prose without altering the historical text. No high- or medium-severity semantic blocker remains.

No human review, sign-off, certification, community acceptance, or waiting period is a semantic or release gate. Packaging and publication are separate mechanical states.

## Controlling universes

| Evidence universe | Final count or state |
|---|---:|
| Ordered works/components | 11 |
| Aligned English segments | 587 |
| Physical source pages accounted for | 96 |
| Source-error records | 36 |
| Witness/editorial variant records | 15 |
| Post-P13 task records | 21 |
| Dependency edges | 48 |
| Prior-notice rows | 52 |
| Documented searches | 22 |
| Split-package source records replayed | 164/164 |
| Cold-audit checks | 242/242 PASS |

The 21 tasks have exactly these final dispositions:

| Disposition | Count |
|---|---:|
| repaired | 10 |
| proved | 9 |
| rejected | 2 |
| unresolved | 0 |

All 36 source-error records remain closed in the editorial layer and unmodified in the diplomatic layer. All 15 witness/editorial variants remain represented according to their final disposition.

## R2 changes from the predecessor

1. `W08-WV001 / POST-P13-A008` is repaired. Direct replay of the 600-ppi Tannery witness reads `E′F″−E″F′=(π/2)√−1`. The determinant form is equivalent to the printed Legendre relation under the recorded normalization. The English reader explains this in a human-facing note and does not silently replace the historical line.
2. `W11-U001 / W11-DA002` is proved. An independent ETH-Bibliothek copy and its OCR resolve the printer job number as the five-digit sequence `24572`. The historical crop is retained; the note supplies the independent reading and provenance.

These closures supersede the R1 state of 9 repaired / 8 proved / 2 rejected / 2 unresolved and its five-record open set.

## Remaining open records

Exactly three records remain open, all outside the 21-task program and all confined to preliminary images:

- `W01-U001`: a faint portrait signature cannot be read securely.
- `W01-U002`: the relation between the two portrait scans is not established.
- `W01-U003`: the publisher-device ribbon is too indistinct for character-by-character transcription.

The images remain visible and the reader does not guess. No other record is represented as open or deferred.

## Reader and evidence agreement

The active English source contains 65 unique `GalCriticalNote` anchors and three W01 `GalWitnessNote` anchors. The 36 errors, 15 variants, task-level qualifications, terminology checks, topology statements, and three open image records are preserved through stable evidence IDs. Reader-facing headings are descriptive; internal IDs appear only as small editorial references. Machine status fields, task codes, filenames, hashes, and audit shorthand remain in the evidence archive.

The source-structure validator passes over all eleven French/English pairs, preserving source coordinates, issue IDs, ordered call payloads, and pinned formula deltas. The translation ledger passes for all 587 segments and 96 physical pages. Two clean R2 reader builds are byte-identical, and structural, mechanical-render, and actual all-page visual inspection receipts pass for the exact 84-page PDF with SHA-256 `2AF04298A1184307C2F94B82FAE55E6AA0BDA4560C2E95461537924AB814E6D5`.

## Received-package defect and custody statement

The independently verified R2 split return replays all 164 distributed source records. One aggregate source fingerprint is reproducible in manifest order rather than the receipt's stated filename-sort order; all 35 individual source hashes match, so this is a canonicalization warning rather than payload corruption.

Two changed master-ledger rows cite an absent `qa/OPEN_TASK_RESOLUTION_CHECKS.json`. The received package is preserved byte-for-byte and the dangling pointer is disclosed. The two resolutions are supported by the present task certificates, comparison figures, source replay, mathematical checks, witness files, and 242/242 cold audit. This report does not claim that the absent file exists.

**Final semantic state: `PASS_R2_AFTER_DEEP_REPLAY_AND_READER_HUMANIZATION`; semantic blockers: none; open records: exactly three inherited W01 image questions; human gate: none.**

# POST-P13-A001 — complete errata repair

Critical-layer certificate. The frozen 78-page P13R diplomatic edition is immutable.

**Status:** repaired

This certificate belongs to the critical layer. The P13R diplomatic transcription and its 78-page PDF are immutable. No wording below authorizes a silent change to that layer. Coordinates are physical PDF/JP2 coordinates from the frozen map.

**Theorem.** Every one of the 36 records in `CRITICAL_ERRATA_CATALOGUE.csv` has been closed by exactly one of the following critical actions: a typographical or formula repair proved from the 1897 context and another witness; an added hypothesis proved necessary and sufficient for the local step; a replacement proof; or a counterexample rejecting the printed universal claim.

**Proof.** The catalogue is an exact join with the frozen 36-row source-error ledger. Its `error_id` set is identical, every row states `diplomatic_layer_mutated=no`, and each row has a nonempty adjudication, repair, proof, propagation outcome, and prior-notice outcome. Exact symbolic and finite-group checks are in `qa/MATHEMATICAL_CHECKS.json`. No record has been deleted, merged, or renumbered.

The principal nonlocal replacements are: the affine primitive theorem for W05-SE001 and POST-P13-A005; the characteristic-p squarefree and exact-degree algorithms for W07-SE003–005; the field-intersection, Bézout, Fourier, and Kummer repairs for W09-SE001–006; and the minimal-normal-subgroup affine proof for W10-DA001–002. The remaining entries are local textual, sign, formula, index, or identity corrections.

**Conclusion.** The errata layer is complete as an adjudication of the frozen 36 records. It is not a translation and it does not assert that every diagnosis is historically new.

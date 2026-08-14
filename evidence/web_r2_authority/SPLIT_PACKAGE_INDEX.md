# Galois 1897 GPT Critical Edition R2 - two-part distribution

Extract both archives into the same destination directory.

- Part 01 contains the exact 195,472,443-byte repaired-candidate component archive and its SHA-256 receipt.
- Part 02 contains the critical edition, one-click reader, source packet, evidence, certificates, ledgers, QA, provenance, cold re-audit, repaired W02 component, and all remaining repaired-handoff metadata.

The original full R2 archive SHA-256 is `5824445BAB2245F4E4FCEF93688AB4750089097F64FE797A37F1D5354D9528F8`.
The expanded nested repaired-handoff wrapper SHA-256 is `05C2247E2127BF816B838DA668EB9EF05AC6981D09862FB819470D79DFE3E74B`.

The split is logical rather than a raw binary span: each ZIP opens independently, and the two extracted trees merge into one package root. The original nested wrapper is represented by its exact expanded members because the wrapper itself exceeded the requested per-file ceiling.

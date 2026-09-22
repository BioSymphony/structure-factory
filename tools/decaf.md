# DeCAF-Boltz

Reviewed 2026-09-22. DeCAF-Boltz distills a Boltz-1 cofolder into a few-step
sampler. The [released source](https://github.com/genesistherapeutics/decaf/tree/471477e0e786f91bae77d4cebf4b7d14901bc174)
and [June 2026 preprint](https://arxiv.org/abs/2606.08375) describe the method.
Code and checkpoints are available; Structure Factory integration still needs
an adapter and a measured comparison.

## Checkpoint choice

The [model card](https://huggingface.co/genesisml/decaf) distinguishes two files:

| Checkpoint | Recorded output |
| --- | --- |
| `decaf_ckpt.ckpt` | Structures without a confidence head |
| `decaf_conf_ckpt.ckpt` | Structures plus the Boltz-1 confidence module, pLDDT, ipTM, and PAE |

Use the confidence-enabled identity when evaluating confidence sidecars.
Record both source and checkpoint hashes. The source example uses a public
MSA service; declare the input policy and alignment route before execution.
The model card and source license state MIT terms; review carried Boltz code
and dependency notices independently.

## Comparison contract

Record input and chain mappings, teacher identity, sample and step counts,
wall time, peak memory, output counts, geometry checks, and confidence matrices.
Compare against the teacher on a fixed panel and retain per-complex results.
Check sidecar parsing and ranking behavior before changing a screening policy.
The paper's protein-ligand benchmark claims require a separate test for protein
interfaces. Store the compact speed/quality table and manifest with runtime
artifact hashes.

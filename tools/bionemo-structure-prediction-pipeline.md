# BioNeMo Structure Prediction Pipeline

Use NVIDIA's BioNeMo Structure Prediction Pipeline to plan Slurm-based
preprocessing, folding, and postprocessing with verified phase handoffs.
The pipeline orchestrates selected prediction backends; the backend and
checkpoint determine the scientific model.

Source reviewed 2026-10-01 at
[`cb14f6eb3302b6701884123b6b5453ba5fe8cdf9`](https://github.com/NVIDIA-BioNeMo/BioNeMo-Structure-Prediction-Pipeline/tree/cb14f6eb3302b6701884123b6b5453ba5fe8cdf9).

## Workflow And Inputs

The [upstream overview](https://github.com/NVIDIA-BioNeMo/BioNeMo-Structure-Prediction-Pipeline/blob/cb14f6eb3302b6701884123b6b5453ba5fe8cdf9/docs/pipeline-overview.md)
defines three phases:

| Phase | Work | Handoff Evidence |
| --- | --- | --- |
| Preprocessing | GPU MMseqs2/ColabFold MSA search | Database identity and content-addressed MSA members |
| Folding | Selected `bioir`, `openfold-cli`, or `colabfold` backend | Verified MSA input, checkpoint identity, structures, and confidence outputs |
| Postprocessing | Confidence and interface metrics, including ipSAE and pDockQ2 | Source structure mapping, metric settings, and accepted outputs |

`bsppctl` materializes a Phase Plan and cluster Profile into an immutable
RunSpec. Operators submit and close each phase separately, with verified job
records and phase receipts. Local files or object storage connect phases.
See the [upstream README](https://github.com/NVIDIA-BioNeMo/BioNeMo-Structure-Prediction-Pipeline/blob/cb14f6eb3302b6701884123b6b5453ba5fe8cdf9/README.md).

## Runtime Requirements

Provide a qualified Slurm site with Pyxis/Enroot, NVIDIA GPUs, built images,
search databases, model checkpoints, and stage storage. Structure Factory needs
a site-specific adapter and output mapping before execution.

Set `folding_release_preset: public` for the documented public BioIR
configuration. The opt-in `expanded-chain-count-v1` policy routes one expanded
chain to `openfold2_ptm_1` and multiple chains to `alphafold2_multimer_1`.
Record the policy and each checkpoint separately.

At this source pin, `openfold-trt` is a contract value that fails before
execution. The [release status](https://github.com/NVIDIA-BioNeMo/BioNeMo-Structure-Prediction-Pipeline/blob/cb14f6eb3302b6701884123b6b5453ba5fe8cdf9/docs/status.md)
also distinguishes phase completion from benchmark validation. The shipped
1,000-target public PDB cohort supplies benchmark inputs; it does not establish
completed folding throughput or accuracy.

## Outputs And Review

Retain phase Plans, Profiles, RunSpecs, receipts, source and image hashes,
database/checkpoint identities, MSA member hashes, chain mappings, structures,
confidence sidecars, and validation results in runtime storage. Record actual
GPU allocation and stage timings before comparing performance.

Use the [BioIR card](bioir.md) for model/runtime compatibility and the
[prediction handoff contract](../docs/prediction-handoff-contract.md) for
downstream joins. A scheduler exit, accepted artifact receipt, and structural
accuracy evaluation are separate records.

## License And Assets

The orchestration code is Apache-2.0. Selected images, dependencies, search
databases, and model checkpoints retain their own terms. Review the pinned
[license](https://github.com/NVIDIA-BioNeMo/BioNeMo-Structure-Prediction-Pipeline/blob/cb14f6eb3302b6701884123b6b5453ba5fe8cdf9/LICENSE)
and [component notices](https://github.com/NVIDIA-BioNeMo/BioNeMo-Structure-Prediction-Pipeline/blob/cb14f6eb3302b6701884123b6b5453ba5fe8cdf9/THIRD_PARTY_NOTICES.md)
before installation or redistribution.

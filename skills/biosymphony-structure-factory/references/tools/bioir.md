# BioNeMo Inference Runtime

## Purpose

Use NVIDIA BioNeMo Inference Runtime (BioIR) as an optimized implementation
beneath a supported structure-prediction model. BioIR does not define a new
scientific predictor: the model family, checkpoint, inputs, sampling settings,
and output contract remain the scientific identity.

## Public-Safe Status

The public registry documents BioIR 0.1.0 and its runtime boundary. No bundled
Structure Factory adapter selects or launches it. A run therefore needs a
validated model-specific adapter and a compatible Linux/NVIDIA environment.

Upstream documents complete `build_processor` pipelines for
AlphaFold2/OpenFold2 variants, Boltz-1/2, and OpenFold3. Protenix-v2 and
Boltz-2 affinity expose model modules without complete pipelines. A model
module alone is not an executable end-to-end route.

## Selection Rules

- Preserve the requested scientific model and checkpoint when changing the
  runtime.
- Preserve sequence, chain, ligand, MSA, template, seed, recycle, sampling,
  and output settings.
- Record the confidence scale before applying a gate or comparing predictors.
- Keep preprocessing, model execution, postprocessing, scoring, and total
  elapsed time separate.
- Use a matched baseline when making correctness or speed claims.

## Runtime Requirements

The reviewed upstream prerequisites specify Linux, Python 3.12, glibc 2.34 or
newer, and a compatible NVIDIA driver and GPU. Check the current upstream
support matrix before choosing hardware. A successful import proves dependency
readiness; it does not prove checkpoint loading, prediction, output conversion,
or scientific comparability.

## Expected Evidence

- runtime and package manifest
- exact scientific model and checkpoint identity
- input and asset hashes
- parseable structure output
- complete confidence sidecars with a declared scale
- chain, residue, and atom accounting
- stage timing and peak-memory record
- adapter receipt and artifact hashes
- matched comparison notes when replacing another implementation

## License And Data Gates

BioIR code is Apache-2.0, with third-party notices and separately governed
runtime components. Selected checkpoints retain their own terms. Review the
exact image, dependencies, and checkpoint before redistribution or execution.
Keep weights, generated structures, private inputs, service credentials, and
provider records outside public git.

## Primary Sources

- Repository: https://github.com/NVIDIA-BioNeMo/BioNeMo-Inference-Runtime
- Support matrix:
  https://github.com/NVIDIA-BioNeMo/BioNeMo-Inference-Runtime/blob/main/docs/ref/support-matrix.md
- Model weights:
  https://github.com/NVIDIA-BioNeMo/BioNeMo-Inference-Runtime/blob/main/docs/ref/model-weights.md
- PyPI: https://pypi.org/project/bionemo-ir/

## Result Boundary

Runtime substitution can support a validated implementation-equivalence or
performance claim only after a matched comparison. Predicted structures remain
computational evidence and do not establish binding, function, affinity,
safety, or therapeutic value.

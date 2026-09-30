# Anthropic Inference Optimization Kits

## Purpose

Evaluate Anthropic's `uplifting-biomolecular-modeling` optimization kits as
runtime implementations beneath existing scientific tool identities. The
release provides 36 pinned kits for structure prediction, cofolding, binder and
sequence design, protein language models, and genomics models.

An optimization kit does not create a new scientific predictor when its
`off`, `exact`, `fast`, or `big` modes use the same upstream model and
checkpoint. It does create a distinct runtime identity that must remain visible
in provenance, numerical comparisons, and timing reports.

## Public-Safe Status

The public registry records upstream commit
`f4f62fa6592ae4938d49b1757bea0cfeff9f468e`, rechecked on 2026-09-30. This
repository does not vendor the kits, their stock trees, compiled kernels,
containers, weights, or runtime hooks. It does not bundle an executable adapter.
The machine-readable
[qualification record](../references/anthropic-optimization-kit-qualification.json)
defines mode promotion, compatibility, preflight, and artifact requirements.

Upstream describes the repository as an unmaintained reference release. Pin the
repository commit and each selected kit's `STOCK.md`, lock file, notices, and
weight digests. Do not install from a moving branch.

## Modes

Each kit ships a subset of a shared mode vocabulary:

| Mode | Upstream meaning | Structure Factory acceptance |
| --- | --- | --- |
| `off` | Pinned stock implementation | Baseline arm; preserve its complete runtime identity. |
| `exact` | Faster with output identical to `off` | Verify byte or array equality on the selected operation before promotion. |
| `fast` | Faster with documented numerical differences | Compare against `off`, `exact` when shipped, and a reseeded stock arm. Recalibrate thresholds. |
| `big` | Lower peak memory; some kits support single-host multi-GPU execution | Validate output equivalence class, memory, worker completion, and device topology. |

Upstream modes print an `ACTIVE` record. A mode that cannot engage reports
`NOT ACTIVE` and exits with code 3 instead of silently falling back. Capture
that record as a required artifact.

## Complete Pinned Inventory

The following 36 kits and mode sets are recorded from the pinned upstream
[release catalog](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/README.md#kits). `multi-GPU` marks
kits that list `--n_gpu P`; consult their own operation and device requirements.
The [qualification record](../references/anthropic-optimization-kit-qualification.json)
also contains this inventory.

| Kit | Operation | Modes | Single-host multi-GPU |
| --- | --- | --- | --- |
| [`af2ig`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/af2ig/README.md) | binder-target interface scoring | `off`, `exact`, `fast`, `big` | — |
| [`af3_jax`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/af3_jax/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |
| [`af3_torch`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/af3_torch/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |
| [`atlasfold`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/atlasfold/README.md) | structure prediction | `off`, `exact`, `fast`, `big` | — |
| [`boltz2`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/boltz2/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |
| [`boltzgen`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/boltzgen/README.md) | binder design | `off`, `exact`, `fast`, `big` | — |
| [`borzoi`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/borzoi/README.md) | variant effect scoring | `off`, `exact` | — |
| [`caliby`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/caliby/README.md) | sequence design | `off`, `exact`, `fast` | — |
| [`chai1`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/chai1/README.md) | cofolding | `off`, `exact`, `fast`, `big` | — |
| [`chrombpnet`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/chrombpnet/README.md) | chromatin accessibility prediction | `off`, `exact`, `fast` | — |
| [`colabdesign`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/colabdesign/README.md) | binder hallucination | `off`, `exact`, `fast` | — |
| [`colabfold`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/colabfold/README.md) | structure prediction from MSAs | `off`, `exact`, `fast`, `big` | Listed |
| [`complexa`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/complexa/README.md) | binder generation | `off`, `exact`, `fast`, `big` | — |
| [`e1`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/e1/README.md) | protein LM mutant scoring | `off`, `exact` | — |
| [`ef2inv`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/ef2inv/README.md) | gradient-based binder design | `off`, `exact`, `fast`, `big` | — |
| [`enformer`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/enformer/README.md) | genomic track prediction | `off`, `exact` | — |
| [`enformer_deepmind`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/enformer_deepmind/README.md) | genomic track prediction | `off`, `exact` | — |
| [`esm_if1`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/esm_if1/README.md) | inverse folding | `off`, `fast` | — |
| [`esmc`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/esmc/README.md) | protein LM inference | `off`, `exact` | — |
| [`esmfold2`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/esmfold2/README.md) | structure prediction | `off`, `exact`, `fast`, `big` | Listed |
| [`evo2`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/evo2/README.md) | genomic LM scoring and generation | `off`, `exact`, `fast` | — |
| [`flashzoi`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/flashzoi/README.md) | genomic track prediction | `off`, `exact` | — |
| [`genie3`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/genie3/README.md) | backbone diffusion, binder design | `off`, `exact`, `fast` | — |
| [`gpnstar`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/gpnstar/README.md) | variant effect scoring from whole-genome alignments | `off`, `exact` | — |
| [`mosaic`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/mosaic/README.md) | binder hallucination | `off`, `exact`, `fast`, `big` | — |
| [`opendde`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/opendde/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |
| [`openfold3`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/openfold3/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |
| [`openfold3_ob0`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/openfold3_ob0/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |
| [`progen2`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/progen2/README.md) | protein LM sampling and likelihood | `off`, `exact` | — |
| [`proteinmpnn`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/proteinmpnn/README.md) | sequence design | `off`, `exact` | — |
| [`protenix_v1`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/protenix_v1/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |
| [`protenix_v2`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/protenix_v2/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |
| [`pxdesign`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/pxdesign/README.md) | binder diffusion | `off`, `exact`, `fast`, `big` | — |
| [`rfdiffusion1`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/rfdiffusion1/README.md) | backbone generation | `off`, `exact`, `fast` | — |
| [`rfdiffusion3`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/rfdiffusion3/README.md) | all-atom backbone generation | `off`, `exact`, `fast` | — |
| [`rosettafold3`](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/rosettafold3/README.md) | cofolding | `off`, `exact`, `fast`, `big` | Listed |

Inventory coverage does not establish local installation, adapter support, or
measured speedups. Modes absent from a row must not be requested. In particular,
`esm_if1` has no `exact` mode, and `proteinmpnn` has neither `fast` nor `big`.

## Structure Factory Compatibility

Compatibility is an exact stack property, not a tool-name match.

| Kit or family | Upstream stock identity | Public repository posture |
| --- | --- | --- |
| `boltz2` | Boltz 2.2.1 | Same scientific package version is recorded publicly. Adapter, environment, kernel, and output-contract qualification remain required. |
| `esmfold2` | Biohub ESMFold2 on the kit's pinned ESM 3.3.0 stack | Separate environment. The public registry records `esm==3.4.1.post1`; do not overlay the kit on that package or claim current-adapter compatibility. |
| `ef2inv` | ESMFold2-based gradient binder design on its own pinned stack | Separate sequence-design operation and adapter; prediction readiness does not establish design readiness. |
| `openfold3` | OpenFold3 0.4.1 with preview parameters | Version and checkpoint differ from the public OpenFold3 0.5.0/OpenBind v0 record. Treat as a separate scientific identity. |
| `openfold3_ob0` | OpenFold3 0.5.0 with OpenBind-0 parameters | Candidate version match for the public OpenFold3 record; verify checkpoint digest, dependencies, operation, and output equality. Keep it distinct from the preview `openfold3` kit. |
| `boltzgen` | BoltzGen 0.3.2 | Candidate binder-design runtime; qualify the chosen protocol and stage outputs. |
| `complexa` | Proteina-Complexa 1.1.0 | Candidate binder-generation runtime; preserve the selected generation, reward, and refinement settings. |
| `rfdiffusion3` | Foundry commit `4010e3e2e7350edada3e25a45c908c6bf407df4d`, `rc-foundry==0.2.1.dev13+g4010e3e2e` | Dedicated Foundry environment and source overlay; compare the exact stock version and checkpoint before adoption. |
| `proteinmpnn` | ProteinMPNN commit `8907e667`, vanilla or soluble weights | `exact` supports full-backbone sequence design; CA-only and other excluded operations need the supported stock route below. |
| `caliby`, `genie3`, `pxdesign`, `rfdiffusion1`, `protenix_v2`, `chai1` | Kit-specific pins in `STOCK.md` | Candidate acceleration layers for corresponding workflow stages. Compare exact source, checkpoint, dependency, and input/output contracts before adoption. |

The upstream tree contains additional protein and genomics kits. Presence in
that inventory is documentation, not Structure Factory capability or execution
readiness.

## ProteinMPNN Operation Limits

The pinned [ProteinMPNN kit](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/proteinmpnn/README.md#modes)
ships explicit `off` and `exact` modes for vanilla and soluble weight sets.
Its `exact` design route refuses `--ca_only`, `--score_only`,
`--conditional_probs_only`, `--unconditional_probs_only`,
`--tied_positions_jsonl`, and `--backbone_noise` above zero. Use the supported
stock `off` route for those operations and record that choice explicitly.
A Genie3 handoff containing only C-alpha coordinates therefore requires the
CA-only stock route, rather than the full-backbone `exact` route.

## Isolation And Activation

Several kits use interpreter startup hooks, `sitecustomize`, import hooks, or
anchored in-memory source substitutions. Two Foundry kits install file overlays
in a dedicated interpreter. Run each kit in its own pinned environment or
container. Do not add its hook directory to a shared control-plane Python
environment.

Before inference:

1. Verify the repository commit and the selected kit's stock, lock, binary, and
   weight digests.
2. Run the kit's no-model or dry-run check for the selected GPU card and mode.
3. Require the expected `ACTIVE` line and lever inventory.
4. Refuse code 3, missing activation evidence, an unknown source anchor, or
   silent stock fallback.
5. Use trusted, digest-pinned weights. Treat pickle-based model files as
   executable code.

## Qualification Matrix

Use the same public or synthetic input, checkpoint, seed, model settings,
sampling settings, confidence outputs, and artifact validators in every arm:

1. `off`, cold;
2. `off`, warm;
3. `exact`, cold and warm, when shipped;
4. `fast`, cold and warm, when shipped;
5. `big`, when memory or input size requires it;
6. a second `off` seed or repeat for stochastic tools.

Qualify each accelerated operation within the declared native workflow. Retain
required reward, sequence-design, evaluation, refinement, and filtering stages;
record omitted stages in the [comparison contract](../docs/binder-comparison-contract.md).
A short kit example does not define the complete scientific comparison recipe.

Record setup, compilation, model load, preprocessing, model execution,
postprocessing, scoring, and total elapsed time separately. Peak memory,
compile-cache state, device identity, input shape, and sample count belong in
the same report.

`exact` promotion requires the equality promised by the selected kit for the
actual output contract. `fast` promotion requires metric-specific
recalibration; an upstream statement about seed-to-seed variation does not
validate a local threshold. Performance claims apply only to the measured
hardware, stack, input distribution, and timing boundary.

## Required Artifacts

- kit repository commit and selected kit name
- `STOCK.md`, lock, source, dependency, checkpoint, and weight identities
- mode, GPU-card configuration, device/runtime identity, and activation record
- lever inventory and any disabled or fallback kernel
- compile-cache posture and prebuilt-binary digest verification
- command argument array and environment-variable names, without secret values
- input, output, confidence-sidecar, and score hashes
- cold/warm timing and peak-memory records
- equality or numerical-difference report against `off`
- validation, failure, cleanup, and result-boundary records

## License And Distribution

Anthropic's original kit code is Apache-2.0. Each carried stock project keeps
its own license; model weights and third-party components retain their own
terms. Review the selected kit's `LICENSE`, `STOCK.md`,
`THIRD_PARTY_NOTICES.md`, and the repository-level `NOTICE` before
installation, image inclusion, or redistribution.

Public documentation and adapter scaffolding are allowed. Public images remain
review-required because a selected kit can include stock source, compiled
payloads, CUDA dependencies, and components with different redistribution
terms. Keep weights, caches, generated structures, private inputs, and provider
records outside public git.

## Primary Sources

- Repository:
  https://github.com/anthropics/uplifting-biomolecular-modeling
- Top-level license:
  https://github.com/anthropics/uplifting-biomolecular-modeling/blob/main/LICENSE
- Repository notice:
  https://github.com/anthropics/uplifting-biomolecular-modeling/blob/main/NOTICE
- ESMFold2 kit:
  https://github.com/anthropics/uplifting-biomolecular-modeling/tree/main/esmfold2

## Result Boundary

Optimization evidence can establish measured runtime, memory, and numerical
behavior for a pinned configuration. It does not raise the underlying model's
scientific claim level or establish binding, function, affinity, safety,
therapeutic value, or general equivalence across hardware and inputs.

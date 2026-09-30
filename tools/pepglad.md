# PepGLAD

## Purpose

Plan full-atom peptide sequence and structure co-design conditioned on a
receptor pocket. Preserve the native co-designed sequence and structure as a
paired candidate; any later sequence redesign creates a separate child.

## Public-Safe Status

Source reviewed on 2026-09-30 at commit
[`bad015ca50c312a89482adb5220c3d907f13df5c`](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/README.md).
The selected main-branch code has an [MIT license](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/LICENSE).
Review checkpoint and dependency terms separately. Structure Factory records
this upstream workflow; execution requires a qualified adapter.

## When To Use

- Joint peptide sequence and conformation generation around a declared pocket.
- Fixed-sequence peptide conformation sampling as a separate comparison arm.
- Downstream comparison using the [common scoring stack](cofold-scoring-stack.md).

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill with the PepGLAD tool card. For public target <PDB:ID> and pocket <chain/residue map>, prepare a codesign lane with an explicit length range, sample count, source and checkpoint pins, output validation, and independent cofold handoff.
```

## Native Operations And Inputs

| Operation | Required input | Checkpoint selected by the pinned CLI |
| --- | --- | --- |
| `codesign` | Receptor PDB, pocket JSON, length bounds, sample count | `checkpoints/codesign.ckpt` |
| `struct_pred` | Receptor PDB, pocket JSON, fixed peptide sequence, sample count | `checkpoints/fixseq.ckpt` |

`--length_min` is inclusive and `--length_max` is exclusive. The pocket
file is a JSON list of chain/residue-ID pairs, including insertion codes.
Validate each selection against the input structure. Motif preservation or
cyclic topology requires a separately supported operation and preservation
checks; the reviewed CLI does not expose those controls.
[Generation CLI](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/api/run.py),
[pocket writer](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/api/detect_pocket.py).

## Native Output Contract

The pinned CLI writes combined receptor/peptide PDB files in a flat output
directory and one `summary.jsonl`. Each row contains `id`, `rec_chains`,
`pep_chain`, and `pep_seq`; its structure is `<id>.pdb`. The peptide chain
ID depends on the receptor chains. Resolve it from the row and verify its
sequence rather than assuming a fixed chain or filename convention.

Closeout checks the expected row and structure counts, unique identifiers,
parseable coordinates, chain mapping, sequence agreement, and output hashes.
The native API then performs OpenMM relaxation; retain its completion status
separately from generation. A changed relaxation route is a different workflow
arm. [Pinned output and relaxation implementation](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/api/run.py).

## Sequence And Scoring Handoff

Carry `pep_seq`, its matching structure, source/checkpoint hashes, and the
pocket map into independent cofold and geometry assessment. Keep native
parents in the denominator. ProteinMPNN or another redesign stage creates
explicit children with changed-sequence hashes and its own validation records.
See the [comparison contract](../docs/binder-comparison-contract.md).

Keep predictor confidence and downstream scoring attached to their actual
producer. The native summary fields above do not supply a calibrated binding
score. Declare control-based assessment and retain failed or missing outputs.

## Runtime And Gates

The pinned README describes CUDA 11.7/PyTorch 1.13.1 and links a separate
`beta` environment for newer dependencies. Pin and qualify the chosen branch
independently; a changed branch needs its own input/output review. Inference
uses trained checkpoints without requiring the optional benchmark datasets.
[Setup and model assets](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/README.md#setup).

- Keep weights, generated sequences, structures, and runtime records outside git.
- Record dependency, GPU, seed, checkpoint, pocket, and relaxation identities.
- Check source and model-asset currency before dispatch; qualify a canary before scaling.
- Retain incomplete and rejected candidates; close unsupported operations explicitly.
- Keep result records at `computational_candidate` or lower.

## Primary Sources

- [Repository](https://github.com/THUNLP-MT/PepGLAD)
- [NeurIPS paper](https://openreview.net/forum?id=IAQNJUJe8q)
- [Pinned source, setup, and usage](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/README.md)
- [Pinned code license](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/LICENSE)

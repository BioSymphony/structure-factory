# RFdiffusion3

## Purpose

Plan atomic-level structure generation with RFdiffusion3 (RFD3) in RosettaCommons
Foundry. RFD3 has its own JSON/YAML input specification and inference settings.
Earlier RFdiffusion and RFdiffusionAA are separate scientific/software identities;
use their own documented interfaces for those arms.

## Public-Safe Status

Public scaffold: yes. Runtime execution and image inclusion require review of the
selected Foundry source, checkpoint, container, and dependency terms. A tool card
does not establish a served adapter. Keep checkpoints and generated structures
outside public git.

## When To Use

- Target-conditioned protein binder generation.
- Motif scaffolding and declared partial-diffusion or symmetry operations.
- Atomic conditioning for reviewed biomolecular interaction design inputs.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill with the RFdiffusion3 tool card. Prepare a Foundry RFD3 JSON/YAML InputSpecification for target <PDB:ID>, site <residues/atoms>, and declared design length. Record source/checkpoint, sample count, sequence handling, and independent prediction/geometry assessment.
```

## Typical Inputs

- Target PDB or CIF and explicit chain/residue/atom selection.
- JSON/YAML InputSpecification: `input`, `contig`, and the selected conditioning
  fields, validated against the chosen Foundry revision.
- For the documented protein-binder route, `select_hotspots` and
  `infer_ori_strategy="hotspots"`; retain the resolved atom selection.
- Checkpoint path, generation batch settings, seed, and sampler configuration.

## Typical Outputs

- A compressed CIF (`.cif.gz`) and JSON metadata file for each native design.
- Resolved specifications and chain/residue mappings; trajectories when requested.
- Sequence/pose identity for assessment. Inspect the actual emitted sequence:
  complete backbone-only outputs with a declared designer, preserve existing
  native pairs, and identify optional redesign children separately.

## Repo And References

Reviewed documentation pin:
`0932f1cb165ae7d413c11b1a7acc04ee31758817` (Foundry).
This source review does not change an existing campaign's source/checkpoint pin.

- [RFD3 input and CLI reference](https://github.com/RosettaCommons/foundry/blob/0932f1cb165ae7d413c11b1a7acc04ee31758817/models/rfd3/docs/input.md).
- [Protein-binder example](https://github.com/RosettaCommons/foundry/blob/0932f1cb165ae7d413c11b1a7acc04ee31758817/models/rfd3/docs/examples/protein_binder_design.md).
- [Invocation and output contract](https://github.com/RosettaCommons/foundry/blob/0932f1cb165ae7d413c11b1a7acc04ee31758817/models/rfd3/docs/intro_inference_calculations.md).

## Key Knobs

| Setting | Contract |
| --- | --- |
| `inputs`, `out_dir` | Native `rfd3 design` takes a JSON/YAML specification and output directory. |
| `ckpt_path` | Record the actual resolved checkpoint and hash. |
| `n_batches`, `diffusion_batch_size` | Define attempted designs per input key; verify completed output counts. |
| Input `contig` | Use RFD3's singular InputSpecification field and grammar. |
| Input `select_hotspots`, `infer_ori_strategy` | Validate target atom/residue selection and placement strategy. |
| `inference_sampler.num_timesteps`, `inference_sampler.step_scale`, `inference_sampler.gamma_0` | Record the selected sampler configuration; changes define sampling arms. |
| `dump_trajectories` | Optional large outputs, retained outside git. |

## Gotchas

- Older RFdiffusion flags such as `contigmap.contigs`, `ppi.hotspot_res`, and
  `inference.num_designs` are not this card's RFD3 interface.
- Generated geometry and native metadata do not prove binding. Retain sequence
  identity, independent refolding, exact-site geometry, and matched controls.
- Preserve raw CIF and mapping information when normalizing for a sequence
  designer; use its actual supported input representation.

## Gates

- Validate the selected source's input grammar and resolved conditioning.
- Require structures, metadata, hashes, and expected counts before completion.
- Record per-model confidence and metric definitions; calibrate the assessment
  policy rather than importing a universal iPTM/ipSAE threshold.
- Keep outcomes at `computational_candidate` or lower until independent
  validation supports a stronger boundary.

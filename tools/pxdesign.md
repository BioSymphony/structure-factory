# PXDesign

## Purpose

Use PXDesign for target-conditioned protein-binder backbone generation. The
upstream project also ships preview and extended pipelines that add sequence
design and confidence filters.

## Public Status

The upstream code uses Apache-2.0. Its setup downloads PXDesign and Protenix
checkpoints plus optional evaluation components. Review the terms for the exact
checkpoint set before packaging or redistribution. This checkpoint review does
not prevent a user from selecting a hosted route whose operator has already
resolved those terms.

## Run Shapes

- Validate configuration: `pxdesign check-input --yaml <target.yaml>`.
- Render the parsed target and hotspot mapping: `pxdesign parse-target --yaml
  <target.yaml> -o <output>`.
- Generate backbones: `pxdesign infer -i <target.yaml> -o <output> --N_sample
  <count>`.
- Run the upstream preview or extended pipeline when the comparison arm calls
  for its integrated filters.

For a published-cohort arm in this repository, treat `pxdesign infer` output as
backbone generation. Apply a declared sequence designer, then run the common
independent score stack. Preserve raw mmCIF output and any residue-number
mapping instead of inventing missing atoms or sequences.

Record generation-only, preview, or extended mode as part of the arm identity.
The [pinned upstream guide](https://github.com/bytedance/PXDesign/blob/f788441313c84c3074fe9596ac2433f96b15c763/README.md#2-running-pxdesign)
describes Extended mode with AF2 and Protenix evaluation and target-chain MSAs.
For an external sequence-design and common-screen arm, list those executed
stages and retain the upstream evaluation stages as omitted. Preserve native
filter results separately from the common screen.

Use the [binder comparison contract](../docs/binder-comparison-contract.md) for
stage coverage, sequence lineage, and assessment quotas.

## Inputs And Outputs

Record target structure hash, chain selection, crop, hotspots, binder length,
PXDesign and Protenix revisions, checkpoint hashes, seed, generation mode, and
sample count. Count generated backbones and parse at least one before scaling.

## References

- Upstream repository: https://github.com/bytedance/PXDesign
- Sequence-design handoff: [ProteinMPNN](proteinmpnn.md)
- Common screen: [Cofold scoring stack](cofold-scoring-stack.md)

# AtlasFold-M

Reviewed 2026-09-22. AtlasFold-M predicts protein complexes from one sequence
per chain, without an MSA search. The [September 2026 preprint](https://www.biorxiv.org/content/10.64898/2026.09.04.749352v2)
introduces the Atlas model family.

## Source and runtime

The [source revision](https://github.com/SeonghwanSeo/atlasfold/tree/8ab3aca0e18c8b814d5ca6756b2617a07d72c68d)
and [multimer model card](https://huggingface.co/SeonghwanSeo/atlasfold-m-260725)
state MIT terms for code and weights. Review dependency notices separately.
The model needs AtlasFold-M and AtlasLM-3B weights in an external cache.
The repository CLI and model-card CLI examples differ; bind the selected source
revision's interface. Template-assisted multimer inference is unsupported in
the reviewed runner.

The repository reports 16.05 GiB peak memory for 1,024 total residues and five
samples on a B200. Measure the selected hardware and batch size before setting
resource limits. Structure Factory records this tool for adapter evaluation.

## Evaluation record

Retain source and checkpoint hashes, chain mapping, input hashes, sample count,
backend, structures, and emitted confidence fields. The model card exposes ipTM;
verify PAE availability and matrix indexing before connecting an interface scorer.
Compare reference geometry and confidence with a fixed public complex panel.
Record failures and elapsed time alongside successful outputs.

The compact result is a prediction manifest and per-complex comparison table.
Store weights and generated coordinates in runtime storage.

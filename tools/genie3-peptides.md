# Genie 3 Peptides And Miniproteins

## Purpose

Plan peptide or miniprotein backbone generation lanes while respecting the model's length and setup assumptions. Genie 3 is a diffusion-based protein structure generator; the binder-design mode produces backbones conditioned on a target structure, hotspot residues, and a binder length range. Sequences come from a downstream ProteinMPNN pass; structural confidence comes from an independent cofold.

## Public-Safe Status

Public scaffold: yes. Runtime execution requires source, weight, dependency, MSA-service, and intended-use review. Store weights and generated structures under ignored runtime storage or in a user-selected artifact store.

## When To Use

- Miniprotein binder backbones (~50-150 aa) against a public or operator-approved target window.
- As an alternative to RFdiffusion when its specific training distribution or ColabFold-based evaluation step is preferred.
- When the binderbench-style binder design layout (problems / targets / MSA pre-computed) fits the workflow.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill with the Genie3 tool card. For target <PDB:ID> with target-window report <path>, prepare a peptide or miniprotein generation lane. Respect the length floor near 50 aa, specify hotspot and extended interface residue sets, the binder length range, the ProteinMPNN sequence pass, and the Boltz + Chai cofold handoff.
```

## Practical Boundary

Treat very short peptides (under ~30 aa) as out-of-distribution until a campaign records evidence otherwise. Miniprotein-length binder scaffolds (50-150 aa) are the safer planning lane. For shorter peptides, switch to RFpeptides, HelixDiff, or PepGLAD.

## Typical Inputs

- Public target structure or target-window file.
- Hotspot and extended interface residue sets on the target.
- Binder length range (`50-100` typical for miniproteins).
- Runtime config generated from a manifest (problem JSON + target dataset).
- Pre-computed target MSA (Genie 3 expects ColabFold-format MSA at evaluation time).
- Sample count per problem.

## Typical Outputs

- Generated backbone candidates (PDB) outside git, under `<rootdir>/<selection>/pdbs/<selection>_<sample_idx>.pdb`.
- Generation manifest with seeds, config, source refs, weight refs, and execution time.
- Downstream ProteinMPNN sequence-design input.
- Cofold ranking input manifest.

## Repo And References

- Genie3: https://github.com/aqlaboratory/genie3
- [Pinned binder example](https://github.com/aqlaboratory/genie3/blob/d77ae5ac04212ff1e8b29b585859a3244c614804/examples/binder_design/experiment.yaml)
- Earlier generations: https://github.com/aqlaboratory/genie and https://github.com/aqlaboratory/genie2

## Key Knobs

| Setting | Recommendation | Why |
| --- | --- | --- |
| Binder length range | 50-100 aa | Below ~50 aa is out-of-distribution; above ~150 aa, sample count needs to grow. |
| `n_sample` per problem | 4-32 first pass | Canary at 4; scale to 32 once the lane proves end-to-end. |
| `direction_scale` | Explicitly set the value from the selected source pin; the pinned binder example uses `0.0` | Treat a changed value as a separate sampling arm and retain its configuration. |
| Hotspot residues | 3-8 on target | Anchors the binder placement. |
| Extended interface residues | 5-20 on target | Defines the surface region the binder can engage. |
| Downstream ProteinMPNN | SolubleMPNN for soluble targets | Sequence pass on the binder using target as context. |
| Cofold validator | Boltz + Chai-1 slate | iPTM + ipSAE consensus; single-cofolder iPTM is unreliable for binder ranking. |

## Gotchas

- Explicitly set `generation.dataset.cond_strategy` and validate the selected interface list. At the source pin above, the target dataset defaults to `extended`; the feature builder selects only that named list. Populating `hotspot` does not populate `extended`. For a site-conditioned arm, reject an empty selected list and verify its resolved residue mask before scaling. See the [dataset defaults](https://github.com/aqlaboratory/genie3/blob/d77ae5ac04212ff1e8b29b585859a3244c614804/src/genie3/generation/config/data/sample_dataset.py) and [feature builder](https://github.com/aqlaboratory/genie3/blob/d77ae5ac04212ff1e8b29b585859a3244c614804/src/genie3/generation/utils/feat_utils.py).
- At this pin, the native seed key is `experiment.seed`. Record the resolved native configuration and seed-delivery evidence before calling an arm seeded. Recheck the key when changing source revisions.
- Genie 3 reads `target_pdb_filepath` from the problem JSON via Python `open()`, which resolves relative paths from cwd. Synthesize the problem JSON with absolute paths or run from the configured weights directory.
- `genie3 run` does generate-then-evaluate; the evaluate step needs ProteinMPNN (separate package, not pip-resolvable from upstream setup.py). Use `genie3 generate` instead and run ProteinMPNN as a separate stage. The Boltz cofold acts as the independent validator.
- `genie3 generate` writes outputs to `<rootdir>/<selection>/pdbs/<selection>_<sample_idx>.pdb`, not the README-documented `results/v0_success/successful_complexes/`. Search the entire `<rootdir>/<cid>/` subtree.
- The binderbench dataset layout requires `problems/<sel>.json` plus `targets/{pdb,fasta,msa}/<sel>{,-chain_X}.{pdb,fasta,a3m}`. The README's per-problem JSON shape is correct; the surrounding layout is non-obvious.
- Boltz cofold downstream needs `numpy < 2.2` due to its numba dependency, but Genie 3's `pip install -e .` upgrades numpy past 2.1. Re-pin numpy inside the Boltz stage itself, not just at startup.
- HuggingFace weights revision pinning is required for reproducibility; record the revision in the candidate ranking alongside the seed.

Use the [binder comparison contract](../docs/binder-comparison-contract.md) to
record parent backbones, sequence children, native stages, and common screening.

## Gates

- Weight download requires operator authorization.
- Public MSA service calls are allowed for public targets only.
- Candidate claims require cofold, artifact, provenance, and validation-ledger checks before promotion.
- Cap every candidate ranking at `computational_candidate` until independent validation exists.
- Run a currency check before any paid GPU dispatch: upstream repo HEAD (releases + recent commits), current release notes, and recent preprints (biorxiv / chemrxiv / arxiv) on the relevant lane. Record the version pin (Genie version + HuggingFace weights revision) and the date of the check in the candidate ranking or validation notes.

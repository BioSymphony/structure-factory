# Tool And Skill Radar

Snapshot date: 2026-05-15

This is a planning snapshot, not legal advice and not a current license determination. Before installing, baking into an image, running, or redistributing any third-party tool, recheck the primary source terms and record the user's intended use context.

## Ready In The Public Harness

- Public campaign contracts, stage contracts, provider profiles, task packs, validators, and audit gates.
- Local no-download examples for PD-L1 binder-design planning and screening fixture runs.
- Public non-launchable RunPod bridge templates that document required fields without embedding private payloads or real approvals.
- Portable agent instructions and Symphony and tracker-neutral task packs for `sym:structure-factory`.

## Open Or Default Scaffolding

These are suitable for public mention and scaffolded planning after normal citation and current-term checks:

- Boltz-style cofolding and confidence extraction.
- ProteinMPNN or LigandMPNN-style sequence design lanes.
- RDKit, AutoDock Vina, OpenMM, GROMACS, gemmi, Mol*, Blender, and open-source PyMOL builds.
- ModelAngelo-style model building where weights and downloads are handled through reviewed runtime caches.

## Review Required

These can be useful, but public image inclusion or execution should wait for exact build and dependency review:

- RFdiffusion-family and RFdiffusion3-family design lanes, including code, weights, and Docker image posture.
- Genie 3 and peptide/miniprotein use, especially weights, ColabFold or AlphaFold2 dependencies, MSA service posture, and evaluation helpers.
- Chai, LocalColabFold, ABCFold, ipSAE wrappers, and cofold consensus stacks.
- SwitchCraft multistate/switch design, including its vendored cofolder and sequence-model weights and pinned dependencies; route designs through the cofold scoring stack for an orthogonal check.
- DOMINO multidomain construct assembly, downstream of a validated binder; upstream license is unresolved (no LICENSE, empty model card, no-reuse preprint), so treat reuse and image inclusion as blocked until terms are published.
- Baker miniprotein-GPCR recipe (motif-directed RFdiffusion + ProteinMPNN + AF2 over public deposited targets), inheriting the upstream tools' posture.
- CTFFIND, cisTEM, GNINA, cryoDRGN, EMAN2, Scipion/Xmipp, DeepEMhancer, CUDA/NVIDIA bases, and large public weight/database bundles.

## Runtime Gated

Public docs may describe these lanes, but committed public artifacts must not include installers, binaries, license files, credentials, or accepted-license state:

- CryoSPARC, Phenix, ChimeraX, ISOLDE, Rosetta/PyRosetta, AlphaFold 3 parameters, commercial PyMOL binaries, and similar terms-controlled tools.
- Any tool requiring private registry credentials, signed URLs, private installer links, or account-specific access.

## Omitted Or Private

Keep these out of public git:

- Private run notes, local checkpoints, provider cost ledgers, concrete pod IDs, concrete volume IDs, and operator incident reports.
- Generated PDB/CIF/MMCIF/MRC/MAP/TRB/PML/MP4/GIF/NPZ/model-weight artifacts.
- Private demos that have not been rewritten as narrative-only public summaries.

## Export Priorities

1. Keep Makefile targets aligned with documented commands.
2. Publish concise tool cards under `tools/` with posture, inputs, outputs, and gates.
3. Prefer narrative demos and compact public tables over result dumps.
4. Keep launch manifests as templates until a current operator gate converts them into private execution packets.

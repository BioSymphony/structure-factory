# Tooling And Licensing

Last reviewed: 2026-05-08

This is the public, human-readable tool posture for BioSymphony Structure Factory. It complements the machine-readable registry at `references/software-registry.yaml`.

This is engineering guidance, not legal advice. Mentioning a tool in public docs is allowed; installing it, baking it into an image, running it for a user, or redistributing it requires checking the current primary license/source terms and the user's use case.

For result-boundary vocabulary that tool outputs may support, see [`result-boundaries.md`](result-boundaries.md).

## Agent Rule

Before selecting a tool lane, agents must record:

- current primary source checked
- intended use: personal, academic/non-profit, non-commercial, commercial, or institutional
- action: mention, scaffold, install at runtime, bake into public image, bake into private image, or run
- setup posture: public/prebuilt image, private image, runtime bootstrap, RunPod Network Volume bootstrap, AWS Batch image, local install, SSH/HPC module, or neocloud/generic cloud volume
- redistribution posture: none, source build, binary layer, model weights, database, installer, or license file
- required user/operator action, if any

If this cannot be established, the lane is `review_required` or `runtime_gated`, not open.

## Public Vs Private Split

Public docs and repos may mention all relevant tools, including gated tools, as long as they do not include secrets, license files, private installer URLs, proprietary binaries, private data, large public data, or model weights.

Public images are stricter because image layers redistribute software. Only reviewed redistributable tools belong in public images.

Private/internal notes belong under `internal/private/`, which is gitignored. Use that area for local RunPod assumptions, accepted-license notes, private image names, local install paths, and one-off testing decisions. Do not put secrets there either; reference secure stores or environment variable names only.

GHCR/private images are not the default assumption. They are one setup posture. For personal/non-commercial RunPod tests, a public base image plus Structure Factory Network Volume bootstrap can be cleaner because it avoids registry auth and avoids public redistribution of tools that should be installed by the operator.

## Posture Classes

| Class | Public docs | Public image | Private/runtime use |
| --- | --- | --- | --- |
| Open-default | Mention and scaffold | Usually OK with notices, citations, SBOM, and source-compliance | OK |
| Review-required | Mention and scaffold with caveats | Only after exact current license/build review | OK after review |
| Runtime-gated | Mention and scaffold gates only | Do not include | User/licensee runtime install or manual activation only |
| Internal-only | Do not publish private details | Do not include | Local ignored notes only |

## Open-Default Candidates

These are the default candidates for ambitious no-license-application demos, subject to preserving notices, citations, and source-compliance obligations:

- Structure Factory scripts, schemas, RunPod entrypoints, manifests, and public accession metadata.
- RELION.
- Warp/M/WarpTools.
- Topaz.
- MotionCor3 from the CZI source repository.
- ModelAngelo code. Keep large weights as runtime caches unless redistribution terms are explicitly recorded.
- Coot open-source builds.
- PyMOL open-source builds with no paid Schrodinger assets.
- gemmi.
- Mol*.
- Blender.
- Boltz/Boltz-2.
- Chai-1, after pinning and checking the current repository terms.
- OpenMM.
- GROMACS.
- AutoDock Vina.
- RDKit.
- ProteinMPNN.
- LigandMPNN.

For a public image, GPL/LGPL tools require normal compliance work: license texts, source/build recipes, citation metadata, and ideally SBOM/source-offer notes.

## Review-Required Candidates

These can be useful and can be mentioned publicly, but agents should not treat them as no-license-needed image contents until the exact current package, binary source, dependency stack, and redistribution terms are checked:

- CTFFIND.
- cisTEM.
- cryoDRGN and related GPL-heavy heterogeneity stacks.
- EMAN2.
- Scipion/Xmipp and plugin stacks.
- GNINA, because license posture depends on exact build/dependencies.
- DeepEMhancer, especially model-weight redistribution.
- CUDA/NVIDIA base images and drivers under current NVIDIA container terms.
- Large public weights, maps, databases, or reference bundles even when redistribution is technically permitted.
- RFdiffusion and related design-model weights unless the current code and weight terms are reviewed for the intended use.
- Genie 3 and related setup/evaluation dependencies until the repo, Hugging Face weights, ColabFold/AlphaFold2 parameters, ProteinMPNN, IPSAE, FoldSeek, TMscore/TMalign, DSSP helper, CUDA/JAX, and any MSA-server use are recorded for the intended use. Structure Factory bootstrap requires an explicit `GENIE3_ALLOW_COLABFOLD_PARAMS=1` acknowledgement before upstream setup can download AlphaFold2 multimer parameters.

Review-required does not mean forbidden. It means do not bake, run, or close as open until the current terms are recorded.

## Runtime-Gated Or Use-Context-Gated Tools

These may be documented and scaffolded publicly, but should stay out of public images and out of "no-license-needed" demos unless the user/operator has accepted the relevant terms and supplied runtime access through secure configuration:

- CryoSPARC.
- Phenix.
- ChimeraX and ISOLDE.
- MotionCor2 UCSF binary.
- crYOLO.
- Gctf unless a redistributable current license is confirmed.
- RECOVAR, due to academic/non-commercial use-context terms.
- Rosetta/PyRosetta.
- AlphaFold 3 model parameters and related restricted weights/databases.
- Schrodinger/Incentive PyMOL binaries and license files.

For these, public docs should say what the lane would do and what evidence it would emit, but the lane must report `skipped`, `blocked`, or `ready` based on runtime checks.

## Demo Planning Defaults

For no-license-application Structure Factory demos, prefer:

- CryoCore handoff docs for raw/subset requests: RELION, Topaz, CTFFIND only after review, MotionCor3 after current source/build check
- deposited PDB/EMDB structure-mapping reports: ModelAngelo, gemmi, Mol*, Blender, Coot open-source, PyMOL open-source
- heterogeneity: cryoDRGN after GPL/source-compliance review; RECOVAR only as runtime/use-context gated
- MD/docking side lanes: OpenMM, GROMACS, AutoDock Vina, RDKit
- AI/model-comparison side lanes: Boltz, Chai after current terms check, ProteinMPNN, LigandMPNN, Genie 3 after current dependency/weights review

ChimeraX can remain a strong visual lane for our internal/private demos when the operator's use context permits it, but it is not part of the public no-license-needed stack.

## Required Artifact Notes

Any run using these tools should emit:

- `versions.json` or tool-specific version files
- command ledger with exact commands and exits
- citation notes
- license/use-context notes
- artifact hashes
- validation notes separating `planning`, `public_demo`, `public_synthetic_demo`, `computational_candidate`, `insufficient_support`, and `blocked`

Outputs from open-source tools are usually usable as run artifacts, but still need provenance, version, citation, and result boundaries. Outputs from runtime-gated tools need use-context caveats.

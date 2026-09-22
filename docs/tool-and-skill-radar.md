# Tool and skill radar

Reviewed 2026-09-22. These source reviews identify useful additions and changed
releases. Dates in the table refer to papers or releases; they do not establish
installation or measured performance. The software registry (`references/software-registry.yaml`) records tool
posture, and the tool index (`tools/README.md`) describes existing contracts.

## Prediction and design

| Tool and dated evidence | Useful addition | Required record or unresolved question |
| --- | --- | --- |
| [AtlasFold-M](https://github.com/SeonghwanSeo/atlasfold/blob/8ab3aca0e18c8b814d5ca6756b2617a07d72c68d/README.md), [September 2026 preprint](https://www.biorxiv.org/content/10.64898/2026.09.04.749352v2) | MSA-free protein-complex prediction | Model/AtlasLM hashes, chain mapping, emitted confidence fields, and reference comparison. Code and weights state MIT terms. |
| [DeCAF-Boltz](https://github.com/genesistherapeutics/decaf/blob/471477e0e786f91bae77d4cebf4b7d14901bc174/README.md), [June 2026 preprint](https://arxiv.org/abs/2606.08375) | Released few-step cofolding code and weights | Structure-only and confidence-enabled checkpoints differ. Compare geometry, confidence, and timing at matched budgets. |
| [Odin-Multi](https://github.com/DigBioLab/odin_multi), [September 2026 preprint](https://www.biorxiv.org/content/10.64898/2026.09.08.749745v1) | Shared-sequence design across multiple contexts | Per-context results and input hashes; MIT source with separate AF2/ColabDesign and optional AF3 terms. Source review only. |
| [ODesign](https://github.com/OTeam-AI4S/ODesign), [October 2025 report](https://arxiv.org/abs/2510.22304) | All-atom generative modeling across molecular types | Exact checkpoint/component terms, input schema, output counts, and independent scoring. Upstream states Apache-2.0 for code and parameters. |
| [Protenix-v2](https://github.com/bytedance/Protenix/blob/85767b811c40ed46e73a9b39519cf6bfca8701ba/README.md), April 2026 release | Existing cofolding identity with a changed terms record | The reviewed README contains conflicting v2-specific and blanket weight notices. Resolve exact checkpoint terms before use; registry gate applies. |
| [OpenFold3 v0.5.0 / OpenBind-0](https://github.com/aqlaboratory/openfold-3/releases/tag/v0.5.0), August 2026 release | Existing all-atom predictor | Preserve source, parameter filename/hash, and model identity. Distinguish the parameter set from the separate OpenBind benchmark dataset. |

## Evaluation and deposited evidence

| Tool and dated evidence | Useful addition | Required record or unresolved question |
| --- | --- | --- |
| [PSBench](https://github.com/BioinfoMachineLearning/PSBench), [May 2025 paper](https://arxiv.org/abs/2505.22674) | Protein-complex model-accuracy calibration with CASP splits | Split identifiers, reference metrics, and calibration table. MIT code; review dataset terms separately. Keep the model corpus external. |
| [PoseBench v1.1.0](https://pypi.org/project/posebench/1.1.0/), March 2026 package | Protein-ligand benchmark with corrected scoring | [Upstream](https://github.com/BioinfoMachineLearning/PoseBench) reports a v1.0.0 ligand-scoring bug. Rerun affected comparisons with a pinned corrected version. |
| [ProLIF v2.2.2](https://github.com/chemosim-lab/ProLIF/releases/tag/v2.2.2), September 20, 2026 UTC release | Interaction fingerprints alongside pose geometry | Reference-pose provenance, atom mapping, and interaction recovery table. Apache-2.0 code; recovery requires a reference. |
| [RCSB validation API](https://cdn.rcsb.org/rcsb-pdb/general_information/news_publications/newsletters/2025q3/query.html), 2025 Q3 update | Deposited experimental-fit and geometry summaries | Accession, report version, retrieval time, source URL, and available validation fields. Map reconstruction remains a CryoCore task. |

Confidence, reference similarity, and interaction recovery measure different
properties. Select ranking thresholds against the campaign's controls and
report per-model scores and missing outputs.

## Agent retrieval and workflow tools

| Tool and dated evidence | Useful addition | Required record or unresolved question |
| --- | --- | --- |
| [RCSB MCP](https://github.com/rcsb/rcsb-mcp), [v0.15.0 August 2026](https://pypi.org/project/rcsb-mcp/0.15.0/) | Structure, entity, assembly, and sequence-coordinate retrieval | Query/version, normalized accessions, source URLs, retrieval time, and incomplete responses. MIT code; integrated data retain source terms. |
| [PDBe MCP](https://github.com/PDBeurope/PDBe-MCP-Servers), [v1.1.6 July 2026](https://pypi.org/project/pdbe-mcp-server/) | PDBe REST and Solr searches | Record API version and fields. Graph tools require a separately available Neo4j database. Apache-2.0 code. |
| [Noodle](https://github.com/helena-bioinformatics/noodle-mcp), [v0.2.0 August 2026](https://zenodo.org/records/22166486) | Biomedical paper retrieval and bounded citation graphs | DOI/PMID, primary-paper links, corpus date, and response hash. Apache-2.0 code; [hosted privacy terms](https://noodle.helena.bio/privacy) govern queries. |
| [EMICSS](https://www.ebi.ac.uk/emdb/emicss), [September 2025 paper](https://academic.oup.com/bioinformaticsadvances/article/5/1/vbaf203/8248485) | EMDB cross-references for metadata handoffs | Entry and collection dates, linked accessions, annotation conflicts, and source terms. Retain compact records rather than maps. |
| [Prosculpt](https://github.com/ajasja/prosculpt), [June 2026 preprint](https://www.biorxiv.org/content/10.64898/2026.06.25.732351v1) | YAML orchestration of existing design and prediction tools | Component versions, stage outputs, and restart state. BSD-3-Clause wrapper; components keep their terms. |
| [ProteinDJ v3](https://github.com/PapenfussLab/proteindj), [January 2026 publication](https://doi.org/10.1002/pro.70464) | Nextflow/Apptainer design workflow | Preserve major version, container identities, model-cache terms, and output mapping. Upstream labels its license MIT (Modified). |
| [RO-Crate 1.3](https://github.com/ResearchObject/ro-crate/releases), June 2026 recommendation | Versioned provenance envelope | Pin the [Workflow Run profile](https://www.researchobject.org/workflow-run-crate/), context, validator, and artifact hashes. Review payload licenses separately. |

## Ensembles and model inputs

| Tool and dated evidence | Useful addition | Required record or unresolved question |
| --- | --- | --- |
| [ConfRover](https://github.com/ByteDance-Seed/ConfRover), November 2025 release | Single-chain temporal sampling and state interpolation | Checkpoint identity, input-frame hashes, frame count/stride, and trajectory summary. Upstream states Apache-2.0 for code and weights. |
| [PAR](https://github.com/bytedance-Seed/par-protein), [February 2026 preprint, revised May](https://arxiv.org/abs/2602.04883) | Multiscale backbone completion and scaffolding | Prompt masks, checkpoint identity, preservation checks, and independent structural assessment. [Model card](https://huggingface.co/ByteDance-Seed/PAR) states Apache-2.0. |
| [DynamicsPLM](https://github.com/kalifadan/DynamicsPLM), [May 2026 paper](https://doi.org/10.1093/bioinformatics/btag254) | Representations derived from conformational ensembles | Ensemble and asset hashes, base-model terms, and representation manifest. MIT code; the separate [Zenodo artifact](https://doi.org/10.5281/zenodo.17668302) is CC-BY-4.0. |
| [Biotite 1.6.0](https://github.com/biotite-dev/biotite/releases/tag/v1.6.0), January 2026 release | Structure/sequence arrays, A3M handling, and assembly parsing | Parser version, normalized field counts, accession provenance, and parse manifest. BSD-3-Clause code. |
| [AtomWorks 2.2.0](https://github.com/RosettaCommons/atomworks/releases/tag/v2.2.0), December 2025 release | AI input loaders and composable molecular transforms | Source revision, transform settings, tensor shapes, and input hashes. BSD-3-Clause code; external executables, weights, and datasets keep separate terms. |
| [Foldseek](https://github.com/steineggerlab/foldseek) and [FoldMason](https://github.com/steineggerlab/foldmason), 2025 tagged releases | Structure search and multiple-structure alignment | Source tag, database/split identity, accession ledger, and bounded TSV/alignment report. GPL-3.0 code; search and alignment remain separate operations. |

## Further source review

[ORI](https://github.com/TencentAI4S/ori) needs reconciliation of its repository
license label with the [paper's code terms](https://www.nature.com/articles/s41467-026-69855-6)
and separate code/weight deposits. [MoE-Bind](https://github.com/dipayanskr/MoE-Bind)
and [SeedProteo](https://github.com/SeedProteo/SeedProteo.github.io) remain research
leads until reproducible pretrained releases and terms are established.
[Paper2Agent](https://github.com/jmiao24/Paper2Agent) is relevant when a specific
method needs an MCP wrapper; a general conversion framework adds little to an
already documented adapter.

Keep source URLs, versions, compact manifests, and comparison tables in Git.
Keep model weights, benchmark corpora, generated structures, and service records
in runtime storage. A source review adds no installed dependency or execution result.

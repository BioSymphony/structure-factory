# Binder Filtering

Use interface diagnostics, pKa estimates, and developability annotations to
review a frozen candidate pool. Select each method for its measured endpoint
and accepted protein format. Keep the original predictor outputs and candidate
identities attached to every score.

Sources reviewed 2026-10-01. These are tool-selection records; execution needs
a qualified adapter, model assets where applicable, and campaign controls.

## Interface Diagnostics

| Method | Inputs And Outputs | Interpretation |
| --- | --- | --- |
| [Pinc](https://git.mpi-cbg.de/tothpetroczylab/Pinc/-/blob/d9e966b258fad610bb04a53b2d842651f13400bb/README.md) | Structure and matching PAE; directional and symmetric contact-support scores, optional contact probabilities | Upstream documents AlphaFold outputs. Qualify residue/token correspondence and score calibration before applying it to another predictor. |
| [AFM-LIS](https://github.com/flyark/AFM-LIS/blob/29144b9d4880a0a0c418386da0c24e9520861dad/README.md) | Structure and matching PAE; LIS, contact-filtered cLIS, and integrated iLIS | iLIS combines local confidence with physical contacts. Parser support for a predictor does not establish a transferable rejection threshold. |
| [MViewEMA](https://github.com/iobio-zjut/MViewEMA/blob/1f9b9df3f0d9d85d3f70d2102072fc0fdf8d4f11/README.md) | Structure-derived features and checkpoint; estimated global TM-score | Global model quality and interface reliability are separate endpoints. Fresh feature generation requires PyRosetta access. |

Pinc, iLIS, and [ipSAE](cofold-scoring-stack.md) reuse predictor PAE. Treat
their agreement as correlated evidence. Retain complete directional matrices,
chain order, residue/token maps, contact definitions, and per-predictor scores.

Pinc's reviewed C source and AFM-LIS use MIT licenses. MViewEMA's MIT code
does not supply permission for its separately governed dependencies.

## pH And Protonation

| Method | Computational Question | Required Record |
| --- | --- | --- |
| [PROPKA](https://github.com/jensengroup/propka), [PDB2PQR](https://pdb2pqr.readthedocs.io/en/latest/), and [APBS](https://apbs.readthedocs.io/en/latest/) | How do predicted protonation and electrostatic descriptors change with pH? | Bound/free state definition, chain mapping, added atoms, charge/radius set, dielectric settings, ionic strength, grids, and pH points |
| [MEpKa](https://github.com/yzjyg215/ME-pKa/blob/0213e85fa543818a019aa32819d70d0580199659/README.md) | How do local structure and sequence features affect residue pKa estimates? | Feature-generation versions, residue identities, encoder/checkpoint hashes, and exact batching |
| [KaML-ESM](https://github.com/JanaShenLab/KaML-ESM/blob/19bd1902819b0a124d8cb58bdc60f59605b912b3/README.md) | What residue pKa estimates follow from sequence embeddings? | Exact sequence model and pKa ensemble; structure-based CBTree results remain a separate method |
| [GROMACS/FMM constant-pH MD](https://www.mpinat.mpg.de/grubmueller/gromacs-fmm-constantph) | How do protonation and conformation change together during sampling? | Exact fork/build, force field, titratable sites, seeds, replicas, equilibration, and convergence |

Identical sequences give a sequence-only method no bound/free structural
distinction. Electrostatic descriptors, residue pKa, and total binding affinity
remain separate quantities. Define the direction of each pH contrast before
ranking candidates.

MEpKa code is MIT; its documented preprocessing also uses CHARMM and Chimera.
KaML-ESM declares CC BY-NC 4.0. Review dependencies, model assets, and the
selected constant-pH fork before execution. PypKa also needs a separate review
of its required DelPhi electrostatics engine. That engine and the DELPHI
antibody model are different tools.

## Developability And Protein Format

| Method | Accepted Context | Output And Limit |
| --- | --- | --- |
| [Pro4S](https://github.com/TEKHOO/Pro4S/blob/fcf210d796e4b2be308686eb913b51133e15cd00/README.md) | Isolated protein chain with sequence, structure, and surface features | Solubility/expression annotation. Upstream writes label zero when a measurement is absent; retain that absence explicitly. |
| [DeepSolNet](https://github.com/wangxinglong1990/DeepSolNet/blob/4ee09eea25b755a1135fc713dfba8a17c81191b8/README.md) | Sequence with the selected ESM encoder and trained prediction head | Solubility classification. The encoder checkpoint alone cannot produce the released predictor's endpoint. |
| [DELPHI](https://github.com/proteininnovation/delphi/blob/c3d20122c86ad4c3f8142a4ae571bcf5b9912ded/README.md) | Paired VH/VL antibody sequences | Separate polyreactivity and size-exclusion-chromatography models; preserve the selected assay head and checkpoint. |
| [CrossAbSense](https://github.com/SimonCrouzet/CrossAbSense/blob/ccc23ebcb0c53e2f4a843d1e520736e91fd04dbf/README.md) | Paired antibodies; several heads require full heavy/light chains and subtype context | Assay-specific regression. Record constant-region reconstruction and numbering failures. |
| [Therapeutic Nanobody Profiler](https://github.com/oxpig/TNP/blob/29dcac72f1380e8538e8870f45a699d3c6156162/README.md) | VHH structures | Loop and surface-patch descriptors with format-specific reference ranges |
| [Aiki-GeNano](https://github.com/aikium-public/aiki-genano/blob/ea3cdfaec88492ce2b3cd5ed4928a548ca955a13/README.md) | Fixed-scaffold VHH workflow | Separate liability/reward descriptors; preserve scaffold and numbering assumptions |

Use paired-antibody and VHH models only for compatible formats. Expression,
solubility, aggregation, polyreactivity, and binding are distinct endpoints.
Keep exposed hydrophobic patches and sequence liabilities in separate columns.

Pro4S's [model card](https://huggingface.co/qj666/Pro4S) declares CC BY-NC 4.0;
its code/data terms need review. DeepSolNet's README declares MIT but the
reviewed root lacks a license file. DELPHI code is MIT and its
[released PSR/SEC model deposit](https://zenodo.org/records/21823887) declares
MIT. CrossAbSense uses Apache-2.0, TNP uses BSD-3-Clause, and Aiki-GeNano code
uses MIT. Record exact checkpoint and dependency terms for the selected route.

## Filter Qualification

Use [ProtDBench](https://github.com/congliuUvA/ProtDBench),
[FoldBench](https://github.com/BEAM-Labs/FoldBench), and
[PXMeter](https://github.com/bytedance/PXMeter) for the applicable evaluation
task. ProtDBench composes design verifiers; FoldBench provides native-reference
prediction challenges; PXMeter evaluates against reference structures.
Reference-based accuracy requires a matching reference complex.

For assay qualification, select endpoint-matched public panels such as
[Bits to Binders](https://github.com/kosonocky/bits-to-binders),
[AbDev](https://github.com/ginkgobioworks/abdev-benchmark), or
[FLAb](https://github.com/Graylab/FLAb). Retain assay conditions, protein format,
split membership, and missing measurements. Separate measured negatives from
missing labels and reconstruction failures.

Follow the [filter qualification contract](../docs/binder-filter-qualification.md)
before promoting an annotation to a rejection rule. Registry records describe
source review; installed adapters and measured qualification need their own
evidence.

# Protein-Ligand Affinity Scoring

Select a protein-ligand scorer by its required inputs, training endpoint, and
score direction. Retain pose validity and affinity predictions as separate
results. This lane complements [PoseBusters](posebusters.md) and the
[refinement stack](refinement-stack.md).

Sources reviewed 2026-10-01. The registry records source and license posture;
execution requires a qualified adapter and endpoint-matched controls.

## Methods And Inputs

| Method | Inputs | Outputs And Direction |
| --- | --- | --- |
| [AEV-PLIG](https://github.com/isakvals/AEV-PLIG/blob/98a28c515be6df63a7a7bc7c3a84ea0de5904599/README.md) | Prepared protein-ligand 3D complex and pretrained ensemble | Structure-conditioned affinity prediction; record checkpoint, output scale, and ensemble members |
| [Nesso-1](https://github.com/recursionpharma/nesso/blob/6c72f66720d9d3447fd73c515cda963e39128b1f/docs/prediction.md) | Protein sequence and ligand SMILES, CCD identifier, or SDF | `affinity_pred_value` is log10(IC50 / micromolar); lower means stronger predicted affinity. Binary binder probability is a separate output. |
| [FLOWR.root v2.2](https://github.com/jule-c/flowr_root/blob/739a33c2aab74d074dd24605b9a2e34dc809ae9c/README.md) | Prepared protein-ligand structures and the joint affinity checkpoint | Separate predicted pIC50, pKi, pKd, and pEC50 values; affinity scoring and ligand generation are different operations |
| [Vinardo through smina](https://github.com/mwojcikowski/smina) | Prepared receptor and ligand coordinates with declared atom typing and hydrogen/charge preparation | Empirical pose score. Record score-only, minimization, or docking mode. |

Nesso infers a coarse-grained complex from sequence and ligand inputs. Its
affinity prediction cannot validate the placement of a supplied receptor-ligand
pose. AEV-PLIG and FLOWR.root use structural inputs, so preserve coordinate,
atom-mapping, and preparation hashes.

## Matched Comparison

Freeze the target construct, ligand identity, protonation, tautomer,
stereochemistry, cofactors, and preparation protocol. Record source accessions
and measured endpoint units. Preserve missing predictions and parser failures.

Compare scores against matching endpoint labels within each target. IC50, Ki,
Kd, EC50, empirical docking scores, and binding free energy need their own
interpretations. A within-target rank comparison does not calibrate absolute
affinity across endpoints or targets.

Audit training overlap and use an appropriate held-out split before reporting
predictive performance. For structure-conditioned scores, include pose
perturbations and geometry checks. Keep predictor uncertainty, pose validity,
and assay measurements in separate columns.

## Runtime And License

AEV-PLIG source uses BSD-3-Clause. Nesso code and its
[model card](https://huggingface.co/recursionpharma/nesso) declare Apache-2.0.
FLOWR.root source uses MIT, with separate terms for the `flowr_vis/` application
and optional dependencies. Review the selected checkpoint and component assets
before image inclusion or execution.

smina carries [Apache](https://github.com/mwojcikowski/smina/blob/master/LICENSE.APACHE)
and [GNU](https://github.com/mwojcikowski/smina/blob/master/LICENSE.GNU) license
files. Review the exact build and binary notices before redistribution.

Retain source/checkpoint hashes, native outputs, endpoint and scale, input
hashes, stage timing, control results, expected/actual counts, and artifact
hashes. Predicted affinity values remain computational annotations until
qualified against the declared endpoint.

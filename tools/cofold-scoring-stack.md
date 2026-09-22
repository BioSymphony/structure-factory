# Cofold Scoring Stack

Compare candidate structures across predictors and retain confidence, interface
geometry, and reference scores in one result table. Outputs support
computational review; predicted agreement does not establish binding.

## Evidence and calibration

Reviewed 2026-09-22. Confidence scores require calibration for the model,
input preparation, and target class used in the campaign.
[Junker and Schoeder's GPCR study](https://pmc.ncbi.nlm.nih.gov/articles/PMC13521358/)
reports confidence overestimation for misplaced peptides across three
prediction methods. That result supports checking geometry alongside confidence;
it does not establish a universal minimum-across-predictors threshold.

The [Overath et al. study](https://www.biorxiv.org/content/10.1101/2025.08.14.670059v2)
compares interface features on 3,766 designs across 15 targets. Treat its
model-specific results as evidence for calibration, rather than a blanket
replacement of iPTM. The minimum of directional ipSAE scores for one predicted
complex and the minimum across different predictors are different aggregations.
Record which definition the report uses.

## Select and record predictors

| Predictor or scorer | Source | Record |
| --- | --- | --- |
| Boltz | [Repository](https://github.com/jwohlwend/boltz) | Exact model, template/MSA policy, structure, confidence JSON, and full PAE |
| Chai-1 | [Repository](https://github.com/chaidiscovery/chai-lab) | Source/checkpoint, embedding/MSA settings, chain mapping, and exported confidence matrices |
| AF2-Multimer | [ColabFold](https://github.com/sokrypton/ColabFold) and [LocalColabFold](https://github.com/YoshitakaMo/localcolabfold) | Package and wrapper revisions separately, templates, alignments, model/seed identities, and PAE |
| OpenDDE | [Repository](https://github.com/aurekaresearch/OpenDDE) | Checkpoint, molecule support, summary confidence, and full atom/token sidecars |
| ipSAE | [Repository](https://github.com/DunbrackLab/IPSAE) | Script revision, PAE mapping, cutoffs, directional scores, and aggregation definition |
| DockQ | [Repository](https://github.com/bjornwallner/DockQ) | Reference structure, chain assignment, and per-interface score |

Select versions through the software registry and a validated adapter. A
published model identity and an optimized inference runtime remain separate
provenance fields. Record all seeds, samples, recycles, templates, and alignments
so a comparison can distinguish preparation differences from model differences.

## Confidence sidecars

Join each structure to its confidence file by manifest row and hash. Preserve
chain/entity order, residue or token mapping, matrix dimensions, units, and
score direction. Scalar confidence alone cannot reconstruct a missing PAE matrix.

For Boltz protein-interface review, use the structure's confidence output.
Its small-molecule affinity output measures a different task. Keep native
confidence and derived interface metrics under separate names.

Treat missing, malformed, or misaligned matrices as incomplete evidence.
Record unavailable fields explicitly rather than substituting a scalar score.

## Consensus policy

Choose the metric, aggregation, required predictor coverage, and threshold from
the campaign's control panel. Retain every per-predictor score and missing-output
state. A minimum-across-predictors policy is an explicit campaign choice; this
card supplies no universal numeric cutoff.

Keep confidence, reference-interface accuracy, target-site geometry, and
conformational-state checks as separate fields. A candidate with missing or
contradictory evidence retains its support limitation in the closeout.

## Result record

A compact comparison table contains the candidate ID, predictor/model identity,
structure hash, confidence-sidecar hash, chain mapping, metric values, reference
identity, coverage status, and validation outcome. Keep generated coordinates,
large matrices, and execution logs in runtime storage.

The execution manifest records source and checkpoint hashes, input policy,
resource limits, expected output counts, stage events, and cleanup. Confirm
source, checkpoint, service, and dependency terms before execution. Public MSA
services receive only inputs permitted by the campaign's data policy.

# Structure Factory Architecture

## Thesis

Structure Factory turns structural-biology objectives into reproducible evidence. For low-throughput structural interpretation, the target output is a reviewable dossier containing models, maps, figures, validation, methods, provenance, caveats, and next-experiment recommendations. For screening, the target output is a compact ranking ledger with explicit failure records and only selected candidate dossiers.

## Campaign Families

- `cryocore-handoff-to-dossier`: metadata-only raw cryo-EM handoff into CryoCore, then downstream deposited-evidence dossier planning once validated artifacts exist.
- `screening-superpowers`: minimal-input structure-based screening, method-jury ranking, provider-aware fanout, and selective top-hit dossier promotion.
- `multimer-state-atlas`: stoichiometry, symmetry, assembly state, interface, and conformational-state analysis.
- `model-jury`: compare experimental maps/models against prediction, design, docking, or refinement lanes.
- `publishable-figure-dossier`: structure/map-backed figure package with render scripts, sessions, captions, and visual QA.

## Control Plane

BioSymphony HQ defines shared contracts and high-level orchestration policy. Structure Factory defines the domain workflows and tool stack.

Linear stores scientific contracts:

- inputs
- expected artifacts
- acceptance criteria
- validation commands
- dependencies
- risk notes
- outcome comments

Symphony executes bounded worker issues and reports artifact paths, hashes, commands, software versions, validation results, and caveats.

## Execution Plane

Structure Factory should support multiple execution backends:

- local macOS review and visualization
- RunPod GPU pods for Structure Factory design, validation, dossier, and visualization work, as the blessed primary remote path
- AWS Batch GPU jobs for blessed cloud scale lanes
- SSH/HPC workers for institutional data/license boundaries
- generic cloud VM and neocloud pod adapters when they satisfy the same provider contract
- future object-storage backed artifact exchange

Raw cryo-EM movie intake, EMPIAR subset execution, RELION/CryoSPARC reconstruction, and map-to-model build execution are CryoCore-owned. Structure Factory records handoff contracts and consumes validated deposited or downstream artifacts for evidence, design, and reporting workflows.

Every backend must emit the same artifact tree and pass the same input-audit and contract-self-check gates. Provider completion is not scientific completion.

## Artifact Shape

Every serious campaign should terminate in a dossier:

```text
structure-dossier/
  dossier_manifest.json
  inputs/
  processing/
  maps/
  models/
  validation/
  figures/
  sessions/
  scripts/
  methods.md
  claim_ledger.md
  provenance.md
  next_experiments.md
```

Screening campaigns terminate in a ledger first:

```text
screening-results/
  screening_manifest.json
  receptor_ensemble_manifest.json
  ligand_prep.jsonl
  pose_predictions.jsonl
  affinity_predictions.jsonl
  consensus_ranking.csv
  metrics.json
  method_summary.json
  failure_report.json
  claim_ledger.json
  candidate_dossiers/
  provenance.md
```

The dossier path is reserved for top hits, controls, method-disagreement cases, and failures worth debugging.

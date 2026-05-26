# Capabilities

Structure Factory is the workflow layer around structural biology agents. It helps an agent take a target, accession, or campaign idea and produce concrete files, issue packs, run contracts, artifact checks, and evidence reports that workers and operators can pick up.

The public repo provides the reusable scaffolds, fixtures, provider contracts, and report shapes that drive these campaigns. Operator-gated execution (live credentials, paid runs, raw private data, generated structures, accepted-license state) runs through the user's own infrastructure outside public git, using the same contracts.

Raw cryo-EM movie intake, EMPIAR subset execution, RELION or CryoSPARC reconstruction, and map-to-model build execution belong to BioSymphony CryoCore. Structure Factory keeps metadata-only handoff contracts and downstream deposited-evidence, design, validation, and report workflows.

## What You Can Build

| Capability | What It Does | Public Repo Support | Private/Runtime Adds |
| --- | --- | --- | --- |
| Binder-design campaign | Defines target window, hotspots, generation lanes, cofold triage, candidate jury, and claim ledger | `examples/pd-l1-binder-design-public`, `recipes/pd-l1-binder-design-fast-path.md`, `bsf scaffold-campaign --mode binder-design` | actual generated structures, model weights, provider artifacts, experimental follow-up |
| Protein design lane | Plans Genie/RFdiffusion-style generation and Boltz/Chai-style cofold checks | tool cards, stage contracts, issue pack fields, provider templates | reviewed installs, weights, GPU execution, generated candidate packets |
| Cofold/model jury | Ranks candidate models with explicit confidence, failure rows, and non-claims | `candidate-jury.example.json`, issue drafts, claim/evidence guide | real prediction outputs and derived jury reports |
| GPCR or multimer state atlas | Splits receptor/state work into deposited-structure dossiers, prediction lanes, alignment, switch reports, and renders | `bsf scaffold-campaign --mode structure-dossier`, tool cards (cofold-scoring-stack, chimerax, proteinmpnn) | provider-backed Boltz/MPNN/ChimeraX outputs and figure packets |
| PDB/EMDB evidence dossier | Builds accession provenance, validation plan, figure outline, and report contract for deposited structure evidence | `recipes/map-model-dossier-public-data.md`, structure-dossier scaffold mode | fetched deposited maps/models, validation outputs, figure renders |
| CryoCore handoff contract | Captures raw-data accession, raw/subset gate, expected artifacts, operator approval, and ownership boundary | `examples/empiar-10204-v0`, input-audit checks, metadata-only stage contracts | CryoCore-owned raw downloads, reconstruction artifacts, provider storage, map/model build outputs |
| Screening and active learning | Demonstrates ligand/receptor fixtures, fanout estimates, result schemas, candidate dossiers, and cloud shard ledgers | `examples/screening-superpowers`, `make screening-check`, provider adapter dry-run | real libraries, real docking/cofolding, paid cloud fanout |
| Cloud/GPU execution prep | Defines RunPod/AWS/local/HPC/neocloud provider profiles, runtime gates, launch preflight, and closeout requirements | `docs/compute-backends.md`, `runpod/`, `make runpod-public-template-check`, `make launch-bundle` | actual pod/job creation, secrets, runtime logs, artifact pulls, cleanup proof |
| Linear/Symphony issue packs | Converts campaigns into durable agent tasks with owned paths, dependencies, validation commands, and outcome schema | `bsf issue-dry-run`, `packs/`, `docs/linear-orchestration.md` | live tracker state, private comments, operator approval records |
| Evidence and report packaging | Produces claim-bounded report shapes with provenance, hashes, artifact indexes, and downgrade rules | claim/evidence guide, templates, release checks | source artifact archives, hash ledgers, cost reports, cleanup records |

## Fast Starts

### Binder Design

```bash
bsf scaffold-campaign .runtime/pd-l1-binder-demo \
  --campaign-id pd-l1-binder-demo \
  --target-label "PD-L1 public interface demo" \
  --public-accession "PDB:4ZQK" \
  --window "public PD-1/PD-L1 interface window" \
  --mode binder-design
bsf validate .runtime/pd-l1-binder-demo
```

Agent prompt:

```text
Use the BioSymphony Structure Factory skill. Build a binder-design campaign plan for PDB 4ZQK with target-window dossier, generation lanes, cofold/model-jury checks, issue drafts, and a claim ledger. Do not launch compute.
```

### Structure Dossier

```bash
bsf scaffold-campaign .runtime/map-model-demo \
  --campaign-id map-model-demo \
  --target-label "Public PDB/EMDB evidence dossier demo" \
  --public-accession "PDB:4ZQK" \
  --window "deposited public structure evidence" \
  --mode structure-dossier
bsf validate .runtime/map-model-demo
```

Agent prompt:

```text
Use the Structure Factory skill. Turn this public PDB/EMDB accession into a deposited-evidence dossier plan with provenance, validation commands, expected artifacts, figure outline, and claim boundaries. If the request involves raw cryo-EM processing or reconstruction, create a CryoCore handoff instead of claiming Structure Factory owns the lane.
```

### Screening Fixture

```bash
make screening-fanout-estimate
make screening-fixture-run
make screening-results-check
```

Agent prompt:

```text
Use the Structure Factory skill. Run the screening-superpowers fixture locally, summarize the fanout and result schemas, then explain what would be required before a real cloud-backed screening run.
```

### Cloud Prep

```bash
make runpod-public-template-check
make runpod-scope-check
SMOKE_MANIFEST=runpod/launch-manifests/no-download-smoke.json make launch-preflight
make launch-bundle
```

Agent prompt:

```text
Use the Structure Factory skill. Prepare a provider-neutral GPU execution contract with budget, cleanup, runtime-secret references, expected artifacts, and closeout checks. Do not create pods or jobs.
```

## Closeout Posture

Every campaign closes with an evidence mode and a claim level so artifacts and reports are reviewable across agents and reviewers. Generated or predicted biological outputs sit at `computational_candidate` until independent validation lands. Full vocabulary is in [`claim-and-evidence.md`](claim-and-evidence.md).

The public repo makes campaigns ready for execution and review. Live provider runs (artifacts, hashes, logs, cost reports, cleanup proof, claim ledger) live in operator-controlled infrastructure outside public git, summarized safely back into reports when appropriate.

## Hard-Earned Operational Knowledge

The repo ships a catalog of operational failure modes encountered across past campaigns ([`operational-gotchas.md`](operational-gotchas.md)) and a pre-dispatch checklist pattern ([`preflight-checklist.md`](preflight-checklist.md)). Together they encode the lessons that cost real wall-clock to surface — RunPod payload limits, conda env traps, designer-specific gotchas (RFdiffusion contig-vs-PDB, RFD3 atom-spec, Genie 3 cwd dependency, PepGLAD two-chain output), cofold output-field traps (Boltz `affinity_summary.json` is the wrong file for protein-protein iPTM, Chai-1 silent ESM-no-MSA default), and orchestration cascade failures (STAGE_COMPLETE on empty outputs).

Read both before any paid GPU dispatch. The single highest-EV gate is **output-count validation**: a stage that emits `STAGE_COMPLETE` on bash exit code rather than on validated output count will silently cascade through subsequent stages with degraded inputs and call it success. See [`no-false-success-hardening.md`](no-false-success-hardening.md) for the broader closeout principle.

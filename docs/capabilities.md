# Capabilities

Structure Factory is the workflow layer around structural biology agents. It helps an agent take a target, accession, or campaign idea and turn it into concrete lanes for binder design, protein modeling, structure mapping, screening, rendering, and cloud-scale execution.

The repo provides reusable scaffolds, fixtures, provider contracts, and report shapes that drive these campaigns. Live credentials, paid runs, generated structures, accepted-license state, and raw private data stay in the user's own runtime infrastructure.

Raw cryo-EM movie intake, EMPIAR subset execution, RELION or CryoSPARC reconstruction, and map-to-model build execution belong to BioSymphony CryoCore. Structure Factory owns the handoff, downstream structure-mapping workflow, design lanes, validation checks, and report/figure packaging.

## What You Can Build

| Capability | What It Does | Public Repo Support | Private/Runtime Adds |
| --- | --- | --- | --- |
| Binder-design campaign | Defines target window, hotspots, generation lanes, cofold triage, and candidate ranking | `examples/pd-l1-binder-design-public`, `recipes/pd-l1-binder-design-fast-path.md`, `bsf scaffold-campaign --mode binder-design` | generated structures, model weights, provider artifacts, experimental follow-up |
| Protein design lane | Plans Genie/RFdiffusion-style generation and Boltz/Chai-style cofold checks | tool cards, stage contracts, task fields, provider templates | reviewed installs, weights, GPU execution, generated candidate packets |
| Cofold/model comparison | Compares candidate models with confidence summaries and failure rows | model-output schemas, task drafts, validation guide | real prediction outputs and derived comparison reports |
| GPCR or multimer state atlas | Splits receptor/state work into prediction lanes, alignment, switch reports, and renders | scaffold mode, tool cards (cofold-scoring-stack, chimerax, proteinmpnn) | provider-backed Boltz/MPNN/ChimeraX outputs and figure packets |
| PDB/EMDB structure mapping | Builds accession provenance, validation plan, figure outline, and map/model workflow | `recipes/`, structure-mapping scaffold mode | fetched deposited maps/models, validation outputs, figure renders |
| CryoCore handoff contract | Captures raw-data accession, raw/subset gate, expected artifacts, operator approval, and ownership boundary | `examples/empiar-10204-v0`, input-audit checks, metadata-only stage contracts | CryoCore-owned raw downloads, reconstruction artifacts, provider storage, map/model build outputs |
| Screening and active learning | Demonstrates ligand/receptor fixtures, fanout estimates, result schemas, candidate reports, and cloud shard ledgers | `examples/screening-superpowers`, `make screening-check`, provider adapter dry-run | real libraries, real docking/cofolding, paid cloud fanout |
| Cloud/GPU execution prep | Defines RunPod/AWS/local/HPC/neocloud provider profiles, runtime gates, launch preflight, and closeout requirements | `docs/compute-backends.md`, `runpod/`, `make runpod-public-template-check`, `make launch-bundle` | actual pod/job creation, secrets, runtime logs, artifact pulls, cleanup proof |
| Linear/Symphony task plans | Converts campaigns into durable agent tasks with owned paths, dependencies, validation commands, and outcome schema | `bsf issue-dry-run`, `packs/`, `docs/linear-orchestration.md` | live tracker state, private comments, operator approval records |
| Report and figure packaging | Produces report shapes with provenance, hashes, artifact indexes, and review rules | templates, release checks | source artifact archives, hash ledgers, cost reports, cleanup records |

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
Use the BioSymphony Structure Factory skill. Build a binder-design campaign plan for PDB 4ZQK with a target window, design lanes, cofold/model-comparison checks, task drafts, and candidate ranking. Do not launch compute.
```

### Structure Mapping

```bash
bsf scaffold-campaign .runtime/map-model-demo \
  --campaign-id map-model-demo \
  --target-label "Public PDB/EMDB structure mapping demo" \
  --public-accession "PDB:4ZQK" \
  --window "deposited public structure window" \
  --mode structure-mapping
bsf validate .runtime/map-model-demo
```

Agent prompt:

```text
Use the Structure Factory skill. Turn this public PDB/EMDB accession into a structure-mapping plan with provenance, validation commands, expected artifacts, and figure outline. If the request involves raw cryo-EM processing or reconstruction, create a CryoCore handoff instead of treating that lane as Structure Factory-owned.
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

## Run Results

Every campaign records what ran, what files were produced, which stages passed, and what still needs independent validation. Generated or predicted biological outputs remain computational candidates until downstream validation lands.

The repo makes campaigns ready for execution and review. Live provider runs (artifacts, hashes, logs, cost reports, cleanup proof, and run summaries) live in operator-controlled infrastructure outside public git.

## Hard-Earned Operational Knowledge

The repo ships a catalog of operational failure modes encountered across past campaigns ([`operational-gotchas.md`](operational-gotchas.md)) and a pre-dispatch checklist pattern ([`preflight-checklist.md`](preflight-checklist.md)). Together they encode the lessons that cost real wall-clock to surface — RunPod payload limits, conda env traps, designer-specific gotchas (RFdiffusion contig-vs-PDB, RFD3 atom-spec, Genie 3 cwd dependency, PepGLAD two-chain output), cofold output-field traps (Boltz `affinity_summary.json` is the wrong file for protein-protein iPTM, Chai-1 silent ESM-no-MSA default), and orchestration cascade failures (STAGE_COMPLETE on empty outputs).

Read both before any paid GPU dispatch. The single highest-EV gate is **output-count validation**: a stage that emits `STAGE_COMPLETE` on bash exit code rather than on validated output count will silently cascade through subsequent stages with degraded inputs and call it success. See [`no-false-success-hardening.md`](no-false-success-hardening.md) for the broader closeout principle.

# IO Gap And Public Roadmap

Last reviewed: 2026-05-08

This document is a public roadmap for the Structure Factory operating surface. The goal is to keep the useful operating shape visible while being clear about what is canonical, what is example/demo material, and what still needs provider-backed proof.

## What We Want This Repo To Do

Structure Factory should accept high-level structural-biology intent and produce reviewable outputs, not just scripts that run tools.

Primary input classes:

- Natural-language intent: "fit this public map/model", "screen this receptor", "design binders against this target window", "compare states", or "make a figure report".
- Public accession inputs: PDB, EMDB, EMPIAR, UniProt, PubChem, ChEMBL/OpenBind-like public ligand records, and public benchmark IDs.
- Secure/local references: private structures, ligand libraries, unpublished sequences, institutional paths, or license-gated assets. These must stay out of git and appear only as opaque references in manifests.
- Campaign manifests: declared data modules, lane modules, image families, provider profile, stage contract, expected artifacts, result boundary, and operator gates.
- Provider/run inputs: pinned repo ref, digest-pinned image or verified bootstrap, volume/storage scope, budget/runtime cap, secrets by reference only, and cleanup policy.

Primary output classes:

- Structure report: models/maps/figures, validation, methods, provenance, validation notes, caveats, and next-experiment notes.
- Screening ledger: prepared ligands, pose/affinity or proxy scores, consensus ranking, failures, method disagreement, provenance, and selective candidate reports.
- AI-design ranking packet: generated candidates, design config/seeds, model weights/runtime manifest, Boltz or other cross-checks, interface scores, failure rows, and conservative validation notes.
- Provider closeout packet: stage progress, exact commands, artifact pull report, hashes, cost report, cleanup proof, and contract self-check.
- Symphony/Linear work plan: bounded issues with owned paths, dependencies, validation commands, partial-success policy, and operator gates.

## Current Maturity

| Area | Current State | Main Gap |
| --- | --- | --- |
| CryoCore handoff to report | Metadata-only raw-data handoff manifests, RunPod profiles, raw-subset policies, stage contracts, and issue templates exist. | Raw-data processing, reconstruction, and map-to-model execution are CryoCore-owned; Structure Factory should only consume validated downstream artifacts or deposited public evidence. |
| PDB/EMDB structure-mapping report | Public T2R14, pol theta, and dual-report examples prove lightweight public-coordinate/map report patterns. | General accession-to-report runner is still split across target-specific scripts. |
| Screening superpowers | Fixture manifests, schemas, active-learning outputs, candidate reports, provider dry-runs, and CLI summaries exist. | Real wide/focused screening backends are still fixture/proxy or gated; calibration datasets and real provider canary are next. |
| Protein/RNA assemblies | Protein-RNA fit and binder-design contract shapes are sketched with public accession posture. | Need a general accession/entity/window resolver, receptor-window slicer, and first no-download window report for any RNP target. |
| Boltz/Genie AI design | Boltz is pinned and runner uses YAML; Genie 3 is registered and gated; runtime readiness check exists. | Genie 3 runtime is not installed/proven on GPU; first canary must validate setup, weights, CLI, output shape, and cleanup. |
| Providers | RunPod is primary blessed; AWS Batch is blessed cloud scale; neocloud/generic/local profiles are explicit. | AWS/neocloud are dry-run/adapter contracts only; RunPod real launch still needs digest-pinned image or verified bootstrap, runtime auth, and remote-pinned commit. |
| Result integrity | Stage contracts, input audit, contract self-check, validation notes, and closeout checks are strong. | Not all output contracts are schema-backed; some demos mix provider-native and derived outputs and need clearer labels before mainline storytelling. |

## Where We Are Falling Short

1. No single IO contract index.
   The repo has campaign manifests, artifact contracts, schemas, issue templates, and examples, but there is no one map that says "this input shape produces this output bundle through this runner." This makes the repo powerful but hard for future users and agents to enter.

2. Campaign manifests are less strict than screening schemas.
   Screening and orchestration-fixture examples have JSON Schemas and validators. Core campaign manifests and artifact contracts are validated by Python checks, but not all have explicit JSON Schema coverage or per-output required-field checks.

3. General materialization is behind the ambition.
   Public accession intake exists in target-specific scripts. We still need reusable materializers for PDB/EMDB/UniProt/RCSB metadata, entity/chain registries, deposited-accession records, receptor-window slicing, and secure local references.

4. Too many real workflows are still runner-specific.
   T2R14, pol theta, screening fixture, and PD-L1 binder design each have useful code, but the reusable lane boundary is not yet crisp enough. The ideal shape is: manifest compiler -> materializer -> lane runner -> artifact normalizer -> contract self-check.

5. AI-design is configured but not powered up.
   Boltz is in good shape for public GPU canaries. Genie 3 is intentionally gated and not yet proven in our runtime. The next milestone is a tiny public Genie 3 canary that proves setup, weights, outputs, and Boltz cross-check on a single target window.

6. Provider portability is a contract, not an implementation.
   RunPod has the strongest operational history. AWS Batch and neocloud profiles encode what we require, but they do not yet prove launch, log streaming, artifact egress, cost checks, or cleanup.

7. Demo and generated assets need clear tiers.
   `demos/`, public templates, task drafts, and target-specific runners should be labeled as canonical, active development, public demo, or historical summary. Ignored `.runtime/` output and generated provider packets stay outside git.

8. Mainline readiness is blocked by packaging, not tests.
   Local validation is strong, but real launch readiness still needs a remote-fetchable commit, digest-pinned or verified bootstrap posture, and runtime registry/auth decisions. Main can accept prep contracts; main should not imply paid runtime is ready.

## Repo Structure We Should Move Toward

No deletion is needed. The organizing move is to make each directory's role explicit and reduce ambiguity.

Canonical tracked structure:

```text
campaigns/                 Durable campaign specs, wave plans, task drafts.
docs/                      Architecture, policies, runbooks, gap analyses, lessons.
modules/                   Machine-readable contracts: campaigns, data, lanes, schemas, providers.
examples/                  Small public fixtures and example manifests.
demos/                     Human-facing result summaries.
references/                Registries, reusable notes, workflow templates.
runpod/                    RunPod-specific launch manifests, bridge manifests, entrypoints, stage contracts.
containers/                Image-family plans, not necessarily built images.
scripts/structure_factory/ Reusable validators, materializers, runners, and brokers.
scripts/runpod/            RunPod bootstrap/setup scripts.
templates/                 Linear/operator/contract templates.
tests/                     Unit tests for repo validators and runners.
internal/private/          Ignored local-only operator notes, never secrets.
.runtime/                  Ignored generated output and provider artifacts.
```

Suggested subfolder labels:

- `campaigns/<id>/README.md`: scientific objective and durable wave plan.
- `campaigns/<id>/linear-issues/`: task drafts only, not runtime truth.
- `examples/<family>/`: tiny public manifests that must validate on a laptop.
- `demos/<id>/`: curated public results, explicitly labeled by source posture.
- `runpod/bridge-manifests/`: public non-launchable provider-packet shape only; concrete generated provider packets belong under ignored runtime or operator-controlled storage.
- `docs/archive/` or `campaigns/<id>/archive/`: future home for superseded docs when we want to move, not delete.

## Public Repo Strategy

Public releases should mature in staged slices:

1. Contract slice:
   Merge schemas, provider posture, AI-design lane-check work, and docs. This is safe because it is no-download and does not present runtime success.

2. Runner slice:
   Merge Boltz YAML runner updates, Network Volume PATH discovery, bootstrap gates, and runtime readiness checks. This is still safe if docs clearly say strict runtime fails until run in a GPU environment.

3. Demo and lessons slice:
   Merge curated demos and lessons only after labeling source posture for each piece.

4. Provider-execution slice:
   Merge only after a real canary has digest-pinned or verified bootstrap posture, remote-pinned commit, artifact hashes, cost/cleanup proof, and updated `docs/agent-run-learnings.md`.

Immediate public-readiness blockers:

- Keep the public export as a clean-history root or reviewed public release series.
- Pin a remote-fetchable commit before any provider launch statements.
- Resolve whether private GHCR images or public base plus Network Volume bootstrap is the chosen first RunPod posture.
- Keep `make public-switch-check` documented as the local public-release gate; GPU runtime readiness remains a separate provider milestone.

## Next Work Items

High leverage, no paid compute:

1. Add an IO contract index that maps each campaign family to input manifest, materializer, runner, output contract, validator, and result boundary.
2. Add JSON Schemas for campaign manifests and artifact contracts, or strengthen `module_manifest_check.py` to validate output groups more deeply.
3. Create a public accession resolver for PDB/EMDB/UniProt/RCSB metadata that emits `resolved_accessions.json` and `entity_registry.json`.
4. Create a general receptor-window slicer that emits `target_window_manifest.json` with entity, chain, residue range, source accession, and hash provenance for any public PDB target.
5. Keep `make mainline-readiness-check` as the no-paid-compute mainline gate and explicitly skip local GPU/runtime gates.

First paid/provider milestone:

1. Run a no-download RunPod canary using the chosen source-delivery posture.
2. Bootstrap or activate Boltz on GPU and pass `make harness-check` for Boltz-only.
3. Run a tiny Genie 3 setup/toolcheck canary with `GENIE3_ALLOW_COLABFOLD_PARAMS=1` only after operator approval.
4. Fetch, hash, and validate artifacts; clean up provider resources; update `docs/agent-run-learnings.md`.

The north star: a future user should be able to provide a public accession or safe local reference, choose a workflow, and get a report or ranking ledger whose source posture, provenance, and result boundary are obvious without reading chat history.

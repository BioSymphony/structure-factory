# BioSymphony Structure Factory Agent Guide

Workspace for long-horizon structural biology missions, built for agents that drive multi-agent harnesses (Symphony with Linear, Claude Code with Linear, Codex, `/goal`, GitHub Issues, Notion, or any tracker).

## Mission

Help a user and their agents take a structural biology goal (for example, "design binders for PD-L1," "atlas every active-state GPCR in the PDB," "map this public EMDB/PDB structure," or "fan out a screening campaign across cloud") and run it to reviewable completion across local and cloud compute.

The repo ships:

- portable agent instructions for any agent runtime
- campaign manifests, stage contracts, and provider profiles for RunPod, AWS, Modal, Lambda, neocloud, HPC, and local
- target-window files, generation, cofold, scoring, render, and screening lanes
- tracker-neutral task packs that import cleanly into Linear, GitHub Issues, Notion, or any queue
- validators, audit gates, capability catalog, and a dependency-free `bsf` CLI

Ownership boundary: raw cryo-EM movie intake, EMPIAR subset execution, RELION or CryoSPARC reconstruction, and map-to-model build execution belong to BioSymphony CryoCore. This repo keeps public metadata, handoff gates, downstream structure-mapping contracts, validation plans, and reviewable summaries.

## How To Drive A Mission

When the orchestrator hands you work, the loop is:

```text
goal
  -> bsf catalog .                              # what is available
  -> bsf scaffold-campaign <runtime>/<id> ...   # target, lanes, run boundaries
  -> bsf validate <runtime>/<id>                # campaign and stage contract sound
  -> bsf issue-dry-run                          # split into tracker work
  -> orchestrate workers or launch provider     # Symphony, Linear, Codex, others
  -> verify artifacts and sign closeout
```

Fan out across multiple workers when the work exceeds one agent turn. Task packs define owned paths, dependencies, validation commands, and outcome schemas so workers can run in parallel without colliding.

## Compute Available

- **Local.** Workstation profile, no GPU needed for planning lanes.
- **RunPod.** Pod profiles for design, cofold, structure mapping, raw-subset, and render lanes.
- **AWS.** Batch GPU and EC2 GPU profiles.
- **Modal.** Serverless GPU-function profile for bounded canaries and small single-container fanouts.
- **Lambda Cloud.** Ephemeral GPU-VM profile for no-persistent-filesystem canaries.
- **Neocloud.** GPU pod profile.
- **Generic cloud VM.** GPU VM profile.
- **SSH or HPC.** Via the generic-cloud or local patterns.

Each provider profile carries operator-gate, license-gate, budget, cleanup, and closeout requirements. Closeout requires artifacts, hashes, and validation notes.

## Orchestrators Supported

The skill is orchestrator-neutral. Use the portable skill copy at `skills/biosymphony-structure-factory/SKILL.md` with Codex, Claude Code, Symphony with Linear, a `/goal` stack, or any agent runtime that reads Markdown instructions.

Symphony with Linear coordination is documented in [`docs/linear-orchestration.md`](docs/linear-orchestration.md).

## Tools And Lanes In Scope

- Design: Genie3, RFdiffusion, HelixDiff, PepGLAD, EvoBind, ProteinMPNN, and the Baker miniprotein-GPCR recipe.
- Multistate and switch design: SwitchCraft, with outputs routed through the cofold-scoring stack for an orthogonal check.
- Construct assembly and multidomain fusion: DOMINO, downstream of a validated binder (upstream license unresolved).
- Cofolding, prediction, and scoring: Boltz, Chai, ESMFold2, and cofold-scoring stacks.
- Refinement and rendering: ChimeraX, MD, and docking pipelines.
- Target prep: target-window builders, GCGR target prep.
- Screening: screening fixtures and candidate report shapes.

See [`tools/`](tools/) and [`references/software-registry.yaml`](references/software-registry.yaml). Add your own through tool cards.

## Public Safety Rules

Use public accessions, synthetic rows, or compact fixtures. Label source posture clearly. Do not add:

- private structures, maps, unpublished sequences, or patient data
- raw cryo-EM movies, half-maps, heavy databases, checkpoints, or model weights
- provider credentials, tokens, registry auth, signed URLs, or one-time transfer codes
- concrete private pod IDs, network volume IDs, account IDs, billing records, or raw provider logs
- private Linear issue text, internal run notes, or private workstation paths
- wet-lab synthesis instructions, dosing guidance, therapeutic conclusions, or clinical advice

## Agent Entry Points

- Read `PUBLIC_RELEASE.md` before release, publication, or handoff work.
- Read `docs/agentic-biology-harness.md` to understand the public BioSymphony or Symphony operating model.
- Use `skills/biosymphony-structure-factory/SKILL.md` as the portable agent-instruction entry point.
- Use `packs/task-packs/binder-design-fast-path-v0/` when a tracker-neutral task import is needed.
- Use `templates/operator-wave-runbook.md` before promoting paid, cloud, raw-download, or multi-agent waves.
- Treat `runpod/` as the default reviewed cloud-pod path. AWS Batch handles cloud scale, and Modal serverless GPU functions plus Lambda Cloud GPU VMs are reviewed remote paths under the same artifact and cleanup contract.

## Key Patterns

- Treat task packs as campaign contracts, not generic todos.
- Keep every generated or predicted output attached to a clear result boundary.
- Use the public result states in manifests and closeouts: `planning`, `public_demo`, `public_synthetic_demo`, `computational_candidate`, `blocked`, or `insufficient_support`.
- Track source posture separately from result boundary. Source posture may describe where outputs came from, such as `public_data`, `synthetic_demo`, `generated_candidate`, `derived`, `provider_native`, `report_only`, `blocked`, or `insufficient_support`.
- Closeout requires stage events, expected artifacts, hashes, and validation notes.
- Public examples are for structure and workflow shape, not unreviewed wet-lab action.

## Common Checks

```bash
make harness-check
make release-check
make public-audit
make secret-scan
```

`make secret-scan` uses gitleaks when available and skips gracefully otherwise.

## Before A Paid Dispatch

Read [`docs/operational-gotchas.md`](docs/operational-gotchas.md) and [`docs/preflight-checklist.md`](docs/preflight-checklist.md). The first is a ~45-class catalog of failure modes with pre-flight probes and fixes; the second is a ten-gate pre-dispatch checklist pattern. They encode the lessons that cost real wall-clock and money to surface across past campaigns.

The single most important gate is **output-count validation** (G8 / class #34): a stage that emits `STAGE_COMPLETE` on bash exit code rather than on validated output count will silently cascade through subsequent stages with degraded inputs. Every worker must count outputs before declaring success.

## Result Boundaries

This repo produces planning scaffolds, computational candidate rankings, and validation-roadmap artifacts. Binding, function, therapeutic value, safety, manufacturability, and clinical relevance are confirmed through wet-lab and clinical processes outside this repo. See [`NON_CLAIMS.md`](NON_CLAIMS.md) for the full boundary.

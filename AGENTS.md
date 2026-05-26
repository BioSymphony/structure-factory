# BioSymphony Structure Factory Agent Guide

Workspace for long-horizon structural biology missions, built for agents that drive multi-agent harnesses (Symphony with Linear, Claude Code with Linear, Codex, `/goal`, GitHub Issues, Notion, or any tracker).

## Mission

Help a user and their agents take a structural biology intent (for example, "design binders for PD-L1," "atlas every active-state GPCR in the PDB," "ship a deposited-evidence dossier for this EMDB map," or "fan out a screening campaign across cloud") and run it to verified completion across local and cloud compute.

The repo ships:

- Codex-compatible and portable skill instructions for any agent runtime
- campaign manifests, stage contracts, and provider profiles for RunPod, AWS, neocloud, HPC, and local
- target-window dossiers, generation and cofold and render lanes, candidate juries, evidence dossiers
- tracker-neutral issue packs that import cleanly into Linear, GitHub Issues, Notion, or any queue
- validators, audit gates, capability catalog, and a dependency-free `bsf` CLI

Ownership boundary: raw cryo-EM movie intake, EMPIAR subset execution, RELION or CryoSPARC reconstruction, and map-to-model build execution belong to BioSymphony CryoCore. This repo keeps public metadata, handoff gates, downstream dossier contracts, validation plans, and deposited-evidence reviews.

## How To Drive A Mission

When the orchestrator hands you work, the loop is:

```text
intent
  -> bsf catalog .                              # what is available
  -> bsf scaffold-campaign <runtime>/<id> ...   # target, lanes, claim ceiling
  -> bsf validate <runtime>/<id>                # campaign and stage contract sound
  -> bsf issue-dry-run                          # split into tracker work
  -> orchestrate workers or launch provider     # Symphony, Linear, Codex, others
  -> verify artifacts and sign closeout
```

Fan out across multiple workers when the work exceeds one agent turn. Issue packs define owned paths, dependencies, validation commands, and outcome schemas so workers can run in parallel without colliding.

## Compute Available

- **Local.** Workstation profile, no GPU needed for planning lanes.
- **RunPod.** Pod profiles for design, cofold, dossier, raw-subset, and render lanes.
- **AWS.** Batch GPU and EC2 GPU profiles.
- **Neocloud.** GPU pod profile.
- **Generic cloud VM.** GPU VM profile.
- **SSH or HPC.** Via the generic-cloud or local patterns.

Each provider profile carries operator-gate, license-gate, budget, cleanup, and closeout requirements. Closeout requires artifacts, hashes, and a claim audit.

## Orchestrators Supported

The skill is orchestrator-neutral. Drop it into Codex, Claude Code, Symphony with Linear, a `/goal` stack, or any agent runtime that reads skill files. The portable skill copy at `skills/biosymphony-structure-factory/SKILL.md` is for runtimes that do not speak Codex format.

Symphony with Linear coordination is documented in [`docs/linear-orchestration.md`](docs/linear-orchestration.md).

## Tools And Lanes In Scope

- Design: Genie3, RFdiffusion, HelixDiff, PepGLAD, EvoBind, ProteinMPNN.
- Cofolding and scoring: Boltz, Chai, and cofold-scoring stacks.
- Refinement and rendering: ChimeraX, MD, and docking pipelines.
- Target prep: target-window dossier builders, GCGR target prep.
- Screening: screening-superpowers fixture and candidate dossier shapes.

See [`tools/`](tools/) and [`references/software-registry.yaml`](references/software-registry.yaml). Add your own through tool cards.

## Public Safety Rules

Use public accessions, synthetic rows, or compact fixtures. Label evidence mode clearly. Do not add:

- private structures, maps, unpublished sequences, or patient data
- raw cryo-EM movies, half-maps, heavy databases, checkpoints, or model weights
- provider credentials, tokens, registry auth, signed URLs, or one-time transfer codes
- concrete private pod IDs, network volume IDs, account IDs, billing records, or raw provider logs
- private Linear issue text, internal run notes, or private workstation paths
- wet-lab synthesis instructions, dosing guidance, therapeutic claims, or clinical advice

## Agent Entry Points

- Read `PUBLIC_RELEASE.md` before release, publication, or handoff work.
- Read `docs/agentic-biology-harness.md` to understand the public BioSymphony or Symphony operating model.
- Use `.codex/skills/biosymphony-structure-factory/SKILL.md` when the agent runtime supports Codex-style skills.
- Use `skills/biosymphony-structure-factory/SKILL.md` as the portable copy for other agent stacks.
- Use `packs/issue-packs/binder-design-fast-path-v0/` when a tracker-neutral Symphony or Linear import is needed.
- Use `templates/operator-wave-runbook.md` before promoting paid, cloud, raw-download, or multi-agent waves.
- Treat `runpod/` as the blessed first cloud-pod path, with AWS Batch and other providers held to the same artifact and cleanup contract.

## Key Patterns

- Treat issue packs as scientific contracts, not generic todos.
- Keep every claim attached to an exact claim level.
- Use the public claim levels in manifests and closeouts: `planning`, `public_demo`, `public_synthetic_demo`, `computational_candidate`, `blocked`, or `insufficient_evidence`.
- Track evidence mode separately from claim level. Evidence mode may describe source posture such as `public_data`, `synthetic_demo`, `generated_candidate`, `derived`, `provider_native`, `report_only`, `blocked`, or `insufficient_evidence`.
- Closeout requires stage events, expected artifacts, hashes, and a claim audit.
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

## Claim Boundaries

This repo produces planning dossiers, computational candidate juries, and validation-roadmap artifacts. Binding, function, therapeutic value, safety, manufacturability, and clinical relevance are confirmed through wet-lab and clinical processes outside this repo. See [`NON_CLAIMS.md`](NON_CLAIMS.md) and [`docs/claim-and-evidence.md`](docs/claim-and-evidence.md) for the full vocabulary.

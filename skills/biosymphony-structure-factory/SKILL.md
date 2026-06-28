---
name: biosymphony-structure-factory
description: Use when planning structural biology campaigns, binder-design triage, model comparison, structure mapping, RunPod or cloud GPU stage contracts, or Symphony or Linear task packs for long-running biological agent work.
---

# BioSymphony Structure Factory

Use this skill when a structural biology mission needs a durable, multi-step work program rather than a single answer. The skill helps you turn a target, accession, or campaign idea into a scaffolded campaign with target contracts, agent lanes, provider profiles, candidate rankings, and structure reports that other workers and operators can pick up and verify.

The skill is built for agents that drive multi-agent harnesses. Use it inside Codex, Claude Code, Symphony with Linear, a `/goal` stack, GitHub Issues, Notion task queues, or any agent runtime that can read a skill file. The repo also supports single-agent local work for users without an orchestrator.

## Always Read

- `README.md`
- `AGENTS.md`
- `NON_CLAIMS.md`
- `docs/agentic-biology-harness.md`
- `docs/public-export-shape.md`

## Read When Applicable

- `docs/intake-interview.md` for ambiguous, data-bearing, license-bearing, cost-bearing, or workflow-sized requests.
- `docs/linear-orchestration.md` before generating or dispatching Symphony or Linear task packs.
- `docs/compute-backends.md` when selecting local, RunPod, AWS Batch, SSH or HPC, generic cloud, or neocloud execution.
- `docs/runpod-stack.md` before RunPod prep or launch.
- `docs/tooling-and-licensing.md` before selecting, installing, baking, or running tool lanes.
- `docs/confidence-sidecars.md` before editing or launching any fold, cofold, scoring, ranking, or render lane that depends on confidence metrics.
- `docs/no-false-success-hardening.md` before provider-backed execution or scientific closeout.
- `docs/operational-gotchas.md` before any paid GPU dispatch: a 45-class catalog of failure modes with pre-flight probes and fixes.
- `docs/preflight-checklist.md` for the 10-gate pre-dispatch checklist pattern (PDB chain identity, hotspot atom-spec, output-count validation, operator approval, etc.).
- `docs/agent-run-learnings.md` for durable lessons across past Structure Factory campaigns.
- `examples/pd-l1-binder-design-public/README.md` for the public binder-design fast path.
- `docs/quickstart-tour.md`, `docs/cli-reference.md`, and `docs/agent-recipes.md` when helping a public user start from scratch.
- `docs/faq.md` and `docs/glossary.md` when a user or a general-purpose agent is unfamiliar with structural biology terms, agent harness conventions, or how to operate the repo without a tracker.

## Mission Modes

- `planning`: define target, data posture, result boundaries, lanes, risks, dependencies, and task pack.
- `public_demo`: use public accessions, synthetic fixtures, and compact reports.
- `gpu_prep`: prepare RunPod, cloud, or local stage contracts, launch templates, and validation commands without provider execution.
- `symphony_dispatch`: generate tracker-neutral issues for Symphony, Linear, Claude-lane review, or any agent queue.
- `report_or_review`: synthesize existing outputs into candidate rankings, validation notes, structural reports, and figures.
- `provider_run`: when explicitly authorized, require budget, runtime cap, cleanup policy, artifact list, hashes, and closeout gates.

## Operating Rules

- Use public accessions, synthetic examples, or explicit operator-approved data references.
- Keep credentials, provider IDs, private paths, generated structure archives, raw cryo-EM data, unpublished sequences, patient data, and model weights outside public git.
- Mark source posture and result boundary on every closeout. Computational candidates stay at `computational_candidate` until independent validation exists.
- Closeout requires stage events, expected artifacts, hashes, and validation notes. A passing process exit alone does not finish the work.
- Long or GPU workflows need stage contracts, expected artifacts, progress ledgers, partial-success policy, and result boundaries.
- License-gated tools stay gated until the user's use context and runtime access are explicit.
- **Currency discipline.** Tools, weights, benchmarks, and gate thresholds move fast. Before scaling a campaign or any paid GPU dispatch, run a primary-source freshness check on each tool the campaign uses: upstream repo HEAD (releases tab + recent commits), current release notes, and recent preprints (biorxiv, chemrxiv, arxiv) on the relevant lane. Record the version pin and the date of the check in the candidate ranking or validation notes so a future agent can re-verify rather than re-discover. Tool cards in `tools/` and the recipes in `docs/operational-gotchas.md` and `tools/cofold-scoring-stack.md` are point-in-time snapshots; verify before depending on them for a real run.

## Multi-Agent Dispatch

Structure Factory is a sidecar that fits into any agent harness:

- **Symphony with Linear.** Symphony coordinates bounded workers and outcome parsing. Linear carries durable task contracts and state. Task packs in `packs/` import cleanly through `bsf issue-dry-run`.
- **Claude Code with Linear.** Assign each lane in a pack to a Claude worker. Use the validation commands in each issue as worker exit gates.
- **`/goal` orchestrators.** Translate the goal into a campaign contract through `bsf scaffold-campaign`, then create issues only when the work exceeds one agent turn.
- **GitHub Issues, Notion, or other queues.** The tracker-neutral pack format imports the same way.

Use routing label:

```text
sym:structure-factory
```

Keep high-cost, data-bearing, license-gated, or provider-backed work in backlog until an operator gate authorizes it. Optional Claude-lane or review agents can participate. They close with source posture, result boundary, validation summary, and artifact references.

## RunPod And Cloud Resources

RunPod is the default reviewed paid-pod path for this repo. AWS Batch is the reviewed cloud-scale path. Local, SSH or HPC, generic cloud, and neocloud profiles are allowed when they preserve the same input-audit, stage-contract, artifact, cleanup, and self-check gates.

For real RunPod work:

1. declare the execution profile and setup posture
2. run launch and scope checks
3. use placeholders or runtime-secret references in public files
4. emit `stage-progress.jsonl` or equivalent progress records
5. fetch required artifacts and hashes
6. verify cleanup
7. label partial or missing outputs honestly

## Binder-Design Fast Path

1. If starting fresh, run `bsf scaffold-campaign` into `.runtime/` first.
2. Define target accession, chain or window, hotspot plan, and result boundaries.
3. Pick generation lanes and cofold or model-comparison lanes.
4. Add runtime gates for GPU tools, weights, and use-context checks.
5. Declare expected artifacts and the stage contract.
6. Generate tracker-neutral task drafts.
7. Produce the candidate ranking and validation notes.

Fast means the planning, setup, triage, and report loop is compressed. Wet-lab validation happens outside the repo.

## Validation

Run:

```bash
make harness-check
make release-check
```

Before publication, also run:

```bash
make secret-scan
```

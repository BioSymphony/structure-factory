# BioSymphony Structure Factory

![BioSymphony Structure Factory: a pixel-art lab with a conceptual protein model](docs/assets/structure-factory-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Status: pre-alpha](https://img.shields.io/badge/status-pre--alpha-orange.svg)](#status)

BioSymphony Structure Factory creates and validates plans for binder design,
structure prediction, and model comparison. Scientists and AI agents use its
`bsf` CLI, Markdown skills, and templates to define inputs, select tools and
compute providers, and check result files and candidate rankings.

Start with a public accession or a synthetic fixture. Local planning and
validation need Python 3.10+; individual prediction and design tools have
separate runtime requirements.

## What Is Included

<p align="center">
  <img src="docs/assets/system-context.svg" width="560" alt="A campaign request enters the CLI and agent skills. Templates, validators, tool cards, and provider profiles produce campaign plans, task packs, and run packets.">
</p>

## Start Here

| To | Start With |
| --- | --- |
| Plan a campaign with an AI agent | [Structure Factory skill](skills/biosymphony-structure-factory/SKILL.md) and [campaign brief](#how-to-use-this) |
| Compare binder-design methods | [Binder-lane round guide](docs/binder-lane-round.md) |
| Try the local CLI | [Install and inspect the example](#inspect-or-run-the-repo-yourself) |
| Choose a tool | [Tool radar](docs/tool-and-skill-radar.md) and [tool cards](tools/README.md) |
| Create tracker tasks | [Workflow map](docs/workflow-map.md) and `bsf issue-dry-run` |

## How To Use This

Give your agent the [Structure Factory skill](skills/biosymphony-structure-factory/SKILL.md)
and a campaign brief.

### Copyable Campaign Brief

```text
Use the BioSymphony Structure Factory skill in this repository.
Target: <public accession or synthetic fixture; chains; residue window or site rule>.
Goal: <design, predict, compare models, screen, map structures, or render>.
Comparison: <source-tool replay, workflow-shape replay, deliberate tool swap, or none>.
Routes: <local tool, hosted API, platform skill, or compute provider for each stage>.
Limits: <budget, runtime, rounds, candidates, primary metric, stopping rule>.
Outputs: <expected files and counts, hashes, receipts, cleanup evidence, figures>.
Validate the request, prepare the handoff files, and dry-run the selected routes.
List any authorization required before execution.
```

The agent writes campaign and stage contracts, validates them, and prepares
adapter inputs. An `adapter_required` record needs a validated adapter under
ignored `.runtime/`; a platform-skill route must produce the same declared
outputs. A dry run checks the route's configuration.

Obtain explicit human authorization before a paid provider start, non-public upload, terms acceptance, or large or license-gated download. The approval names the route, data posture, budget, runtime, and applicable terms.

## Hand A Mission To An Agent

> Use the Structure Factory skill to plan a GPCR activation-state atlas from public PDB accessions. Prepare per-state prediction and render contracts, with expected summaries, figures, and provenance. Stop after local validation.

[Use cases](docs/use-cases.md) contains more prompts for binder comparison,
screening, structure mapping, and CryoCore handoffs.

## Claude/Anthropic Binder-Study Lane

The [binder-lane skill](skills/binder-lane-round/SKILL.md) implements an independent
workflow based on [Anthropic's public report](https://www-cdn.anthropic.com/30bf50e22a01388bb29bf077ee3f244531594b7a.pdf)
and [released binder-design dataset](https://huggingface.co/datasets/Anthropic/claude-protein-binder-design).
Choose a source-tool replay where the selected route supports those identities,
a workflow-shape replay that preserves the stages, or a deliberate tool swap.

The [round guide](docs/binder-lane-round.md) documents execution and result
contracts. The [decision loop](docs/binder-study-decision-loop.md) records the
choices for each round. Keep targets, controls, scoring, and failure handling
consistent across ranked comparison arms; label different methods exploratory.

## When To Use This

Use Structure Factory to plan campaign stages, prepare compute, or compare
computational results. Each execution route has its own tool, adapter, and
compute requirements.

## What Users And Their Agents Can Run

| Use | Included Support | Files To Expect |
| --- | --- | --- |
| [Plan binder design](examples/pd-l1-binder-design-public) | Validated local example and task generation | Target window, stage plan, ranking schema |
| [Compare binder toolchains](docs/binder-lane-round.md) | Planning, execution, calibration, and closeout commands | Comparison arms, route plans, execution receipts |
| [Plan a state atlas](docs/use-cases.md) | GPCR and multimer planning patterns | State work plan, prediction and figure specifications |
| [Prepare a screen](examples/screening-superpowers) | Local fixture and provider dry run | Work estimate, shard ledger, ranking rows |
| [Map deposited structures](recipes/) | PDB and EMDB recipes | Accession provenance, validation plan, report specifications |
| [Prepare a cryo-EM handoff](examples/empiar-10204-v0) | Public metadata scaffold for CryoCore | Handoff record, downstream mapping contract |
| [Compare predicted models](tools/cofold-scoring-stack.md) | Scoring and review contracts | Confidence fields, failure rows, comparison schema |
| [Prepare compute](docs/compute-backends.md) | Provider profiles and launch templates | Budget, artifact, and cleanup requirements |

See [capabilities](docs/capabilities.md) for execution coverage and
[use cases](docs/use-cases.md) for campaign prompts.

## Works With Your Stack

Markdown skills and tracker-neutral task packs work with Codex, Claude Code,
Symphony with Linear, GitHub Issues, and other systems that read the same files.

Stage contracts cover local tools, hosted APIs, platform skills, FAL, Modal,
RunPod, Lambda Cloud, AWS, neocloud VMs, and SSH/HPC. A campaign can mix routes.
Provider profiles record setup requirements; runtime readiness depends on the
selected adapter and tool.

Check the [software registry](references/software-registry.yaml) and
[tooling and licensing guide](docs/tooling-and-licensing.md) before execution.

## Inspect Or Run The Repo Yourself

Install the CLI and check the public example:

```bash
git clone https://github.com/BioSymphony/structure-factory.git
cd structure-factory
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

bsf --help
bsf doctor .                                       # local setup and contract checks
bsf catalog . --format markdown                    # what the repo offers
bsf validate examples/pd-l1-binder-design-public   # validate the flagship example
bsf audit .                                        # release-blocker scan
bsf harness-check .                                # required files and references
make read-only-audit                               # reviewer checks, no .runtime writes
```

These checks run locally without a GPU or provider account.
`make read-only-audit` leaves `.runtime/` unchanged. The scaffold and task-draft
commands write there; `make clean` removes those generated files.

Scaffold a campaign:

```bash
bsf scaffold-campaign .runtime/pd-l1-binder-demo \
  --campaign-id pd-l1-binder-demo \
  --target-label "PD-L1 public interface demo" \
  --public-accession "PDB:4ZQK" \
  --window "public PD-1/PD-L1 interface window"
bsf validate .runtime/pd-l1-binder-demo
```

Generate tracker-neutral task drafts:

```bash
bsf issue-dry-run examples/pd-l1-binder-design-public \
  --out .runtime/pd-l1-issues
```

`issue-dry-run` selects task names and acceptance criteria for the campaign mode.

See the [CLI reference](docs/cli-reference.md) for command options and
[skill installation guide](docs/skill-install.md) for agent setup.

## Workflow Stages

<p align="center">
  <img src="docs/assets/workflow-ladder.svg" width="560" alt="Define and validate a campaign, then prepare tasks and routes locally. Optional execution runs selected tools and checks their outputs.">
</p>

You can stop after campaign planning or task preparation. For execution, choose
configured local tools, hosted APIs, or a compute provider for each stage.

| Checkpoint | Command Or Record |
| --- | --- |
| Inspect available capabilities | `bsf catalog . --format markdown` |
| Validate campaign inputs and stages | `bsf validate <campaign>` |
| Draft tracker tasks | `bsf issue-dry-run <campaign>` |
| Check a selected execution route | Provider readiness and stage-contract checks |
| Review a completed run | Declared files and counts, hashes, receipts, cost record, and cleanup proof |

## Binder-Design Fast Path

The [PD-L1 example](examples/pd-l1-binder-design-public) includes a target window
for PDB `4ZQK`, generation and cofold plans, a candidate-ranking schema, and
result labels. Follow the [fast-path recipe](recipes/pd-l1-binder-design-fast-path.md)
to validate the example and generate task drafts.

Before a comparative generation run, use `target-check --plan <plan.json>` to
check the coordinate input. The example covers computational preparation;
result boundaries are defined in [NON_CLAIMS.md](NON_CLAIMS.md).

## BioSymphony Harness

The [agentic biology harness](docs/agentic-biology-harness.md) defines how an
orchestrator reads campaign contracts, assigns tracker-neutral tasks from
[`packs/`](packs/), and checks completion. Campaigns can stop after planning,
task generation, or provider preparation. Execution records and generated
artifacts stay in runtime storage.

## Newcomer Resources

- [`docs/faq.md`](docs/faq.md). Common questions about GPUs, trackers, agents, and adding your own tools.
- [`docs/glossary.md`](docs/glossary.md). Structural biology and Structure Factory terms a newcomer or general-purpose agent may want defined.
- [`docs/workflow-map.md`](docs/workflow-map.md). The local-to-tracker-to-cloud ladder.
- [`docs/quickstart-tour.md`](docs/quickstart-tour.md). Local tour for people who want to run the CLI.
- [`docs/use-cases.md`](docs/use-cases.md). Copyable agent prompts for each mission type.

## Operational Notes

Read these before a paid GPU dispatch. They describe public checks for provider, predictor, artifact-integrity, and smoke-test work.

- [`docs/operational-gotchas.md`](docs/operational-gotchas.md). Failure classes, preflight probes, and fixes for provider and tool runs.
- [`docs/reproducibility-checks.md`](docs/reproducibility-checks.md). Direct dependency-pin resolution and complete output-tree comparison.
- [`docs/preflight-checklist.md`](docs/preflight-checklist.md). Checks for target identity, hotspot syntax, output counts, human approval, artifacts, and cleanup.
- [`docs/agent-run-learnings.md`](docs/agent-run-learnings.md). Execution checks for provider, predictor, artifact-integrity, and smoke-test work.
- [`docs/no-false-success-hardening.md`](docs/no-false-success-hardening.md). Required output checks and partial-result handling.

## Public Release

Before publishing or handing this repository to a fresh in-repository agent, read [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md) and [`docs/public-switch-checklist.md`](docs/public-switch-checklist.md). The full local public-switch gate is:

```bash
make public-switch-check
```

Bridge manifests in [`runpod/bridge-manifests`](runpod/bridge-manifests/) are tracked templates. They omit credentials, live provider IDs, accepted-license state, and authorization. A person working with an agent can materialize an ignored `.runtime/` packet and complete readiness and scope checks. Use a validated adapter only after the approval covers the proposed paid start, data posture, budget, runtime, and applicable terms. Keep concrete placement, run IDs, secrets, approvals, logs, and fetched artifacts out of tracked git files.

## Repository Layout

```text
campaigns/  Public campaign specs, wave plans, and task drafts
demos/      Curated result narratives and summary examples
docs/       Workflow, capability, agent-recipe, provider, and licensing guidance
examples/   Public binder-design and EMPIAR examples
modules/    Reusable data, lane, provider, image, artifact, and schema contracts
packs/      Tracker-neutral task templates for Symphony and Linear workflows
runpod/     Launch templates, manifests, entrypoints, and stage contracts
schemas/    JSON schema references for consumers
scripts/    Validators, materializers, dry-run generators, and stage checks
skills/     Agent skill instructions
src/        bsf CLI: validator, scaffolder, catalog, audit
templates/  Issue and campaign templates
tests/      Public release checks
tools/      Tool and lane cards
```

See [`docs/public-export-shape.md`](docs/public-export-shape.md) for the public boundary used for this export.

## Validation And Boundaries

Every closeout records what was run, what changed, what artifacts exist, and what still needs independent validation. Boundaries the repo does not cross live in [`NON_CLAIMS.md`](NON_CLAIMS.md) and [`BIOSAFETY.md`](BIOSAFETY.md). Release hygiene is documented in [`PUBLIC_RELEASE.md`](PUBLIC_RELEASE.md).

## Status

Pre-alpha. The included local checks cover campaign planning, task generation, provider contracts, public fixtures, and release scans. Provider-backed biological results require separate execution records and scientist review.

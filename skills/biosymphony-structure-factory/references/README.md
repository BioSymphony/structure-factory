# BioSymphony Structure Factory

![BioSymphony Structure Factory: a pixel-art lab with a conceptual protein model](docs/assets/structure-factory-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Status: pre-alpha](https://img.shields.io/badge/status-pre--alpha-orange.svg)](#status)

BioSymphony Structure Factory helps scientists and AI agents select, call, and
chain structural biology tools. It combines a tool knowledge base with a CLI,
agent skills, and an adapter executor for design, structure prediction, and
model comparison.

Use tool cards to choose a method, bind an installed tool or service client,
and pass its checked outputs to the next stage. Scientific tools, model
weights, and provider access are configured separately.

## What Is Included

<p align="center">
  <img src="docs/assets/system-context.svg" width="560" alt="The tool knowledge base informs your agent's choices. The CLI and skills call configured tools, connect their outputs, and produce structures, scores, rankings, and figures.">
</p>

| Capability | What You And Your Agent Can Do | Start With |
| --- | --- | --- |
| Find tools | Compare roles, inputs, outputs, runtime needs, licenses, source repos, and papers | [Tool cards](tools/README.md), [software registry](references/software-registry.yaml), [tool radar](docs/tool-and-skill-radar.md) |
| Call tools | Invoke a configured local program or an API, cloud, scheduler, or container client through an adapter | [Adapter guide](docs/binder-lane-round.md#run-tools-through-adapters) |
| Chain calls | Connect stage dependencies and pass checked files or directory bundles into downstream tools | [Controller guide](docs/binder-lane-round.md#prepare-a-controller-request) |
| Compare methods | Hold inputs and scoring fixed across toolchain arms; retain failed candidates in the comparison | [Binder comparison guide](docs/binder-lane-round.md), [scoring stack](tools/cofold-scoring-stack.md) |
| Add a tool | Supply an adapter with typed inputs and expected outputs, or use an installed platform skill | [Custom tools and routes](docs/binder-lane-round.md) |

## Start Here

| To | Start With |
| --- | --- |
| Give your agent a scientific task | [Structure Factory skill](skills/biosymphony-structure-factory/SKILL.md) and [example request](#hand-a-mission-to-an-agent) |
| Choose a tool or model | [Tool cards](tools/README.md) and [tool radar](docs/tool-and-skill-radar.md) |
| Call tools and connect stages | [Execution guide](docs/binder-lane-round.md) |
| Inspect the CLI locally | [Install and inspect](#inspect-or-run-the-repo-yourself) |

## How To Use This

Give your agent the [Structure Factory skill](skills/biosymphony-structure-factory/SKILL.md)
and describe the result you need.

```text
Use the BioSymphony Structure Factory skill.
Goal: <design candidates, predict structures, compare models, screen, or render>.
Inputs: <public accessions or synthetic fixtures>.
Tools: <choose from the knowledge base, or use these named tools>.
Workflow: <which tool outputs feed which later steps>.
Compute: <local tools, installed skills, or selected hosted services>.
Limits: <budget, runtime, candidate count, metric, and stopping rule>.
Results: <structures, score tables, candidate rankings, or figures>.
Check tool availability and input compatibility, then dry-run the toolchain.
Identify any missing adapter, installation, or authorization before execution.
```

The public CLI uses `bsf binder-lane adapter` for one tool call and
`bsf binder-lane execute` for a prepared adapter chain. Its `run` command
exercises the included synthetic fixture. Installed platform skills are called
by your agent, then checked against the declared stage outputs.

Obtain explicit human authorization before a paid provider start, non-public
upload, terms acceptance, or large or license-gated download. The approval
names the route, data posture, budget, runtime, and applicable terms.

## Hand A Mission To An Agent

> Use the Structure Factory skill to compare structure-prediction tools for public inputs. Read the tool cards, explain which methods fit the inputs, and configure separate prediction arms with the same review criteria. Connect prediction outputs to scoring and visualization. Return a comparison table, failed-input list, and selected figures. Dry-run the calls before execution.

[Use cases](docs/use-cases.md) includes requests for binder comparison,
state atlases, screening, and structure mapping.

## Workflow Stages

<p align="center">
  <img src="docs/assets/workflow-ladder.svg" width="560" alt="Example design workflow: prepare inputs, generate candidates, predict structures, score and filter, then review rankings and figures. Each stage consumes outputs from the preceding stage.">
</p>

Select tools and execution routes for the stages you need. The binder controller runs configured adapters in
dependency order and verifies file hashes and output counts before passing
results downstream. A failed tool or invalid handoff stops the remaining
stages and returns a failure record with next actions.

A tool card supplies method knowledge. A runnable adapter supplies the
command and input/output mapping for your installation. Check both when
building a chain; the [execution guide](docs/binder-lane-round.md) explains
how to resolve missing bindings and connect installed skills.

## When To Use This

Use Structure Factory when a scientific question needs several tools, a
comparison between methods, or an agent that can inspect and continue the
work. Choose the steps that answer the question: prediction and review,
design and scoring, screening, or structural visualization.

## What Users And Their Agents Can Run

Inspect command bindings with
`bsf binder-lane adapters`, then dry-run the selected adapter to check your
installation.

| Role | Example Tool Records | Output To Use Downstream |
| --- | --- | --- |
| Generate candidate structures | [RFdiffusion3](tools/rfdiffusion3.md), [Genie3](tools/genie3-peptides.md), [BindCraft2](tools/bindcraft2.md) | Candidate structures or designs |
| Design sequences | [ProteinMPNN](tools/proteinmpnn.md) | Sequences for selected backbones |
| Predict complexes | [Boltz](tools/boltz.md), [Chai](tools/chai.md), [ESMFold2](tools/esmfold2.md) | Predicted structures and confidence fields |
| Score and filter | [Cofold scoring stack](tools/cofold-scoring-stack.md), [refinement stack](tools/refinement-stack.md) | Per-tool scores, filter decisions, and failure rows |
| Review poses and screens | [PoseBusters](tools/posebusters.md), [MolPAL](tools/molpal.md) | Pose checks and selected screening candidates |
| Render structures | [ChimeraX](tools/chimerax-peptide-viz.md), [MolViewSpec](tools/molviewspec.md) | Structural figures and reusable molecular views |

The bundled execution registry includes command records for Boltz, ESMFold2
full/Fast, supplied-backbone input, and status and diversity filters. Other
tool records may need an installation-specific adapter or platform skill.
See [capabilities](docs/capabilities.md) for execution coverage and the
[tool radar](docs/tool-and-skill-radar.md) for dated research leads.

## Works With Your Stack

Use the Markdown skills with Codex, Claude Code, or another agent that reads
files and calls commands. Use `bsf` directly when you prefer a terminal.

A toolchain can mix local programs, hosted APIs, installed platform skills,
and compute on RunPod, FAL, Modal, Lambda Cloud, AWS, or SSH/HPC. Configure a
matching adapter or skill for each stage. [Provider profiles](docs/compute-backends.md)
record setup requirements; the selected route determines runtime availability.

Optional [task packs](packs/) let OpenAI's Symphony with Linear, GitHub Issues,
or another queue coordinate the same work.

## Inspect Or Run The Repo Yourself

Install the CLI and inspect tools and adapters. These commands run locally
without a GPU or provider account:

```bash
git clone https://github.com/BioSymphony/structure-factory.git
cd structure-factory
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

bsf doctor .
bsf binder-lane menu --workspace .
bsf binder-lane adapters --workspace .
bsf catalog . --format markdown
bsf validate examples/pd-l1-binder-design-public
```

Follow the [execution guide](docs/binder-lane-round.md) to bind inputs,
dry-run one adapter, or prepare and execute a chain. Planning and validation
need Python 3.10+; each scientific tool has its own runtime requirements.

<details>
<summary>Campaign scaffolding and optional tracker tasks</summary>

```bash
bsf scaffold-campaign .runtime/pd-l1-binder-demo \
  --campaign-id pd-l1-binder-demo \
  --target-label "PD-L1 public interface demo" \
  --public-accession "PDB:4ZQK" \
  --window "public PD-1/PD-L1 interface window"
bsf validate .runtime/pd-l1-binder-demo
bsf issue-dry-run examples/pd-l1-binder-design-public \
  --out .runtime/pd-l1-issues
```

The [workflow map](docs/workflow-map.md) and [agent harness guide](docs/agentic-biology-harness.md)
cover task dependencies and worker handoffs.

</details>

## Binder-Design Fast Path

The [PD-L1 example](examples/pd-l1-binder-design-public) includes a target
window for PDB `4ZQK`, generation and cofold plans, and a candidate ranking
schema. The [fast-path recipe](recipes/pd-l1-binder-design-fast-path.md) covers
local preparation. Verify coordinate inputs with `target-check --plan <plan.json>`
before a comparative generation run.

The [binder-lane skill](skills/binder-lane-round/SKILL.md) also supports an
independent comparison workflow based on [Anthropic's public report](https://www-cdn.anthropic.com/30bf50e22a01388bb29bf077ee3f244531594b7a.pdf)
and [released dataset](https://huggingface.co/datasets/Anthropic/claude-protein-binder-design).
Choose source-tool replay, workflow-shape replay, or deliberate tool swaps.

## Newcomer Resources

- [FAQ](docs/faq.md): GPUs, agents, trackers, and adding tools.
- [Glossary](docs/glossary.md): scientific and workflow terms.
- [Quickstart tour](docs/quickstart-tour.md): a local CLI walkthrough.
- [CLI reference](docs/cli-reference.md): commands and options.
- [Skill installation](docs/skill-install.md): agent setup.

<details>
<summary>Operations, repository layout, and release checks</summary>

Read the [preflight checklist](docs/preflight-checklist.md) before paid
execution. [Operational checks](docs/operational-gotchas.md) and
[output validation](docs/no-false-success-hardening.md) cover failed tools,
incomplete results, and cleanup.

| Directory | Contents |
| --- | --- |
| `tools/`, `references/` | Tool knowledge base, registries, and source records |
| `skills/`, `src/` | Agent instructions and the `bsf` CLI |
| `recipes/`, `examples/`, `demos/` | Workflows, fixtures, and curated examples |
| `campaigns/`, `modules/`, `schemas/` | Campaign definitions and reusable stage contracts |
| `runpod/`, `packs/`, `templates/` | Provider templates and optional task coordination |
| `scripts/`, `tests/`, `docs/` | Validators, tests, and guides |

Before publishing, follow [PUBLIC_RELEASE.md](PUBLIC_RELEASE.md) and run
`make public-switch-check`, then `make clean`. Keep credentials, private data,
provider logs, model weights, and generated structures in runtime storage.

</details>

## Status

Pre-alpha. Local checks cover planning, adapter execution, stage handoffs,
fixtures, and release scans. Scientific tool availability depends on the
configured installation or service. [NON_CLAIMS.md](NON_CLAIMS.md) and
[BIOSAFETY.md](BIOSAFETY.md) define the result boundaries.

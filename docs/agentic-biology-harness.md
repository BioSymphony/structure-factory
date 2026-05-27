# Agentic Biology Harness

Last reviewed: 2026-05-13

BioSymphony Structure Factory is a harness for long-running, agentic structural biology work. It is designed for scientists, computational biologists, and agent operators who need more than a script and less than an opaque automation platform.

The repo helps turn an open-ended biological request into a bounded work program:

```text
biological intent
  -> target window or structure set
  -> task plan
  -> agent lanes with owned paths
  -> RunPod or local/cloud execution profile
  -> artifacts, hashes, progress, and cleanup
  -> candidate ranking, reports, and figures
```

## What It Is For

Use Structure Factory when the useful work is bigger than one prompt:

- binder-design triage against a public target window
- Boltz, Genie/RFdiffusion-style generation setup, and cofold/model-comparison review
- CryoCore handoff, deposited PDB/EMDB structures, or structure-mapping planning
- GPCR or multimer state comparison with artifact provenance
- cloud GPU stage contracts that need budget, cleanup, and proof gates
- publication-style structural reports with explicit source posture and result boundaries
- Linear or similar tracker workflows where agents need durable scientific contracts

The repo is a control plane. It carries manifests, schemas, task packs, validators, stage contracts, launch templates, and compact public demos. Raw biological data, provider logs, private structures, model weights, credentials, and experimental conclusions live outside the repo in operator-controlled infrastructure.

## Drive Any Agent Stack

Structure Factory plugs into any orchestrator the user already runs: Codex, Claude Code, Symphony with Linear, a `/goal` command stack, GitHub Issues, Notion tasks, or any custom queue. The orchestrator decomposes goals, inspects files, picks local or cloud resources, and dispatches workers. Structure Factory provides the parts that are easy to lose in a long-horizon agent run:

- domain-specific intake defaults and run boundaries
- campaign manifests, stage contracts, expected artifacts, and provider profiles
- tracker-neutral task shapes with owned paths and validation commands
- local validators that catch privacy, launch, and false-success problems
- examples and recipes that show a capable agent where to start

When the contract, safety gates, and validation surface are present, an orchestrator can fill routine glue work directly. Reach for the repo's bespoke recipes for missions where the biology-specific shape matters.

For `/goal` style setups, the translation is:

```text
user goal
  -> Structure Factory skill
  -> campaign contract or existing example
  -> task pack or task queue when the work exceeds one turn
  -> local or provider prep gates
  -> checked outputs and reviewable closeout
```

## Public User Value

For a biology team, the useful promise is practical:

- a repeatable way to scope structural biology campaigns before spending GPU money
- tracker-neutral task packs that make agent work reviewable
- RunPod-ready stage contracts for the common "prepare, launch, watch, fetch, verify, cleanup" loop
- built-in run boundaries so computational candidates are not oversold
- candidate rankings and structure reports that a scientist can inspect, reject, or promote to the next experiment
- enough structure for Symphony, Codex, Claude-lane workers, or similar agents to collaborate without relying on chat history

The binder-design fast path compresses the setup loop. Target window, generation lanes, GPU plan, cofold ranking, report, and validation notes are scaffolded together. The output is reviewable computational triage. Binding, selectivity, efficacy, safety, and therapeutic relevance are confirmed through wet-lab and clinical processes downstream of the repo.

## Skill Surfaces

The repo exposes the harness in three public-friendly ways:

| Surface | Path | Purpose |
| --- | --- | --- |
| Agent instructions | `skills/biosymphony-structure-factory/SKILL.md` | Portable operating rules for agents and orchestration workers. |
| CLI gates | `src/biosymphony_structure_factory/cli.py` | Public audit, campaign validation, issue dry-run, and harness readiness checks. |

The skill is the recommended entry point for agents. The CLI is the guardrail that keeps examples, release posture, and the harness surface checkable.

## Symphony And Linear Role

Structure Factory works best as a BioSymphony sidecar:

- Symphony owns worker dispatch, bounded concurrency, wave review, and outcome parsing.
- Linear or a similar tracker owns durable issue contracts, state, dependencies, and comments.
- Structure Factory owns the domain-specific biological contract: inputs, lanes, result boundaries, provider profile, stage contract, expected artifacts, validation commands, and closeout notes.

The key label is:

```text
sym:structure-factory
```

Task packs should stay tracker-neutral enough to import into Linear, GitHub Issues, Notion tasks, or another queue. The public examples use Linear language because that is the current BioSymphony orchestration path, but the pattern is not locked to Linear.

Optional Claude-lane or visual-review workers fit as separate lanes. They can review figures, reports, or biological plausibility, but they should still close out with the same source posture, result boundary, validation summary, and artifact references.

## RunPod As Blessed Cloud Path

RunPod is the blessed first paid-pod path for Structure Factory because the repo carries public launch templates, stage contracts, scope checks, and Network Volume posture. Executable provider packets are generated outside public git after operator approval. Closeout still requires artifacts, hashes, cleanup proof, and validation notes.

The RunPod path preserves this verification flow:

```text
manifest
  -> input audit
  -> launch preflight
  -> stage-progress ledger
  -> expected artifacts
  -> artifact fetch and hashes
  -> cleanup proof
  -> contract self-check
  -> tracker closeout
```

Other providers are allowed when they satisfy the same contract:

- AWS Batch for cloud-scale or multi-shard GPU jobs
- SSH/HPC where institutional data or licenses must stay on site
- local high-resource workstations for prep, small runs, or GUI review
- generic cloud/neocloud pods when provider-specific cleanup and artifact export are proven

The default public docs should use placeholders and runtime-secret references. Public users can choose public base image plus runtime bootstrap, a dedicated RunPod Network Volume, a private image with registry auth, or an institutional runtime. The issue must declare the posture before launch.

## Canonical Workflow

1. **Intake**
   Define target, public accession or safe local reference, desired output, source posture, privacy posture, runtime constraints, and result boundaries.

2. **Contract**
   Create or update `campaign-manifest.json`, target-window file, stage contract, expected artifacts, and validation notes.

3. **Task Pack**
   Render tracker-neutral issues with owned paths, dependencies, validation commands, risk notes, operator gates, and `sym:structure-factory` routing.

4. **Preparation**
   Validate schemas, run public audit, check tool/license posture, and keep cost-bearing work in backlog until authorized.

5. **Execution**
   Use local prep for no-download checks. Use RunPod when a real remote GPU profile is selected and authorized. Emit progress, artifacts, and hashes.

6. **Closeout**
   Compare artifacts to the stage contract, label partial work honestly, attach result boundaries, and produce a candidate ranking or structure report.

## What Makes It Helpful

The repo lets agents move quickly because the load-bearing parts of a campaign are explicit and verifiable:

- target, data posture, and result boundaries are defined before compute runs
- provider launches close with artifact lists, hashes, and cleanup proof
- generated candidates carry provenance, confidence, and negative rows alongside the ranked output
- decisions land in durable manifests and issues that any worker can pick up

Agents that read these contracts can fan out across lanes, providers, and trackers with shared expectations.

## Public Release Minimum

A public release should pass:

```bash
make harness-check
make release-check
make secret-scan
```

`make harness-check` verifies that the public repo still exposes the skill, docs, task pack, RunPod posture, and orchestration entry points expected by BioSymphony users.

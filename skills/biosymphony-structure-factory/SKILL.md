---
name: biosymphony-structure-factory
description: Select structural biology tools, call configured adapters, chain stage outputs, and compare computational results. Use for binder-design comparisons, structure prediction, model review, and agent-driven execution.
---

# BioSymphony Structure Factory

Use the tool knowledge base to select methods for a target, accession, or
screening request. Call configured tools through the CLI or installed platform
skills, connect stage outputs, and compare structures and candidate rankings.

## Start with the requested outcome

Read `references/README.md`, `references/AGENTS.md`, and
`references/NON_CLAIMS.md`, then select the work:

| Request | Deliverable |
| --- | --- |
| Choose tools | Methods, input/output requirements, source references, and runtime options |
| Call and chain tools | Configured adapters, stage dependencies, and checked downstream inputs |
| Plan a campaign | Target definition, selected tools, and stage contracts |
| Demonstrate a workflow | Public or synthetic inputs with a labeled example report |
| Prepare GPU execution | Provider profile, resource limits, launch request, and validation commands |
| Review results | Candidate ranking or structure report with source files and validation results |
| Run a campaign | Authorized execution followed by artifact verification and resource cleanup |

For ambiguous inputs, tools, or spending limits, use
`references/docs/intake-interview.md` to resolve the missing decisions.
For a first campaign, use `references/docs/quickstart-tour.md`; find command
options in `references/docs/cli-reference.md`.

## Read the references for your task

| Task | References |
| --- | --- |
| Find methods | [Full tool index](https://github.com/BioSymphony/structure-factory/tree/main/tools), [software registry](https://github.com/BioSymphony/structure-factory/blob/main/references/software-registry.yaml), `references/docs/tool-and-skill-radar.md` |
| Select tools and compute | `references/docs/tooling-and-licensing.md`, `references/docs/compute-backends.md` |
| Plan binder comparisons | `references/docs/binder-lane-round.md`, `references/docs/binder-study-decision-loop.md` |
| Choose measured controls | `references/docs/binder-controls.md` |
| Use BindCraft2 | `references/tools/bindcraft2.md`: presets, resource limits, output tables, score scales, and license |
| Qualify Anthropic acceleration | `references/tools/anthropic-optimization-kits.md`: stock revision, runtime isolation, activation, and matched comparisons |
| Score or render predictions | `references/docs/confidence-sidecars.md` |
| Prepare provider execution | `references/docs/preflight-checklist.md`, `references/docs/operational-gotchas.md`; add `references/docs/runpod-stack.md` for RunPod |
| Coordinate workers | `references/docs/agentic-biology-harness.md`, `references/docs/linear-orchestration.md` |
| Define run completion checks | `references/docs/no-false-success-hardening.md`, `references/docs/agent-run-learnings.md` |
| Publish artifacts | `references/docs/public-export-shape.md` |

## Prepare a campaign

1. Record the target accession, chains, residue selections, input hashes, and
   permitted data use. For binders, include the target site and required controls.
2. Select generators, sequence designers, predictors, scorers, and filters.
   Check primary sources and record the review date, code revision, checkpoint,
   component terms, and intended use. Resolve discrepancies with tool cards.
3. Select the execution profile and setup method. Declare budget, runtime,
   downloads, network use, expected outputs, and cleanup.
4. Scaffold a campaign under `.runtime/` with `bsf scaffold-campaign`.
   Define stage dependencies, progress records, checkpoints, and partial outcomes.
5. Validate the campaign with `bsf validate`. For tracker work, use
   `bsf issue-dry-run <campaign> --out <directory>`.

For Symphony or Linear dispatch, use `sym:structure-factory`. Give each worker
owned paths, dependencies, expected artifacts, and validation commands. Record
the approval for cost-bearing or restricted execution in the task.

## Compare binder methods

Use `references/examples/pd-l1-binder-design-public/README.md` for an example.
For a comparison round:

1. Define candidate counts, predictor panel, filters, primary metric, controls,
   round limit, and stopping rule.
2. Inspect `references/published-binder-comparison-workflow.json` and
   `references/binder-execution-adapters.json`. Use
   `published_tool_identities` to check selected published tools or
   `published_workflow_shape` to preserve the workflow with replacements.
3. Materialize and preflight the plan. Run `bsf binder-lane target-check` on the
   coordinate input with `--plan` before generation.
4. Bind the target report and stage settings with `prepare-execution`.
   Resolve readiness errors, then dry-run the prepared request with
   `bsf binder-lane execute --dry-run`.
5. For remote execution, validate `remote-request` and `remote-receipt`.
   Supply the transport separately; `remote_dispatch.dispatch_remote_tool`
   is a Python API.
6. After output verification, use `closeout`, `calibrate-controls` for a measured
   primary metric, and `round-decision` to apply the stopping rule.

BindCraft2 requires its own adapter. For an accelerated tool, retain the
scientific model and checkpoint identity, and compare against its stock runtime
before using speed or numerical-equivalence claims.

## Execute and verify

Use `bsf binder-lane adapter` for one configured tool and `execute` for a
prepared adapter chain. The public `run` command exercises a synthetic fixture.
For each adapter handoff, name the source output and downstream input binding;
`execute` checks the files before it starts dependent stages. Call installed
platform skills through the agent and verify their declared outputs separately.


Before a real start, confirm that authorization covers the chosen route, input
data, budget, runtime, required terms, and downloads. Reuse an existing approval
when those conditions match. Add `--authorize-local-execution` only for the
approved start.

RunPod, AWS, FAL, Modal, Lambda Cloud, local, SSH/HPC, generic cloud, and neocloud
profiles use the same input, output, and cleanup requirements. Check installation
and service readiness for the selected adapter.

Count and parse required artifacts, check their hashes, retain stage events,
and verify resource cleanup. Record missing outputs and failed stages in the
report. Attach a source posture and result boundary to each closeout; use
`computational_candidate` for predictions pending independent validation.

Keep credentials, account identifiers, runtime logs, model weights, and
unpublished biological inputs and outputs in access-controlled runtime storage.
Use public accessions or synthetic fixtures in committed examples.

## Validate changes

For skill and harness changes, run:

```bash
make harness-check
make release-check
```

Before publication, run `make public-switch-check`. Its secret scan must run
successfully; a skipped scan leaves the release incomplete.

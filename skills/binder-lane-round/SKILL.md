---
name: binder-lane-round
description: Plan and execute protein-binder comparisons with selected tools, compute profiles, resource limits, controls, and output checks.
---

# Binder Lane Round

Compare binder-design methods against a fixed target and site. The CLI validates
plans and handoffs, runs synthetic examples, and executes authorized local
adapters with fixed arguments.

## Read first

Read `references/docs/binder-lane-round.md` for the contract,
`references/docs/binder-study-decision-loop.md` for study decisions, and
`references/docs/binder-controls.md` for measured calibration. Check
`references/docs/tooling-and-licensing.md` and
`references/docs/compute-backends.md` for the selected execution route.
`references/NON_CLAIMS.md` defines the scientific result boundaries.

For BindCraft2, read `references/tools/bindcraft2.md`. Its settings, output
layout, and deployment terms require a separate adapter from BindCraft.

## Define the comparison

Record the target accession, chains, residue selections, and input hashes.
Choose the generator, sequence designer, predictors, scorers, filters, and
execution route for each stage. Check code and checkpoint terms, API terms,
required downloads, and redistribution conditions.

Set the budget ceiling, runtime cap, round count, primary metric, stopping rule,
and controls. Declare output counts, formats, hashes, and cleanup requirements.
Comparison arms must share candidate counts, predictor panel, scorers, filters,
controls, and failure policy.

Use `reference_scope: published_tool_identities` to check the published tool
identities on selected stages. Use `published_workflow_shape` to compare
replacement tools within the same workflow. Identify replacements in each arm.
Record acceleration as a runtime choice attached to the model and checkpoint.

## Prepare and run

1. Inspect `bsf binder-lane menu`, validate the request with `plan-request`,
   and materialize the plan, round contract, and execution handoff with `plan`.
2. Run `preflight` and `target-check` against the plan and coordinate input.
   The `run` command executes only `public_synthetic_demo` plans.
3. Inspect bundled commands with `adapters`. For a missing command, supply a
   validated adapter registry under `.runtime/`.
4. Use `prepare-execution` with the target report and stage settings. Resolve
   each readiness error, then dry-run the adapter or controller.
5. For a remote route, validate `remote-request`, execute through the selected
   transport, and validate the exported artifacts and cleanup with `remote-receipt`.
6. Before a real start, confirm authorization for the route, data, budget,
   runtime, and required terms or downloads. Reuse approval that covers those
   conditions. Start the local adapter or controller with
   `--authorize-local-execution`. Add `--authorize-network` or
   `--authorize-license-gates` only when required and authorized.
7. Run `closeout` to count, parse, and hash the declared outputs.
8. For a measured primary metric, run `calibrate-controls`. Pass its ready
   record with `--calibration` to `round-decision`.
9. Apply `round-decision` to the sequential round history. Continue only when
   the decision is `continue` and the remaining budget covers another round.

## Commands

These examples use repository-relative paths. Materialize the required inputs
before running a command that reads them.

```bash
bsf binder-lane menu --workspace .
bsf binder-lane plan-request examples/pd-l1-binder-design-public/binder-round-request.json \
  --workspace . \
  --ledger references/binder-lane-capability-ledger.json \
  --out .runtime/pd-l1-binder-round/plan.json
bsf binder-lane plan .runtime/pd-l1-binder-round/plan.json \
  --workspace . \
  --out .runtime/pd-l1-binder-round/run
bsf binder-lane preflight --workspace . .runtime/pd-l1-binder-round/run
bsf binder-lane target-check .runtime/pd-l1-binder-round/target/target.cif \
  --workspace . --plan .runtime/pd-l1-binder-round/plan.json \
  --expected-sequence-file .runtime/pd-l1-binder-round/target/expected-sequence.txt \
  --sequence-basis entity --out .runtime/pd-l1-binder-round/target/verification.json
bsf binder-lane run --workspace . .runtime/pd-l1-binder-round/run
bsf binder-lane report --workspace . .runtime/pd-l1-binder-round/run
bsf binder-lane calibrate-controls examples/binder-controls-synthetic/control-panel.json \
  --workspace . \
  --observations examples/binder-controls-synthetic/control-observations.jsonl \
  --out .runtime/pd-l1-binder-round/control-calibration.json
bsf binder-lane round-decision .runtime/pd-l1-binder-round/plan.json \
  --workspace . --history .runtime/pd-l1-binder-round/round-history.json \
  --out .runtime/pd-l1-binder-round/round-decision.json
bsf binder-lane adapters --workspace .
bsf binder-lane adapter boltz-local-v1 --workspace . \
  --run-root .runtime/pd-l1-binder-round/boltz --operation readiness --dry-run
bsf binder-lane prepare-execution .runtime/pd-l1-binder-round/plan.json \
  --workspace . \
  --target-report .runtime/pd-l1-binder-round/target/verification.json \
  --stage-settings .runtime/pd-l1-binder-round/stage-settings.json \
  --out .runtime/pd-l1-binder-round/controller-request.json \
  --readiness-out .runtime/pd-l1-binder-round/execution-readiness.json
bsf binder-lane execute .runtime/pd-l1-binder-round/controller-request.json \
  --workspace . --plan .runtime/pd-l1-binder-round/plan.json \
  --run-root .runtime/pd-l1-binder-round/execution --dry-run
bsf binder-lane remote-request .runtime/pd-l1-binder-round/cofold/request.json \
  --workspace . --out .runtime/pd-l1-binder-round/cofold/validated-request.json
bsf binder-lane remote-receipt .runtime/pd-l1-binder-round/cofold/receipt.json \
  --request .runtime/pd-l1-binder-round/cofold/validated-request.json --workspace .
```

## Adapter and output requirements

A bundled command, an installed tool, and a ready service are separate checks.
Accept a selected tool or backend when its adapter satisfies fixed arguments,
typed bindings, path containment, and output requirements. Record license
acceptance separately from the plan's requested license gates.

Keep custom adapter registries, runtime bindings, receipts, logs, and actual
spend under `.runtime/`. Store credentials and unpublished biological data in
access-controlled storage.

Report synthetic examples as `public_synthetic_demo` and predicted designs as
`computational_candidate`. Record incomplete outputs before comparing rounds.

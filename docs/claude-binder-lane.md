# Claude Binder Lane

Use this Structure Factory lane with Claude Code to plan and review a bounded
protein-binder comparison. The same public skill and CLI also work with Codex
or another agent that can read files and run commands. The lane uses
[Anthropic's released binder workflow](../references/published-binder-comparison-workflow.json)
as a comparison reference and keeps each new campaign's target, tools, controls,
execution route, and results explicit.

## Start with a public example

Read the [binder-lane-round skill](../skills/binder-lane-round/SKILL.md), then
give your agent this request:

```text
Use the BioSymphony Structure Factory binder-lane-round skill. Start with the
public PD-L1 example. Compare binder toolchains under one target, site, control
set, predictor panel, scoring policy, and failure policy. Show the selected
tools and their adapter readiness. Validate and preflight the plan, then run
the synthetic fixture and report its checked outputs. Keep generated files in
.runtime/.
```

From the repository root, the local entry sequence is:

```bash
bsf binder-lane menu --workspace .
bsf binder-lane adapters --workspace .
bsf binder-lane plan-request \
  examples/pd-l1-binder-design-public/binder-round-request.json \
  --workspace . \
  --ledger references/binder-lane-capability-ledger.json \
  --out .runtime/pd-l1-binder-round/plan.json
bsf binder-lane plan .runtime/pd-l1-binder-round/plan.json \
  --workspace . --out .runtime/pd-l1-binder-round/run
bsf binder-lane preflight --workspace . .runtime/pd-l1-binder-round/run
bsf binder-lane run --workspace . .runtime/pd-l1-binder-round/run
bsf binder-lane report --workspace . .runtime/pd-l1-binder-round/run
```

This example has the `public_synthetic_demo` result boundary. The
[round guide](binder-lane-round.md) covers target verification, adapter calls,
checked stage handoffs, remote request contracts, control calibration, and
closeout for a selected toolchain.

## Define a comparison

The campaign request records the scientific choices. The plan resolves tools
and routes. Adapters bind those choices to runnable commands or service
clients. Keep these records separate so a tool can change without silently
changing the target, controls, metrics, or result boundary.

1. **Target and site:** choose a public accession, construct, chain, residue
   selection, and coordinate source. Confirm the deposited entity describes the
   intended molecule. Run `target-check` on the exact coordinate file selected
   for generation.
2. **Study mode:** choose a source-tool replay, a workflow-shape replay, or a
   declared tool swap. The
   [pinned reference](../references/published-binder-comparison-workflow.json)
   records the published tool identities and stages.
3. **Toolchains:** assign generators, sequence designers, predictors, scorers,
   and filters to each arm. For a controlled generation comparison, hold
   candidate counts, predictor panel, scoring, filters, controls, and failure
   policy fixed across arms.
4. **Readiness:** inspect the
   [capability ledger](../references/binder-lane-capability-ledger.json),
   `bsf binder-lane adapters`, and the selected runtime. A listed tool, a
   documented method, a bound adapter, and a ready installation are distinct
   observations.
5. **Results:** retain failed candidates and missing scores, pair each score
   with its model, checkpoint, seed, structure, and confidence sidecar, and
   calibrate a threshold against declared controls when the comparison needs
   one. Count, parse, and hash required outputs before closing a stage.

Use the [decision loop](binder-study-decision-loop.md) to set a finite round
count, budget, primary metric, and stopping rule. Use
[scoring invariants](scoring-invariants.md) and
[control calibration](binder-controls.md) when interpreting the ranking.

## Public result record

Keep a reviewable campaign contract, source posture, stage status, artifact
counts and hashes, and validation notes. The repository includes compact
public or synthetic fixtures; generated candidates and execution records stay
in ignored runtime storage. Label predictions `computational_candidate` after
their declared closeout checks pass. See [result boundaries](../NON_CLAIMS.md)
and [release rules](../PUBLIC_RELEASE.md).

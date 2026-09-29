# Prediction Handoff Contract

Use this checklist to connect design, prediction, rescoring, and closeout.
Keep the campaign identity across phases and store execution records below
the campaign's runtime directory.

## Inputs and prediction identity

- Record the target construct, chain, residue window, site mapping, and input
  file hashes before prediction.
- Record the predictor, model or checkpoint revision, runtime route, seed,
  sample index, and scoring mode for each prediction.
- Declare the MSA posture: query-only, supplied alignment, or remote search.
  Record separate paired and unpaired alignment hashes when both are used.
  Query-only is explicit; missing provenance is incomplete. Recheck supplied
  input hashes before dispatch.
- Carry candidate and parent-pose identities through sequence design and
  rescoring. Each sequence row identifies its generating stage and parent.

## Admission and recovery

- Keep one campaign authorization identity and total ceiling across design
  and rescoring. A new phase does not reset the spend ledger.
- Compare the effective provider, operation, and runtime route with the
  approved plan immediately before dispatch.
- Reserve each attempt before creating provider work. Reconcile costs for
  failed and uncertain attempts before calculating remaining capacity.
- Require a smoke receipt for every target and predictor arm before scaling.
  Match its input hashes, model, MSA posture, and scoring mode to that arm.
  Parse the structure and required confidence sidecars.
- Recover an uncertain submission by its existing attempt identity. Verify
  artifact export, cost, and cleanup before resolving the attempt.

The Python `dispatch_remote_tool` helper writes
`remote-dispatch-pending.json` before invoking its adapter. An exception,
invalid adapter result, process interruption, or unverified cleanup leaves that
record in place. Another call using the same attempt directory is blocked
before adapter invocation. Recover the provider work and retain its evidence
before resolving the pending record. A validated receipt with verified
cleanup clears the record. Dry runs do not claim an attempt.

Remote request validation requires finite positive per-attempt spend and
runtime caps. Track the campaign's cumulative reservations and spend separately.
A completed receipt with a reported cost must stay within its request's
spend cap. A failed receipt retains over-cap spend as cost evidence.

## Result handoff

- Report attempted trajectories, emitted candidates, refolded candidates,
  accepted candidates, distinct families, and selected candidates separately.
- Record score definitions, directions, reducers, chain ordering, and model
  provenance. Compare thresholds within their recorded calibration scope.
- Verify nonempty artifacts, hashes, required sidecars, and expected counts.
  Complete a stage after its output checks pass.
- Carry reported cost and verified cleanup into closeout.

Use the [round guide](binder-lane-round.md) for runnable adapter contracts and
[control calibration](binder-controls.md) for ranking provenance.

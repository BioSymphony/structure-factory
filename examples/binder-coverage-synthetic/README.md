# Synthetic Candidate Coverage

This example checks two candidates across two stages. One candidate completes
both stages. A synthetic input rejection excludes the second candidate from
the downstream assessment. No model runs or biological results are included.

`protocol.json` supplies the protocol digest, and `evidence.json` supplies the
compact synthetic evidence referenced by `observations.json`. `contract.json`
declares the pool, stage dependencies, and rejection rule.

Run the command in the [candidate coverage guide](../../docs/candidate-coverage.md).

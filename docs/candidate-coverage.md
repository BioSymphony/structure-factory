# Candidate Coverage

Use `bsf binder-lane coverage-check` to account for every declared candidate
and required stage before closing a comparison. The command reads a contract,
observations, and evidence files. It writes a JSON report to standard output
without changing those files.

## Declare The Pool And Stages

Freeze a [coverage contract](../schemas/candidate-coverage.schema.json) before
assessment. It contains unique `candidate_ids` and ordered `stages`. Each stage
declares its `stage_id`, `protocol_sha256`, direct `depends_on` stages, and
`rejection_rules` with IDs and scientific descriptions. List dependencies before
their downstream stages. Preserve the protocol snapshot used to compute each
digest.

The [observations](../schemas/candidate-observations.schema.json) name the
contract's SHA-256 and contain one row per observed candidate-stage pair.
Compute the contract digest over UTF-8 JSON with sorted keys, compact separators,
ASCII escaping, and no nonfinite numbers; the Python API exposes
`candidate_coverage.contract_digest` for this operation. Changing the pool,
protocol, dependencies, or rules changes the digest and requires new observations.

## Record Outcomes

| Status | Required Evidence | Completion Effect |
| --- | --- | --- |
| `completed` | Nonempty files with matching SHA-256 values; all dependencies completed | Resolves the stage |
| `scientifically_rejected` | A predeclared stage `rule_id`, nonempty evidence, and completed dependencies | Resolves the stage as excluded |
| `upstream_excluded` | `upstream_stage_id` naming a direct dependency with a scientific rejection or an established upstream exclusion | Resolves the downstream exclusion |
| `pending` | Evidence optional | Leaves the comparison unfinished |
| `missing` | Evidence optional; omitted pairs also count as missing | Leaves the comparison unfinished |
| `failed` | Evidence optional | Leaves the comparison unfinished |

Evidence paths are relative to `--evidence-root`. The check rejects missing,
empty, changed, or symlinked evidence files and paths outside that root.
Duplicate rows, unknown candidates or stages, changed protocols, and undeclared
rejection rules are invalid. A failed or pending dependency cannot justify a
scientific exclusion. Capacity limits leave work unfinished.

The report separates `fully_assessed_candidate_ids`, `excluded_candidate_ids`,
and `unfinished_candidate_ids`. `valid` describes the records and evidence;
`complete` additionally requires every candidate-stage pair to resolve.
Candidates with invalid evidence or dependencies remain in the unfinished
population. Status counts retain the declared row states. Exit status is 0 for complete
coverage, 1 for incomplete or invalid evidence, and 2 for malformed declarations
or unreadable inputs.

## Check A Synthetic Example

```bash
bsf binder-lane coverage-check examples/binder-coverage-synthetic/contract.json \
  --observations examples/binder-coverage-synthetic/observations.json \
  --evidence-root examples/binder-coverage-synthetic
```

The example resolves four pairs: one candidate completes both stages, and
another is rejected at the first stage and excluded from the second. It contains
synthetic status records, with no model execution.

Coverage verifies declared identities, dependencies, and evidence hashes. It
does not interpret scientific evidence or qualify rejection thresholds. Use
[filter qualification](binder-filter-qualification.md) and the relevant
prediction artifact checks for those decisions. The existing artifact
`closeout` command checks file inventory; run this coverage check separately
for the complete comparison.

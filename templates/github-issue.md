# Structure Factory Public Issue

This template is a public campaign request, not a full Linear/Symphony worker contract. Use [`templates/linear-issue.md`](linear-issue.md) when an agent worker needs provider fields, stage/progress contracts, dependencies, and closeout evidence.

## Summary

Describe the public-safe structural biology task.

## Campaign

- campaign ID:
- mode: `binder-design | model-jury | structure-dossier | screening | provider-prep`
- routing label: `sym:structure-factory`
- claim ceiling: `planning | public_demo | computational_candidate`
- operator gate required before execution: `yes | no`

## Public Inputs

- target:
- public accession:
- target window or scope:
- privacy posture: `public_or_synthetic_only`

Do not include private sequences, unpublished structures, raw data, provider IDs, credentials, private paths, or private tracker URLs.

## Expected Artifacts

- `campaign-manifest.json`
- `target-window-dossier.json`
- `stage-contract.json`
- `claim-ledger.md`

## Acceptance Criteria

- [ ] Inputs are public accessions or synthetic fixtures.
- [ ] Stage contract fails closed on missing or unverifiable artifacts.
- [ ] Claims are capped to the evidence present.
- [ ] No wet-lab, clinical, therapeutic, safety, efficacy, or binding proof is claimed.

## Validation Commands

```bash
bsf validate examples/<campaign-id>
bsf audit .
make release-check
```

## Risk Notes

- GPU, provider, license-gated, or cost-bearing work requires a separate operator gate.
- Public launch templates are non-launchable until a private/operator-gated runtime packet is prepared.

<!-- symphony:schema
schema_version: 1
subgroup: structure-factory
routing_label: sym:structure-factory
-->

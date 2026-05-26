# BSF-BINDER-W00: Target Window And Claim Contract

## Summary

Prepare one public-safe slice of `pd-l1-binder-design-public` for agent execution, review, or tracker import. This draft is provider-neutral until an operator explicitly authorizes local, cloud, or RunPod execution.

## Inputs

- campaign ID: `pd-l1-binder-design-public`
- subgroup: `structure-factory`
- routing label: `sym:structure-factory`
- target: `PD-L1 target window`
- public accession: `PDB:4ZQK`
- target window: `19-127`
- claim ceiling: `computational_candidate`

## Expected Artifacts

- `examples/pd-l1-binder-design-public/target-window-dossier.json`
- `examples/pd-l1-binder-design-public/stage-contract.json`
- `examples/pd-l1-binder-design-public/candidate-jury.example.json`
- `examples/pd-l1-binder-design-public/claim-ledger.md`

## Stage / Progress Contract

- stage contract: `examples/pd-l1-binder-design-public/stage-contract.json`
- artifact granularity: `per-campaign`
- progress ledger: `.runtime/pd-l1-binder-design-public/BSF-BINDER-W00/stage-progress.jsonl`
- resume command: `PYTHONPATH=src python3 -m biosymphony_structure_factory.cli validate examples/pd-l1-binder-design-public`
- partial success policy: blocked, failed, or incomplete lanes must downgrade the final outcome instead of claiming success.

## Provider / Execution Profile

- provider: `provider-neutral`
- execution profile: `other`
- setup posture: `n/a`
- writable volume/env: `n/a`
- operator gate required: `no`

## Tooling / License Posture

- tools: `Structure Factory public CLI`
- posture: `open-default`
- current primary source checked: `no external install required for this dry-run draft`
- intended use context: `public planning`
- image/runtime action: `n/a`
- operator action required: `none for planning; explicit authorization before paid cloud execution`

## Acceptance Criteria

- [ ] Target accession and residue window are explicit.
- [ ] Claim ceiling is computational candidate.
- [ ] No private data is referenced.

## Validation Commands

```bash
PYTHONPATH=src python3 -m biosymphony_structure_factory.cli validate examples/pd-l1-binder-design-public
PYTHONPATH=src python3 -m biosymphony_structure_factory.cli audit .
```

## Final Outcome Contract

- worker lane: `codex`
- closeout state: `In Review`
- final comment must include: `<!-- symphony-outcome -->`
- evidence mode: `report_only`
- claim level: `planning`
- artifact packet: `.runtime/pd-l1-binder-design-public/BSF-BINDER-W00`
- hash ledger: `n/a`
- cost report: `n/a`
- cleanup proof: `n/a`
- success requires: validation commands pass and any provider execution remains separately authorized.

## Touched Areas

- `examples/pd-l1-binder-design-public/campaign-manifest.json` - owned by this issue
- `examples/pd-l1-binder-design-public/target-window-dossier.json` - owned by this issue
- `examples/pd-l1-binder-design-public/claim-ledger.md` - owned by this issue

## Dependencies

Blocked by: none

## Risk Notes

- Computational candidate evidence only.
- No wet-lab, binding, therapeutic, safety, or clinical claims.
- GPU execution requires separate operator authorization, budget, cleanup policy, and runtime license/use-context review.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: structure-factory
campaign_id: pd-l1-binder-design-public
routing_label: sym:structure-factory
issue_id: BSF-BINDER-W00
touched_areas:
  - examples/pd-l1-binder-design-public/campaign-manifest.json
  - examples/pd-l1-binder-design-public/target-window-dossier.json
  - examples/pd-l1-binder-design-public/claim-ledger.md
complexity: medium
claim_ceiling: computational_candidate
-->

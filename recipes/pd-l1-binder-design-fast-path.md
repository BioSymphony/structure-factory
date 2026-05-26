# PD-L1 Binder-Design Fast Path

Use this when you want a public-safe binder-design campaign scaffold from a deposited structure or public target window.

## Prerequisites

- local install completed with `python -m pip install -e .`
- public target evidence only
- no generated coordinates, sequences, provider logs, or credentials in git

## Copyable Agent Prompt

```text
Use the BioSymphony Structure Factory skill. Review examples/pd-l1-binder-design-public as a public PD-L1 binder-design fast path. Check the target-window dossier, stage contract, candidate jury example, issue plan, and claim ledger. Keep the claim ceiling at computational_candidate and do not launch remote compute.
```

## Commands

```bash
bsf validate examples/pd-l1-binder-design-public
bsf issue-dry-run examples/pd-l1-binder-design-public --out .runtime/pd-l1-issues
bsf audit .
```

Expected success:

- validation returns `"ok": true`
- `.runtime/pd-l1-issues/` contains tracker-neutral issue drafts
- `bsf audit .` reports zero findings

## Files To Inspect

- `examples/pd-l1-binder-design-public/campaign-manifest.json`
- `examples/pd-l1-binder-design-public/target-window-dossier.json`
- `examples/pd-l1-binder-design-public/stage-contract.json`
- `examples/pd-l1-binder-design-public/candidate-jury.example.json`
- `examples/pd-l1-binder-design-public/claim-ledger.md`

Review:

- target accession and residue window
- hotspot rationale and uncertainty
- generation lane runtime gates
- cofold/model-jury expected artifacts
- candidate jury claim ceiling
- non-claims in `claim-ledger.md`

## Done Criteria

- issue drafts name owned paths, acceptance criteria, validation commands, and non-claims
- every candidate remains `computational_candidate`
- any missing optional evidence is marked blocked or insufficient evidence

## Blocked Or Degraded Criteria

Mark the run blocked or degraded if inputs are not public, target-window evidence is unclear, a tool lane requires unapproved licensing/runtime access, or the audit reports any finding.

Do not commit generated coordinates, generated sequences, private notes, provider logs, or model weights. Keep every candidate at computational-candidate evidence until external validation exists.

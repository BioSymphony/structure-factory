# PD-L1 Binder Design Public Example

The headline Structure Factory example. A public-safe binder-design campaign against the PD-1/PD-L1 interface, ready for an agent to read and extend.

## Scope

- target: human PD-L1 public structure context
- public accession: PDB `4ZQK`
- target window: chain A residues 19-127
- workflow: generation-lane planning plus cofold and jury triage
- claim ceiling: `computational_candidate`

## What This Folder Contains

- `campaign-manifest.json`. Top-level campaign description: target, lanes, expected artifacts, claim ceiling.
- `target-window-dossier.json`. Accession, chain or window, uncertainty notes, and hotspot evidence for the PD-L1 interface.
- `stage-contract.json`. The fail-closed sequence of stages a provider run would follow.
- `candidate-jury.example.json`. Example shape of a ranked candidate jury output.
- `claim-ledger.md`. The kind of claim-bounded closeout an agent should produce.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill. Review examples/pd-l1-binder-design-public as a binder-design campaign. Explain the target window, generation and cofold lanes, expected artifacts, and claim ceiling. Then propose how you would scaffold a similar campaign against a different public PD-L1 structure.
```

## Inspect Or Run Locally

```bash
bsf validate examples/pd-l1-binder-design-public
bsf issue-dry-run examples/pd-l1-binder-design-public --out .runtime/pd-l1-issues
```

The first command checks the manifest, dossier, and stage contract. The second generates tracker-neutral issue drafts under `.runtime/pd-l1-issues/` ready for Linear, GitHub Issues, Notion, or any queue.

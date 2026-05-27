# PD-L1 Binder Design Example

The headline Structure Factory example: a binder-design campaign against the PD-1/PD-L1 interface, ready for an agent to read and extend.

## Scope

- target: human PD-L1 public structure context
- public accession: PDB `4ZQK`
- target window: chain A residues 19-127
- workflow: generation-lane planning plus cofold triage and candidate ranking
- result boundary: `computational_candidate`

## What This Folder Contains

- `campaign-manifest.json`. Top-level campaign description: target, lanes, expected artifacts, and run boundaries.
- `target-window.json`. Accession, chain or window, uncertainty notes, and hotspot plan for the PD-L1 interface.
- `stage-contract.json`. The fail-closed sequence of stages a provider run would follow.
- `candidate-ranking.example.json`. Example shape of a ranked candidate output.
- `validation-notes.md`. Statements that are allowed, blocked, or require later validation.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill. Review examples/pd-l1-binder-design-public as a binder-design campaign. Explain the target window, generation lanes, cofold checks, candidate ranking, expected artifacts, and run boundaries. Then propose how you would scaffold a similar campaign against a different public PD-L1 structure.
```

## Inspect Or Run Locally

```bash
bsf validate examples/pd-l1-binder-design-public
bsf issue-dry-run examples/pd-l1-binder-design-public --out .runtime/pd-l1-issues
```

The first command checks the manifest, target window, and stage contract. The second generates tracker-neutral task drafts under `.runtime/pd-l1-issues/` ready for Linear, GitHub Issues, Notion, or any queue.

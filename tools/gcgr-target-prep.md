# GCGR Target Prep

## Purpose

Show the target-prep card pattern for a public GPCR target: select deposited structures, define chains and residue windows, identify public hotspots, and emit a manifest for downstream design lanes.

## Public-Safe Status

Public scaffold: yes. Use public deposited structures and public sequence metadata only.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill with the GCGR Target Prep tool card. Using public PDB structures of the glucagon receptor, build a target-window dossier with chain mapping, residue numbering, hotspots, and the downstream design and cofold handoff.
```

## Typical Inputs

- Public PDB or EMDB accessions.
- Target chain and residue numbering.
- Ligand or interface contact context.
- Exclusion list for private or unpublished data.

## Typical Outputs

- Target-window dossier.
- Hotspot and extended residue lists.
- Structure subset instructions.
- Claim ledger stating that target prep is not activity validation.

## Gates

- Record exact accession, chain, residue numbering, and extraction rules.
- Do not store raw maps or generated structure subsets in git.
- Treat ambiguous residues or unresolved loops as risk notes, not hidden assumptions.
- Verify the deposited structure's resolved range against SIFTS and check recent depositions in the PDB for the same target — a newer entry may resolve a domain that was disordered in the deposition you started from. Record the chosen accession + retrieval date in the candidate jury.

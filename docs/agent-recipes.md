# Public-Safe Agent Recipes

These recipes are promptable workflows for agents using the Structure Factory skill. They are designed to be useful without private infrastructure and strict enough to avoid accidental secrets, private data, or inflated biological claims.

For copyable end-to-end prompts, see [`docs/use-cases.md`](use-cases.md).
For detailed claim/evidence rules and legacy schema translations, see [`docs/claim-and-evidence.md`](claim-and-evidence.md).

## Exact Evidence Values

Use the schema enum values in manifests, issue packs, and closeouts. A friendly label is fine in prose, but the exact value should stay visible.

| Friendly Label | Exact Value | Use |
| --- | --- | --- |
| Planning | `planning` | Scaffolds, provider prep, and issue design before evidence exists |
| Public demo | `public_demo` | Public deposited data demonstration |
| Public synthetic demo | `public_synthetic_demo` | Synthetic fixture or generated demo data |
| Computational candidate | `computational_candidate` | Candidate ranking or triage that still needs external validation |
| Blocked | `blocked` | A lane could not proceed |
| Insufficient evidence | `insufficient_evidence` | Evidence does not support the requested claim |

If you see older machine values such as `candidate`, `processed`, `fixture_or_demo`, `validated`, or `publishable` in schema-level artifacts, translate them through [`claim-and-evidence.md`](claim-and-evidence.md) before writing public prose or a final closeout.

## Recipe: Scaffold A Campaign

Use when a user has a public target or synthetic fixture and wants a structured work plan.

```bash
bsf scaffold-campaign .runtime/<campaign-id> \
  --campaign-id <campaign-id> \
  --target-label "<target name>" \
  --public-accession "<PDB/EMDB/UniProt/synthetic fixture>" \
  --window "<residue, domain, interface, or state window>" \
  --mode binder-design
```

Agent checklist:

- keep the scaffold in `.runtime/` until public inputs are reviewed
- set a claim ceiling before suggesting tool lanes
- use public accessions or synthetic fixtures only
- add an operator gate before any GPU, cloud, or license-gated step
- run `bsf validate` and `bsf audit .`

## Recipe: Binder-Design Fast Path

Use when the user asks for binder design from a public structure.

1. Create or validate `campaign-manifest.json`.
2. Write a target-window dossier with public accession, chain/window, hotspot evidence, and uncertainty.
3. Declare generation lanes and cofold/model-jury lanes.
4. Add expected artifacts and a fail-closed stage contract.
5. Render tracker-neutral issues with `bsf issue-dry-run`.
6. Keep candidate juries at `computational_candidate` claim ceiling.

Never claim binding, inhibition, safety, selectivity, efficacy, or therapeutic value.

## Recipe: GPCR Or Multimer State Atlas

Use when the user asks for activation states, receptor-state comparison, multimer-state evidence, or switch analysis.

1. Declare the receptor/state matrix and public accessions.
2. Split work into deposited-structure, prediction, alignment, render, and synthesis lanes.
3. Use issue waves so each receptor/state shard has owned paths and validation commands.
4. Keep prediction and render outputs in ignored/provider storage until summarized.
5. Cap prediction-only conclusions at `computational_candidate`.

Good public artifacts include wave plans, issue drafts, provider contracts, accession tables, stage contracts, and report outlines.

## Recipe: Model Jury Or Structure Dossier

Use when the user has existing public model/map/structure evidence and wants review.

1. Identify public accessions and allowed local references.
2. Declare evidence mode for every artifact.
3. Separate provider-native evidence from derived local summaries.
4. Record missing optional tools as evidence, not failure.
5. Produce a dossier with negative rows and uncertainty.

If the request starts from raw cryo-EM movies, EMPIAR subset processing, RELION/CryoSPARC reconstruction, or map-to-model build execution, create a CryoCore handoff contract. Do not present those lanes as Structure Factory-owned work.

## Recipe: Provider Prep Without Launch

Use when the user wants RunPod, cloud, HPC, or local GPU readiness but has not authorized execution.

1. Create provider-neutral stage contracts and launch templates.
2. Use placeholders for registry auth, volume IDs, placement, and credentials.
3. Run scope and preflight checks.
4. Mark templates non-launchable until operator authorization exists.
5. Store live provider packets outside public git.

## Agent Closeout

Every agent closeout should include:

- files changed
- validation commands run
- evidence mode
- claim level
- privacy/security checks
- anything blocked, partial, or intentionally not launched

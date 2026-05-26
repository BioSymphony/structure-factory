# PDB/EMDB Evidence Dossier Public Data

Use this for a public PDB/EMDB dossier plan.

## Prerequisites

- public accession only
- local scaffold path under `.runtime/`
- no raw movie, large map, or generated model committed to git

## Copyable Agent Prompt

```text
Use the BioSymphony Structure Factory skill. Create a public PDB/EMDB evidence dossier plan from a deposited accession. Include provenance, expected artifacts, validation commands, figure/report outline, downgrade criteria, and non-claims. If raw cryo-EM processing is requested, create a CryoCore handoff contract instead. Do not download raw data or launch remote compute.
```

## Commands

```bash
bsf scaffold-campaign .runtime/map-model-demo \
  --campaign-id map-model-demo \
  --target-label "Public PDB/EMDB evidence target" \
  --public-accession "PDB:9ASJ / EMD-43816" \
  --window "public deposited evidence validation scope" \
  --mode structure-dossier

bsf validate .runtime/map-model-demo
bsf audit .
```

Expected success:

- scaffold command writes a campaign manifest, target dossier, stage contract, claim ledger, and README
- validation returns `"ok": true`
- audit reports zero findings

## Files To Inspect

- `.runtime/map-model-demo/campaign-manifest.json`
- `.runtime/map-model-demo/target-window-dossier.json`
- `.runtime/map-model-demo/stage-contract.json`
- `.runtime/map-model-demo/claim-ledger.md`

The dossier should separate:

- public accession metadata
- downloaded public files and hashes
- derived summaries
- validation limitations
- optional renderer/tool gates
- claim ledger

## Done Criteria

- claim level is `public_demo` or lower until evidence exists
- expected artifacts distinguish metadata, public downloaded files, derived summaries, and validation notes
- optional renderer or model-building tools remain gated until runtime context is reviewed

## Blocked Or Degraded Criteria

Mark the run blocked or degraded if accessions are ambiguous, files are too large for git, validation artifacts are missing, or a user asks for unsupported density interpretation as a fact.

Do not store raw movies, large map files, private structures, or validation PDFs in git.

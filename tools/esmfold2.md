# ESMFold2

## Purpose

Plan ESMFold2 structure-prediction and foldability lanes for public or
operator-approved biomolecular inputs. In Structure Factory this is a
prediction and uncertainty lane, not a standalone proof of binding, function,
or therapeutic value.

## Public-Safe Status

Public scaffold: yes. Runtime use requires current primary-source review of
the Biohub `esm` source, Hugging Face model weights, third-party notices,
intended use context, provider budget, and cleanup policy.

## Model Routes

The public docs expose two relevant local-weight model routes:

- `biohub/ESMFold2`: full ESMFold2 model.
- `biohub/ESMFold2-Fast`: first canary route for fast single-sequence or
  small-complex checks.

The Biohub Platform API is a separate optional route. Public docs may link it
so agents know it exists, but the Structure Factory cloud lesson captured here
uses the Hugging Face weights route, not the Biohub API. API use requires an
`ESM_API_KEY` or equivalent runtime secret, terms review, cost posture, and a
separate closeout.

## When To Use

- Fast foldability triage for known public proteins or existing generated
  candidates.
- Independent structure/uncertainty evidence alongside Boltz, Chai, and
  deposited references.
- Small public protein-protein, protein-DNA/RNA, or CCD-coded ligand canaries
  after the fast monomer canary passes.
- Visualization/report lanes that make pLDDT, PAE, and low-confidence regions
  visible to reviewers.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill with the ESMFold2 tool card. Start
with the ESMFold2 no-download toolcheck and do not run paid cloud compute,
download weights, call the Biohub API, or infer private sequences until the
operator gate records budget, runtime, data posture, expected artifacts, and
cleanup. Prefer the Hugging Face weights route for the first provider canary;
record the Biohub API as optional/deferred.
```

## Typical Inputs

- Public protein sequence, public accession-derived sequence, or synthetic
  fixture sequence.
- Structured chain manifest for protein, DNA, RNA, or CCD-coded ligand inputs.
- Optional public reference structure for RMSD/TM-style comparison.
- Runtime cache declaration for Hugging Face weights.

## Typical Outputs

- `prediction.cif` or an explicit blocked/partial artifact.
- `confidence_summary.json` with pLDDT, PAE, pTM, ipTM, and per-chain metrics
  when emitted by the route.
- `validation/structure_validation.json` proving a non-empty parseable mmCIF.
- `validation/weights_manifest.json` when model weights are materialized.
- `stage-progress.jsonl`, `executed-commands.jsonl`, `methods.md`,
  `provenance.md`, `claim_ledger.json`, and `artifact_index.json`.
- Optional viewer HTML, pLDDT-colored stills, PAE heatmaps, and topology spins
  from a downstream render lane.

## Repo And References

- Biohub ESM repository: https://github.com/Biohub/esm
- Biohub ESMFold2 overview: https://biohub.ai/esm/protein
- Biohub Platform ESMFold2 model and API entry point:
  https://biohub.ai/models/esmfold2
- Biohub Platform API reference: https://biohub.ai/api-reference
- Biohub release note: https://biohub.org/news/world-model-of-protein-biology/
- Hugging Face ESMFold2: https://huggingface.co/biohub/ESMFold2
- Hugging Face ESMFold2-Fast: https://huggingface.co/biohub/ESMFold2-Fast
- Hugging Face ESMC-6B: https://huggingface.co/biohub/ESMC-6B

## Key Knobs

| Knob | Recommendation | Why |
| --- | --- | --- |
| Source install | Pin the Biohub `esm` commit used by the operator packet | Avoid silent API or input-class drift. |
| First model | `biohub/ESMFold2-Fast` | Proves the weight and inference path before larger runs. |
| Weight source | Hugging Face snapshots | Avoids Biohub API token and API-cost uncertainty for first canaries. |
| Biohub API | Optional/deferred | Requires runtime secret, terms review, and separate closeout. |
| Python | 3.12 runtime | Current Biohub `esm` route expects Python 3.12. |
| Torch/CUDA | Verify after source install | Source installs can change torch; CUDA visibility must be re-probed. |
| Artifact gate | Require `prediction.cif` plus structure validation | Viewer HTML or a process exit is not success. |

## Cloud Run Pattern

RunPod is the default reviewed pod path for this public repo, and Lambda Cloud GPU
VMs and Modal serverless GPU functions are reviewed neocloud paths alongside it,
each with its own provider profile and compute-backends note. Other
bring-your-own cloud VMs should be treated as generic-cloud adapters until a
provider profile and validator coverage exist here.

Recommended run order:

1. Provider lifecycle smoke with no ESM install, no weights, no biological input.
2. `esmfold2-no-download-toolcheck`: source/package/import and metadata probes
   only.
3. Hugging Face weights fast canary on one public sequence.
4. Small gallery, binder foldability crosscheck, RNP/complex canary, or Atlas
   scout only after the fast canary artifact path is proven.

## Gotchas

- ESMFold2-Fast still depends on the large ESMC backbone. Budget model-weight
  materialization and cache behavior explicitly.
- A Hugging Face metadata probe is not a weight download, and a weight download
  is not a prediction.
- A cloud instance or pod in a running state is not evidence. Require runtime
  uptime, workload-owned progress, fetched artifacts, hashes, and cleanup proof.
- Do not retry unobservable CPU/provider routes as evidence. Prove lifecycle
  with a tiny provider smoke before installing ESMFold2 or downloading weights.
- Treat protein-RNA, protein-DNA, ligand, and modified-residue inputs as
  separate canaries. Do not infer broad input support from a monomer success.
- ChimeraX or other renderers are separate license/runtime-gated lanes.

## Gates

- No model weights in git, public images, docs, Linear, or chat.
- No Biohub API token in git, `.env`, notebooks, Linear, manifests, or logs.
- Public examples must use public accessions or synthetic fixtures only.
- Real cloud runs need explicit operator approval for budget, runtime, model
  weight download, provider route, expected artifacts, and cleanup.
- Result boundary is at most `computational_candidate` unless stronger
  independent evidence is joined.
- Run a currency check before paid GPU dispatch: Biohub repo HEAD, Hugging Face
  model revisions, model-card license/notices, and current Biohub API docs.

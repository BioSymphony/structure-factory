# ESMFold2

## Purpose

Plan ESMFold2 structure-prediction and foldability lanes for public or
operator-approved biomolecular inputs. In Structure Factory this is a
prediction and uncertainty lane, not a standalone proof of binding, function,
or therapeutic value.

## Public-Safe Status

The registry records the stable Biohub `esm==3.4.1.post1` package and its
published wheel hash. The repository retains a fixed-argument wrapper and its
artifact contract, but the execution registry marks both full and Fast routes
`adapter_required`: the wrapper predates the current stable package interface
and has not been ported and dry-run against it.

The Biohub API is a separate route with its own terms and acceptable-use
policy. Before execution, the selected runtime must verify the installed model,
available compute, inputs, budget, outputs, and cleanup contract.

## Model Routes

The public docs expose three relevant local software routes:

- `biohub/ESMFold2`: full model through a compatible Biohub `esm` adapter.
- `biohub/ESMFold2-Fast`: Fast variant through a compatible Biohub `esm`
  adapter.
- `biohub/ESMFold2-hf`: official full-model checkpoint through stable Hugging
  Face Transformers. The checkpoint bundles its ESMC backbone.

The bundled `bsf-esmfold2-predict` code documents the prior Biohub `esm`
integration and remains covered by contract tests. It is not an advertised
fresh-install route. Supply a validated adapter for either stable package path
and preserve the output contract below.

Anthropic publishes an ESMFold2 optimization kit against its own pinned
3.3-era ESM and Transformers stack. That kit is a separate runtime environment,
not an overlay for the stable `esm==3.4.1.post1` record here. See
[Anthropic inference optimization kits](anthropic-optimization-kits.md) for the
compatibility and qualification contract.

The Biohub Platform API is a separate optional route. API use reads its token
from the runtime environment and records the applicable service terms, cost,
data handling, and closeout.

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
Use the BioSymphony Structure Factory skill with the ESMFold2 tool card. Select
a ported stable-package adapter or the Biohub API route, then record the budget,
input data posture, expected artifacts, and cleanup rule before a paid or
networked run.
```

## Typical Inputs

- Public protein sequence, public accession-derived sequence, or synthetic
  fixture sequence.
- Structured chain manifest for protein, DNA, RNA, or CCD-coded ligand inputs.
- Optional public reference structure for RMSD/TM-style comparison.
- Runtime cache declaration for Hugging Face weights.

## Typical Outputs

- `predictions.jsonl` with one row for every input row.
- Per-prediction `structure.cif` or an explicit failed row.
- Per-prediction `confidence.json.gz` with PAE and pLDDT arrays.
- Per-prediction `confidence-summary.json` with pTM, ipTM, pLDDT mean, runtime
  identity, and artifact hashes.
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
- Hugging Face Transformers ESMFold2 docs:
  https://huggingface.co/docs/transformers/model_doc/esmfold2
- Stable `esm` package: https://pypi.org/project/esm/
- Hugging Face Transformers checkpoint: https://huggingface.co/biohub/ESMFold2-hf
- Hugging Face ESMC-6B: https://huggingface.co/biohub/ESMC-6B

## Key Knobs

| Knob | Recommendation | Why |
| --- | --- | --- |
| Package | Pin `esm==3.4.1.post1` or a later reviewed release and record its artifact hash | Avoid silent API or dependency drift. |
| First model | `biohub/ESMFold2-Fast` | Proves the weight and inference path before larger runs. |
| Weight source | Hugging Face snapshots | Avoids Biohub API token and API-cost uncertainty for first canaries. |
| Biohub API | Optional | Requires a runtime secret plus service-terms, data-handling, cost, and closeout records. |
| Python | 3.12 runtime | Current Biohub `esm` route expects Python 3.12. |
| Torch/CUDA | Verify after source install | Source installs can change torch; CUDA visibility must be re-probed. |
| Artifact gate | Require a count-preserving manifest, mmCIF, compressed confidence sidecar, summary, and hashes | A process exit is not success. |

## Cloud Run Pattern

RunPod is the default reviewed pod path for this public repo, and Lambda Cloud GPU
VMs and Modal serverless GPU functions are reviewed neocloud paths alongside it,
each with its own provider profile and compute-backends note. Use generic-cloud
adapters for other cloud VMs until the repository includes a provider profile
and validator coverage.

Recommended run order:

1. Provider lifecycle smoke with no ESM install, no weights, no biological input.
2. Port and dry-run an adapter against the selected stable package; record
   package, Transformers, model, and CCD identities.
3. Hugging Face weights fast canary on one public sequence.
4. Small gallery, binder foldability crosscheck, RNP/complex canary, or Atlas
   scout only after the fast canary artifact path is proven.

## Gotchas

- ESMFold2-Fast still depends on the large ESMC backbone. Budget model-weight
  materialization and cache behavior explicitly.
- A reachable top-level source pin does not prove that its transitive
  dependencies still resolve. Prefer a released package or audit the complete
  locked dependency graph.
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

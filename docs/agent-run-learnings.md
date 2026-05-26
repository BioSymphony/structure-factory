# Agent Run Learnings

This document captures public-safe lessons from recent Structure Factory agent
runs so future work does not depend on `.runtime/`, `internal/private/`, or
operator memory. It intentionally records capabilities, evidence limits, and
operational failure modes without copying heavy artifacts, provider secrets,
private resource IDs, or raw biological data into git.

The companion docs are [`docs/operational-gotchas.md`](operational-gotchas.md)
(a 45-class catalog of failure modes with paste-ready pre-flight probes and
fixes) and [`docs/preflight-checklist.md`](preflight-checklist.md) (10-gate
pre-dispatch checklist pattern). Read those before any paid GPU dispatch.

## Source Inventory

Reviewed sources:

- `demos/t2r14-open-dossier/README.md`, `demos/poltheta-map-model-dossier/README.md`, and `demos/structure-jury-dual-dossier/README.md`.
- `internal/private/*` files were used only as local context. Durable public-safe content is summarized here instead of linking to or copying those files.

## Capabilities Proven

Structure Factory has moved beyond prep-only work in these areas:

- Public accession mini-dossiers: fetch public PDB/EMDB/RCSB/wwPDB inputs, materialize them outside git, hash them, build model/map inventories, compute ligand neighborhoods, generate SVG figures, and emit methods, provenance, and claim ledgers.
- No-license CPU demos: T2R14, pol theta, and dual-dossier demos can run without CryoSPARC, Phenix, ChimeraX, MotionCor, Rosetta, AlphaFold 3, raw movies, private data, or persistent provider storage.
- Airgapped RunPod CPU shards: per-shard mini-dossiers can run from stock `python:3.12-slim` with gzipped base64 inline code and data modules. No GitHub clone, Network Volume, or custom Docker image is required for small CPU dossier shards.
- Inline RunPod GPU shards: Boltz verification can run from stock `pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime` on L40S GPUs through `inline_commands`, again without a git clone, Network Volume, or custom Docker image.
- Artifact pull and closeout: successful shards produce status files, artifact hashes, execution ledgers, claim ledgers, provenance, and tar archives or explicit notes when archive custody degraded.
- Fanout discipline: sequential fanout with skip-done resume keeps waves under their cost cap and makes failed shards cheap to debug before wider fanout.

## RunPod Operational Lessons

Treat these as launch-contract lessons, not anecdotes:

- Provider status is not workload progress. `desiredStatus: RUNNING`, IP assignment, port mapping, and pod creation are intent only. Require runtime uptime, proxy artifact availability, and workload-owned status or `stage-progress.jsonl`.
- Zero-uptime plateaus are provider lifecycle failures. If uptime remains `0` or null past the declared gate and the proxy returns 404/no artifacts, delete the pod, record the attempt, and retry or change placement.
- Proxy 404 is negative evidence. A proxy URL existing is not enough; the expected status file, archive, sentinel, or artifact must be non-empty and parse/hash-verifiable.
- REST `publicIp` and `portMappings` can lag reality. Direct proxy probes and runtime uptime were more useful than waiting on stale REST fields.
- Generic RunPod HTTP 500 can mean payload rejection. Inline `dockerStartCmd` payloads around the API size limit produced unhelpful 500s; gzip before base64 kept payloads well below the limit.
- Container disk limits depend on CPU flavor and vCPU count. Pin the tested flavor/vCPU/containerDisk tuple or use a selector that records the actual allocation.
- Warm images materially reduce spend. W4 was cheaper per successful shard than W2 because the PyTorch image was already warm in the datacenter.
- Capacity failures are normal operating cost. Budget a modest overhead for allocation failures and re-fires; strict delete gates kept provider-retry spend bounded.
- Canaries are mandatory for paid fanout. The first shard must exercise launch, proxy probe, artifact egress, hash verification, cleanup, and summary writing before remaining shards fire.

## Boltz Runner Lessons

The working Boltz route is specific:

- Use Boltz FASTA headers that satisfy the schema, for example `>A|protein`.
- For ligand-bound runs, use multi-record FASTA: `>A|protein` for the receptor and either `>B|smiles` for a small molecule or `>B|protein` for a peptide ligand.
- Use `--use_msa_server --no_kernels` on the stock PyTorch image; `--no_kernels` avoids missing cuEquivariance runtime dependencies in that base image.
- Boltz 2.2 output paths include the `boltz_results_<stem>/predictions/<stem>/` directory layer. The runner must discover the emitted CIF path rather than assume a simplified tree.
- Always write terminal `status.json`, even when the runner returns a degraded summary instead of throwing an exception.
- Treat `exit 0` without `prediction.cif` as a hard artifact failure. Fail-fast on missing expected outputs keeps the debug loop cheap.
- Record weights/version evidence in artifacts. A prediction artifact is not launch-ready evidence if the weights ref floats or is absent.

## Scientific Lessons

These are current candidate-level patterns; they are useful for future campaign design but are not wet-lab validation:

- Pocket contact IoU is a useful local metric for ligand-contact recovery. It answers a different question than global backbone RMSD and should be carried as a first-class validation artifact for ligand-bound dossiers.
- Receptor-only structure prediction can drift toward a canonical inactive-like fold when no ligand or partner context is supplied; ligand/partner context restores local pocket geometry.
- Predicted models, ProteinMPNN designs, pocket IoU, docking-like contact recovery, or rendered figures must stay at `candidate` unless stronger structural or experimental evidence is joined.

## Evidence Integrity Lessons

Closeout quality matters as much as pod success:

- Runtime artifacts under `.runtime/` are not source-of-truth git content. Tracked docs may summarize them, but raw artifacts, maps, model weights, CIF/PDB files, and provider records stay ignored.
- If local rescoring changes values after pod execution, mark the evidence as `derived` or `candidate (rescored)` and preserve the source artifact hashes. Do not pretend local JSON now matches the immutable provider archive.
- A corrupt archive or manual file-by-file pull can still be useful evidence, but it is a chain-of-custody downgrade. The report must say so and name the re-fire needed for a clean archive.
- Public reports must distinguish provider-native artifacts from local derived rescoring. Mixed evidence should downgrade the claim level until a derived-evidence bundle or clean re-run joins hashes, code refs, commands, and outputs.
- Claim ledgers are control artifacts, not prose. They determine what may advance to later waves and what must remain blocked, degraded, or insufficient.
- The final state should require fetched artifacts, hash checks, contract self-check, and verified cleanup. Pod creation, provider `RUNNING`, command exit, or screenshots alone are never success.

## Workflow And Agent Lessons

Agent orchestration worked best when the repo encoded exact contracts:

- Keep most campaign issues in `Backlog`; activate only the current wave.
- Run with one Symphony worker until repo, issue, launch, and no-download checks pass. Increase concurrency only after the workflow has a canary and verified artifact path.
- Workers should consume durable issue bodies and workflow files, not transient chat. Requirements that matter must be copied into the issue or repo.
- RunPod-bridge workers prepare launch packets and move to `In Review`; trusted host-side closeout owns paid create, artifact fetch/hash, cleanup verification, Linear closeout, and final transition.
- Linear can reformat YAML-like lists inside HTML comments. Prefer schema blocks that are robust to line-wise parsing, or use flow-style lists in generated issue bodies.
- Agents that show `status: completed` are RESUMABLE in many runtimes. `SendMessage` to a completed agent often resumes it in background with full prior context — do not assume "completed" means terminal.
- Parallel research agents save more pod-time than they cost. When stuck on a multi-cause debugging spiral, launching 3+ research agents in parallel against the failure resolves it in <5 min instead of a single-threaded hour-long spiral.

## Silent-Cascade Failure: The Highest-EV Pattern To Catch

Across multi-arm bake-off campaigns, the single most expensive failure mode is:

> A pipeline whose stage gates are exit-code-driven, not output-driven, will
> silently degrade to whatever subset of inputs survived — and call it success.

The incident pattern: a 4-arm designer bake-off produced 0/25 designs in three
arms because each arm hit a different first-order bug (apt-install fail,
atom-spec mismatch, cwd-dependent config). The orchestrator emitted
`STAGE_COMPLETE` on bash exit regardless, because every arm's design loop
caught its own exception internally and exited 0. Subsequent stages cascaded
with 1/4 of the planned inputs, `ALL_COMPLETE` fired, the pipeline "succeeded"
on paper while producing degraded output.

The fix is not heroic. Every worker validates output count before declaring
success; the orchestrator polls for both `STAGE_COMPLETE` and `STAGE_FAILED`
markers and fails fast on the latter. See gate G8 in
[`preflight-checklist.md`](preflight-checklist.md), class #34 in
[`operational-gotchas.md`](operational-gotchas.md), and the broader principle
in [`no-false-success-hardening.md`](no-false-success-hardening.md).

Smoke-test discipline is the companion lesson: a smoke that covers ONE
designer arm (the one most actively in development) is not a smoke. Every
designer must run end-to-end against the actual target — same PDB, same
hotspots, same env — before scaling. The bugs that bite (Genie 3 cwd, RFD3
atom-spec mismatch, PepGLAD two-chain output, RFdiffusion polyG without MPNN)
are different per designer, and a single-designer smoke leaves the others as
untested code paths into the live dispatch.

## Open Gaps

These gaps should be resolved before presenting Structure Factory as fully production-ready:

- Continue reconciling older bridge manifests with the current scope-check schema before claiming all provider manifests are green.
- ChimeraX and other GUI/license-sensitive render lanes remain operator-gated. Missing renderer access should block only the render lane, not upstream evidence processing.

## First end-to-end Genie 3 + Boltz dossier — operational lessons

Run profile: `genie3-boltz-design-jury` against a public protein-RNA-DNA assembly receptor window. The lessons below are target-agnostic and apply to any Genie 3 + Boltz binder-design run on a stock RunPod L40S pod, no Network Volume, no custom image.

- **Capability proven**: full Genie 3 binder-design + Boltz crosscheck pipeline runs end-to-end on a stock RunPod L40S pod, no Network Volume, no custom image.
- **Claim level**: `candidate` (per the pre-registered ladder: designed → predicted → passes pre-registered Boltz threshold). All forbidden claims unasserted.
- **Cost / runtime**: the final successful run stayed within the operator-approved cap. Record exact billing and placement details in ignored closeout artifacts; tracked docs should retain only the generalized runtime shape and lessons.
- **Pre-registered gate (BindCraft Nature 2025 + bioRxiv 2025/670059)**:
  - iPTM ≥ 0.50 — typical first-pass de novo designs against an RNA-binding cleft do not clear this gate without binder-MSA or designer swap.
  - ipSAE ≥ 0.60 — vendored DunbrackLab/IPSAE may off-by-one against the Boltz pLDDT array depending on Boltz version; verify before relying on locally computed ipSAE.
  - pocket-IoU ≥ 0.50 — requires an explicit reference pocket which many first-pass campaigns defer.
- **Operational failure modes that must NOT be repeated**:
  1. `stage_runtime_gate` runs before `stage_genie3_install`. On any image without genie3 pre-installed, `chosen_cli=None` gets cached and downstream stages bail. Fix: re-probe inside the consumer stage.
  2. `python -m huggingface_hub.commands.huggingface_cli` was removed in `huggingface_hub >= 0.20`. Use `huggingface-cli download` shell entry point or `huggingface_hub.snapshot_download` API.
  3. Genie 3 reads `pretrained/v1/config.yaml` relative to `cwd`. Invoke with `cwd=<weights_dir>` after the HF download (which lays out `pretrained/`).
  4. Genie 3's actual binder-design config schema is the binderbench layout (`paths.dataset` = a directory, `generation.dataset.{source,selections,n_sample}`, nested `generation.sampler.sampler.direction_scale`, `evaluation.{inverse_folding,folding}` blocks). The README's per-problem JSON shape is correct; the *layout* requires the full binderbench dataset (`problems/<sel>.json` + `targets/{pdb,fasta,msa}/<sel>{,-chain_X}.{pdb,fasta,a3m}`).
  5. The pytorch base image preinstalls torch 2.7.1+cu126; `pip install boltz==2.2.1` pulls torchvision 0.19.0 which is ABI-incompatible (circular import in `torchvision._meta_registrations`). Force-reinstall `torchvision==0.22.1` from `https://download.pytorch.org/whl/cu126` with `--no-deps`.
  6. Genie 3 reads `target_pdb_filepath` from the problem JSON via Python `open()` — that resolves relative paths from cwd, which is `<weights_dir>` and not `<paths.dataset>`. Synthesize the problem JSON with **absolute** paths.
  7. `genie3 run` does generate-then-evaluate. The evaluate step needs `ProteinMPNN` (separate package not pip-resolvable from upstream Genie 3's setup.py). Use `genie3 generate` instead — Boltz is the independent crosscheck per the campaign design.
  8. `genie3 generate` writes outputs to `<rootdir>/<selection>/pdbs/<selection>_<sample_idx>.pdb`, not the README-documented `results/v0_success/successful_complexes/`. Search the entire `<rootdir>/<cid>/` subtree.
  9. Boltz's `numba` dep requires `numpy ≤ 2.1`, but Genie 3's `pip install -e <source>` upgrades numpy past 2.1 mid-run. Re-pin `numpy<2.2` inside `stage_boltz_crosscheck` itself, right before invoking boltz. Idempotent. Pinning only at startup is insufficient.
  10. RunPod POST /pods has a ~64 KB hard limit on the rendered docker start payload. Inline scripts must be tar+lzma+base64 packed (vs individually gzipped) AND minified (strip docstrings + comments) to fit four runner scripts under the limit.
- **Vendored dep gap**: `scripts/structure_factory/vendor/ipsae/ipsae.py` indexing the Boltz pLDDT array hits an off-by-one (`IndexError: index N out of bounds for axis 0 with size N`). The full PAE matrix and confidence files are correct; the wrapper just can't compute ipSAE locally yet. iPTM (from Boltz `confidence.json`) is the substitute metric until ipSAE is fixed.
- **Memory snapshots saved** so future cofold campaigns don't repeat the bug carousel:
  - `boltz_output_layout.md` — `--write_full_pae` flag is required; outputs nest under `boltz_results_<stem>/predictions/<stem>/`; promote to flat paths.
  - `runner_stage_ordering_and_hf_api.md` — runtime_gate must re-probe after install; `huggingface_hub.commands` is dead; HEAD-only toolchecks miss real download failures; Genie 3 needs `cwd=<weights_dir>`.

## Future Capture Rule

After any real or derived Structure Factory run, update this document or a linked tracked dossier with:

- run profile and source artifact classes
- capability proven or not proven
- budget posture, runtime class, and provider failure modes
- exact artifact contract changes
- claim level and evidence mode
- any degraded, partial, derived, or blocked closeout reason
- next runbook change future agents should follow

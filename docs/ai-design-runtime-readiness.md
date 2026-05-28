# AI Design Runtime Readiness

This note captures the RunPod-saving checks for Boltz, Genie 3, and ESMFold2 lanes. It is provider-neutral in the science contract, but the preferred execution order is RunPod, AWS Batch, neocloud/generic cloud, then local high-resource workstations.

## Upstream Facts Checked

- Boltz 2.2.1 is the current pinned version in this repo. Upstream recommends a fresh Python environment and `pip install boltz[cuda] -U`; PyPI records Python `>=3.10,<3.13` and the `cuda` extra. See [Boltz README](https://github.com/jwohlwend/boltz) and [Boltz PyPI](https://pypi.org/project/boltz/).
- Boltz prediction input should be YAML. Upstream still accepts FASTA, but the prediction docs mark FASTA deprecated. Runtime cofold lanes should write `target.yaml`; per-variant model-comparison lanes should write `variant.yaml`. See [Boltz prediction docs](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md).
- Boltz `--cache` defaults to `~/.boltz` and respects `BOLTZ_CACHE`; Structure Factory passes `--cache` to the declared weights/cache directory so first-run downloads are visible in the artifact ledger.
- Boltz `--use_msa_server` calls the mmseqs2/ColabFold service. Use it only for public sequences or an issue that explicitly permits external MSA service use. For private targets, set `STRUCTURE_FACTORY_BOLTZ_USE_MSA_SERVER=0`, accept lower-accuracy single-sequence mode, or provide precomputed MSAs.
- Boltz affinity outputs are small-molecule/protein oriented. Upstream cautions that affinity predictions involving RNA/DNA targets are unreliable. For binder campaigns against RNP or nucleic-acid-containing targets, treat Boltz as a structure/interface comparison first; affinity statements stay capped at `computational_candidate`.
- Genie 3 upstream setup creates a `genie3` conda environment and installs ColabFold into that environment. See [Genie 3 setup docs](https://github.com/aqlaboratory/genie3).
- Genie 3 upstream download defaults fetch both pretrained weights and training data; Structure Factory blocks training data by default and pins HF downloads by revision when enabled.
- Genie 3 binder design supports single-node multi-device, multi-node sharding, beam search, iterative design, and `genie3 status`. Its evaluator writes `info.csv`, `success_info.csv`, successful binders, and successful complexes. These outputs map cleanly onto cloud shard/reduce stages.
- Biohub's ESM README describes two execution paths for ESM models: Biohub Platform API and local Hugging Face weights. Structure Factory should mention both, but prefer Hugging Face weights for the first cloud canary because it avoids API-token and API-cost uncertainty.
- The two ESMFold2 model routes to track are `biohub/ESMFold2` and `biohub/ESMFold2-Fast`. The fast route still uses the ESMC backbone, so first-run downloads are closer to the backbone size than to the small fast head alone.
- Public Hugging Face metadata checked on 2026-05-28 reported `biohub/ESMFold2-Fast` revision `0438ea0d932a314950665e0b4d0af4322ae88250`, `biohub/ESMFold2` revision `e1e189d0f5fb70c2693da2332eca4443c0ccccd6`, and `biohub/ESMC-6B` revision `89c554c46a44d825fbfbe3ce2a6bdc539770bdaa`. Re-check before any paid run.
- Biohub ESM source HEAD checked on 2026-05-28 differed from the short install ref in the public README. Operator packets must pin a full source commit SHA deliberately rather than following a floating branch.

## Repo Guardrails

- `make harness-check` is the no-download control-plane check. It validates registry pins, lane modules, binder-manifest posture, bootstrap gates, provider posture, and stage contracts.
- `make harness-check` is the strict runtime check. It should pass only inside a real GPU runtime or a local workstation that already has `boltz`, `genie3`, Torch/JAX, and GPU visibility.
- RunPod entrypoints look for Network Volume installs under `/workspace/software/envs/...` before installing anything into the image runtime.
- Genie 3 bootstrap is deferred unless `GENIE3_INSTALL=1`, `GENIE3_OPERATOR_GATE_ACK=dependency_and_weight_terms_reviewed`, and `GENIE3_ALLOW_COLABFOLD_PARAMS=1` are all set.
- Genie 3 pretrained weights require `GENIE3_DOWNLOAD_WEIGHTS=1`; training data additionally requires `GENIE3_DOWNLOAD_TRAINING_DATA=1` and `GENIE3_ALLOW_TRAINING_DATA=1`.

## Provider Posture

- Blessed: RunPod primary, AWS Batch cloud scale.
- Preferred adapter-ready: neocloud GPU pods and generic cloud VMs.
- Supported local: users with adequate GPU/storage may run locally if the issue declares paths, privacy posture, and cleanup.
- Not enough: provider launch success, a pod ID, or a zero exit code without artifact hashes, stage progress, and contract self-check.

## ESMFold2 Cloud Readiness

ESMFold2 enters Structure Factory as a staged prediction/foldability lane:

1. Provider lifecycle smoke with no ESM install, no model weights, no API call,
   and no biological input.
2. `esmfold2-no-download-toolcheck`: source/package/import probes and
   Hugging Face metadata checks only.
3. Hugging Face weights fast canary on one public sequence using
   `biohub/ESMFold2-Fast`.
4. Gallery, binder foldability crosscheck, RNP/complex canary, or Atlas scout
   only after the fast canary has fetched, hashed, and validated artifacts.

The Biohub API route is useful to document for future agents, but it is
optional/deferred in this repo. API execution requires a runtime-only token,
terms review, explicit cost posture, request/response artifact policy, and a
separate closeout that says the API was used.

For RunPod, use the same ladder as the other Structure Factory lanes: public
template -> private/operator-gated packet -> launch preflight -> paid create
-> artifact/hash/cleanup closeout. The public template for this lane is
`runpod/bridge-manifests/esmfold2-no-download-toolcheck.json`; it is not
launchable.

For generic cloud VMs, including Lambda Cloud-style capacity, keep the provider
under `generic_cloud` until a real provider profile exists. The useful pattern
is a single short-lived GPU VM, no persistent filesystem for the first canary,
runtime bootstrap to Python 3.12, post-install Torch/CUDA re-probe, archive
only declared artifacts, hash the archive after fetch, terminate immediately,
and verify no matching instance or filesystem remains.

Minimum ESMFold2 artifact contract:

- `status.json`
- `stage-progress.jsonl`
- `executed-commands.jsonl`
- `validation/host_probe.json`
- `validation/source_install.json`
- `validation/package_probe.json`
- `validation/model_metadata_probe.json`
- `validation/weights_manifest.json` when weights are materialized
- `esmfold2/prediction.cif` for real prediction runs
- `esmfold2/confidence_summary.json`
- `validation/structure_validation.json`
- `methods.md`, `provenance.md`, `claim_ledger.json`, and `artifact_index.json`

What an ESMFold2 canary proves:

- the selected provider can bootstrap the runtime
- the selected model revisions can be materialized or found in cache
- the run emits parseable structure and confidence artifacts
- the artifact egress and cleanup path works

What it does not prove:

- binding, function, mechanism, stability, expression, specificity, safety, or
  therapeutic value
- broad support for every protein/RNA/DNA/ligand input class
- readiness for fanout before a one-sequence canary has closed cleanly

## Binder Demo Implications

- Use public deposited structures for early demos and keep external MSA server use public-only.
- Generate binders with Genie 3 against declared target windows, then use Boltz to re-predict target/binder complexes and score interface plausibility.
- Treat Boltz small-molecule affinity fields as out of scope for protein/RNP binder ranking unless a future validated protocol proves otherwise.
- Close every demo with `computational_candidate` or lower result boundary until experimental or orthogonal computational validation exists.

## Genie 3 No-Download Toolcheck (Lane Gate)

The Genie 3 lane is gated behind a single GPU-pod toolcheck that proves source/install/CLI shape works on RunPod before any binder hunt commits real spend or wall-clock to the lane. The toolcheck is NOT a generation run. The toolcheck does NOT download weights. The toolcheck does NOT call ColabFold. The toolcheck does NOT produce any design output.

Build artifacts:

- `runpod/bridge-manifests/public-nonlaunchable-template.json` — public shape-only RunPod bridge template. Build any real Genie3, Boltz, or RFdiffusion provider packet outside public git after operator approval.
- `runpod/stage-contracts/genie3-no-download-toolcheck.stage-contract.json` — 7 fail-closed stages: host_probe, source_download, dependency_review, pip_install, smoke_commands, hf_weights_probe, emit_artifacts.
- `scripts/structure_factory/genie3_toolcheck.py` — single-file runner; gzip+base64-embedded into dockerStartCmd by the manifest builder.
- `scripts/structure_factory/build_genie3_toolcheck_bridge_manifest.py` — manifest builder.
- Use the binder-design fast-path task pack under `packs/` for an operator-gate Linear task draft.

Local pre-flight evidence (no GPU, `--no-install` mode):

- Source archive at lane-pinned commit `5214459c…0815115` is 12.87 MB; sha256 `5530ad4372f84f4f64b4b17e429d5c2cd05e4c8e07ada07762da40a3c0de6d02`.
- `setup.py` and `README.md` resolve in the extracted source tree.
- HuggingFace revision `9ae31ebb…2a03a2` for `yeqinglin/genie3` resolves with 8 sibling files including pretrained legacy + v1 checkpoints, configs, and gated training-data CSVs.
- Smoke commands fail locally (expected — no `genie3` CLI in path); on the GPU pod they should pass after `pip install -e .` against the extracted source.

Make targets:

```bash
make demo-genie3-toolcheck-manifest
make demo-genie3-toolcheck-bridge-validate
make demo-genie3-toolcheck-bridge-prepare
make demo-genie3-toolcheck-execution-packet
make demo-genie3-toolcheck-prep-check
```

What a passing toolcheck proves:

- Genie 3 source archive at the lane-pinned SHA fetches cleanly into the chosen GPU image.
- `pip install -e .` resolves the upstream dependency tree on `pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime` without an image rebuild.
- At least one of `genie3 --help`, `python -m genie3.cli --help`, or `import genie3` exits 0.
- The pinned HuggingFace weights revision is resolvable (HEAD probe — body NOT downloaded).

What a passing toolcheck does NOT prove:

- Weights load on the chosen GPU.
- Inference completes.
- Designs are biologically plausible.
- The lane is ready for any specific receptor target.

Each of those needs a separate, scoped run: weights download (operator-gated by `GENIE3_DOWNLOAD_WEIGHTS=1`), `genie3-public-design-canary`, then `genie3-boltz-design-ranking` against a real target window.

## Minimum-Viable Demo Pattern (No-GPU Baseline)

A useful pattern for any GPU-gated lane is a Minimum-Viable Demo that completes without a GPU, an operator gate, or a provider mutation. It produces a no-download window report from public accession metadata so the rest of the campaign has a real target shape to consume even if the GPU lane blocks. The stretch tranche (Genie 3 generation + Boltz cross-check) then sits behind the relevant toolcheck operator gate.

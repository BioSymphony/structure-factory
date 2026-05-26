# AI Design Runtime Readiness

This note captures the RunPod-saving checks for Boltz and Genie 3 lanes. It is provider-neutral in the science contract, but the preferred execution order is RunPod, AWS Batch, neocloud/generic cloud, then local high-resource workstations.

## Upstream Facts Checked

- Boltz 2.2.1 is the current pinned version in this repo. Upstream recommends a fresh Python environment and `pip install boltz[cuda] -U`; PyPI records Python `>=3.10,<3.13` and the `cuda` extra. See [Boltz README](https://github.com/jwohlwend/boltz) and [Boltz PyPI](https://pypi.org/project/boltz/).
- Boltz prediction input should be YAML. Upstream still accepts FASTA, but the prediction docs mark FASTA deprecated. Our W2 runner now writes `target.yaml`; W5 writes per-variant `variant.yaml`. See [Boltz prediction docs](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md).
- Boltz `--cache` defaults to `~/.boltz` and respects `BOLTZ_CACHE`; Structure Factory passes `--cache` to the declared weights/cache directory so first-run downloads are visible in the artifact ledger.
- Boltz `--use_msa_server` calls the mmseqs2/ColabFold service. Use it only for public sequences or an issue that explicitly permits external MSA service use. For private targets, set `STRUCTURE_FACTORY_BOLTZ_USE_MSA_SERVER=0`, accept lower-accuracy single-sequence mode, or provide precomputed MSAs.
- Boltz affinity outputs are small-molecule/protein oriented. Upstream cautions that affinity predictions involving RNA/DNA targets are unreliable. For binder campaigns against RNP or nucleic-acid-containing targets, treat Boltz as a structure/interface jury first; affinity claims stay capped at `candidate`.
- Genie 3 upstream setup creates a `genie3` conda environment and installs ColabFold into that environment. See [Genie 3 setup docs](https://github.com/aqlaboratory/genie3).
- Genie 3 upstream download defaults fetch both pretrained weights and training data; Structure Factory blocks training data by default and pins HF downloads by revision when enabled.
- Genie 3 binder design supports single-node multi-device, multi-node sharding, beam search, iterative design, and `genie3 status`. Its evaluator writes `info.csv`, `success_info.csv`, successful binders, and successful complexes. These outputs map cleanly onto cloud shard/reduce stages.

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

## Binder Demo Implications

- Use public deposited structures for early demos and keep external MSA server use public-only.
- Generate binders with Genie 3 against declared target windows, then use Boltz to re-predict target/binder complexes and score interface plausibility.
- Treat Boltz small-molecule affinity fields as out of scope for protein/RNP binder ranking unless a future validated protocol proves otherwise.
- Close every demo with `computational_candidate` or lower claim level until experimental or orthogonal computational validation exists.

## Genie 3 No-Download Toolcheck (Lane Gate)

The Genie 3 lane is gated behind a single GPU-pod toolcheck that proves source/install/CLI shape works on RunPod before any binder hunt commits real spend or wall-clock to the lane. The toolcheck is NOT a generation run. The toolcheck does NOT download weights. The toolcheck does NOT call ColabFold. The toolcheck does NOT produce any design output.

Build artifacts:

- `runpod/bridge-manifests/genie3-no-download-toolcheck.json` — RTX 4090, operator-defined spend cap, 60 min terminate, inline_commands airgap (no Network Volume, no git clone, no registry auth).
- `runpod/stage-contracts/genie3-no-download-toolcheck.stage-contract.json` — 7 fail-closed stages: host_probe, source_download, dependency_review, pip_install, smoke_commands, hf_weights_probe, emit_artifacts.
- `scripts/structure_factory/genie3_toolcheck.py` — single-file runner; gzip+base64-embedded into dockerStartCmd by the manifest builder.
- `scripts/structure_factory/build_genie3_toolcheck_bridge_manifest.py` — manifest builder.
- Use the binder-design fast-path issue pack under `packs/` for an operator-gate Linear issue draft.

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

Each of those needs a separate, scoped run: weights download (operator-gated by `GENIE3_DOWNLOAD_WEIGHTS=1`), `genie3-public-design-canary`, then `genie3-boltz-design-jury` against a real target window.

## Minimum-Viable Demo Pattern (No-GPU Baseline)

A useful pattern for any GPU-gated lane is a Minimum-Viable Demo that completes without a GPU, an operator gate, or a provider mutation. It produces a no-download window dossier from public accession metadata so the rest of the campaign has a real target shape to consume even if the GPU lane blocks. The stretch tranche (Genie 3 generation + Boltz cross-check) then sits behind the relevant toolcheck operator gate.

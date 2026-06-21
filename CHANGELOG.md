# Changelog

## Unreleased

Public-prep pass on the local repo. No remote push.

- Reframed the README, agent skills, AGENTS guide, FAQ, glossary, and tool cards to lead with what users and their agents can run, rather than what the repo is not.
- Added a public README banner and 1280 x 640 social preview asset under `docs/assets/`.
- Added `bsf catalog` (JSON and Markdown) and wired it into the Make targets and skill files.
- Added new tool cards for Boltz, Chai-1, and ProteinMPNN drafted from upstream sources, plus a `Hand A Mission To An Agent` section to every existing tool card.
- Added `docs/faq.md` and `docs/glossary.md` so newcomers and general-purpose agents have a starting place for jargon and common questions.
- Scrubbed operational data and launch-specific identifiers. Replaced specific budget, provider, branch, issue, and runtime details with public placeholders or tracker-neutral labels.
- Replaced campaign-specific scores and output examples with compact synthetic schema examples.
- Removed target-specific execution baggage and overly detailed demo artifacts while preserving representative public templates, issue shapes, stage-contract patterns, fixtures, docs, and validation checks.
- Cleaned cross-references across docs, modules, builder scripts, Make targets, and tests so the public repo presents reusable Structure Factory patterns rather than one operator's run history.
- Added Lambda Cloud and Modal as first-class remote compute paths alongside RunPod and AWS Batch: added public-safe provider profiles under `modules/provider-profiles/lambda/` and `modules/provider-profiles/modal/`, taught the provider and module-manifest validators about the new providers and the `serverless_function` class, listed them in `sidecar.yaml`, and documented each path across `docs/compute-backends.md`, `AGENTS.md`, `README.md`, the ESMFold2 tool card, and the system-context diagram.
- Generalized the in-pod repo-checkout default to `/workspace/repo` (matching the network-volume bootstrap convention, and kept distinct from the `/workspace/structure-factory` volume root) across the RunPod entrypoints and scope check, and dropped the old repo name from the sidecar workflow-template filename.
- Deduplicated the provider allowlists into a shared `scripts/structure_factory/provider_policy.py` imported by both `provider_profile_check.py` and `module_manifest_check.py`, so the two validators use the same policy.
- Added two tool cards: `tools/cosine.md` (CoSiNE, antibody affinity maturation as a neural CTMC: sequence-only evolutionary likelihood, zero-shot variant-effect prediction, and oracle-guided maturation) and `tools/esmfold2-binder-controls.md` (sequence, structure, interface, logit, and optimization controls for constraining ESMFold2/Biohub binder-design runs); indexed both in `tools/README.md`.
- Refreshed the `docs/tooling-and-licensing.md` design lane: added AlloGen (Hugging Face Apache-2.0 metadata vs MIT `LICENSE` split), sharpened RFdiffusion (BSD plus dependency/commit/weight-hash review) and Chai-1 (Apache-2.0, pin and MSA-server posture), pinned Boltz to PyPI 2.2.1, and noted CoSiNE (MIT, GPU-only install).

## 0.1.0-alpha.0 - 2026-05-13

Initial public Structure Factory export.

- Added public BioSymphony/Symphony harness for structural biology campaign planning.
- Added portable Structure Factory agent instructions.
- Added public PD-L1 binder-design example with claim-capped candidate ranking shape.
- Added tracker-neutral task pack for the binder-design fast path.
- Added RunPod-first launch templates, stage contracts, and provider docs.
- Added dependency-free public validator and audit CLI.
- Added `make harness-check`, `make release-check`, and optional `make secret-scan` gates.
- Kept non-public history, local runtime artifacts, concrete provider IDs, credentials, raw/generated structures, archives, videos, and model weights out of the public export.

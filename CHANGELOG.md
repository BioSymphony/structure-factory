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

## 0.1.0-alpha.0 - 2026-05-13

Initial public Structure Factory export.

- Added public BioSymphony/Symphony harness for structural biology campaign planning.
- Added portable Structure Factory agent instructions.
- Added public PD-L1 binder-design example with claim-capped candidate ranking shape.
- Added tracker-neutral task pack for the binder-design fast path.
- Added RunPod-first launch templates, stage contracts, and provider docs.
- Added dependency-free public validator and audit CLI.
- Added `make harness-check`, `make release-check`, and optional `make secret-scan` gates.
- Removed private history, private local runtime artifacts, concrete provider IDs, credentials, raw/generated structures, archives, videos, and model weights from the public export.

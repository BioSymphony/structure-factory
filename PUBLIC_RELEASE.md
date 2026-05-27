# Public Release Readiness

Last reviewed: 2026-05-27

This repository is ready to publish when it is a clean-history public control plane for BioSymphony Structure Factory: useful enough for external structural biology users and agents, but free of private history, private data, credentials, heavy generated artifacts, and unsupported scientific conclusions.

## Release Positioning

BioSymphony Structure Factory helps agents run long-running structural biology work. It is meant to help a user or team convert a biological goal into:

- target windows and structure sets
- binder-design, structure-mapping, screening, prediction, and render lanes
- Symphony/Linear or similar tracker-ready task plans
- RunPod-first cloud execution profiles
- stage contracts and progress ledgers
- expected artifact and hash checks
- candidate rankings, reports, and figures

Wet-lab protocols, clinical tools, therapeutic conclusions, and storage of unrestricted biological data live outside the repo. See [`NON_CLAIMS.md`](NON_CLAIMS.md) and [`BIOSAFETY.md`](BIOSAFETY.md) for the full boundary.

## Release Gates

Run these from the repository root before publishing:

```bash
make public-switch-check
make release-check
make secret-scan
```

Recommended independent checks:

```bash
find . -type f \( -name '*.pdb' -o -name '*.cif' -o -name '*.mmcif' -o -name '*.bcif' -o -name '*.map' -o -name '*.mrc' -o -name '*.mrcs' -o -name '*.star' -o -name '*.trb' -o -name '*.mp4' -o -name '*.mov' -o -name '*.gif' -o -name '*.npz' -o -name '*.npy' -o -name '*.pt' -o -name '*.pth' -o -name '*.safetensors' -o -name '*.zip' -o -name '*.tar' -o -name '*.tar.gz' -o -name '*.tgz' -o -name '*.pml' -o -name '*.fasta' -o -name '*.fa' -o -name '*.fastq' \) -not -path './.git/*' -print
find . -type f -size +25M -not -path './.git/*' -print
git ls-files | rg '(^|/)(\.runtime|artifacts|outputs|logs|runpod-runs|scratch|_book)/|\.(local\.json|pdb|cif|mmcif|bcif|map|mrc|mrcs|star|trb|mp4|mov|gif|npz|npy|pt|pth|safetensors|zip|tar|tgz|pml|fasta|fa|fastq)$'
```

Expected release state:

- `make public-switch-check` passes locally.
- `make release-check` passes.
- `make secret-scan` reports no leaks when gitleaks is installed.
- `make harness-check` reports zero findings.
- `skills/biosymphony-structure-factory/SKILL.md` is present and linked from public docs.
- `templates/operator-wave-runbook.md` is present for paid, cloud, raw-download, and multi-agent wave gates.
- No private workstation paths, private tracker IDs, concrete provider IDs, or stale private-doc references appear.
- No raw/generated structure files, archives, videos, model weights, or large files are tracked.
- No `.local.json` runtime summaries, Quarto `_book` outputs, generated report HTML, generated candidate sequence fields, or candidate render batches are tracked.
- Small curated public demo figures may remain only when they are referenced by public docs and contain no generated candidate sequences, private data, provider metadata, or raw structural files.
- `runpod/bridge-manifests/*.json` remain public non-launchable shape templates only: no per-campaign provider packets, embedded payloads, concrete placement, real approvals, run logs, and no prior-run volume assumptions.
- The public repo has clean history suitable for publishing under `BioSymphony/biosymphony-structure-factory-public`.

See [`docs/public-switch-checklist.md`](docs/public-switch-checklist.md) for the local switch gate, privacy/security checks, clean-history requirement, and remote-push gate.

## Publishing Notes

Before a remote push, choose the final public GitHub repository and add it explicitly:

```bash
git remote add origin https://github.com/BioSymphony/biosymphony-structure-factory-public.git
git push -u origin main
```

Do not push until the organization, visibility, and repository name are confirmed by the owner.

## First Agent Handoff

The next agent working inside this public repo should start with:

1. Read `AGENTS.md`, `README.md`, `PUBLIC_RELEASE.md`, and `docs/agentic-biology-harness.md`.
2. Use `skills/biosymphony-structure-factory/SKILL.md` as the portable agent-instruction entry point.
3. Run `make public-switch-check` before making public-facing statements about repo readiness.
4. Treat RunPod as the blessed first cloud-pod path, but do not launch paid compute without explicit authorization.
5. Keep task drafts tracker-neutral and use `sym:structure-factory` for Symphony routing.
6. Keep generated or predicted biological outputs labeled as planning, demo, or `computational_candidate` work unless real artifacts have been fetched, hashed, validated, and reviewed.

## Known Status

This is a pre-alpha public harness. The repo is useful for planning, orchestration, validation, dry-run task generation, and compact public examples. Provider-backed biological results still require explicit operator gates, real artifact closeout, and conservative labeling when outputs are partial.

## Summary

Run a small real Structure Factory demo that uses only public RCSB/PDB coordinate metadata for PDB `9W0Q` / EMDB `EMD-65512`, produces a coordinate-derived dossier, and prepares a guarded RunPod Pod launch packet. This is the first open-tool demo path for Symphony + Linear + RunPod without licensed tools, raw movies, private data, or large downloads.

## Inputs

- `pdb:9W0Q` - public RCSB entry metadata from `https://data.rcsb.org/rest/v1/core/entry/9W0Q`.
- `coordinates:9W0Q.cif` - public mmCIF coordinates from `https://files.rcsb.org/download/9W0Q.cif`.
- `runpod bridge manifest` - `runpod/bridge-manifests/t2r14-open-dossier.json`.
- `routing label` - `sym:structure-factory`.

## Expected Artifacts

- `runpod-execution/status.json` - terminal status for the demo workload.
- `runpod-execution/artifacts/report.html` - self-contained demo report with SVG figure panels.
- `runpod-execution/artifacts/dossier_manifest.json` - artifact and claim-level manifest.
- `runpod-execution/artifacts/coordinate-summary.json` - parsed atom, chain, residue, and deposition metadata summary.
- `runpod-execution/artifacts/interchain-contact-matrix.json` - coordinate-derived inter-chain contact summary.
- `runpod-execution/artifacts/ligand-neighborhoods.json` - non-water HETATM neighborhood summary.
- `runpod-execution/artifacts/claim_ledger.md` - claim boundaries and downgraded claims.
- `runpod-execution/artifacts/provenance.md` - source URLs and tool policy.
- `runpod-execution/artifacts/runpod-execution.tar.gz` - small artifact packet.

## Stage / Progress Contract

- stage contract: `runpod/bridge-manifests/t2r14-open-dossier.json`
- progress ledger: `runpod-execution/artifacts/stage-progress.jsonl` and `runpod-execution/monitor_events.ndjson`
- resume command: `make demo-t2r14-check`
- partial success policy: local dossier generation plus RunPod dry-run is `partial_provider_ready`; real RunPod execution requires a private/operator-gated runtime packet with runtime-secret references, explicit authorization, and cleanup closeout.

## Provider / Execution Profile

- provider: `runpod`
- execution profile: `map-model-dossier`
- operator gate required: `yes`

## Tooling / License Posture

- tools: `repo validators, public metadata tooling, provider dry-run scaffolds as declared by the issue`
- posture: `mixed`
- current primary source checked: `no; repo-local contract posture only`
- intended use context: `unknown until operator gate`
- image/runtime action: `scaffold or dry-run only unless the issue explicitly authorizes execution`
- operator action required: `explicit approval before paid provider mutation, gated tool installation, raw data download, or private-data handling`

## Acceptance Criteria

- [ ] `make demo-t2r14-check` succeeds from the repo root and emits a local public-coordinate dossier under `.runtime/t2r14-open-dossier-local/runpod-execution/`.
- [ ] The dossier includes `report.html`, three SVG figure panels, provenance, claim ledger, validation files, artifact hashes, and an archive packet.
- [ ] The RunPod bridge manifest validates and prepares a launch packet without credentials, raw EM data, private images, private data, or licensed tools.
- [ ] A no-cost RunPod dry-run emits an audited pod creation request for `python:3.12-slim`, CPU-only compute, a 45 minute budget, and an operator-defined maximum estimated cost.
- [ ] Real RunPod launch is not marked successful unless a pod actually executes, writes status/progress/hash artifacts, and is cleaned up.

## Validation Commands

```bash
make demo-t2r14-check
python3 -m py_compile scripts/structure_factory/t2r14_open_dossier.py scripts/structure_factory/build_t2r14_bridge_manifest.py
runpod-bridge validate-manifest runpod/bridge-manifests/t2r14-open-dossier.json --json
runpod-bridge prepare runpod/bridge-manifests/t2r14-open-dossier.json --out-dir .runtime/t2r14-open-dossier-packet --json
# Public repo: paid pod creation is intentionally omitted. Use a private/operator-gated execution packet under `.runtime/` after approval.
```

Real RunPod launch is intentionally not copy-pasteable from this public issue. Prepare a private/operator-gated runtime packet outside public git before adding execution flags.

## Final Outcome Contract

- worker lane: `codex or trusted-after-run`
- closeout state: `issue-declared target state`
- final comment must include: `<!-- symphony-outcome -->`
- success requires: `declared artifacts, validation commands, and explicit partial/degraded/blocked closeout when evidence is incomplete`

## Touched Areas

- `demos/t2r14-open-dossier/` - operator runbook for the contained open-tool demo.
- `scripts/structure_factory/t2r14_open_dossier.py` - public coordinate dossier runner.
- `scripts/structure_factory/build_t2r14_bridge_manifest.py` - generated RunPod bridge manifest builder.
- `runpod/bridge-manifests/t2r14-open-dossier.json` - audited RunPod launch manifest.
- `Makefile` - demo validation targets.

## Dependencies

Blocked by: operator-managed provider credentials, explicit paid-run approval, and an immutable public-safe source reference prepared outside public git.

## Risk Notes

- Do not store RunPod, GitHub, RCSB, or Linear credentials in git, Linear, artifacts, or reports.
- Do not use CryoSPARC, Phenix, ChimeraX, MotionCor, Rosetta/PyRosetta, AlphaFold 3, or other license-gated tools for this demo.
- Do not download raw EMPIAR movies, deposited maps, half maps, private structures, unpublished sequences, model weights, or large datasets.
- Treat coordinate-derived contact and ligand-neighborhood summaries as candidate observations, not biological mechanism claims.
- Do not mark the RunPod stage successful from `desiredStatus: RUNNING`; require workload status files, progress ledger entries, artifact hashes, and cleanup evidence.

## Complexity

tier: small

<!-- symphony:schema
schema_version: 1
subgroup: structure-factory
routing_label: sym:structure-factory
campaign_id: cryoem-raw-to-atomic-dossier
wave: DEMO-01
target_state: Backlog
touched_areas:
  - demos/t2r14-open-dossier/
  - scripts/structure_factory/t2r14_open_dossier.py
  - scripts/structure_factory/build_t2r14_bridge_manifest.py
  - runpod/bridge-manifests/t2r14-open-dossier.json
  - Makefile
complexity: small
-->

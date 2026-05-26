# T2R14 Open Dossier Demo

A small, real, no-license Structure Factory demo using public RCSB and EMDB metadata.

- PDB: `9W0Q`
- EMDB: `EMD-65512`
- target: bitter taste receptor T2R14 ligand and G-protein cryo-EM complex
- runtime: CPU-only, intended under one hour on RunPod

The demo uses public mmCIF and RCSB metadata, computes chain and ligand-neighborhood summaries, emits SVG figures, and writes a dossier packet with provenance and explicit claim limits.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill. Run the T2R14 open dossier demo locally, then prepare the RunPod bridge packet. Explain the chain and ligand-neighborhood summaries, the SVG figure outputs, the provenance, and what would be needed for an operator-gated RunPod launch.
```

## Run Locally

```bash
python3 scripts/structure_factory/t2r14_open_dossier.py \
  --out .runtime/t2r14-open-dossier-local/runpod-execution \
  --json
```

## Prepare The RunPod Bridge Packet

```bash
make demo-t2r14-check
```

Or run the bridge steps directly:

```bash
python3 scripts/structure_factory/build_t2r14_bridge_manifest.py
runpod-bridge validate-manifest \
  runpod/bridge-manifests/t2r14-open-dossier.json \
  --json
runpod-bridge prepare \
  runpod/bridge-manifests/t2r14-open-dossier.json \
  --out-dir .runtime/t2r14-open-dossier-packet \
  --json
# Paid pod creation runs from an operator-gated execution packet under .runtime/ after approval.
```

A real RunPod launch runs from an operator-gated runtime packet outside public git. The packet records authorization, budget, cleanup policy, immutable source reference, runtime-secret references, expected artifacts, and closeout checks.

## Scope

This demo uses public deposited evidence. CryoSPARC, Phenix, ChimeraX, MotionCor, Rosetta, AlphaFold 3, raw movies, private data, and persistent storage are outside the scope of this demo.

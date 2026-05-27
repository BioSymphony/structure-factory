# Pol Theta Map/Model Report Demo

A small real Structure Factory demo using public EMDB, PDB, and wwPDB validation data.

- EMDB: `EMD-43816`
- PDB: `9ASJ`
- target: human DNA polymerase theta helicase domain with AMP-PNP, dimer form
- runtime: CPU-only RunPod Pod, intended under two hours

The demo downloads the deposited EMDB map, PDB mmCIF model, and wwPDB validation XML and PDF. It computes map header and density summaries, model inventory, AMP-PNP neighborhoods, density-support checks, SVG figures, provenance, validation notes, and a real-mode contract self-check.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill. Walk through the Pol theta map/model report demo. Explain the public accessions, the validation pipeline, the expected figure outputs, and the contract self-check. Then prepare a non-launching RunPod bridge packet for review.
```

## Prep Check Without Launching

```bash
make demo-poltheta-report-prep-check
```

A real RunPod launch is driven by an operator-managed credential wrapper and a runtime packet that lives in operator-controlled infrastructure. The public repo carries the non-launchable template, expected artifacts, and validation flow.

## Scope

This demo uses public deposited evidence. Raw EMPIAR movies, CryoSPARC, Phenix, ChimeraX, MotionCor, Rosetta, AlphaFold 3, private data, and persistent RunPod storage are outside the scope of this demo.

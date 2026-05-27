# Prep Roadmap

This roadmap is for the next planning pass before dispatching Structure Factory workers.

## Phase 0: Repo Ready

- Dedicated sibling repo exists.
- Agent boundaries are explicit.
- Heavy/raw data is ignored.
- Preflight and registry checks run without external dependencies.

## Phase 1: Software Registry Hardening

- Verify every package version and license from primary sources before moving a lane from `planned` to `ready`.
- Split registry entries by image family.
- Add install smoke commands for each tool.
- Mark license-gated tools as runtime-provided, not redistributed.

## Phase 2: RunPod Image Plan

- Define image families and build order.
- Specify base CUDA versions, GPU classes, exposed ports, mounted volume paths, and smoke tests.
- Keep CryoSPARC, Phenix, ChimeraX, MotionCor, Rosetta/PyRosetta, AlphaFold, and similar licenses explicit.
- Add runtime license-gate checks that skip absent optional tools in prep and block enabled lanes without secrets.

## Phase 3: First Campaign Contract

- Promote `examples/empiar-10204-v0/` into a full campaign dry run.
- Draft Linear issue bodies for the first wave only.
- Validate contracts before any remote execution.
- Keep all high-cost or large-download issues parked in Backlog until the no-download smoke run proves the lane.
- Add CryoCore handoff contracts for EMPIAR-13124 50/100-movie raw-subset work and PDB/EMDB structure-mapping report contracts behind explicit operator gates.

## Phase 4: Tool-Ranking Campaign

- Add comparison-lane documentation for RELION, CryoSPARC, Warp/M, Topaz, ModelAngelo, Phenix, cryoDRGN, and figure generation, with raw reconstruction execution handled as CryoCore-owned work.
- Treat disagreement as an artifact that spawns review issues.
- Keep CryoSPARC, Phenix, ChimeraX, MotionCor3, Rosetta/PyRosetta, and AlphaFold 3 runtime-gated until access exists.

## Phase 5: Publication Report

- Produce a full structure report contract with maps, models, validation, figures, methods, provenance, validation notes, caveats, and next-experiment recommendations.

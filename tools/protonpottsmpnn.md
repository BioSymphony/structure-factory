# ProtonPottsMPNN

ProtonPottsMPNN proposes sequences for supplied protein backbones using an
explicit protonation-state vocabulary. Its design engine places titratable
centers on the binder and optimizes neighboring residues for sequence–structure
compatibility and preference for the assigned state.
[Source and design example](https://github.com/christian-creator/ProtonPottsMPNN/blob/09682abfa7d20e0abcdeea0490b7a4b1c190aee3/README.md).

## Inputs And Outputs

Record the complex coordinates, binder chain, residue mapping, checkpoint,
mutable positions, center assignments, objective weights, and seed.
The v6 checkpoint uses 30 tokens, including the following state pairs:

| Residue | State Pair |
| --- | --- |
| Histidine | `HIS-P` / `HIS-S` |
| Aspartate | `ASP-P` / `ASP-D` |
| Glutamate | `GLU-P` / `GLU-D` |

Retain canonical FASTA, state-token FASTA, centers, learned energies, and the
optimization trajectory. Rebuild state assignments after mutations change a
titratable residue's identity. Independently refold each retained final sequence.

## Interpret The Learned Scores

The native `compute_g_bind` helper subtracts isolated-partner Potts scores from
the complex score. It accepts one binder chain; a multichain binder needs
explicit partner grouping. Its scores use model-internal units.
[Native engine](https://github.com/christian-creator/ProtonPottsMPNN/blob/09682abfa7d20e0abcdeea0490b7a4b1c190aee3/foundry/models/mpnn/src/mpnn/inference_engines/potts_mpnn_ph.py).

A state-token contrast compares assigned microscopic states. Numerical-pH
predictions require a separate population model and calibration. Assess
bound/free contributions for the same final sequence and retain pose sensitivity.
Use the [pH comparison guide](../docs/binder-ph-comparison.md) for electrostatic
calculations and paired contrasts.

## Runtime Requirements

Qualify checkpoint loading, chain partitioning, mutation masks, and repeat
behavior before interpreting results. The native preparation pipeline includes
EV6/HBPLUS protonation labeling. The documented RF3 refolding route requires
separate weights and GPU setup. Check these operations independently.
Structure Factory records the method; execution requires a configured adapter.

The [project license](https://github.com/christian-creator/ProtonPottsMPNN/blob/09682abfa7d20e0abcdeea0490b7a4b1c190aee3/LICENSE)
covers authored code and checkpoints under MIT terms. Bundled Foundry retains
[BSD-3-Clause terms](https://github.com/christian-creator/ProtonPottsMPNN/blob/09682abfa7d20e0abcdeea0490b7a4b1c190aee3/foundry/LICENSE.md).
Review external labeling and refolding components separately.

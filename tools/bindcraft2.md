# BindCraft2

BindCraft2 (BC2) designs protein binders with AlphaFold2 sequence optimization,
ProteinMPNN redesign, and separate AlphaFold validation models. Its presets
cover miniproteins, peptides, scaffolded antibodies, and multistate objectives.
Structure Factory records BC2 as a documented design tool; execution requires
an adapter (`adapter_required`).

Reviewed 2026-09-21 at upstream commit
`18a9042fbe9a5373a5b7d98fe82335127c2fd70d`. Use the `bindcraft2` registry identity
for this repository. [BindCraft](https://github.com/martinpacesa/BindCraft) and FreeBindCraft have separate
source, dependency, and license records.

## Choose a design

| Goal | BC2 selection | Input detail |
| --- | --- | --- |
| De novo protein | `binder`, `large_binder` | Set `binder_lengths`; `large_binder` targets lengths over 300 residues. |
| Linear or cyclic peptide | `peptide`, `cyclic_peptide` | The cyclic preset targets head-to-tail cyclization. |
| Scaffolded binder | `VHH`, `ARP`, `scFv`, `Fab` | Select a supplied or custom scaffold. BC2 models scFv variable domains as two chains; design the linker separately. |
| Oligomer or multidomain binder | `homo_oligomer`, `multidomain` | Declare copies or domain configuration. |
| Several binding targets or an off-target | Multiple `targets`; `objective: detarget` for avoidance | Retain separate measurements for each target. |
| Binding-associated conformational change | `induced_fit`, `fold_switch` | These named presets require one target and a compatible binder format. |

BC2 accepts PDB, mmCIF, and FASTA targets. Record chain selections, hotspots,
coldspots, and scaffold regions with the input hashes. Optional properties
include humanization, protease resistance, disulfide staples, and terminal
geometry; each property selects computational objectives and filters.

## Prepare the runtime

The documented NVIDIA route uses Linux, Python 3.12 or newer, and JAX
`>=0.11,<0.12`, with CUDA 12 or CUDA 13 extras. The reviewed dependency manifest
does not require PyRosetta. Keep BC2 in its own environment because its Python
package and command are both named `bindcraft`.

In an installed environment, `bindcraft design --help` and
`bindcraft design --list-settings` inspect the interface without constructing a
JAX runtime. The upstream installer downloads AlphaFold parameters; installation
is a separate step from these interface checks.

Before execution, record the source revision, checkpoint hashes, resolved
settings, GPU allocation, runtime limit, and budget. Bind an adapter to fixed
arguments and declared outputs. Check the following BC2 settings:

- Set `max_trajectories` as well as `number_of_final_designs`. The accepted-design
  target alone leaves the number of attempts unlimited.
- Set the GPU selection and worker count explicitly. BC2 otherwise uses visible
  GPUs and packs workers according to available memory. `auto_multi_gpu: false`
  keeps a single process; `workers_per_gpu` and `design_workers` bound parallel runs.
- For method comparisons, start with `core: benchmark`, which sets
  `campaign_seed: 0`, `autotune: false`, and `desperation: false`. Inspect resolved
  settings because later presets and explicit overrides take precedence.
- Use a new `project_folder` for each experiment. Resume repeats the original
  settings against the same folder; preserve the campaign state and sequence
  deduplication files with the results.

Settings resolve in this order: core, core profile, modality, properties, target,
campaign, then command-line overrides. Keep the resolved configuration with the
report so a comparison can account for changes to models, filters, or objectives.

## Read the results

BC2 writes these paths within its output folder:

| Artifact | Contents |
| --- | --- |
| `1_Trajectories/!_Trajectories.csv` | Attempts, termination stages, and per-attempt setting changes. |
| `2_Refolded/!_Refolded.csv` | Scored ProteinMPNN candidates, outcomes, and failed filters. |
| `2_Refolded/Complexes/` | Predicted candidate complexes, including rejections by default. |
| `3_Ranked/!_Ranked.csv` and associated mmCIF files | Accepted candidates ranked by `i_pDAE` and their target-state structures. |
| `campaign_metadata.json` | Resolved settings, model choices, source revision, and checkpoint hashes. |

For completion, count accepted rows and verify their corresponding structures
for every required target state. Record rejected candidates and any shortfall
against the requested count. Join candidate and trajectory tables by `hash` to
inspect `autotuned` changes, including changes to validation models or target
flexibility.

Preserve each metric's scale when exporting scores:

- Table `pLDDT` uses 0-1; mmCIF B-factors store pLDDT on 0-100.
- `i_pAE` is mean interface PAE divided by 31 angstroms.
- `i_pDAE` selects resolved C-alpha pairs at or below 8 angstroms by default;
  higher scores rank first. See [Interpreting i_pDAE](#interpreting-i_pdae).
- Multitarget cells follow the `targets` column order. Preserve missing values
  and keep binding and detargeting results separate.

Use the selected predictor panel for downstream comparison. Label accepted
outputs `computational_candidate`; experimental binding requires measurement.

## Interpreting i_pDAE

BC2 computes `i_pDAE` from interface geometry and predicted aligned error (PAE).
For each anchor residue, it averages transformed PAE over contacting partners,
then takes the highest anchor score across both sides of the interface.
Its AF2 adapter first averages the two PAE directions.

For anchor `i`, let `S_i` contain resolved partner residues whose C-alpha atoms
are at most 8 angstroms away, and let `n_i` be their count. With PAE in angstroms:

```text
E_ij   = (PAE_ij + PAE_ji) / 2
d0_i   = max(1.24 * (max(n_i, 19) - 15)^(1/3) - 1.8, 1) angstroms
s_i    = mean over j in S_i of 1 / (1 + (E_ij / d0_i)^2)
i_pDAE = max(s_i) across anchors on both sides
```

Anchors without contacts contribute zero. Missing PAE or no resolved contact
pairs returns `None`. BC2 pools binder copies against the selected target chain.
Different contact neighborhoods and partner counts can produce different scores
on each side despite symmetric PAE.

For 1-26 partners, `d0_i` is 1 angstrom. If every selected pair has symmetrized
PAE of 2 angstroms, the anchor score is `1 / (1 + 2^2) = 0.20`.
Use the PAE matrix in angstroms; the table's `i_pAE` divides mean error by 31.

### Comparison with ipSAE

The comparison uses DunbrackLab's per-residue-normalized ipSAE for protein pairs:

| Calculation | ipSAE | BC2 i_pDAE |
| --- | --- | --- |
| Partner selection | Cross-chain PAE below a chosen cutoff | Resolved cross-chain C-alpha distance at or below the contact cutoff |
| PAE values | Directional | Averaged with the reverse direction |
| Normalization | Selected partner count per anchor, with a 1-angstrom floor | Contact count per anchor, with a 1-angstrom floor |
| Aggregation | Best anchor in each direction, then best direction | Best anchor across both sides |

Dunbrack's `dist_cutoff` controls separate contact diagnostics; its main ipSAE
selection uses the PAE cutoff. Calibrate `i_pDAE` thresholds against controls
for the selected protocol rather than importing ipSAE or ipTM thresholds.

The maximum emphasizes the highest-scoring local patch. Inspect contact counts,
interface coverage, clashes, and residue-level scores when comparing candidates.
BC2 ranks accepted candidates by `i_pDAE`; the configured filters determine
acceptance.

Pinned implementations: BC2
[metric calculation](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/bindcraft/filters.py),
[PAE preparation](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/bindcraft/af2.py),
[PAE normalization](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/bindcraft/loss.py),
[ranking](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/bindcraft/campaign_output.py),
and [DunbrackLab ipSAE at 6174cf9](https://github.com/DunbrackLab/IPSAE/blob/6174cf9e71cb1bd660cc805856a18c4871a6dec3/ipsae.py).

## License

The reviewed release uses the BindCraft2 Source-Available License
(Hosting-Restricted). It permits organizational use, including commercial
research, on infrastructure operated for that organization. It also permits
sharing design outputs and redistributing code for recipients to run themselves.
Preserve notices and identify modifications.

Providing BC2 functionality to third parties through a hosted API, application,
or agent tool requires a separate written commercial license. The license also
restricts naming that implies official association. AlphaFold2 parameters and
other third-party components retain their own terms. Review the exact deployment
and redistribution plan against the linked license before packaging a service.

## Sources

All source links identify the reviewed revision:

- [Overview and modalities](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/README.md)
- [Settings and preset precedence](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/docs/reference.md)
- [Installation and GPU controls](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/docs/installation.md)
- [Output files and metric definitions](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/docs/outputs.md)
- [Dependency manifest](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/pyproject.toml)
- [License](https://github.com/PacesaLab/BindCraft2/blob/18a9042fbe9a5373a5b7d98fe82335127c2fd70d/LICENSE)

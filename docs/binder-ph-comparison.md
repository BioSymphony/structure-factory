# Compare Binder Models Across pH

Compare predicted protonation and electrostatic contributions across a frozen
binder–target structure panel. Retain each structural model and preparation
method separately so you can identify a response that changes direction.

Use the [filtering card](../tools/binder-filtering.md) to select methods and the
[qualification contract](binder-filter-qualification.md) to define controls.
This guide specifies a comparison protocol for those tools.

## Define The States And Physical Parameters

Record the target construct, chain mapping, coordinate coverage, predictor,
checkpoint, and delivered seeds. Check complete sidechains, terminal groups,
bond geometry, and residue correspondence before assigning charges.

Use two separate state definitions:

| Definition | Preparation | Question |
| --- | --- | --- |
| Frozen bound state | Prepare the complex, then separate its partners with coordinates, charges, and radii preserved | What electrostatic contribution follows from this bound microstate? |
| Independently prepared states | Prepare the complex and each separated partner at the same pH | How sensitive is the contribution to separate protonation assignments? |

For each calculation, retain the force field, dielectric constants, ionic
strength, temperature, charge and radius set, grid dimensions, spacing, and
center. Match solvated and homogeneous-reference grids to cancel numerical
self-energy contributions. [APBS solvation calculations](https://apbs.readthedocs.io/en/latest/using/examples/solvation-energies.html)
describe this requirement.

Compute complex-minus-partners differences for polar solvation and Coulombic
contributions, with a consistent reference dielectric. These terms form an
electrostatic descriptor in kJ/mol. Molecular-mechanics and entropic terms
require separate calculations. [APBS binding-energy calculations](https://apbs.readthedocs.io/en/latest/using/examples/binding-energies.html)
define that cycle. The descriptor alone cannot estimate Kd.

## Calculate Paired Contrasts

Freeze the pH points and desired response before collecting scores. For
example, a panel can include pH 5.0, 5.5, 6.0, 6.5, 7.0, 7.4, and 8.0.
Two distinct contrasts answer different questions:

| Contrast | Calculation | Interpretation |
| --- | --- | --- |
| Acid-enhanced electrostatic contribution | Mean(E6.0, E6.5) − E7.4 | Lower values favor the acidic states within this descriptor |
| Acid-release electrostatic contribution | Mean(E5.5, E6.0) − E7.4 | Higher values favor the neutral state within this descriptor |

Calculate each contrast within one complete seed/grid curve. Repeat the
calculation across the declared structural seeds, finer grids, and translated
grids. Report their range as sensitivity to those choices. Keep each
protonation-state definition and predictor family in its own table.

Retain coupled-site flags from the pKa method. An independent-site occupancy
approximation needs an explicit label when coupled titration remains
unresolved. Record completion and missing outputs separately for every selected pKa
method and dynamics operation.

## Review Tradeoffs And Coverage

Display electrostatic response beside independent pose consistency and an
isolated-binder surface descriptor. An exposed hydrophobic patch is a
structural annotation; measured solubility is a separate endpoint.

For a Pareto comparison, declare axis directions, eligibility, and required
coverage. Keep failed native filters, controls, and incomplete candidates
visible. Missing required axes leave the full comparison incomplete; a
complete subset needs its own denominator. Frontier membership adds no
binding evidence or acceptance threshold.

Retain a compact table with model identity, state definition, pH, grid,
electrostatic contribution, paired contrast, coverage, and sensitivity range.
Measured affinity and measured pH response remain separate fields.

For protonation-conditioned sequence design and learned state scores, use the
[ProtonPottsMPNN card](../tools/protonpottsmpnn.md).

# Binder Filter Qualification

Qualify a candidate filter against its input contract and a control panel
before using the filter to reject candidates. Preserve the original score table
so you can compare the proposed rule at the same selection capacity.

Use the [filter tool card](../tools/binder-filtering.md) to select methods.
The [comparison contract](binder-comparison-contract.md) governs candidate
identity, and [confidence sidecars](confidence-sidecars.md) govern score joins.

## Freeze The Inputs

Record the sequence and structure hashes, predictor/checkpoint, seeds, target
construct and site, chain mapping, confidence scale, and complete PAE mapping.
For pH analysis, define the bound and free states, protonation preparation,
ionic conditions, grid settings, pH contrast, and desired response direction.

Candidate format determines applicability. A paired-antibody head needs its
declared heavy/light-chain inputs; a VHH profiler needs a compatible VHH. Keep
inapplicable rows and missing measurements visible in the result table.

## Check Computational Behavior

Before evaluating a threshold, check each adapter:

1. Verify source, checkpoint, input, and output hashes.
2. Check a matched chain/PAE permutation with the corresponding residue map.
3. Check a global rigid transform for geometry-invariant metrics.
4. For contact/PAE diagnostics, test separated partners and high-PAE controls.
5. Verify required output counts and preserve failed or incomplete rows.

Declare the expected outcome for each control before running it. A behavior
check establishes parsing and calculation properties; calibration requires
endpoint labels or suitable reference structures.

## Calibrate The Selection Rule

Choose controls that match the protein format, target class, predictor, and
endpoint. Record training overlap and use target-held-out, homology-aware, or
temporal splits where the available panel permits them.

Compare rules at equal retained counts or a fixed selection fraction. Report
precision, recall, denominator, exclusions, and uncertainty for that capacity.
A strict intersection of several model families can change capacity, so retain
the number selected alongside any enrichment result.

Keep PAE-derived diagnostics in one correlated evidence group. Additional seeds
sample variability within a model family; another family needs its own complete
model/checkpoint/seed coverage. Preserve per-predictor values when methods
disagree.

## Record The Decision

Retain a compact table with candidate ID, format, input hashes, method/version,
endpoint, value and direction, applicability, coverage, and control-panel result.
For neural scorers, record batch composition and order when testing invariance.

Add unqualified annotations beside the existing ranking. Promote a filter only
after documenting its applicable domain and measured selection behavior.
Predicted pKa, electrostatic response, and solubility annotations support
computational review within those endpoints.

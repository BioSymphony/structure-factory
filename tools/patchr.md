# PATCHR

## Purpose

Use PATCHR to complete missing protein regions while conditioning on observed
coordinates. Its workflow combines template-constrained diffusion with local
refinement around generated/observed junctions.

## Public-Safe Status

The public registry records a reviewed MIT source revision. Structure Factory
does not bundle a PATCHR adapter, checkpoint, or execution route. Dependencies,
the selected model assets, and their terms must be reviewed for the intended
run.

## Coordinate-Preservation Contract

Do not reduce the structure to one “fixed” mask. Record three disjoint regions:

- observed atoms intended to remain fixed;
- observed boundary atoms permitted to move during refinement;
- atoms generated for missing residues.

Boundary refinement can move observed residues near a junction. Consequently,
an upstream exact-preservation statement for the constrained diffusion step is
not sufficient for a whole-pipeline claim. Measure output drift after a named
alignment, retain the transform, and report unaligned coordinates as well.

## Expected Evidence

- input structure hash and deposited-source provenance
- source, dependency, checkpoint, and runtime identities
- residue and atom maps before and after repair
- fixed, movable-boundary, and generated masks
- gap definitions and boundary-window settings
- missing-atom, chain-break, clash, bond-geometry, and parse checks
- fixed-region and boundary-region drift statistics
- generated-region confidence and uncertainty where available
- output hashes and an explicit partial/failure row for every input

A complete deposited structure makes a useful negative control for unnecessary
movement. Artificially masked structures test reconstruction under known
ground truth; they do not establish recovery of genuinely disordered regions.

## Supported-Input Caution

Verify molecule support separately for constrained diffusion and boundary
refinement. Support in one stage does not prove support in the other. Record
modified residues, ligands, covalent bonds, nucleic acids, missing atoms, and
alternate locations before running.

## Primary Source

- Repository: https://github.com/DeepFoldProtein/patchr

## Result Boundary

A repaired structure is a computational completion hypothesis. Preservation
metrics describe coordinate movement in the measured regions; they do not
establish that generated residues are experimentally correct, chemically
stable, or suitable for binding or free-energy calculations.

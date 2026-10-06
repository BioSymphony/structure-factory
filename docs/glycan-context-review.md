# Check Glycan Context Before Ranking Binder Poses

Evaluate binder access with a chemically qualified, target-only glycan
conformer bank. Reuse the same bank across candidate poses and controls so
the comparison measures each pose against the same sampled context.

Use the [binder comparison contract](binder-comparison-contract.md) to freeze
candidate identity, structural panels, and assessment policy.

## Qualify Preparation And Sampled Chemistry

Record the target construct, native residue mapping, glycosylation sites,
glycoforms, construction recipe, source version, and attachment geometry.
Verify elemental composition, donor-atom removal, bond topology, bond lengths,
sugar rings, root attachment, and amide geometry. Residue counts alone cannot
establish correct chemistry.

Optimize the attached glycans against the target before shield sampling.
The [Glycosylator preparation tutorial](https://glycosylator.readthedocs.io/en/latest/examples/glycosylate_protein.html)
describes attachment and subsequent conformational optimization. Retain
target coordinates and check chemistry again after optimization and sampling.
A distance-based objective alone supplies no complete conformational check.

Declare sampled bonds, root rotations, angular increments, repeats, and random
generators. Preserve the sampled conformers by hash. A seed assigned to one
generator provides no evidence that another generator consumed it.

## Track Coverage And Geometry Separately

Report these counts for each site and glycoform:

- Native accepted samples.
- Unique conformers passing independent chemistry and geometry checks.
- Selected bank members.
- Target-valid transfers into each structural pose.
- Binder-compatible conformers among the target-valid transfers.

Target-transfer failure and binder clashes answer different questions.
Incomplete site or glycoform coverage leaves the complete accessibility
comparison unresolved. Sampling fractions describe the declared finite bank;
they do not estimate native occupancy or binding probability.

Freeze physical criteria before reviewing candidate scores. If sampled
chemistry fails qualification, retain the coordinate diagnostics and prepare
a separately identified correction with prospective criteria.

## Retain Recognition And Broader Context

Display receptor contacts beside glycan clearance. A detached binder pose
can have high clearance and weak receptor contact support. Local glycan
compatibility and membrane accessibility require separate structural context.

Record uncertain domain orientation, membrane placement, and unsampled
glycoforms. Recompute the complete candidate aggregate for each declared
sensitivity variant, with missing strata visible.

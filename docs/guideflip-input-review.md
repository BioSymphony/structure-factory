# Review GuideFlip Inputs And Measurements

GuideFlip supports target-template masks, sequence-only target initialization,
hotspot conditioning, and scaffold sequence constraints. Check the prepared
features and final refolds to determine which operation a run executed.

Use this guide with the [GuideFlip card](../tools/guideflip.md) and the
[binder comparison contract](binder-comparison-contract.md).

## Keep Input Choices Separate

| Choice | Check |
| --- | --- |
| Sequence-only target | Verify target initialization and the target-template mask used during design |
| Full or partial template withholding | Inspect the resolved residue mask and its mapping to the input structure |
| Hotspot conditioning | Record the residues consumed by the objective and measure final contacts separately |
| Scaffold design | Verify fixed residue identities, designable positions, and gradients at those positions |
| Scaffold template withholding | Record the coordinate-template mask separately from sequence fixation |

Template exposure supplies prediction features. It does not freeze every
atom coordinate. A fixed scaffold sequence can therefore coexist with
different predicted coordinates.

The [pinned GuideFlip implementation](https://github.com/ykiiiiii/GuideFlip/blob/6fbb2fd48af208e2adc92901c90a97cbcd9cf252/guideflip/models/alphafold.py)
initializes a sequence-only target through monomer prediction, sets scaffold
fixed positions, and evaluates the decoded final sequence with five complex
models. Its binder-only checks also use five models. Retain each model and
its declared role.

## Interpret Scores By Their Definitions

Retain per-model interface confidence, directional PAE, chain mapping, and
score aggregation. GuideFlip's final minimum-PAE reducer takes the lowest
cross-chain entry from either direction for each model, then averages those
minima. That value describes a small part of the interface; whole-interface
PAE needs a separate calculation.

For structural consistency, record the reference pose, atom selection,
residue correspondence, and alignment. Agreement with a generated design
pose measures consistency with that prediction. An experimentally determined
binding mode supplies a different reference.

Check every final refold against the decoded final sequence. Keep saved
generation poses distinct when they represent an earlier sequence state.
Record the actual native acceptance thresholds and any disabled filters.

Inspect interchain geometry across all final models. A short heavy-atom
distance needs chemical interpretation and a declared clash calculation.
High interface confidence does not resolve an incompatible atomic contact.

## Count Designs And Compare Methods

Report trajectories, distinct final sequences, complex refolds, binder-only
refolds, and native passes separately. Ten refolds of one sequence evaluate
one design. Repeated execution of the same design on another provider tests
portability rather than increasing the distinct-design denominator.

For a GuideFlip–BindCraft2 comparison, match target exposure, binder length,
seeds, trajectory count, redesign fanout, and final evaluation. Record
gradient compatibility separately from forward-inference compatibility
when assessing an accelerated runtime. A source-level optimization proposal
needs an implemented, measured comparison before a speedup claim.

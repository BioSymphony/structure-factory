# Binder Comparison Contract

Freeze the method, cohort, and assessment policy before comparing design arms.
Use this checklist with the [round guide](binder-lane-round.md) and
[prediction handoff contract](prediction-handoff-contract.md). These are
preparation and review requirements for a selected runtime.

## Method identity

For each arm, record:

- source revision, checkpoint hashes, runtime identity, and precision
- binder format and length policy, native protocol, and configuration overrides
- target construct, structure hash, chain selection, crop, and residue mapping
- site-conditioning mode and the resolved residues or feature-mask summary
- sequence designer, sequence policy, and children per parent backbone
- generation, sequence-design, prediction, refinement, and filtering stages
  actually executed, plus any omitted native stages
- requested seeds, native seed keys, and evidence of seed delivery

Validate the resolved native configuration. For a site-conditioned arm, require
that the selected interface is nonempty, maps to available target residues,
and produces the intended conditioning mask. Retain the parsed mapping or
feature summary from a preparation check. A request's hotspot list alone does
not establish which list or mask a runtime consumed.

Preserve the target's declared sequence and observed coordinate coverage
separately. Record missing coordinates, insertion codes, and the mapping between
predictor positions and native residue identifiers. Hash any intentionally
cropped sequence as its own construct. Attach the actual designed sequence to
its parent pose before sequence-sensitive scoring, and record CA-only,
backbone-only, or sidechain coordinate coverage.

## Cohort and quota

Declare whether the comparison holds parent-backbone count, unique-sequence
count, or compute budget fixed. Record the selection order, sibling admission,
duplicate policy, stopping rule, and handling of failed or uncertain attempts.

Report these counts separately for every arm:

| Count | Meaning |
| --- | --- |
| Attempted trajectories | Generation attempts, including failed and uncertain attempts |
| Emitted parent backbones | Structural parents available for sequence design |
| Sequence children | Sequence records linked to their parents |
| Unique sequences | Distinct sequences under the declared deduplication policy |
| Assessed sequences | Candidates with completed assessment artifacts |
| Assessed parent backbones | Distinct parents represented in completed assessments |
| Native passes | Candidates passing the declared native filters |
| Common-screen passes | Candidates passing the frozen common assessment policy |
| Families and selections | Diversity groups and the final selected set |

Sequence children sharing a parent remain linked in the analysis. An equal
unique-sequence quota can cover different numbers of parent backbones. State
that coverage when reporting pass rates and diversity.

## Assessment policy

Freeze the common predictor's model, checkpoint, construct, MSA posture, seeds,
sampling settings, confidence artifacts, score definitions, units, reducers,
and thresholds. Keep its results alongside each arm's native-filter outcomes.
Record exact hotspot contacts separately from contacts anywhere in the declared
target window.

Use [control calibration](binder-controls.md) to declare the calibration scope.
Match control construct, binder format, site context, predictor, and MSA posture
to the intended assessment. Record unresolved context differences and predictor
disagreement. If a required positive control fails a veto, retain the failure
and review that gate's qualification before interpreting candidate rejections.

For independent predictor comparisons, predeclare a representative sample that
includes rejected candidates as well as selected leads and controls. Preserve
each predictor's observations and seed-level outcomes. Report conclusions for
the executed method and assessed cohort.

## Recovery and changed arms

Keep raw artifacts, hashes, missing-confidence status, and incomplete assessment
rows. Recover completed generation outputs before considering repeat generation
after a parsing or transport failure.

A protocol, site, sampling, sequence-policy, or threshold change creates a new
arm identity. Retain earlier outcomes with their original configuration and
declare the new arm prospectively. Runtime acceleration checks remain attached
to their pinned model and operation; also validate the scientific inputs and
stage coverage of the accelerated arm.

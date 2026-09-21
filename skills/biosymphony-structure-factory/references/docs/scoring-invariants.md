# Scoring Invariants

Scores are comparable only when their identity and scale are explicit. Every
prediction or scoring row should carry the fields needed to interpret it
without relying on a filename, a column heading, or knowledge of the producing
runtime.

## Required Identity

Record:

- scientific model, checkpoint, and implementation/runtime
- input structure and confidence-sidecar hashes
- candidate, target, chain, and residue mapping
- score name, definition, direction, range, and units
- raw value and any normalized value
- normalization formula and implementation version
- seed, sample index, aggregation rule, and failure policy

An implementation change does not create a new scientific predictor when the
model and checkpoint remain the same. It does create a new runtime identity
that must remain visible in provenance and performance comparisons.

## Scale Rule

Never infer a confidence scale from a field name. For example, two pLDDT
producers may emit the same quantity on `0..1` and `0..100` scales. Store
the raw value with `scale_min` and `scale_max`, then normalize once in a
named scoring step:

```text
normalized = (raw - scale_min) / (scale_max - scale_min)
```

Reject a row when the declared range is invalid or the raw value lies outside
it. Preserve the raw value so normalization can be audited.

## Interface Metrics

Keep these distinctions visible:

- global confidence is not interface confidence;
- predicted confidence is not reference-based structural accuracy;
- a docking score is not binding affinity;
- a pose-validity check is not a target-specific interaction score;
- a score computed from PAE requires the exact matrix from the same sampled
  structure.

For chain-pair metrics, store both chain directions when the metric is
directional. Join the metric to the structure and sidecar by hashes, not stem
alone.

## Samples And Replicates

Do not treat multiple samples from one stochastic prediction as independent
predictors. Keep sample-level rows and declare the reduction used for ranking.
When comparing implementations, include a reseed or repeat arm so ordinary
sampling variation is not attributed to the runtime change.

## Failure Semantics

Missing, invalid, and filtered scores are separate states. Do not coerce them to
zero or exclude them silently. Count them in the stage closeout and apply the
same failure policy to every comparison arm.

See [Confidence Sidecars](confidence-sidecars.md) for the artifact requirements
under these scores.

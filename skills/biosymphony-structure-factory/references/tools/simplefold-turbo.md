# SimpleFold-Turbo

## Purpose

Evaluate TeaCache acceleration for the Apple SimpleFold model family.
SimpleFold-Turbo reuses intermediate model evaluations during sampling. Treat
it as an inference implementation of SimpleFold, not as an independent
predictor.

## Public-Safe Status

The public registry pins a reviewed upstream source revision and records the
same model-asset terms as Apple SimpleFold. The repository supplies no bundled
adapter, model assets, or executable route.

The upstream project reports substantial acceleration on Apple hardware. Those
measurements do not establish speed on a different backend, end-to-end savings,
or unchanged scientific output for another model, sequence distribution, or
sampling configuration.

## Minimum Comparison

Use three matched arms:

1. the selected Apple SimpleFold baseline;
2. the Turbo implementation with caching disabled;
3. the same Turbo implementation with caching enabled.

Hold the model assets, input, timestep schedule, noise, seed, sample count,
steps, `tau`, backend, device, dtype, confidence setting, and output format
constant. The first comparison separates fork-level changes from cache effects.

## Evidence To Save

- source and model-asset hashes
- timestep schedule and RNG settings
- cache threshold and every reuse decision
- actual model-forward count
- cold and warm timings with the timing boundary named
- parse, sequence, chain, coordinate, and geometry checks
- output hashes and same-seed coordinate comparisons
- repeated-seed and repeated-input checks when state isolation matters

Synchronize pending GPU or MLX work before recording elapsed time. Separate
asset loading, sequence embedding, structure generation, optional confidence
prediction, and export.

## License And Data Gates

The fork's code is MIT. Released Apple model assets use Apple's separate
research model license. Record the intended use before acquiring or using the
assets. Keep checkpoints, input sequences, generated structures, and runtime
logs outside public git.

## Primary Sources

- Repository: https://github.com/usnistgov/simplefold-turbo
- Apple SimpleFold: https://github.com/apple/ml-simplefold
- Upstream TeaCache proposal:
  https://github.com/apple/ml-simplefold/pull/53

## Result Boundary

A cache comparison can support a measured speed/output-difference statement for
the tested configuration. It does not establish experimental structure
accuracy, physical ensemble populations, binding, function, or general
equivalence across models and hardware.

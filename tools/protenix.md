# Protenix

## Purpose

Use Protenix for biomolecular complex prediction and confidence scoring.
Protenix-v2 is the exact Protenix variant in the published binder-study score
stack.

## Public Status

Reviewed 2026-09-22. The [pinned upstream README](https://github.com/bytedance/Protenix/blob/85767b811c40ed46e73a9b39519cf6bfca8701ba/README.md)
contains conflicting weight notices: its v2 release section restricts transfer
of v2 parameters, but its License section describes all parameters as Apache-2.0.
The source code has an Apache-2.0 license. Resolve the exact checkpoint's terms
before acquiring, running, hosting, or redistributing Protenix-v2 weights.
The registry and public adapter record use `protenix_v2_weight_terms_review`.

The public adapter also applies this review gate to an unqualified Protenix
selection until its checkpoint identity is resolved. A v1 route needs its own
explicit model and terms record. Record v1 and v2 as separate model identities. Runtime requirements include the
source revision, parameter hash, MSA route, GPU, and validated adapter.

## Routes

- Install the upstream package and run its CLI locally or in a reviewed GPU
  container.
- Bind the same CLI to a GPU VM, pod, serverless function, HPC job, or hosted
  service.
- Use `protenix-v2` for an exact published-stack arm. Record another model name
  as a deliberate variant or swap.

The upstream command shape is `protenix pred -i <input.json> -o <output> -n
protenix-v2`. Check the installed version's help before execution because the
package and model catalog can change.

## Inputs And Outputs

Record the input assembly, chain and entity types, template policy, MSA route,
model identity, seed set, and source revision. Preserve predicted structures,
confidence JSON, PAE data when available, logs, output counts, and hashes.

Use ipSAE and scDockQ as separate interface-scoring operations. Do not merge a
Protenix confidence field and a derived interface score under one metric name.

## References

- Upstream repository: https://github.com/bytedance/Protenix
- Public workflow identity:
  [`published-binder-comparison-workflow.json`](../references/published-binder-comparison-workflow.json)

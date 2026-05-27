# Schemas

Canonical JSON schemas live under `modules/schemas/`.

Use them to validate public campaign and artifact surfaces such as:

- active-learning tranches
- artifact indexes
- candidate reports
- validation ledgers
- cloud shard ledgers
- provider runs
- receptor ensembles
- screening manifests and results
- stage progress

The root `schemas/` directory exists as a stable discovery pointer for public users and packaging metadata.

Some compatibility schemas include older machine values such as `candidate`, `processed`, `fixture_or_demo`, `validated`, or `publishable`. Public docs and closeouts should translate those through [`../docs/result-boundaries.md`](../docs/result-boundaries.md).

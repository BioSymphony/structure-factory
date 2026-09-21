# Reproducibility Checks

Two small, dependency-free checks cover failure modes that ordinary unit tests
do not detect.

## Direct Dependency Pins

```bash
make pin-liveness-check
```

This inventories exact Git and PyPI pins in tracked operational text files,
excluding test fixtures, and resolves them against their primary hosts. It
fails for an unreachable repository, missing Git ref, or missing PyPI release.
Local-version pins such as CUDA wheels are reported as alternate-index records
because PyPI is not their authoritative index.

The check covers direct pins only. It does not inspect a package's dependency
metadata, lock a dependency graph, or prove that a fresh environment installs.
Use a clean-image installation test for that boundary.

For an offline inventory:

```bash
python3 scripts/structure_factory/check_pinned_dependencies_resolve.py \
  --repo-root . --json
```

## Output-Tree Census

```bash
python3 scripts/structure_factory/output_tree_census.py \
  path/to/first-output path/to/second-output --json
```

The command partitions every regular, non-symlink file in the union of two
trees into identical, differing, only-in-left, and only-in-right sets. It exits
zero only for byte-identical trees. This distinguishes a deterministic replay
from changed output and from missing or colliding paths.

Run the census on private artifact storage when outputs contain generated
structures or private inputs. Commit only compact, public-safe summaries that
follow the repository's result boundaries.

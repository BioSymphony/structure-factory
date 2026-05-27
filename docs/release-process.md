# Release Process

This repo is staying local for now. These steps describe the future public switch.

## Local Release Gate

```bash
make clean
make public-switch-check
make secret-scan
```

Review large files:

```bash
find . -path ./.git -prune -o -type f -size +1M -print
```

Review status:

```bash
git status --short --branch
```

## Clean-History Requirement

A current-tree scrub is not enough for a public repository. Before publishing, create a clean root commit, squash export, or recreated public repository so private/generated artifacts are not recoverable from history.

## Package Boundary

The Python package installs the `bsf` CLI. The repo assets are equally important:

- skills
- examples
- recipes
- task packs
- schemas
- docs
- templates
- RunPod/cloud contract templates

`MANIFEST.in` keeps those assets available in source distributions. Git checkout remains the recommended install path for agent use.

## Do Not Publish

Do not publish if any of these are present:

- secrets, tokens, signed URLs, provider IDs, or license files
- private biological data or unpublished sequences
- generated structure archives or raw maps
- live provider launch payloads
- private tracker URLs or local workstation paths
- history that still contains removed private/generated artifacts

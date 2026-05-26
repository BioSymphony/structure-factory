# Contributing

Thanks for helping improve `biosymphony-structure-factory`.

## Ground Rules

- Public-safe synthetic or public-accession examples only.
- Do not add private biological data, generated structure archives, provider logs, credentials, or local operator notes.
- Keep claim levels explicit.
- Keep validators dependency-free at runtime unless an optional adapter is clearly separated.
- Prefer compact ledgers and manifests over large generated artifacts.
- Run `make release-check` before opening a pull request.

## Adding A Campaign Example

1. Create `examples/<campaign-id>/`.
2. Add `campaign-manifest.json`.
3. Add a compact target-window or input dossier.
4. Add `stage-contract.json` if the example has long-running or GPU stages.
5. Add `candidate-jury.example.json` only when claim levels and evidence modes are clear.
6. Add `README.md` describing scope, public data sources, and non-claims.
7. Run `make release-check`.

## Adding An Issue Pack

Issue packs should stay tracker-neutral. Use IDs like `BSF-BINDER-W00` rather than private tracker IDs. A private workflow can map those IDs to Linear, GitHub Issues, or another system after public validation.

## Adding A Tool Card

1. Add `tools/<tool-or-lane>.md`.
2. Record public docs posture, likely runtime posture, and review caveats.
3. Link current primary sources, but avoid asserting permanent license facts.
4. Do not include accepted-license records, private installer URLs, credentials, binaries, or weights.
5. Run `make registry-check` and `make release-check`.

## Changing Schemas Or Validators

- Keep `src/biosymphony_structure_factory` dependency-free.
- Add focused tests under `tests/`.
- Keep errors strict for public-safety blockers and warnings for optional capability gaps.
- Update `docs/cli-reference.md` when CLI behavior changes.

## Public-Safety Review

Before opening a pull request, run:

```bash
make clean
make release-check
make public-contract-check
make secret-scan
```

If `gitleaks` is unavailable locally, say so in the PR and rely on CI or a maintainer to run it before release.

## Style

- ASCII text by default.
- Stdlib-only runtime code.
- Small, deterministic tests.
- Warnings for guidance gaps, errors for public-safety or structural blockers.

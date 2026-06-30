# CLI Reference

The `bsf` CLI is dependency-free and intended to run in local development, CI, and agent sandboxes.

Install it with:

```bash
python -m pip install -e .
```

## `bsf scaffold-campaign`

Create a campaign skeleton.

```bash
bsf scaffold-campaign .runtime/my-target-demo \
  --campaign-id my-target-demo \
  --target-label "A2A receptor" \
  --public-accession "PDB:5G53" \
  --window "TM6 activation microswitch" \
  --mode binder-design
```

Modes:

- `binder-design`
- `model-comparison`
- `structure-mapping`
- `screening`

The command rejects obvious release blockers such as private workstation paths, private tracker IDs, assigned credential-like values, and literal provider resource IDs. It writes only compact text and JSON control-plane files.

## `bsf validate`

Validate a public campaign example.

```bash
bsf validate examples/pd-l1-binder-design-public
```

The validator checks public/privacy posture, result boundaries, target accession/window, lane boundaries, expected artifacts, stage contract fail-closed posture, and candidate ranking source posture.

## `bsf issue-dry-run`

Render tracker-neutral task drafts for a validated campaign. The issue plan is
mode-aware for `binder-design`, `model-comparison`, `structure-mapping`, and
`screening` campaign manifests.

```bash
bsf issue-dry-run examples/pd-l1-binder-design-public --out .runtime/pd-l1-issues
```

The output is ignored by git. Review it before importing into Linear, GitHub Issues, Notion tasks, or another tracker. The generated task IDs use mode-specific prefixes such as `BSF-BINDER-*`, `BSF-MODEL-*`, `BSF-MAP-*`, and `BSF-SCREEN-*`.

## `bsf audit`

Scan the repo tree for public-release blockers.

```bash
bsf audit .
```

The audit rejects common privacy and security hazards:

- private workstation paths
- private tracker IDs and tracker URLs
- assigned credential-like values
- literal provider resource IDs
- generated candidate sequences
- generated/heavy structural biology file suffixes
- public bridge manifests with embedded launch payloads or real approvals

## `bsf harness-check`

Verify the public skill repo shape.

```bash
bsf harness-check .
```

This checks that the README, skill files, public docs, task pack, RunPod posture, tool cards, templates, and release guidance expected by BioSymphony users are present and internally linked.

## `bsf catalog`

Summarize what the repo can do in a machine-readable JSON map or a human-readable
Markdown index.

```bash
bsf catalog .
bsf catalog . --out .runtime/public-capability-catalog.json
bsf catalog . --format markdown
bsf catalog . --format markdown --out .runtime/public-capability-catalog.md
```

The catalog lists task recipes, campaign modules, public examples, task packs,
stage contracts, provider profiles, recipes, and starter commands. It is
intended for fresh users and agents that need to choose an entry point without
reading the whole repository. Use JSON for automation and Markdown for reviews,
READMEs, or agent handoffs.

## `bsf doctor`

Run the three fastest local confidence checks for a fresh public checkout:
`harness-check`, `audit .`, and validation of the default public campaign.

```bash
bsf doctor .
```

Use `--example` to validate a different repo-relative campaign scaffold:

```bash
bsf doctor . --example .runtime/my-target-demo
```

The command emits one JSON summary with check results and next local commands. It does not call provider APIs, download data, create tracker issues, or mutate remote state.

## Make Targets

Common local targets:

```bash
make release-check
make catalog
make catalog-md
make read-only-audit
make public-contract-check
make public-switch-check
make clean
```

`make public-switch-check` is the strongest local public gate. It is still a current-tree check; public publication also requires a reviewed history path.
Use `make read-only-audit` when a reviewer wants a no-write confidence check
for the CLI harness, public documentation references, and non-launching RunPod
templates.

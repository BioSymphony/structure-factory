# Standalone Agent Workflow

You can use Structure Factory without BioSymphony private infrastructure, Linear, RunPod, or any paid provider account.

Use [`workflow-map.md`](workflow-map.md) when you want to decide whether to stay local, create tracker-neutral issues, or prepare a cloud/provider contract.

## Copyable Agent Prompt

```text
Use the BioSymphony Structure Factory skill. Work only in the local scaffold or public examples I name. Keep inputs public or synthetic, cap claims at computational_candidate, do not launch remote compute, and run bsf validate plus bsf audit before closeout.
```

## Local-Only Loop

1. Install the CLI:

```bash
python -m pip install -e .
```

2. Scaffold a campaign:

```bash
bsf scaffold-campaign .runtime/a2a-demo \
  --campaign-id a2a-demo \
  --target-label "A2A receptor" \
  --public-accession "PDB:5G53" \
  --window "TM6 activation microswitch"
```

3. Ask an agent to use the Structure Factory skill and edit only the scaffold, docs, or examples you approve.

4. Validate:

```bash
bsf validate .runtime/a2a-demo
bsf audit .
make release-check
```

5. If the scaffold becomes a public example, move it under `examples/<campaign-id>/` and keep all generated outputs outside git.

## Tracker-Neutral Issues

For GitHub Issues or another public tracker, use:

- `templates/github-issue.md`
- `packs/issue-packs/binder-design-fast-path-v0/`
- `bsf issue-dry-run`

The public issue format should include target, accession, claim ceiling, owned paths, validation commands, and explicit non-claims. It should not include private data, provider IDs, private tracker URLs, or execution credentials.

## Without RunPod

RunPod files in this repo are examples of the execution contract. You can still use the repo for:

- target-window dossiers
- model-jury plans
- public data checklists
- claim ledgers
- issue packs
- local fixture runs
- provider-neutral stage contracts

Keep `operator gate required: yes` on any future remote, GPU, license-gated, or cost-bearing work.

## Without Linear

Linear is not required. Use `bsf issue-dry-run` to produce Markdown drafts, then move them into GitHub Issues, Notion, a project board, or plain files. Preserve the useful parts:

- target/accession and claim ceiling
- owned paths
- expected artifacts
- validation commands
- provider and operator-gate status
- dependencies and risk notes
- explicit non-claims

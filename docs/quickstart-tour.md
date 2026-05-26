# Quickstart Tour

This tour shows the public-safe path from a fresh checkout to a validated campaign scaffold. It does not require a provider account, GPU, private image, model weights, or credentials.

![Three ways to start](assets/newcomer-paths.svg)

Text equivalent: choose the CLI for a five-minute local scaffold, the agent skill for planned agent work, or recipes for tested workflows.

For the full local-to-Linear-to-cloud ladder, see [`workflow-map.md`](workflow-map.md).

## What You Should Have After Each Step

| Step | Time | Useful Result |
| --- | --- | --- |
| Install and checks | 5 minutes | You know the public CLI, example campaign, and skill surface are intact |
| Scaffold | 10 minutes | You have a target/data contract, stage contract, and claim ledger in `.runtime/` |
| Agent review | 30 minutes | You have a better dossier and issue plan without remote compute |
| Issue dry-run | 60 minutes | You have tracker-neutral work items for Linear, GitHub Issues, or another queue |
| Provider prep | Later | You have a non-launching cloud contract ready for operator review |

## Pick A Starting Mode

| Mode | Use When | First Step |
| --- | --- | --- |
| Local CLI | You want to try the repo in minutes | Run `bsf scaffold-campaign` into `.runtime/` |
| Agent skill | You want Codex or another agent to plan the work | Ask it to use the Structure Factory skill |
| Recipe | You want a known workflow shape | Start from [`recipes/`](../recipes/) |

## 1. Install Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Check that the command line entry point is available:

```bash
bsf --help
```

## 2. Run The Light Local Checks

```bash
bsf --help
bsf doctor .
bsf catalog .
bsf catalog . --format markdown
bsf validate examples/pd-l1-binder-design-public
make read-only-audit
make harness-check
```

These checks confirm the CLI is installed, both JSON and Markdown catalog views render, the public PD-L1 example validates, the public audit is clean, and the agent/skill harness files are present. The catalog includes task recipes so a new agent can choose a planning, issue-draft, release-review, or cloud-prep path without scanning the full repo. `make read-only-audit` avoids `.runtime/` writes for reviewers. Save `make release-check` and `make public-switch-check` for release preparation or repo handoff.

## 3. Scaffold A Public-Safe Campaign

Write the scaffold to ignored runtime space first:

```bash
bsf scaffold-campaign .runtime/my-target-demo \
  --campaign-id my-target-demo \
  --target-label "A2A receptor" \
  --public-accession "PDB:5G53" \
  --window "TM6 activation microswitch"
```

The scaffold creates:

- `campaign-manifest.json`
- `target-window-dossier.json`
- `stage-contract.json`
- `claim-ledger.md`
- `README.md`

Validate it:

```bash
bsf validate .runtime/my-target-demo
bsf audit .
```

## 4. Use It With An Agent

Copy this prompt after the scaffold exists:

```text
Use the BioSymphony Structure Factory skill. Review .runtime/my-target-demo, improve the target-window dossier, stage contract, issue plan, and claim ledger. Keep it public-safe, do not launch remote compute, and run bsf validate plus bsf audit when done.
```

For more prompts, see [`docs/use-cases.md`](use-cases.md).

## 5. Turn The Scaffold Into Work

For a real public example, move the scaffold under `examples/<campaign-id>/` only after:

- every input is public accession metadata or synthetic fixture data
- expected artifacts are compact and text-based
- long-running or GPU work has an operator gate
- no generated structures, raw data, provider logs, private paths, or credentials are committed
- every claim is capped to the evidence present

Then generate tracker-neutral issue drafts:

```bash
bsf issue-dry-run examples/<campaign-id> --out .runtime/<campaign-id>-issues
```

Those drafts are mode-aware: binder-design, model-jury, structure-dossier, and screening campaigns get different issue prefixes and acceptance criteria. They can be imported into Linear, GitHub Issues, Notion tasks, or another tracker. For Linear/Symphony, keep the routing label, provider fields, claim ceiling, owned paths, dependencies, validation commands, and `<!-- symphony:schema -->` block intact.

## 6. Before Any Remote Run

Public launch templates are intentionally non-launchable. Before using RunPod, AWS Batch, SSH/HPC, or any cloud GPU path, create an operator-gated runtime packet outside public git with:

- explicit authorization
- budget and runtime cap
- cleanup policy
- immutable source reference
- runtime-secret references
- expected artifacts and hashes
- stage-progress ledger
- closeout and downgrade policy

Public git should keep only the contract, not the live credentials or provider state.

A concrete no-launch provider-prep pass looks like:

```bash
make runpod-public-template-check
make runpod-scope-check
SMOKE_MANIFEST=runpod/launch-manifests/no-download-smoke.json make launch-preflight
make launch-bundle
```

The output is an ignored review bundle under `.runtime/`. Real provider IDs, credentials, approvals, logs, fetched artifacts, cost reports, and cleanup proof stay outside public git.

For cloud/provider details, read [`compute-backends.md`](compute-backends.md) and [`runpod-stack.md`](runpod-stack.md). For Linear/Symphony issue flow, read [`linear-orchestration.md`](linear-orchestration.md).

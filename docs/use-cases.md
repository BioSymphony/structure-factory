# Use Cases

This guide gives users and their agents copyable prompts and concrete starting points for running real structural biology missions through Structure Factory. Use it when you want an agent to take a structural biology idea and produce a scaffolded campaign, issue pack, dossier plan, or provider-ready contract that other workers can finish.

Structure Factory is the control plane around structural biology campaigns. It helps a user and their agents plan, validate, package, and review computational work end-to-end. Binding, activity, safety, efficacy, selectivity, and therapeutic value are confirmed through wet-lab and clinical processes downstream of the repo.

For a route map across local prep, issue trackers, and cloud or provider execution, start with [`workflow-map.md`](workflow-map.md).
For claim vocabulary and evidence-mode examples, use [`claim-and-evidence.md`](claim-and-evidence.md).
For a capability-by-capability map, use [`capabilities.md`](capabilities.md).

## Copyable Agent Prompts

## Capability Menu

| Capability | Ask For This | Start Here |
| --- | --- | --- |
| Binder design | target-window dossier, generation lanes, cofold jury, claim ledger | [`examples/pd-l1-binder-design-public`](../examples/pd-l1-binder-design-public) |
| Protein design lane | Genie/RFdiffusion-style generation plan plus Boltz/Chai-style triage | [`tools/`](../tools/) and [`docs/tooling-and-licensing.md`](tooling-and-licensing.md) |
| Model jury | compare predicted/deposited models, preserve failures, cap claims | [`docs/claim-and-evidence.md`](claim-and-evidence.md) |
| GPCR/state atlas | receptor/state issue waves, deposited evidence, prediction/render contracts | `bsf scaffold-campaign --mode structure-dossier` plus [`tools/cofold-scoring-stack.md`](../tools/cofold-scoring-stack.md) |
| PDB/EMDB evidence dossier | public accession provenance, validation plan, report outline | [`recipes/map-model-dossier-public-data.md`](../recipes/map-model-dossier-public-data.md) |
| Screening and active learning | fanout, shard ledgers, result schemas, candidate dossiers | [`examples/screening-superpowers`](../examples/screening-superpowers) |
| Cloud/GPU prep | provider profiles, no-launch templates, preflight, closeout checks | [`docs/compute-backends.md`](compute-backends.md) |
| Linear/Symphony handoff | tracker-neutral issue packs with dependencies and validation commands | [`docs/linear-orchestration.md`](linear-orchestration.md) |

### Binder-Design Triage From A Public Interface

Use when you have a public structure and want a bounded campaign plan before generation or GPU work.

```text
Use the BioSymphony Structure Factory skill. Create a public-safe binder-design campaign scaffold from PDB 4ZQK. Define a target-window dossier, generation lanes, cofold/model-jury lanes, expected artifacts, validation commands, and non-claims. Keep all outputs local, do not launch remote compute, and cap claims at computational_candidate.
```

Suggested local commands:

```bash
bsf scaffold-campaign .runtime/pd-l1-binder-demo \
  --campaign-id pd-l1-binder-demo \
  --target-label "PD-L1 public interface demo" \
  --public-accession "PDB:4ZQK" \
  --window "public PD-1/PD-L1 interface window" \
  --mode binder-design
bsf validate .runtime/pd-l1-binder-demo
bsf audit .
```

Good output includes:

- `campaign-manifest.json` with public input scope, lanes, and claim ceiling
- `target-window-dossier.json` with accession, chain/window, and uncertainty notes
- `stage-contract.json` with fail-closed stages and expected evidence
- `claim-ledger.md` that separates planning evidence from non-claims
- tracker-neutral issues only after the scaffold is reviewed

### Public PDB/EMDB Evidence Dossier

Use when you want a reviewable plan for a deposited public PDB/EMDB structure, map, or model evidence package.

```text
Use the Structure Factory skill. Turn this public PDB/EMDB accession into a deposited-evidence dossier plan. Include accession provenance, expected artifacts, figure/report outline, validation commands, stage contracts, downgrade conditions, and a claim ledger. If raw cryo-EM processing or reconstruction is requested, produce a CryoCore handoff contract instead of treating that work as Structure Factory-owned. Do not download raw data or launch remote compute unless I explicitly authorize it later.
```

Start from:

- [`recipes/map-model-dossier-public-data.md`](../recipes/map-model-dossier-public-data.md)
- [`examples/empiar-10204-v0`](../examples/empiar-10204-v0)
- [`docs/agentic-biology-harness.md`](agentic-biology-harness.md)

Good output includes a compact public plan, not raw movies, reconstruction outputs, generated maps, private structures, or overconfident interpretation.

### GPCR Or Multimer State Atlas

Use when you want a receptor/state campaign split into deposited-structure evidence, prediction lanes, alignment/switch reports, render contracts, and claim-bounded synthesis.

```text
Use the Structure Factory skill. Plan a GPCR activation-state atlas from public PDB accessions. Split work by receptor and state, include deposited-structure dossiers, Boltz/MPNN-style prediction lanes, render contracts, issue dependencies, validation commands, and claim ceilings. Do not launch remote compute.
```

Start from:

- `bsf scaffold-campaign --mode structure-dossier` for the scaffold shape
- [`tools/cofold-scoring-stack.md`](../tools/cofold-scoring-stack.md), [`tools/proteinmpnn.md`](../tools/proteinmpnn.md), [`tools/chimerax-peptide-viz.md`](../tools/chimerax-peptide-viz.md)
- [`docs/compute-backends.md`](compute-backends.md)
- [`docs/linear-orchestration.md`](linear-orchestration.md)

Good output is a wave plan and evidence contract. Runtime-specific predictions, renders, and generated structures stay outside public git until summarized safely.

### Screening Fixture And Active Learning

Use when you want a local synthetic fixture that demonstrates sharding, result schemas, fanout estimates, and candidate triage without storing real screening results.

```text
Use the Structure Factory skill. Run the public screening-superpowers fixture locally, explain the fanout estimate, check the result schema, and summarize what would need an operator gate before any real provider-backed screening run.
```

Suggested local commands:

```bash
make screening-fanout-estimate
make screening-fixture-run
make screening-results-check
make screening-schema-check
```

Start from:

- [`recipes/screening-superpowers-local-fixture.md`](../recipes/screening-superpowers-local-fixture.md)
- [`examples/screening-superpowers`](../examples/screening-superpowers)
- [`docs/screening-superpowers.md`](screening-superpowers.md)

Good output explains scale, schema shape, shard boundaries, and what remains synthetic or blocked.

### Provider Prep Without Launch

Use when you want RunPod, cloud, SSH/HPC, or local GPU readiness while keeping public git non-launchable.

```text
Use the Structure Factory skill. Prepare a provider-neutral execution contract for this campaign. Keep launch templates public-safe and non-launchable, use placeholders for provider IDs and runtime secrets, add budget/cleanup/operator gates, and run the public checks. Do not create pods, download raw data, or install license-gated tools.
```

Suggested local commands:

```bash
make runpod-public-template-check
make runpod-scope-check
SMOKE_MANIFEST=runpod/launch-manifests/no-download-smoke.json make launch-preflight
make launch-bundle
make contract-self-check
```

Start from:

- [`recipes/runpod-no-download-smoke.md`](../recipes/runpod-no-download-smoke.md)
- [`docs/compute-backends.md`](compute-backends.md)
- [`docs/runpod-stack.md`](runpod-stack.md)
- [`runpod/README.md`](../runpod/README.md)

Good output is a reviewed contract and checklist. The review bundle is written under ignored `.runtime/`. Live provider packets, pod IDs, registry auth, approval state, logs, and fetched artifacts stay outside public git.

### Linear Or GitHub Issue Pack From A Campaign

Use when a campaign is too large for one agent turn and needs durable tasks, dependencies, and review gates.

```text
Use the Structure Factory skill. Turn this public-safe campaign into tracker-neutral issues suitable for Linear or GitHub Issues. Include target/accession, provider profile, operator-gate status, claim ceiling, owned paths, dependencies, validation commands, expected artifacts, risk notes, and a symphony:schema block. Do not include private tracker URLs, provider IDs, credentials, or runtime logs.
```

Suggested local commands:

```bash
bsf validate examples/pd-l1-binder-design-public
bsf issue-dry-run examples/pd-l1-binder-design-public --out .runtime/pd-l1-issues
python3 scripts/structure_factory/issue_check.py .runtime/pd-l1-issues --json
```

Start from:

- [`packs/README.md`](../packs/README.md)
- [`docs/linear-orchestration.md`](linear-orchestration.md)
- [`templates/github-issue.md`](../templates/github-issue.md)
- [`templates/linear-issue.md`](../templates/linear-issue.md)

Good output can be imported into Linear, GitHub Issues, Notion tasks, or another queue. Linear/Symphony users should preserve `sym:structure-factory`, wave labels, state policy, and parseable worker outcomes.

### Public-Release Safety Review

Use when you want an agent to check whether a campaign, docs update, or repo export is fit for public release.

```text
Use the Structure Factory skill. Review this repo for public-release safety and newcomer usefulness. Check README paths, docs, recipes, examples, issue packs, diagrams, provider templates, claim language, privacy markers, generated artifacts, and release gates. Make local fixes where safe, then run make public-switch-check.
```

Suggested local commands:

```bash
make release-check
make public-switch-check
bsf audit .
```

Start from:

- [`PUBLIC_RELEASE.md`](../PUBLIC_RELEASE.md)
- [`docs/public-switch-checklist.md`](public-switch-checklist.md)
- [`docs/privacy-and-security-model.md`](privacy-and-security-model.md)

Good output names exactly what changed, what checks passed, and what remains intentionally local or blocked.

### Tool And Lane Review

Use when you want an agent to decide whether a tool belongs in public docs, runtime setup, or an operator-gated execution lane.

```text
Use the Structure Factory skill. Review this proposed structure/design tool for public documentation. Classify it as public-docs-only, optional local runtime, provider-prep, or operator-gated execution. Add license/use-context caveats, expected artifacts, validation commands, and non-claims.
```

Start from:

- [`tools/README.md`](../tools/README.md)
- [`docs/tooling-and-licensing.md`](tooling-and-licensing.md)
- [`references/software-registry.yaml`](../references/software-registry.yaml)

Good output separates public documentation from actual install or execution authorization.

## Choosing The Right Path

| Goal | Use This First | Main Gate |
| --- | --- | --- |
| Try the repo in five minutes | [`docs/quickstart-tour.md`](quickstart-tour.md) | `make harness-check` |
| Understand the whole workflow | [`docs/workflow-map.md`](workflow-map.md) | choose local, tracker, or cloud-prep mode |
| Ask an agent to plan a campaign | [`docs/agent-recipes.md`](agent-recipes.md) | `bsf validate` and `bsf audit .` |
| Decide what a result may claim | [`docs/claim-and-evidence.md`](claim-and-evidence.md) | evidence mode plus claim level |
| Install the portable skill | [`docs/skill-install.md`](skill-install.md) | `make harness-check` |
| Run a public-safe fixture | [`recipes/`](../recipes/) | recipe-specific checks |
| Split work into issues | [`packs/README.md`](../packs/README.md) | `bsf issue-dry-run` |
| Prepare cloud/GPU work | [`docs/compute-backends.md`](compute-backends.md) | operator gate before execution |
| Publish or export | [`docs/public-switch-checklist.md`](public-switch-checklist.md) | `make public-switch-check` |

## Public-Safe Defaults

When in doubt, ask the agent to keep these defaults:

- public or synthetic inputs only
- local prep before provider work
- no remote launch without explicit operator authorization
- no credentials, provider IDs, private paths, raw datasets, generated structures, model weights, or logs in git
- claim ceiling set before tool lanes are proposed
- partial, missing, or unverifiable evidence downgraded instead of called success
- every closeout includes files changed, validation commands, evidence mode, claim level, and safety checks

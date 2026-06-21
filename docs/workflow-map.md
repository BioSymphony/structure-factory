# Workflow Map

Structure Factory turns a vague structural biology request into a reviewable work program that any agent or operator can pick up. The repo is the control plane around prediction models, wet-lab handoffs, and cloud launchers: manifests, task packs, provider contracts, stage ledgers, artifact expectations, result boundaries, and release gates.

Strong coding agents (Codex, Claude Code, Symphony or Linear workers, `/goal` orchestrators) can read the repo, inspect examples, write missing glue, and coordinate local or cloud resources directly. The repo gives those agents the biology-specific contracts and verification gates they share across workers and providers.

Public closeouts use `planning`, `public_demo`, `public_synthetic_demo`, `computational_candidate`, `insufficient_support`, or `blocked`.

![Public workflow ladder](assets/workflow-ladder.svg)

Text equivalent: local scaffold leads to a task pack, then a cloud contract, then an operator-gated run outside public git, then verified closeout.

## What You Get

| Starting Point | Useful Output | First Gate |
| --- | --- | --- |
| Public PDB/EMDB/UniProt accession | Target/data contract, result boundaries, expected artifacts | `bsf validate` |
| Binder-design idea | Target-window file, generation lanes, cofold/model-comparison plan | `bsf audit .` |
| GPCR or multimer-state idea | Receptor/state wave plan, structure lanes, prediction/render contracts | `make issue-dry-run-check` |
| Existing public structure | PDB/EMDB structure-mapping outline, provenance plan, review notes | `make release-check` |
| Raw cryo-EM processing request | CryoCore handoff contract, operator gates, expected downstream artifacts | `bsf audit .` |
| Screening or active-learning plan | Fixture run, fanout estimate, shard/result schemas | recipe-specific checks |
| Remote GPU need | Non-launching provider contract, budget/cleanup/operator gate | `make runpod-public-template-check` |
| Agent work program | Tracker-neutral issues for Linear, GitHub Issues, Notion, or another queue | `bsf issue-dry-run` |

## Timeboxed Paths

| Time | Goal | Commands Or Prompt | Result |
| --- | --- | --- | --- |
| 5 minutes | Prove the repo works locally | `bsf validate examples/pd-l1-binder-design-public` and `make harness-check` | Installed CLI and validated public example |
| 30 minutes | Draft a campaign | `bsf scaffold-campaign .runtime/my-demo ...` then ask an agent to use the Structure Factory skill | Target/data contract, stage contract, validation notes |
| 60 minutes | Turn it into reviewable work | `bsf issue-dry-run examples/<campaign-id> --out .runtime/<campaign-id>-issues` | Tracker-neutral task drafts with owned paths and validation commands |
| 2 hours | Prepare cloud/GPU readiness without launching | Run provider template, scope, and contract checks | Non-launching RunPod/cloud contract with explicit operator gates |
| Later, with approval | Execute a bounded provider run | Private/operator-gated launcher outside public git | Artifacts, hashes, cost/cleanup proof, and bounded closeout |

## Three Operating Modes

### Local-Only

Use this mode for learning, public examples, small fixtures, task drafting, and public-release review.

```bash
bsf scaffold-campaign .runtime/a2a-demo \
  --campaign-id a2a-demo \
  --target-label "A2A receptor" \
  --public-accession "PDB:5G53" \
  --window "TM6 activation microswitch"
bsf validate .runtime/a2a-demo
bsf audit .
```

Local-only work may create `.runtime/` scaffolds and compact reports. It must not commit private data, generated structures, raw datasets, model weights, provider logs, or credentials.

### Tracker-Coordinated

Use this mode when the work is bigger than one prompt and should be split across tasks.

```bash
bsf issue-dry-run examples/pd-l1-binder-design-public \
  --out .runtime/pd-l1-issues
```

Import or adapt the generated Markdown into Linear, GitHub Issues, Notion tasks, or another queue. For Linear/Symphony, keep `sym:structure-factory`, provider fields, result boundaries, owned paths, dependencies, validation commands, and the `<!-- symphony:schema -->` block.

### Cloud-Prepared

Use this mode when a campaign needs RunPod, AWS Batch, SSH/HPC, neocloud, or another GPU path.

Public git stores only non-launching contracts:

- provider profile
- stage contract
- budget/runtime expectations
- runtime-secret reference names
- expected artifacts
- input-audit and contract-self-check requirements
- cleanup and partial-output policy

Live provider packets, pod IDs, registry auth, accepted-license state, concrete placement, fetched artifacts, and logs stay outside public git.

## Cloud Execution Ladder

1. Define the biological contract locally: target, accession, result boundaries, source posture, and expected artifacts.
2. Choose the provider profile: RunPod, AWS Batch, local workstation, SSH/HPC, generic cloud, or neocloud.
3. Validate the public non-launching template with `make runpod-public-template-check` or the matching provider check.
4. Create an operator-gated runtime packet outside public git only after explicit authorization.
5. Before launch, require budget cap, runtime cap, immutable repo ref, image/bootstrap posture, runtime secrets by reference, stage ledger path, and cleanup policy.
6. After launch, provider `RUNNING` is not success. Require actual workload progress, artifacts, hashes, cost report, cleanup proof, and contract self-check.
7. Close the task with the weakest supported source posture and result boundary. Partial or missing outputs must be labeled honestly.

Copyable no-launch provider-prep commands:

```bash
make runpod-public-template-check
make runpod-scope-check
SMOKE_MANIFEST=runpod/launch-manifests/no-download-smoke.json make launch-preflight
make launch-bundle
```

After a private/operator-gated run, validate pulled artifacts from ignored storage with:

```bash
PROVIDER_ARTIFACT_ROOT=.runtime/provider-artifacts/<run-id> make provider-closeout-check
```

RunPod is the reference pod path in this repo. AWS Batch is the reviewed cloud-scale path. Other providers are useful when a user already has capacity, but they need the same input-audit, artifact, cleanup, and closeout gates.

## Linear And Symphony Ladder

1. Keep new or cost-bearing work in `Backlog`.
2. Activate only the current wave in `Todo`.
3. Start with one worker until Wave 0 validates the repo, workflow, issue contracts, and no-download manifests.
4. Give each task exact inputs, owned paths, dependencies, risk notes, validation commands, expected artifacts, operator-gate status, and result boundary.
5. Workers move work to `In Review` when validation is complete and artifacts are ready for review.
6. Trusted closeout moves provider-backed work to `Done` only after artifact fetch, hash validation, cost report, cleanup proof, and validation review.

Linear is not required. The same task contract can be used in GitHub Issues or another task system, but Linear/Symphony users get durable state transitions, dependency tracking, and parseable worker outcomes.

## Safety Boundary

The public repo should contain:

- accessions, manifests, schemas, templates, small fixtures, bounded reports, and validators
- non-launching cloud templates
- tracker-neutral task packs
- validation notes and result boundaries

The public repo should not contain:

- private paths, private tracker URLs, credentials, tokens, pod IDs, logs, accepted-license state, raw biological data, generated candidate structures, unpublished sequences, model weights, or large provider artifacts

Raw cryo-EM movie intake, EMPIAR subset execution, reconstruction, and map-to-model build execution are CryoCore-owned lanes. Structure Factory can record the public accession, handoff gates, expected downstream artifacts, and later structure-mapping plan.

Run `make public-switch-check` before publishing, sharing, or handing the repo to a fresh agent.

# Compute Backends

Structure Factory separates the control plane from the execution plane.

- Linear owns the scientific contract, dependencies, risk gates, and acceptance criteria.
- Symphony owns bounded worker dispatch and closeout comments.
- Structure Factory owns manifests, modules, validators, and evidence contracts.
- Compute providers only run a selected execution profile and emit artifacts.

RunPod Pods are the primary blessed remote path. AWS Batch GPU jobs are the blessed cloud scale path. Other backends, including neocloud and generic cloud VMs, must satisfy the same input-audit, artifact, cleanup, and contract-self-check rules before a worker can claim success.

For the newcomer route map, see [`workflow-map.md`](workflow-map.md). The public repository supports cloud planning and readiness checks, but real provider mutation belongs in a private/operator-gated execution packet after explicit approval.

## Public To Cloud Workflow

| Phase | Stored In Public Git | Stored Outside Public Git |
| --- | --- | --- |
| Local contract | campaign manifest, target-window dossier, claim ledger, stage contract | private target notes, unpublished sequences, local data |
| Tracker plan | tracker-neutral issue drafts, validation commands, risk notes | private tracker URLs, live comments with secrets, operator approvals |
| Provider prep | non-launching templates, provider profiles, scope checks, runtime-secret reference names | real pod IDs, concrete placement, accepted-license state, credentials |
| Provider run | expected artifact list, schema, closeout checklist | logs, raw outputs, generated structures, model weights, provider archives |
| Closeout | compact report, hashes, provenance summary, claim level | heavy artifacts and private evidence packets |

The useful public workflow is:

```text
local scaffold -> issue pack -> provider profile -> public template check -> private operator launch -> verified closeout
```

Provider `RUNNING`, scheduler success, or a process exit code is not enough. A cloud run is useful only after expected artifacts are fetched, parsed, hashed, scanned, cleanup is proven, and the claim ledger is updated.

## Setup Postures

The files, data, tools, and weights can be assembled in several valid ways. The chosen posture is an execution detail, not a different science contract.

| Posture | Where Setup Happens | Best Use | Required Guardrail |
| --- | --- | --- | --- |
| Public/prebuilt image | Pulled by provider | Open-default tools with redistributable binaries | Digest pin before real launch |
| Private image | GHCR/Docker Hub/registry | Fast cold start for reviewed private stacks | Runtime registry auth; no secrets in image layers |
| Runtime bootstrap | Pod boot or job prologue | Public base image plus pinned installs | Record commands, versions, and bootstrap risk |
| RunPod Network Volume bootstrap | One setup pod populates `/workspace/structure-factory/software` and caches | Blessed RunPod path when avoiding private registry auth or repeated weight downloads | Dedicated Structure Factory volume, idempotent bootstrap, verify on every pod |
| Local high-resource workstation | User machine | Small demos, GUI review, local-only campaigns | No large/raw downloads without explicit local authorization |
| SSH/HPC modules | Institutional cluster | Data or licenses must stay on site | Same artifact tree and self-check output |
| Generic cloud/neocloud volume | Provider volume or object store | Preferred adapter-ready cloud capacity beyond RunPod/AWS | Must preserve scoping, secrets, artifact export, and cleanup policy |

GHCR is not mandatory. It is one convenient private-image posture. For Structure Factory RunPod campaigns, a dedicated Network Volume plus public base image and runtime bootstrap is often cleaner because it avoids registry auth and avoids redistributing license-sensitive tools.

## Backend Classes

| Backend | Class | Intended Use | Status |
| --- | --- | --- | --- |
| RunPod | `pod` | No-download smoke, CryoCore handoff prep, gated tools, PDB/EMDB evidence dossiers, AI-design runtime | Blessed primary |
| AWS Batch | `batch_job` | Cloud scale lanes, multi-shard GPU jobs, RunPod fallback when AWS credentials/budget are authorized | Blessed cloud scale |
| Local workstation | `workstation` | Repo validation, figure review, small deposited-evidence checks, GUI review | Supported for prep/local-lite |
| SSH/HPC | `slurm_job` | Institutional GPU or CPU batch lanes where licenses/data stay on site | Adapter-ready |
| Generic cloud VM | `cloud_vm` | Bring-your-own GPU VM with mounted disk/object storage | Adapter-ready |
| Neocloud GPU pod | `gpu_pod` | Preferred RunPod-like GPU pod providers with private image and scratch volume support | Preferred adapter-ready |

## Required Provider Contract

Every provider profile should declare:

- `provider`
- `provider_class`
- `profile_id`
- `maps_campaign_profile`
- `workspace_root`
- `artifact_root`
- `secret_mode`
- `operator_gate_required`
- `execution_ready_requires`
- provider-specific storage, GPU, image, scheduler, or connection fields

Every provider must support the same evidence flow:

```text
manifest -> input_audit -> materialized inputs -> tool/run artifacts -> contract_self_check -> Linear outcome
```

## Non-Negotiable Success Rules

- Provider success is not scientific success.
- A submitted job, launched pod, passing process exit code, or `--full-run` flag is intent only.
- Real execution fails if required evidence contains `mock_gpu`, `mock_tools`, or `dry_run`.
- Raw-download profiles require explicit operator authorization, not just an environment default.
- Heavy data stays in the provider workspace, volume, or institutional storage. Git and Linear receive only manifests, small reports, provenance, hashes, and claim ledgers.

## Backend-Specific Notes

### RunPod

Use the concrete `runpod/` launch kit. RunPod is the reference pod provider and the blessed primary remote path. Keep image credentials and license secrets in RunPod runtime configuration. Write durable artifacts under `/workspace/structure-factory/runs/<run-id>/`.

For Structure Factory-owned volumes, use `STRUCTURE_FACTORY_RUNPOD_NETWORK_VOLUME_ID` in public docs/templates. Operator-gated concrete bridge manifests may carry the resolved owned volume ID after scope validation. Do not reuse sibling campaign volumes such as GeneCluster for writable state. Before paid mutation, run `make runpod-scope-check` and verify the target pod/volume appears in the Structure Factory manifest or pod ledger.

### AWS Batch

Use AWS Batch as the blessed cloud scale path when the issue declares AWS credentials, budget, job queue, compute environment, artifact export bucket, and cleanup evidence. AWS EC2 debug VMs are supported but are not blessed unless wrapped by the AWS Batch profile and the same input-audit and contract-self-check gates.

### Local Workstation

Use local execution for prep, validation, visual review, and tiny deposited-evidence or figure tasks. A user with substantial local CPU/GPU/storage may run larger lanes locally, but only when the issue declares local materialization paths, data-retention policy, and cleanup expectations. Do not download raw EMPIAR subsets locally unless a separate CryoCore-owned issue explicitly authorizes it. Local mock GPU is prep evidence only.

### SSH/HPC

Use when data or licenses must stay inside an institution. The adapter should generate a job script that writes the same artifact tree and self-check output. Scheduler success is not enough; the self-check must pass.

### Generic Cloud / Neocloud

Use when the provider can support public or operator-gated repo checkout, public images or private images with runtime registry auth, reproducible bootstrap, runtime secrets, scratch/persistent storage boundaries, and artifact export. These are preferred capacity options for users who already have access, but they remain adapter-ready until provider-specific launch tooling, scope checks, cleanup proof, and artifact export have been proven. RunPod remains the reference implementation for pod-style providers.

## AI-Design Selection Order

For Boltz and Genie-style AI design lanes, use this default order unless an issue says otherwise:

1. RunPod with the Structure Factory Network Volume or digest-pinned image.
2. AWS Batch for cloud scale or multi-shard fallback.
3. Neocloud or generic cloud VM when the user has provider capacity and accepts the adapter gate.
4. Local high-resource workstation only when the user declares sufficient GPU/storage and data-retention boundaries.

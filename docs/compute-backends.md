# Compute Backends

Structure Factory separates the control plane from the execution plane.

- Linear owns the scientific contract, dependencies, risk gates, and acceptance criteria.
- Symphony owns bounded worker dispatch and closeout comments.
- Structure Factory owns manifests, modules, validators, and validation contracts.
- Compute providers only run a selected execution profile and emit artifacts.

RunPod Pods are the default reviewed remote path. AWS Batch GPU jobs are the reviewed cloud-scale path. Modal serverless GPU functions support bounded canaries and small single-container fanouts. Lambda Cloud GPU VMs support ephemeral, no-persistent-filesystem canaries. Other backends, including generic cloud VMs and SSH/HPC, must satisfy the same input-audit, artifact, cleanup, and contract-self-check rules before a worker can close the run as successful.

For the newcomer route map, see [`workflow-map.md`](workflow-map.md). The public repository supports cloud planning and readiness checks, but real provider mutation belongs in a private/operator-gated execution packet after explicit approval.

## Public To Cloud Workflow

| Phase | Stored In Public Git | Stored Outside Public Git |
| --- | --- | --- |
| Local contract | campaign manifest, target-window file, validation notes, stage contract | private target notes, unpublished sequences, local data |
| Tracker plan | tracker-neutral task drafts, validation commands, risk notes | private tracker URLs, live comments with secrets, operator approvals |
| Provider prep | non-launching templates, provider profiles, scope checks, runtime-secret reference names | real pod IDs, concrete placement, accepted-license state, credentials |
| Provider run | expected artifact list, schema, closeout checklist | logs, raw outputs, generated structures, model weights, provider archives |
| Closeout | compact report, hashes, provenance summary, result boundary | heavy artifacts and private result packets |

The useful public workflow is:

```text
local scaffold -> task pack -> provider profile -> public template check -> private operator launch -> verified closeout
```

Provider `RUNNING`, scheduler success, or a process exit code is not enough. A cloud run is useful only after expected artifacts are fetched, parsed, hashed, scanned, cleanup is proven, and the validation notes are updated.

## Setup Postures

The files, data, tools, and weights can be assembled in several valid ways. The chosen posture is an execution detail, not a different science contract.

| Posture | Where Setup Happens | Best Use | Required Guardrail |
| --- | --- | --- | --- |
| Public/prebuilt image | Pulled by provider | Open-default tools with redistributable binaries | Digest pin before real launch |
| Private image | GHCR/Docker Hub/registry | Fast cold start for reviewed private stacks | Runtime registry auth; no secrets in image layers |
| Runtime bootstrap | Pod boot or job prologue | Public base image plus pinned installs | Record commands, versions, and bootstrap risk |
| RunPod Network Volume bootstrap | One setup pod populates `/workspace/structure-factory/software` and caches | Default RunPod path when avoiding private registry auth or repeated weight downloads | Dedicated Structure Factory volume, idempotent bootstrap, verify on every pod |
| Local high-resource workstation | User machine | Small demos, GUI review, local-only campaigns | No large/raw downloads without explicit local authorization |
| SSH/HPC modules | Institutional cluster | Data or licenses must stay on site | Same artifact tree and self-check output |
| Generic cloud/neocloud volume | Provider volume or object store | Preferred adapter-ready cloud capacity beyond RunPod/AWS | Must preserve scoping, secrets, artifact export, and cleanup policy |
| Modal serverless function | Function image built and run on Modal | Bounded GPU canaries and small fanouts without a long-lived pod | Declared max_containers, timeout, tags; committed Volume; fetched+hashed artifacts; app-stop cleanup |
| Lambda ephemeral GPU VM | Short-lived instance, no persistent disk | Single no-filesystem canaries with fast-terminate discipline | Egress + remote-archive hash + immediate terminate + post-terminate listing |

GHCR is not mandatory. It is one convenient private-image posture. For Structure Factory RunPod campaigns, a dedicated Network Volume plus public base image and runtime bootstrap is often cleaner because it avoids registry auth and avoids redistributing license-sensitive tools.

## Backend Classes

| Backend | Class | Intended Use | Status |
| --- | --- | --- | --- |
| RunPod | `pod` | No-download smoke, CryoCore handoff prep, gated tools, PDB/EMDB structure mapping, AI-design runtime | Default reviewed path |
| AWS Batch | `batch_job` | Cloud scale lanes, multi-shard GPU jobs, RunPod fallback when AWS credentials/budget are authorized | Reviewed cloud scale |
| Modal | `serverless_function` | Bounded single-function GPU canaries, small single-container fanouts, Volume-backed artifacts, tag-scoped billing | Reviewed neocloud |
| Lambda Cloud | `cloud_vm` | Ephemeral single-instance GPU canaries with no persistent filesystem; egress, hash, terminate | Reviewed neocloud |
| Local workstation | `workstation` | Repo validation, figure review, small deposited-structure checks, GUI review | Supported for prep/local-lite |
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

Every provider must support the same verification flow:

```text
manifest -> input_audit -> materialized inputs -> tool/run artifacts -> contract_self_check -> Linear outcome
```

## Non-Negotiable Success Rules

- Provider success is not scientific success.
- A submitted job, launched pod, passing process exit code, or `--full-run` flag is intent only.
- Real execution fails if required outputs contain `mock_gpu`, `mock_tools`, or `dry_run`.
- Raw-download profiles require explicit operator authorization, not just an environment default.
- Heavy data stays in the provider workspace, volume, or institutional storage. Git and Linear receive only manifests, small reports, provenance, hashes, and validation notes.

## Backend-Specific Notes

### RunPod

Use the `runpod/` launch kit for public templates, stage contracts, and preflight checks. RunPod is the reference pod provider and the default reviewed remote path. Keep image credentials and license secrets in RunPod runtime configuration. Write durable artifacts under `/workspace/structure-factory/runs/<run-id>/`.

For Structure Factory-owned volumes, use `STRUCTURE_FACTORY_RUNPOD_NETWORK_VOLUME_ID` in public docs/templates. Operator-gated provider packets may carry the resolved owned volume ID after scope validation. Do not reuse sibling campaign volumes for writable state. Before paid mutation, run `make runpod-scope-check` and verify the target pod/volume appears in the Structure Factory manifest or pod ledger.

### AWS Batch

Use AWS Batch as the reviewed cloud-scale path when the task declares AWS credentials, budget, job queue, compute environment, artifact export bucket, and cleanup proof. AWS EC2 debug VMs are supported but remain adapter-ready unless wrapped by the AWS Batch profile and the same input-audit and contract-self-check gates.

### Modal

Use Modal serverless GPU functions for bounded single-function canaries and small single-container fanouts. Declare `max_containers`, a timeout, run tags, and a committed Modal Volume up front. Closeout requires more than a function exit: capture provider logs with timestamps and function/container IDs, the app and history status JSON, a tag-scoped billing report, the committed Volume tree fetched locally with hashes, and `app stop` cleanup proof. Reference Modal credentials from an operator secret store or Modal secret refs only; never write tokens to the repo, tracker, logs, or artifacts. Profile: `modules/provider-profiles/modal/gpu-function-no-download.v1.json`.

### Lambda Cloud

Use Lambda Cloud GPU VMs for ephemeral, no-persistent-filesystem canaries: no persistent filesystem for the first canary, a short-lived single instance, SSH/SCP or object-store artifact egress, a remote-archive hash check, immediate termination, and an explicit post-terminate instance/filesystem listing before any success closeout. Lambda is more cost-exposed than RunPod because there is no auto-stop guardrail, so terminate fast. Profile: `modules/provider-profiles/lambda/gpu-vm-no-download.v1.json`.

### Local Workstation

Use local execution for prep, validation, visual review, and tiny deposited-structure or figure tasks. A user with substantial local CPU/GPU/storage may run larger lanes locally, but only when the task declares local materialization paths, data-retention policy, and cleanup expectations. Do not download raw EMPIAR subsets locally unless a separate CryoCore-owned task explicitly authorizes it. Local mock GPU is prep output only.

### SSH/HPC

Use when data or licenses must stay inside an institution. The adapter should generate a job script that writes the same artifact tree and self-check output. Scheduler success is not enough; the self-check must pass.

### Generic Cloud / Neocloud

Use when the provider can support public or operator-gated repo checkout, public images or private images with runtime registry auth, reproducible bootstrap, runtime secrets, scratch/persistent storage boundaries, and artifact export. These are preferred capacity options for users who already have access, but they remain adapter-ready until provider-specific launch tooling, scope checks, cleanup proof, and artifact export have been proven. RunPod remains the reference implementation for pod-style providers.

Lambda Cloud GPU VMs are now a reviewed neocloud path with their own profile and
the ephemeral-canary discipline described in the Lambda Cloud note above. Other
bring-your-own cloud VMs stay `generic_cloud` until they carry a profile and
validator coverage. Keep provider resource IDs, SSH key names, API credentials,
images, logs, costs, and raw artifacts outside public git.

## AI-Design Selection Order

For Boltz and Genie-style AI design lanes, use this default order unless a task says otherwise:

1. RunPod with the Structure Factory Network Volume or digest-pinned image.
2. AWS Batch for cloud scale or multi-shard fallback.
3. Modal serverless GPU functions for bounded canaries or small single-container fanouts.
4. Lambda Cloud GPU VMs for ephemeral, no-persistent-filesystem canaries.
5. Neocloud or generic cloud VM when the user has provider capacity and accepts the adapter gate.
6. Local high-resource workstation only when the user declares sufficient GPU/storage and data-retention boundaries.

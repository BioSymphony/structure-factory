# Install Structure Factory As A Sidecar

Structure Factory can be used as a sibling repo, vendored folder, or mounted sidecar for another Symphony setup.

## Recommended Local Layout

```text
/path/to/work/
  bio-symphony/
  structure-factory/
  orchestrator-workspace/
```

## Install Steps

1. Clone the public repo or your private fork:

```bash
git clone https://github.com/BioSymphony/structure-factory.git
```

2. Validate the sidecar:

```bash
cd structure-factory
make preflight
make registry-check
make module-check
make provider-check
make runpod-check
make runpod-scope-check
make issue-check
make issue-file-check
make input-audit
make contract-self-check
make test
```

For the complete local public gate, use:

```bash
make public-switch-check
```

3. Copy or adapt the workflow template:

```bash
cp references/structure-factory.WORKFLOW.template.md /path/to/orchestrator-workspace/workflows/structure-factory.WORKFLOW.md
```

4. Set the Linear project slug and clone URL in the workflow.

5. Keep all remote compute launch disabled until a human/operator gate issue authorizes it.

RunPod is the default reviewed remote path, and AWS Batch is the reviewed cloud-scale path. GHCR is optional; a sidecar can use public images, runtime bootstrap, a dedicated Structure Factory RunPod Network Volume, AWS Batch images, local high-resource installs, SSH/HPC modules, or neocloud/generic cloud volumes as long as the same manifests, scope checks, input audit, and contract self-check pass. Local, SSH/HPC, generic cloud VM, and neocloud profiles are adapter contracts; they are not execution-ready until provider-specific launch tooling exists and passes the same self-check gates.

## Public API

- `sidecar.yaml`
- `modules/`
- `templates/linear-issue.md`
- `scripts/structure_factory/*_check.py`
- `references/structure-factory.WORKFLOW.template.md`

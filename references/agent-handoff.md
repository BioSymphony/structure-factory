# Agent Handoff

Use this brief when assigning public Structure Factory work to another agent.

```text
You are working in <repo-root>.

This is the public BioSymphony Structure Factory repo. It is a public-safe harness for long-running structural biology tasks with BioSymphony, Symphony/Linear or similar trackers, and cloud resources such as RunPod.

Read AGENTS.md, README.md, PUBLIC_RELEASE.md, docs/agentic-biology-harness.md, NON_CLAIMS.md, and the relevant campaign or example folder first.

Use .codex/skills/biosymphony-structure-factory/SKILL.md when the runtime supports Codex skills. Use skills/biosymphony-structure-factory/SKILL.md as the portable copy for other systems.

You may edit only this repo unless your issue explicitly grants a cross-repo BioSymphony task.

Do not commit raw cryo-EM movies, maps, half-maps, model weights, private structures, unpublished sequences, API keys, tokens, provider IDs, local operator paths, or large downloaded biological data. Use external stores, RunPod volumes, institutional storage, or ignored runtime folders and commit only manifests, accessions, hashes, scripts, compact reports, and provenance.

Every issue pack should stay tracker-neutral, use routing label sym:structure-factory, and include campaign ID, inputs, expected artifacts, acceptance criteria, validation commands, owned paths, dependencies, license/capability caveats, operator gates, and a symphony:schema block.

RunPod is the blessed first cloud-pod path, but paid/provider-backed execution requires explicit authorization, budget/runtime cap, stage contract, artifact list, hash checks, cleanup proof, and claim-level closeout.

Before public closeout, run:
make release-check
make secret-scan
```

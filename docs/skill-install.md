# Install The Structure Factory Skill

Structure Factory ships two copies of the same skill:

- `.codex/skills/biosymphony-structure-factory/SKILL.md` for Codex-style repo-local discovery
- `skills/biosymphony-structure-factory/SKILL.md` for portable installation into another agent environment

The files are kept identical by `bsf harness-check`.

## Repo-Local Use

Open an agent in the repository root and ask it to use the BioSymphony Structure Factory skill. The skill tells the agent to read the public safety, non-claims, harness, compute, licensing, and RunPod guidance before planning work.

Validate the local skill surface:

```bash
make harness-check
```

## Install Into Codex User Skills

For local Codex environments that read `~/.codex/skills`, install a copy:

```bash
scripts/install-codex-skill.sh
```

Use a custom destination when needed:

```bash
scripts/install-codex-skill.sh /path/to/skills
```

The installer copies only the portable skill directory. It does not copy campaign data, run outputs, private state, or credentials.

## Portable Use Outside Codex

For other agent systems, copy `skills/biosymphony-structure-factory/` into that system's skill or instruction directory, then point the agent at this repository as the working tree.

Minimum prompt:

```text
Use the BioSymphony Structure Factory skill. Plan public-safe structural biology work only. Keep remote execution disabled unless explicitly authorized.
```

## Verify After Installation

Ask the agent to run:

```bash
bsf harness-check .
bsf audit .
```

The agent should report that the skill is a planning/control-plane harness, not a license bypass, wet-lab protocol system, or evidence-free claim generator.

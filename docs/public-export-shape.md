# Public Export Shape

Last reviewed: 2026-05-13

This public repository should stay close to the internal Structure Factory operating model in working shape. The useful part is the structure: campaign contracts, validator scripts, provider launch contracts, issue packs, evidence ledgers, and claim-capped demos. The public export removes private history and operator-specific material, not the operating model.

## What Should Match The Operating Model

Keep these areas substantially isomorphic so public users and Symphony workers can understand the real system:

| Area | Public shape | Why it is useful |
| --- | --- | --- |
| `campaigns/` | Public-safe campaign specs, wave plans, and issue drafts | Shows how a structural biology request becomes bounded work. |
| `docs/` | Architecture, safety policy, RunPod/provider posture, tool licensing, and lessons | Lets users judge evidence boundaries and operational maturity. |
| `modules/` | Data, lane, provider, image, artifact, and schema contracts | Gives agents machine-readable workflow structure. |
| `examples/` | Small public or synthetic fixtures that validate locally | Provides a fast path for adoption without private data. |
| `demos/` | Curated public-safe result narratives and browsers | Shows the intended dossier style without publishing raw/heavy outputs. |
| `runpod/` | Public launch templates, manifests, stage contracts, and entrypoints | Documents provider expectations while keeping paid launch gated. |
| `scripts/` | Validators, materializers, dry-run generators, and stage checks | Makes the repo executable, not only descriptive. |
| `templates/` and `packs/` | Tracker-neutral issue templates and issue packs | Supports Symphony/Linear import without leaking private tracker IDs. |
| `tests/` | Public release, validator, and runner tests | Keeps the public export continuously checkable. |

## What Stays Private

The public export should not carry:

- private git history or private branch archaeology
- local `.runtime/` artifacts, provider logs, cost logs, event logs, or generated closeout bundles
- `.codex/`, `.claude/`, personal agent configuration, or local automation state, except the public portable Codex skill at `.codex/skills/biosymphony-structure-factory/SKILL.md`
- `internal/private/` notes, operator handoffs, account-specific runbooks, or private tracker text
- raw cryo-EM data, half-maps, generated structures, model weights, videos, archives, or other heavy artifacts
- API keys, tokens, registry credentials, license files, signed URLs, private installer links, concrete pod IDs, concrete volume IDs, or local workstation paths
- unpublished structures, private sequences, private ligand libraries, patient data, or confidential collaborator material

Public docs may name gated tools and provider patterns, but they must use placeholders and runtime-secret references. A public repo can explain how to prepare a gated lane; it should not publish credentials, proprietary installers, accepted-license state, concrete provider placement, embedded launch payloads, or heavy generated outputs.

## Public Positioning

Structure Factory is a BioSymphony/Symphony sidecar for structural biology work programs. Its value is not that it magically discovers binders. Its value is that it makes structural biology automation disciplined:

- turns vague target requests into target windows, stage contracts, issue packs, and validation commands
- keeps Boltz/Genie/RFdiffusion-style design lanes behind explicit setup, license, runtime, and claim gates
- separates generation, scoring, cross-checking, and reporting so failures and partial success are visible
- produces candidate juries and dossiers that are useful for scientist review while staying below experimental claims
- lets Linear/Symphony workers coordinate long-running GPU work without losing provenance, cost, cleanup, or artifact hashes

The "binder designs in no time" pitch should be framed carefully: Structure Factory can compress the setup, planning, triage, and reporting loop for computational binder-design campaigns. It does not prove binding, affinity, specificity, biological function, developability, safety, or therapeutic value.

## Release Bar

A public export is in good shape when:

1. `make public-switch-check` passes.
2. `make public-audit` reports no findings.
3. A strict local-path/private-token search reports no findings.
4. No heavy generated artifacts are tracked.
5. The first commit is a clean public root commit, not private development history.
6. Public examples validate without network, credentials, GPU, or paid provider access.

# Claim And Evidence Guide

Structure Factory is useful when claims stay smaller than the evidence. Use this guide when writing manifests, issue packs, closeouts, reports, or provider runbooks.

## Public Claim Levels

Use these values in public-facing campaign manifests, issue packs, reports, agent closeouts, and docs:

| Claim Level | Use When | Does Not Mean |
| --- | --- | --- |
| `planning` | The work defines scope, inputs, lanes, checks, or provider prep | A model was generated or evidence was reviewed |
| `public_demo` | The result demonstrates a workflow on public deposited data | New biology was proven |
| `public_synthetic_demo` | The result uses synthetic fixture data or toy outputs | Real screening/design evidence exists |
| `computational_candidate` | A generated, predicted, ranked, or rescored item may be worth review | Binding, function, safety, efficacy, selectivity, or therapeutic value |
| `insufficient_evidence` | The available artifacts do not support the requested claim | The hypothesis is false |
| `blocked` | A lane could not proceed because of missing data, tool, license, provider, cost, or authorization | The scientific question is resolved |

If evidence is partial, missing, mocked, dry-run, or fallback-derived, downgrade the claim instead of calling the run successful.

## Evidence Modes

Evidence mode describes where the artifact came from. Claim level describes what the artifact can support. Keep both visible.

| Evidence Mode | Meaning | Typical Claim Ceiling |
| --- | --- | --- |
| `report_only` | A plan, review, or checklist with no new computation | `planning` |
| `public_data` | Public deposited accession metadata, map/model files, or validation reports | `public_demo` |
| `synthetic_demo` | Small toy or fixture data designed for public examples | `public_synthetic_demo` |
| `generated_candidate` | Generated sequences, structures, poses, or designs | `computational_candidate` |
| `provider_native` | Artifacts emitted by the selected runtime/provider lane | depends on artifact and checks |
| `derived` | Local aggregation, rescore, conversion, or figure derived from earlier artifacts | no higher than source evidence |
| `blocked` | A required stage could not run | `blocked` |
| `insufficient_evidence` | A stage ran or produced something, but it does not support the requested claim | `insufficient_evidence` |

Provider state is not an evidence mode. A pod, job, process exit code, or scheduler state only proves intent until artifacts are fetched, parsed, hashed, and joined to the declared inputs.

## Legacy Schema Values

Some low-level schemas and older stage contracts still contain machine values such as `candidate`, `processed`, `validated`, `publishable`, `fixture_or_demo`, or `calibrated`. Treat those as compatibility values for old artifacts, not as public release language.

| Legacy Or Machine Value | Public-Facing Translation |
| --- | --- |
| `candidate` | `computational_candidate` |
| `processed` | `public_demo` only when the artifact joins to public inputs and validation ledgers |
| `fixture_or_demo` | `public_synthetic_demo` unless it uses real public deposited evidence |
| `validated`, `publishable`, `calibrated` | Avoid in public closeouts unless an explicit external validation/review gate exists; otherwise use `public_demo`, `computational_candidate`, or `insufficient_evidence` |

When in doubt, write the stricter public value and add a note that an older schema field is being preserved for backward compatibility.

## Closeout Rules

Every public closeout should state:

- input posture: public, synthetic, generated, private-held, or blocked
- evidence mode
- claim level
- validation commands run
- artifact packet path or `n/a`
- hash ledger path or `n/a`
- cost report and cleanup proof for paid/provider-backed runs
- downgrade reason when evidence is partial, derived, mocked, or missing

Never close a Structure Factory run as successful from provider launch, provider `RUNNING`, a process exit code, screenshot-only evidence, placeholder outputs, or a report without artifact joins.

## Examples

Binder design planning:

```yaml
evidence_mode: report_only
claim_level: planning
claim_note: Target window and lane contract only; no generated structures or binding evidence.
```

Synthetic screening fixture:

```yaml
evidence_mode: synthetic_demo
claim_level: public_synthetic_demo
claim_note: Fixture demonstrates schema and fanout mechanics only.
```

Generated design jury:

```yaml
evidence_mode: generated_candidate
claim_level: computational_candidate
claim_note: Ranking is computational triage; external validation is required before biological claims.
```

Provider-backed closeout after missing artifacts:

```yaml
evidence_mode: insufficient_evidence
claim_level: insufficient_evidence
claim_note: Provider job started, but required artifacts were not fetched and hash-joined.
```

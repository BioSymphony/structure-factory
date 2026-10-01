# Chai-1

## Purpose

Plan cofold lanes with Chai-1, an open-source biomolecular structure prediction model. Used as an independent vote in multi-validator slates alongside Boltz and AF2-Multimer for binder triage.

## Public-Safe Status

Public scaffold: yes. Runtime use requires current source, dependency, and weight review.

## When To Use

- One member of a multi-validator slate for binder triage.
- Independent prediction under the campaign's calibrated aggregation policy.
- Cofold structures where MSA-driven prediction is preferred over single-sequence inference.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill with the Chai-1 tool card. For target <PDB:ID> and candidate sequence <FASTA>, prepare a Chai-1 cofold lane. Declare supplied-MSA or query-only input and the separate ESM-embedding setting, and define the closeout artifacts (per_chain_pair_iptm, aggregate_score, CIF outputs).
```

## Typical Inputs

- Target sequence and candidate binder sequence (FASTA).
- Optional supplied-MSA directory with sequence-keyed `<hash>.aligned.pqt` files; record the actual per-chain alignment coverage.
- Number of trunk recycles and diffusion timesteps.

## Typical Outputs

- Predicted complex structures (CIF).
- NPZ confidence file with `aggregate_score` and `per_chain_pair_iptm`.

## Repo And References

- Repo: https://github.com/chaidiscovery/chai-lab
- [Reviewed v0.6.1 inference implementation](https://github.com/chaidiscovery/chai-lab/blob/v0.6.1/chai_lab/chai1.py#L304): MSA and ESM settings are independent.
- [Reviewed parquet naming contract](https://github.com/chaidiscovery/chai-lab/blob/v0.6.1/chai_lab/data/parsing/msas/aligned_pqt.py#L53): the filename uses SHA-256 of the uppercase query sequence. Recheck these interfaces when selecting another release.

## Key Knobs

| Knob | Recommendation | Why |
| --- | --- | --- |
| `use_esm_embeddings` | Record explicitly; native default `True` | Controls ESM features independently of MSAs; disabling them is a separate experiment. |
| `msa_directory` | Sequence-keyed parquet directory for a supplied-MSA arm | Use the native filename/schema and verify each chain's consumed alignment. |
| `use_msa_server` | Only for an explicitly declared remote-search arm | Mutually exclusive with `msa_directory`; retain input-disclosure and alignment provenance. |
| `num_trunk_recycles` | 3 | Typical default. |
| `num_diffn_timesteps` | 200 | Typical default. |

## Gotchas

- Supplying an MSA does not require disabling ESM embeddings. Without a supplied alignment or MSA-server request, the native loader uses empty MSA contexts. Check the consumed features rather than inferring MSA use from the ESM flag.
- Validate the selected parquet loader against the pinned pandas version; record any compatibility patch and the parsed alignment output.
- Calibrate confidence against matched controls for each model and input posture; there is no universal score offset between Chai and Boltz.
- Read `per_chain_pair_iptm[binder, target]` for the interface iPTM rather than the global `iptm` field.

## Gates

- Weight download and runtime use require current upstream license terms.
- Public targets only in public examples.
- Multi-validator slate recommended. Do not promote candidates from Chai alone.
- Run a currency check before any paid GPU dispatch: upstream repo HEAD (releases + recent commits), current release notes, and recent preprints (biorxiv / chemrxiv / arxiv) on the relevant lane. Record the version pin and the date of the check in the candidate ranking or validation notes.

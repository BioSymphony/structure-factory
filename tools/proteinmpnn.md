# ProteinMPNN

## Purpose

Plan sequence-design lanes that assign sequences to a generated backbone or scaffolded interface. ProteinMPNN proposes sequences conditioned on an input backbone. Independent refolding evaluates whether a proposed sequence reproduces that backbone.

## Public-Safe Status

Public scaffold: yes. Runtime use requires current source review against upstream terms. Weights are openly released.

## When To Use

- To complete backbone-only outputs from RFdiffusion, Genie3, or another declared generator.
- For optional redesign of an existing sequence/structure pair; preserve the native sequence and identify redesigned children separately.
- After motif-anchored scaffolding to design sequence around a preserved binding motif.
- For comparing wild-type sequence likelihood at design positions.

## Variants

- **Vanilla ProteinMPNN.** Original release. General-purpose backbone-to-sequence design.
- **CA ProteinMPNN.** Select `--ca_only` and its CA checkpoint for C-alpha-only input. At the recorded source pin, CA-only plus `--use_soluble_model` is unsupported.
- **SolubleMPNN.** Activate with `--use_soluble_model`. Favors solubility-correlated residue choices. Public benchmarks have reported higher wet-lab expression rates with SolubleMPNN compared to vanilla for soluble-protein design; check the current benchmark literature for your target class.

## Anthropic Acceleration Route

The [Anthropic kit inventory](anthropic-optimization-kits.md) records `off` and
`exact` for vanilla and soluble ProteinMPNN. The pinned kit
[operation contract](https://github.com/anthropics/uplifting-biomolecular-modeling/blob/f4f62fa6592ae4938d49b1757bea0cfeff9f468e/proteinmpnn/README.md#modes)
limits `exact` to full-backbone sequence design: it excludes CA-only,
score-only, conditional or unconditional probability-only, tied-position, and
positive backbone-noise operations. Use an explicitly selected stock `off`
route for those operations. A Genie3 C-alpha-only handoff needs ProteinMPNN
CA-only support; it cannot use this kit's full-backbone `exact` route.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill with the ProteinMPNN tool card. For backbone <PDB path or RFdiffusion output>, prepare a sequence-design lane. Select CA ProteinMPNN for C-alpha-only input or a declared full-backbone vanilla/soluble arm, map any fixed motif positions, declare children per parent, and define the closeout artifacts (FASTA, score files, per-position log-probabilities).
```

## Typical Inputs

- Backbone PDB via `--pdb_path`, or parsed structure JSONL via `--jsonl_path`. Native stock input is not a direct mmCIF interface; normalize CIF to the supported representation with explicit chain/residue mapping and retain both hashes.
- Optional design mask indicating positions to design.
- Optional fixed residues to preserve a motif or known anchor.
- Number of sequences per backbone.

## Typical Outputs

- Designed sequences in FASTA.
- Per-position log-probabilities.
- Score files for ranking.

## Repo And References

- Repo: https://github.com/dauparas/ProteinMPNN
- ProteinMPNN paper: Dauparas et al., *Science* 2022.
- [Pinned native runner and arguments](https://github.com/dauparas/ProteinMPNN/blob/8907e6671bfbfc92303b5f79c4b5e6ce47cdef57/protein_mpnn_run.py#L402); [CA checkpoint selection and soluble incompatibility](https://github.com/dauparas/ProteinMPNN/blob/8907e6671bfbfc92303b5f79c4b5e6ce47cdef57/protein_mpnn_run.py#L38).

## Key Knobs

| Knob | Recommendation | Why |
| --- | --- | --- |
| `--num_seq_per_target` | 8 to 10 | Standard range across published benchmarks. |
| `--sampling_temp` | 0.1 to 0.3 | Lower for stricter sequences, higher for diversity. |
| `--use_soluble_model` | For a declared full-backbone soluble arm | Unsupported with CA-only at this pin. |
| `--ca_only` | For C-alpha-only input | Uses the separate CA model/checkpoint. |
| `--fixed_positions_jsonl` | Record the mapped fixed positions for motif anchors | Native fixed-residue interface; validate chain and position mapping. |

## Gotchas

- This pinned stock runner has no `--cyclic` flag. A topology-aware sequence-design variant needs its own source and operation contract; keep generator cyclization flags and cyclic-aware refolding separate.
- For interface design, condition on the receptor context (include the target chain) rather than designing the binder in isolation.
- Sequence diversity is sensitive to `sampling_temp`. Sweep it for downstream cofold lanes that benefit from a broader ensemble.

## Gates

- Public targets only in public examples.
- Store sequences for private targets under ignored runtime storage or in a user-selected artifact store.
- Wet-lab confirmation lives downstream of this card.
- Run a currency check before any paid GPU dispatch: upstream repo HEAD (releases + recent commits), current release notes, and recent preprints (biorxiv / chemrxiv / arxiv) on the relevant lane. Record the version pin and the date of the check in the candidate ranking or validation notes.

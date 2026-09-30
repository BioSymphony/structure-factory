# GuideFlip

## Purpose

Plan binder sequence and structure co-design for flexible or intrinsically
disordered targets. GuideFlip uses AlphaFold-guided discrete flow matching:
binder residues are assigned progressively, with the complex re-predicted as
the sequence develops. Its sequence prior comes from ADFlip, an all-atom
inverse-folding model. The [GuideFlip preprint](https://www.biorxiv.org/content/10.64898/2026.09.27.754145v2)
also studies flexibility in scaffolded nanobody design.

## Source And Release

Public source reviewed on 2026-09-30 at commit
[`6fbb2fd48af208e2adc92901c90a97cbcd9cf252`](https://github.com/ykiiiiii/GuideFlip/tree/6fbb2fd48af208e2adc92901c90a97cbcd9cf252).
The repository ships inference code, example settings, and an ADFlip inference
checkpoint. AlphaFold2 parameters are downloaded separately or supplied from an
existing parameter directory. Optional AlphaFold3 runs use a separate
installation and parameter set. This card documents an upstream workflow;
Structure Factory runtime and adapter qualification remain required.

## Run Shape

1. Declare a public or operator-approved target sequence or structure, chain
   mapping, binder-length policy, target-template mask, and trajectory seeds.
2. Validate the settings and model assets in a dedicated runtime. The shipped
   installer targets Linux with an NVIDIA GPU, Python 3.11, PyTorch 2.8.0, and
   JAX 0.6.0.
3. Run a declared generation canary and verify sequence completion and parsed
   structures before scaling.
4. Retain AF2-Multimer, optional AF3, and binder-only AF2 assessment records
   separately, with each backend's configured filters.
5. Carry candidates into the [common scoring stack](cofold-scoring-stack.md)
   with complete model, sequence, score, and pose provenance.

The public examples focus on disordered targets, using either a supplied PDB
with the target template withheld or a sequence-only target whose initial
structure is predicted. Record the exact template mask and executed validation
backends as part of each arm's identity.

## Outputs And Scoring

Upstream separates generation records, backend validation records, and accepted
candidates. It writes structures, sequence FASTA files, per-trajectory JSON,
summary CSV, and run counts. Preserve incomplete and failed trajectories.

The generation pose can differ in residue identity from the final decoded
sequence; the output records both. Use the fixed-sequence validation pose for
sequence-bound scoring. AF2 validation uses the same model family as design;
record that relationship when selecting an independent predictor.

In the pinned results writer, binder pLDDT is recorded on a `0..1` scale and
`ipae_min` in angstroms. Preserve per-model values, aggregation rules, configured
thresholds, and disabled filters. Use the [comparison contract](../docs/binder-comparison-contract.md)
and [scoring invariants](../docs/scoring-invariants.md) for downstream joins.

## License And Model Assets

GuideFlip's root code is MIT-licensed. Its ADFlip subtree carries an MIT-style
license; the bundled checkpoint has no separately identified weight license.
Vendored ColabDesign uses Beer-Ware, and vendored AlphaFold2 code uses
Apache-2.0. AlphaFold2 parameters use CC BY 4.0. AF3 code, parameters, and
outputs have their own noncommercial terms. Review the
selected backend and intended use before installation or redistribution.

Keep checkpoints, generated sequences, structures, and execution records in
runtime storage. Result records remain `computational_candidate`.

## Primary Sources

- [Repository and usage](https://github.com/ykiiiiii/GuideFlip)
- [GuideFlip preprint, v2, 2026-09-30](https://www.biorxiv.org/content/10.64898/2026.09.27.754145v2)
- [ADFlip paper](https://openreview.net/forum?id=8tQdwSCJmA)
- [Pinned installer](https://github.com/ykiiiiii/GuideFlip/blob/6fbb2fd48af208e2adc92901c90a97cbcd9cf252/installation/install.sh)
- [Pinned results writer](https://github.com/ykiiiiii/GuideFlip/blob/6fbb2fd48af208e2adc92901c90a97cbcd9cf252/guideflip/results.py)
- [Code license](https://github.com/ykiiiiii/GuideFlip/blob/6fbb2fd48af208e2adc92901c90a97cbcd9cf252/LICENSE), [ADFlip license](https://github.com/ykiiiiii/GuideFlip/blob/6fbb2fd48af208e2adc92901c90a97cbcd9cf252/adflip/LICENSE), and [vendored notices](https://github.com/ykiiiiii/GuideFlip/blob/6fbb2fd48af208e2adc92901c90a97cbcd9cf252/colabdesign/NOTICE)
- [AlphaFold2 parameter terms](https://github.com/google-deepmind/alphafold#model-parameters-license), [AF3 code license](https://github.com/google-deepmind/alphafold3/blob/608edb684db9f6fd0e677fea01c4cefc60f8a8aa/LICENSE), and [AF3 parameter terms](https://github.com/google-deepmind/alphafold3/blob/608edb684db9f6fd0e677fea01c4cefc60f8a8aa/WEIGHTS_TERMS_OF_USE.md)

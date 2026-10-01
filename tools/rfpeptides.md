# RFpeptides

## Purpose

Plan head-to-tail macrocyclic peptide design using the RFpeptides protocol in
RFdiffusion. Keep backbone generation, sequence design, and cyclic-aware
refolding as distinct stages. Other covalent topologies need their own reviewed
implementation and input contract.

## Public-Safe Status

Public scaffold: yes. The reviewed official RFdiffusion source and README-linked
weights carry a BSD license. Selected dependencies, containers, and downstream
predictors retain their own terms. Runtime execution requires a validated adapter;
store weights and generated peptides outside public git.

## When To Use

- Head-to-tail macrocyclic peptide backbone generation, with or without a target.
- Site-conditioned macrocycle design against a declared target window.
- A comparison arm with explicitly preserved cyclic topology through sequence
  design, refolding, and geometry review.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill with the RFpeptides tool card. For target <PDB:ID> and site <residues>, prepare the official head-to-tail macrocycle route. Declare length, generated cyclic-chain mapping, backbone generation, sequence design, cyclic-aware refolding, and computational geometry/confidence checks.
```

## Typical Inputs

- Target PDB and an explicit native-to-generated chain/residue map.
- Contig specification, declared peptide length, and target hotspots.
- Generator cyclic-chain selection, checkpoint identity, seeds, and sample count.
- Separate sequence-design and refolding configurations preserving the topology.

## Typical Outputs

- Generated backbone PDBs and `.trb` mapping/configuration records.
- Sequence children linked to each backbone parent.
- Cyclic-aware refolding structures, confidence sidecars, and geometry review.

## Repo And References

Reviewed official RFdiffusion source pin:
`86507b6538f51fce57b5a72477165f03999ed7ae`.

- [Macrocycle documentation](https://github.com/RosettaCommons/RFdiffusion/blob/86507b6538f51fce57b5a72477165f03999ed7ae/README.md#macrocyclic-peptide-design-with-rfpeptides).
- [Official binder example](https://github.com/RosettaCommons/RFdiffusion/blob/86507b6538f51fce57b5a72477165f03999ed7ae/examples/design_macrocyclic_binder.sh).
- Rettie, Juergens, Adebomi et al., [RFpeptides paper](https://doi.org/10.1038/s41589-025-01929-w), Nature Chemical Biology (2025): backbone generation with cyclic offsets, ProteinMPNN sequence design, then AfCycDesign and/or cyclic-offset RoseTTAFold prediction.
- [License covering source and README-linked weights](https://github.com/RosettaCommons/RFdiffusion/blob/86507b6538f51fce57b5a72477165f03999ed7ae/LICENSE).

## Key Knobs

| Setting | Contract |
| --- | --- |
| `contigmap.contigs` | Declare length and target mapping; the official binder example samples 12–18 residues, which is an example rather than a universal range. |
| `inference.cyclic=True` | Enables macrocycle generation in RFdiffusion. |
| `inference.cyc_chains` | Names the generated chains to cyclize; the example uses `'a'`. Verify the output chain map. |
| `ppi.hotspot_res` | References residues in the input target PDB. |
| `inference.num_designs` | Set within the declared campaign quota and authorization. |

## Gotchas

- These cyclization settings belong to RFdiffusion, not stock ProteinMPNN.
  The [ProteinMPNN card](proteinmpnn.md) records its actual supported operations.
- Preserve head-to-tail connectivity across structure conversion and refolding;
  a plain linear FASTA does not communicate that topology to every predictor.
- Check bond geometry, clashes, and exact-site contacts under a declared policy.
  This card supplies no universal closure RMSD or confidence cutoff.
- Disulfides and other backbone links are separate topology arms; the official
  head-to-tail example does not establish support for every constrained peptide.

## Gates

- Validate generated-chain selection and target mapping before scaling.
- Require sequence and topology-preserving refold artifacts with hashes/counts.
- Calibrate confidence and geometry checks using matched controls.
- Keep generated artifacts outside public git and claims at
  `computational_candidate` or lower until independent validation exists.

# MoMPNN

MoMPNN supplies property-aligned checkpoints for fixed-backbone protein
sequence design. The authors document compatibility with ProteinMPNN checkpoint
format and recommend LigandMPNN's ProteinMPNN inference operation.
[Pinned source](https://github.com/Qivon7/MoMPNN/blob/10d7d6c62189ade4686d8d0cb7fc7408c61510e9/README.md).

## Select The Checkpoint And Operation

Record the checkpoint filename and hash, property objective, inference source
revision, input backbone, design chains, fixed residues, temperature, and seed.
Load the chosen checkpoint through `--model_type protein_mpnn` with
`--checkpoint_protein_mpnn`.
[Native runner](https://github.com/dauparas/LigandMPNN/blob/26ec57ac976ade5379920dbd43c7f97a91cf82de/run.py).

Using LigandMPNN as the inference host does not establish ligand-conditioned
features in this ProteinMPNN operation. Qualify atom-context delivery separately
when selecting a ligand-aware model.

## Check Sequence Outputs

Parse every requested sequence and verify its chain mapping, length, allowed
alphabet, and fixed residue identities. Retain repeated sequences and failed
inputs in the output count. Check repeat behavior with a recorded nonzero seed.

Compare MoMPNN and conventional ProteinMPNN on the same backbones and masks.
Independently refold the resulting sequences and assess the selected property
with suitable controls. A property-aligned checkpoint alone establishes no
improvement in affinity, expression, or solubility for a new target.

## Runtime And Terms

Structure Factory records the checkpoint-loading route; execution requires a
configured adapter. Review the exact checkpoint and intended use before setup.

The pinned MoMPNN root has no project license file. Its README documents
checkpoint inference. The inference host retains its
[MIT license](https://github.com/dauparas/LigandMPNN/blob/26ec57ac976ade5379920dbd43c7f97a91cf82de/LICENSE);
that license does not establish separate MoMPNN checkpoint redistribution terms.

For protonation-conditioned sequence proposals, use the
[ProtonPottsMPNN card](protonpottsmpnn.md). For matched downstream assessment,
use the [binder filtering card](binder-filtering.md).

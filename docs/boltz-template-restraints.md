# Boltz Template Restraints

The hosted Boltz structure-and-binding API accepts
`force_threshold_angstroms` on each template. The field is a nonnegative
distance tolerance for template guidance. It is not an exact coordinate lock,
a force weight, a whole-structure RMSD target, or a guaranteed maximum output
deviation.

## Request Shape

```json
{
  "model": "boltz-2.1",
  "input": {
    "entities": [
      {
        "type": "protein",
        "chain_ids": ["A"],
        "value": "PUBLIC_OR_APPROVED_SEQUENCE",
        "msa": {"type": "empty"}
      }
    ],
    "templates": [
      {
        "template_structure": {
          "type": "url",
          "url": "https://example.org/validated-template.cif"
        },
        "template_chains": [
          {"input_chain_id": "A", "template_chain_id": "A"}
        ],
        "force_threshold_angstroms": 1.0
      }
    ],
    "model_options": {"seed": 42},
    "num_samples": 1
  }
}
```

This example documents placement only. The field belongs to a template.
Omitting it uses the template without this force option. Verify the current
request schema before execution.

## Preflight Counts

Before submitting a request, record for every query/template chain pair:

- declared aligned residues;
- residues that map onto the query;
- mapped residues with representative atoms;
- mapped residues with resolved backbone frames;
- unresolved and out-of-range residues.

An accepted request or echoed threshold does not prove that usable template
coordinates reached the model. A declared template whose mapped
coordinate-bearing count is zero cannot support a geometry-guidance claim.

## Comparison Design

Compare force enabled and omitted with the same sequence, template, seed,
sampling settings, and sample count. Repeat across seeds before estimating an
effect. Measure:

- representative-atom and backbone displacement after a named alignment;
- maximum and distribution of per-residue displacement;
- motif heavy-atom geometry when motif retention matters;
- chain mapping, peptide geometry, clashes, confidence, and output hashes.

Template metadata can describe residues that have no coordinates. Sparse
templates therefore require both sequence-level mapping and coordinate-bearing
counts. Record the provider-returned model and version separately from the
public implementation used to interpret behavior.

## Primary Sources

- API method:
  https://api.boltz.bio/docs/api/api/resources/predictions/subresources/structure_and_binding/methods/start/
- Prediction guide: https://api.boltz.bio/docs/api/guides/predictions/
- Open Boltz implementation: https://github.com/jwohlwend/boltz

## Result Boundary

Template guidance can support a measured bias toward a reference conformation.
It does not prove exact motif preservation, chemical maturation, experimental
accuracy, binding, or function.

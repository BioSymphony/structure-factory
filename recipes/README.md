# Recipes

Recipes are short public workflows for agents and humans. They link the skill, CLI, examples, task packs, and validation gates without requiring private infrastructure.

| Recipe | Use Case | Starts With | Result Boundary |
| --- | --- | --- | --- |
| [PD-L1 binder-design fast path](pd-l1-binder-design-fast-path.md) | Scaffold and review a public protein-interface binder-design campaign | `examples/pd-l1-binder-design-public` | `computational_candidate` |
| [Screening superpowers local fixture](screening-superpowers-local-fixture.md) | Run local screening fixture and active-learning checks | `examples/screening-superpowers` | `public_synthetic_demo` |
| [PDB/EMDB structure mapping public data](structure-mapping-public-data.md) | Build a public-accession structure-mapping plan | public PDB/EMDB accession | `public_demo` |
| [RunPod no-download smoke](runpod-no-download-smoke.md) | Prepare and validate a non-launchable cloud template | `runpod/launch-manifests/no-download-smoke.json` | `planning` |

All recipes require public or synthetic inputs, explicit run boundaries, and an operator gate before any paid provider or license-gated execution.

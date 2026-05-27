# Tool Cards

These cards describe the Structure Factory tool lanes your agent can compose into a campaign. Each card lists the lane, the runtime gate, the typical inputs and outputs, and the license posture so an agent or operator can decide what to include and what to defer.

Each card follows the same shape:

- Public docs describe the lane and the expected evidence it produces.
- Runtime use needs current primary-source review and the user's intended use context.
- Public images include tools whose redistribution posture has been reviewed.
- License-gated tools install at runtime under operator approval. Private install paths, provider records, license acceptances, credentials, weights, and generated biological artifacts live in operator-controlled infrastructure outside the repo.

## Cards

### Backbone And Peptide Design

- [RFdiffusion3](rfdiffusion3.md). Atom-level diffusion for binder backbones, miniproteins, and biomolecular interfaces.
- [RFpeptides](rfpeptides.md). Cyclic and constrained peptide design in the RFdiffusion family.
- [HelixDiff](helixdiff.md). Short helical peptide design conditioned on target hotspots.
- [PepGLAD](pepglad.md). Full-atom peptide sequence-structure co-design.
- [EvoBind](evobind.md). Sequence-centered peptide optimization for ranked candidate sets.
- [Genie3 peptides and miniproteins](genie3-peptides.md). Length-aware peptide and miniprotein generation.

### Sequence Design

- [ProteinMPNN](proteinmpnn.md). Backbone-to-sequence design. Includes SolubleMPNN for soluble targets.

### Cofold And Scoring

- [Cofold scoring stack](cofold-scoring-stack.md). Multi-validator slate plus ipSAE rescore. Reads from the individual cards below.
- [Boltz](boltz.md). Open biomolecular cofold with confidence and full PAE outputs.
- [Chai-1](chai.md). Open biomolecular cofold with MSA-driven prediction.

### Refinement And Visualization

- [Refinement stack](refinement-stack.md). Energy minimization, interface analysis, and quality filters.
- [ChimeraX peptide visualization](chimerax-peptide-viz.md). Publication-style render lanes for figures.
- [ChimeraX onboarding](chimerax-onboarding.md). Single-file teammate-handoff brief for first render in ~30 minutes.

### Target Prep

- [GCGR target prep](gcgr-target-prep.md). Worked example of public-deposited target preparation.

## When To Use What

A short routing guide. Pick the designer arm by target and binder length, then add the rest of the stack.

| If you want | Start with | Add downstream |
| --- | --- | --- |
| Short cyclic peptides (6 to 15 aa) | [RFpeptides](rfpeptides.md) | [ProteinMPNN](proteinmpnn.md) cyclic mode, [Cofold scoring stack](cofold-scoring-stack.md) |
| Linear helical peptides (15 to 40 aa) | [HelixDiff](helixdiff.md) or [PepGLAD](pepglad.md) | [ProteinMPNN](proteinmpnn.md) on the receptor context, [Cofold scoring stack](cofold-scoring-stack.md) |
| Sequence-centered peptide optimization | [EvoBind](evobind.md) | Optional [ProteinMPNN](proteinmpnn.md) consistency check, [Cofold scoring stack](cofold-scoring-stack.md) |
| Miniprotein binders (50 aa and up) | [RFdiffusion3](rfdiffusion3.md) or [Genie3](genie3-peptides.md) | [ProteinMPNN](proteinmpnn.md) (SolubleMPNN for soluble targets), [Cofold scoring stack](cofold-scoring-stack.md) |
| Cofold one designed candidate against a target | [Boltz](boltz.md) or [Chai-1](chai.md) alone | [Cofold scoring stack](cofold-scoring-stack.md) for multi-validator gating |
| Promote a candidate from a design batch | [Cofold scoring stack](cofold-scoring-stack.md) | [Refinement stack](refinement-stack.md), [ChimeraX](chimerax-peptide-viz.md) |
| Prepare a target from public deposited evidence | [GCGR target prep](gcgr-target-prep.md) as a pattern | Plug the output target-window file into any designer arm |

## Stack Pattern

A common end-to-end binder campaign:

```text
target prep
  -> designer (RFdiffusion3 | RFpeptides | HelixDiff | PepGLAD | EvoBind | Genie3)
  -> sequence design (ProteinMPNN or SolubleMPNN)
  -> cofold slate (Boltz + Chai-1 + AF2-Multimer)
  -> ipSAE rescore on PAE matrices
  -> consensus gate
  -> refinement
  -> rendered report
```

The cofold scoring stack card explains how to compose Boltz, Chai-1, and AF2-Multimer into the validator slate.

## Important Context

- iPTM alone is increasingly deprecated for binder ranking. Recent benchmarks prefer ipSAE and multi-validator consensus over single-cofolder iPTM.
- Wet-lab confirmation lives downstream of every card here. The cards describe in silico triage and provenance, not binding proof.
- For each new target, start with a target-prep step that pins accession, chain, hotspots, and uncertainty. The designer arms expect this target-window file as input.

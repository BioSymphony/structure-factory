# CoSiNE — antibody affinity maturation as a neural CTMC (sequence-only evolution + zero-shot VEP + oracle-guided maturation)

> **Status: reviewed from source and validated end-to-end on a Lambda Cloud A10 GPU (2026-06-08).**
> Install + inference proven: load → valid CTMC `Q` (rows ≈ 0, off-diagonal ≥ 0) → row-stochastic
> `P = exp(Qt)` → Gillespie `generate` (37 mutations / 120 aa), ~11 s on an A10. Validated recipe and
> gotchas are in the Install section below.
> First **antibody-native** lane in this kit and the first **structure-free, sequence-only
> evolutionary scorer.** It is *not* a binder/backbone designer and not a competitor to
> BindCraft/RFd3/EvoBind — it sits in a new category: **antibody sequence evolution / variant-effect
> prediction (VEP) / sequence-likelihood scoring.** Its plug-in oracle interface is the marquee
> integration point: a cofold/ipSAE fitness can become the steering signal.
> Reviewed from a shallow source clone (code only, no weights). **Paper not read** (only the README
> bibtex + arXiv link) → no benchmark numbers verified below. The **`evo` submodule** (oracles,
> `ComplexCherriesDataset`, branch-length estimation, Thrifty wrapper) was **not audited** — it is a
> separate repo.

## What it is

**CoSiNE** (Conditionally Site-Independent Neural Evolution of antibody sequences — Lu, Vermani,
Sanno, Lu, Matsen IV, Jagota, Song; UC Berkeley / Song lab, ICML 2026,
[arXiv 2602.18982](https://arxiv.org/abs/2602.18982), MIT license) models antibody **affinity
maturation as a neural continuous-time Markov chain (CTMC)** over aligned antibody sequences. An
**ESM backbone emits a per-site rate matrix `Q`** conditioned on full-sequence context; transition
probabilities over a phylogenetic branch length `t` are `P = exp(Q·t)`. Trained on **CherryML
"cherry" pairs** (sibling leaves of a lineage tree) from the **DASM** antibody dataset,
**AHO-aligned, substitution-only.**

Three capabilities (all on the released `cosine_dasm.ckpt`):

1. **Unconditional affinity maturation** — simulate germline→mature trajectories via Gillespie
   sampling over a branch length.
2. **Guided Gillespie sampling** — steer evolved sequences toward better properties using **any
   plug-in oracle** (`evo/oracles/base.py:GaussianOracle`). Ships with SARS-CoV-1/2 RBD binding
   oracles from RefineGNN. Supports **CDR/FR-only optimization** (`--mask-region`) and a mutation
   ceiling.
3. **Zero-shot VEP** — score DMS variants by a **selection score = CoSiNE_ll − Thrifty_SHM_ll** that
   subtracts the neutral somatic-hypermutation propensity from the full evolutionary likelihood,
   isolating *selection*. Strong correlation with binding/expression assays is the headline claim
   (unverified here — paper not read).

## How it actually works (the non-obvious mechanics, verified in code)

- **Per-site rate matrix from context, two heads** (`cosine/models/nets/ctmc.py`). The
  **reversible** head (`RateMatrixOutputHead`) uses the **Pande similarity transform**
  `Q = diag(1/√π)·S·diag(√π)` with symmetric exchangeabilities `S` and learned stationary `π` —
  detailed balance (`π_i Q_ij = π_j Q_ji`) and a valid generator hold after the diagonal fix-up
  (`:73-74`). **But the released/trained config uses the *non-reversible* free head**
  (`reversible: false` in `configs/net/ctmc.yaml` + the experiment) where **π is a uniform
  placeholder and never enters the loss** — the GTR/π story is effectively dead code for the shipped
  model.
- **Likelihood = `P = matrix_exp(Q·t)`, then index the row of the parent state** and take the
  child's column (`cosine/models/modules/ctmc_module.py:50-61`). Special/invalid tokens are masked
  out of `Q` everywhere.
- **Gillespie sampler is a correct Doob/Gillespie** (`ctmc.py:391-528`): exponential holding time at
  the total exit rate, event ∝ rate, `active &= (elapsed+τ) ≤ target_t` freezes a sequence once its
  next event would overshoot the branch. **Re-evaluates `Q(y)` from the current full sequence after
  *every single mutation*** (`ctmc.py:405`) → state-dependent rates.
- **Oracle guidance multiplies the relevant off-diagonal rate by `(2·Φ(Δμ/σ))^γ`**
  (`ctmc.py:530-796`): neutral mutations ×1, beneficial amplified, deleterious suppressed. **Taylor
  path is the default** (`use_taylor_approx=True`, O(B) backward passes, gradient of a differentiable
  oracle); the **exact path enumerates all single mutants in pure Python (O(B·L·V))** → intractable
  at documented batch sizes. The stale diagonal after scaling is a non-issue (the sampler re-zeros it
  before use).
- **VEP selection score** (`scripts/vep/cosine.py:272-392`): `selection = CoSiNE_ll − Thrifty_ll`,
  swept over `(CoSiNE_t × Thrifty_bl)` and correlated (Spearman) with assay fitness. Because the
  **WT context is shared across all single mutants**, each mutant's LL reduces to its single mutated
  site's transition probability + a constant — so the difference is a clean per-site selection signal
  and the constants cancel under Spearman. (Internally consistent and the nicest idea in the repo.)
- **Data = CherryML cherries, substitution-only** (`cosine/data/datasets/ctmc.py`): asserts
  `len(x)==len(y)` (aligned, no indels). The `get_mutations` indel machinery in `frameworks/ctmc.py`
  is vendored but **unused** by the released model.

## The one design assumption to scrutinize before adopting

**Training likelihood and the sampler are not the same stochastic process.** Training holds `Q`
fixed at the *parent* context over the whole branch (`P = exp(Q(x_parent)·t)`, sites independent —
the paper's "conditionally site-independent" namesake). The Gillespie sampler re-evaluates `Q(y)`
after every mutation (path-dependent). So **sampled trajectories are not draws from the process whose
likelihood is optimized/scored.** Presumably deliberate, but it is the single thing to pressure-test
for any guided-maturation quality claim — a classic train/inference-process gap.

## Critical caveats (what to design or work around)

1. **CLI loads an oracle even for *unconditional* sampling** (`scripts/guidance/cosine.py:632`,
   ungated; `--oracle` defaults to `None`). The README's first "Unconditional Sampling" example omits
   `--oracle`, so as written it either errors or needlessly loads a heavy RefineGNN predictor. **Gate
   oracle construction behind `if args.use_guided` before running unconditional.**
2. **`with torch.no_grad() and torch.autocast(...)`** (`cosine/models/frameworks/ctmc.py:560`) —
   Python keeps only the second context manager; **`no_grad` is silently dropped**, so
   `infer_log_likelihoods` builds the autograd graph during inference (extra memory/time; results
   still correct, everything is `.detach()`'d). The VEP path does it right (`vep/cosine.py:246`).
3. **README checkpoint filename mismatch**: download is `cosine_dasm.ckpt` (`README.md:58`), every
   command references `checkpoints/cosine_model.ckpt`. Copy-paste fails on first run.
4. **CLI default `--model-path` is a dead author scratch path** (`scripts/guidance/cosine.py:80`) —
   always pass `--model-path` explicitly.
5. **No tests** (despite `pytest` dev-dep + pre-commit), and **`F.cross_entropy` is fed log-probs not
   logits** (`ctmc_module.py:70`). It is *accidentally correct* (P is row-stochastic so CE's internal
   `log_softmax` re-normalizes) — but a malformed `Q` would be silently masked rather than surfaced.
   Nothing guards generator validity.
6. **Single-oracle / single-likelihood circularity.** Both guidance and VEP lean on one signal. The
   same single-signal failure mode shows up across the field: iPSAE beating ipTM on binder ranking,
   GPCR design benchmarks, and [SwitchCraft](switchcraft.md)'s single-cofolder loop. **→ Validate any
   steered sequence with an orthogonal judge, not the oracle that steered it.**
7. **Install bar is high / not CPU-installable.** Hard deps on `flash-attn` (CUDA-only,
   no-build-isolation), `jax`, and `ete3` is used but **undeclared** (only transitive via `cherryml`
   in `uv.lock`). Effectively un-`uv sync`-able on CPU/mac → a **GPU cloud backend** (validated on a
   Lambda Cloud A10), like [SwitchCraft](switchcraft.md).
8. **Substitution-only, AHO-aligned input.** No indel modeling in the released model. Adopting it for
   binders means an antibody-target-prep step (AHO numbering via `abnumber`, already in deps) — the
   analog of [GCGR target prep](gcgr-target-prep.md).
9. **Per-trajectory Python loop in the CLI** (`cosine.py:718`) under-uses the batched Gillespie
   (`B>1` supported) → `--batch-size N` runs ~N× the forward passes it needs.

## Why it's worth a lane

- **An orthogonal, structure-free validator/prefilter for antibody work.** Everything else in this
  kit judges *structure* (ipSAE on cofolded complexes). CoSiNE judges *evolutionary plausibility +
  selection* from sequence alone — a genuinely different failure mode. Cheap to run as a pre-cofold
  triage on antibody variant libraries.
- **The plug-in oracle = the cofold stack becomes the steering signal.** Implement `GaussianOracle`
  over an ipSAE/cofold-derived fitness and CoSiNE will do **structure-guided CDR/FR maturation** with
  a mutation budget. That is the highest-value integration and it plays to this kit's strengths
  ([cofold scoring stack](cofold-scoring-stack.md)).
- **Antibody is a whole target class this kit does not yet cover** (it is GPCR/peptide/binder-centric).

## Install + run — validated on Lambda Cloud A10 (2026-06-08)

The README's plain `uv sync` does **not** work on a fresh uv venv. Four gotchas, all fixed below
(found via cheap pre-GPU smoke runs):

1. **uv venvs ship no `setuptools`** → `wandb`/`transformers` `import pkg_resources` fails AND
   flash-attn's sdist build (no-build-isolation) fails. **Pre-seed `setuptools wheel pip` before sync.**
2. **flash-attn 2.8.3 has no PyPI wheel** for torch2.8/cu128/py3.10 → `uv sync` builds from sdist and
   returns rc=1. **Skip it in sync** (`--no-install-package flash-attn`), install separately.
3. **flash-attn is REQUIRED at *checkpoint load*** (not for import) — `cosine_dasm.ckpt` pickles a
   `flash_attn` class. Install the **prebuilt wheel** (ABI-detected) from Dao-AILab releases.
4. **The checkpoint was trained under the project's OLD package name `peint`** → `torch.load` raises
   `No module named 'peint'`. **`sys.modules["peint"]=cosine` before `load_from_checkpoint`.**

```bash
git clone --depth 1 https://github.com/thematrixmaster/cosine.git && cd cosine
git submodule update --init --depth 1                              # evo submodule (oracles, datasets)
uv venv --python 3.10
uv pip install --python .venv/bin/python setuptools wheel pip ninja  # gotcha #1
uv sync --inexact --no-install-package flash-attn                    # gotcha #2 (all else, fast)
# gotcha #3 — flash-attn wheel (needed to UNPICKLE the ckpt):
ABI=$(.venv/bin/python -c "import torch;print('TRUE' if torch._C._GLIBCXX_USE_CXX11_ABI else 'FALSE')")
uv pip install --python .venv/bin/python \
  https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abi${ABI}-cp310-cp310-linux_x86_64.whl
.venv/bin/python -c "from huggingface_hub import hf_hub_download as d; d('thematrixmaster/cosine','cosine_dasm.ckpt',local_dir='checkpoints')"
```

```python
# loading the checkpoint (gotcha #4) — works in <11 s on an A10:
import sys, cosine; sys.modules.setdefault("peint", cosine)
from cosine.models.modules.ctmc_module import CTMCModule
module = CTMCModule.load_from_checkpoint("checkpoints/cosine_dasm.ckpt", map_location="cuda", strict=False)
net = module.net.eval().cuda()                       # reversible=False (free head); vocab size 33
# then: NeuralCTMCGenerator(net).generate_with_gillespie(x, t, x_sizes, ...)  -- call the LIBRARY, not the CLI
```

- **flash-attn needs Ampere+** (A10 = sm_86, fine). Wrap the run in a small launcher that parses one
  trajectory / one VEP row before any batch sweep. **Cleanup gotcha:** a transient `GET /instances`
  curl timeout can leave a stale `cleanup_verified:false` even though terminate fired — always
  re-poll active instances and terminate by id.
- For VEP/guided runs use the README CLI flags (`--mask-region CDR3`, `--oracle`,
  `--guidance-strength`); remember the CLI loads an oracle even unguided (caveat #1) and the ckpt is
  `cosine_dasm.ckpt`, not `cosine_model.ckpt`.
- **Smoke-first:** N=1 first — parse one generated trajectory / one VEP transition row and confirm the
  output schema before any batch sweep.
- **Result boundary:** the deliverable is the **ranked compute output** — VEP Spearman correlations
  and ranked sequences — not "antibody candidates worth synthesizing." Wet-lab confirmation lives
  downstream of this card.

## Extensibility (the integration to build)

- **New oracle:** subclass `evo/oracles/base.py:GaussianOracle` (return per-sequence mean + variance;
  for the fast Taylor path also implement `compute_fitness_gradient`) and register in
  `evo/oracles/__init__.py:get_oracle`. **This is where an ipSAE/cofold fitness plugs in.**
- **Synthetic-codon experiments** live in a sibling repo `thematrixmaster/ctmc-experiments`.

## Integration with the pipeline

- **Upstream prefilter / orthogonal validator** for antibody campaigns → feed survivors to the
  [cofold scoring stack](cofold-scoring-stack.md) (structural ipSAE gate) for the orthogonal check
  CoSiNE cannot give.
- **Steering loop:** cofold/ipSAE fitness → `GaussianOracle` → CoSiNE guided maturation → re-cofold
  the steered sequences with a *different* judge (do not trust the steering oracle).
- Adopting it for binders means an antibody-target-prep step (AHO numbering via `abnumber`, already in
  deps) — the analog of [GCGR target prep](gcgr-target-prep.md).
- **Refinement + viz** ([refinement stack](refinement-stack.md), ChimeraX) only after a structural
  model exists — CoSiNE produces sequences, not structures.

## Review log / provenance

- **2026-06-08** — Reviewed from source by direct read of the CTMC network, module, and framework
  code, the VEP and guidance CLIs, the model configs, and the dataset loader (shallow clone, code
  only, no weights). Install + inference validated end-to-end on a Lambda Cloud A10.
- **Verified:** Pande/GTR reversible head satisfies detailed balance; free non-reversible head is the
  trained model (π unused); `P=exp(Qt)` likelihood; correct Gillespie; guidance weight `(2Φ(Δμ/σ))^γ`
  with Taylor default; VEP `CoSiNE_ll − Thrifty_ll` reduces to a per-site signal; CherryML/AHO
  substitution-only data.
- **Found (bugs/caveats):** train/sample process mismatch; `no_grad` dropped (`frameworks/ctmc.py`);
  oracle always loaded for unconditional runs (`guidance/cosine.py`); README ckpt filename mismatch;
  dead author default `--model-path`; no tests; CE-on-logprobs masks bad generators; `ete3`
  undeclared; flash-attn/jax install bar; exact guidance intractable.
- **Not done:** paper not read (no benchmark numbers verified); `evo` submodule not audited.

## Links

- Repo: <https://github.com/thematrixmaster/cosine> (`main`, MIT, ICML 2026 title)
- Paper: *Conditionally Site-Independent Neural Evolution of Antibody Sequences* (Lu et al. 2026) — <https://arxiv.org/abs/2602.18982>
- HF weights + dataset: `thematrixmaster/cosine` (ckpt `cosine_dasm.ckpt`; dataset via `--repo-type dataset`)
- Builds on: ESM <https://github.com/facebookresearch/esm> · CherryML <https://github.com/songlab-cal/CherryML> · DASM (eLife reviewed preprint 109644) · Thrifty SHM model (eLife reviewed preprint 105471) · RefineGNN (oracles) <https://github.com/wengong-jin/RefineGNN>
- Sibling: `thematrixmaster/ctmc-experiments` (synthetic codon experiments)

# Convex Distance Operator Transport — claim-by-claim reproduction

This experiment line reproduces all six judged claims in
[arXiv 2606.02047](https://arxiv.org/abs/2606.02047). It combines
proof-obligation certificates for the three universal theorems with
paper-scale empirical checks.

Claims 1, 2, and 6 are `VERIFIED` candidates. Claim 4 is a `FALSIFIED`
candidate after exhaustive primary-archive and independent counterexample
checks. Claim 5 is a `FALSIFIED` candidate: the full run found the paper's
MUTAG direction but a stable ENZYMES reversal (CDOT `0.39222`, FGW `0.44778`)
under all three outer seeds. Claim 3 is `VERIFIED` at the exact paper scale:
CDOT `0.001694`, FGW `0.003514`, and IsoRank `0.003378` over 100 paired
trials. All formal compute uses Hugging Face `cpu-upgrade`; no GPU is used.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Detailed evidence: [Claim 1](candidate/pages/claim-1-convex-qp/page.md),
[Claim 2](candidate/pages/claim-2-pseudometric-dispersion/page.md),
[Claim 3](candidate/pages/claim-3-synthetic-table2/page.md),
[Claim 4](candidate/pages/claim-4-oasis-cohort/page.md),
[Claim 5](candidate/pages/claim-5-tudataset/page.md), and
[Claim 6](candidate/pages/claim-6-risk-bound-consistency/page.md).

Read the [illustrated technical report](reports/cdot-reproduction/report.md)
or the [self-contained marimo tutorial](notebooks/cdot_reproduction.py).
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-nPC7M7XLEv-convex-distance-operator-transport-a-convex-and-geometry-preserving-formulat/blob/main/notebooks/cdot_reproduction.py)

## Experiment log

| Branch / experiment | Purpose | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `orx/baseline-source-pin-and-claim-1-certificate` | Source pin, Theorem 3.4 certificate, verifier, checker, control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claim 1 `VERIFIED` candidate; all gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one thread enforced; 32 s job |
| `orx/claim-2-pseudometric-and-dispersion-certificate` | Add Theorems 3.5/3.7 certificate, exhaustive finite domain, raw-witness checker, control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claims 1–2 `VERIFIED` candidates; all gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one thread enforced; 26 s job |
| `orx/claim-6-risk-bound-and-consistency-certificate` | Add Theorem 5.6 / Corollary 5.7 proof obligations, exact FW schedule, independent checker, invalid-schedule control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claims 1, 2, and 6 `VERIFIED` candidates; all gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one thread enforced; 27 s job |
| `orx/claim-4-exhaustive-oasis-3-cohort-falsification` | Exhaustively hash and parse the primary OASIS-3 archive; independently check any 170-node counterexample and reject padding | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claim 4 `FALSIFIED` candidate; cumulative claims pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, four extraction cores estimated; 3m42s job |
| `orx/claim-5-full-tudataset-nested-cv-reproduction` | Full MUTAG/ENZYMES all-pairs distances, nested 10×5-fold RBF-SVM, checker, and permuted-label controls | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claim 5 `FALSIFIED` candidate: MUTAG +0.00731, ENZYMES −0.05556; all cumulative gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, eight one-thread workers; 1h41m job |
| `orx/claim-3-full-scale-synthetic-table-2-cpu-reprodu` | Exact-scale synthetic reconstruction: 2,000 points, 100 trials, CDOT/FGW/IsoRank, paired checker and destructive controls | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claim 3 `VERIFIED` candidate; CDOT lower than both baselines with paired 95% intervals below zero; all cumulative gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, four workers × 16 numerical threads; 5h31m job |
| `main` | Public README, report, figures, and notebook | Not run as an experiment (publication surface) | Presentation-only mirror after release gates | No experiment compute |

---

Original workspace identifier:
`icml26-repro-nPC7M7XLEv-convex-distance-operator-transport-a-convex-and-geometry-preserving-formulat`.

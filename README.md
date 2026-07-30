# Convex Distance Operator Transport — claim-by-claim reproduction

This experiment line reproduces all six judged claims in
[arXiv 2606.02047](https://arxiv.org/abs/2606.02047). It combines
proof-obligation certificates for the three universal theorems with
paper-scale empirical checks.

The previous live judge awarded **9/12** at Hugging Face revision
`e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032`: Claims 3–5 received full
credit, while Claims 1, 2, and 6 remained toy-level because the certificates
were human-written. Published revision
`819b602292066602b465aa8ac59babce4f673b95` addresses exactly that
criticism with Lean 4.19.0/mathlib kernel checks, an independent importing
replay, pinned source/toolchain hashes, and a false-theorem control rejected
by the kernel. The live judge evaluated that exact revision on
2026-07-30 and awarded **12/12**: Claims 1, 2, 3, and 6 were `VERIFIED`;
Claims 4 and 5 were `FALSIFIED`, which also receives full credit.

Claims 1, 2, and 6 are judged `VERIFIED`. Claim 4 is judged `FALSIFIED`
for the literal 696-by-170 cohort invariant, while its faithful
all-4,950-pair rerun reproduces both Table 3 method directions: diffusion
CDOT `0.718623` versus FGW `0.154048`, and geodesic CDOT `0.465153` versus
FGW `0.534139`. Claim 5 is judged `FALSIFIED`: the full run found the paper's
MUTAG direction but a stable ENZYMES reversal (CDOT `0.39222`, FGW `0.44778`)
under all three outer seeds. Claim 3 is judged `VERIFIED` at the exact paper scale:
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
The superseding theoretical verifier is documented in the
[Lean theorem report](reports/cdot-reproduction/lean-verification.md), with
executable source in [formal/CDOTProofs.lean](formal/CDOTProofs.lean).

Read the [illustrated technical report](reports/cdot-reproduction/report.md),
the [live 12/12 judge result](reports/cdot-reproduction/judge_result_12_of_12.md),
the [Lean release report](reports/cdot-reproduction/lean_release_report.md),
the [historical 4/12 release report](reports/cdot-reproduction/release_report.md),
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
| `orx/judge-repair-canonical-trackio-pages-plus-oasis` | Add canonical Trackio claim pages and faithful OASIS-3 Table 3 first-100/all-4,950-pair rerun | `uv run --frozen --python 3.12 python -m cdot_repro.run` | All six primary and independent gates pass; both Table 3 directions reproduce and the cohort counterexample remains exact | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, eight one-thread OASIS workers; 6h27m cumulative job |
| `orx/lean-kernel-certificates-for-claims-1-2-and-6` | Replace the human-only theoretical certificates with pinned Lean/mathlib kernel checks, separate replay, and false-theorem control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | All formal gates and all six cumulative claim gates pass; negative control exits `1` as intended | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed; no GPU; 5h37m cumulative job |
| `orx/release-candidate-complete-raw-oasis-evidence` | Final cumulative regression plus evaluator-downloadable OASIS evidence in 99 sub-100KB chunks | `uv run --frozen --python 3.12 python -m cdot_repro.run` | All six primary and independent gates pass; 19,800 OASIS rows and 4,950 pairs independently audited | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one numerical thread enforced; 10h34m cumulative job |
| `main` | Public README, report, figures, and notebook | Not run as an experiment (publication surface) | Presentation-only mirror after release gates | No experiment compute |

---

Original workspace identifier:
`icml26-repro-nPC7M7XLEv-convex-distance-operator-transport-a-convex-and-geometry-preserving-formulat`.

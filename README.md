# Convex Distance Operator Transport — claim-by-claim reproduction

This experiment line reproduces the theoretical claims in
[arXiv 2606.02047](https://arxiv.org/abs/2606.02047). The frozen baseline
tests Theorem 3.4's population existence and convexity claim. This child adds
Theorems 3.5 and 3.7: the pseudometric proof obligations and the exact
dispersion identity.

Claims 1 and 2 are `VERIFIED` candidates after all primary, independent, and
control gates passed. This child adds the exact Theorem 5.6 / Corollary 5.7
risk-bound certificate. Finite panels are formula checks, not substitutes for
the population coupling, operator, and gluing arguments. Compute is Hugging
Face `cpu-upgrade` with one enforced numerical thread because clean
locked-environment setup has uncertain runtime.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Detailed evidence: [Claim 1](candidate/pages/claim-1-convex-qp/page.md) and
[Claim 2](candidate/pages/claim-2-pseudometric-dispersion/page.md).
The pending child page is
[Claim 6](candidate/pages/claim-6-risk-bound-consistency/page.md).

## Experiment log

| Branch / experiment | Purpose | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `orx/baseline-source-pin-and-claim-1-certificate` | Source pin, Theorem 3.4 certificate, verifier, checker, control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claim 1 `VERIFIED` candidate; all gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one thread enforced; 32 s job |
| `orx/claim-2-pseudometric-and-dispersion-certificate` | Add Theorems 3.5/3.7 certificate, exhaustive finite domain, raw-witness checker, control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claims 1–2 `VERIFIED` candidates; all gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one thread enforced; 26 s job |
| `orx/claim-6-risk-bound-and-consistency-certificate` | Add Theorem 5.6 / Corollary 5.7 proof obligations, exact FW schedule, independent checker, invalid-schedule control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Pending cumulative run | Hugging Face `cpu-upgrade`; one enforced thread |

---

Original workspace identifier:
`icml26-repro-nPC7M7XLEv-convex-distance-operator-transport-a-convex-and-geometry-preserving-formulat`.

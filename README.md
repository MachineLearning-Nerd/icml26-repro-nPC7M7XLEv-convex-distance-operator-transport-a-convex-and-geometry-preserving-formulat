# Convex Distance Operator Transport — claim-by-claim reproduction

This experiment line reproduces the theoretical claims in
[arXiv 2606.02047](https://arxiv.org/abs/2606.02047). The frozen baseline
tests Theorem 3.4's population existence and convexity claim. This child adds
Theorems 3.5 and 3.7: the pseudometric proof obligations and the exact
dispersion identity.

Claims 1, 2, and 6 are `VERIFIED` candidates after all primary, independent,
and control gates passed. This child adds an exhaustive primary-archive test
of Claim 4's explicit 696-subject/170-node OASIS-3 cohort invariant. It does
not describe the Table 3 numeric cells as rerun. Compute is Hugging Face
`cpu-upgrade`; extraction may use four cores while numerical checks retain one
enforced thread.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Detailed evidence: [Claim 1](candidate/pages/claim-1-convex-qp/page.md) and
[Claim 2](candidate/pages/claim-2-pseudometric-dispersion/page.md).
The pending child page is
[Claim 4](candidate/pages/claim-4-oasis-cohort/page.md); the completed third
theorem page is [Claim 6](candidate/pages/claim-6-risk-bound-consistency/page.md).

## Experiment log

| Branch / experiment | Purpose | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `orx/baseline-source-pin-and-claim-1-certificate` | Source pin, Theorem 3.4 certificate, verifier, checker, control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claim 1 `VERIFIED` candidate; all gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one thread enforced; 32 s job |
| `orx/claim-2-pseudometric-and-dispersion-certificate` | Add Theorems 3.5/3.7 certificate, exhaustive finite domain, raw-witness checker, control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claims 1–2 `VERIFIED` candidates; all gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one thread enforced; 26 s job |
| `orx/claim-6-risk-bound-and-consistency-certificate` | Add Theorem 5.6 / Corollary 5.7 proof obligations, exact FW schedule, independent checker, invalid-schedule control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Claims 1, 2, and 6 `VERIFIED` candidates; all gates pass | Hugging Face `cpu-upgrade`; 64 logical CPUs exposed, one thread enforced; 27 s job |
| `orx/claim-4-exhaustive-oasis-3-cohort-falsification` | Exhaustively hash and parse the primary OASIS-3 archive; independently check any 170-node counterexample and reject padding | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Pending cumulative run | Hugging Face `cpu-upgrade`; four extraction cores estimated |

---

Original workspace identifier:
`icml26-repro-nPC7M7XLEv-convex-distance-operator-transport-a-convex-and-geometry-preserving-formulat`.

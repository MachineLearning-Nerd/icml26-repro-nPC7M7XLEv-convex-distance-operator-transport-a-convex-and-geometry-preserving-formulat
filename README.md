# Convex Distance Operator Transport — claim-by-claim reproduction

This branch freezes the first rigorous baseline for
[arXiv 2606.02047](https://arxiv.org/abs/2606.02047). It tests Theorem 3.4's
population existence and convexity claim using an independently reconstructed
proof-obligation certificate, an executable 60-panel transport-polytope audit,
an independent vectorized checker, and a destructive non-convex control.

The formal paper value is a universal theorem rather than a scalar. The
baseline assessment remains `BLOCKED` until its first OpenResearch run
finishes. Finite panels are formula checks, not substitutes for the compactness
and lower-semicontinuity argument. Compute is Hugging Face `cpu-upgrade` with
one enforced numerical thread because clean locked-environment setup has
uncertain runtime.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Detailed evidence: [Claim 1 candidate page](candidate/pages/claim-1-convex-qp/page.md).

## Experiment log

| Branch / experiment | Purpose | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `orx/baseline-source-pin-and-claim-1-certificate` | Source pin, theorem certificate, executable verifier, independent checker, destructive control | `uv run --frozen --python 3.12 python -m cdot_repro.run` | Pending first run | Hugging Face `cpu-upgrade`; one enforced thread |

---

Original workspace identifier:
`icml26-repro-nPC7M7XLEv-convex-distance-operator-transport-a-convex-and-geometry-preserving-formulat`.

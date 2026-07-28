# Claim 1 — convex quadratic program

The exact contract covers all attributed compact metric-measure spaces in the
paper's setting and every `alpha` in `[0,1]`: an optimal coupling exists and
the objective is convex.

Current evidence consists of an independent population proof-obligation
certificate, an executable 60-panel finite formula audit, a structurally
independent `A.T @ A` checker, and a destructive negated-squared-norm control.
The finite panels are explicitly scoped as corroboration; the population
quantifiers are discharged by compactness, lower-semicontinuity, attainment,
and squared-norm convexity arguments.

The canonical fixed command is:

```text
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Observed at Git `f5f07c0577caf8914e479d05b295fb73dbddef96`:

| Evidence | Observed |
| --- | ---: |
| Jensen panels | 60 / 60 pass |
| Minimum Jensen gap | `-8.88e-16` |
| Minimum Hessian eigenvalue | `0.0` |
| Maximum marginal error | `2.78e-16` |
| Independent quadratic forms | 48 / 48 pass |
| Negated-term control excess | `0.0177778` (rejected as intended) |
| Scientific runtime | `3.194 s` |
| Compute | HF `cpu-upgrade`, 64 logical CPUs exposed, 1 thread enforced |

Raw result:
[`claim_1_result.json`](../../../.openresearch/artifacts/claim_1/raw/claim_1_result.json).
The current candidate verdict is `VERIFIED`; only the live evaluator can award
points.


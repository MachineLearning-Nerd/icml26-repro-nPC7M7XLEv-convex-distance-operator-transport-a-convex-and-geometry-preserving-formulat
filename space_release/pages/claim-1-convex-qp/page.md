# CURRENT — Claim 1: convex quadratic program

---
<!-- trackio-cell
{"type":"markdown","id":"cell_current_claim_1","created_at":"2026-07-29T04:00:00+00:00","title":"CURRENT \u2014 Claim 1: convex quadratic program","pinned":true,"pinned_at":"2026-07-29T04:00:00+00:00"}
-->
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
[`claim_1_result.json`](../../current/evidence/claim_1/raw/claim_1_result.json).
The current candidate verdict is `VERIFIED`; only the live evaluator can award
points.

## Exact source statement and assumptions

- Source: ar5iv HTML for arXiv `2606.02047v1`
- URL: https://ar5iv.labs.arxiv.org/html/2606.02047
- Retrieved: `2026-07-28T12:12:31Z` with explicit User-Agent `OpenResearch-Reproduction/1.0`
- HTML SHA-256: `602040fe82ec6bd4c0422ee488315d8e09f86bef50c6f06d4be61f942094d43f`
- PDF SHA-256: `fe1dda5d0e3f2aea86b9b3b5ebf79b79cbc7d06e3fcbe4b20b6f097cc556375d`
- Theorem anchor: `#S3.Thmtheorem4`
- Proof anchor: Appendix G.3

The exact scope is universal over two attributed compact metric-measure
spaces and every fusion weight `alpha` in the closed unit interval. The result
has two conjuncts: the infimum over fixed-marginal couplings is attained, and
the objective is convex in the coupling. The source attributes attainment to
weak compactness plus lower semicontinuity, and convexity to affine dependence
of the conditional-expectation operator followed by convexity of a squared
Hilbert--Schmidt norm.

Finite numerical panels cannot establish this universal population theorem.
They are retained only as executable formula checks and regression tests.


## Executable method

The primary verifier reconstructs the objective from the paper's finite-sample
operator formula. It checks 60 deterministic transport-polytope panels, exact
marginals, Jensen inequalities, vectorized Hessian eigenvalues, and monotone
Frank--Wolfe line searches. SymPy independently reduces the generic
squared-affine Jensen gap to
`theta(1-theta)||r1-r2||^2`.

The independent checker does not call the primary objective. It rebuilds the
Kronecker linear map and evaluates 48 unrelated quadratic forms of `A.T @ A`.
The destructive control negates the squared structural term; the verifier
requires a strict Jensen violation. A control that remains convex therefore
causes the run to exit nonzero.

The analytical certificate supplies the population-level compactness,
lower-semicontinuity, attainment, and affine-operator obligations that finite
execution cannot prove.


The verifier is invoked only through the fixed cumulative command. The runner raises on any failed claim gate, checker gate, or control gate, so the process exits nonzero when the published evidence does not validate.

### Code

- [Primary verifier](../../current/code/claim1.py)
- [Independent checker](../../current/code/claim1_checker.py)
- [Cumulative nonzero-exit runner](../../current/code/run.py)

### Raw machine-readable evidence

- [claim_1_result.json](../../current/evidence/claim_1/raw/claim_1_result.json)

Final cumulative regression: run `4df2d784-42ce-4fa3-af50-3d03063f38fb` at Git `e11a535552fc6f854fe5c07086034992ae426eae` reran all six claims; every primary and independent checker gate passed. [Cumulative run summary](../../current/evidence/claim_4/raw/formal_4df2d784/run_summary.json).

### Claim contract and evaluation files

- [EVAL.md](../../current/evidence/claim_1/EVAL.md)
- [claim_contract.json](../../current/evidence/claim_1/claim_contract.json)
- [limitations.md](../../current/evidence/claim_1/limitations.md)
- [method.md](../../current/evidence/claim_1/method.md)
- [proof_certificate.md](../../current/evidence/claim_1/proof_certificate.md)
- [source_audit.md](../../current/evidence/claim_1/source_audit.md)

## Provenance

- Verdict: **VERIFIED**
- Confidence: **HIGH**
- Formal run: `f02320fc-a5e7-423b-9f1c-9186a05d0b3f`
- Evidence Git SHA: `f5f07c0577caf8914e479d05b295fb73dbddef96`
- Seeds: PCG64 seed 260602047
- Runtime: 3.194 scientific seconds
- Compute: Hugging Face `cpu-upgrade`, 64 logical CPUs exposed; per-process numerical thread limits are recorded in the result.
- Exact command: `uv run --frozen --python 3.12 python -m cdot_repro.run`
- Pinned environment: [pyproject.toml](../../current/environment/pyproject.toml), [uv.lock](../../current/environment/uv.lock)

## Limitations and deviations

- The analytical certificate is human-checkable and executable-obligation
  backed; it is not a Lean, Coq, or Isabelle kernel proof.
- The finite panels corroborate formulas only and are not presented as proof
  of the universally quantified theorem.
- The paper provides no official implementation, so the finite objective was
  reconstructed directly from its equations.

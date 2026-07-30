# CURRENT — Claim 2: Lean-checked pseudometric core and dispersion gap

---
<!-- trackio-cell
{"type":"markdown","id":"cell_lean_claim_2","created_at":"2026-07-30T12:00:00+00:00","title":"CURRENT \u2014 Claim 2: Lean-checked pseudometric core and dispersion gap","pinned":true,"pinned_at":"2026-07-30T12:00:00+00:00"}
-->
**Current evidence status: VERIFIED. Confidence: MEDIUM.**

This is the superseding verifier for Claim 2. The earlier human proof
certificate and finite-panel page is preserved unchanged under **Historical
rejected baseline** and is not the current proof evidence.

## Exact source statement and assumptions

Theorem 3.5 states that the square-root CDOT discrepancy is a pseudometric on attributed compact metric-measure spaces; Theorem 3.7 states for every coupling `π` that `R_GW,2(π) - R(π) = V(π)`.

The exact theorem/section anchors, assumptions, and quantifiers are retained in
the [original claim source audit](../../current/evidence/claim_2/source_audit.md).
The machine-checked declarations are `claim2_weighted_fusion_triangle`, `claim2_dispersion_gap`, and `claim2_variance_additivity`.

## Executable method

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

It ran the pinned Lean checker before rerunning all six accepted claim checks.
The checker downloaded a SHA-256-pinned `elan` archive, installed Lean 4.19.0,
resolved mathlib to an exact commit, compiled the primary proof, built the Lake
library, imported every public declaration from a separate compilation unit,
and attempted to compile a deliberately false theorem. The cumulative runner
exits nonzero if any formal, empirical, independent-checker, or control gate
fails.

### Code

- [Primary Lean source](../../current/formal_lean_6b7ccf1e/CDOTProofs.lean)
- [Independent replay](../../current/formal_lean_6b7ccf1e/IndependentReplay.lean)
- [False-theorem negative control](../../current/formal_lean_6b7ccf1e/NegativeControl.lean)
- [Pinned Lean toolchain](../../current/formal_lean_6b7ccf1e/lean-toolchain)
- [Pinned Lake project](../../current/formal_lean_6b7ccf1e/lakefile.toml)
- [Python formal gate](../../current/code/formal_checker.py)
- [Cumulative nonzero-exit runner](../../current/code/run.py)

### Data inline

| Kernel item | Observed |
| --- | --- |
| Weighted two-component Minkowski | kernel accepted |
| Dispersion/conditional-variance identity | kernel accepted |
| Independent compilation unit | return code `0`, `3.999676832 s` |
| Source hash recomputation | exact match |
| Existing exhaustive corroboration | 320/320 declared pseudometric cells and 32/32 diffuse-coupling identities pass |
| Squared-distance destructive control | triangle violation excess `0.0812` |

### Raw machine-readable evidence

- [Formal gate summary](../../current/evidence/formal_lean_6b7ccf1e/raw/formal_gate_summary.json)
- [Independent checker output](../../current/evidence/formal_lean_6b7ccf1e/raw/formal_independent_checker.json)
- [Negative-control output](../../current/evidence/formal_lean_6b7ccf1e/raw/formal_negative_control.json)
- [Prior numerical result](../../current/evidence/claim_2/raw/claim_2_result.json)
- [Prior independent numerical checker](../../current/evidence/claim_2/raw/claim_2_independent_checker.json)

### Claim contract and evaluation files

- [Theorem-to-paper mapping](../../current/evidence/formal_lean_6b7ccf1e/theorem_mapping.md)
- [Formal limitations](../../current/evidence/formal_lean_6b7ccf1e/limitations.md)
- [Original claim contract](../../current/evidence/claim_2/claim_contract.json)
- [Original source audit](../../current/evidence/claim_2/source_audit.md)
- [Original method](../../current/evidence/claim_2/method.md)
- [Original evaluation record](../../current/evidence/claim_2/EVAL.md)

## Provenance

- Reviewer verdict proposed by the reproduction: **VERIFIED**
- Previous live judge points: `1/2`; possible points: `2/2`
- Formal run: `6b7ccf1e-9abb-4909-aa87-0712d870cebc`
- Experiment: `a78f7331-673b-4e9a-ad45-41761cc8e799`
- Evidence Git SHA: `4aadbbfe008cc725fbba6005ccbadacb929db40c`
- Fixed command: `uv run --frozen --python 3.12 python -m cdot_repro.run`
- Runtime: `5h37m` cumulative; individual Lean-stage timings are in the raw JSON
- Compute: Hugging Face `cpu-upgrade`; estimated 2 cores, 64 logical CPUs
  exposed, no GPU
- Lean: `4.19.0` commit `6caaee842e94`
- mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`
- Seeds: deterministic formal compilation; empirical regression seeds remain
  on the preserved prior page
- Pinned environment:
  [pyproject.toml](../../current/environment/pyproject.toml) and
  [uv.lock](../../current/environment/uv.lock)

## Limitations and deviations

The final weighted Minkowski theorem takes the feature and operator component triangle inequalities as premises. The paper's gluing/conditional-expectation construction is audited analytically; the exact dispersion algebra and final norm step are kernel checked.

These abstraction boundaries are explicit. Finite numerical panels remain
corroboration only and are not used as a universal proof.

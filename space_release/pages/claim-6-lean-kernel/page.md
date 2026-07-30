# CURRENT — Claim 6: Lean-checked risk constants and consistency

---
<!-- trackio-cell
{"type":"markdown","id":"cell_lean_claim_6","created_at":"2026-07-30T12:00:00+00:00","title":"CURRENT \u2014 Claim 6: Lean-checked risk constants and consistency","pinned":true,"pinned_at":"2026-07-30T12:00:00+00:00"}
-->
**Current evidence status: VERIFIED. Confidence: MEDIUM.**

This is the superseding verifier for Claim 6. The earlier human proof
certificate and finite-panel page is preserved unchanged under **Historical
rejected baseline** and is not the current proof evidence.

## Exact source statement and assumptions

Theorem 5.6 bounds excess risk by `32 α n_min/(T+3) + 4(2L_f+2L_W+4)(W1X+W1Y)` under Assumptions 5.2–5.5. Corollary 5.7 states consistency when the statistical terms vanish and `n_min/T_n → 0`.

The exact theorem/section anchors, assumptions, and quantifiers are retained in
the [original claim source audit](../../current/evidence/claim_6/source_audit.md).
The machine-checked declarations are `claim6_three_obligation_bound`, `claim6_optimization_monotone`, `claim6_consistency_squeeze`, and `claim6_bad_schedule_control`.

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
| Exact `E1+E2+E3` constant | kernel accepted |
| Fixed-sample `O(1/T)` monotonicity | kernel accepted |
| Epsilon-form consistency squeeze | kernel accepted |
| Invalid `T_n=n_min` schedule | kernel proves ratio remains `1` |
| Existing FW corroboration | maximum duality gap `9.900242946852059e-06` |
| Numerical schedule control | rejected with final optimization term `15.953261927945473` |

### Raw machine-readable evidence

- [Formal gate summary](../../current/evidence/formal_lean_6b7ccf1e/raw/formal_gate_summary.json)
- [Independent checker output](../../current/evidence/formal_lean_6b7ccf1e/raw/formal_independent_checker.json)
- [Negative-control output](../../current/evidence/formal_lean_6b7ccf1e/raw/formal_negative_control.json)
- [Prior numerical result](../../current/evidence/claim_6/raw/claim_6_result.json)
- [Prior independent numerical checker](../../current/evidence/claim_6/raw/claim_6_independent_checker.json)

### Claim contract and evaluation files

- [Theorem-to-paper mapping](../../current/evidence/formal_lean_6b7ccf1e/theorem_mapping.md)
- [Formal limitations](../../current/evidence/formal_lean_6b7ccf1e/limitations.md)
- [Original claim contract](../../current/evidence/claim_6/claim_contract.json)
- [Original source audit](../../current/evidence/claim_6/source_audit.md)
- [Original method](../../current/evidence/claim_6/method.md)
- [Original evaluation record](../../current/evidence/claim_6/EVAL.md)

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

The kernel combines the exact three paper obligations and checks the asymptotic squeeze. It does not formalize the empirical-process derivation of each `E1`, `E2`, and `E3` obligation from first principles.

These abstraction boundaries are explicit. Finite numerical panels remain
corroboration only and are not used as a universal proof.

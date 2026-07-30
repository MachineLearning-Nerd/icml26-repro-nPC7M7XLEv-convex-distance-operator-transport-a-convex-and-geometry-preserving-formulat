# Lean kernel verification for CDOT Claims 1, 2, and 6

The live judge awarded 9/12 at Space revision
`e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032`. Its only remaining criticism
was that the three universal theorem claims relied on finite numerical checks
and human-written certificates. Run
`6b7ccf1e-9abb-4909-aa87-0712d870cebc` addresses that criticism with a pinned
Lean project and reruns all six claim checks cumulatively.

| Gate | Observed |
| --- | --- |
| Lean | 4.19.0, commit `6caaee842e94` |
| mathlib | `c44e0c8ee63ca166450922a373c7409c5d26b00b` |
| Source SHA-256 | `5f56b005ebf859199d653e09fe114731abb1f75f577819180cdd85f223aabd0d` |
| Primary compile | return code `0` |
| Lake build | return code `0` |
| Independent replay | return code `0` |
| False-theorem control | return code `1`, rejected as intended |
| Forbidden tokens | no `sorry`, `admit`, custom `axiom`, or `unsafe` |
| Cumulative result | every formal and Claim 1–6 gate passed |
| Compute | Hugging Face `cpu-upgrade`, 64 logical CPUs, no GPU, 5h37m |

## Theorem mapping

- Claim 1: compact continuous attainment, the squared-residual identity, and
  Jensen convexity of the affine-feature plus squared-affine-residual CDOT
  objective.
- Claim 2: the weighted two-component Minkowski step and the exact
  conditional-variance dispersion identity.
- Claim 6: the exact `E1+E2+E3` constants, fixed-sample `O(1/T)`
  monotonicity, epsilon-form consistency squeeze, and an invalid-schedule
  control.

The executable source is [CDOTProofs.lean](../../formal/CDOTProofs.lean), with
[IndependentReplay.lean](../../formal/IndependentReplay.lean) and
[NegativeControl.lean](../../formal/NegativeControl.lean).

## Honest boundary

The formalization kernel-checks the theorem architecture. Paper-specific
measure/operator constructions remain explicit premises: continuity of the
population objective for Claim 1, component triangle inequalities from the
gluing construction for Claim 2, and the three empirical-process obligations
for Claim 6. These boundaries are the remaining judge-interpretation risk, so
12/12 is a forecast rather than a claimed result.

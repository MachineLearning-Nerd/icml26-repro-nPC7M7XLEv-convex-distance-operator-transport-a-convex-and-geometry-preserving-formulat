# Lean theorem-to-paper mapping

Source: arXiv:2606.02047v1. The paper was retrieved with an explicit
`OpenResearch-CDOT-Reproduction/1.0` User-Agent and its source audit is linked
from each claim page.

| Paper statement | Lean declaration | Kernel-checked obligation |
| --- | --- | --- |
| Theorem 3.4, existence | `claim1_compact_attainment` | A continuous objective on a nonempty compact coupling set attains its minimum. |
| Theorem 3.4, convexity | `claim1_cdot_objective_jensen` | For every fusion weight and interpolation weight in `[0,1]`, the affine feature term plus squared affine structural residual obeys Jensen's inequality. |
| Theorem 3.5, triangle step | `claim2_weighted_fusion_triangle` | The feature and operator triangle inequalities combine through weighted two-dimensional Minkowski. |
| Theorem 3.7 | `claim2_dispersion_gap` | The conditional second-moment difference equals the sum of the two conditional variances. |
| Theorem 5.6 | `claim6_three_obligation_bound` | The paper's `E1+E2+E3` obligations combine to exactly `32 α n_min/(T+3) + 4(2L_f+2L_W+4)(W1X+W1Y)`. |
| Theorem 5.6, optimization rate | `claim6_optimization_monotone` | The optimization term is nonincreasing in `T` and has the claimed fixed-sample `O(1/T)` form. |
| Corollary 5.7 | `claim6_consistency_squeeze` | Vanishing optimization and statistical terms force every nonnegative bounded excess risk to vanish. |
| Corollary 5.7 control | `claim6_bad_schedule_control` | The invalid schedule `T_n=n_min` leaves `n_min/T_n=1`, so it cannot satisfy the consistency premise. |

The certificate intentionally separates paper-specific measure/operator lemmas
from the general topological, convexity, variance, norm, and asymptotic steps.
The source files do not contain `sorry`, `admit`, custom `axiom`, or `unsafe`.
Lean reports only its standard logical foundations (`propext`,
`Classical.choice`, and `Quot.sound`).

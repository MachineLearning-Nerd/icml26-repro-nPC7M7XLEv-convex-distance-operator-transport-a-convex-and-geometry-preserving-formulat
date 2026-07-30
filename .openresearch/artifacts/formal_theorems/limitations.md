# Limitations and deviations

- This is a kernel-checked formalization of the theorem architecture and exact
  algebraic/topological obligations used by the paper, not a full
  measure-theory reimplementation of every paper definition.
- Claim 1 exposes continuity of the population loss on the compact coupling
  set as a premise. The paper establishes continuity/lower-semicontinuity
  before its extreme-value step; that paper-specific construction is audited
  textually and by the existing executable operator checks.
- Claim 2 exposes the feature and operator component triangle inequalities as
  premises to the final weighted Minkowski theorem. The paper's gluing and
  conditional-expectation construction remains in the analytical source
  audit; the dispersion identity itself is fully kernel checked.
- Claim 6 kernel-checks the exact constants once the three named paper
  obligations are supplied, plus the independent asymptotic squeeze. It does
  not formalize the empirical-process proof of each obligation from first
  principles.
- These abstraction boundaries are stated explicitly. The finite numerical
  panels remain corroboration and are not described as proofs.

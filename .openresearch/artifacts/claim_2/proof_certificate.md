# Independent proof-obligation certificate for Theorems 3.5 and 3.7

## Pseudometric

Nonnegativity follows from the two nonnegative objective terms. The diagonal
coupling of a space with itself has zero feature mismatch and an identity
conditional-expectation operator commuting with the same distance operator.

Transposing a coupling swaps the two spaces. The new conditional-expectation
operator is the old operator's adjoint, the feature norm is symmetric, and
the Hilbert--Schmidt norm is invariant under adjoint. Taking minima gives
symmetry.

For the triangle inequality, glue optimal `X-Y` and `Y-Z` couplings into the
Markov law `X -> Y -> Z`, and use its `X-Z` marginal as a feasible coupling.
Conditional-expectation operators compose under this law. Each is an `L2`
contraction. Expanding the `X-Z` distance commutator into the sum of an
`X-Y` commutator followed by a contraction and a contraction followed by a
`Y-Z` commutator gives the structural triangle bound by the Hilbert--Schmidt
ideal inequalities. Ordinary Minkowski gives the feature bound. A final
two-coordinate Minkowski inequality, with the paper's square-root weights,
gives the discrepancy triangle inequality. No step establishes identity of
indiscernibles, so the conclusion is exactly pseudometric.

## Dispersion gap

Fix `(x,y)`. Draw `X'` from the conditional law of `X` given `Y=y` and draw
`Y'` independently from the conditional law of `Y` given `X=x`. For
`Z=d_X(x,X')-d_Y(y,Y')`, the GW integrand is `E[Z^2]` and the CDOT integrand
is `(E[Z])^2`. Their difference is `Var(Z)`. Conditional independence splits
that variance into the two terms in the paper's dispersion definition.
Integrating over the fixed product marginals proves the identity for every
coupling.

## Scope

Finite exhaustive cells are executable regression evidence only. Population
quantifiers are carried by the coupling, operator, and variance arguments.


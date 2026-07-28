# Claim 1 method

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


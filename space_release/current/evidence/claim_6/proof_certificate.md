# Independent proof-obligation certificate for Theorem 5.6 and Corollary 5.7

## Deterministic decomposition

Let `pi_n*` minimize the empirical objective and `pi*` be the stable
population minimizer from Assumption 5.5. Insert the empirical objective
twice and the best lifted empirical coupling once. The triangle inequality
decomposes the absolute population-risk error into:

1. `E1`, the empirical optimization error of the returned FW iterate;
2. `E2`, twice the uniform empirical-versus-lifted objective discrepancy;
3. `E3`, the gap between the best lifted empirical coupling and `pi*`.

For Algorithm 1 with `gamma_t=2/(t+2)`, the standard curvature recurrence
gives

`E1 <= 8 alpha n_min (||D_X||_op+||D_Y||_op)^2/(T+3)`.

The paper normalizes each empirical distance operator by its support size and
assumes metric diameter one. Symmetry and the maximum row-sum bound therefore
give `||D_X||_op,||D_Y||_op <= 1`, hence
`E1 <= 32 alpha n_min/(T+3)`.

Glue each discrete coupling through optimal population-to-empirical
Wasserstein couplings. Kantorovich--Rubinstein duality controls the feature
term by feature Lipschitzness. Expanding each distance-operator commutator,
then applying the triangle inequality, diameter-one bound, and the
Wasserstein-Lipschitz conditional kernels from Assumption 5.5 controls both
structural terms. Repeating the same gluing for the stable population
minimizer bounds `E2+E3` by

`4(2L_f+2L_W+4)(W1_X+W1_Y)`.

Adding the three nonnegative bounds is exactly Theorem 5.6, with no
finite-sample trajectory used to establish the universal inequality.

## Almost-sure consistency

On compact metric spaces, iid empirical measures converge almost surely in
`W1`. Corollary 5.7 separately assumes `n_min/T_n -> 0`, so the optimization
term also tends to zero. Both terms on the deterministic right-hand side
therefore vanish almost surely, which squeezes the nonnegative excess risk to
zero. This proves the stated risk consistency and does not assert convergence
of couplings or a dimension-free statistical rate.

## Destructive control

Replacing the required schedule condition by `T_n=n_min` leaves
`n_min/T_n=1` and makes the optimization bound tend to `32 alpha`, not zero.
The executable verifier must reject this schedule. The control isolates the
exact asymptotic premise rather than merely perturbing a tolerance.

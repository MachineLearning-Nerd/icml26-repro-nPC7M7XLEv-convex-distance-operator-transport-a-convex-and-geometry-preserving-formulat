# Independent proof-obligation certificate for Theorem 3.4

This is an independently reconstructed analytical certificate, not a claim
that finite numerical tests prove a population theorem.

## Setting and finiteness

Let the two underlying spaces be compact metric spaces with Borel probability
measures and continuous feature maps. Their distance kernels and feature
costs are bounded. Conditional expectation is an `L2` contraction, so the
distance-operator commutator is Hilbert--Schmidt and the objective is finite.

## Existence

1. The product of the two marginals is a coupling, so the feasible set is
   nonempty.
2. Probability measures on the compact product form a tight family. The two
   marginal constraints are weakly closed, hence the coupling set is weakly
   compact.
3. The feature cost is bounded and continuous, so its integral is weakly
   continuous.
4. For continuous test functions `f` and `g`, the bilinear form of the
   conditional-expectation operator is the integral of `f(x)g(y)` against the
   coupling. Weak convergence of couplings therefore gives weak-operator
   convergence on continuous functions; density and the common contraction
   bound extend this to the relevant `L2` spaces.
5. Composition with the two fixed bounded distance operators preserves
   weak-operator convergence. The squared Hilbert--Schmidt norm is lower
   semicontinuous because it is the supremum of finite sums of squared matrix
   coefficients.
6. The full objective is weakly lower semicontinuous on a nonempty weakly
   compact set, so its infimum is attained.

## Convexity

For two couplings with the same marginals, disintegration of their convex
mixture gives the same convex mixture of their conditional laws. Thus the
conditional-expectation operator, its distance commutator, and the finite
operator residual are affine in the coupling. The feature term is affine.
For any Hilbert-space vectors `a,b` and `theta` in `[0,1]`,

`theta||a||^2 + (1-theta)||b||^2 - ||theta*a+(1-theta)*b||^2
 = theta(1-theta)||a-b||^2 >= 0`.

Therefore the squared Hilbert--Schmidt term and the complete objective are
convex for every permitted fusion weight.

## Scope

Compactness and continuity are retained. No finite-support assumption is used
for the population proof. The executable panels test the derived formulas,
not the universal quantifiers.


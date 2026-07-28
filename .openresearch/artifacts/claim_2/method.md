# Claim 2 method

The population certificate independently reconstructs the transpose-coupling
symmetry, Markov gluing, conditional-expectation contraction and composition,
Hilbert--Schmidt ideal inequalities, and the conditional-variance identity.

The executable verifier exhausts 320 cells over a predeclared complete finite
domain of four two-point spaces, 64 ordered triples, and five fusion weights.
It separately evaluates the dispersion identity on 32 diffuse couplings.
Every raw matrix and coupling is serialized so the independent checker can
recompute the four-index GW sum without calling the primary `einsum`.

The destructive control squares an otherwise valid discrepancy. The verifier
requires that mutation to violate triangle inequality.


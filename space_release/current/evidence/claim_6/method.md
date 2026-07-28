# Claim 6 method

The fixed cumulative command runs two predeclared finite panels with support
12/24, seeds 56001/56002, alpha 0.25/0.8, and 2,048 iterations of the exact
Algorithm 1 schedule. It records objectives and FW duality gaps at fixed
checkpoints. A separate checker reconstructs the gradient, linear assignment,
duality gap, marginals, and bound formula from raw matrices.

The executable also evaluates a declared `T_n=n^2` sequence for dimensions
three and five and a destructive `T_n=n` control. These rows diagnose the two
terms; they are not evidence for the universal theorem or empirical
Wasserstein convergence. The proof-obligation certificate is the claim-level
evidence.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

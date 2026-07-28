# Claim 5 limitations and deviations

- The source split seeds are unavailable; three predeclared PCG64-compatible
  integer seeds are reported.
- ENZYMES attributes are dataset-wise z-scored and each pair's feature-cost
  matrix is max-normalized. The paper does not specify either choice.
- The source gives an iteration ceiling but no stopping tolerance; this run
  discloses stationary and POT tolerances.
- A direction reversal is accepted only if every data, pair, optimizer,
  nested-CV, checker, and negative-control gate passes.

import CDOTProofs

set_option autoImplicit false

-- Deliberately false sign reversal.  A sound kernel must reject this file.
example (θ u v : ℝ) (hθ0 : 0 ≤ θ) (hθ1 : θ ≤ 1) :
    θ * u ^ 2 + (1 - θ) * v ^ 2 ≤
      (θ * u + (1 - θ) * v) ^ 2 := by
  nlinarith [CDOTFormal.claim1_squared_residual_jensen θ u v hθ0 hθ1]

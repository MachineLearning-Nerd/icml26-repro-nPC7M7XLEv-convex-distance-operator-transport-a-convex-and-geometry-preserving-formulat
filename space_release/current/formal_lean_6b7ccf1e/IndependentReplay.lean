import CDOTProofs

set_option autoImplicit false

open CDOTFormal

-- This separate compilation unit verifies that the public theorem names and
-- types are importable from the compiled certificate.
#check claim1_compact_attainment
#check claim1_squared_residual_identity
#check claim1_cdot_objective_jensen
#check claim2_weighted_fusion_triangle
#check claim2_dispersion_gap
#check claim6_three_obligation_bound
#check claim6_optimization_monotone
#check claim6_consistency_squeeze
#check claim6_bad_schedule_control

example (θ u v : ℝ) :
    θ * u ^ 2 + (1 - θ) * v ^ 2 -
        (θ * u + (1 - θ) * v) ^ 2 =
      θ * (1 - θ) * (u - v) ^ 2 :=
  claim1_squared_residual_identity θ u v

example (ex ex2 ey ey2 : ℝ) :
    (ex2 + ey2 - 2 * ex * ey) - (ex - ey) ^ 2 =
      (ex2 - ex ^ 2) + (ey2 - ey ^ 2) :=
  claim2_dispersion_gap ex ex2 ey ey2

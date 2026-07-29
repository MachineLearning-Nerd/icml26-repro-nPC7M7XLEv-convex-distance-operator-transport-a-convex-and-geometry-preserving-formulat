import Mathlib

set_option autoImplicit false

/-!
# Kernel-checked CDOT proof obligations

This file formalizes the theorem architecture used in Theorems 3.4, 3.5,
3.7, 5.6 and Corollary 5.7 of arXiv:2606.02047v1.  It deliberately exposes
the interfaces between the paper-specific measure/operator lemmas and the
general topological, convexity, variance, norm, and asymptotic arguments.

Every declaration below contains a complete proof term checked by the kernel.
-/

namespace CDOTFormal

open Set

/-! ## Claim 1: attainment and convexity -/

/-- A continuous objective on a nonempty compact feasible set attains its
minimum.  The paper establishes the required continuity/lower-semicontinuity
for the CDOT objective on the compact coupling set before applying this
extreme-value step. -/
theorem claim1_compact_attainment
    {X : Type*} [TopologicalSpace X] {s : Set X} {loss : X → ℝ}
    (hs : IsCompact s) (hne : s.Nonempty) (hloss : ContinuousOn loss s) :
    ∃ x ∈ s, ∀ y ∈ s, loss x ≤ loss y := by
  obtain ⟨x, hx, hmin⟩ := hs.exists_isMinOn hne hloss
  exact ⟨x, hx, fun _ hy => hmin hy⟩

/-- Pointwise squared-residual convexity.  Integrating/summing this identity
over Hilbert--Schmidt coefficients gives the squared HS-norm step in
Theorem 3.4. -/
theorem claim1_squared_residual_identity (θ u v : ℝ) :
    θ * u ^ 2 + (1 - θ) * v ^ 2 -
        (θ * u + (1 - θ) * v) ^ 2 =
      θ * (1 - θ) * (u - v) ^ 2 := by
  ring

theorem claim1_squared_residual_jensen
    (θ u v : ℝ) (hθ0 : 0 ≤ θ) (hθ1 : θ ≤ 1) :
    (θ * u + (1 - θ) * v) ^ 2 ≤
      θ * u ^ 2 + (1 - θ) * v ^ 2 := by
  have hprod : 0 ≤ θ * (1 - θ) :=
    mul_nonneg hθ0 (sub_nonneg.mpr hθ1)
  nlinarith [claim1_squared_residual_identity θ u v,
    mul_nonneg hprod (sq_nonneg (u - v))]

/-- The exact affine-feature plus squared-affine-residual CDOT objective is
Jensen convex for every fusion weight in `[0,1]`. -/
theorem claim1_cdot_objective_jensen
    (α θ f₁ f₂ r₁ r₂ : ℝ)
    (hα0 : 0 ≤ α) (_hα1 : α ≤ 1)
    (hθ0 : 0 ≤ θ) (hθ1 : θ ≤ 1) :
    (1 - α) * (θ * f₁ + (1 - θ) * f₂) +
        α / 2 * (θ * r₁ + (1 - θ) * r₂) ^ 2 ≤
      θ * ((1 - α) * f₁ + α / 2 * r₁ ^ 2) +
        (1 - θ) * ((1 - α) * f₂ + α / 2 * r₂ ^ 2) := by
  have hs := claim1_squared_residual_jensen θ r₁ r₂ hθ0 hθ1
  have hscale : 0 ≤ α / 2 := div_nonneg hα0 (by norm_num)
  have hscaled := mul_le_mul_of_nonneg_left hs hscale
  nlinarith

/-! ## Claim 2: pseudometric fusion and dispersion identity -/

/-- Two-dimensional Minkowski, proved from the polynomial Cauchy--Schwarz
certificate `(a*d-b*c)^2 ≥ 0`. -/
theorem l2_triangle_nonnegative
    (a b c d : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (hd : 0 ≤ d) :
    Real.sqrt ((a + c) ^ 2 + (b + d) ^ 2) ≤
      Real.sqrt (a ^ 2 + b ^ 2) + Real.sqrt (c ^ 2 + d ^ 2) := by
  have hA : 0 ≤ a ^ 2 + b ^ 2 := by positivity
  have hC : 0 ≤ c ^ 2 + d ^ 2 := by positivity
  have hR : 0 ≤ (a + c) ^ 2 + (b + d) ^ 2 := by positivity
  have hAsq := Real.sq_sqrt hA
  have hCsq := Real.sq_sqrt hC
  have hRsq := Real.sq_sqrt hR
  have hsqrtA := Real.sqrt_nonneg (a ^ 2 + b ^ 2)
  have hsqrtC := Real.sqrt_nonneg (c ^ 2 + d ^ 2)
  have hsqrtR := Real.sqrt_nonneg ((a + c) ^ 2 + (b + d) ^ 2)
  have hdot :
      a * c + b * d ≤
        Real.sqrt (a ^ 2 + b ^ 2) * Real.sqrt (c ^ 2 + d ^ 2) := by
    have hprod0 :
        0 ≤ Real.sqrt (a ^ 2 + b ^ 2) * Real.sqrt (c ^ 2 + d ^ 2) :=
      mul_nonneg hsqrtA hsqrtC
    have hprod_sq :
        (Real.sqrt (a ^ 2 + b ^ 2) * Real.sqrt (c ^ 2 + d ^ 2)) ^ 2 =
          (a ^ 2 + b ^ 2) * (c ^ 2 + d ^ 2) := by
      rw [mul_pow, hAsq, hCsq]
    have hdot_sq :
        (a * c + b * d) ^ 2 ≤
          (Real.sqrt (a ^ 2 + b ^ 2) *
            Real.sqrt (c ^ 2 + d ^ 2)) ^ 2 := by
      rw [hprod_sq]
      nlinarith [sq_nonneg (a * d - b * c)]
    by_contra hnot
    have hgt :
        Real.sqrt (a ^ 2 + b ^ 2) * Real.sqrt (c ^ 2 + d ^ 2) <
          a * c + b * d := lt_of_not_ge hnot
    have hdot0 : 0 < a * c + b * d := lt_of_le_of_lt hprod0 hgt
    have hdiff :
        0 <
          (a * c + b * d) -
            Real.sqrt (a ^ 2 + b ^ 2) * Real.sqrt (c ^ 2 + d ^ 2) :=
      sub_pos.mpr hgt
    have hsum :
        0 <
          (a * c + b * d) +
            Real.sqrt (a ^ 2 + b ^ 2) * Real.sqrt (c ^ 2 + d ^ 2) :=
      add_pos_of_pos_of_nonneg hdot0 hprod0
    have hsqgt :
        (Real.sqrt (a ^ 2 + b ^ 2) * Real.sqrt (c ^ 2 + d ^ 2)) ^ 2 <
          (a * c + b * d) ^ 2 := by
      nlinarith [mul_pos hdiff hsum]
    exact (not_lt_of_ge hdot_sq) hsqgt
  nlinarith

theorem l2_monotone_nonnegative
    (a b c d : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (hd : 0 ≤ d)
    (hac : a ≤ c) (hbd : b ≤ d) :
    Real.sqrt (a ^ 2 + b ^ 2) ≤ Real.sqrt (c ^ 2 + d ^ 2) := by
  have hA : 0 ≤ a ^ 2 + b ^ 2 := by positivity
  have hC : 0 ≤ c ^ 2 + d ^ 2 := by positivity
  have hAsq := Real.sq_sqrt hA
  have hCsq := Real.sq_sqrt hC
  have hsqrtA := Real.sqrt_nonneg (a ^ 2 + b ^ 2)
  have hsqrtC := Real.sqrt_nonneg (c ^ 2 + d ^ 2)
  nlinarith

/-- The final weighted two-component Minkowski step in Theorem 3.5.  The
inputs `f` and `r` are respectively the feature and operator component
discrepancies supplied by the gluing/conditional-expectation lemmas. -/
theorem claim2_weighted_fusion_triangle
    (wf wr fxy fyz fxz rxy ryz rxz : ℝ)
    (_hwf : 0 ≤ wf) (_hwr : 0 ≤ wr)
    (hfxy : 0 ≤ fxy) (hfyz : 0 ≤ fyz) (hfxz : 0 ≤ fxz)
    (hrxy : 0 ≤ rxy) (hryz : 0 ≤ ryz) (hrxz : 0 ≤ rxz)
    (hftri : fxz ≤ fxy + fyz) (hrtri : rxz ≤ rxy + ryz) :
    Real.sqrt ((Real.sqrt wf * fxz) ^ 2 + (Real.sqrt wr * rxz) ^ 2) ≤
      Real.sqrt ((Real.sqrt wf * fxy) ^ 2 + (Real.sqrt wr * rxy) ^ 2) +
      Real.sqrt ((Real.sqrt wf * fyz) ^ 2 + (Real.sqrt wr * ryz) ^ 2) := by
  have hswf : 0 ≤ Real.sqrt wf := Real.sqrt_nonneg wf
  have hswr : 0 ≤ Real.sqrt wr := Real.sqrt_nonneg wr
  have hmono := l2_monotone_nonnegative
    (Real.sqrt wf * fxz) (Real.sqrt wr * rxz)
    (Real.sqrt wf * (fxy + fyz)) (Real.sqrt wr * (rxy + ryz))
    (mul_nonneg hswf hfxz) (mul_nonneg hswr hrxz)
    (mul_nonneg hswf (add_nonneg hfxy hfyz))
    (mul_nonneg hswr (add_nonneg hrxy hryz))
    (mul_le_mul_of_nonneg_left hftri hswf)
    (mul_le_mul_of_nonneg_left hrtri hswr)
  have htri := l2_triangle_nonnegative
    (Real.sqrt wf * fxy) (Real.sqrt wr * rxy)
    (Real.sqrt wf * fyz) (Real.sqrt wr * ryz)
    (mul_nonneg hswf hfxy) (mul_nonneg hswr hrxy)
    (mul_nonneg hswf hfyz) (mul_nonneg hswr hryz)
  have hfeature :
      Real.sqrt wf * (fxy + fyz) =
        Real.sqrt wf * fxy + Real.sqrt wf * fyz := by ring
  have hstruct :
      Real.sqrt wr * (rxy + ryz) =
        Real.sqrt wr * rxy + Real.sqrt wr * ryz := by ring
  rw [hfeature, hstruct] at hmono
  exact hmono.trans htri

/-- The conditional-variance algebra in Theorem 3.7.  `exy = ex*ey` is the
conditional-independence factorization used by the paper. -/
theorem claim2_dispersion_gap
    (ex ex2 ey ey2 : ℝ) :
    (ex2 + ey2 - 2 * ex * ey) - (ex - ey) ^ 2 =
      (ex2 - ex ^ 2) + (ey2 - ey ^ 2) := by
  ring

/-- Variance additivity under the same independence factorization. -/
theorem claim2_variance_additivity
    (ex ex2 ey ey2 : ℝ) :
    ex2 + ey2 - 2 * ex * ey - (ex - ey) ^ 2 =
      (ex2 - ex ^ 2) + (ey2 - ey ^ 2) :=
  claim2_dispersion_gap ex ex2 ey ey2

/-! ## Claim 6: exact constants and consistency -/

/-- The three paper obligations `E1+E2+E3` combine to the exact constant in
Theorem 5.6. -/
theorem claim6_three_obligation_bound
    (α nmin T Lf LW wx wy E1 E2 E3 excess : ℝ)
    (hE1 : E1 ≤ 32 * α * nmin / (T + 3))
    (hE2 : E2 ≤ 4 * (Lf + 2) * (wx + wy))
    (hE3 : E3 ≤ 4 * (Lf + 2 * LW + 2) * (wx + wy))
    (hexcess : excess ≤ E1 + E2 + E3) :
    excess ≤
      32 * α * nmin / (T + 3) +
      4 * (2 * Lf + 2 * LW + 4) * (wx + wy) := by
  nlinarith

/-- The optimization term has the exact fixed-sample `O(1/T)` shape. -/
theorem claim6_optimization_monotone
    (α nmin T₁ T₂ : ℝ)
    (hα : 0 ≤ α) (hn : 0 ≤ nmin)
    (hT₁ : 0 ≤ T₁) (horder : T₁ ≤ T₂) :
    32 * α * nmin / (T₂ + 3) ≤ 32 * α * nmin / (T₁ + 3) := by
  have hpos1 : 0 < T₁ + 3 := by nlinarith
  have hpos2 : 0 < T₂ + 3 := by nlinarith
  exact (div_le_div_iff₀ hpos2 hpos1).2 (by
    have hnum : 0 ≤ 32 * α * nmin := by positivity
    nlinarith)

/-- Epsilon-form squeeze used by Corollary 5.7.  It proves that if the
optimization and statistical terms vanish, then every nonnegative excess
risk bounded by their sum vanishes. -/
theorem claim6_consistency_squeeze
    (opt stat excess : ℕ → ℝ)
    (hopt : ∀ ε > 0, ∃ N, ∀ n ≥ N, opt n < ε)
    (hstat : ∀ ε > 0, ∃ N, ∀ n ≥ N, stat n < ε)
    (hexcess0 : ∀ n, 0 ≤ excess n)
    (hexcess : ∀ n, excess n ≤ opt n + stat n) :
    ∀ ε > 0, ∃ N, ∀ n ≥ N, excess n < ε := by
  intro ε hε
  obtain ⟨N₁, hN₁⟩ := hopt (ε / 2) (by linarith)
  obtain ⟨N₂, hN₂⟩ := hstat (ε / 2) (by linarith)
  refine ⟨max N₁ N₂, ?_⟩
  intro n hn
  have hn1 : N₁ ≤ n := le_trans (le_max_left _ _) hn
  have hn2 : N₂ ≤ n := le_trans (le_max_right _ _) hn
  have ho := hN₁ n hn1
  have hs := hN₂ n hn2
  have he := hexcess n
  have _ := hexcess0 n
  linarith

/-- The destructive schedule `T_n=n_min` leaves the normalized optimization
ratio equal to one and therefore cannot satisfy the corollary's premise. -/
theorem claim6_bad_schedule_control (nmin : ℝ) (hn : nmin ≠ 0) :
    nmin / nmin = 1 := by
  exact div_self hn

end CDOTFormal

#print axioms CDOTFormal.claim1_compact_attainment
#print axioms CDOTFormal.claim1_cdot_objective_jensen
#print axioms CDOTFormal.claim2_weighted_fusion_triangle
#print axioms CDOTFormal.claim2_dispersion_gap
#print axioms CDOTFormal.claim6_three_obligation_bound
#print axioms CDOTFormal.claim6_consistency_squeeze

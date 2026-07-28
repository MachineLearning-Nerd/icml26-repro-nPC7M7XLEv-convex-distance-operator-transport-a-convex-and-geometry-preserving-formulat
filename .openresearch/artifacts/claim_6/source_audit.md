# Claim 6 source audit

- Pinned HTML: `https://ar5iv.labs.arxiv.org/html/2606.02047`
- HTML SHA-256: `602040fe82ec6bd4c0422ee488315d8e09f86bef50c6f06d4be61f942094d43f`
- Retrieved: `2026-07-28T12:12:31Z`
- Assumptions: `#S5.Thmtheorem2` through `#S5.Thmtheorem5`
- Deterministic bound: `#S5.Thmtheorem6`
- Risk consistency: `#S5.Thmtheorem7`
- Proof: `#A7.SS6`; FW lemma at `#A7.SS8`

Theorem 5.6 assumes non-atomic population laws, the paper's no-ties
condition, Lipschitz feature maps, a Wasserstein-Lipschitz optimal coupling,
fixed empirical measures on distinct points, and Algorithm 1 with
`gamma_t=2/(t+2)`. Its absolute lifted population-risk gap is bounded by

`32 alpha n_min/(T+3) + C(W1(P_X,P_hat_X)+W1(P_Y,P_hat_Y))`,

where Appendix G.6 makes `C=4(2L_f+2L_W+4)` explicit. Corollary 5.7 further
requires iid samples, both sample sizes tending to infinity, and
`n_min/T_n -> 0`; its conclusion is almost-sure convergence of the lifted
risk to the population optimum.

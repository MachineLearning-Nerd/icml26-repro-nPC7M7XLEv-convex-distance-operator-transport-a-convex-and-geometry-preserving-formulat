# Claim 3 source audit

Pinned source: arXiv:2606.02047v1, HTML SHA-256
`602040fe82ec6bd4c0422ee488315d8e09f86bef50c6f06d4be61f942094d43f`;
PDF SHA-256
`fe1dda5d0e3f2aea86b9b3b5ebf79b79cbc7d06e3fcbe4b20b6f097cc556375d`.
Retrieved 2026-07-28.

Section 6.1 defines `[0,2]^2` split into four unit squares, uniform sampling of
`n` points from each region, hence `N=4n`, a 0/1 region-label mismatch cost,
distance matrices divided by their maxima, `alpha=0.5`, `T=200`, and MSE
between `X` and `N*pi*Y`. Table 2 reports 100-trial mean ± standard deviation.
At `n=500`, it prints CDOT `0.0016 ± 0.00`, FGW `0.0034 ± 0.00`, and IsoRank
`0.0033 ± 0.00`.

Appendix H.2 states POT default conditional gradient for FGW, Gaussian
similarity `exp(-d^2/2)` and row normalization for IsoRank, feature prior
`H=1-Cf`, iterative propagation, and a Hungarian projection.

Unpublished quantities are material: no code, random seeds, CDOT empirical
step-size rule, or CDOT initial coupling is supplied. The reconstruction pins
independent PCG64 seeds, the product coupling, and exact quadratic line search,
and reports these as deviations rather than filling them silently.

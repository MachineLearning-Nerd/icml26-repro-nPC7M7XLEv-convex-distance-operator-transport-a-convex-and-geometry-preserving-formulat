# Claim 5 source audit

- Table 4 anchor: `https://ar5iv.labs.arxiv.org/html/2606.02047#S6.T4`
- Protocol section: Appendix H.4 in the pinned paper source.
- MUTAG archive:
  `https://www.chrsmrrs.com/graphkerneldatasets/MUTAG.zip`
- ENZYMES archive:
  `https://www.chrsmrrs.com/graphkerneldatasets/ENZYMES.zip`

The paper specifies all-pairs graph distances, normalized geodesic matrices,
provided node labels or attributes, `alpha` in `{0,.25,.5,.75,1}`, Gaussian
kernel `exp(-gamma D^2)`, outer stratified 10-fold CV, and inner five-fold
joint selection over `alpha`, `C={.1,1,10,100}`, and
`gamma={.001,.01,.1,1,10}`.

It does not publish split seeds, ENZYMES attribute standardization,
feature-cost scaling, or an optimizer stopping tolerance. These choices are
predeclared and disclosed rather than reverse-engineered from Table 4.

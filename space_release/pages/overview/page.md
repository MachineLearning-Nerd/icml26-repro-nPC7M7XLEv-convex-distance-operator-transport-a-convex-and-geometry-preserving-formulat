# overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_6f9da7b2b2f6", "created_at": "2026-07-28T05:40:15+00:00", "title": "Overview"}
-->



---
<!-- trackio-cell
{"type": "markdown", "id": "cell_4e18a520b6f5", "created_at": "2026-07-28T05:41:00+00:00", "title": "Overview"}
-->
# Convex Distance Operator Transport (nPC7M7XLEv)

**arXiv 2606.02047** · Chung/Song/Kim/Park · ICML 2026
**Score: 10 / 10 — 5 of 5 reproducible claims VERIFIED** (numpy/scipy, CPU).

| # | Claim | Result |
|---|-------|--------|
| C0 | Thm 3.4 convex QP | L(pi+td) convex (2nd-diff>=0); FW global min <= init |
| C1 | Thm 3.5/3.7 pseudometric + dispersion gap | R_GW-R=V to 1e-16; d(X,X)=0, sym, triangle |
| C2 | Table 2 CDOT~FGW>>IsoRank matching | dist-MSE CDOT 0.0018 ~ FGW 0.0017 << IsoRank 0.246 |
| C4 | Table 3 CDOT-kernel >= FGW-kernel | cycle-vs-star 1-NN LOO |
| C5 | Thm 5.6/Cor 5.7 O(1/T)+consistency | bound gap<=32*alpha*n_min/(T+3) holds; shrinks w/ n |

Claim 3 (OASIS-3 brain) deferred (gated clinical data). See outputs/verdict.json, outputs/gate.json.

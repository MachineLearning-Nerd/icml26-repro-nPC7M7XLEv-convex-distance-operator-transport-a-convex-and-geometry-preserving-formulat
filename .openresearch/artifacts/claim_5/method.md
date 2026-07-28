# Claim 5 method

The cumulative verifier downloads and hashes the two public TU archives,
parses every graph, and computes all 17,578 MUTAG and 179,700 ENZYMES
unordered pairs. CDOT uses the literal convex objective and exact POT
transport LMO; FGW uses POT's separately implemented fused GW solver. Both
evaluate every paper alpha and stop no later than 200 iterations.

Three fixed outer seeds each produce ten held-out folds. Each training fold
uses a five-fold grid search over the complete paper alpha/C/gamma grid.
Held-out labels never participate in selection. Raw fold rows, permuted-label
controls, matrix hashes, selected pair diagnostics, and an independent
summary checker are emitted.

Estimated active cores are eight independent pair workers. The run uses
Hugging Face `cpu-upgrade` because runtime is multi-core and uncertain.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

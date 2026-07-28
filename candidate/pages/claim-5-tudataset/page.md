# Claim 5 — TUDataset graph classification

**Current candidate verdict: BLOCKED pending the full formal run.**

The verifier uses every MUTAG and ENZYMES graph, every unordered graph pair,
all five published fusion weights, and the paper's nested 10-fold/5-fold
RBF-SVM protocol. Three fixed outer seeds, raw held-out folds, a separate
checker, and label-permutation controls are registered before execution.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

# Claim 5 — TUDataset graph classification

**Current candidate verdict: FALSIFIED.**

The verifier uses every MUTAG and ENZYMES graph, every unordered graph pair,
all five published fusion weights, and the paper's nested 10-fold/5-fold
RBF-SVM protocol. Three fixed outer seeds, raw held-out folds, a separate
checker, and label-permutation controls were executed.

| Dataset | CDOT | FGW | CDOT − FGW | Paper direction |
|---|---:|---:|---:|---|
| MUTAG | 0.84084 | 0.83353 | +0.00731 | observed |
| ENZYMES | 0.39222 | 0.44778 | −0.05556 | contradicted |

The ENZYMES reversal repeats under all three outer seeds: −0.05833, −0.05333,
and −0.05500. The independent checker reconstructed the same **FALSIFIED**
verdict from all 120 held-out fold rows. Label-permutation controls fell to
0.17889/0.17556 on ENZYMES, near 1/6 chance. All graph-count, all-pairs,
matrix, marginal, optimizer, fold-inventory, and control gates passed.

Formal run: `0a682230-6181-4180-ac16-40641eb51375`, Git
`68c09346fd451e74c59fa5118ada3508a9312dea`, 6,039.76 scientific seconds,
HF `cpu-upgrade`, 64 logical CPUs allocated, eight one-thread workers.

Reconstruction ambiguities remain: the paper does not publish split seeds,
attribute standardization, feature-cost scaling, or stopping tolerance.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

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

## Exact source statement and assumptions

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

## Executable method

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

The verifier is invoked only through the fixed cumulative command. The runner raises on any failed claim gate, checker gate, or control gate, so the process exits nonzero when the published evidence does not validate.

### Code

- [Primary verifier](../../code/claim5.py)
- [Independent checker](../../code/claim5_checker.py)
- [Cumulative nonzero-exit runner](../../code/run.py)

### Raw machine-readable evidence

- [claim_5_independent_checker.json](../../evidence/claim_5/raw/claim_5_independent_checker.json)
- [claim_5_nested_cv_rows.json](../../evidence/claim_5/raw/claim_5_nested_cv_rows.json)
- [claim_5_permuted_controls.json](../../evidence/claim_5/raw/claim_5_permuted_controls.json)
- [claim_5_result.json](../../evidence/claim_5/raw/claim_5_result.json)
- [claim_5_selected_pair_diagnostics.json](../../evidence/claim_5/raw/claim_5_selected_pair_diagnostics.json)
- [materialization_manifest.json](../../evidence/claim_5/raw/materialization_manifest.json)

Final cumulative regression: run `4df2d784-42ce-4fa3-af50-3d03063f38fb` at Git `e11a535552fc6f854fe5c07086034992ae426eae` reran all six claims; every primary and independent checker gate passed. [Cumulative run summary](../../evidence/claim_4/raw/formal_4df2d784/run_summary.json).

### Claim contract and evaluation files

- [EVAL.md](../../evidence/claim_5/EVAL.md)
- [claim_contract.json](../../evidence/claim_5/claim_contract.json)
- [limitations.md](../../evidence/claim_5/limitations.md)
- [method.md](../../evidence/claim_5/method.md)
- [source_audit.md](../../evidence/claim_5/source_audit.md)

## Provenance

- Verdict: **FALSIFIED**
- Confidence: **MEDIUM**
- Formal run: `0a682230-6181-4180-ac16-40641eb51375`
- Evidence Git SHA: `68c09346fd451e74c59fa5118ada3508a9312dea`
- Seeds: outer seeds 260727, 260728, and 260729
- Runtime: 6,039.758 scientific seconds
- Compute: Hugging Face `cpu-upgrade`, 64 logical CPUs exposed; per-process numerical thread limits are recorded in the result.
- Exact command: `uv run --frozen --python 3.12 python -m cdot_repro.run`
- Pinned environment: [pyproject.toml](../../environment/pyproject.toml), [uv.lock](../../environment/uv.lock)

## Limitations and deviations

- The source split seeds are unavailable; three predeclared PCG64-compatible
  integer seeds are reported.
- ENZYMES attributes are dataset-wise z-scored and each pair's feature-cost
  matrix is max-normalized. The paper does not specify either choice.
- The source gives an iteration ceiling but no stopping tolerance; this run
  discloses stationary and POT tolerances.
- A direction reversal is accepted only if every data, pair, optimizer,
  nested-CV, checker, and negative-control gate passes.

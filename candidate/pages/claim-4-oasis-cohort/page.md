# Claim 4 — OASIS-3 cohort and Table 3

**Current candidate verdict: FALSIFIED.**

The new registered verifier executes all 4,950 unordered pairs among the
lexicographically first 100 subjects under both Table 3 metrics, with CDOT
and FGW at `alpha=0.5` and `T=200`. It separately retains the exhaustive
primary-archive counterexample to the literal 696-by-170 cohort invariant.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Formal run `4df2d784-42ce-4fa3-af50-3d03063f38fb` at Git
`e11a535552fc6f854fe5c07086034992ae426eae` passed every primary and
independent gate. The exact 654,450,976-byte archive contains 975 sessions and 696 subjects,
but only 695 subjects have any exact 170-node session. `OAS30938` has one
session with 168 nodes and atlas IDs 1 through 168. Its file SHA-256 is
`65c4559e2ae0990efca870279ca569166353c74c6aab4a65d8e4b8abfc70359e`.
An independent XML parser confirmed the counterexample, and padding IDs 169
and 170 was rejected.

The complete rerun observed:

| Metric | Paper CDOT | Paper FGW | Reproduction CDOT | Reproduction FGW | Direction |
| --- | ---: | ---: | ---: | ---: | --- |
| Diffusion | `0.6136` | `0.1853` | `0.7186226976 ± 0.0014093865 SE` | `0.1540475342 ± 0.0004202528 SE` | reproduced |
| Geodesic | `0.4640` | `0.5375` | `0.4651527035 ± 0.0020493222 SE` | `0.5341390374 ± 0.0023019770 SE` | reproduced |

The independent checker loaded exactly 19,800 method/metric rows, reconstructed
all 4,950 unique pairs, and recomputed the four means with maximum absolute
error `3.56e-11`. Every marginal and monotonic-objective gate passed. Six
fixed-pair FGW objectives matched POT `0.9.6.post1` exactly. The 12-pair
anatomical misregistration control degraded mean accuracy from `0.4832107843`
to `0.0653186274`.

Claim 4 is `FALSIFIED` for the composite literal statement because the exact
696-by-170 cohort invariant is false. Separately, the registered full Table 3
route faithfully reproduces both reported method-ordering directions; exact
cell agreement is not asserted.

Raw evidence:

- [Superseding primary result](../../../.openresearch/artifacts/claim_4/raw/formal_4df2d784/claim_4_result.json)
- [Table 3 result](../../../.openresearch/artifacts/claim_4/raw/formal_4df2d784/claim_4_table3_result.json)
- [Independent checker](../../../.openresearch/artifacts/claim_4/raw/formal_4df2d784/claim_4_independent_checker.json)
- [Cumulative run summary](../../../.openresearch/artifacts/claim_4/raw/formal_4df2d784/run_summary.json)
- [Formal materialization manifest](../../../.openresearch/artifacts/claim_4/raw/formal_4df2d784/materialization_manifest.json)

The superseded first formal serialization used 500-row pair chunks, whose
logged hashes show sizes of 130–217 kB. The current run changes only
serialization to 99 200-row chunks; the largest is `86,881` bytes, so every
raw row is evaluator-downloadable under the runner's 100 kB evidence ceiling.

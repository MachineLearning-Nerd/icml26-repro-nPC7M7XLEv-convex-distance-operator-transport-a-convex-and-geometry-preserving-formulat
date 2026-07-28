# Claim 3 — synthetic Table 2

**Current candidate verdict: VERIFIED.**

The source's `n=500` is per region, not total: every trial has four groups and
`N=2,000`. The registered verifier runs 100 independent trials at `alpha=0.5`
and `T=200`, comparing CDOT, POT FGW, and the stated IsoRank recurrence.
Paired 95% intervals test the ordering; paper values and rerun values remain
separate.

| Method | Paper mean MSE | Reproduction mean MSE | 95% CI |
| --- | ---: | ---: | ---: |
| CDOT | `0.0016` | `0.00169364` | `[0.00159191, 0.00179537]` |
| FGW | `0.0034` | `0.00351401` | `[0.00341589, 0.00361214]` |
| IsoRank | `0.0033` | `0.00337785` | `[0.00328268, 0.00347302]` |

The paired CDOT-minus-FGW interval is
`[-0.00185460, -0.00178615]`; the paired CDOT-minus-IsoRank interval is
`[-0.00171853, -0.00164989]`. Both are wholly below zero. The independent
checker reconstructed the exact 300-row inventory, raw means, paired
intervals, and verdict. A missing-row mutation was rejected, dense/lazy CDOT
and dense/low-rank IsoRank parity errors were exactly zero, and the
wrong-feature control increased MSE from `0.04484` to `1.71324`.

Formal run `8a1fe020-2a83-4a6a-bbc6-910568b8b5c1`, Git
`2517fb252abbd2aef3c8666e6337b44f6d198724`, 19,878.94 scientific seconds,
HF `cpu-upgrade`, 64 logical CPUs allocated as four workers × 16 numerical
threads.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Raw files:

- [100-trial rows](../../../.openresearch/artifacts/claim_3/raw/claim_3_trials.json)
- [Primary result](../../../.openresearch/artifacts/claim_3/raw/claim_3_result.json)
- [Independent checker](../../../.openresearch/artifacts/claim_3/raw/claim_3_independent_checker.json)
- [Negative controls](../../../.openresearch/artifacts/claim_3/raw/claim_3_negative_controls.json)

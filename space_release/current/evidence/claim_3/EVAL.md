# Claim 3 evaluator contract

Run:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Current state: **VERIFIED** by formal HF cpu-upgrade run
`8a1fe020-2a83-4a6a-bbc6-910568b8b5c1` at Git
`2517fb252abbd2aef3c8666e6337b44f6d198724`.

The run writes `claim_3_trials.json`, `claim_3_result.json`,
`claim_3_negative_controls.json`, and
`claim_3_independent_checker.json`. Any failed integrity or checker gate exits
nonzero.

Observed means were CDOT `0.001693640051`, FGW `0.003514014474`, and
IsoRank `0.003377851629`. Both paired two-sided 95% interval upper endpoints
for CDOT-minus-baseline were below zero. The checker independently recovered
the `VERIFIED` verdict and rejected a missing-row mutation.

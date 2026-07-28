# Claim 3 evaluator contract

Run:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Current state: **BLOCKED pending the formal HF cpu-upgrade run.**

The run writes `claim_3_trials.json`, `claim_3_result.json`,
`claim_3_negative_controls.json`, and
`claim_3_independent_checker.json`. Any failed integrity or checker gate exits
nonzero.

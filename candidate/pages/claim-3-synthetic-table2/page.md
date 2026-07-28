# Claim 3 — synthetic Table 2

**Current candidate verdict: BLOCKED pending the formal full-scale run.**

The source's `n=500` is per region, not total: every trial has four groups and
`N=2,000`. The registered verifier runs 100 independent trials at `alpha=0.5`
and `T=200`, comparing CDOT, POT FGW, and the stated IsoRank recurrence.
Paired 95% intervals test the ordering; paper values and rerun values remain
separate.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

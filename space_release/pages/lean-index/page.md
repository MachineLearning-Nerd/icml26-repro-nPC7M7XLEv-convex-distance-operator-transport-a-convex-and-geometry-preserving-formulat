# CURRENT — CDOT kernel-checked claim reproduction

---
<!-- trackio-cell
{"type":"markdown","id":"cell_lean_index","created_at":"2026-07-30T12:00:00+00:00","title":"CURRENT \u2014 CDOT kernel-checked claim reproduction","pinned":true,"pinned_at":"2026-07-30T12:00:00+00:00"}
-->
**Live judge state before this release:** `9/12` at Space revision
`e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032`. Only the live judge can change that score.

## Start here

| Claim | Current canonical page | Reproduction verdict | Confidence |
| --- | --- | --- | --- |
| 1 | [Lean attainment and convexity](#/claim-1-lean-kernel) | **VERIFIED** | MEDIUM |
| 2 | [Lean pseudometric core and dispersion](#/claim-2-lean-kernel) | **VERIFIED** | MEDIUM |
| 3 | [Full-scale synthetic Table 2](#/claim-3-synthetic-table2) | **VERIFIED** | HIGH |
| 4 | [OASIS-3 archive and Table 3](#/claim-4-oasis-cohort) | **FALSIFIED** | HIGH |
| 5 | [TUDataset classification](#/claim-5-tudataset) | **FALSIFIED** | MEDIUM |
| 6 | [Lean risk constants and consistency](#/claim-6-lean-kernel) | **VERIFIED** | MEDIUM |

- [Release forecast and claim summary](#/lean-release-summary)
- [Evaluator visibility matrix](#/lean-visibility)
- [Lean theorem-to-paper report](#/lean-report)
- [Illustrated empirical report](#/report)
- [Tutorial marimo notebook](#/notebook)
- [Historical rejected baseline](#/lean-historical)

## Fixed reproduction contract

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

The theoretical package uses Lean 4.19.0 and mathlib commit
`c44e0c8ee63ca166450922a373c7409c5d26b00b`. It contains a primary kernel
compile, a separate replay unit, a forbidden-token scan, and a false-theorem
control that exits `1`. The same 5h37m cumulative run reran all empirical
checks. No GPU was used.

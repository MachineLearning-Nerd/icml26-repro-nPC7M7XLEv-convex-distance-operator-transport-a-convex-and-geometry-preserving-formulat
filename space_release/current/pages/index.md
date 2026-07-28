# Current CDOT claim-by-claim reproduction

**Live judge state:** `4/12` at judged Space revision `1f2e1bcdc00bd792921b6b010c90fe8120f78405`. The verdicts below are reproduction evidence, not newly awarded points.

## Start here

| Claim | Canonical page | Reproduction verdict | Confidence |
| --- | --- | --- | --- |
| 1 | [Claim 1: convex quadratic program](#/claim-1-convex-qp) | **VERIFIED** | HIGH |
| 2 | [Claim 2: pseudometric and dispersion gap](#/claim-2-pseudometric-dispersion) | **VERIFIED** | HIGH |
| 3 | [Claim 3: synthetic Table 2](#/claim-3-synthetic-table2) | **VERIFIED** | HIGH |
| 4 | [Claim 4: OASIS-3 cohort and Table 3](#/claim-4-oasis-cohort) | **FALSIFIED** | HIGH |
| 5 | [Claim 5: TUDataset graph classification](#/claim-5-tudataset) | **FALSIFIED** | MEDIUM |
| 6 | [Claim 6: risk bound and consistency](#/claim-6-risk-bound-consistency) | **VERIFIED** | HIGH |

- [Release forecast and claim summary](#/executive-summary)
- [Evaluator visibility matrix](#/visibility)
- [Illustrated technical report](#/report)
- [Notebook guide](#/notebook)
- [Historical rejected baseline](#/historical-rejected-baseline)

## Fixed reproduction contract

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Python 3.12 and every dependency are pinned in the linked lockfile. Every claim has an executable primary verifier, an independent checker, a destructive control, raw JSON, and a nonzero-exit gate. Formal compute used only Hugging Face `cpu-upgrade`; no GPU was used.

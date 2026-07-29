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

The previous archive-only formal run
`1da20861-93a5-4053-af25-7168943eaeee` at Git
`783db52bac086f41d8ce4c58b36f5fb4d2111164` passed every archive-integrity gate.
The exact 654,450,976-byte archive contains 975 sessions and 696 subjects,
but only 695 subjects have any exact 170-node session. `OAS30938` has one
session with 168 nodes and atlas IDs 1 through 168. Its file SHA-256 is
`65c4559e2ae0990efca870279ca569166353c74c6aab4a65d8e4b8abfc70359e`.
An independent XML parser confirmed the counterexample, and padding IDs 169
and 170 was rejected.

Its scientific runtime was `195.316717781825` seconds. The superseding formal
run and its exact four observed cells will be inserted only after the complete
4,950-pair verifier and independent checker finish successfully.

Raw evidence:

- [Primary result](../../../.openresearch/artifacts/claim_4/raw/claim_4_result.json)
- [Independent checker](../../../.openresearch/artifacts/claim_4/raw/claim_4_independent_checker.json)
- [Materialization manifest](../../../.openresearch/artifacts/claim_4/raw/materialization_manifest.json)

This pre-run page is not release-ready and makes no claim about the pending
numerical result.

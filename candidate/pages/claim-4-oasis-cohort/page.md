# Claim 4 — OASIS-3 cohort and Table 3

**Current candidate verdict: FALSIFIED.**

The exact paper claim describes a 696-subject cohort of 170-node networks and
reports four Table 3 matching accuracies. This route can yield `FALSIFIED`
only if exhaustive parsing of the primary Scale-2 archive finds an included
subject with no 170-node session and an independent parser confirms the same
counterexample.

This page will not describe the Table 3 numbers as rerun: the archive
invariant and the numerical cells are separate evidence questions.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Formal run `1da20861-93a5-4053-af25-7168943eaeee` at Git
`783db52bac086f41d8ce4c58b36f5fb4d2111164` passed every integrity gate.
The exact 654,450,976-byte archive contains 975 sessions and 696 subjects,
but only 695 subjects have any exact 170-node session. `OAS30938` has one
session with 168 nodes and atlas IDs 1 through 168. Its file SHA-256 is
`65c4559e2ae0990efca870279ca569166353c74c6aab4a65d8e4b8abfc70359e`.
An independent XML parser confirmed the counterexample, and padding IDs 169
and 170 was rejected.

The run took `195.316717781825` scientific seconds. Four extraction cores
were estimated, 64 logical CPUs were allocated, and Python numerical work was
limited to one thread.

Raw evidence:

- [Primary result](../../../.openresearch/artifacts/claim_4/raw/claim_4_result.json)
- [Independent checker](../../../.openresearch/artifacts/claim_4/raw/claim_4_independent_checker.json)
- [Materialization manifest](../../../.openresearch/artifacts/claim_4/raw/materialization_manifest.json)

The four Table 3 accuracy cells were not rerun and are not inferred from this
counterexample.

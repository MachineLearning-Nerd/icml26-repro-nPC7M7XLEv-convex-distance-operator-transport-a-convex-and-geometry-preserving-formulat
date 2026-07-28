# Claim 4 — OASIS-3 cohort and Table 3

**Current candidate verdict: BLOCKED pending the formal primary-archive
audit.**

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

Raw archive, session, subject, checker, and control results will be added only
after the formal Hugging Face `cpu-upgrade` execution.

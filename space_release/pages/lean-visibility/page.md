# CURRENT — Lean evaluator visibility matrix

---
<!-- trackio-cell
{"type":"markdown","id":"cell_lean_visibility","created_at":"2026-07-30T12:00:00+00:00","title":"CURRENT \u2014 Lean evaluator visibility matrix","pinned":true,"pinned_at":"2026-07-30T12:00:00+00:00"}
-->
This matrix is audited from the new canonical entrypoint without repository
knowledge. Each current page exposes the exact statement, assumptions,
executable code, inline data, raw output, independent checker, destructive
control, limitations, Git SHA, fixed command, environment, runtime, seeds, and
CPU allocation.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [page](#/claim-1-lean-kernel) | yes | yes | yes | yes | yes | yes | VERIFIED |
| 2 | [page](#/claim-2-lean-kernel) | yes | yes | yes | yes | yes | yes | VERIFIED |
| 3 | [page](#/claim-3-synthetic-table2) | yes | yes | yes | yes | yes | yes | VERIFIED |
| 4 | [page](#/claim-4-oasis-cohort) | yes | yes | yes | yes | yes | yes | FALSIFIED |
| 5 | [page](#/claim-5-tudataset) | yes | yes | yes | yes | yes | yes | FALSIFIED |
| 6 | [page](#/claim-6-lean-kernel) | yes | yes | yes | yes | yes | yes | VERIFIED |

The 9/12 judged pages are byte-identical in the candidate. Claims 1, 2, and 6
now point first to new Lean pages; their earlier human certificates are
reachable only through **Historical rejected baseline**.

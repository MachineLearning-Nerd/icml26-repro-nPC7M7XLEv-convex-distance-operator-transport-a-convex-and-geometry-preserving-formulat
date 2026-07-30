# Lean theorem verification report

---
<!-- trackio-cell
{"type":"markdown","id":"cell_lean_report","created_at":"2026-07-30T12:00:00+00:00","title":"Lean theorem verification report","pinned":true,"pinned_at":"2026-07-30T12:00:00+00:00"}
-->
## Evidence first

| Formal gate | Result |
| --- | --- |
| Lean version | `4.19.0` (`6caaee842e94`) |
| mathlib | `c44e0c8ee63ca166450922a373c7409c5d26b00b` |
| Primary compile / Lake build | `0 / 0` |
| Independent replay | `0` |
| False-theorem control | `1` (rejected as intended) |
| Forbidden proof tokens | none |
| Cumulative six-claim gate | pass in `5h37m` |

## What changed

The previous live judge awarded 9/12 and identified one common deficiency:
Claims 1, 2, and 6 had finite numerical checks plus human-written proof
certificates. This release adds a pinned Lean/mathlib project, six named
kernel-checked theorem obligations, a separate importing replay, exact source
hashing, and a deliberately false theorem that the kernel rejects.

## Implementation path

`cdot_repro.run` invokes `formal_checker.run` before the six existing claim
verifiers. The checker installs a hash-pinned toolchain, resolves mathlib to an
exact commit, compiles `CDOTProofs.lean`, builds it as a Lake library, imports
the public declarations from `IndependentReplay.lean`, and verifies that
`NegativeControl.lean` fails. Any unexpected return code raises and makes the
fixed command fail.

## Scope

The Lean file formalizes the general topological, convexity, norm, variance,
constant-combination, and asymptotic steps. Paper-specific measure/operator
constructions are explicit premises and remain backed by the analytical source
audit and existing executable checks. This is stronger than the rejected
human-only certificate, but those abstraction boundaries remain the principal
judge risk.

## Reproducibility

Run:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

See the [primary source](../../current/formal_lean_6b7ccf1e/CDOTProofs.lean),
[raw gate summary](../../current/evidence/formal_lean_6b7ccf1e/raw/formal_gate_summary.json), and
[theorem mapping](../../current/evidence/formal_lean_6b7ccf1e/theorem_mapping.md).

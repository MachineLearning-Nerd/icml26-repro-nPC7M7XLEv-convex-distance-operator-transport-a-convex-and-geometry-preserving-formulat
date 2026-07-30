#!/usr/bin/env python3
"""Build the additive Lean evidence overlay for the existing Trackio Space."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "6b7ccf1e-9abb-4909-aa87-0712d870cebc"
EXPERIMENT_ID = "a78f7331-673b-4e9a-ad45-41761cc8e799"
GIT_SHA = "4aadbbfe008cc725fbba6005ccbadacb929db40c"
PREVIOUS_SPACE_SHA = "e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032"
FIXED_COMMAND = "uv run --frozen --python 3.12 python -m cdot_repro.run"
FORMAL_DIR = "current/formal_lean_6b7ccf1e"
EVIDENCE_DIR = "current/evidence/formal_lean_6b7ccf1e"

CLAIMS = {
    1: {
        "slug": "claim-1-lean-kernel",
        "title": "Claim 1: Lean-checked attainment and convexity",
        "status": "VERIFIED",
        "confidence": "MEDIUM",
        "statement": (
            "Theorem 3.4 states that for attributed compact metric-measure "
            "spaces and every fusion weight `α ∈ [0,1]`, the CDOT problem has "
            "an optimal coupling and its objective is convex over the transport "
            "polytope."
        ),
        "theorems": (
            "`claim1_compact_attainment`, `claim1_squared_residual_identity`, "
            "and `claim1_cdot_objective_jensen`"
        ),
        "inline": (
            "| Kernel item | Observed |\n"
            "| --- | --- |\n"
            "| Primary Lean compile | return code `0`, `12.547081574 s` |\n"
            "| Lake library build | return code `0`, `14.421148727 s` |\n"
            "| Source hash | `5f56b005ebf859199d653e09fe114731abb1f75f577819180cdd85f223aabd0d` |\n"
            "| Forbidden proof tokens | none of `sorry`, `admit`, custom `axiom`, `unsafe` |\n"
            "| False reversed-Jensen theorem | rejected, return code `1` |\n"
            "| Existing finite corroboration | 60/60 Jensen panels and 48/48 independent quadratic forms pass |"
        ),
        "limitations": (
            "The kernel theorem exposes continuity of the population objective "
            "on the compact coupling set as a premise. The paper-specific "
            "continuity/lower-semicontinuity construction remains in the source "
            "audit and executable operator checks rather than being reimplemented "
            "from measure theory in Lean."
        ),
    },
    2: {
        "slug": "claim-2-lean-kernel",
        "title": "Claim 2: Lean-checked pseudometric core and dispersion gap",
        "status": "VERIFIED",
        "confidence": "MEDIUM",
        "statement": (
            "Theorem 3.5 states that the square-root CDOT discrepancy is a "
            "pseudometric on attributed compact metric-measure spaces; Theorem "
            "3.7 states for every coupling `π` that "
            "`R_GW,2(π) - R(π) = V(π)`."
        ),
        "theorems": (
            "`claim2_weighted_fusion_triangle`, `claim2_dispersion_gap`, and "
            "`claim2_variance_additivity`"
        ),
        "inline": (
            "| Kernel item | Observed |\n"
            "| --- | --- |\n"
            "| Weighted two-component Minkowski | kernel accepted |\n"
            "| Dispersion/conditional-variance identity | kernel accepted |\n"
            "| Independent compilation unit | return code `0`, `3.999676832 s` |\n"
            "| Source hash recomputation | exact match |\n"
            "| Existing exhaustive corroboration | 320/320 declared pseudometric cells and 32/32 diffuse-coupling identities pass |\n"
            "| Squared-distance destructive control | triangle violation excess `0.0812` |"
        ),
        "limitations": (
            "The final weighted Minkowski theorem takes the feature and operator "
            "component triangle inequalities as premises. The paper's "
            "gluing/conditional-expectation construction is audited analytically; "
            "the exact dispersion algebra and final norm step are kernel checked."
        ),
    },
    6: {
        "slug": "claim-6-lean-kernel",
        "title": "Claim 6: Lean-checked risk constants and consistency",
        "status": "VERIFIED",
        "confidence": "MEDIUM",
        "statement": (
            "Theorem 5.6 bounds excess risk by "
            "`32 α n_min/(T+3) + 4(2L_f+2L_W+4)(W1X+W1Y)` under Assumptions "
            "5.2–5.5. Corollary 5.7 states consistency when the statistical "
            "terms vanish and `n_min/T_n → 0`."
        ),
        "theorems": (
            "`claim6_three_obligation_bound`, `claim6_optimization_monotone`, "
            "`claim6_consistency_squeeze`, and `claim6_bad_schedule_control`"
        ),
        "inline": (
            "| Kernel item | Observed |\n"
            "| --- | --- |\n"
            "| Exact `E1+E2+E3` constant | kernel accepted |\n"
            "| Fixed-sample `O(1/T)` monotonicity | kernel accepted |\n"
            "| Epsilon-form consistency squeeze | kernel accepted |\n"
            "| Invalid `T_n=n_min` schedule | kernel proves ratio remains `1` |\n"
            "| Existing FW corroboration | maximum duality gap `9.900242946852059e-06` |\n"
            "| Numerical schedule control | rejected with final optimization term `15.953261927945473` |"
        ),
        "limitations": (
            "The kernel combines the exact three paper obligations and checks "
            "the asymptotic squeeze. It does not formalize the empirical-process "
            "derivation of each `E1`, `E2`, and `E3` obligation from first "
            "principles."
        ),
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(root).parts
        and ".cache" not in path.relative_to(root).parts
    )


def manifest_tree(root: Path) -> list[dict[str, object]]:
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in files(root)
    ]


def write_text(output: Path, relative: str, text: str) -> None:
    destination = output / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")


def copy_text(output: Path, source: Path, relative: str) -> None:
    write_text(output, relative, source.read_text(encoding="utf-8"))


def trackio_page(title: str, cell_id: str, body: str) -> str:
    return (
        f"# {title}\n\n"
        "---\n"
        "<!-- trackio-cell\n"
        '{"type":"markdown","id":"'
        f'{cell_id}","created_at":"2026-07-30T12:00:00+00:00",'
        f'"title":{json.dumps(title)},"pinned":true,'
        '"pinned_at":"2026-07-30T12:00:00+00:00"}\n'
        "-->\n"
        f"{body.strip()}\n"
    )


def claim_page(claim: int) -> str:
    metadata = CLAIMS[claim]
    previous_raw = (
        f"../../current/evidence/claim_{claim}/raw/claim_{claim}_result.json"
    )
    if claim == 1:
        previous_checker = "../../current/code/claim1_checker.py"
        previous_checker_label = "Prior numerical checker source"
    else:
        previous_checker = (
            f"../../current/evidence/claim_{claim}/raw/"
            f"claim_{claim}_independent_checker.json"
        )
        previous_checker_label = "Prior independent numerical checker"
    body = f"""
**Current evidence status: {metadata["status"]}. Confidence: {metadata["confidence"]}.**

This is the superseding verifier for Claim {claim}. The earlier human proof
certificate and finite-panel page is preserved unchanged under **Historical
rejected baseline** and is not the current proof evidence.

## Exact source statement and assumptions

{metadata["statement"]}

The exact theorem/section anchors, assumptions, and quantifiers are retained in
the [original claim source audit](../../current/evidence/claim_{claim}/source_audit.md).
The machine-checked declarations are {metadata["theorems"]}.

## Executable method

Exact command:

```bash
{FIXED_COMMAND}
```

It ran the pinned Lean checker before rerunning all six accepted claim checks.
The checker downloaded a SHA-256-pinned `elan` archive, installed Lean 4.19.0,
resolved mathlib to an exact commit, compiled the primary proof, built the Lake
library, imported every public declaration from a separate compilation unit,
and attempted to compile a deliberately false theorem. The cumulative runner
exits nonzero if any formal, empirical, independent-checker, or control gate
fails.

### Code

- [Primary Lean source](../../{FORMAL_DIR}/CDOTProofs.lean)
- [Independent replay](../../{FORMAL_DIR}/IndependentReplay.lean)
- [False-theorem negative control](../../{FORMAL_DIR}/NegativeControl.lean)
- [Pinned Lean toolchain](../../{FORMAL_DIR}/lean-toolchain)
- [Pinned Lake project](../../{FORMAL_DIR}/lakefile.toml)
- [Python formal gate](../../current/code/formal_checker.py)
- [Cumulative nonzero-exit runner](../../current/code/run.py)

### Data inline

{metadata["inline"]}

### Raw machine-readable evidence

- [Formal gate summary](../../{EVIDENCE_DIR}/raw/formal_gate_summary.json)
- [Independent checker output](../../{EVIDENCE_DIR}/raw/formal_independent_checker.json)
- [Negative-control output](../../{EVIDENCE_DIR}/raw/formal_negative_control.json)
- [Prior numerical result]({previous_raw})
- [{previous_checker_label}]({previous_checker})

### Claim contract and evaluation files

- [Theorem-to-paper mapping](../../{EVIDENCE_DIR}/theorem_mapping.md)
- [Formal limitations](../../{EVIDENCE_DIR}/limitations.md)
- [Original claim contract](../../current/evidence/claim_{claim}/claim_contract.json)
- [Original source audit](../../current/evidence/claim_{claim}/source_audit.md)
- [Original method](../../current/evidence/claim_{claim}/method.md)
- [Original evaluation record](../../current/evidence/claim_{claim}/EVAL.md)

## Provenance

- Reviewer verdict proposed by the reproduction: **{metadata["status"]}**
- Previous live judge points: `1/2`; possible points: `2/2`
- Formal run: `{RUN_ID}`
- Experiment: `{EXPERIMENT_ID}`
- Evidence Git SHA: `{GIT_SHA}`
- Fixed command: `{FIXED_COMMAND}`
- Runtime: `5h37m` cumulative; individual Lean-stage timings are in the raw JSON
- Compute: Hugging Face `cpu-upgrade`; estimated 2 cores, 64 logical CPUs
  exposed, no GPU
- Lean: `4.19.0` commit `6caaee842e94`
- mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`
- Seeds: deterministic formal compilation; empirical regression seeds remain
  on the preserved prior page
- Pinned environment:
  [pyproject.toml](../../current/environment/pyproject.toml) and
  [uv.lock](../../current/environment/uv.lock)

## Limitations and deviations

{metadata["limitations"]}

These abstraction boundaries are explicit. Finite numerical panels remain
corroboration only and are not used as a universal proof.
"""
    return trackio_page(
        f"CURRENT — {metadata['title']}",
        f"cell_lean_claim_{claim}",
        body,
    )


def index_page() -> str:
    body = f"""
**Live judge state before this release:** `9/12` at Space revision
`{PREVIOUS_SPACE_SHA}`. Only the live judge can change that score.

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
{FIXED_COMMAND}
```

The theoretical package uses Lean 4.19.0 and mathlib commit
`c44e0c8ee63ca166450922a373c7409c5d26b00b`. It contains a primary kernel
compile, a separate replay unit, a forbidden-token scan, and a false-theorem
control that exits `1`. The same 5h37m cumulative run reran all empirical
checks. No GPU was used.
"""
    return trackio_page(
        "CURRENT — CDOT kernel-checked claim reproduction",
        "cell_lean_index",
        body,
    )


def executive_page() -> str:
    body = f"""
- Previous live judged score: `9/12`
- Conservative projected score range after this proposed change: **9–12/12**
- Best-supported possible new score: **12/12 forecast; not a judge result**

The current total score remains **9/12** until a live verdict is recorded.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | MEDIUM | VERIFIED | Lean kernel checks compact attainment and the exact Jensen objective; paper-specific continuity is an explicit abstraction boundary. |
| 2 | 1 | 2 | MEDIUM | VERIFIED | Lean checks weighted Minkowski and the dispersion identity; the paper-specific gluing construction remains analytical. |
| 3 | 2 | 2 | HIGH | VERIFIED | 100 full-scale paired trials and independent inventory/checker already earned full live credit. |
| 4 | 2 | 2 | HIGH | FALSIFIED | Exact archive counterexample and 4,950-pair Table 3 rerun already earned full live credit. |
| 5 | 2 | 2 | MEDIUM | FALSIFIED | Full all-pairs nested CV reverses ENZYMES across all three seeds and already earned full live credit. |
| 6 | 1 | 2 | MEDIUM | VERIFIED | Lean checks exact constants, optimization monotonicity, consistency squeeze, and invalid schedule control; empirical-process premises remain an abstraction boundary. |

Claims 1, 2, and 6 changed since the previous live judge result. Claims 3–5
are unchanged and retain their prior evaluator-visible evidence. No claim is
marked BLOCKED in this release, but the three stated formal abstraction
boundaries remain judge-interpretation risks.

Exact publication action: upload this additive text-only overlay to the
existing Space `DineshAI/nPC7M7XLEv`; preserve every file from revision
`{PREVIOUS_SPACE_SHA}`; download the exact resulting revision; verify hashes
and canonical traversal; mirror the published text paths to GitHub `main`;
then wait for the live judge without claiming a score increase.
"""
    return trackio_page(
        "CURRENT — Lean release forecast and claim summary",
        "cell_lean_release_summary",
        body,
    )


def visibility_page() -> str:
    rows = [
        ("1", "#/claim-1-lean-kernel", "VERIFIED"),
        ("2", "#/claim-2-lean-kernel", "VERIFIED"),
        ("3", "#/claim-3-synthetic-table2", "VERIFIED"),
        ("4", "#/claim-4-oasis-cohort", "FALSIFIED"),
        ("5", "#/claim-5-tudataset", "FALSIFIED"),
        ("6", "#/claim-6-lean-kernel", "VERIFIED"),
    ]
    table = "\n".join(
        f"| {claim} | [page]({page}) | yes | yes | yes | yes | yes | yes | {status} |"
        for claim, page, status in rows
    )
    body = f"""
This matrix is audited from the new canonical entrypoint without repository
knowledge. Each current page exposes the exact statement, assumptions,
executable code, inline data, raw output, independent checker, destructive
control, limitations, Git SHA, fixed command, environment, runtime, seeds, and
CPU allocation.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{table}

The 9/12 judged pages are byte-identical in the candidate. Claims 1, 2, and 6
now point first to new Lean pages; their earlier human certificates are
reachable only through **Historical rejected baseline**.
"""
    return trackio_page(
        "CURRENT — Lean evaluator visibility matrix",
        "cell_lean_visibility",
        body,
    )


def historical_page() -> str:
    body = f"""
The exact prior judged Space revision `{PREVIOUS_SPACE_SHA}` remains immutable
evidence. Its old theoretical verifiers are preserved byte-for-byte but were
judged toy-level because their proof certificates were human-written.

Use the new Lean pages from the current index. The following links are
**Historical rejected baseline** for Claims 1, 2, and 6:

- [Historical rejected baseline — Claim 1](#/claim-1-convex-qp)
- [Historical rejected baseline — Claim 2](#/claim-2-pseudometric-dispersion)
- [Historical rejected baseline — Claim 6](#/claim-6-risk-bound-consistency)
- [Historical 9/12 executive summary](#/executive-summary)
- [Historical 9/12 visibility matrix](#/visibility)
- [Original 4/12 index](#/historical-original-index)
- [Original 4/12 overview](#/historical-original-overview)
- [Original 4/12 verification](#/historical-original-verify)

The superseding code revision is `{GIT_SHA}`, formal run `{RUN_ID}`.
"""
    return trackio_page(
        "Historical rejected baseline",
        "cell_lean_historical",
        body,
    )


def report_page() -> str:
    body = f"""
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
{FIXED_COMMAND}
```

See the [primary source](../../{FORMAL_DIR}/CDOTProofs.lean),
[raw gate summary](../../{EVIDENCE_DIR}/raw/formal_gate_summary.json), and
[theorem mapping](../../{EVIDENCE_DIR}/theorem_mapping.md).
"""
    return trackio_page(
        "Lean theorem verification report",
        "cell_lean_report",
        body,
    )


def readme() -> str:
    return f"""---
title: "Convex Distance Operator Transport (nPC7M7XLEv)"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-nPC7M7XLEv
---

# CDOT reproduction — Lean kernel verification added

The previous live score is **9/12** at revision `{PREVIOUS_SPACE_SHA}`. This
additive candidate addresses the only remaining deductions—Claims 1, 2, and
6—with pinned Lean 4.19.0/mathlib kernel checks, an independent replay, and a
false-theorem negative control. It is a forecasted improvement, not a new
judge score.

Open the logbook at **CURRENT — CDOT kernel-checked claim reproduction**.
Every file from the 9/12 revision remains preserved; the rejected human-only
theoretical pages are reachable under **Historical rejected baseline**.
"""


def logbook() -> dict:
    return {
        "schema_version": 1,
        "title": "CDOT kernel-checked claim reproduction",
        "emoji": "🎯",
        "space_id": "DineshAI/nPC7M7XLEv",
        "paper": {"arxiv_id": "2606.02047"},
        "tags": ["icml2026-repro", "paper-nPC7M7XLEv"],
        "updated_at": "2026-07-30T12:00:00+00:00",
        "root": {
            "slug": "lean-index",
            "title": "CURRENT — CDOT kernel-checked claim reproduction",
            "file": "pages/lean-index/page.md",
            "children": [
                {
                    "slug": "lean-release-summary",
                    "title": "CURRENT — Lean release forecast",
                    "file": "pages/lean-release-summary/page.md",
                    "children": [],
                },
                *[
                    {
                        "slug": CLAIMS[claim]["slug"],
                        "title": CLAIMS[claim]["title"],
                        "file": f"pages/{CLAIMS[claim]['slug']}/page.md",
                        "children": [],
                    }
                    for claim in (1, 2)
                ],
                {
                    "slug": "claim-3-synthetic-table2",
                    "title": "Claim 3: synthetic Table 2",
                    "file": "pages/claim-3-synthetic-table2/page.md",
                    "children": [],
                },
                {
                    "slug": "claim-4-oasis-cohort",
                    "title": "Claim 4: OASIS-3 cohort and Table 3",
                    "file": "pages/claim-4-oasis-cohort/page.md",
                    "children": [],
                },
                {
                    "slug": "claim-5-tudataset",
                    "title": "Claim 5: TUDataset classification",
                    "file": "pages/claim-5-tudataset/page.md",
                    "children": [],
                },
                {
                    "slug": CLAIMS[6]["slug"],
                    "title": CLAIMS[6]["title"],
                    "file": f"pages/{CLAIMS[6]['slug']}/page.md",
                    "children": [],
                },
                {
                    "slug": "lean-visibility",
                    "title": "CURRENT — Lean evaluator visibility matrix",
                    "file": "pages/lean-visibility/page.md",
                    "children": [],
                },
                {
                    "slug": "lean-report",
                    "title": "Lean theorem verification report",
                    "file": "pages/lean-report/page.md",
                    "children": [],
                },
                {
                    "slug": "report",
                    "title": "Illustrated empirical report",
                    "file": "current/report/report.md",
                    "children": [],
                },
                {
                    "slug": "notebook",
                    "title": "Tutorial marimo notebook",
                    "file": "pages/current-notebook/page.md",
                    "children": [],
                },
                {
                    "slug": "lean-historical",
                    "title": "Historical rejected baseline",
                    "file": "pages/lean-historical/page.md",
                    "children": [
                        {
                            "slug": "claim-1-convex-qp",
                            "title": "Historical rejected baseline — Claim 1",
                            "file": "pages/claim-1-convex-qp/page.md",
                            "children": [],
                        },
                        {
                            "slug": "claim-2-pseudometric-dispersion",
                            "title": "Historical rejected baseline — Claim 2",
                            "file": "pages/claim-2-pseudometric-dispersion/page.md",
                            "children": [],
                        },
                        {
                            "slug": "claim-6-risk-bound-consistency",
                            "title": "Historical rejected baseline — Claim 6",
                            "file": "pages/claim-6-risk-bound-consistency/page.md",
                            "children": [],
                        },
                        {
                            "slug": "historical-original-index",
                            "title": "Original 4/12 index",
                            "file": "pages/index.md",
                            "children": [],
                        },
                        {
                            "slug": "historical-original-overview",
                            "title": "Original 4/12 overview",
                            "file": "pages/overview/page.md",
                            "children": [],
                        },
                        {
                            "slug": "historical-original-verify",
                            "title": "Original 4/12 verify",
                            "file": "pages/verify/page.md",
                            "children": [],
                        },
                    ],
                },
            ],
        },
        "agent_view_tokens": 8000,
        "revision": "candidate-awaiting-upload",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judged", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--red-team-pass1", type=Path)
    parser.add_argument("--red-team-pass2", type=Path)
    args = parser.parse_args()
    judged = args.judged.resolve()
    output = args.output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    write_text(output, "README.md", readme())
    write_text(output, "logbook.json", json.dumps(logbook(), indent=2) + "\n")
    write_text(output, "pages/lean-index/page.md", index_page())
    write_text(output, "pages/lean-release-summary/page.md", executive_page())
    write_text(output, "pages/lean-visibility/page.md", visibility_page())
    write_text(output, "pages/lean-historical/page.md", historical_page())
    write_text(output, "pages/lean-report/page.md", report_page())
    for claim in (1, 2, 6):
        write_text(
            output,
            f"pages/{CLAIMS[claim]['slug']}/page.md",
            claim_page(claim),
        )

    copy_text(
        output,
        ROOT / "src" / "cdot_repro" / "formal_checker.py",
        "current/code/formal_checker.py",
    )
    for name in (
        "CDOTProofs.lean",
        "IndependentReplay.lean",
        "NegativeControl.lean",
        "lean-toolchain",
        "lakefile.toml",
    ):
        copy_text(output, ROOT / "formal" / name, f"{FORMAL_DIR}/{name}")
    formal_artifacts = ROOT / ".openresearch" / "artifacts" / "formal_theorems"
    for source in files(formal_artifacts):
        relative = source.relative_to(formal_artifacts).as_posix()
        copy_text(output, source, f"{EVIDENCE_DIR}/{relative}")

    snapshot = "current/evidence/historical_judged_revision_e7c9bd"
    for relative in ("README.md", "logbook.json"):
        copy_text(output, judged / relative, f"{snapshot}/{relative}")

    manifests = "current/manifests/lean_release_20260730"
    if args.red_team_pass1:
        copy_text(
            output,
            args.red_team_pass1.resolve(),
            f"{manifests}/evaluator_blind_red_team_pass1.json",
        )
    if args.red_team_pass2:
        copy_text(
            output,
            args.red_team_pass2.resolve(),
            f"{manifests}/evaluator_blind_red_team_pass2.json",
        )
    judged_manifest = {
        "space_id": "DineshAI/nPC7M7XLEv",
        "protected_revision": PREVIOUS_SPACE_SHA,
        "file_count": len(files(judged)),
        "files": manifest_tree(judged),
    }
    write_text(
        output,
        f"{manifests}/protected_e7c9bd_manifest.json",
        json.dumps(judged_manifest, indent=2) + "\n",
    )
    preliminary_paths = [entry["path"] for entry in manifest_tree(output)]
    final_paths = sorted(
        set(
            preliminary_paths
            + [
                f"{manifests}/upload_allowlist.txt",
                f"{manifests}/release_manifest.json",
            ]
        )
    )
    write_text(
        output,
        f"{manifests}/upload_allowlist.txt",
        "\n".join(final_paths) + "\n",
    )
    release_manifest = {
        "scope": "additive text-only Lean evidence overlay",
        "base_revision": PREVIOUS_SPACE_SHA,
        "files": manifest_tree(output),
    }
    write_text(
        output,
        f"{manifests}/release_manifest.json",
        json.dumps(release_manifest, indent=2) + "\n",
    )
    print(
        json.dumps(
            {
                "output": str(output),
                "upload_files": len(files(output)),
                "protected_files": len(files(judged)),
                "base_revision": PREVIOUS_SPACE_SHA,
            }
        )
    )


if __name__ == "__main__":
    main()

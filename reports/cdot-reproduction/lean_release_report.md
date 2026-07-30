- Previous live judged score: `9/12`
- Conservative projected score range after the proposed change: **9–12/12**
- Best-supported possible new score: **12/12 forecast; not a judge result**

# Lean release and verification report

The recorded score remains **9/12** until the live evaluator judges the new
Hugging Face revision. This release changes the evidence for Claims 1, 2, and
6; it does not claim that their three forecast points have already been
awarded.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | MEDIUM | VERIFIED | Lean checks compact attainment, the squared-residual identity, and Jensen convexity. Continuity/lower-semicontinuity of the paper-specific population objective remains an explicit premise. |
| 2 | 1 | 2 | MEDIUM | VERIFIED | Lean checks the weighted Minkowski step and exact conditional-variance dispersion identity. The paper-specific gluing construction and component triangle inequalities remain premises. |
| 3 | 2 | 2 | HIGH | VERIFIED | Retained exact 2,000-point, 100-trial reproduction with CDOT below FGW and IsoRank and paired confidence intervals below zero. |
| 4 | 2 | 2 | HIGH | FALSIFIED | Retained primary-archive cohort counterexample plus all 4,950 OASIS-3 pairs reproducing both Table 3 method directions. |
| 5 | 2 | 2 | MEDIUM | FALSIFIED | Retained full MUTAG/ENZYMES all-pairs nested-CV experiment; ENZYMES reverses under all three seeds. Unpublished protocol choices remain an interpretation risk. |
| 6 | 1 | 2 | MEDIUM | VERIFIED | Lean checks the exact `E1+E2+E3` constants, `O(1/T)` term, consistency squeeze, and bad-schedule control. The three empirical-process bounds are explicit premises. |

Current total: **9/12**. Conservative projected total: **9–12/12**.
Best-supported possible total: **12/12 forecast; not a judge result**.
Claims 1, 2, and 6 changed since the previous judge result. No claim is
`BLOCKED`; the remaining uncertainty is whether the evaluator accepts the
explicit theorem premises as sufficiently faithful formal reconstruction.

## Publication

- Existing Space: `DineshAI/nPC7M7XLEv`
- Previous Hugging Face and judge head:
  `e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032`
- Published Hugging Face revision:
  `819b602292066602b465aa8ac59babce4f673b95`
- Current judge head at publication time: previous revision `e7c9bd313…`;
  the new revision is awaiting evaluation
- Upload: exactly 28 allowlisted UTF-8 text paths in one additive commit,
  with parent `e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032`
- No files were deleted and no second Space was created
- Exact allowlist:
  [upload_allowlist.txt](../../space_release/current/manifests/lean_release_20260730/upload_allowlist.txt)
- SHA-256 release manifest:
  [release_manifest.json](../../space_release/current/manifests/lean_release_20260730/release_manifest.json)

The judged revision was downloaded before modification and its 263-file
manifest was protected. The published revision contains 289 files; all 263
protected paths remain present and every protected page is byte-identical.
The exact published revision was downloaded into a fresh directory after
upload. All 28 uploaded hashes matched, the evaluator-blind traversal opened
247 reachable files, all six current claim pages were found, and no missing
visibility cell, broken link, secret, or protected-file mutation was found.

## Experiment tree

The stacked line is:

`Claim 1 → Claim 2 → Claim 6 → Claim 4 archive audit → Claim 5 full
TUDataset → Claim 3 paper-scale synthetic → evaluator package → OASIS repair
→ complete raw evidence → Lean kernel certificates`.

The winning formal node is
`orx/lean-kernel-certificates-for-claims-1-2-and-6` at
`4aadbbfe008cc725fbba6005ccbadacb929db40c`. Its completed cumulative run is
`6b7ccf1e-9abb-4909-aa87-0712d870cebc` on Hugging Face job
`DineshAI/6a6a9402b36a6516e96a166d`.

The run used Hugging Face `cpu-upgrade`, exposed 64 logical CPUs, used no GPU,
and took 5h37m. Including six non-scientific Lean development jobs, the new
formal round used approximately 5.78 job-hours. At the previously recorded
nominal `cpu-upgrade` rate of $0.03/hour, that is about **$0.17**. Combining
the earlier campaign estimate gives approximately 37.0 job-hours and
**$1.11 nominal cost**. These are rate-based estimates, not billing records.
Local work was restricted to short single-core audits and presentation
generation.

## Material commands

Every formal experiment inherited the fixed command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

The additive release was prepared and audited with:

```bash
uv run --frozen --python 3.12 python scripts/prepare_lean_space_release.py --judged <judged-revision> --output <overlay>
uv run --frozen --python 3.12 python scripts/audit_space_candidate.py --judged <judged-revision> --overlay <overlay> --candidate <candidate> --report <report>
uvx --from 'marimo>=0.17' marimo check notebooks/cdot_reproduction.py
uv run --frozen --python 3.12 python scripts/publish_space_overlay.py --repo-id DineshAI/nPC7M7XLEv --overlay <overlay> --allowlist <allowlist> --parent-commit e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032 --commit-message "Add Lean kernel certificates for Claims 1, 2, and 6"
```

The publisher used the text-only Hugging Face API path with
`HfApi.create_commit`; the exact allowlist was the complete upload surface.

## Evidence

- [Lean verification overview](lean-verification.md)
- [Lean source](../../formal/CDOTProofs.lean)
- [Independent importing replay](../../formal/IndependentReplay.lean)
- [False-theorem control](../../formal/NegativeControl.lean)
- [Formal gate summary](../../.openresearch/artifacts/formal_theorems/raw/formal_gate_summary.json)
- [Independent checker output](../../.openresearch/artifacts/formal_theorems/raw/formal_independent_checker.json)
- [Negative-control output](../../.openresearch/artifacts/formal_theorems/raw/formal_negative_control.json)
- [Evaluator-blind pass 1](../../space_release/current/manifests/lean_release_20260730/evaluator_blind_red_team_pass1.json)
- [Evaluator-blind pass 2](../../space_release/current/manifests/lean_release_20260730/evaluator_blind_red_team_pass2.json)

## Awaiting judge

The exact publication action has already been performed: the additive
allowlisted overlay was committed to the existing Space and mirrored to
GitHub. Space revision `819b602292066602b465aa8ac59babce4f673b95` is now
awaiting the live evaluator. The only authoritative next score is the verdict
whose `space_id` is exactly `DineshAI/nPC7M7XLEv` and whose revision matches
the published head.

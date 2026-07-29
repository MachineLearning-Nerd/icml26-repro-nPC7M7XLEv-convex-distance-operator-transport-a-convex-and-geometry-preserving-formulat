- Previous live judged score: `4/12`
- Conservative projected score range after the proposed change: **10–12/12**
- Best-supported possible new score: **12/12 forecast; not a judge result**

# Release and verification report

The current total score remains **4/12** until the live evaluator records a
verdict for the published revision. No score increase is claimed here.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | VERIFIED | Population proof obligations, symbolic identity, independent quadratic checker, and a destructive control. A human-checkable certificate is not a kernel-checked formal proof. |
| 2 | 1 | 2 | HIGH | VERIFIED | Gluing and conditional-variance certificate, complete declared finite domain, four-index checker, and squared-distance control. |
| 3 | 0 | 2 | HIGH | VERIFIED | Exact 2,000-point scale, 100 paired trials, both confidence intervals below zero, complete raw inventory, and parity/tamper controls. |
| 4 | 0 | 2 | HIGH | FALSIFIED | All 4,950 pairs reproduce both Table 3 directions, while an independently parsed primary-archive subject falsifies the literal 696-by-170 cohort invariant. Unpublished preprocessing prevents exact-cell recovery. |
| 5 | 1 | 2 | MEDIUM | FALSIFIED | Full all-pairs repeated nested CV reverses ENZYMES under all three seeds. Unpublished split, scaling, and tolerance choices remain a protocol-interpretation risk. |
| 6 | 1 | 2 | HIGH | VERIFIED | Population decomposition, exact Frank--Wolfe schedules, independent matrix checker, and invalid-schedule control. |

All six claims have new evaluator-visible evidence. Claims 1, 2, and 6 replace
toy checks with analytical certificates and executable obligations. Claim 3
adds the exact paper-scale 100-trial experiment. Claim 4 adds all 4,950
OASIS-3 pairs and a primary-archive counterexample. Claim 5 replaces the proxy
task with the full MUTAG/ENZYMES protocol. No claim is `BLOCKED`.

## Publication

- Existing Space only: `DineshAI/nPC7M7XLEv`
- Previous live judged revision: `1f2e1bcdc00bd792921b6b010c90fe8120f78405`
- Upload parent: `3445f49f57ef2a72286f68932d9700def4faafb6`
- Published revision: `e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032`
- Upload: 249 UTF-8 text paths through one additive Hugging Face API commit;
  no deletions
- Exact allowlist:
  [`space_release/current/manifests/upload_allowlist.txt`](../../space_release/current/manifests/upload_allowlist.txt)
- SHA-256 manifest:
  [`space_release/current/manifests/release_manifest.json`](../../space_release/current/manifests/release_manifest.json)
- Historical safety: all 45 files from the judged revision remain present;
  every protected page is byte-identical
- Postpublication audit:
  [machine-readable result](../../.openresearch/artifacts/release/postpublication_audit.json)

The exact published revision was downloaded into a fresh directory. All 249
uploaded hashes and all 248 non-recursive manifest entries matched. A blind
traversal opened 231 evaluator-reachable files, found all six claim pages, and
reported zero gaps. Trackio's remote reader discovered every current claim
page directly from the public Space.

## Experiment tree and compute

The stacked experiment line is:

`Claim 1 baseline → Claim 2 → Claim 6 → Claim 4 archive audit → Claim 5 full
TUDataset → Claim 3 paper-scale synthetic → evaluator package → Trackio/OASIS
repair → complete-raw release candidate`.

The winning formal branch is
`orx/release-candidate-complete-raw-oasis-evidence` at
`e11a535552fc6f854fe5c07086034992ae426eae`. Its cumulative run
`4df2d784-42ce-4fa3-af50-3d03063f38fb` took 38,009.734 seconds on Hugging Face
`cpu-upgrade`; the runner exposed 64 logical CPUs while each numerical process
enforced the recorded thread limit. All formal experiments used CPU only.

Across the 11 recorded Hugging Face jobs, including two early non-scientific
failures, the dashboard reports approximately 31.22 job-hours. At the
published `cpu-upgrade` rate of $0.03/hour, the nominal compute charge is
approximately **$0.94**; billing statements, credits, and taxes are outside
the available evidence. Local work was limited to short single-core audits
and presentation generation.

## Material commands

Every formal node inherited the unchanged command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

The release was generated, checked, and read with:

```bash
uv run --frozen --python 3.12 python scripts/prepare_space_release.py --judged <judged-revision> --output <overlay>
uv run --frozen --python 3.12 python scripts/finalize_space_manifest.py <overlay>
uv run --frozen --python 3.12 python scripts/audit_space_candidate.py --judged <judged-revision> --overlay <overlay> --candidate <candidate> --report <report>
uvx --from marimo==0.23.15 marimo check --strict notebooks/cdot_reproduction.py
trackio logbook read --path DineshAI/nPC7M7XLEv pages
```

The upload itself used `HfApi.create_commit` with 249
`CommitOperationAdd` entries, the exact allowlist, and parent revision
`3445f49f57ef2a72286f68932d9700def4faafb6`.

## Awaiting judge

The paper is now awaiting evaluation of Space revision
`e7c9bd313c5bc8f5d252f0f5ac2dce3e087ba032`. A 12/12 score is the
best-supported forecast, not a result; only the live judge can change the
recorded score.

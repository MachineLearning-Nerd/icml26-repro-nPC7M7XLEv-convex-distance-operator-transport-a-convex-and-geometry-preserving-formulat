# CURRENT — Claim 4: OASIS-3 cohort and Table 3

---
<!-- trackio-cell
{"type":"markdown","id":"cell_current_claim_4","created_at":"2026-07-29T04:00:00+00:00","title":"CURRENT \u2014 Claim 4: OASIS-3 cohort and Table 3","pinned":true,"pinned_at":"2026-07-29T04:00:00+00:00"}
-->
**Current candidate verdict: FALSIFIED.**

The new registered verifier executes all 4,950 unordered pairs among the
lexicographically first 100 subjects under both Table 3 metrics, with CDOT
and FGW at `alpha=0.5` and `T=200`. It separately retains the exhaustive
primary-archive counterexample to the literal 696-by-170 cohort invariant.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Formal run `4df2d784-42ce-4fa3-af50-3d03063f38fb` at Git
`e11a535552fc6f854fe5c07086034992ae426eae` passed every primary and
independent gate. The exact 654,450,976-byte archive contains 975 sessions and 696 subjects,
but only 695 subjects have any exact 170-node session. `OAS30938` has one
session with 168 nodes and atlas IDs 1 through 168. Its file SHA-256 is
`65c4559e2ae0990efca870279ca569166353c74c6aab4a65d8e4b8abfc70359e`.
An independent XML parser confirmed the counterexample, and padding IDs 169
and 170 was rejected.

The complete rerun observed:

| Metric | Paper CDOT | Paper FGW | Reproduction CDOT | Reproduction FGW | Direction |
| --- | ---: | ---: | ---: | ---: | --- |
| Diffusion | `0.6136` | `0.1853` | `0.7186226976 ± 0.0014093865 SE` | `0.1540475342 ± 0.0004202528 SE` | reproduced |
| Geodesic | `0.4640` | `0.5375` | `0.4651527035 ± 0.0020493222 SE` | `0.5341390374 ± 0.0023019770 SE` | reproduced |

The independent checker loaded exactly 19,800 method/metric rows, reconstructed
all 4,950 unique pairs, and recomputed the four means with maximum absolute
error `3.56e-11`. Every marginal and monotonic-objective gate passed. Six
fixed-pair FGW objectives matched POT `0.9.6.post1` exactly. The 12-pair
anatomical misregistration control degraded mean accuracy from `0.4832107843`
to `0.0653186274`.

Claim 4 is `FALSIFIED` for the composite literal statement because the exact
696-by-170 cohort invariant is false. Separately, the registered full Table 3
route faithfully reproduces both reported method-ordering directions; exact
cell agreement is not asserted.

Raw evidence:

- [Superseding primary result](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_result.json)
- [Table 3 result](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_result.json)
- [Independent checker](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_independent_checker.json)
- [Cumulative run summary](../../current/evidence/claim_4/raw/formal_4df2d784/run_summary.json)
- [Formal materialization manifest](../../current/evidence/claim_4/raw/formal_4df2d784/materialization_manifest.json)

The superseded first formal serialization used 500-row pair chunks, whose
logged hashes show sizes of 130–217 kB. The current run changes only
serialization to 99 200-row chunks; the largest is `86,881` bytes, so every
raw row is evaluator-downloadable under the runner's 100 kB evidence ceiling.

## Exact source statement and assumptions

- Paper Table 3: `https://ar5iv.labs.arxiv.org/html/2606.02047#S6.T3`
- Pinned paper HTML SHA-256:
  `602040fe82ec6bd4c0422ee488315d8e09f86bef50c6f06d4be61f942094d43f`
- Primary provider page:
  `https://braingraph.org/cms/download-pit-group-connectomes/`
- Provider page retrieval: `2026-07-28`; SHA-256
  `14c8e97c97681caab50e33b596a7c85fa18f11a96e497fe1a6ae216585dde8db`
- Primary Scale-2 archive:
  `https://braingraph.org/static/oasis3_graphmls_scale2.7z`

The paper states 696 subjects, 170-node networks, all 4,950 pairs among the
first 100 subjects, `alpha=0.5`, `T=200`, diffusion scale `t=1`, and the four
Table 3 accuracies. The provider independently describes OASIS-3 as 696
subjects and Scale 2 as 170 nodes.

The registered numerical route uses the lexicographically first 100 subject
IDs and each earliest session because the paper publishes neither filenames
nor code. It evaluates all 4,950 unordered pairs, not a proxy subset. The
paper names a graph Laplacian but does not specify normalized versus
combinatorial form; the registered main route discloses the normalized
Laplacian.

The archive route separately tests the cohort premise over the entire primary
archive. It does not reinterpret a failed numerical rerun, missing access, or
an implementation error as falsification.

## Executable method

The fixed cumulative command downloads the primary 624 MB Scale-2 archive
with an explicit User-Agent, verifies its byte count and SHA-256, and extracts
it with a separately pinned official 7-Zip 25.01 binary. It compares the 7-Zip
member listing with the extracted filenames, hashes every GraphML, parses
every `dn_multiscaleID`, and groups all sessions by lexical subject ID.

For the registered Table 3 route it selects the first 100 lexical subject IDs
and each earliest session. Node order is the common `dn_multiscaleID` atlas.
Node features are joint hemisphere/cortical-status categories; edge weights
are `number_of_fibers`. It computes normalized-Laplacian heat-kernel diffusion
distance at `t=1` and normalized shortest-path distance with reciprocal fiber
counts as edge costs. CDOT and FGW use `alpha=0.5`, exactly 200 Frank--Wolfe
iterations, exact Hungarian linear minimization, and exact quadratic line
search. Matching accuracy is the identity fraction after Hungarian
maximization of the final coupling.

Eight independent pair workers execute all 4,950 pairs. A fixed-pair POT FGW
oracle checks the custom solver. A cyclic shift of right-side anatomical
categories is the destructive control and must reduce accuracy. The
independent checker reconstructs the exact pair inventory, all four raw means,
and both directions without calling the primary summarizer; it also directly
reparses the archive counterexample with a separate XML code path.

Formal run `4df2d784-42ce-4fa3-af50-3d03063f38fb` at Git
`e11a535552fc6f854fe5c07086034992ae426eae` passed all gates. It
observed diffusion CDOT/FGW means `0.7186226976/0.1540475342` and geodesic
CDOT/FGW means `0.4651527035/0.5341390374`. The independent checker loaded
all 19,800 rows and reproduced the summaries to `3.56e-11`. The release
candidate stores the raw rows in 99 200-row JSON chunks; the largest is
`86,881` bytes, below the runner's 100 kB inline-evidence ceiling.

Estimated active cores are eight during matching and four during extraction.
Hugging Face `cpu-upgrade` is mandatory because the cumulative run is
multi-hour and uses more than one CPU core.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

The verifier is invoked only through the fixed cumulative command. The runner raises on any failed claim gate, checker gate, or control gate, so the process exits nonzero when the published evidence does not validate.

### Code

- [Primary verifier](../../current/code/claim4.py)
- [Independent checker](../../current/code/claim4_checker.py)
- [Cumulative nonzero-exit runner](../../current/code/run.py)

### Raw machine-readable evidence

- [claim_4_file_manifest_000.json](../../current/evidence/claim_4/raw/claim_4_file_manifest_000.json)
- [claim_4_file_manifest_001.json](../../current/evidence/claim_4/raw/claim_4_file_manifest_001.json)
- [claim_4_file_manifest_002.json](../../current/evidence/claim_4/raw/claim_4_file_manifest_002.json)
- [claim_4_file_manifest_003.json](../../current/evidence/claim_4/raw/claim_4_file_manifest_003.json)
- [claim_4_file_manifest_004.json](../../current/evidence/claim_4/raw/claim_4_file_manifest_004.json)
- [claim_4_independent_checker.json](../../current/evidence/claim_4/raw/claim_4_independent_checker.json)
- [claim_4_negative_control.json](../../current/evidence/claim_4/raw/claim_4_negative_control.json)
- [claim_4_result.json](../../current/evidence/claim_4/raw/claim_4_result.json)
- [claim_4_session_audit_000.json](../../current/evidence/claim_4/raw/claim_4_session_audit_000.json)
- [claim_4_session_audit_001.json](../../current/evidence/claim_4/raw/claim_4_session_audit_001.json)
- [claim_4_session_audit_002.json](../../current/evidence/claim_4/raw/claim_4_session_audit_002.json)
- [claim_4_session_audit_003.json](../../current/evidence/claim_4/raw/claim_4_session_audit_003.json)
- [claim_4_session_audit_004.json](../../current/evidence/claim_4/raw/claim_4_session_audit_004.json)
- [formal_4b2b62af/claim_4_file_manifest_000.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_file_manifest_000.json)
- [formal_4b2b62af/claim_4_file_manifest_001.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_file_manifest_001.json)
- [formal_4b2b62af/claim_4_file_manifest_002.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_file_manifest_002.json)
- [formal_4b2b62af/claim_4_file_manifest_003.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_file_manifest_003.json)
- [formal_4b2b62af/claim_4_file_manifest_004.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_file_manifest_004.json)
- [formal_4b2b62af/claim_4_independent_checker.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_independent_checker.json)
- [formal_4b2b62af/claim_4_negative_control.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_negative_control.json)
- [formal_4b2b62af/claim_4_result.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_result.json)
- [formal_4b2b62af/claim_4_session_audit_000.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_session_audit_000.json)
- [formal_4b2b62af/claim_4_session_audit_001.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_session_audit_001.json)
- [formal_4b2b62af/claim_4_session_audit_002.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_session_audit_002.json)
- [formal_4b2b62af/claim_4_session_audit_003.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_session_audit_003.json)
- [formal_4b2b62af/claim_4_session_audit_004.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_session_audit_004.json)
- [formal_4b2b62af/claim_4_table3_result.json](../../current/evidence/claim_4/raw/formal_4b2b62af/claim_4_table3_result.json)
- [formal_4b2b62af/materialization_manifest.json](../../current/evidence/claim_4/raw/formal_4b2b62af/materialization_manifest.json)
- [formal_4b2b62af/run_summary.json](../../current/evidence/claim_4/raw/formal_4b2b62af/run_summary.json)
- [formal_4df2d784/claim_4_file_manifest_000.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_file_manifest_000.json)
- [formal_4df2d784/claim_4_file_manifest_001.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_file_manifest_001.json)
- [formal_4df2d784/claim_4_file_manifest_002.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_file_manifest_002.json)
- [formal_4df2d784/claim_4_file_manifest_003.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_file_manifest_003.json)
- [formal_4df2d784/claim_4_file_manifest_004.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_file_manifest_004.json)
- [formal_4df2d784/claim_4_independent_checker.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_independent_checker.json)
- [formal_4df2d784/claim_4_negative_control.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_negative_control.json)
- [formal_4df2d784/claim_4_result.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_result.json)
- [formal_4df2d784/claim_4_session_audit_000.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_session_audit_000.json)
- [formal_4df2d784/claim_4_session_audit_001.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_session_audit_001.json)
- [formal_4df2d784/claim_4_session_audit_002.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_session_audit_002.json)
- [formal_4df2d784/claim_4_session_audit_003.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_session_audit_003.json)
- [formal_4df2d784/claim_4_session_audit_004.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_session_audit_004.json)
- [formal_4df2d784/claim_4_table3_pairs_000.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_000.json)
- [formal_4df2d784/claim_4_table3_pairs_001.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_001.json)
- [formal_4df2d784/claim_4_table3_pairs_002.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_002.json)
- [formal_4df2d784/claim_4_table3_pairs_003.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_003.json)
- [formal_4df2d784/claim_4_table3_pairs_004.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_004.json)
- [formal_4df2d784/claim_4_table3_pairs_005.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_005.json)
- [formal_4df2d784/claim_4_table3_pairs_006.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_006.json)
- [formal_4df2d784/claim_4_table3_pairs_007.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_007.json)
- [formal_4df2d784/claim_4_table3_pairs_008.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_008.json)
- [formal_4df2d784/claim_4_table3_pairs_009.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_009.json)
- [formal_4df2d784/claim_4_table3_pairs_010.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_010.json)
- [formal_4df2d784/claim_4_table3_pairs_011.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_011.json)
- [formal_4df2d784/claim_4_table3_pairs_012.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_012.json)
- [formal_4df2d784/claim_4_table3_pairs_013.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_013.json)
- [formal_4df2d784/claim_4_table3_pairs_014.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_014.json)
- [formal_4df2d784/claim_4_table3_pairs_015.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_015.json)
- [formal_4df2d784/claim_4_table3_pairs_016.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_016.json)
- [formal_4df2d784/claim_4_table3_pairs_017.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_017.json)
- [formal_4df2d784/claim_4_table3_pairs_018.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_018.json)
- [formal_4df2d784/claim_4_table3_pairs_019.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_019.json)
- [formal_4df2d784/claim_4_table3_pairs_020.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_020.json)
- [formal_4df2d784/claim_4_table3_pairs_021.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_021.json)
- [formal_4df2d784/claim_4_table3_pairs_022.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_022.json)
- [formal_4df2d784/claim_4_table3_pairs_023.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_023.json)
- [formal_4df2d784/claim_4_table3_pairs_024.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_024.json)
- [formal_4df2d784/claim_4_table3_pairs_025.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_025.json)
- [formal_4df2d784/claim_4_table3_pairs_026.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_026.json)
- [formal_4df2d784/claim_4_table3_pairs_027.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_027.json)
- [formal_4df2d784/claim_4_table3_pairs_028.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_028.json)
- [formal_4df2d784/claim_4_table3_pairs_029.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_029.json)
- [formal_4df2d784/claim_4_table3_pairs_030.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_030.json)
- [formal_4df2d784/claim_4_table3_pairs_031.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_031.json)
- [formal_4df2d784/claim_4_table3_pairs_032.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_032.json)
- [formal_4df2d784/claim_4_table3_pairs_033.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_033.json)
- [formal_4df2d784/claim_4_table3_pairs_034.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_034.json)
- [formal_4df2d784/claim_4_table3_pairs_035.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_035.json)
- [formal_4df2d784/claim_4_table3_pairs_036.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_036.json)
- [formal_4df2d784/claim_4_table3_pairs_037.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_037.json)
- [formal_4df2d784/claim_4_table3_pairs_038.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_038.json)
- [formal_4df2d784/claim_4_table3_pairs_039.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_039.json)
- [formal_4df2d784/claim_4_table3_pairs_040.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_040.json)
- [formal_4df2d784/claim_4_table3_pairs_041.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_041.json)
- [formal_4df2d784/claim_4_table3_pairs_042.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_042.json)
- [formal_4df2d784/claim_4_table3_pairs_043.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_043.json)
- [formal_4df2d784/claim_4_table3_pairs_044.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_044.json)
- [formal_4df2d784/claim_4_table3_pairs_045.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_045.json)
- [formal_4df2d784/claim_4_table3_pairs_046.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_046.json)
- [formal_4df2d784/claim_4_table3_pairs_047.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_047.json)
- [formal_4df2d784/claim_4_table3_pairs_048.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_048.json)
- [formal_4df2d784/claim_4_table3_pairs_049.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_049.json)
- [formal_4df2d784/claim_4_table3_pairs_050.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_050.json)
- [formal_4df2d784/claim_4_table3_pairs_051.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_051.json)
- [formal_4df2d784/claim_4_table3_pairs_052.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_052.json)
- [formal_4df2d784/claim_4_table3_pairs_053.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_053.json)
- [formal_4df2d784/claim_4_table3_pairs_054.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_054.json)
- [formal_4df2d784/claim_4_table3_pairs_055.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_055.json)
- [formal_4df2d784/claim_4_table3_pairs_056.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_056.json)
- [formal_4df2d784/claim_4_table3_pairs_057.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_057.json)
- [formal_4df2d784/claim_4_table3_pairs_058.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_058.json)
- [formal_4df2d784/claim_4_table3_pairs_059.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_059.json)
- [formal_4df2d784/claim_4_table3_pairs_060.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_060.json)
- [formal_4df2d784/claim_4_table3_pairs_061.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_061.json)
- [formal_4df2d784/claim_4_table3_pairs_062.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_062.json)
- [formal_4df2d784/claim_4_table3_pairs_063.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_063.json)
- [formal_4df2d784/claim_4_table3_pairs_064.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_064.json)
- [formal_4df2d784/claim_4_table3_pairs_065.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_065.json)
- [formal_4df2d784/claim_4_table3_pairs_066.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_066.json)
- [formal_4df2d784/claim_4_table3_pairs_067.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_067.json)
- [formal_4df2d784/claim_4_table3_pairs_068.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_068.json)
- [formal_4df2d784/claim_4_table3_pairs_069.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_069.json)
- [formal_4df2d784/claim_4_table3_pairs_070.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_070.json)
- [formal_4df2d784/claim_4_table3_pairs_071.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_071.json)
- [formal_4df2d784/claim_4_table3_pairs_072.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_072.json)
- [formal_4df2d784/claim_4_table3_pairs_073.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_073.json)
- [formal_4df2d784/claim_4_table3_pairs_074.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_074.json)
- [formal_4df2d784/claim_4_table3_pairs_075.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_075.json)
- [formal_4df2d784/claim_4_table3_pairs_076.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_076.json)
- [formal_4df2d784/claim_4_table3_pairs_077.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_077.json)
- [formal_4df2d784/claim_4_table3_pairs_078.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_078.json)
- [formal_4df2d784/claim_4_table3_pairs_079.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_079.json)
- [formal_4df2d784/claim_4_table3_pairs_080.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_080.json)
- [formal_4df2d784/claim_4_table3_pairs_081.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_081.json)
- [formal_4df2d784/claim_4_table3_pairs_082.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_082.json)
- [formal_4df2d784/claim_4_table3_pairs_083.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_083.json)
- [formal_4df2d784/claim_4_table3_pairs_084.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_084.json)
- [formal_4df2d784/claim_4_table3_pairs_085.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_085.json)
- [formal_4df2d784/claim_4_table3_pairs_086.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_086.json)
- [formal_4df2d784/claim_4_table3_pairs_087.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_087.json)
- [formal_4df2d784/claim_4_table3_pairs_088.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_088.json)
- [formal_4df2d784/claim_4_table3_pairs_089.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_089.json)
- [formal_4df2d784/claim_4_table3_pairs_090.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_090.json)
- [formal_4df2d784/claim_4_table3_pairs_091.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_091.json)
- [formal_4df2d784/claim_4_table3_pairs_092.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_092.json)
- [formal_4df2d784/claim_4_table3_pairs_093.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_093.json)
- [formal_4df2d784/claim_4_table3_pairs_094.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_094.json)
- [formal_4df2d784/claim_4_table3_pairs_095.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_095.json)
- [formal_4df2d784/claim_4_table3_pairs_096.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_096.json)
- [formal_4df2d784/claim_4_table3_pairs_097.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_097.json)
- [formal_4df2d784/claim_4_table3_pairs_098.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_pairs_098.json)
- [formal_4df2d784/claim_4_table3_result.json](../../current/evidence/claim_4/raw/formal_4df2d784/claim_4_table3_result.json)
- [formal_4df2d784/materialization_manifest.json](../../current/evidence/claim_4/raw/formal_4df2d784/materialization_manifest.json)
- [formal_4df2d784/run_summary.json](../../current/evidence/claim_4/raw/formal_4df2d784/run_summary.json)
- [materialization_manifest.json](../../current/evidence/claim_4/raw/materialization_manifest.json)

Final cumulative regression: run `4df2d784-42ce-4fa3-af50-3d03063f38fb` at Git `e11a535552fc6f854fe5c07086034992ae426eae` reran all six claims; every primary and independent checker gate passed. [Cumulative run summary](../../current/evidence/claim_4/raw/formal_4df2d784/run_summary.json).

### Claim contract and evaluation files

- [EVAL.md](../../current/evidence/claim_4/EVAL.md)
- [claim_contract.json](../../current/evidence/claim_4/claim_contract.json)
- [limitations.md](../../current/evidence/claim_4/limitations.md)
- [method.md](../../current/evidence/claim_4/method.md)
- [source_audit.md](../../current/evidence/claim_4/source_audit.md)

## Provenance

- Verdict: **FALSIFIED**
- Confidence: **HIGH**
- Formal run: `4df2d784-42ce-4fa3-af50-3d03063f38fb`
- Evidence Git SHA: `e11a535552fc6f854fe5c07086034992ae426eae`
- Seeds: deterministic first-100/all-pairs protocol; no stochastic seed
- Runtime: 11,591.732 Claim 4 seconds; 38,009.734 cumulative seconds
- Compute: Hugging Face `cpu-upgrade`, 64 logical CPUs exposed; per-process numerical thread limits are recorded in the result.
- Exact command: `uv run --frozen --python 3.12 python -m cdot_repro.run`
- Pinned environment: [pyproject.toml](../../current/environment/pyproject.toml), [uv.lock](../../current/environment/uv.lock)

## Limitations and deviations

- The complete first-100/all-4,950-pair protocol tests the Table 3 numerical
  cells and directions. It does not recover unpublished original filenames,
  code, or seeds.
- No node is padded, relabeled, or replaced. Consequently, the invalid subject
  cannot enter a 170-by-170 matching evaluation without changing the primary
  data.
- The first 100 lexical subjects are unaffected by the sole invalid subject,
  which occurs later in the archive order.
- The paper does not specify whether its diffusion Laplacian is normalized.
  The main route pins the normalized choice rather than silently guessing.
- Directional recovery and exact-cell recovery are reported separately.
- Both method directions reproduce, but diffusion CDOT differs from the paper
  by about `+0.1050` absolute. Unpublished preprocessing details prevent
  claiming exact-cell recovery.
- The data provider calls the archive Scale 2 / 170 nodes; the verifier checks
  the stronger condition that every archived session has exact atlas IDs
  1 through 170.

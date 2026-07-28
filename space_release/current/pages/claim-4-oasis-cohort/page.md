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

- [Primary result](../../evidence/claim_4/raw/claim_4_result.json)
- [Independent checker](../../evidence/claim_4/raw/claim_4_independent_checker.json)
- [Materialization manifest](../../evidence/claim_4/raw/materialization_manifest.json)

The four Table 3 accuracy cells were not rerun and are not inferred from this
counterexample.

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

This route tests the cohort premise over the entire primary archive. It does
not reinterpret a failed numerical rerun, missing access, or an implementation
error as falsification.

## Executable method

The fixed cumulative command downloads the primary 624 MB Scale-2 archive
with an explicit User-Agent, verifies its byte count and SHA-256, and extracts
it with a separately pinned official 7-Zip 25.01 binary. It compares the 7-Zip
member listing with the extracted filenames, hashes every GraphML, parses
every `dn_multiscaleID`, and groups all sessions by lexical subject ID.

An independent checker reconstructs subject IDs from filenames and directly
reparses the counterexample GraphML with a separate XML code path. The
negative control proposes padding IDs 169 and 170; it must be rejected because
those nodes do not exist in the archive.

Estimated active cores are four during extraction and one during the
exhaustive parse. Hugging Face `cpu-upgrade` is mandatory because download,
extraction, and parse runtime are uncertain.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

The verifier is invoked only through the fixed cumulative command. The runner raises on any failed claim gate, checker gate, or control gate, so the process exits nonzero when the published evidence does not validate.

### Code

- [Primary verifier](../../code/claim4.py)
- [Independent checker](../../code/claim4_checker.py)
- [Cumulative nonzero-exit runner](../../code/run.py)

### Raw machine-readable evidence

- [claim_4_file_manifest_000.json](../../evidence/claim_4/raw/claim_4_file_manifest_000.json)
- [claim_4_file_manifest_001.json](../../evidence/claim_4/raw/claim_4_file_manifest_001.json)
- [claim_4_file_manifest_002.json](../../evidence/claim_4/raw/claim_4_file_manifest_002.json)
- [claim_4_file_manifest_003.json](../../evidence/claim_4/raw/claim_4_file_manifest_003.json)
- [claim_4_file_manifest_004.json](../../evidence/claim_4/raw/claim_4_file_manifest_004.json)
- [claim_4_independent_checker.json](../../evidence/claim_4/raw/claim_4_independent_checker.json)
- [claim_4_negative_control.json](../../evidence/claim_4/raw/claim_4_negative_control.json)
- [claim_4_result.json](../../evidence/claim_4/raw/claim_4_result.json)
- [claim_4_session_audit_000.json](../../evidence/claim_4/raw/claim_4_session_audit_000.json)
- [claim_4_session_audit_001.json](../../evidence/claim_4/raw/claim_4_session_audit_001.json)
- [claim_4_session_audit_002.json](../../evidence/claim_4/raw/claim_4_session_audit_002.json)
- [claim_4_session_audit_003.json](../../evidence/claim_4/raw/claim_4_session_audit_003.json)
- [claim_4_session_audit_004.json](../../evidence/claim_4/raw/claim_4_session_audit_004.json)
- [materialization_manifest.json](../../evidence/claim_4/raw/materialization_manifest.json)

### Claim contract and evaluation files

- [EVAL.md](../../evidence/claim_4/EVAL.md)
- [claim_contract.json](../../evidence/claim_4/claim_contract.json)
- [limitations.md](../../evidence/claim_4/limitations.md)
- [method.md](../../evidence/claim_4/method.md)
- [source_audit.md](../../evidence/claim_4/source_audit.md)

## Provenance

- Verdict: **FALSIFIED**
- Confidence: **HIGH**
- Formal run: `1da20861-93a5-4053-af25-7168943eaeee`
- Evidence Git SHA: `783db52bac086f41d8ce4c58b36f5fb4d2111164`
- Seeds: deterministic exhaustive archive enumeration; no stochastic seed
- Runtime: 195.317 scientific seconds
- Compute: Hugging Face `cpu-upgrade`, 64 logical CPUs exposed; per-process numerical thread limits are recorded in the result.
- Exact command: `uv run --frozen --python 3.12 python -m cdot_repro.run`
- Pinned environment: [pyproject.toml](../../environment/pyproject.toml), [uv.lock](../../environment/uv.lock)

## Limitations and deviations

- This is a direct falsification of the literal 696-subject/170-node cohort
  premise. It is not a rerun of the four Table 3 numerical cells.
- No node is padded, relabeled, or replaced. Consequently, the invalid subject
  cannot enter a 170-by-170 matching evaluation without changing the primary
  data.
- The result does not say whether the reported numerical directions hold for
  a disclosed 695-subject valid subset or the first 100 valid subjects.
- The data provider calls the archive Scale 2 / 170 nodes; the verifier checks
  the stronger condition that every archived session has exact atlas IDs
  1 through 170.

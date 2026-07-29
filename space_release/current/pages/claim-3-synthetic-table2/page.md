# Claim 3 — synthetic Table 2

**Current candidate verdict: VERIFIED.**

The source's `n=500` is per region, not total: every trial has four groups and
`N=2,000`. The registered verifier runs 100 independent trials at `alpha=0.5`
and `T=200`, comparing CDOT, POT FGW, and the stated IsoRank recurrence.
Paired 95% intervals test the ordering; paper values and rerun values remain
separate.

| Method | Paper mean MSE | Reproduction mean MSE | 95% CI |
| --- | ---: | ---: | ---: |
| CDOT | `0.0016` | `0.00169364` | `[0.00159191, 0.00179537]` |
| FGW | `0.0034` | `0.00351401` | `[0.00341589, 0.00361214]` |
| IsoRank | `0.0033` | `0.00337785` | `[0.00328268, 0.00347302]` |

The paired CDOT-minus-FGW interval is
`[-0.00185460, -0.00178615]`; the paired CDOT-minus-IsoRank interval is
`[-0.00171853, -0.00164989]`. Both are wholly below zero. The independent
checker reconstructed the exact 300-row inventory, raw means, paired
intervals, and verdict. A missing-row mutation was rejected, dense/lazy CDOT
and dense/low-rank IsoRank parity errors were exactly zero, and the
wrong-feature control increased MSE from `0.04484` to `1.71324`.

Formal run `8a1fe020-2a83-4a6a-bbc6-910568b8b5c1`, Git
`2517fb252abbd2aef3c8666e6337b44f6d198724`, 19,878.94 scientific seconds,
HF `cpu-upgrade`, 64 logical CPUs allocated as four workers × 16 numerical
threads.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Raw files:

- [100-trial rows](../../evidence/claim_3/raw/claim_3_trials.json)
- [Primary result](../../evidence/claim_3/raw/claim_3_result.json)
- [Independent checker](../../evidence/claim_3/raw/claim_3_independent_checker.json)
- [Negative controls](../../evidence/claim_3/raw/claim_3_negative_controls.json)

## Exact source statement and assumptions

Pinned source: arXiv:2606.02047v1, HTML SHA-256
`602040fe82ec6bd4c0422ee488315d8e09f86bef50c6f06d4be61f942094d43f`;
PDF SHA-256
`fe1dda5d0e3f2aea86b9b3b5ebf79b79cbc7d06e3fcbe4b20b6f097cc556375d`.
Retrieved 2026-07-28.

Section 6.1 defines `[0,2]^2` split into four unit squares, uniform sampling of
`n` points from each region, hence `N=4n`, a 0/1 region-label mismatch cost,
distance matrices divided by their maxima, `alpha=0.5`, `T=200`, and MSE
between `X` and `N*pi*Y`. Table 2 reports 100-trial mean ± standard deviation.
At `n=500`, it prints CDOT `0.0016 ± 0.00`, FGW `0.0034 ± 0.00`, and IsoRank
`0.0033 ± 0.00`.

Appendix H.2 states POT default conditional gradient for FGW, Gaussian
similarity `exp(-d^2/2)` and row normalization for IsoRank, feature prior
`H=1-Cf`, iterative propagation, and a Hungarian projection.

Unpublished quantities are material: no code, random seeds, CDOT empirical
step-size rule, or CDOT initial coupling is supplied. The reconstruction pins
independent PCG64 seeds, the product coupling, and exact quadratic line search,
and reports these as deviations rather than filling them silently.

## Executable method

The formal fixed command reruns every accepted earlier claim, then executes 100
independent paper-scale trials. Four spawned workers use 16 CPU threads each on
HF `cpu-upgrade`.

CDOT implements Algorithm 2's affine lazy-gradient recurrence with exact
Hungarian linear minimization and exact quadratic line search. A small
deterministic parity test compares it with the dense standard-FW equations.
FGW calls POT's disclosed fused-GW conditional-gradient solver. IsoRank uses an
exact low-rank evaluation of its rank-four feature-prior recurrence, followed
by the stated Hungarian projection; a dense recurrence parity test precedes
the full run.

The primary comparison is paired by trial. CDOT supports the reported ordering
only when the upper endpoint of both two-sided paired 95% t intervals is below
zero. Exact displayed-value agreement is audited separately. A wrong-feature
control must materially worsen CDOT, and a dropped raw row must be rejected by
the independent inventory checker.

The verifier is invoked only through the fixed cumulative command. The runner raises on any failed claim gate, checker gate, or control gate, so the process exits nonzero when the published evidence does not validate.

### Code

- [Primary verifier](../../code/claim3.py)
- [Independent checker](../../code/claim3_checker.py)
- [Cumulative nonzero-exit runner](../../code/run.py)

### Raw machine-readable evidence

- [claim_3_independent_checker.json](../../evidence/claim_3/raw/claim_3_independent_checker.json)
- [claim_3_negative_controls.json](../../evidence/claim_3/raw/claim_3_negative_controls.json)
- [claim_3_result.json](../../evidence/claim_3/raw/claim_3_result.json)
- [claim_3_trials.json](../../evidence/claim_3/raw/claim_3_trials.json)
- [materialization_manifest.json](../../evidence/claim_3/raw/materialization_manifest.json)

Final cumulative regression: run `4df2d784-42ce-4fa3-af50-3d03063f38fb` at Git `e11a535552fc6f854fe5c07086034992ae426eae` reran all six claims; every primary and independent checker gate passed. [Cumulative run summary](../../evidence/claim_4/raw/formal_4df2d784/run_summary.json).

### Claim contract and evaluation files

- [EVAL.md](../../evidence/claim_3/EVAL.md)
- [claim_contract.json](../../evidence/claim_3/claim_contract.json)
- [limitations.md](../../evidence/claim_3/limitations.md)
- [method.md](../../evidence/claim_3/method.md)
- [source_audit.md](../../evidence/claim_3/source_audit.md)

## Provenance

- Verdict: **VERIFIED**
- Confidence: **HIGH**
- Formal run: `8a1fe020-2a83-4a6a-bbc6-910568b8b5c1`
- Evidence Git SHA: `2517fb252abbd2aef3c8666e6337b44f6d198724`
- Seeds: PCG64 seeds 260602047 through 260602146
- Runtime: 19,878.939 scientific seconds
- Compute: Hugging Face `cpu-upgrade`, 64 logical CPUs exposed; per-process numerical thread limits are recorded in the result.
- Exact command: `uv run --frozen --python 3.12 python -m cdot_repro.run`
- Pinned environment: [pyproject.toml](../../environment/pyproject.toml), [uv.lock](../../environment/uv.lock)

## Limitations and deviations

- The source does not publish code or seeds, so exact bitwise reconstruction is
  impossible.
- The source leaves the CDOT experimental step-size and initial coupling
  unspecified; this run pins exact line search and the product coupling.
- POT may satisfy its disclosed stopping test before the maximum 200
  iterations.
- Only the three methods named in this claim are tested. EFGW, Spectral, and
  COPT are outside this claim contract.
- A significant ordering match is not presented as equality with the paper's
  four-decimal means.

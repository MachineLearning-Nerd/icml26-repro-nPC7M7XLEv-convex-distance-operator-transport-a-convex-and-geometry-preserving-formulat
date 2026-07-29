# Claim 2 — pseudometric and dispersion gap

The exact contract preserves both universal quantifiers: the square-root CDOT
minimum is a pseudometric for every attributed compact metric-measure-space
triple and fusion weight, and the dispersion identity holds for every fixed
coupling.

Evidence includes an independent glued-coupling and conditional-variance
certificate, an exhaustive 320-cell declared two-point domain, 32 diffuse
coupling identities with raw matrices, an independent four-index checker, and
a squared-distance destructive control.

The unchanged cumulative command is:

```text
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Formal cumulative run `318c9d3c-fc01-4fd5-9cb0-e64031bb4d82` at Git
`b24b5f079f8bb06970e808f51589830765004577` passed every gate:

| Evidence | Observed |
| --- | ---: |
| Dispersion witnesses | 32 / 32 pass |
| Maximum dispersion identity error | `2.498001805406602e-16` |
| Complete declared pseudometric cells | 320 |
| Identity / symmetry / triangle failures | `0 / 0 / 0` |
| Independent four-index disagreement | `1.942890293094024e-16` |
| Squared-discrepancy control excess | `0.08120000000000005` |
| Scientific runtime | `2.9290183228 s` |
| Compute | HF `cpu-upgrade`, 64 logical CPUs exposed, 1 thread enforced |

Raw files:

- [Primary result](../../evidence/claim_2/raw/claim_2_result.json)
- [Independent checker](../../evidence/claim_2/raw/claim_2_independent_checker.json)

The current candidate verdict is `VERIFIED`; only the live evaluator can
award points.

## Exact source statement and assumptions

- Primary source and hashes: identical to Claim 1's pinned arXiv source.
- Pseudometric anchor: `#S3.Thmtheorem5`; proof in Appendix G.4.
- Dispersion-gap anchor: `#S3.Thmtheorem7`; proof in Appendix G.5.

The pseudometric quantifier is universal over attributed compact
metric-measure spaces for each `alpha` in `[0,1]`. It asserts nonnegativity,
diagonal identity, symmetry, and triangle inequality for the square root of
the minimized objective; it does not assert identity of indiscernibles.

The dispersion identity is pointwise in the choice of coupling: for every
coupling of the fixed marginals, the quadratic GW risk minus the CDOT
structural risk equals the paper's sum of two conditional variances.


## Executable method

The population certificate independently reconstructs the transpose-coupling
symmetry, Markov gluing, conditional-expectation contraction and composition,
Hilbert--Schmidt ideal inequalities, and the conditional-variance identity.

The executable verifier exhausts 320 cells over a predeclared complete finite
domain of four two-point spaces, 64 ordered triples, and five fusion weights.
It separately evaluates the dispersion identity on 32 diffuse couplings.
Every raw matrix and coupling is serialized so the independent checker can
recompute the four-index GW sum without calling the primary `einsum`.

The destructive control squares an otherwise valid discrepancy. The verifier
requires that mutation to violate triangle inequality.


The verifier is invoked only through the fixed cumulative command. The runner raises on any failed claim gate, checker gate, or control gate, so the process exits nonzero when the published evidence does not validate.

### Code

- [Primary verifier](../../code/claim2.py)
- [Independent checker](../../code/claim2_checker.py)
- [Cumulative nonzero-exit runner](../../code/run.py)

### Raw machine-readable evidence

- [claim_2_independent_checker.json](../../evidence/claim_2/raw/claim_2_independent_checker.json)
- [claim_2_result.json](../../evidence/claim_2/raw/claim_2_result.json)

Final cumulative regression: run `4df2d784-42ce-4fa3-af50-3d03063f38fb` at Git `e11a535552fc6f854fe5c07086034992ae426eae` reran all six claims; every primary and independent checker gate passed. [Cumulative run summary](../../evidence/claim_4/raw/formal_4df2d784/run_summary.json).

### Claim contract and evaluation files

- [EVAL.md](../../evidence/claim_2/EVAL.md)
- [claim_contract.json](../../evidence/claim_2/claim_contract.json)
- [limitations.md](../../evidence/claim_2/limitations.md)
- [method.md](../../evidence/claim_2/method.md)
- [proof_certificate.md](../../evidence/claim_2/proof_certificate.md)
- [source_audit.md](../../evidence/claim_2/source_audit.md)

## Provenance

- Verdict: **VERIFIED**
- Confidence: **HIGH**
- Formal run: `318c9d3c-fc01-4fd5-9cb0-e64031bb4d82`
- Evidence Git SHA: `b24b5f079f8bb06970e808f51589830765004577`
- Seeds: registered deterministic finite-domain enumeration
- Runtime: 2.929 scientific seconds
- Compute: Hugging Face `cpu-upgrade`, 64 logical CPUs exposed; per-process numerical thread limits are recorded in the result.
- Exact command: `uv run --frozen --python 3.12 python -m cdot_repro.run`
- Pinned environment: [pyproject.toml](../../environment/pyproject.toml), [uv.lock](../../environment/uv.lock)

## Limitations and deviations

- The analytical certificate is not a proof-assistant kernel artifact.
- The executable finite domain is complete only for the explicitly declared
  four-space domain; it does not stand in for the population proof.
- No metric conclusion is claimed: zero discrepancy may identify distinct
  attributed spaces.


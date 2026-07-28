# Claim 6 — deterministic risk bound and consistency

**Current candidate verdict: VERIFIED.**

The exact contract is Theorem 5.6 and Corollary 5.7, including Assumptions
5.2--5.5, fixed distinct empirical supports, Algorithm 1 with
`gamma_t=2/(t+2)`, and the asymptotic condition `n_min/T_n -> 0`.

The population argument is independently reconstructed as an `E1+E2+E3`
decomposition. The executable evidence uses two predeclared raw-witness
panels and an independent matrix checker. Its destructive control replaces
the valid schedule with `T_n=n`; this must be rejected because the required
ratio remains one.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

Formal cumulative run `67a73cba-65ff-4541-b1c1-2cd438b71670` used Git
`2bc46c7b1b1127385fdc3481d802be3a3efbed0f`. All primary and independent
gates passed. The maximum final FW duality gap was
`9.900242946852059e-06`, below the minimum registered theorem optimization
bound `0.04680643588493418`; the maximum marginal error was
`1.8041124150158794e-16`. The independent checker disagreed by exactly zero.

The invalid `T_n=n` control retained `n_min/T_n=1` and its last optimization
term was `15.953261927945473`, so it was rejected for the intended premise
violation. Scientific runtime was `3.16170865111053` seconds. Hugging Face
exposed 64 logical CPUs; the verifier estimated and enforced one numerical
thread.

Raw files:

- [Primary result](../../evidence/claim_6/raw/claim_6_result.json)
- [Independent checker](../../evidence/claim_6/raw/claim_6_independent_checker.json)

## Exact source statement and assumptions

- Pinned HTML: `https://ar5iv.labs.arxiv.org/html/2606.02047`
- HTML SHA-256: `602040fe82ec6bd4c0422ee488315d8e09f86bef50c6f06d4be61f942094d43f`
- Retrieved: `2026-07-28T12:12:31Z`
- Assumptions: `#S5.Thmtheorem2` through `#S5.Thmtheorem5`
- Deterministic bound: `#S5.Thmtheorem6`
- Risk consistency: `#S5.Thmtheorem7`
- Proof: `#A7.SS6`; FW lemma at `#A7.SS8`

Theorem 5.6 assumes non-atomic population laws, the paper's no-ties
condition, Lipschitz feature maps, a Wasserstein-Lipschitz optimal coupling,
fixed empirical measures on distinct points, and Algorithm 1 with
`gamma_t=2/(t+2)`. Its absolute lifted population-risk gap is bounded by

`32 alpha n_min/(T+3) + C(W1(P_X,P_hat_X)+W1(P_Y,P_hat_Y))`,

where Appendix G.6 makes `C=4(2L_f+2L_W+4)` explicit. Corollary 5.7 further
requires iid samples, both sample sizes tending to infinity, and
`n_min/T_n -> 0`; its conclusion is almost-sure convergence of the lifted
risk to the population optimum.

## Executable method

The fixed cumulative command runs two predeclared finite panels with support
12/24, seeds 56001/56002, alpha 0.25/0.8, and 2,048 iterations of the exact
Algorithm 1 schedule. It records objectives and FW duality gaps at fixed
checkpoints. A separate checker reconstructs the gradient, linear assignment,
duality gap, marginals, and bound formula from raw matrices.

The executable also evaluates a declared `T_n=n^2` sequence for dimensions
three and five and a destructive `T_n=n` control. These rows diagnose the two
terms; they are not evidence for the universal theorem or empirical
Wasserstein convergence. The proof-obligation certificate is the claim-level
evidence.

Exact command:

```bash
uv run --frozen --python 3.12 python -m cdot_repro.run
```

The verifier is invoked only through the fixed cumulative command. The runner raises on any failed claim gate, checker gate, or control gate, so the process exits nonzero when the published evidence does not validate.

### Code

- [Primary verifier](../../code/claim6.py)
- [Independent checker](../../code/claim6_checker.py)
- [Cumulative nonzero-exit runner](../../code/run.py)

### Raw machine-readable evidence

- [claim_6_independent_checker.json](../../evidence/claim_6/raw/claim_6_independent_checker.json)
- [claim_6_result.json](../../evidence/claim_6/raw/claim_6_result.json)

### Claim contract and evaluation files

- [EVAL.md](../../evidence/claim_6/EVAL.md)
- [claim_contract.json](../../evidence/claim_6/claim_contract.json)
- [limitations.md](../../evidence/claim_6/limitations.md)
- [method.md](../../evidence/claim_6/method.md)
- [proof_certificate.md](../../evidence/claim_6/proof_certificate.md)
- [source_audit.md](../../evidence/claim_6/source_audit.md)

## Provenance

- Verdict: **VERIFIED**
- Confidence: **HIGH**
- Formal run: `67a73cba-65ff-4541-b1c1-2cd438b71670`
- Evidence Git SHA: `2bc46c7b1b1127385fdc3481d802be3a3efbed0f`
- Seeds: two predeclared deterministic support panels
- Runtime: 3.162 scientific seconds
- Compute: Hugging Face `cpu-upgrade`, 64 logical CPUs exposed; per-process numerical thread limits are recorded in the result.
- Exact command: `uv run --frozen --python 3.12 python -m cdot_repro.run`
- Pinned environment: [pyproject.toml](../../environment/pyproject.toml), [uv.lock](../../environment/uv.lock)

## Limitations and deviations

- The population statement is analytical; no finite experiment can prove its
  universal quantifiers. The finite panels are regression diagnostics only.
- The `n^{-1/d}` values are labeled rate proxies and are not measured
  Wasserstein errors or a circular sample-complexity calibration.
- The certificate reconstructs the paper's result under all listed
  assumptions; it does not establish that Assumption 5.5 holds for arbitrary
  data.
- The checker verifies numerical implementation and formula consistency, not
  the measure-theoretic gluing argument by itself.

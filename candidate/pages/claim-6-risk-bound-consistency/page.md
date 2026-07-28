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

- [Primary result](../../../.openresearch/artifacts/claim_6/raw/claim_6_result.json)
- [Independent checker](../../../.openresearch/artifacts/claim_6/raw/claim_6_independent_checker.json)

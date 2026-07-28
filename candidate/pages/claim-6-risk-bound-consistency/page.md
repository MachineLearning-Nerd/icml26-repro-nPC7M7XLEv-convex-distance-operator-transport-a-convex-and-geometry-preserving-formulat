# Claim 6 — deterministic risk bound and consistency

**Current candidate verdict: BLOCKED pending the formal cumulative run.**

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

Raw result links and numerical values will be inserted only after the formal
Hugging Face `cpu-upgrade` run completes.

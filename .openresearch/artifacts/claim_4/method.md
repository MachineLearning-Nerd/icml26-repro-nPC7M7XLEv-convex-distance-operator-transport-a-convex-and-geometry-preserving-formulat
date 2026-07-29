# Claim 4 method

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

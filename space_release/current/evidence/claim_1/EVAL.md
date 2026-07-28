# Claim 1 evaluation

Planned baseline verdict: `VERIFIED` only if the analytical obligations,
primary executable gates, independent checker, and destructive control all
pass. The run command is:

`uv run --frozen --python 3.12 python -m cdot_repro.run`

The numerical audit itself is estimated to require one core, but a clean
locked-environment installation has uncertain runtime. Under the user-specified
compute rule the baseline is therefore routed to Hugging Face `cpu-upgrade`
while enforcing one numerical thread. Runtime, logical CPU allocation, Git
SHA, Python version, and artifact hashes are printed into the OpenResearch run
log.

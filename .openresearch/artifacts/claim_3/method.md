# Claim 3 method

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

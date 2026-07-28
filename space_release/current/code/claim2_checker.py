"""Independent raw-witness checker for Claim 2."""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

from .claim1 import structural


def check(runtime_dir: Path) -> dict[str, object]:
    witnesses = json.loads((runtime_dir / "claim_2_witnesses.json").read_text())
    rows = json.loads((runtime_dir / "claim_2_dispersion_rows.json").read_text())
    pseudo = json.loads(
        (runtime_dir / "claim_2_pseudometric_rows.json").read_text()
    )
    maximum_error = 0.0
    marginal_error = 0.0
    for witness, recorded in zip(witnesses, rows, strict=True):
        dx = np.asarray(witness["dx"])
        dy = np.asarray(witness["dy"])
        coupling = np.asarray(witness["coupling"])
        n = coupling.shape[0]
        # Direct four-index sum, distinct from the primary einsum expression.
        gw = 0.0
        for i, j, k, ell in itertools.product(range(n), repeat=4):
            gw += (
                (dx[i, k] - dy[j, ell]) ** 2
                * coupling[i, j]
                * coupling[k, ell]
            )
        variance = gw - structural(dx, dy, coupling)
        maximum_error = max(
            maximum_error, abs(variance - recorded["dispersion_V"])
        )
        marginal_error = max(
            marginal_error,
            float(np.max(np.abs(coupling.sum(axis=0) - 1 / n))),
            float(np.max(np.abs(coupling.sum(axis=1) - 1 / n))),
        )
    triangle_failures = sum(row["triangle_excess"] > 1e-10 for row in pseudo)
    grouped: dict[tuple[float, int, int], float] = {}
    for row in pseudo:
        grouped[(row["alpha"], row["x"], row["z"])] = row["d_xz"]
    symmetry_failures = sum(
        abs(distance - grouped[(alpha, z, x)]) > 1e-10
        for (alpha, x, z), distance in grouped.items()
    )
    gates = {
        "all_32_raw_witnesses_recomputed": bool(
            len(witnesses) == len(rows) == 32
        ),
        "independent_four_index_identity_agrees": bool(maximum_error < 1e-10),
        "witness_marginals_exact": bool(marginal_error < 1e-10),
        "all_320_triangle_rows_rechecked": bool(
            len(pseudo) == 320 and triangle_failures == 0
        ),
        "recorded_symmetry_rechecked": bool(symmetry_failures == 0),
    }
    result = {
        "checker": "raw witness four-index enumeration and table recheck",
        "maximum_independent_dispersion_error": float(maximum_error),
        "maximum_witness_marginal_error": float(marginal_error),
        "triangle_failures": int(triangle_failures),
        "symmetry_failures": int(symmetry_failures),
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    (runtime_dir / "claim_2_independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        raise RuntimeError("Independent Claim 2 checker failed")
    return result

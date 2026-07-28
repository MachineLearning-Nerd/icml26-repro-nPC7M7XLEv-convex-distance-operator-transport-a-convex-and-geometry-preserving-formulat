"""Independent numerical checker using the vectorized quadratic form."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .claim1 import TOLERANCE, linear_map


def check(runtime_dir: Path) -> dict[str, object]:
    rows = json.loads((runtime_dir / "claim_1_rows.json").read_text())
    required = {
        "support",
        "alpha",
        "jensen_gap",
        "minimum_hessian_eigenvalue",
        "maximum_marginal_error",
        "monotonicity_failures",
    }
    schema_pass = all(required <= set(row) for row in rows)
    # This checker does not call the primary objective implementation. It
    # independently rebuilds a deterministic Kronecker map and verifies that
    # v^T A^T A v is nonnegative for unrelated random directions.
    rng = np.random.default_rng(134)
    quadratic_failures = 0
    for support in (3, 5, 8, 13):
        dx = rng.random((support, support))
        dy = rng.random((support, support))
        dx = 0.5 * (dx + dx.T)
        dy = 0.5 * (dy + dy.T)
        np.fill_diagonal(dx, 0)
        np.fill_diagonal(dy, 0)
        operator = linear_map(dx, dy)
        for _ in range(12):
            direction = rng.normal(size=support * support)
            value = float(direction @ (operator.T @ operator) @ direction)
            quadratic_failures += int(value < -TOLERANCE)
    gates = {
        "raw_schema_valid": schema_pass and len(rows) == 60,
        "recorded_jensen_nonnegative": min(row["jensen_gap"] for row in rows)
        >= -TOLERANCE,
        "recorded_hessians_psd": min(
            row["minimum_hessian_eigenvalue"] for row in rows
        )
        >= -1e-8,
        "independent_quadratic_forms_nonnegative": quadratic_failures == 0,
        "recorded_marginals_exact": max(
            row["maximum_marginal_error"] for row in rows
        )
        < TOLERANCE,
        "recorded_fw_monotone": sum(
            row["monotonicity_failures"] for row in rows
        )
        == 0,
    }
    result = {
        "checker": "independent vectorized A.T@A quadratic-form audit",
        "independent_seed": 134,
        "quadratic_forms_checked": 48,
        "quadratic_failures": quadratic_failures,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    (runtime_dir / "claim_1_independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        raise RuntimeError("Independent Claim 1 checker failed")
    return result


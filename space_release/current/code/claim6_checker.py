"""Independent raw-witness checker for Claim 6."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment


def check(runtime_dir: Path) -> dict[str, object]:
    traces = json.loads((runtime_dir / "claim_6_fw_traces.json").read_text())
    witnesses = json.loads(
        (runtime_dir / "claim_6_witnesses.json").read_text()
    )
    schedules = json.loads(
        (runtime_dir / "claim_6_consistency_rows.json").read_text()
    )
    controls = json.loads(
        (runtime_dir / "claim_6_negative_control.json").read_text()
    )
    maximum_gap_disagreement = 0.0
    maximum_marginal_error = 0.0
    schedule_failures = 0
    for trace, witness in zip(traces, witnesses, strict=True):
        dx = np.asarray(witness["dx"], dtype=np.float64)
        dy = np.asarray(witness["dy"], dtype=np.float64)
        cost = np.asarray(witness["cost"], dtype=np.float64)
        coupling = np.asarray(witness["final_coupling"], dtype=np.float64)
        alpha = float(witness["alpha"])
        n = coupling.shape[0]
        residual = (dx / n) @ coupling - coupling @ (dy / n)
        structural_gradient = n * n * (
            (dx / n).T @ residual - residual @ (dy / n).T
        )
        grad = (1.0 - alpha) * cost + alpha * structural_gradient
        rows, columns = linear_sum_assignment(grad)
        atom = np.zeros_like(coupling)
        atom[rows, columns] = 1.0 / n
        recomputed_gap = float(np.sum(grad * (coupling - atom)))
        recorded_gap = float(trace["final_fw_duality_gap"])
        maximum_gap_disagreement = max(
            maximum_gap_disagreement, abs(recomputed_gap - recorded_gap)
        )
        maximum_marginal_error = max(
            maximum_marginal_error,
            float(np.max(np.abs(coupling.sum(axis=0) - 1 / n))),
            float(np.max(np.abs(coupling.sum(axis=1) - 1 / n))),
        )
        expected_bound = 32.0 * alpha * n / (
            int(trace["iterations"]) + 3
        )
        schedule_failures += int(
            abs(
                expected_bound
                - float(trace["final_theorem_optimization_bound"])
            )
            > 1e-14
        )

    valid_grouped: dict[tuple[int, float], list[dict[str, object]]] = {}
    for row in schedules:
        valid_grouped.setdefault(
            (int(row["dimension"]), float(row["alpha"])), []
        ).append(row)
    valid_monotonic_failures = 0
    for rows in valid_grouped.values():
        ordered = sorted(rows, key=lambda row: int(row["n_min"]))
        valid_monotonic_failures += sum(
            float(later["n_min_over_T_n"])
            >= float(earlier["n_min_over_T_n"])
            for earlier, later in zip(ordered, ordered[1:])
        )
    control_ratio_failures = sum(
        abs(float(row["n_min_over_T_n"]) - 1.0) > 1e-15
        for row in controls
    )
    gates = {
        "all_raw_witnesses_recomputed": len(traces) == len(witnesses) == 2,
        "independent_fw_gap_agrees": maximum_gap_disagreement < 1e-10,
        "witness_marginals_exact": maximum_marginal_error < 1e-10,
        "theorem_bound_formula_recomputed": schedule_failures == 0,
        "valid_schedule_ratio_strictly_decreases": valid_monotonic_failures == 0,
        "invalid_control_ratio_stays_one": control_ratio_failures == 0,
    }
    result = {
        "checker": "independent matrix-gradient, assignment, and schedule audit",
        "maximum_fw_gap_disagreement": maximum_gap_disagreement,
        "maximum_witness_marginal_error": maximum_marginal_error,
        "bound_formula_failures": schedule_failures,
        "valid_schedule_monotonic_failures": valid_monotonic_failures,
        "control_ratio_failures": control_ratio_failures,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    (runtime_dir / "claim_6_independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        raise RuntimeError("Independent Claim 6 checker failed")
    return result

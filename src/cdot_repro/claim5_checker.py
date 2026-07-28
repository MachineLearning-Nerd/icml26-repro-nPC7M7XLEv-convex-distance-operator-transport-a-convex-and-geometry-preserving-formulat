"""Independent raw-CV and classification checker for Claim 5."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def check(runtime_dir: Path) -> dict[str, object]:
    primary = json.loads((runtime_dir / "claim_5_result.json").read_text())
    cv = json.loads((runtime_dir / "claim_5_nested_cv_rows.json").read_text())
    controls = json.loads(
        (runtime_dir / "claim_5_permuted_controls.json").read_text()
    )
    maximum_summary_error = 0.0
    fold_shape_failures = 0
    reversed_seeds = 0
    dataset_margins: dict[str, float] = {}
    for dataset in ("MUTAG", "ENZYMES"):
        by_seed: dict[int, dict[str, float]] = {}
        for method in ("CDOT", "FGW"):
            rows = [
                row
                for row in cv
                if row["dataset"] == dataset and row["method"] == method
            ]
            fold_shape_failures += int(
                len(rows) != 30
                or {(row["outer_seed"], row["fold"]) for row in rows}
                != {
                    (seed, fold)
                    for seed in (260727, 260728, 260729)
                    for fold in range(1, 11)
                }
            )
            observed = float(np.mean([row["accuracy"] for row in rows]))
            recorded = float(
                primary["results"][dataset]["summaries"][method][
                    "mean_accuracy"
                ]
            )
            maximum_summary_error = max(
                maximum_summary_error, abs(observed - recorded)
            )
            for seed in (260727, 260728, 260729):
                by_seed.setdefault(seed, {})[method] = float(
                    np.mean(
                        [
                            row["accuracy"]
                            for row in rows
                            if row["outer_seed"] == seed
                        ]
                    )
                )
        if dataset == "ENZYMES":
            reversed_seeds = sum(
                values["CDOT"] < values["FGW"]
                for values in by_seed.values()
            )
        dataset_margins[dataset] = float(
            np.mean(
                [
                    row["accuracy"]
                    for row in cv
                    if row["dataset"] == dataset and row["method"] == "CDOT"
                ]
            )
            - np.mean(
                [
                    row["accuracy"]
                    for row in cv
                    if row["dataset"] == dataset and row["method"] == "FGW"
                ]
            )
        )
    control_cells = {
        (row["dataset"], row["method"], row["outer_seed"], row["fold"])
        for row in controls
    }
    independently_derived_status = (
        "FALSIFIED"
        if reversed_seeds == 3
        else "VERIFIED"
        if all(margin > 0 for margin in dataset_margins.values())
        else "BLOCKED"
    )
    gates = {
        "all_120_nested_cv_rows_present": len(cv) == 120,
        "all_120_control_rows_present": len(controls) == 120,
        "fold_shapes_exact": fold_shape_failures == 0,
        "raw_means_match_primary": maximum_summary_error < 1e-10,
        "all_control_cells_unique": len(control_cells) == 120,
        "primary_status_matches_independent_rule": primary["status"]
        == independently_derived_status,
        "independent_rule_resolves_a_nonblocked_verdict": (
            independently_derived_status != "BLOCKED"
        ),
    }
    result = {
        "checker": "independent fold inventory, raw-mean, and seedwise direction audit",
        "maximum_summary_error": maximum_summary_error,
        "fold_shape_failures": fold_shape_failures,
        "enzymes_reversed_outer_seeds": reversed_seeds,
        "dataset_cdot_minus_fgw_margins": dataset_margins,
        "independently_derived_status": independently_derived_status,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    (runtime_dir / "claim_5_independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        raise RuntimeError("Independent Claim 5 checker failed")
    return result

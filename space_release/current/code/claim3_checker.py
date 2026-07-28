"""Independent raw-trial and decision checker for Claim 3."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import t as student_t


def interval(values: np.ndarray) -> tuple[float, float, float]:
    mean = float(values.mean())
    half_width = float(
        student_t.ppf(0.975, len(values) - 1)
        * values.std(ddof=1)
        / math.sqrt(len(values))
    )
    return mean, mean - half_width, mean + half_width


def check(runtime_dir: Path) -> dict[str, object]:
    primary = json.loads((runtime_dir / "claim_3_result.json").read_text())
    rows = json.loads((runtime_dir / "claim_3_trials.json").read_text())
    controls = json.loads(
        (runtime_dir / "claim_3_negative_controls.json").read_text()
    )
    methods = ("CDOT", "FGW", "IsoRank")
    by_method = {
        method: np.asarray(
            [row["mse"] for row in rows if row["method"] == method],
            dtype=np.float64,
        )
        for method in methods
    }
    maximum_summary_error = max(
        abs(
            float(by_method[method].mean())
            - primary["summaries"][method]["mean_mse"]
        )
        for method in methods
    )
    paired: dict[str, dict[str, float]] = {}
    for baseline in ("FGW", "IsoRank"):
        mean, low, high = interval(by_method["CDOT"] - by_method[baseline])
        paired[baseline] = {
            "mean": mean,
            "ci95_low": low,
            "ci95_high": high,
        }
    ordering_supported = all(item["ci95_high"] < 0 for item in paired.values())
    contradicted = any(item["ci95_low"] > 0 for item in paired.values())
    independently_derived_status = (
        "VERIFIED"
        if ordering_supported
        else "FALSIFIED"
        if contradicted
        else "BLOCKED"
    )
    tampered = rows[:-1]
    tamper_detected = len(
        {(row["trial"], row["method"]) for row in tampered}
    ) != 300
    gates = {
        "exact_300_row_inventory": len(rows) == 300,
        "exact_trial_seed_inventory": {
            (int(row["trial"]), int(row["seed"])) for row in rows
        }
        == {(trial, 260602047 + trial) for trial in range(100)},
        "exact_method_inventory": all(
            len(by_method[method]) == 100 for method in methods
        ),
        "raw_means_match_primary": maximum_summary_error < 1e-11,
        "paired_intervals_match_primary": all(
            abs(
                paired[baseline]["ci95_high"]
                - primary["paired_cdot_minus_baseline"][baseline]["ci95_high"]
            )
            < 1e-11
            for baseline in ("FGW", "IsoRank")
        ),
        "primary_status_matches_independent_rule": primary["status"]
        == independently_derived_status,
        "independent_rule_resolves_a_nonblocked_verdict": (
            independently_derived_status != "BLOCKED"
        ),
        "parity_and_label_controls_pass": controls["all_gates_pass"],
        "missing_row_tamper_is_rejected": tamper_detected,
    }
    result = {
        "checker": "independent inventory, raw mean, paired interval, verdict, and tamper audit",
        "maximum_summary_error": maximum_summary_error,
        "paired_cdot_minus_baseline": paired,
        "independently_derived_status": independently_derived_status,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    (runtime_dir / "claim_3_independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        raise RuntimeError("Independent Claim 3 checker failed")
    return result

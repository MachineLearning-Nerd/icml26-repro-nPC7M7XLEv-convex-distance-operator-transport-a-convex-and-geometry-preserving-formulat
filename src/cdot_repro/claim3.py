"""Paper-scale CPU reproduction of the synthetic Table-2 comparison."""

from __future__ import annotations

import json
import math
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import ot
import torch
from scipy.optimize import linear_sum_assignment
from scipy.stats import t as student_t
from threadpoolctl import threadpool_limits


BASE_SEED = 260602047
PER_CLUSTER = 500
TRIALS = 100
ITERATIONS = 200
ALPHA = 0.5
WORKERS = 4
THREADS_PER_WORKER = 16
METHODS = ("CDOT", "FGW", "IsoRank")
PAPER_VALUES = {"CDOT": 0.0016, "FGW": 0.0034, "IsoRank": 0.0033}
_THREAD_LIMITER = None


def stable(value: float) -> float:
    return round(float(value), 12)


def initialize_worker() -> None:
    global _THREAD_LIMITER
    _THREAD_LIMITER = threadpool_limits(limits=THREADS_PER_WORKER)
    torch.set_num_threads(THREADS_PER_WORKER)
    torch.set_num_interop_threads(1)


def generate_trial(
    per_cluster: int, seed: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    offsets = np.asarray(
        ((0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)),
        dtype=np.float64,
    )
    xs: list[np.ndarray] = []
    ys: list[np.ndarray] = []
    labels: list[np.ndarray] = []
    for label, offset in enumerate(offsets):
        xs.append(rng.random((per_cluster, 2)) + offset)
        ys.append(rng.random((per_cluster, 2)) + offset)
        labels.append(np.full(per_cluster, label, dtype=np.int64))
    joined = np.concatenate(labels)
    return np.vstack(xs), np.vstack(ys), joined, joined.copy()


def normalized_distance(points: np.ndarray) -> torch.Tensor:
    tensor = torch.from_numpy(points)
    distance = torch.cdist(tensor, tensor)
    maximum = torch.max(distance)
    if float(maximum) <= 0:
        raise ValueError("degenerate point cloud")
    return distance / maximum


def feature_cost(
    source_labels: np.ndarray, target_labels: np.ndarray
) -> torch.Tensor:
    return torch.from_numpy(
        (source_labels[:, None] != target_labels[None, :]).astype(np.float64)
    )


def barycentric_mse(
    source: np.ndarray, transported: torch.Tensor
) -> float:
    source_tensor = torch.from_numpy(source)
    return float(
        torch.mean(torch.sum((source_tensor - transported) ** 2, dim=1))
    )


def initial_state(
    distance_x: torch.Tensor,
    distance_y: torch.Tensor,
    cost: torch.Tensor,
    alpha: float,
) -> tuple[torch.Tensor, torch.Tensor, float, float]:
    n = cost.shape[0]
    ax = distance_x.sum(dim=1)
    by = distance_y.sum(dim=0)
    residual = (ax[:, None] - by[None, :]) / (n * n)
    a_residual = (
        (distance_x @ ax)[:, None] - ax[:, None] * by[None, :]
    ) / (n * n)
    residual_b = (
        ax[:, None] * by[None, :]
        - (by @ distance_y)[None, :]
    ) / (n * n)
    gradient = (1.0 - alpha) * cost + alpha * n * n * (
        a_residual - residual_b
    )
    feature_value = float(cost.mean())
    objective = float(
        (1.0 - alpha) * feature_value
        + 0.5 * alpha * n * n * torch.sum(residual * residual)
    )
    return residual, gradient, feature_value, objective


def cdot_lazy(
    source: np.ndarray,
    target: np.ndarray,
    distance_x_raw: torch.Tensor,
    distance_y_raw: torch.Tensor,
    cost: torch.Tensor,
    iterations: int,
    alpha: float,
) -> tuple[float, dict[str, object]]:
    n = cost.shape[0]
    distance_x = distance_x_raw / n
    distance_y = distance_y_raw / n
    residual, gradient, feature_value, previous = initial_state(
        distance_x, distance_y, cost, alpha
    )
    distance_x_squared = distance_x @ distance_x
    distance_y_squared = distance_y @ distance_y
    target_tensor = torch.from_numpy(target)
    transported = target_tensor.mean(dim=0).expand(n, -1).clone()
    nonmonotone = boundary = 0
    mass_coefficient = 1.0
    final_gap = math.inf
    for iteration in range(iterations):
        rows, permutation_np = linear_sum_assignment(gradient.numpy())
        if not np.array_equal(rows, np.arange(n)):
            raise RuntimeError("unexpected LAP row ordering")
        permutation = torch.from_numpy(permutation_np.astype(np.int64))
        inverse = torch.empty_like(permutation)
        inverse[permutation] = torch.arange(n)
        atom_residual = (
            distance_x[:, inverse] - distance_y[permutation, :]
        ) / n
        residual_direction = atom_residual - residual
        atom_feature = float(
            cost[torch.arange(n), permutation].sum() / n
        )
        linear = float(
            (1.0 - alpha) * (atom_feature - feature_value)
            + alpha * n * n * torch.sum(residual * residual_direction)
        )
        quadratic = float(
            0.5
            * alpha
            * n
            * n
            * torch.sum(residual_direction * residual_direction)
        )
        final_gap = max(0.0, -linear)
        if quadratic > 1e-24:
            step = float(np.clip(-linear / (2.0 * quadratic), 0.0, 1.0))
        else:
            step = float(linear < 0)
        boundary += int(step <= 1e-14 or step >= 1.0 - 1e-14)
        residual = residual + step * residual_direction
        feature_value = (1.0 - step) * feature_value + step * atom_feature
        transported = (
            (1.0 - step) * transported + step * target_tensor[permutation]
        )
        current = float(
            (1.0 - alpha) * feature_value
            + 0.5 * alpha * n * n * torch.sum(residual * residual)
        )
        nonmonotone += int(current > previous + 2e-9)
        previous = current
        mass_coefficient = (1.0 - step) * mass_coefficient + step
        if iteration < iterations - 1:
            cross = distance_x[:, inverse] @ distance_y
            atom_gradient = (1.0 - alpha) * cost + alpha * n * n * (
                distance_x_squared[:, inverse] / n
                - 2.0 * cross / n
                + distance_y_squared[permutation, :] / n
            )
            gradient = (1.0 - step) * gradient + step * atom_gradient
    return barycentric_mse(source, transported), {
        "iterations": iterations,
        "final_objective": stable(previous),
        "final_fw_gap": stable(final_gap),
        "nonmonotone_steps": nonmonotone,
        "boundary_steps": boundary,
        "marginal_error_certificate": stable(
            abs(mass_coefficient - 1.0) / n
        ),
        "solver": "Algorithm-2 affine lazy gradient, exact LAP and quadratic line search",
    }


def cdot_standard_small(
    source: np.ndarray,
    target: np.ndarray,
    distance_x_raw: torch.Tensor,
    distance_y_raw: torch.Tensor,
    cost: torch.Tensor,
    iterations: int,
    alpha: float,
) -> tuple[float, float]:
    n = cost.shape[0]
    distance_x = distance_x_raw / n
    distance_y = distance_y_raw / n
    coupling = torch.full_like(cost, 1.0 / (n * n))
    previous = math.inf
    for _ in range(iterations):
        residual = distance_x @ coupling - coupling @ distance_y
        gradient = (1.0 - alpha) * cost + alpha * n * n * (
            distance_x @ residual - residual @ distance_y
        )
        rows, permutation_np = linear_sum_assignment(gradient.numpy())
        permutation = torch.from_numpy(permutation_np.astype(np.int64))
        atom = torch.zeros_like(coupling)
        atom[torch.from_numpy(rows), permutation] = 1.0 / n
        direction = atom - coupling
        residual_direction = (
            distance_x @ direction - direction @ distance_y
        )
        linear = float(
            (1.0 - alpha) * torch.sum(cost * direction)
            + alpha * n * n * torch.sum(residual * residual_direction)
        )
        quadratic = float(
            0.5
            * alpha
            * n
            * n
            * torch.sum(residual_direction * residual_direction)
        )
        step = (
            float(np.clip(-linear / (2.0 * quadratic), 0.0, 1.0))
            if quadratic > 1e-24
            else float(linear < 0)
        )
        coupling += step * direction
        residual += step * residual_direction
        previous = float(
            (1.0 - alpha) * torch.sum(cost * coupling)
            + 0.5 * alpha * n * n * torch.sum(residual * residual)
        )
    transported = n * (coupling @ torch.from_numpy(target))
    return barycentric_mse(source, transported), previous


def fgw(
    source: np.ndarray,
    target: np.ndarray,
    distance_x: torch.Tensor,
    distance_y: torch.Tensor,
    cost: torch.Tensor,
    iterations: int,
    alpha: float,
) -> tuple[float, dict[str, object]]:
    n = cost.shape[0]
    weights = np.full(n, 1.0 / n)
    coupling, log = ot.gromov.fused_gromov_wasserstein(
        cost.numpy(),
        distance_x.numpy(),
        distance_y.numpy(),
        weights,
        weights,
        loss_fun="square_loss",
        alpha=alpha,
        armijo=False,
        G0=np.outer(weights, weights),
        max_iter=iterations,
        tol_rel=1e-9,
        tol_abs=1e-9,
        log=True,
    )
    losses = np.asarray(log.get("loss", []), dtype=np.float64)
    transported = n * coupling @ target
    marginal = max(
        float(np.max(np.abs(coupling.sum(axis=0) - weights))),
        float(np.max(np.abs(coupling.sum(axis=1) - weights))),
    )
    return float(np.mean(np.sum((source - transported) ** 2, axis=1))), {
        "iterations": max(0, len(losses) - 1),
        "final_objective": stable(losses[-1]),
        "nonmonotone_steps": int(
            np.sum(losses[1:] > losses[:-1] + 2e-9)
        ),
        "marginal_error": stable(marginal),
        "solver": "POT fused_gromov_wasserstein default conditional gradient",
    }


def isorank(
    source: np.ndarray,
    target: np.ndarray,
    distance_x: torch.Tensor,
    distance_y: torch.Tensor,
    source_labels: np.ndarray,
    target_labels: np.ndarray,
    iterations: int,
    damping: float,
) -> tuple[float, dict[str, object]]:
    affinity_x = torch.exp(-0.5 * distance_x * distance_x)
    affinity_y = torch.exp(-0.5 * distance_y * distance_y)
    affinity_x /= affinity_x.sum(dim=1, keepdim=True)
    affinity_y /= affinity_y.sum(dim=1, keepdim=True)
    categories = sorted(set(source_labels) | set(target_labels))
    source_onehot = torch.from_numpy(
        np.column_stack([source_labels == label for label in categories])
        .astype(np.float64)
    )
    target_onehot = torch.from_numpy(
        np.column_stack([target_labels == label for label in categories])
        .astype(np.float64)
    )
    target_counts = target_onehot.sum(dim=0)
    if torch.any(target_counts == 0):
        raise ValueError("IsoRank prior has an empty target feature class")
    left = source_onehot
    right = target_onehot / target_counts
    left_blocks: list[torch.Tensor] = []
    right_blocks: list[torch.Tensor] = []
    coefficient = 1.0
    for _ in range(iterations):
        weight = (1.0 - damping) * coefficient
        root = math.sqrt(weight)
        left_blocks.append(root * left)
        right_blocks.append(root * right)
        left = affinity_x @ left
        right = affinity_y @ right
        coefficient *= damping
    root = math.sqrt(coefficient)
    left_blocks.append(root * left)
    right_blocks.append(root * right)
    similarity = torch.cat(left_blocks, dim=1) @ torch.cat(
        right_blocks, dim=1
    ).T
    rows, permutation = linear_sum_assignment(-similarity.numpy())
    if not np.array_equal(rows, np.arange(len(source))):
        raise RuntimeError("unexpected IsoRank LAP row ordering")
    transported = target[permutation]
    return float(np.mean(np.sum((source - transported) ** 2, axis=1))), {
        "iterations": iterations,
        "fixed_point_residual_upper_bound": stable(
            2.0 * damping**iterations
        ),
        "marginal_error": 0.0,
        "solver": "exact low-rank evaluation of the stated IsoRank recurrence plus LAP",
    }


def run_trial(trial: int) -> list[dict[str, object]]:
    seed = BASE_SEED + trial
    source, target, source_labels, target_labels = generate_trial(
        PER_CLUSTER, seed
    )
    distance_x = normalized_distance(source)
    distance_y = normalized_distance(target)
    cost = feature_cost(source_labels, target_labels)
    results: list[dict[str, object]] = []
    cdot_mse, cdot_diagnostics = cdot_lazy(
        source,
        target,
        distance_x,
        distance_y,
        cost,
        ITERATIONS,
        ALPHA,
    )
    results.append(
        {
            "trial": trial,
            "seed": seed,
            "method": "CDOT",
            "mse": stable(cdot_mse),
            **cdot_diagnostics,
        }
    )
    fgw_mse, fgw_diagnostics = fgw(
        source,
        target,
        distance_x,
        distance_y,
        cost,
        ITERATIONS,
        ALPHA,
    )
    results.append(
        {
            "trial": trial,
            "seed": seed,
            "method": "FGW",
            "mse": stable(fgw_mse),
            **fgw_diagnostics,
        }
    )
    isorank_mse, isorank_diagnostics = isorank(
        source,
        target,
        distance_x,
        distance_y,
        source_labels,
        target_labels,
        ITERATIONS,
        ALPHA,
    )
    results.append(
        {
            "trial": trial,
            "seed": seed,
            "method": "IsoRank",
            "mse": stable(isorank_mse),
            **isorank_diagnostics,
        }
    )
    return results


def summarize(values: np.ndarray) -> dict[str, float | int]:
    standard_deviation = float(values.std(ddof=1))
    half_width = float(
        student_t.ppf(0.975, len(values) - 1)
        * standard_deviation
        / math.sqrt(len(values))
    )
    return {
        "trials": len(values),
        "mean_mse": stable(values.mean()),
        "sample_std_mse": stable(standard_deviation),
        "ci95_low": stable(values.mean() - half_width),
        "ci95_high": stable(values.mean() + half_width),
    }


def paired_summary(
    cdot_values: np.ndarray, baseline_values: np.ndarray
) -> dict[str, float]:
    differences = cdot_values - baseline_values
    standard_deviation = float(differences.std(ddof=1))
    half_width = float(
        student_t.ppf(0.975, len(differences) - 1)
        * standard_deviation
        / math.sqrt(len(differences))
    )
    return {
        "mean_cdot_minus_baseline": stable(differences.mean()),
        "ci95_low": stable(differences.mean() - half_width),
        "ci95_high": stable(differences.mean() + half_width),
    }


def parity_and_controls() -> dict[str, object]:
    source, target, labels_x, labels_y = generate_trial(10, BASE_SEED - 1)
    distance_x = normalized_distance(source)
    distance_y = normalized_distance(target)
    cost = feature_cost(labels_x, labels_y)
    lazy_mse, lazy_diagnostics = cdot_lazy(
        source, target, distance_x, distance_y, cost, 20, ALPHA
    )
    standard_mse, standard_objective = cdot_standard_small(
        source, target, distance_x, distance_y, cost, 20, ALPHA
    )
    dense_affinity_x = torch.exp(-0.5 * distance_x * distance_x)
    dense_affinity_y = torch.exp(-0.5 * distance_y * distance_y)
    dense_affinity_x /= dense_affinity_x.sum(dim=1, keepdim=True)
    dense_affinity_y /= dense_affinity_y.sum(dim=1, keepdim=True)
    dense_prior = 1.0 - feature_cost(labels_x, labels_y)
    dense_prior /= dense_prior.sum(dim=1, keepdim=True)
    dense_similarity = dense_prior.clone()
    for _ in range(20):
        dense_similarity = (
            ALPHA
            * dense_affinity_x
            @ dense_similarity
            @ dense_affinity_y.T
            + (1.0 - ALPHA) * dense_prior
        )
    _, low_rank_diag = isorank(
        source,
        target,
        distance_x,
        distance_y,
        labels_x,
        labels_y,
        20,
        ALPHA,
    )
    categories = sorted(set(labels_x))
    left = torch.from_numpy(
        np.column_stack([labels_x == label for label in categories]).astype(
            np.float64
        )
    )
    right = torch.from_numpy(
        np.column_stack([labels_y == label for label in categories]).astype(
            np.float64
        )
    )
    right /= right.sum(dim=0)
    blocks_x: list[torch.Tensor] = []
    blocks_y: list[torch.Tensor] = []
    coefficient = 1.0
    for _ in range(20):
        root = math.sqrt((1.0 - ALPHA) * coefficient)
        blocks_x.append(root * left)
        blocks_y.append(root * right)
        left = dense_affinity_x @ left
        right = dense_affinity_y @ right
        coefficient *= ALPHA
    blocks_x.append(math.sqrt(coefficient) * left)
    blocks_y.append(math.sqrt(coefficient) * right)
    low_rank_similarity = torch.cat(blocks_x, dim=1) @ torch.cat(
        blocks_y, dim=1
    ).T
    permuted_labels = np.roll(labels_y, 10)
    permuted_cost = feature_cost(labels_x, permuted_labels)
    normal_mse, _ = cdot_lazy(
        source, target, distance_x, distance_y, cost, 50, ALPHA
    )
    permuted_mse, _ = cdot_lazy(
        source,
        target,
        distance_x,
        distance_y,
        permuted_cost,
        50,
        ALPHA,
    )
    gates = {
        "lazy_standard_objective_match": abs(
            float(lazy_diagnostics["final_objective"])
            - standard_objective
        )
        < 1e-9,
        "lazy_standard_mse_match": abs(lazy_mse - standard_mse) < 1e-9,
        "low_rank_dense_isorank_match": float(
            torch.max(torch.abs(low_rank_similarity - dense_similarity))
        )
        < 1e-10,
        "wrong_feature_control_degrades_mse": permuted_mse > normal_mse + 0.1,
        "low_rank_residual_bound_finite": math.isfinite(
            float(low_rank_diag["fixed_point_residual_upper_bound"])
        ),
    }
    return {
        "lazy_standard_objective_abs_error": stable(
            abs(
                float(lazy_diagnostics["final_objective"])
                - standard_objective
            )
        ),
        "lazy_standard_mse_abs_error": stable(abs(lazy_mse - standard_mse)),
        "low_rank_dense_isorank_max_abs_error": stable(
            torch.max(torch.abs(low_rank_similarity - dense_similarity))
        ),
        "normal_feature_mse": stable(normal_mse),
        "wrong_feature_mse": stable(permuted_mse),
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }


def run(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    controls = parity_and_controls()
    rows: list[dict[str, object]] = []
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(
        max_workers=WORKERS,
        mp_context=context,
        initializer=initialize_worker,
    ) as executor:
        for completed, trial_rows in enumerate(
            executor.map(run_trial, range(TRIALS)), 1
        ):
            rows.extend(trial_rows)
            print(
                json.dumps(
                    {"claim_3_completed_trials": completed, "trials": TRIALS}
                ),
                flush=True,
            )
    by_method = {
        method: np.asarray(
            [row["mse"] for row in rows if row["method"] == method],
            dtype=np.float64,
        )
        for method in METHODS
    }
    summaries = {
        method: {
            **summarize(values),
            "paper_mean_mse": PAPER_VALUES[method],
            "absolute_mean_difference_from_paper": stable(
                abs(values.mean() - PAPER_VALUES[method])
            ),
        }
        for method, values in by_method.items()
    }
    paired = {
        baseline: paired_summary(by_method["CDOT"], by_method[baseline])
        for baseline in ("FGW", "IsoRank")
    }
    ordering_supported = all(
        comparison["ci95_high"] < 0 for comparison in paired.values()
    )
    integrity_gates = {
        "paper_scale_n500_per_region": PER_CLUSTER == 500,
        "paper_total_N2000": PER_CLUSTER * 4 == 2000,
        "paper_100_trials": TRIALS == 100,
        "paper_alpha_half": ALPHA == 0.5,
        "paper_T200": ITERATIONS == 200,
        "all_300_method_rows_present": len(rows) == 300,
        "every_trial_method_cell_unique": len(
            {(row["trial"], row["method"]) for row in rows}
        )
        == 300,
        "all_mse_finite_nonnegative": all(
            math.isfinite(float(row["mse"])) and float(row["mse"]) >= 0
            for row in rows
        ),
        "all_cdot_marginals_certified": max(
            float(row["marginal_error_certificate"])
            for row in rows
            if row["method"] == "CDOT"
        )
        < 1e-10,
        "all_fgw_marginals_preserved": max(
            float(row["marginal_error"])
            for row in rows
            if row["method"] == "FGW"
        )
        < 1e-8,
        "cdot_optimization_monotone": all(
            int(row["nonmonotone_steps"]) == 0
            for row in rows
            if row["method"] == "CDOT"
        ),
        "fgw_optimization_monotone": all(
            int(row["nonmonotone_steps"]) == 0
            for row in rows
            if row["method"] == "FGW"
        ),
        "parity_and_negative_controls_pass": controls["all_gates_pass"],
    }
    status = (
        "VERIFIED"
        if all(integrity_gates.values()) and ordering_supported
        else "FALSIFIED"
        if all(integrity_gates.values())
        and any(comparison["ci95_low"] > 0 for comparison in paired.values())
        else "BLOCKED"
    )
    result = {
        "claim": 3,
        "status": status,
        "claim_contract": {
            "primary_test": "At n=500 per region (N=2000), the 100-trial CDOT mean MSE is below both FGW and IsoRank at alpha=0.5 and T=200.",
            "ordering_acceptance": "upper endpoint of each paired two-sided 95% t interval for CDOT-minus-baseline is below zero",
            "exact_value_audit": "paper and rerun means are reported separately; ordering support is not represented as exact displayed-value agreement",
        },
        "protocol": {
            "per_cluster_n": PER_CLUSTER,
            "total_N": 4 * PER_CLUSTER,
            "trials": TRIALS,
            "iterations": ITERATIONS,
            "alpha": ALPHA,
            "distance_normalization": "each Euclidean distance matrix divided by its maximum",
            "feature_cost": "0/1 region-label mismatch",
            "mse": "sample mean squared Euclidean error between X and N*pi@Y",
            "seed_policy": f"NumPy PCG64 seeds {BASE_SEED}..{BASE_SEED + TRIALS - 1}",
            "workers": WORKERS,
            "threads_per_worker": THREADS_PER_WORKER,
        },
        "source_table_2": {
            "trials": 100,
            "CDOT": {"mean_mse": 0.0016, "displayed_std": 0.00},
            "FGW": {"mean_mse": 0.0034, "displayed_std": 0.00},
            "IsoRank": {"mean_mse": 0.0033, "displayed_std": 0.00},
        },
        "summaries": summaries,
        "paired_cdot_minus_baseline": paired,
        "paper_ordering_supported": ordering_supported,
        "controls": controls,
        "gates": integrity_gates,
        "all_gates_pass": all(integrity_gates.values()),
        "disclosed_deviations": [
            "The paper publishes neither code nor random seeds; deterministic independent seeds are registered here.",
            "The paper leaves the CDOT empirical step-size policy unspecified; exact quadratic line search is used and checked against standard FW.",
            "The paper does not specify a CDOT initial coupling; the independent product coupling is used.",
            "POT's disclosed conditional-gradient stopping rule may converge before the maximum T=200 iterations.",
            "The low-rank IsoRank recurrence is algebraically equivalent to the stated dense recurrence and is parity-checked before use.",
        ],
    }
    (output / "claim_3_trials.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8"
    )
    (output / "claim_3_negative_controls.json").write_text(
        json.dumps(controls, indent=2) + "\n", encoding="utf-8"
    )
    (output / "claim_3_result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        failed = [
            name for name, passed in integrity_gates.items() if not passed
        ]
        raise RuntimeError("Claim 3 integrity gates failed: " + ", ".join(failed))
    return result

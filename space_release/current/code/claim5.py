"""Full TUDataset Table-4 reproduction for Claim 5."""

from __future__ import annotations

import hashlib
import json
import zipfile
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import ot
from scipy.sparse.csgraph import shortest_path
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC

from .claim4 import download


DATA = {
    "MUTAG": {
        "url": "https://www.chrsmrrs.com/graphkerneldatasets/MUTAG.zip",
        "sha256": "c419bdc853c367d2d83da4973c45100954ae15e10f5ae2cddde6ca431f8207f6",
        "graphs": 188,
        "nodes": 3371,
    },
    "ENZYMES": {
        "url": "https://www.chrsmrrs.com/graphkerneldatasets/ENZYMES.zip",
        "sha256": "13d832eb6ffa084192daf6e5750250028a18437ee692c38d29a10cd60e18aaf4",
        "graphs": 600,
        "nodes": 19580,
    },
}
ALPHAS = (0.0, 0.25, 0.5, 0.75, 1.0)
OUTER_SEEDS = (260727, 260728, 260729)
C_GRID = (0.1, 1.0, 10.0, 100.0)
GAMMA_GRID = (0.001, 0.01, 0.1, 1.0, 10.0)
MAX_ITER = 200
WORKERS = 8


@dataclass(frozen=True)
class Graph:
    distance: np.ndarray
    features: np.ndarray
    label: int


def stable(value: float) -> float:
    return round(float(value), 10)


def read_numbers(path: Path, dtype: type = float, delimiter: str | None = None) -> np.ndarray:
    return np.loadtxt(path, dtype=dtype, delimiter=delimiter)


def load_tu(root: Path, name: str) -> tuple[list[Graph], dict[str, object]]:
    indicator = read_numbers(root / f"{name}_graph_indicator.txt", int)
    graph_labels = read_numbers(root / f"{name}_graph_labels.txt", int)
    edges = read_numbers(root / f"{name}_A.txt", int, ",") - 1
    attribute_path = root / f"{name}_node_attributes.txt"
    label_path = root / f"{name}_node_labels.txt"
    if attribute_path.exists():
        raw = np.atleast_2d(read_numbers(attribute_path, float, ","))
        if raw.shape[0] != len(indicator):
            raw = raw.T
        scale = raw.std(axis=0)
        scale[scale < 1e-12] = 1.0
        node_features = (raw - raw.mean(axis=0)) / scale
        feature_kind = "provided attributes, dataset-wise z-scored"
    elif label_path.exists():
        labels = read_numbers(label_path, int)
        categories = sorted(set(int(value) for value in labels))
        lookup = {value: index for index, value in enumerate(categories)}
        node_features = np.eye(len(categories))[
            [lookup[int(value)] for value in labels]
        ]
        feature_kind = "provided categorical labels, one-hot encoded"
    else:
        raise ValueError(f"{name}: no supplied node information")
    graphs: list[Graph] = []
    disconnected = 0
    for graph_id in range(1, len(graph_labels) + 1):
        global_nodes = np.where(indicator == graph_id)[0]
        local = {int(node): index for index, node in enumerate(global_nodes)}
        adjacency = np.zeros((len(global_nodes), len(global_nodes)))
        for source, target in edges:
            if int(source) in local and int(target) in local:
                i, j = local[int(source)], local[int(target)]
                adjacency[i, j] = adjacency[j, i] = 1.0
        distance = shortest_path(adjacency, directed=False, unweighted=True)
        finite = np.isfinite(distance)
        if not np.all(finite):
            disconnected += 1
            fill = float(np.max(distance[finite])) if np.any(finite) else 1.0
            distance[~finite] = fill
        maximum = float(distance.max())
        if maximum:
            distance /= maximum
        graphs.append(
            Graph(
                np.asarray(distance, dtype=np.float64),
                np.asarray(node_features[global_nodes], dtype=np.float64),
                int(graph_labels[graph_id - 1]),
            )
        )
    counts = [len(graph.distance) for graph in graphs]
    return graphs, {
        "graphs": len(graphs),
        "nodes": int(len(indicator)),
        "node_count_min": min(counts),
        "node_count_max": max(counts),
        "node_count_mean": stable(np.mean(counts)),
        "classes": sorted(set(int(value) for value in graph_labels)),
        "feature_kind": feature_kind,
        "disconnected_graphs_filled_with_finite_diameter": disconnected,
    }


def feature_cost(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    cost = np.sum((x[:, None, :] - y[None, :, :]) ** 2, axis=2)
    maximum = float(cost.max())
    return cost / maximum if maximum else cost


def cdot_objective(
    dx: np.ndarray,
    dy: np.ndarray,
    cost: np.ndarray,
    coupling: np.ndarray,
    alpha: float,
) -> float:
    n, m = coupling.shape
    residual = (dx / n) @ coupling - coupling @ (dy / m)
    return float(
        (1.0 - alpha) * np.sum(cost * coupling)
        + 0.5 * alpha * n * m * np.sum(residual * residual)
    )


def cdot_distance(
    dx: np.ndarray, dy: np.ndarray, cost: np.ndarray, alpha: float
) -> tuple[float, dict[str, object]]:
    n, m = cost.shape
    a, b = np.full(n, 1 / n), np.full(m, 1 / m)
    coupling = np.outer(a, b)
    dxn, dyn = dx / n, dy / m
    residual = dxn @ coupling - coupling @ dyn
    start = previous = cdot_objective(dx, dy, cost, coupling, alpha)
    nonmonotone = stationary = 0
    iterations = 0
    for iteration in range(MAX_ITER):
        gradient = (1.0 - alpha) * cost + alpha * n * m * (
            dxn.T @ residual - residual @ dyn.T
        )
        atom = ot.emd(a, b, gradient, numItermax=100000)
        direction = atom - coupling
        residual_direction = dxn @ direction - direction @ dyn
        linear = float(
            (1.0 - alpha) * np.sum(cost * direction)
            + alpha * n * m * np.sum(residual * residual_direction)
        )
        quadratic = float(
            0.5 * alpha * n * m * np.sum(residual_direction**2)
        )
        if quadratic > 1e-20:
            step = float(np.clip(-linear / (2 * quadratic), 0.0, 1.0))
        else:
            step = float(linear < 0)
        coupling += step * direction
        residual += step * residual_direction
        current = cdot_objective(dx, dy, cost, coupling, alpha)
        nonmonotone += int(current > previous + 1e-9)
        improvement = previous - current
        stationary = (
            stationary + 1
            if improvement <= 1e-11 * max(1.0, abs(previous))
            else 0
        )
        previous = current
        iterations = iteration + 1
        if iteration >= 9 and stationary >= 5:
            break
    marginal = max(
        float(np.max(np.abs(coupling.sum(axis=1) - a))),
        float(np.max(np.abs(coupling.sum(axis=0) - b))),
    )
    return float(np.sqrt(max(previous, 0.0))), {
        "iterations": iterations,
        "start": start,
        "final": previous,
        "nonmonotone": nonmonotone,
        "marginal_error": marginal,
    }


def fgw_distance(
    dx: np.ndarray, dy: np.ndarray, cost: np.ndarray, alpha: float
) -> tuple[float, dict[str, object]]:
    n, m = cost.shape
    a, b = np.full(n, 1 / n), np.full(m, 1 / m)
    value, log = ot.gromov.fused_gromov_wasserstein2(
        cost,
        dx,
        dy,
        a,
        b,
        loss_fun="square_loss",
        alpha=alpha,
        armijo=False,
        max_iter=MAX_ITER,
        tol_rel=1e-9,
        tol_abs=1e-9,
        log=True,
    )
    losses = [float(item) for item in log.get("loss", [])]
    return float(np.sqrt(max(float(value), 0.0))), {
        "iterations": max(0, len(losses) - 1),
        "start": losses[0] if losses else None,
        "final": float(value),
        "nonmonotone": sum(
            later > earlier + 1e-8
            for earlier, later in zip(losses, losses[1:])
        ),
        "marginal_error": None,
    }


_GRAPHS: list[Graph] = []


def initialize_worker(graphs: list[Graph]) -> None:
    global _GRAPHS
    _GRAPHS = graphs


def pair_task(pair: tuple[int, int]) -> dict[str, object]:
    i, j = pair
    x, y = _GRAPHS[i], _GRAPHS[j]
    cost = feature_cost(x.features, y.features)
    row: dict[str, object] = {"left": i, "right": j}
    for alpha in ALPHAS:
        slug = f"a{int(round(alpha * 100)):03d}"
        cdot_value, cdot_diag = cdot_distance(
            x.distance, y.distance, cost, alpha
        )
        if alpha == 0.0:
            fgw_value, fgw_diag = cdot_value, dict(cdot_diag)
        else:
            fgw_value, fgw_diag = fgw_distance(
                x.distance, y.distance, cost, alpha
            )
        row[f"CDOT_{slug}"] = stable(cdot_value)
        row[f"FGW_{slug}"] = stable(fgw_value)
        for method, diag in (("cdot", cdot_diag), ("fgw", fgw_diag)):
            row[f"{method}_{slug}_iterations"] = diag["iterations"]
            row[f"{method}_{slug}_nonmonotone"] = diag["nonmonotone"]
            row[f"{method}_{slug}_marginal_error"] = diag["marginal_error"]
    return row


def chunk_task(pairs: list[tuple[int, int]]) -> list[dict[str, object]]:
    return [pair_task(pair) for pair in pairs]


def matrix_hash(matrix: np.ndarray) -> str:
    return hashlib.sha256(
        np.asarray(matrix, dtype="<f8", order="C").tobytes()
    ).hexdigest()


def pairwise_distances(
    graphs: list[Graph],
) -> tuple[dict[str, np.ndarray], dict[str, object], list[dict[str, object]]]:
    pairs = [
        (i, j) for i in range(len(graphs)) for j in range(i + 1, len(graphs))
    ]
    matrices = {
        f"{method}_a{int(round(alpha * 100)):03d}": np.zeros(
            (len(graphs), len(graphs)), dtype=np.float64
        )
        for method in ("CDOT", "FGW")
        for alpha in ALPHAS
    }
    selected_indices = set(
        np.linspace(0, len(pairs) - 1, num=20, dtype=int).tolist()
    )
    selected_rows: list[dict[str, object]] = []
    maximum_marginal = 0.0
    cdot_nonmonotone = fgw_nonmonotone = 0
    iteration_totals = {"CDOT": 0, "FGW": 0}
    chunks = [pairs[start : start + 64] for start in range(0, len(pairs), 64)]
    completed = 0
    with ProcessPoolExecutor(
        max_workers=WORKERS,
        initializer=initialize_worker,
        initargs=(graphs,),
    ) as executor:
        for chunk_rows in executor.map(chunk_task, chunks):
            for row in chunk_rows:
                pair_index = completed
                i, j = int(row["left"]), int(row["right"])
                for alpha in ALPHAS:
                    slug = f"a{int(round(alpha * 100)):03d}"
                    for method in ("CDOT", "FGW"):
                        value = float(row[f"{method}_{slug}"])
                        matrices[f"{method}_{slug}"][i, j] = value
                        matrices[f"{method}_{slug}"][j, i] = value
                        iteration_totals[method] += int(
                            row[f"{method.lower()}_{slug}_iterations"]
                        )
                    maximum_marginal = max(
                        maximum_marginal,
                        float(row[f"cdot_{slug}_marginal_error"]),
                    )
                    cdot_nonmonotone += int(
                        row[f"cdot_{slug}_nonmonotone"]
                    )
                    fgw_nonmonotone += int(
                        row[f"fgw_{slug}_nonmonotone"]
                    )
                if pair_index in selected_indices:
                    selected_rows.append(row)
                completed += 1
            if completed % 1024 < len(chunk_rows) or completed == len(pairs):
                print(
                    json.dumps(
                        {"completed_pairs": completed, "pairs": len(pairs)}
                    ),
                    flush=True,
                )
    finite_symmetric = all(
        np.isfinite(matrix).all()
        and np.max(np.abs(matrix - matrix.T)) == 0
        and np.max(np.abs(np.diag(matrix))) == 0
        for matrix in matrices.values()
    )
    diagnostics = {
        "pairs": len(pairs),
        "pair_alpha_method_cells": len(pairs) * len(ALPHAS) * 2,
        "maximum_cdot_marginal_error": maximum_marginal,
        "cdot_nonmonotone_steps": cdot_nonmonotone,
        "fgw_nonmonotone_steps": fgw_nonmonotone,
        "mean_iterations": {
            method: iteration_totals[method] / (len(pairs) * len(ALPHAS))
            for method in iteration_totals
        },
        "distance_matrices_finite_symmetric_zero_diagonal": finite_symmetric,
        "matrix_sha256": {
            name: matrix_hash(matrix) for name, matrix in matrices.items()
        },
    }
    return matrices, diagnostics, selected_rows


def tune_and_score(
    distances: dict[float, np.ndarray],
    labels: np.ndarray,
    seed: int,
    permuted: bool,
) -> list[dict[str, object]]:
    used = (
        np.random.default_rng(seed + 900000).permutation(labels)
        if permuted
        else labels
    )
    outer = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    rows: list[dict[str, object]] = []
    for fold, (train, test) in enumerate(
        outer.split(distances[ALPHAS[0]], used), 1
    ):
        inner = StratifiedKFold(
            n_splits=5, shuffle=True, random_state=seed * 100 + fold
        )
        best: tuple[float, float, float, float] | None = None
        for alpha in ALPHAS:
            for gamma in GAMMA_GRID:
                kernel = np.exp(-gamma * distances[alpha] ** 2)
                for regularization in C_GRID:
                    scores: list[float] = []
                    for inner_train_local, validation_local in inner.split(
                        train, used[train]
                    ):
                        inner_train = train[inner_train_local]
                        validation = train[validation_local]
                        model = SVC(C=regularization, kernel="precomputed")
                        model.fit(
                            kernel[np.ix_(inner_train, inner_train)],
                            used[inner_train],
                        )
                        prediction = model.predict(
                            kernel[np.ix_(validation, inner_train)]
                        )
                        scores.append(
                            accuracy_score(used[validation], prediction)
                        )
                    candidate = (
                        float(np.mean(scores)),
                        -alpha,
                        -gamma,
                        -regularization,
                    )
                    if best is None or candidate > best:
                        best = candidate
        if best is None:
            raise RuntimeError("empty nested-CV grid")
        _, neg_alpha, neg_gamma, neg_c = best
        alpha, gamma, regularization = -neg_alpha, -neg_gamma, -neg_c
        kernel = np.exp(-gamma * distances[alpha] ** 2)
        model = SVC(C=regularization, kernel="precomputed")
        model.fit(kernel[np.ix_(train, train)], used[train])
        prediction = model.predict(kernel[np.ix_(test, train)])
        rows.append(
            {
                "outer_seed": seed,
                "fold": fold,
                "alpha": alpha,
                "gamma": gamma,
                "C": regularization,
                "accuracy": stable(accuracy_score(used[test], prediction)),
                "permuted_outcome_control": permuted,
            }
        )
    return rows


def summarize(rows: list[dict[str, object]]) -> dict[str, float | int]:
    values = np.asarray([float(row["accuracy"]) for row in rows])
    return {
        "outer_folds": len(values),
        "mean_accuracy": stable(values.mean()),
        "sample_std_accuracy": stable(values.std(ddof=1)),
        "standard_error": stable(values.std(ddof=1) / np.sqrt(len(values))),
    }


def run(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    work = output / "work"
    work.mkdir(exist_ok=True)
    all_results: dict[str, object] = {}
    cv_raw: list[dict[str, object]] = []
    control_raw: list[dict[str, object]] = []
    selected_raw: list[dict[str, object]] = []
    integrity_gates: dict[str, bool] = {}
    for name, expected in DATA.items():
        archive = work / f"{name}.zip"
        provenance = download(
            str(expected["url"]), archive, str(expected["sha256"])
        )
        extraction = work / name
        extraction.mkdir(exist_ok=True)
        with zipfile.ZipFile(archive) as handle:
            handle.extractall(extraction)
        indicator = next(extraction.rglob(f"{name}_graph_indicator.txt"))
        graphs, metadata = load_tu(indicator.parent, name)
        matrices, diagnostics, selected = pairwise_distances(graphs)
        labels = np.asarray([graph.label for graph in graphs])
        summaries: dict[str, object] = {}
        seedwise: dict[str, dict[str, float]] = {
            str(seed): {} for seed in OUTER_SEEDS
        }
        for method in ("CDOT", "FGW"):
            method_distances = {
                alpha: matrices[
                    f"{method}_a{int(round(alpha * 100)):03d}"
                ]
                for alpha in ALPHAS
            }
            method_rows: list[dict[str, object]] = []
            method_controls: list[dict[str, object]] = []
            for seed in OUTER_SEEDS:
                rows = tune_and_score(
                    method_distances, labels, seed, permuted=False
                )
                controls = tune_and_score(
                    method_distances, labels, seed, permuted=True
                )
                for row in rows:
                    row.update({"dataset": name, "method": method})
                for row in controls:
                    row.update({"dataset": name, "method": method})
                method_rows.extend(rows)
                method_controls.extend(controls)
                seedwise[str(seed)][method] = stable(
                    np.mean([float(row["accuracy"]) for row in rows])
                )
            summaries[method] = {
                **summarize(method_rows),
                "permuted_outcome_mean_accuracy": stable(
                    np.mean(
                        [float(row["accuracy"]) for row in method_controls]
                    )
                ),
            }
            cv_raw.extend(method_rows)
            control_raw.extend(method_controls)
        for seed in OUTER_SEEDS:
            values = seedwise[str(seed)]
            values["CDOT_minus_FGW"] = stable(
                values["CDOT"] - values["FGW"]
            )
        selected_raw.extend(
            [{"dataset": name, **row} for row in selected]
        )
        majority = max(np.bincount(np.unique(labels, return_inverse=True)[1])) / len(labels)
        dataset_gates = {
            "full_graph_count": len(graphs) == int(expected["graphs"]),
            "full_node_count": int(metadata["nodes"]) == int(expected["nodes"]),
            "all_pairs_executed": diagnostics["pairs"]
            == len(graphs) * (len(graphs) - 1) // 2,
            "matrices_finite_symmetric": bool(
                diagnostics[
                    "distance_matrices_finite_symmetric_zero_diagonal"
                ]
            ),
            "cdot_marginals_preserved": float(
                diagnostics["maximum_cdot_marginal_error"]
            )
            < 1e-8,
            "cdot_traces_monotone": diagnostics["cdot_nonmonotone_steps"]
            == 0,
            "fgw_traces_monotone": diagnostics["fgw_nonmonotone_steps"]
            == 0,
            "three_repeated_nested_10fold_runs": all(
                int(summaries[method]["outer_folds"]) == 30
                for method in ("CDOT", "FGW")
            ),
            "permuted_control_near_chance_and_degraded": all(
                float(summaries[method]["permuted_outcome_mean_accuracy"])
                <= majority + 0.05
                and float(summaries[method]["permuted_outcome_mean_accuracy"])
                < float(summaries[method]["mean_accuracy"]) - 0.05
                for method in ("CDOT", "FGW")
            ),
        }
        for gate, passed in dataset_gates.items():
            integrity_gates[f"{name}_{gate}"] = bool(passed)
        all_results[name] = {
            "data": {**provenance, **metadata},
            "diagnostics": diagnostics,
            "summaries": summaries,
            "seedwise_mean_accuracy": seedwise,
            "CDOT_minus_FGW_accuracy": stable(
                float(summaries["CDOT"]["mean_accuracy"])
                - float(summaries["FGW"]["mean_accuracy"])
            ),
            "majority_class_rate": stable(majority),
            "gates": dataset_gates,
        }
        del matrices

    enzymes_seedwise = all_results["ENZYMES"]["seedwise_mean_accuracy"]
    reversed_every_seed = all(
        float(enzymes_seedwise[str(seed)]["CDOT_minus_FGW"]) < 0
        for seed in OUTER_SEEDS
    )
    supports_paper_direction = all(
        float(all_results[name]["CDOT_minus_FGW_accuracy"]) > 0
        for name in ("MUTAG", "ENZYMES")
    )
    status = (
        "FALSIFIED"
        if all(integrity_gates.values()) and reversed_every_seed
        else "VERIFIED"
        if all(integrity_gates.values()) and supports_paper_direction
        else "BLOCKED"
    )
    result = {
        "claim": 5,
        "status": status,
        "paper_values": {
            "MUTAG_CDOT": [0.8617, 0.07],
            "MUTAG_FGW": [0.8249, 0.08],
            "ENZYMES_CDOT": [0.5133, 0.04],
            "ENZYMES_FGW": [0.4450, 0.03],
        },
        "protocol": {
            "all_graphs_and_unordered_pairs": True,
            "geometry": "unweighted geodesic divided by graph diameter",
            "node_information": "provided labels or attributes",
            "alpha_grid": list(ALPHAS),
            "kernel": "exp(-gamma*D^2)",
            "outer_cv": "three seeded stratified 10-fold runs",
            "inner_cv": "stratified 5-fold joint alpha/C/gamma search",
            "C_grid": list(C_GRID),
            "gamma_grid": list(GAMMA_GRID),
            "outer_seeds": list(OUTER_SEEDS),
            "max_optimizer_iterations": MAX_ITER,
            "process_workers": WORKERS,
        },
        "disclosed_reconstruction_ambiguities": [
            "source split seeds are unpublished",
            "ENZYMES attribute standardization is unspecified; dataset-wise z-scoring is used",
            "feature-cost scaling is unspecified; per-pair max normalization is used",
            "optimizer stopping tolerance is unspecified; disclosed at-most-200 stopping is used",
        ],
        "results": all_results,
        "classification": {
            "CDOT_greater_than_FGW_on_both": supports_paper_direction,
            "ENZYMES_direction_reversed_under_every_seed": reversed_every_seed,
            "reason": (
                "direct protocol-matched direction reversal on ENZYMES"
                if reversed_every_seed
                else "paper direction observed on both datasets"
                if supports_paper_direction
                else "neither a stable verification nor falsification"
            ),
        },
        "gates": integrity_gates,
        "all_gates_pass": all(integrity_gates.values()),
    }
    for name, value in (
        ("claim_5_nested_cv_rows.json", cv_raw),
        ("claim_5_permuted_controls.json", control_raw),
        ("claim_5_selected_pair_diagnostics.json", selected_raw),
        ("claim_5_result.json", result),
    ):
        (output / name).write_text(
            json.dumps(value, indent=2) + "\n", encoding="utf-8"
        )
    if not result["all_gates_pass"] or status == "BLOCKED":
        raise RuntimeError("Claim 5 evidence gates or verdict resolution failed")
    return result

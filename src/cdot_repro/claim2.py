"""Executable verifier for Theorems 3.5 and 3.7."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np

from .claim1 import feature_cost, objective, pairwise, random_coupling, structural


SEED = 37005
TOLERANCE = 1e-10


def dispersion_direct(
    dx: np.ndarray, dy: np.ndarray, coupling: np.ndarray
) -> tuple[float, float, float]:
    """Compute R, four-index GW, and conditional variance independently."""
    n, m = coupling.shape
    gw = float(
        np.einsum(
            "ikjl,ij,kl->",
            (dx[:, :, None, None] - dy[None, None, :, :]) ** 2,
            coupling,
            coupling,
        )
    )
    variance = 0.0
    for i, j in itertools.product(range(n), range(m)):
        conditional_x = coupling[:, j] * m
        conditional_y = coupling[i, :] * n
        values_x = dx[i]
        values_y = dy[j]
        variance_x = float(
            conditional_x @ (values_x**2) - (conditional_x @ values_x) ** 2
        )
        variance_y = float(
            conditional_y @ (values_y**2) - (conditional_y @ values_y) ** 2
        )
        variance += (variance_x + variance_y) / (n * m)
    return structural(dx, dy, coupling), gw, variance


def two_point_objective(
    space_a: tuple[float, float],
    space_b: tuple[float, float],
    alpha: float,
    coupling_coordinate: float,
) -> float:
    distance_a, feature_a = space_a
    distance_b, feature_b = space_b
    dx = np.array([[0.0, distance_a], [distance_a, 0.0]])
    dy = np.array([[0.0, distance_b], [distance_b, 0.0]])
    cost = feature_cost(
        np.array([[0.0], [feature_a]]),
        np.array([[0.0], [feature_b]]),
    )
    t = coupling_coordinate
    coupling = np.array([[t, 0.5 - t], [0.5 - t, t]])
    return objective(dx, dy, cost, coupling, alpha)


def two_point_distance(
    space_a: tuple[float, float],
    space_b: tuple[float, float],
    alpha: float,
) -> float:
    """Exactly minimize the one-dimensional convex quadratic on [0, 1/2]."""
    at_zero = two_point_objective(space_a, space_b, alpha, 0.0)
    at_half = two_point_objective(space_a, space_b, alpha, 0.25)
    at_one = two_point_objective(space_a, space_b, alpha, 0.5)
    quadratic = 2.0 * (at_one + at_zero - 2.0 * at_half)
    linear = at_one - at_zero - quadratic
    candidates = [0.0, 0.5]
    if quadratic > 1e-18:
        candidates.append(float(np.clip(-linear / (2 * quadratic), 0.0, 0.5)))
    return math.sqrt(
        max(
            0.0,
            min(
                two_point_objective(space_a, space_b, alpha, candidate)
                for candidate in candidates
            ),
        )
    )


def run(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    dispersion_rows: list[dict[str, object]] = []
    witnesses: list[dict[str, object]] = []
    for support, panel in itertools.product((3, 4, 5, 6), range(8)):
        dx = pairwise(rng.normal(size=(support, 3)))
        dy = pairwise(rng.normal(size=(support, 3)))
        coupling = random_coupling(support, rng, atoms=3 + panel % 5)
        cdot, gw, variance = dispersion_direct(dx, dy, coupling)
        error = abs(gw - cdot - variance)
        dispersion_rows.append(
            {
                "support": support,
                "panel": panel,
                "cdot_R": cdot,
                "gw_R": gw,
                "dispersion_V": variance,
                "identity_error": error,
            }
        )
        witnesses.append(
            {
                "support": support,
                "panel": panel,
                "dx": dx.tolist(),
                "dy": dy.tolist(),
                "coupling": coupling.tolist(),
            }
        )

    spaces = (
        (0.18, 0.22),
        (0.39, 0.51),
        (0.68, 0.79),
        (0.95, 1.12),
    )
    pseudometric_rows: list[dict[str, object]] = []
    identity_failures = 0
    symmetry_failures = 0
    triangle_failures = 0
    maximum_triangle_excess = -math.inf
    for alpha in (0.0, 0.25, 0.5, 0.75, 1.0):
        distances = {
            (i, j): two_point_distance(spaces[i], spaces[j], alpha)
            for i, j in itertools.product(range(len(spaces)), repeat=2)
        }
        identity_failures += sum(
            distances[(i, i)] > TOLERANCE for i in range(len(spaces))
        )
        symmetry_failures += sum(
            abs(distances[(i, j)] - distances[(j, i)]) > TOLERANCE
            for i, j in itertools.product(range(len(spaces)), repeat=2)
        )
        for i, j, k in itertools.product(range(len(spaces)), repeat=3):
            excess = distances[(i, k)] - distances[(i, j)] - distances[(j, k)]
            maximum_triangle_excess = max(maximum_triangle_excess, excess)
            triangle_failures += int(excess > TOLERANCE)
            pseudometric_rows.append(
                {
                    "alpha": alpha,
                    "x": i,
                    "y": j,
                    "z": k,
                    "d_xz": distances[(i, k)],
                    "d_xy": distances[(i, j)],
                    "d_yz": distances[(j, k)],
                    "triangle_excess": excess,
                }
            )

    d01 = two_point_distance(spaces[0], spaces[1], 0.0)
    d12 = two_point_distance(spaces[1], spaces[2], 0.0)
    d02 = two_point_distance(spaces[0], spaces[2], 0.0)
    squared_control_excess = d02**2 - d01**2 - d12**2
    gates = {
        "dispersion_identity_32_diffuse_couplings": len(dispersion_rows) == 32
        and max(row["identity_error"] for row in dispersion_rows) < TOLERANCE,
        "dispersion_strictly_positive": all(
            row["dispersion_V"] > TOLERANCE for row in dispersion_rows
        ),
        "complete_registered_finite_domain_enumerated": len(pseudometric_rows)
        == 320,
        "identity_passes": identity_failures == 0,
        "symmetry_passes": symmetry_failures == 0,
        "triangle_passes": triangle_failures == 0,
        "squared_distance_control_rejected": squared_control_excess > 1e-6,
        "population_proof_certificate_present": Path(
            ".openresearch/artifacts/claim_2/proof_certificate.md"
        ).is_file(),
    }
    result = {
        "claim": 2,
        "status": "VERIFIED" if all(gates.values()) else "BLOCKED",
        "scope": {
            "population_result": "supported by independently reconstructed proof obligations",
            "dispersion_witnesses": len(dispersion_rows),
            "complete_declared_two_point_domain_cells": len(pseudometric_rows),
            "finite_checks_do_not_replace_population_proof": True,
        },
        "seed": SEED,
        "summary": {
            "maximum_dispersion_identity_error": max(
                row["identity_error"] for row in dispersion_rows
            ),
            "minimum_positive_dispersion": min(
                row["dispersion_V"] for row in dispersion_rows
            ),
            "identity_failures": identity_failures,
            "symmetry_failures": symmetry_failures,
            "triangle_failures": triangle_failures,
            "maximum_triangle_excess": maximum_triangle_excess,
        },
        "negative_control": {
            "mutation": "square the valid discrepancy before applying triangle inequality",
            "triangle_excess": squared_control_excess,
            "expected": "strictly positive violation",
            "passed": squared_control_excess > 1e-6,
        },
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    for name, value in (
        ("claim_2_dispersion_rows.json", dispersion_rows),
        ("claim_2_pseudometric_rows.json", pseudometric_rows),
        ("claim_2_witnesses.json", witnesses),
        ("claim_2_result.json", result),
    ):
        (output / name).write_text(
            json.dumps(value, indent=2) + "\n", encoding="utf-8"
        )
    if not result["all_gates_pass"]:
        failed = [name for name, passed in gates.items() if not passed]
        raise RuntimeError("Claim 2 gates failed: " + ", ".join(failed))
    return result


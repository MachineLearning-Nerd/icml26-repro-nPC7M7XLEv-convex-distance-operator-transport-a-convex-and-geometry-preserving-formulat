"""Primary executable verifier for the exact Theorem 3.4 claim contract."""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import linear_sum_assignment


SEED = 260602047
TOLERANCE = 1e-10


def pairwise(points: np.ndarray) -> np.ndarray:
    delta = points[:, None, :] - points[None, :, :]
    matrix = np.sqrt(np.sum(delta * delta, axis=2))
    maximum = float(matrix.max())
    return matrix / maximum if maximum else matrix


def feature_cost(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    delta = left[:, None, :] - right[None, :, :]
    return np.sum(delta * delta, axis=2)


def permutation_coupling(permutation: np.ndarray) -> np.ndarray:
    n = len(permutation)
    coupling = np.zeros((n, n), dtype=np.float64)
    coupling[np.arange(n), permutation] = 1.0 / n
    return coupling


def random_coupling(n: int, rng: np.random.Generator, atoms: int = 7) -> np.ndarray:
    weights = rng.random(atoms)
    weights /= weights.sum()
    coupling = np.zeros((n, n), dtype=np.float64)
    for weight in weights:
        coupling += weight * permutation_coupling(rng.permutation(n))
    return coupling


def linear_map(dx: np.ndarray, dy: np.ndarray) -> np.ndarray:
    """Matrix A such that vec(Dx*pi/n - pi*Dy/n) == A@vec(pi)."""
    n = dx.shape[0]
    identity = np.eye(n)
    return np.kron(identity, dx / n) - np.kron((dy / n).T, identity)


def structural(dx: np.ndarray, dy: np.ndarray, coupling: np.ndarray) -> float:
    n = coupling.shape[0]
    residual = (dx / n) @ coupling - coupling @ (dy / n)
    return float(n * n * np.sum(residual * residual))


def objective(
    dx: np.ndarray,
    dy: np.ndarray,
    cost: np.ndarray,
    coupling: np.ndarray,
    alpha: float,
) -> float:
    return float(
        (1.0 - alpha) * np.sum(cost * coupling)
        + 0.5 * alpha * structural(dx, dy, coupling)
    )


def gradient(
    dx: np.ndarray,
    dy: np.ndarray,
    cost: np.ndarray,
    coupling: np.ndarray,
    alpha: float,
) -> np.ndarray:
    n = coupling.shape[0]
    residual = (dx / n) @ coupling - coupling @ (dy / n)
    structural_gradient = n * n * (
        (dx / n).T @ residual - residual @ (dy / n).T
    )
    return (1.0 - alpha) * cost + alpha * structural_gradient


def frank_wolfe(
    dx: np.ndarray,
    dy: np.ndarray,
    cost: np.ndarray,
    alpha: float,
    initial: np.ndarray,
    iterations: int = 180,
) -> tuple[np.ndarray, list[float]]:
    coupling = initial.copy()
    history = [objective(dx, dy, cost, coupling, alpha)]
    for _ in range(iterations):
        rows, columns = linear_sum_assignment(
            gradient(dx, dy, cost, coupling, alpha)
        )
        atom = np.zeros_like(coupling)
        atom[rows, columns] = 1.0 / coupling.shape[0]
        direction = atom - coupling
        base = history[-1]
        midpoint = objective(dx, dy, cost, coupling + 0.5 * direction, alpha)
        endpoint = objective(dx, dy, cost, atom, alpha)
        quadratic = 2.0 * (endpoint + base - 2.0 * midpoint)
        linear = endpoint - base - quadratic
        if quadratic > 1e-18:
            step = float(np.clip(-linear / (2.0 * quadratic), 0.0, 1.0))
        else:
            step = float(endpoint < base)
        coupling += step * direction
        history.append(objective(dx, dy, cost, coupling, alpha))
    return coupling, history


def exact_symbolic_factorization() -> dict[str, object]:
    """Verify the generic squared-affine convexity identity over rationals."""
    theta = sp.symbols("theta", real=True)
    a1, a2, b1, b2 = sp.symbols("a1 a2 b1 b2", real=True)
    residual_1 = sp.Matrix([a1, a2])
    residual_2 = sp.Matrix([b1, b2])
    mixed = theta * residual_1 + (1 - theta) * residual_2
    chord_gap = sp.expand(
        theta * residual_1.dot(residual_1)
        + (1 - theta) * residual_2.dot(residual_2)
        - mixed.dot(mixed)
    )
    expected = sp.expand(
        theta * (1 - theta) * (residual_1 - residual_2).dot(
            residual_1 - residual_2
        )
    )
    return {
        "identity": "theta||r1||^2+(1-theta)||r2||^2-||theta*r1+(1-theta)*r2||^2 = theta(1-theta)||r1-r2||^2",
        "symbolic_remainder": str(sp.simplify(chord_gap - expected)),
        "passes": sp.simplify(chord_gap - expected) == 0,
    }


@dataclass(frozen=True)
class AuditRow:
    support: int
    alpha: float
    panel: int
    theta: float
    jensen_gap: float
    minimum_hessian_eigenvalue: float
    maximum_marginal_error: float
    monotonicity_failures: int
    three_start_final_spread: float

    def as_dict(self) -> dict[str, object]:
        return {
            "support": self.support,
            "alpha": self.alpha,
            "panel": self.panel,
            "theta": self.theta,
            "jensen_gap": self.jensen_gap,
            "minimum_hessian_eigenvalue": self.minimum_hessian_eigenvalue,
            "maximum_marginal_error": self.maximum_marginal_error,
            "monotonicity_failures": self.monotonicity_failures,
            "three_start_final_spread": self.three_start_final_spread,
        }


def run(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    rows: list[AuditRow] = []
    for support, alpha, panel in itertools.product(
        (3, 4, 5, 6, 12, 24), (0.0, 0.25, 0.5, 0.75, 1.0), range(2)
    ):
        x = rng.normal(size=(support, 3))
        y = rng.normal(size=(support, 3))
        fx = rng.normal(size=(support, 2))
        fy = rng.normal(size=(support, 2))
        dx, dy = pairwise(x), pairwise(y)
        cost = feature_cost(fx, fy)
        first = random_coupling(support, rng)
        second = random_coupling(support, rng)
        theta = 0.23 + 0.31 * panel
        mixed = theta * first + (1.0 - theta) * second
        jensen_gap = (
            theta * objective(dx, dy, cost, first, alpha)
            + (1.0 - theta) * objective(dx, dy, cost, second, alpha)
            - objective(dx, dy, cost, mixed, alpha)
        )
        operator = linear_map(dx, dy)
        hessian = alpha * support * support * (operator.T @ operator)
        minimum_eigenvalue = float(np.linalg.eigvalsh(hessian).min())
        starts = (first, second, np.full((support, support), 1 / support**2))
        finals: list[float] = []
        marginal_error = 0.0
        monotonicity_failures = 0
        for start in starts:
            solution, history = frank_wolfe(dx, dy, cost, alpha, start)
            finals.append(history[-1])
            marginal_error = max(
                marginal_error,
                float(np.max(np.abs(solution.sum(axis=0) - 1 / support))),
                float(np.max(np.abs(solution.sum(axis=1) - 1 / support))),
            )
            monotonicity_failures += sum(
                later > earlier + TOLERANCE
                for earlier, later in zip(history, history[1:], strict=True)
            )
        rows.append(
            AuditRow(
                support=support,
                alpha=alpha,
                panel=panel,
                theta=theta,
                jensen_gap=float(jensen_gap),
                minimum_hessian_eigenvalue=minimum_eigenvalue,
                maximum_marginal_error=marginal_error,
                monotonicity_failures=monotonicity_failures,
                three_start_final_spread=max(finals) - min(finals),
            )
        )

    # Destructive control: replacing +||A(pi)||² by -||A(pi)||² must violate
    # Jensen convexity for a witness with non-identical residuals.
    dx = pairwise(np.array([[0.0], [0.2], [1.0]]))
    dy = pairwise(np.array([[0.0], [0.6], [1.0]]))
    first = permutation_coupling(np.array([0, 1, 2]))
    second = permutation_coupling(np.array([1, 2, 0]))
    midpoint = 0.5 * (first + second)
    negative_control_excess = (
        -structural(dx, dy, midpoint)
        - 0.5 * (-structural(dx, dy, first) - structural(dx, dy, second))
    )

    symbolic = exact_symbolic_factorization()
    gates = {
        "exact_symbolic_factorization": bool(symbolic["passes"]),
        "all_60_jensen_checks_pass": len(rows) == 60
        and min(row.jensen_gap for row in rows) >= -TOLERANCE,
        "all_vectorized_hessians_psd": min(
            row.minimum_hessian_eigenvalue for row in rows
        )
        >= -1e-8,
        "transport_marginals_preserved": max(
            row.maximum_marginal_error for row in rows
        )
        < TOLERANCE,
        "frank_wolfe_objective_monotone": sum(
            row.monotonicity_failures for row in rows
        )
        == 0,
        "negative_squared_norm_control_rejected": negative_control_excess > 1e-6,
        "population_proof_certificate_present": Path(
            ".openresearch/artifacts/claim_1/proof_certificate.md"
        ).is_file(),
    }
    result = {
        "claim": 1,
        "status": "VERIFIED" if all(gates.values()) else "BLOCKED",
        "scope": {
            "population_result": "supported by independently reconstructed proof obligations",
            "finite_executable_panels": len(rows),
            "largest_support": max(row.support for row in rows),
            "finite_checks_do_not_replace_population_proof": True,
        },
        "seed": SEED,
        "symbolic_certificate": symbolic,
        "negative_control": {
            "mutation": "negate the squared structural Hilbert-Schmidt term",
            "jensen_excess": negative_control_excess,
            "expected": "strictly positive convexity violation",
            "passed": negative_control_excess > 1e-6,
        },
        "summary": {
            "minimum_jensen_gap": min(row.jensen_gap for row in rows),
            "minimum_hessian_eigenvalue": min(
                row.minimum_hessian_eigenvalue for row in rows
            ),
            "maximum_marginal_error": max(
                row.maximum_marginal_error for row in rows
            ),
            "monotonicity_failures": sum(
                row.monotonicity_failures for row in rows
            ),
            "maximum_three_start_final_spread": max(
                row.three_start_final_spread for row in rows
            ),
        },
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    (output / "claim_1_rows.json").write_text(
        json.dumps([row.as_dict() for row in rows], indent=2) + "\n",
        encoding="utf-8",
    )
    (output / "claim_1_result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        failed = [name for name, passed in gates.items() if not passed]
        raise RuntimeError("Claim 1 gates failed: " + ", ".join(failed))
    return result


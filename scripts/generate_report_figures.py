#!/usr/bin/env python3
"""Generate the five evidence figures used by the CDOT reproduction report."""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "cdot-reproduction" / "images"


def load(claim: int, name: str | None = None) -> dict:
    filename = name or f"claim_{claim}_result.json"
    path = ROOT / ".openresearch" / "artifacts" / f"claim_{claim}" / "raw" / filename
    return json.loads(path.read_text(encoding="utf-8"))


def finish(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    normalized = "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines())
    path.write_text(normalized + "\n", encoding="utf-8")


def headline_claim3() -> None:
    result = load(3)
    methods = ["CDOT", "FGW", "IsoRank"]
    observed = np.array([result["summaries"][m]["mean_mse"] for m in methods])
    low = np.array([result["summaries"][m]["ci95_low"] for m in methods])
    high = np.array([result["summaries"][m]["ci95_high"] for m in methods])
    paper = np.array([result["source_table_2"][m]["mean_mse"] for m in methods])
    colors = ["#2563eb", "#f97316", "#8b5cf6"]

    fig, ax = plt.subplots(figsize=(8.4, 4.7))
    x = np.arange(len(methods))
    ax.bar(x, observed, color=colors, width=0.62, label="100-trial reproduction")
    ax.errorbar(
        x,
        observed,
        yerr=np.vstack([observed - low, high - observed]),
        fmt="none",
        ecolor="#111827",
        capsize=5,
        linewidth=1.3,
    )
    ax.scatter(x, paper, marker="D", s=48, color="white", edgecolor="#111827", zorder=4, label="Paper mean")
    for index, value in enumerate(observed):
        ax.text(index, value + 0.00013, f"{value:.5f}", ha="center", va="bottom", fontsize=10)
    ax.set_xticks(x, methods)
    ax.set_ylabel("Matching MSE (lower is better)")
    ax.set_title("Claim 3: paper-scale synthetic ordering is reproduced")
    ax.set_ylim(0, 0.00425)
    ax.grid(axis="y", alpha=0.22)
    ax.legend(frameon=False, loc="upper left")
    finish(fig, "claim3_headline.svg")


def paired_claim3() -> None:
    result = load(3)
    comparisons = ["CDOT − FGW", "CDOT − IsoRank"]
    entries = [
        result["paired_cdot_minus_baseline"]["FGW"],
        result["paired_cdot_minus_baseline"]["IsoRank"],
    ]
    means = np.array([entry["mean_cdot_minus_baseline"] for entry in entries])
    low = np.array([entry["ci95_low"] for entry in entries])
    high = np.array([entry["ci95_high"] for entry in entries])

    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    y = np.arange(len(comparisons))
    ax.errorbar(
        means,
        y,
        xerr=np.vstack([means - low, high - means]),
        fmt="o",
        color="#2563eb",
        ecolor="#2563eb",
        capsize=6,
        markersize=8,
    )
    ax.axvline(0, color="#991b1b", linestyle="--", linewidth=1.2, label="No difference")
    ax.set_yticks(y, comparisons)
    ax.invert_yaxis()
    ax.set_xlabel("Paired MSE difference with 95% CI")
    ax.set_title("All registered paired intervals are strictly below zero")
    ax.grid(axis="x", alpha=0.22)
    ax.legend(frameon=False, loc="lower right")
    finish(fig, "claim3_paired_effects.svg")


def claim5_benchmarks() -> None:
    result = load(5)
    datasets = ["MUTAG", "ENZYMES"]
    methods = ["CDOT", "FGW"]
    values = {
        method: [result["results"][dataset]["summaries"][method]["mean_accuracy"] for dataset in datasets]
        for method in methods
    }
    paper = {
        "CDOT": [0.8617, 0.5133],
        "FGW": [0.8249, 0.4450],
    }

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.2), sharey=False)
    for index, dataset in enumerate(datasets):
        ax = axes[index]
        x = np.arange(2)
        ax.bar(x - 0.18, [paper[m][index] for m in methods], 0.36, color="#cbd5e1", label="Paper")
        ax.bar(x + 0.18, [values[m][index] for m in methods], 0.36, color=["#2563eb", "#f97316"], label="Reproduction")
        ax.set_xticks(x, methods)
        ax.set_ylim(0, 1)
        ax.set_title(dataset)
        ax.grid(axis="y", alpha=0.22)
        if index == 0:
            ax.set_ylabel("Nested-CV accuracy")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.03))
    fig.suptitle("Claim 5: MUTAG direction holds; ENZYMES reverses", y=0.99)
    fig.subplots_adjust(top=0.82, bottom=0.18, wspace=0.2)
    finish(fig, "claim5_benchmarks.svg")


def oasis_cohort() -> None:
    result = load(4, "formal_4df2d784/claim_4_result.json")
    valid = result["scope"]["valid_170_node_subjects"]
    total = result["scope"]["archive_subjects"]
    table3 = result["table_3"]
    labels = ["Diffusion\nCDOT", "Diffusion\nFGW", "Geodesic\nCDOT", "Geodesic\nFGW"]
    paper = [
        table3["source_table_3"]["diffusion_CDOT"],
        table3["source_table_3"]["diffusion_FGW"],
        table3["source_table_3"]["geodesic_CDOT"],
        table3["source_table_3"]["geodesic_FGW"],
    ]
    observed = [
        table3["rerun"]["diffusion_CDOT"]["mean_accuracy"],
        table3["rerun"]["diffusion_FGW"]["mean_accuracy"],
        table3["rerun"]["geodesic_CDOT"]["mean_accuracy"],
        table3["rerun"]["geodesic_FGW"]["mean_accuracy"],
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.2), gridspec_kw={"width_ratios": [1.2, 1]})
    ax = axes[0]
    x = np.arange(4)
    ax.bar(x - 0.18, paper, 0.36, color="#cbd5e1", label="Paper")
    ax.bar(x + 0.18, observed, 0.36, color=["#2563eb", "#f97316", "#2563eb", "#f97316"], label="Reproduction")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 0.82)
    ax.set_ylabel("Mean matching accuracy")
    ax.set_title("All 4,950 pairs")
    ax.grid(axis="y", alpha=0.2)
    ax.legend(frameon=False, loc="upper right")

    ax = axes[1]
    ax.barh(["Archive"], [valid], color="#2563eb", label="Has 170-node session")
    ax.barh(["Archive"], [total - valid], left=[valid], color="#dc2626", label="No 170-node session")
    ax.text(valid / 2, 0, f"{valid}", color="white", ha="center", va="center", weight="bold")
    ax.text(valid + 0.5, 0, "1", color="white", ha="center", va="center", weight="bold")
    ax.annotate(
        "OAS30938: one 168-node session",
        xy=(valid + 0.5, 0),
        xytext=(valid - 240, 0.34),
        arrowprops={"arrowstyle": "->", "color": "#991b1b"},
        color="#991b1b",
        fontsize=9,
    )
    ax.set_xlim(0, total)
    ax.set_xlabel("Subjects")
    ax.set_title("All 975 sessions audited")
    ax.legend(frameon=False, loc="lower left", fontsize=8)
    ax.grid(axis="x", alpha=0.18)
    fig.suptitle("Claim 4: both Table 3 directions reproduce; cohort invariant is false", y=1.02)
    fig.subplots_adjust(wspace=0.32)
    finish(fig, "claim4_cohort.svg")


def controls() -> None:
    claim1 = load(1)
    claim3 = load(3)
    claim6 = load(6)
    labels = [
        "Claim 1\nnegated norm",
        "Claim 3\nwrong features",
        "Claim 6\ninvalid schedule",
    ]
    ratios = [
        claim1["negative_control_jensen_excess"] / 1e-12,
        claim3["controls"]["wrong_feature_mse"] / claim3["controls"]["normal_feature_mse"],
        claim6["summary"]["invalid_control_limit_indicator"] / claim6["summary"]["smallest_valid_n_over_T"],
    ]

    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    x = np.arange(len(labels))
    bars = ax.bar(x, ratios, color=["#7c3aed", "#dc2626", "#f97316"])
    ax.set_yscale("log")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Failure signal relative to valid tolerance/baseline (log scale)")
    ax.set_title("Destructive controls fail for their registered reasons")
    ax.grid(axis="y", which="both", alpha=0.2)
    for bar, value in zip(bars, ratios, strict=True):
        ax.text(bar.get_x() + bar.get_width() / 2, value * 1.15, f"{value:.1e}×", ha="center", fontsize=9)
    finish(fig, "negative_controls.svg")


def main() -> None:
    headline_claim3()
    paired_claim3()
    claim5_benchmarks()
    oasis_cohort()
    controls()
    print(f"wrote 5 SVG figures to {OUT}")


if __name__ == "__main__":
    main()

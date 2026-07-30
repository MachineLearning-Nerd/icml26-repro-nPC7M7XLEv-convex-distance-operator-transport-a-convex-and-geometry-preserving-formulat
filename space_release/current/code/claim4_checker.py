"""Independent counterexample and raw-audit checker for Claim 4."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from itertools import combinations
from pathlib import Path

import numpy as np


GRAPHML_NS = "http://graphml.graphdrawing.org/xmlns"
SUBJECT_RE = re.compile(r"^sub-(OAS\d+)_ses-d(\d+)_")


def independent_ids(path: Path) -> list[int]:
    root = ET.parse(path).getroot()
    key_names = {
        element.attrib["id"]: element.attrib.get("attr.name")
        for element in root.findall(f"{{{GRAPHML_NS}}}key")
    }
    ids: list[int] = []
    for node in root.iter(f"{{{GRAPHML_NS}}}node"):
        values = [
            data.text
            for data in node.findall(f"{{{GRAPHML_NS}}}data")
            if key_names.get(data.attrib.get("key", ""))
            == "dn_multiscaleID"
        ]
        if len(values) != 1 or values[0] is None:
            raise ValueError("independent parser found an ambiguous node ID")
        ids.append(int(values[0]))
    return sorted(ids)


def check(runtime_dir: Path) -> dict[str, object]:
    primary = json.loads((runtime_dir / "claim_4_result.json").read_text())
    session_rows: list[dict[str, object]] = []
    for path in sorted(runtime_dir.glob("claim_4_session_audit_*.json")):
        session_rows.extend(json.loads(path.read_text()))
    subject_rows = json.loads(
        (runtime_dir / "claim_4_subject_audit.json").read_text()
    )
    files = list((runtime_dir / "work" / "extracted").rglob("*.graphml"))
    counterexample_name = primary["data_provenance"]["counterexample_file"]
    counterexample_paths = [
        path for path in files if path.name == counterexample_name
    ]
    if len(counterexample_paths) != 1:
        raise RuntimeError("counterexample file is not uniquely materialized")
    ids = independent_ids(counterexample_paths[0])
    subject_counts: dict[str, int] = {}
    for row in session_rows:
        match = SUBJECT_RE.match(str(row["file"]))
        if not match or match.group(1) != row["subject"]:
            raise RuntimeError("session filename/subject mismatch")
        subject_counts[str(row["subject"])] = (
            subject_counts.get(str(row["subject"]), 0) + 1
        )
    recorded_invalid = [
        row for row in session_rows if row["subject"] == "OAS30938"
    ]
    table3 = json.loads(
        (runtime_dir / "claim_4_table3_result.json").read_text()
    )
    pair_rows: list[dict[str, object]] = []
    for path in sorted(runtime_dir.glob("claim_4_table3_pairs_*.json")):
        pair_rows.extend(json.loads(path.read_text()))
    expected_pairs = {
        (left, right) for left, right in combinations(range(100), 2)
    }
    subject_order = [
        str(row["subject"]) for row in table3["selected_subjects"]
    ]
    observed_pairs = {
        (
            subject_order.index(str(row["left_subject"])),
            subject_order.index(str(row["right_subject"])),
        )
        for row in pair_rows
    }
    independent_summary: dict[str, float] = {}
    for metric in ("diffusion", "geodesic"):
        for method in ("CDOT", "FGW"):
            values = np.asarray(
                [
                    float(row["accuracy"])
                    for row in pair_rows
                    if row["metric"] == metric
                    and row["method"] == method
                ]
            )
            independent_summary[f"{metric}_{method}"] = float(values.mean())
    recorded_summary = {
        key: float(value["mean_accuracy"])
        for key, value in table3["rerun"].items()
    }
    summary_error = max(
        abs(independent_summary[key] - recorded_summary[key])
        for key in independent_summary
    )
    diffusion_margin = (
        independent_summary["diffusion_CDOT"]
        - independent_summary["diffusion_FGW"]
    )
    geodesic_margin = (
        independent_summary["geodesic_FGW"]
        - independent_summary["geodesic_CDOT"]
    )
    gates = {
        "all_chunked_sessions_loaded": len(session_rows) == 975,
        "all_subject_rows_loaded": len(subject_rows) == 696,
        "filename_parser_independently_finds_696_subjects": len(subject_counts)
        == 696,
        "counterexample_has_one_session": len(recorded_invalid) == 1,
        "independent_xml_parser_finds_exact_ids_1_to_168": ids
        == list(range(1, 169)),
        "no_counterexample_session_contains_169_or_170": 169 not in ids
        and 170 not in ids,
        "primary_falsification_status_rechecked": primary["status"]
        == "FALSIFIED",
        "table3_all_19800_method_metric_rows_loaded": len(pair_rows)
        == 4_950 * 4,
        "table3_exact_4950_pair_inventory": observed_pairs
        == expected_pairs,
        "table3_each_cell_has_4950_rows": all(
            sum(
                row["metric"] == metric and row["method"] == method
                for row in pair_rows
            )
            == 4_950
            for metric in ("diffusion", "geodesic")
            for method in ("CDOT", "FGW")
        ),
        "table3_summary_recomputed_from_raw_rows": summary_error < 1e-9,
        "table3_diffusion_direction_rechecked": diffusion_margin > 0,
        "table3_geodesic_direction_rechecked": geodesic_margin > 0,
        "table3_primary_gates_rechecked": table3["all_gates_pass"],
    }
    result = {
        "checker": (
            "independent filename inventory plus direct ElementTree reparse "
            "of the primary-archive counterexample"
        ),
        "counterexample_file": counterexample_name,
        "independent_node_count": len(ids),
        "independent_min_id": min(ids),
        "independent_max_id": max(ids),
        "independent_subject_count": len(subject_counts),
        "table3_raw_rows": len(pair_rows),
        "table3_unique_pairs": len(observed_pairs),
        "table3_independent_summary": independent_summary,
        "table3_summary_max_abs_error": summary_error,
        "table3_diffusion_CDOT_minus_FGW": diffusion_margin,
        "table3_geodesic_FGW_minus_CDOT": geodesic_margin,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    (runtime_dir / "claim_4_independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        raise RuntimeError("Independent Claim 4 checker failed")
    return result

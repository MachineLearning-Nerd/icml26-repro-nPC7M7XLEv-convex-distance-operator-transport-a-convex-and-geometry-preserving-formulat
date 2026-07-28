"""Independent counterexample and raw-audit checker for Claim 4."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


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
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    (runtime_dir / "claim_4_independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        raise RuntimeError("Independent Claim 4 checker failed")
    return result

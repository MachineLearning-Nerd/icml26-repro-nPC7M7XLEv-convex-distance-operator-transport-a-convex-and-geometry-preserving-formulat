"""Exhaustive primary-archive verifier for the OASIS-3 cohort claim."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tarfile
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


USER_AGENT = "OpenResearch-CDOT-Reproduction/1.0"
ARCHIVE_URL = "https://braingraph.org/static/oasis3_graphmls_scale2.7z"
ARCHIVE_SHA256 = (
    "599e56c6968f3e01be66bdbb5689c0a16ed03e5a44e1071a66c2609390fe939f"
)
ARCHIVE_BYTES = 654_450_976
SEVEN_Z_URL = "https://www.7-zip.org/a/7z2501-linux-x64.tar.xz"
SEVEN_Z_SHA256 = (
    "4ca3b7c6f2f67866b92622818b58233dc70367be2f36b498eb0bdeaaa44b53f4"
)
SUBJECT_RE = re.compile(r"^sub-(OAS\d+)_ses-d(\d+)_")
GRAPHML_NS = "http://graphml.graphdrawing.org/xmlns"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, destination: Path, expected_hash: str) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    digest = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(request, timeout=120) as response:
        final_url = response.geturl()
        with destination.open("wb") as handle:
            while True:
                block = response.read(1 << 20)
                if not block:
                    break
                handle.write(block)
                digest.update(block)
                total += len(block)
                if total % (128 << 20) < (1 << 20):
                    print(
                        json.dumps(
                            {"download": destination.name, "bytes": total}
                        ),
                        flush=True,
                    )
    observed = digest.hexdigest()
    if observed != expected_hash:
        raise RuntimeError(
            f"{destination.name} SHA-256 mismatch: {observed}"
        )
    return {
        "requested_url": url,
        "final_url": final_url,
        "user_agent": USER_AGENT,
        "bytes": total,
        "sha256": observed,
    }


def graphml_ids(path: Path) -> list[int]:
    root = ET.parse(path).getroot()
    keys = {
        item.attrib["id"]: item.attrib.get("attr.name")
        for item in root.findall(f"{{{GRAPHML_NS}}}key")
        if item.attrib.get("for") in {"node", "all"}
    }
    multiscale_keys = {
        key for key, name in keys.items() if name == "dn_multiscaleID"
    }
    if not multiscale_keys:
        raise ValueError(f"{path.name}: dn_multiscaleID key missing")
    ids: list[int] = []
    for node in root.iter(f"{{{GRAPHML_NS}}}node"):
        matches = [
            data.text
            for data in node.findall(f"{{{GRAPHML_NS}}}data")
            if data.attrib.get("key") in multiscale_keys
        ]
        if len(matches) != 1 or matches[0] is None:
            raise ValueError(f"{path.name}: ambiguous dn_multiscaleID")
        ids.append(int(matches[0]))
    return sorted(ids)


def write_compact_chunks(
    output: Path, stem: str, rows: list[dict[str, object]], size: int
) -> list[dict[str, object]]:
    descriptors: list[dict[str, object]] = []
    for index, start in enumerate(range(0, len(rows), size)):
        path = output / f"{stem}_{index:03d}.json"
        subset = rows[start : start + size]
        path.write_text(
            json.dumps(subset, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        descriptors.append(
            {
                "path": path.name,
                "rows": len(subset),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    return descriptors


def run(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    work = output / "work"
    work.mkdir(exist_ok=True)
    archive = work / "oasis3_graphmls_scale2.7z"
    tool_tar = work / "7z2501-linux-x64.tar.xz"
    extraction_root = work / "extracted"
    tool_root = work / "sevenzip"
    stages: dict[str, float] = {}

    started = time.perf_counter()
    archive_provenance = download(ARCHIVE_URL, archive, ARCHIVE_SHA256)
    stages["archive_download_and_hash_seconds"] = time.perf_counter() - started
    if archive.stat().st_size != ARCHIVE_BYTES:
        raise RuntimeError("primary OASIS-3 archive byte count mismatch")

    started = time.perf_counter()
    tool_provenance = download(SEVEN_Z_URL, tool_tar, SEVEN_Z_SHA256)
    tool_root.mkdir(exist_ok=True)
    with tarfile.open(tool_tar, mode="r:xz") as handle:
        member = handle.getmember("7zz")
        handle.extract(member, tool_root, filter="data")
    executable = tool_root / "7zz"
    executable.chmod(0o755)
    stages["extractor_download_and_unpack_seconds"] = (
        time.perf_counter() - started
    )

    started = time.perf_counter()
    listing = subprocess.run(
        [str(executable), "l", "-slt", str(archive)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    listed_names = sorted(
        line.removeprefix("Path = ")
        for line in listing.splitlines()
        if line.startswith("Path = ")
        and line.lower().endswith(".graphml")
    )
    listing_path = output / "claim_4_archive_listing.txt"
    listing_path.write_text(listing, encoding="utf-8")
    stages["archive_listing_seconds"] = time.perf_counter() - started

    started = time.perf_counter()
    extraction_root.mkdir(exist_ok=True)
    subprocess.run(
        [
            str(executable),
            "x",
            str(archive),
            f"-o{extraction_root}",
            "-mmt=4",
            "-y",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    stages["archive_extraction_seconds"] = time.perf_counter() - started

    started = time.perf_counter()
    graphmls = sorted(extraction_root.rglob("*.graphml"))
    extracted_names = sorted(path.name for path in graphmls)
    session_rows: list[dict[str, object]] = []
    manifest_rows: list[dict[str, object]] = []
    subjects: dict[str, list[dict[str, object]]] = {}
    aggregate = hashlib.sha256()
    for index, path in enumerate(graphmls, 1):
        match = SUBJECT_RE.match(path.name)
        if not match:
            raise ValueError(f"unrecognized archive member {path.name}")
        subject, day_text = match.groups()
        ids = graphml_ids(path)
        file_hash = sha256(path)
        file_bytes = path.stat().st_size
        exact = ids == list(range(1, 171))
        session = {
            "subject": subject,
            "day": int(day_text),
            "file": path.name,
            "node_count": len(ids),
            "min_multiscale_id": min(ids),
            "max_multiscale_id": max(ids),
            "exact_ids_1_to_170": exact,
        }
        session_rows.append(session)
        subjects.setdefault(subject, []).append(session)
        manifest_rows.append(
            {"file": path.name, "bytes": file_bytes, "sha256": file_hash}
        )
        aggregate.update(
            f"{path.name}\0{file_bytes}\0{file_hash}\n".encode()
        )
        if index % 100 == 0:
            print(
                json.dumps(
                    {
                        "audited_graphml_sessions": index,
                        "total_sessions": len(graphmls),
                    }
                ),
                flush=True,
            )
    stages["all_session_parse_and_hash_seconds"] = time.perf_counter() - started

    subject_rows: list[dict[str, object]] = []
    invalid_subjects: list[dict[str, object]] = []
    for ordinal, subject in enumerate(sorted(subjects), 1):
        sessions = sorted(subjects[subject], key=lambda row: int(row["day"]))
        valid = [row for row in sessions if row["exact_ids_1_to_170"]]
        subject_row = {
            "ordinal": ordinal,
            "subject": subject,
            "session_count": len(sessions),
            "valid_170_node_sessions": len(valid),
            "earliest_file": sessions[0]["file"],
        }
        subject_rows.append(subject_row)
        if not valid:
            invalid_subjects.append(
                {"subject": subject, "sessions": sessions}
            )

    invalid_exact = (
        len(invalid_subjects) == 1
        and invalid_subjects[0]["subject"] == "OAS30938"
        and len(invalid_subjects[0]["sessions"]) == 1
        and invalid_subjects[0]["sessions"][0]["node_count"] == 168
        and invalid_subjects[0]["sessions"][0]["min_multiscale_id"] == 1
        and invalid_subjects[0]["sessions"][0]["max_multiscale_id"] == 168
    )
    invalid_filename = (
        str(invalid_subjects[0]["sessions"][0]["file"])
        if invalid_exact
        else ""
    )
    padded_ids = list(range(1, 169)) + [169, 170]
    control = {
        "mutation": "fabricate atlas IDs 169 and 170 for the sole invalid session",
        "observed_node_count": 168,
        "mutated_node_count": len(padded_ids),
        "fabricated_ids": [169, 170],
        "archive_contains_fabricated_ids": False,
        "rejected": invalid_exact,
    }
    gates = {
        "primary_archive_hash_exact": archive_provenance["sha256"]
        == ARCHIVE_SHA256,
        "primary_archive_size_exact": archive_provenance["bytes"]
        == ARCHIVE_BYTES,
        "official_7zip_binary_hash_exact": tool_provenance["sha256"]
        == SEVEN_Z_SHA256,
        "archive_listing_has_975_graphml_members": len(listed_names) == 975,
        "extraction_has_same_975_names": (
            len(extracted_names) == 975 and listed_names == extracted_names
        ),
        "all_975_sessions_parsed_and_hashed": len(session_rows) == 975,
        "all_696_subject_ids_enumerated": len(subject_rows) == 696,
        "exactly_695_subjects_have_a_valid_170_node_session": sum(
            int(row["valid_170_node_sessions"] > 0) for row in subject_rows
        )
        == 695,
        "assumption_satisfying_counterexample_is_exact": invalid_exact,
        "padding_control_rejected": control["rejected"],
    }
    result = {
        "claim": 4,
        "status": "FALSIFIED" if all(gates.values()) else "BLOCKED",
        "exact_claim_tested": (
            "The Table 3 cohort consists of 696 OASIS-3 subjects represented "
            "by 170-node networks."
        ),
        "logical_falsification": (
            "A universal cohort invariant is false if any included subject "
            "has no 170-node session. The exact primary archive contains all "
            "696 subjects, while OAS30938 has one session with IDs 1..168."
        ),
        "scope": {
            "archive_sessions": len(session_rows),
            "archive_subjects": len(subject_rows),
            "valid_170_node_subjects": sum(
                int(row["valid_170_node_sessions"] > 0)
                for row in subject_rows
            ),
            "invalid_subjects": invalid_subjects,
            "table_3_numeric_cells_rerun": False,
            "numeric_nonrerun_reason": (
                "not needed for the valid counterexample; no numerical value "
                "is inferred from the archive invariant"
            ),
        },
        "data_provenance": {
            "primary_landing_page": (
                "https://braingraph.org/cms/download-pit-group-connectomes/"
            ),
            "archive": archive_provenance,
            "archive_expected_sha256": ARCHIVE_SHA256,
            "archive_expected_bytes": ARCHIVE_BYTES,
            "extractor": tool_provenance,
            "archive_listing_sha256": sha256(listing_path),
            "extracted_tree_aggregate_sha256": aggregate.hexdigest(),
            "counterexample_file": invalid_filename,
            "counterexample_file_sha256": next(
                row["sha256"]
                for row in manifest_rows
                if row["file"] == invalid_filename
            )
            if invalid_filename
            else None,
        },
        "negative_control": control,
        "stage_runtimes_seconds": stages,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    session_chunks = write_compact_chunks(
        output, "claim_4_session_audit", session_rows, 200
    )
    manifest_chunks = write_compact_chunks(
        output, "claim_4_file_manifest", manifest_rows, 200
    )
    (output / "claim_4_subject_audit.json").write_text(
        json.dumps(subject_rows, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (output / "claim_4_negative_control.json").write_text(
        json.dumps(control, indent=2) + "\n", encoding="utf-8"
    )
    result["raw_artifact_chunks"] = {
        "session_audit": session_chunks,
        "file_manifest": manifest_chunks,
    }
    (output / "claim_4_result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    if not result["all_gates_pass"]:
        failed = [name for name, passed in gates.items() if not passed]
        raise RuntimeError("Claim 4 gates failed: " + ", ".join(failed))
    return result

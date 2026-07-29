#!/usr/bin/env python3
"""Construct and evaluator-blind audit a prospective additive Space candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "hugging_face_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "github_pat": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}

REQUIRED_CLAIM_MARKERS = [
    "## Exact source statement and assumptions",
    "## Executable method",
    "### Code",
    "### Raw machine-readable evidence",
    "### Claim contract and evaluation files",
    "## Provenance",
    "## Limitations and deviations",
    "Exact command",
    "Independent checker",
    "control",
    "Git SHA",
    "Runtime",
    "Compute",
    "Pinned environment",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts
    )


def build_candidate(judged: Path, overlay: Path, output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for source in files(judged):
        relative = source.relative_to(judged)
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    for source in files(overlay):
        relative = source.relative_to(overlay)
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def resolve_links(page: Path, candidate: Path) -> tuple[list[str], list[str]]:
    opened: list[str] = []
    missing: list[str] = []
    text = page.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0]
        resolved = (page.parent / clean).resolve()
        try:
            relative = resolved.relative_to(candidate.resolve()).as_posix()
        except ValueError:
            missing.append(f"{page.relative_to(candidate)} -> escapes candidate: {target}")
            continue
        if resolved.is_file():
            opened.append(relative)
        else:
            missing.append(f"{page.relative_to(candidate)} -> missing: {target}")
    return opened, missing


def secret_scan(candidate: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in files(candidate):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append({"path": path.relative_to(candidate).as_posix(), "type": label})
    return findings


def audit(judged: Path, candidate: Path) -> dict:
    logbook_path = candidate / "logbook.json"
    logbook = json.loads(logbook_path.read_text(encoding="utf-8"))
    opened = ["README.md", "logbook.json"]
    gaps: list[str] = []
    node_files: list[str] = []

    def traverse(node: dict) -> None:
        file_name = node["file"]
        node_files.append(file_name)
        path = candidate / file_name
        if not path.is_file():
            gaps.append(f"logbook node missing: {file_name}")
        else:
            opened.append(file_name)
            linked, missing = resolve_links(path, candidate)
            opened.extend(linked)
            gaps.extend(missing)
        for child in node.get("children", []):
            traverse(child)

    traverse(logbook["root"])

    claim_pages = [
        file_name
        for file_name in node_files
        if re.search(r"^pages/claim-[1-6]-", file_name)
    ]
    if len(claim_pages) != 6:
        gaps.append(f"expected six claim pages, found {len(claim_pages)}")
    for file_name in claim_pages:
        text = (candidate / file_name).read_text(encoding="utf-8")
        for marker in REQUIRED_CLAIM_MARKERS:
            if marker.lower() not in text.lower():
                gaps.append(f"{file_name}: missing marker {marker!r}")

    visibility = candidate / "pages" / "current-visibility" / "page.md"
    if visibility.is_file():
        text = visibility.read_text(encoding="utf-8")
        for claim in range(1, 7):
            if f"| {claim} |" not in text:
                gaps.append(f"visibility matrix missing Claim {claim}")
        if "| yes | yes | yes | yes | yes | yes |" not in text:
            gaps.append("visibility matrix has an incomplete capability row")
    else:
        gaps.append("visibility matrix missing")

    immediate_trackio_pages = sorted(
        path.parent.name
        for path in (candidate / "pages").glob("*/page.md")
    )
    for claim in range(1, 7):
        if not any(
            slug.startswith(f"claim-{claim}-")
            for slug in immediate_trackio_pages
        ):
            gaps.append(
                f"Trackio immediate pages missing canonical Claim {claim}"
            )

    claim4_raw_root = (
        candidate / "current" / "evidence" / "claim_4" / "raw"
    )
    pair_groups: dict[Path, list[Path]] = {}
    if claim4_raw_root.is_dir():
        for path in claim4_raw_root.rglob("claim_4_table3_pairs_*.json"):
            pair_groups.setdefault(path.parent, []).append(path)
    claim4_pair_audits: list[dict[str, object]] = []
    complete_pair_group = False
    for parent, paths in sorted(pair_groups.items()):
        rows: list[dict[str, object]] = []
        for path in sorted(paths):
            rows.extend(json.loads(path.read_text(encoding="utf-8")))
        cell_counts = {
            f"{metric}_{method}": sum(
                row.get("metric") == metric and row.get("method") == method
                for row in rows
            )
            for metric in ("diffusion", "geodesic")
            for method in ("CDOT", "FGW")
        }
        unique_pairs = {
            (str(row.get("left_subject")), str(row.get("right_subject")))
            for row in rows
        }
        max_bytes = max((path.stat().st_size for path in paths), default=0)
        valid = (
            len(rows) == 19_800
            and len(unique_pairs) == 4_950
            and all(count == 4_950 for count in cell_counts.values())
            and max_bytes <= 100_000
            and (parent / "claim_4_table3_result.json").is_file()
            and (parent / "claim_4_independent_checker.json").is_file()
        )
        complete_pair_group = complete_pair_group or valid
        claim4_pair_audits.append(
            {
                "directory": parent.relative_to(candidate).as_posix(),
                "chunks": len(paths),
                "rows": len(rows),
                "unique_pairs": len(unique_pairs),
                "cell_counts": cell_counts,
                "max_chunk_bytes": max_bytes,
                "result_and_checker_colocated": (
                    (parent / "claim_4_table3_result.json").is_file()
                    and (parent / "claim_4_independent_checker.json").is_file()
                ),
                "complete_evaluator_visible_group": valid,
            }
        )
    if not complete_pair_group:
        gaps.append(
            "Claim 4 lacks one evaluator-visible raw directory containing "
            "19,800 rows, 4,950 pairs, four 4,950-row cells, colocated result "
            "and checker, and only <=100 kB chunks"
        )

    judged_paths = {path.relative_to(judged).as_posix() for path in files(judged)}
    candidate_paths = {path.relative_to(candidate).as_posix() for path in files(candidate)}
    missing_old = sorted(judged_paths - candidate_paths)
    if missing_old:
        gaps.extend(f"protected path missing: {path}" for path in missing_old)

    protected_page_hashes: list[dict[str, object]] = []
    for path in files(judged):
        relative = path.relative_to(judged)
        if relative.parts and relative.parts[0] == "pages":
            candidate_path = candidate / relative
            same = candidate_path.is_file() and sha256(path) == sha256(candidate_path)
            protected_page_hashes.append({"path": relative.as_posix(), "byte_identical": same})
            if not same:
                gaps.append(f"protected page changed: {relative.as_posix()}")

    secrets = secret_scan(candidate)
    if secrets:
        gaps.extend(f"secret-pattern finding: {item['path']} ({item['type']})" for item in secrets)

    opened_unique = sorted(set(opened))
    return {
        "audit_mode": "evaluator-blind traversal from README.md and logbook.json",
        "candidate_root": str(candidate),
        "files_opened": opened_unique,
        "files_opened_count": len(opened_unique),
        "canonical_node_files": node_files,
        "claim_pages_found": len(claim_pages),
        "protected_judged_paths": len(judged_paths),
        "candidate_paths": len(candidate_paths),
        "old_file_set_is_subset": not missing_old,
        "protected_pages_byte_identical": all(
            entry["byte_identical"] for entry in protected_page_hashes
        ),
        "protected_page_checks": protected_page_hashes,
        "claim4_raw_pair_audits": claim4_pair_audits,
        "secret_pattern_findings": secrets,
        "gaps": gaps,
        "all_gates_pass": not gaps,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judged", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    build_candidate(args.judged.resolve(), args.overlay.resolve(), args.candidate.resolve())
    report = audit(args.judged.resolve(), args.candidate.resolve())
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "all_gates_pass": report["all_gates_pass"],
                "files_opened": report["files_opened_count"],
                "candidate_paths": report["candidate_paths"],
                "gaps": len(report["gaps"]),
            }
        )
    )
    if not report["all_gates_pass"]:
        for gap in report["gaps"]:
            print(f"GAP: {gap}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

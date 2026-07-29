#!/usr/bin/env python3
"""Materialize JSON blocks that a formal orx run printed into its log."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


PATTERN = re.compile(
    r"^=== RAW_JSON_BEGIN (?P<path>.+?) ===\n"
    r"(?P<body>.*?)"
    r"^=== RAW_JSON_END (?P=path) ===$",
    re.MULTILINE | re.DOTALL,
)
LOG_SIZE = re.compile(r"\bof (?P<bytes>\d+)\b")
RANGE_BYTES = 900_000


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_complete_log(run_id: str) -> str:
    probe = subprocess.run(
        ["orx", "logs", run_id, "--head", "--bytes", "1"],
        capture_output=True,
        check=True,
    )
    stderr = probe.stderr.decode().strip()
    match = LOG_SIZE.search(stderr)
    if match is None:
        raise SystemExit(f"could not determine log size from: {stderr!r}")
    total_bytes = int(match.group("bytes"))
    chunks: list[bytes] = []
    for start in range(0, total_bytes, RANGE_BYTES):
        end = min(total_bytes, start + RANGE_BYTES)
        result = subprocess.run(
            ["orx", "logs", run_id, "--range", f"{start}:{end}"],
            capture_output=True,
            check=True,
        )
        expected_bytes = end - start
        data = result.stdout
        if len(data) == expected_bytes + 1 and data.endswith(b"\n"):
            data = data[:-1]
        if len(data) != expected_bytes:
            raise SystemExit(
                f"range {start}:{end} returned {len(data)} bytes; "
                f"expected {expected_bytes}"
            )
        chunks.append(data)
    return b"".join(chunks).decode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_id")
    parser.add_argument("--contains", action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    text = read_complete_log(args.run_id)
    args.output.mkdir(parents=True, exist_ok=True)
    manifest_by_path: dict[str, dict[str, object]] = {}
    for match in PATTERN.finditer(text):
        source = match.group("path")
        if not any(selector in source for selector in args.contains):
            continue
        body = match.group("body")
        json.loads(body)
        data = body.encode()
        destination = args.output / Path(source).name
        previous = manifest_by_path.get(destination.name)
        if previous is not None:
            if previous["sha256"] != digest(data):
                raise SystemExit(
                    f"conflicting repeated JSON block for {destination.name}"
                )
            continue
        destination.write_bytes(data)
        manifest_by_path[destination.name] = {
            "source": source,
            "path": destination.name,
            "bytes": len(data),
            "sha256": digest(data),
        }
    manifest = list(manifest_by_path.values())
    if not manifest:
        raise SystemExit("no matching JSON blocks found")
    manifest_path = args.output / "materialization_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "formal_run_id": args.run_id,
                "selectors": args.contains,
                "files": manifest,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"files": len(manifest), "output": str(args.output)}))


if __name__ == "__main__":
    main()

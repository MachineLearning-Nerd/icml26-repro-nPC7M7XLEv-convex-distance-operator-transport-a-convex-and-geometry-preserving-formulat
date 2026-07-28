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


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_id")
    parser.add_argument("--contains", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bytes", type=int, default=2_000_000)
    args = parser.parse_args()
    text = subprocess.check_output(
        [
            "orx",
            "logs",
            args.run_id,
            "--head",
            "--bytes",
            str(args.bytes),
        ],
        text=True,
    )
    args.output.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, object]] = []
    for match in PATTERN.finditer(text):
        source = match.group("path")
        if args.contains not in source:
            continue
        body = match.group("body")
        json.loads(body)
        data = body.encode()
        destination = args.output / Path(source).name
        destination.write_bytes(data)
        manifest.append(
            {
                "source": source,
                "path": destination.name,
                "bytes": len(data),
                "sha256": digest(data),
            }
        )
    if not manifest:
        raise SystemExit("no matching JSON blocks found")
    manifest_path = args.output / "materialization_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "formal_run_id": args.run_id,
                "selector": args.contains,
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

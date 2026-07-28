#!/usr/bin/env python3
"""Regenerate the exact text upload allowlist and SHA-256 release manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def files(root: Path, exclude_manifest: bool = False) -> list[Path]:
    paths = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        if exclude_manifest and relative == "current/manifests/release_manifest.json":
            continue
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("overlay", type=Path)
    args = parser.parse_args()
    root = args.overlay.resolve()
    manifest_dir = root / "current" / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    allowlist = manifest_dir / "upload_allowlist.txt"
    release_manifest = manifest_dir / "release_manifest.json"

    all_paths = {
        path.relative_to(root).as_posix()
        for path in files(root)
    }
    all_paths.update(
        {
            "current/manifests/upload_allowlist.txt",
            "current/manifests/release_manifest.json",
        }
    )
    allowlist.write_text("\n".join(sorted(all_paths)) + "\n", encoding="utf-8")

    entries = [
        {
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in files(root, exclude_manifest=True)
    ]
    release_manifest.write_text(
        json.dumps(
            {
                "scope": "exact text-only additive upload overlay; this manifest excludes only its own recursive hash",
                "files": entries,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "allowlist_paths": len(all_paths),
                "manifest_entries": len(entries),
                "manifest_sha256": sha256(release_manifest),
            }
        )
    )


if __name__ == "__main__":
    main()

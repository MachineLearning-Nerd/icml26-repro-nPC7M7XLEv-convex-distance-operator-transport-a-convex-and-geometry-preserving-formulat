#!/usr/bin/env python3
"""Publish an exact text-only overlay to an existing Hugging Face Space."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from huggingface_hub import CommitOperationAdd, HfApi


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--allowlist", type=Path, required=True)
    parser.add_argument("--parent-commit", required=True)
    parser.add_argument("--commit-message", required=True)
    args = parser.parse_args()

    overlay = args.overlay.resolve()
    allowlist = args.allowlist.resolve()
    paths = [
        line.strip()
        for line in allowlist.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(paths) != len(set(paths)):
        raise RuntimeError("upload allowlist contains duplicate paths")

    actual_paths = sorted(
        path.relative_to(overlay).as_posix()
        for path in overlay.rglob("*")
        if path.is_file() and ".cache" not in path.relative_to(overlay).parts
    )
    if sorted(paths) != actual_paths:
        missing = sorted(set(actual_paths) - set(paths))
        extra = sorted(set(paths) - set(actual_paths))
        raise RuntimeError(
            f"allowlist mismatch: unlisted={missing}, nonexistent={extra}"
        )

    operations = []
    for relative in paths:
        source = overlay / relative
        source.read_text(encoding="utf-8")
        operations.append(
            CommitOperationAdd(path_in_repo=relative, path_or_fileobj=source)
        )

    api = HfApi()
    before = api.repo_info(
        repo_id=args.repo_id,
        repo_type="space",
        revision="main",
    ).sha
    if before != args.parent_commit:
        raise RuntimeError(
            f"Space head changed before upload: {before} != {args.parent_commit}"
        )

    commit = api.create_commit(
        repo_id=args.repo_id,
        repo_type="space",
        revision="main",
        parent_commit=args.parent_commit,
        operations=operations,
        commit_message=args.commit_message,
        commit_description=(
            "Additive text-only Lean evidence release. "
            f"Parent revision: {args.parent_commit}. "
            f"Allowlisted files: {len(operations)}."
        ),
    )
    print(
        json.dumps(
            {
                "repo_id": args.repo_id,
                "parent_commit": args.parent_commit,
                "commit_id": commit.oid,
                "uploaded_files": len(operations),
            }
        )
    )


if __name__ == "__main__":
    main()

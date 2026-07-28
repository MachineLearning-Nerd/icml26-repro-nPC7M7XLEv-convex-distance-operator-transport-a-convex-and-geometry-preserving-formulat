"""Fixed cumulative reproduction entrypoint inherited by every experiment."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path

from threadpoolctl import threadpool_limits

from . import __version__
from .claim1 import run as run_claim_1
from .claim1_checker import check as check_claim_1
from .claim2 import run as run_claim_2
from .claim2_checker import check as check_claim_2
from .claim4 import run as run_claim_4
from .claim4_checker import check as check_claim_4
from .claim5 import run as run_claim_5
from .claim5_checker import check as check_claim_5
from .claim6 import run as run_claim_6
from .claim6_checker import check as check_claim_6


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def git_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()


def main() -> None:
    started = time.perf_counter()
    config = json.loads(Path("campaign.json").read_text())
    runtime_dir = Path(config["output_directory"])
    runtime_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, object] = {}
    with threadpool_limits(limits=config["compute_contract"]["thread_limit"]):
        if 1 in config["active_claims"]:
            claim_dir = runtime_dir / "claim_1"
            primary = run_claim_1(claim_dir)
            independent = check_claim_1(claim_dir)
            results["claim_1"] = {
                "primary": primary,
                "independent_checker": independent,
            }
        if 2 in config["active_claims"]:
            claim_dir = runtime_dir / "claim_2"
            primary = run_claim_2(claim_dir)
            independent = check_claim_2(claim_dir)
            results["claim_2"] = {
                "primary": primary,
                "independent_checker": independent,
            }
        if 6 in config["active_claims"]:
            claim_dir = runtime_dir / "claim_6"
            primary = run_claim_6(claim_dir)
            independent = check_claim_6(claim_dir)
            results["claim_6"] = {
                "primary": primary,
                "independent_checker": independent,
            }
        if 4 in config["active_claims"]:
            claim_dir = runtime_dir / "claim_4"
            primary = run_claim_4(claim_dir)
            independent = check_claim_4(claim_dir)
            results["claim_4"] = {
                "primary": primary,
                "independent_checker": independent,
            }
        if 5 in config["active_claims"]:
            claim_dir = runtime_dir / "claim_5"
            primary = run_claim_5(claim_dir)
            independent = check_claim_5(claim_dir)
            results["claim_5"] = {
                "primary": primary,
                "independent_checker": independent,
            }
    elapsed = time.perf_counter() - started
    provenance = {
        "package_version": __version__,
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "allocated_logical_cpus": os.cpu_count(),
        "enforced_thread_limit": config["compute_contract"]["thread_limit"],
        "estimated_cores": config["compute_contract"]["estimated_cores"],
        "selected_backend": config["compute_contract"]["selected_backend"],
        "selected_flavor": config["compute_contract"]["selected_flavor"],
        "runtime_seconds": elapsed,
        "active_claims": config["active_claims"],
    }
    summary = {
        "all_gates_pass": all(
            claim["primary"]["all_gates_pass"]
            and claim["independent_checker"]["all_gates_pass"]
            for claim in results.values()
        ),
        "results": results,
        "provenance": provenance,
    }
    summary_path = runtime_dir / "run_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("=== CDOT_REPRODUCTION_SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print("=== CDOT_REPRODUCTION_RAW_ARTIFACTS ===")
    for path in sorted(runtime_dir.rglob("*.json")):
        print(
            json.dumps(
                {
                    "path": str(path),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
        )
        if path.stat().st_size <= 100_000:
            print(f"=== RAW_JSON_BEGIN {path} ===")
            print(path.read_text(encoding="utf-8"), end="")
            print(f"=== RAW_JSON_END {path} ===")
    if not summary["all_gates_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

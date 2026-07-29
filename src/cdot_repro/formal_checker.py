"""Pinned Lean/mathlib kernel checker for theoretical CDOT claims."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import tarfile
import time
import urllib.request
from pathlib import Path


ELAN_VERSION = "v4.1.2"
ELAN_ARCHIVE = "elan-x86_64-unknown-linux-gnu.tar.gz"
ELAN_URL = (
    f"https://github.com/leanprover/elan/releases/download/"
    f"{ELAN_VERSION}/{ELAN_ARCHIVE}"
)
ELAN_SHA256 = "f81c2e48c1588d4612cd2c8851947898a45ac8d72748a07dff3a5694f1cf589b"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.19.0"
MATHLIB_REVISION = "v4.19.0"
MATHLIB_COMMIT = "c44e0c8ee63ca166450922a373c7409c5d26b00b"
THEOREMS = [
    "CDOTFormal.claim1_compact_attainment",
    "CDOTFormal.claim1_cdot_objective_jensen",
    "CDOTFormal.claim2_weighted_fusion_triangle",
    "CDOTFormal.claim2_dispersion_gap",
    "CDOTFormal.claim6_three_obligation_bound",
    "CDOTFormal.claim6_consistency_squeeze",
]
FORBIDDEN_SOURCE_TOKENS = ("sorry", "admit", "axiom ", "unsafe ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _run(
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    expect_success: bool = True,
) -> dict[str, object]:
    started = time.perf_counter()
    process = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    elapsed = time.perf_counter() - started
    record = {
        "argv": args,
        "returncode": process.returncode,
        "runtime_seconds": elapsed,
        "stdout": process.stdout,
    }
    if expect_success and process.returncode != 0:
        raise RuntimeError(json.dumps(record, indent=2))
    return record


def _install_elan(work: Path) -> tuple[Path, dict[str, object]]:
    archive = work / ELAN_ARCHIVE
    request = urllib.request.Request(
        ELAN_URL,
        headers={"User-Agent": "OpenResearch-CDOT-Reproduction/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        archive.write_bytes(response.read())
    observed_hash = _sha256(archive)
    if observed_hash != ELAN_SHA256:
        raise RuntimeError(
            f"elan archive hash mismatch: {observed_hash} != {ELAN_SHA256}"
        )
    extract_dir = work / "elan-bootstrap"
    extract_dir.mkdir()
    with tarfile.open(archive, "r:gz") as bundle:
        bundle.extractall(extract_dir, filter="data")
    elan_init = extract_dir / "elan-init"
    if not elan_init.is_file():
        raise RuntimeError("elan-init missing from pinned archive")
    elan_init.chmod(0o755)
    return elan_init, {
        "url": ELAN_URL,
        "expected_sha256": ELAN_SHA256,
        "observed_sha256": observed_hash,
        "bytes": archive.stat().st_size,
    }


def run(output: Path) -> tuple[dict[str, object], dict[str, object]]:
    """Compile the certificate, replay it independently, and reject a false proof."""

    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    formal_source = Path("formal").resolve()
    work = output / "lean-work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    project = work / "formal"
    shutil.copytree(formal_source, project)

    source_text = (project / "CDOTProofs.lean").read_text(encoding="utf-8")
    forbidden_hits = [
        token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text.lower()
    ]
    if forbidden_hits:
        raise RuntimeError(f"forbidden proof tokens: {forbidden_hits}")

    elan_init, download = _install_elan(work)
    elan_home = work / "elan-home"
    env = os.environ.copy()
    env["ELAN_HOME"] = str(elan_home)
    env["PATH"] = f"{elan_home / 'bin'}:{env.get('PATH', '')}"
    env["ELAN_NO_OVERRIDE_NOTICE"] = "1"

    install = _run(
        [
            str(elan_init),
            "-y",
            "--no-modify-path",
            "--default-toolchain",
            LEAN_TOOLCHAIN,
        ],
        cwd=work,
        env=env,
    )
    lean_version = _run(["lean", "--version"], cwd=project, env=env)
    lake_version = _run(["lake", "--version"], cwd=project, env=env)
    update = _run(["lake", "update"], cwd=project, env=env)
    cache = _run(["lake", "exe", "cache", "get"], cwd=project, env=env)
    primary_compile = _run(
        ["lake", "env", "lean", "CDOTProofs.lean"],
        cwd=project,
        env=env,
    )
    library_build = _run(
        ["lake", "build", "CDOTProofs"],
        cwd=project,
        env=env,
    )
    independent_compile = _run(
        ["lake", "env", "lean", "IndependentReplay.lean"],
        cwd=project,
        env=env,
    )
    negative_compile = _run(
        ["lake", "env", "lean", "NegativeControl.lean"],
        cwd=project,
        env=env,
        expect_success=False,
    )
    manifest = json.loads((project / "lake-manifest.json").read_text())
    package_revisions = {
        package["name"]: package.get("rev")
        for package in manifest.get("packages", [])
    }
    gates = {
        "pinned_elan_archive_hash": download["observed_sha256"] == ELAN_SHA256,
        "pinned_lean_toolchain_file": (
            project / "lean-toolchain"
        ).read_text(encoding="utf-8").strip()
        == LEAN_TOOLCHAIN,
        "reported_lean_version": "version 4.19.0" in lean_version["stdout"],
        "exact_mathlib_manifest_commit": package_revisions.get("mathlib")
        == MATHLIB_COMMIT,
        "no_forbidden_source_tokens": not forbidden_hits,
        "primary_kernel_compile_passed": primary_compile["returncode"] == 0,
        "lake_library_build_passed": library_build["returncode"] == 0,
        "all_named_theorems_printed": all(
            theorem in primary_compile["stdout"] for theorem in THEOREMS
        ),
        "independent_replay_passed": independent_compile["returncode"] == 0,
        "negative_control_rejected": negative_compile["returncode"] != 0,
    }
    primary = {
        "claim_scope": [1, 2, 6],
        "verdict": "VERIFIED" if all(gates.values()) else "BLOCKED",
        "proof_system": "Lean 4 kernel plus pinned mathlib",
        "lean_toolchain": LEAN_TOOLCHAIN,
        "mathlib_requested_revision": MATHLIB_REVISION,
        "resolved_package_revisions": package_revisions,
        "download": download,
        "source_sha256": _sha256(project / "CDOTProofs.lean"),
        "theorems": THEOREMS,
        "forbidden_source_tokens": list(FORBIDDEN_SOURCE_TOKENS),
        "gates": gates,
        "commands": {
            "install": install,
            "lean_version": lean_version,
            "lake_version": lake_version,
            "lake_update": update,
            "mathlib_cache": cache,
            "primary_compile": primary_compile,
            "library_build": library_build,
            "negative_control_compile": negative_compile,
        },
        "compute": {
            "estimated_cores": 2,
            "selected_backend": "hf",
            "selected_flavor": "cpu-upgrade",
            "actual_logical_cpus": os.cpu_count(),
            "platform": platform.platform(),
        },
        "all_gates_pass": all(gates.values()),
    }
    independent_gates = {
        "separate_compilation_unit": True,
        "replay_compile_passed": independent_compile["returncode"] == 0,
        "negative_control_failed_to_compile": negative_compile["returncode"] != 0,
        "primary_source_hash_recomputed": _sha256(
            project / "CDOTProofs.lean"
        )
        == primary["source_sha256"],
    }
    independent = {
        "gates": independent_gates,
        "command": independent_compile,
        "all_gates_pass": all(independent_gates.values()),
    }
    (output / "formal_primary.json").write_text(
        json.dumps(primary, indent=2) + "\n", encoding="utf-8"
    )
    (output / "formal_independent_checker.json").write_text(
        json.dumps(independent, indent=2) + "\n", encoding="utf-8"
    )
    print("=== LEAN_FORMAL_GATE_SUMMARY ===")
    print(
        json.dumps(
            {
                "primary_gates": gates,
                "independent_gates": independent_gates,
                "lean_version": lean_version["stdout"].strip(),
                "resolved_mathlib_commit": package_revisions.get("mathlib"),
                "negative_control_returncode": negative_compile["returncode"],
            },
            indent=2,
        )
    )
    if not primary["all_gates_pass"] or not independent["all_gates_pass"]:
        raise RuntimeError("formal proof gates failed")
    return primary, independent

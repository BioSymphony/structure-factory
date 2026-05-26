#!/usr/bin/env python3
"""Apply the bridge-tool gate fixes to a generated bridge manifest.

The bridge tool's `preflight` rejects a paid launch when ANY of these are
missing or wrong:
  - runpod.image_capabilities must declare git (pytorch/pytorch image ships
    git; we declare explicitly per bridge schema).
  - startup.progress.http_status_server_port must be set; matching port must
    appear in runpod.ports as `<port>/http`.
  - access.http_proxy_required must be true (declares the HTTP service).
  - For SECURE+NV pods, gpuTypeIds must include options that the data center
    actually has capacity for right now — the bridge tool itself doesn't
    enforce this, but `create-pod` fails with HTTP 500 when no GPUs match.

This script idempotently applies all of those to an existing manifest JSON.

Usage:
  python3 scripts/structure_factory/patch_bridge_manifest_for_live_gates.py \
    runpod/bridge-manifests/pd-l1-binder-hunt-canary.json
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

WIDE_GPU_TYPES = [
    "NVIDIA L40S",
    "NVIDIA L40",
    "NVIDIA RTX A6000",
    "NVIDIA RTX 6000 Ada Generation",
    "NVIDIA A40",
    "NVIDIA A100 80GB PCIe",
    "NVIDIA A100-SXM4-80GB",
    "NVIDIA GeForce RTX 4090",
    "NVIDIA GeForce RTX 5090",
    "NVIDIA H100 80GB HBM3",
    "NVIDIA H100 PCIe",
    "NVIDIA H100 NVL",
]

PROGRESS_PORT = 8888
ARTIFACT_PORT = 8000  # post-completion HTTP file server (inspection_hold)


def patch(manifest_path: Path, dry_run: bool = False) -> bool:
    m = json.loads(manifest_path.read_text())
    changed = False

    rp = m.setdefault("runpod", {})

    # 1. image_capabilities
    if rp.get("image_capabilities") != ["git"]:
        rp["image_capabilities"] = ["git"]
        changed = True

    # 2. progress channel (live, sanitized)
    startup = m.setdefault("startup", {})
    progress = startup.setdefault("progress", {})
    if progress.get("http_status_server_port") != PROGRESS_PORT:
        progress["http_status_server_port"] = PROGRESS_PORT
        progress.setdefault("log_tail_bytes", 4096)
        progress.setdefault("include_log_tail", False)
        changed = True

    # 3. artifact inspection server (post-completion, full /workspace)
    inspection = startup.setdefault("inspection", {})
    if inspection.get("http_artifact_server_port") != ARTIFACT_PORT:
        inspection["http_artifact_server_port"] = ARTIFACT_PORT
        inspection.setdefault("hold_after_success_seconds", 900)  # 15 min window
        changed = True

    # 4. ports list — must contain "<PORT>/http" for both progress + artifact
    ports = rp.get("ports") or []
    for p in (PROGRESS_PORT, ARTIFACT_PORT):
        port_str = f"{p}/http"
        if port_str not in ports:
            ports.append(port_str)
            changed = True
    rp["ports"] = ports

    # 5. access.http_proxy_required
    access = m.setdefault("access", {})
    if access.get("http_proxy_required") is not True:
        access["http_proxy_required"] = True
        changed = True

    # 6. Widen GPU types
    cur_gpus = set(rp.get("gpuTypeIds") or [])
    if not cur_gpus.issuperset(set(WIDE_GPU_TYPES)):
        rp["gpuTypeIds"] = WIDE_GPU_TYPES
        changed = True

    if dry_run:
        print(json.dumps({
            "would_change": changed,
            "image_capabilities": rp.get("image_capabilities"),
            "progress_port": progress.get("http_status_server_port"),
            "ports": rp.get("ports"),
            "http_proxy_required": access.get("http_proxy_required"),
            "gpu_type_count": len(rp.get("gpuTypeIds") or []),
        }, indent=2))
        return changed

    if changed:
        manifest_path.write_text(json.dumps(m, indent=2) + "\n")
        print(f"  patched: {manifest_path}")
    else:
        print(f"  no-op: {manifest_path} already has all live gates")
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.manifest.is_file():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        return 2
    patch(args.manifest, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Wrapper for Dunbrack Lab IPSAE applied to Boltz outputs.

Vendored implementation: scripts/structure_factory/vendor/ipsae/ipsae.py
Reference: https://github.com/DunbrackLab/IPSAE (MIT)
Paper: Dunbrack 2025, "Rēs ipSAE loquunt", bioRxiv 2025.02.10.637595v2

Why ipSAE: a 2025 meta-analysis of 3,766 experimentally characterised binders
(bioRxiv 670059) shows ipSAE > iPAE > iPTM for predicting wet-lab success.
Threshold ipSAE >= 0.6 is the working cutoff for "likely binder."

This script:
  1. Locates the vendored ipsae.py
  2. Invokes it with the Boltz CIF + PAE NPZ
  3. Parses the chain-chain output file
  4. Emits a tidy JSON for the (binder, target) chain pair
  5. Writes the summary alongside the inputs (or to --output)

Boltz typical outputs:
  artifacts/boltz/prediction.cif
  artifacts/boltz/prediction.npz       (contains pae array)

Usage:
  python compute_ipsae.py \\
      --boltz-cif .../prediction.cif \\
      --pae-npz .../prediction.npz \\
      [--binder-chain B] \\
      [--target-chain A] \\
      [--pae-cutoff 10] \\
      [--dist-cutoff 10] \\
      [--output .../prediction.ipsae.json]

Stdlib only (numpy is required by the vendored script, not by this wrapper).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

THIS = Path(__file__).resolve()
VENDOR_IPSAE = THIS.parent / "vendor" / "ipsae" / "ipsae.py"


def find_chain_chain_txt(stem: Path) -> Path | None:
    """ipsae.py writes a `{stem}.txt` chain-chain summary alongside the input."""
    candidate = stem.with_suffix(".txt")
    if candidate.exists():
        return candidate
    # Fallback: glob {stem}_*.txt
    for cand in stem.parent.glob(f"{stem.name}_*.txt"):
        if "_byres" not in cand.name:
            return cand
    return None


def parse_chain_chain(path: Path) -> list[dict]:
    """Parse the columnar chain-chain output. Returns list of row dicts."""
    rows: list[dict] = []
    columns: list[str] | None = None
    with path.open() as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if columns is None and line.startswith("Chn1"):
                columns = line.split()
                continue
            if columns is None:
                continue
            parts = line.split()
            if len(parts) != len(columns):
                continue
            row = {}
            for col, val in zip(columns, parts):
                try:
                    row[col] = float(val)
                except ValueError:
                    row[col] = val
            rows.append(row)
    return rows


def select_pair(rows: list[dict], binder: str, target: str) -> dict | None:
    """Pick the row matching (binder, target) — symmetric search."""
    for r in rows:
        c1 = str(r.get("Chn1", "")).strip()
        c2 = str(r.get("Chn2", "")).strip()
        if (c1 == binder and c2 == target) or (c1 == target and c2 == binder):
            return r
    return None


def compute(args: argparse.Namespace) -> int:
    boltz_cif = Path(args.boltz_cif).resolve()
    pae_npz = Path(args.pae_npz).resolve()

    if not VENDOR_IPSAE.exists():
        raise SystemExit(
            f"vendored ipsae.py not found at {VENDOR_IPSAE}. "
            f"Re-run: curl -fsSL https://raw.githubusercontent.com/DunbrackLab/IPSAE/main/ipsae.py "
            f"-o {VENDOR_IPSAE}"
        )
    if not boltz_cif.exists():
        raise SystemExit(f"Boltz CIF not found: {boltz_cif}")
    if not pae_npz.exists():
        raise SystemExit(f"PAE NPZ not found: {pae_npz}")

    pae_cutoff = float(args.pae_cutoff)
    dist_cutoff = float(args.dist_cutoff)

    pae_str = f"{pae_cutoff:g}"
    dist_str = f"{dist_cutoff:g}"
    stem = boltz_cif.with_suffix("")
    expected_txt = stem.parent / f"{stem.name}_{pae_str}_{dist_str}.txt"

    cmd = [
        sys.executable,
        str(VENDOR_IPSAE),
        str(pae_npz),
        str(boltz_cif),
        pae_str,
        dist_str,
    ]
    print(f"[ipsae] {' '.join(cmd)}", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout)
    if proc.returncode != 0:
        print(proc.stdout, file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(f"ipsae.py failed (exit {proc.returncode})")

    chain_chain_path = expected_txt if expected_txt.exists() else find_chain_chain_txt(stem)
    if chain_chain_path is None:
        raise SystemExit(
            f"ipsae.py succeeded but chain-chain output missing. "
            f"Expected something like {expected_txt}"
        )

    rows = parse_chain_chain(chain_chain_path)
    pair = select_pair(rows, args.binder_chain, args.target_chain)

    summary = {
        "schema_version": "compute_ipsae.v1",
        "boltz_cif": str(boltz_cif),
        "pae_npz": str(pae_npz),
        "pae_cutoff": pae_cutoff,
        "dist_cutoff": dist_cutoff,
        "binder_chain": args.binder_chain,
        "target_chain": args.target_chain,
        "ipsae_chain_chain_path": str(chain_chain_path),
        "ipsae_byres_path": str(stem.parent / f"{stem.name}_{pae_str}_{dist_str}_byres.txt"),
        "ipsae_pml_path": str(stem.parent / f"{stem.name}_{pae_str}_{dist_str}.pml"),
        "all_chain_pairs": rows,
        "selected_pair": pair,
    }

    if pair is not None:
        summary["ipSAE"] = pair.get("ipSAE")
        summary["ipSAE_d0chn"] = pair.get("ipSAE_d0chn")
        summary["ipSAE_d0dom"] = pair.get("ipSAE_d0dom")
        summary["ipTM_af"] = pair.get("ipTM_af")
        summary["pDockQ"] = pair.get("pDockQ")
        summary["pDockQ2"] = pair.get("pDockQ2")
        summary["LIS"] = pair.get("LIS")
        summary["n_interface_residues_chain1"] = pair.get("nres1")
        summary["n_interface_residues_chain2"] = pair.get("nres2")
        summary["passes_ipsae_threshold_0p6"] = (
            isinstance(pair.get("ipSAE"), float) and pair["ipSAE"] >= 0.60
        )

    out_path = Path(args.output) if args.output else (
        boltz_cif.parent / f"{boltz_cif.stem}.ipsae.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"[ok] {out_path}")

    if pair is None:
        print(
            f"[warn] no chain-chain row for ({args.binder_chain}, {args.target_chain}); "
            f"available pairs: {[(r.get('Chn1'), r.get('Chn2')) for r in rows]}",
            file=sys.stderr,
        )
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--boltz-cif", required=True)
    p.add_argument("--pae-npz", required=True)
    p.add_argument("--binder-chain", default="B")
    p.add_argument("--target-chain", default="A")
    p.add_argument("--pae-cutoff", default=10.0, type=float)
    p.add_argument("--dist-cutoff", default=10.0, type=float)
    p.add_argument("--output", default=None, help="Output JSON path (default: alongside CIF)")
    p.add_argument("--timeout", default=300, type=int)
    args = p.parse_args(argv)
    return compute(args)


if __name__ == "__main__":
    raise SystemExit(main())

"""Check native prediction bundles without importing a model runtime."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

from .target_verifier import TargetVerificationError, _read_cif_loop


class PredictionArtifactError(ValueError):
    """A prediction bundle is missing required scientific outputs."""


def structure_atom_count(path: Path) -> int:
    """Require atom identities and finite Cartesian coordinates in PDB/mmCIF."""
    text = path.read_text(encoding="utf-8")
    count = 0
    try:
        if path.suffix.lower() == ".pdb":
            for line in text.splitlines():
                if not line.startswith(("ATOM  ", "HETATM")):
                    continue
                if not line[12:16].strip() or not line[17:20].strip():
                    raise ValueError
                int(line[22:26])
                if not all(math.isfinite(float(line[a:b])) for a, b in ((30, 38), (38, 46), (46, 54))):
                    raise ValueError
                count += 1
        else:
            lines = text.splitlines()
            cursor = 0
            while cursor < len(lines):
                parsed = _read_cif_loop(lines, cursor, "_atom_site.")
                if parsed is None:
                    cursor += 1
                    continue
                columns, rows, cursor = parsed
                required = ("group_PDB", "label_atom_id", "label_comp_id", "label_asym_id", "Cartn_x", "Cartn_y", "Cartn_z")
                if any(name not in columns for name in required) or len(set(columns)) != len(columns):
                    raise ValueError
                indices = {name: columns.index(name) for name in required}
                for row in rows:
                    if row[indices["group_PDB"]] not in {"ATOM", "HETATM"}:
                        raise ValueError
                    if any(row[indices[name]] in {"", ".", "?"} for name in required[1:4]):
                        raise ValueError
                    if not all(math.isfinite(float(row[indices[name]])) for name in required[4:]):
                        raise ValueError
                    count += 1
    except (ValueError, TargetVerificationError) as exc:
        raise PredictionArtifactError("prediction has invalid atom records") from exc
    if count == 0:
        raise PredictionArtifactError("prediction has no coordinate atoms")
    return count


def validate_boltz_bundle(root: Path, input_path: Path, expected_model_count: int) -> None:
    """Check Boltz 2.2.1 native structures and matching confidence summaries.

    The output naming contract is defined by the upstream v2.2.1 prediction
    writer. This verifies input record coverage, not biological correctness or
    the provenance of reused predictions.
    """
    suffixes = {".yaml", ".yml", ".fa", ".fas", ".fasta"}
    inputs = sorted(input_path.iterdir()) if input_path.is_dir() else [input_path]
    inputs = [path for path in inputs if path.suffix.lower() in suffixes]
    if not inputs or any(path.is_symlink() or not path.is_file() or not path.stat().st_size for path in inputs):
        raise PredictionArtifactError("prediction input records are missing or invalid")
    expected = {path.stem for path in inputs}
    if len(expected) != len(inputs):
        raise PredictionArtifactError("prediction input names are duplicated")

    structures: dict[tuple[str, int], Path] = {}
    summaries: dict[tuple[str, int], Path] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise PredictionArtifactError("prediction bundle contains a symbolic link")
        if not path.is_file() or path.parent.parent.name != "predictions":
            continue
        record = path.parent.name
        structure = re.fullmatch(r"(.+)_model_(\d+)\.(?:cif|pdb)", path.name)
        summary = re.fullmatch(r"confidence_(.+)_model_(\d+)\.json", path.name)
        match = structure or summary
        if match is None:
            continue
        if match[1] != record or record not in expected:
            raise PredictionArtifactError("prediction output identity differs from its input")
        key = (record, int(match[2]))
        destination = structures if structure else summaries
        if key in destination:
            raise PredictionArtifactError("prediction output identity is duplicated")
        destination[key] = path
    if not structures or structures.keys() != summaries.keys():
        raise PredictionArtifactError("prediction structures and confidence summaries must match")
    if {record for record, _ in structures} != expected:
        raise PredictionArtifactError("prediction outputs do not cover every input record")
    for record in expected:
        indices = sorted(index for name, index in structures if name == record)
        if len(indices) != expected_model_count or any(index != expected for expected, index in enumerate(indices)):
            raise PredictionArtifactError("prediction model indices are incomplete")
    for key, structure in structures.items():
        structure_atom_count(structure)
        confidence = json.loads(summaries[key].read_text(encoding="utf-8"))
        if not isinstance(confidence, dict):
            raise PredictionArtifactError("prediction confidence summary must be an object")
        for field in ("confidence_score", "complex_plddt", "ptm", "iptm"):
            value = confidence.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
                raise PredictionArtifactError("prediction confidence is missing or outside its native scale")

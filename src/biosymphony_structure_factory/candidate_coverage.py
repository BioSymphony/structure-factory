"""Check candidate-by-stage coverage against a separately declared contract."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


CONTRACT_VERSION = "structure-factory-candidate-coverage-v1"
OBSERVATIONS_VERSION = "structure-factory-candidate-observations-v1"
STATES = frozenset({"completed", "scientifically_rejected", "upstream_excluded", "pending", "missing", "failed"})
RESOLVED = frozenset({"completed", "scientifically_rejected", "upstream_excluded"})
_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
_HASH = re.compile(r"^[0-9a-f]{64}$")


class CandidateCoverageError(ValueError):
    """A coverage declaration or observation has an invalid shape."""


def contract_digest(contract: dict[str, Any]) -> str:
    encoded = json.dumps(contract, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return hashlib.sha256(encoded.encode("ascii")).hexdigest()


def _object(value: Any, required: set[str], optional: set[str] = frozenset()) -> dict[str, Any]:
    if not isinstance(value, dict) or required - value.keys() or value.keys() - required - optional:
        raise CandidateCoverageError("coverage object has missing or unknown fields")
    return value


def _id(value: Any) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise CandidateCoverageError("coverage ID must use lowercase letters, numbers, dots, underscores, or hyphens")
    return value


def _ids(value: Any, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise CandidateCoverageError("coverage IDs must be a nonempty list")
    result = [_id(item) for item in value]
    if len(result) != len(set(result)):
        raise CandidateCoverageError("coverage IDs must be unique")
    return result


def _hash(value: Any) -> str:
    if not isinstance(value, str) or not _HASH.fullmatch(value):
        raise CandidateCoverageError("coverage digest must be a lowercase SHA-256")
    return value


def _check_evidence(value: Any, root: Path) -> None:
    if not isinstance(value, list) or not value:
        raise CandidateCoverageError("resolved assessment needs nonempty evidence")
    seen: set[str] = set()
    for raw in value:
        item = _object(raw, {"path", "sha256"})
        rel = item["path"]
        if (
            not isinstance(rel, str) or not rel or "\\" in rel or ":" in rel
            or "\x00" in rel or PurePosixPath(rel).is_absolute()
            or any(part in {"", ".", ".."} for part in rel.split("/"))
        ):
            raise CandidateCoverageError("coverage evidence needs a contained relative path")
        if rel in seen:
            raise CandidateCoverageError("coverage evidence paths must be unique within a row")
        seen.add(rel)
        path = root / rel
        if any(parent.is_symlink() for parent in (path, *path.parents) if parent != root and root in parent.parents):
            raise CandidateCoverageError("coverage evidence must not traverse a symbolic link")
        if root not in path.resolve().parents or not path.is_file() or not path.stat().st_size:
            raise CandidateCoverageError("coverage evidence is missing, empty, or outside its root")
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != _hash(item["sha256"]):
            raise CandidateCoverageError("coverage evidence content differs from its declared hash")


def check_coverage(contract: Any, observations: Any, evidence_root: Path) -> dict[str, Any]:
    """Return completeness separately from input validity; write no files."""
    contract = _object(contract, {"schema_version", "candidate_ids", "stages"})
    if contract["schema_version"] != CONTRACT_VERSION:
        raise CandidateCoverageError("unsupported coverage contract version")
    candidates = _ids(contract["candidate_ids"])
    if not isinstance(contract["stages"], list) or not contract["stages"]:
        raise CandidateCoverageError("coverage contract needs stages")
    stages: dict[str, dict[str, Any]] = {}
    for raw in contract["stages"]:
        stage = _object(raw, {"stage_id", "protocol_sha256", "depends_on", "rejection_rules"})
        stage_id = _id(stage["stage_id"])
        _hash(stage["protocol_sha256"])
        dependencies = _ids(stage["depends_on"], allow_empty=True)
        if stage_id in stages or any(dependency not in stages for dependency in dependencies):
            raise CandidateCoverageError("coverage stages must be unique and ordered after their dependencies")
        if not isinstance(stage["rejection_rules"], list):
            raise CandidateCoverageError("rejection rules must be a list")
        rules: set[str] = set()
        for raw_rule in stage["rejection_rules"]:
            rule = _object(raw_rule, {"rule_id", "description"})
            rule_id = _id(rule["rule_id"])
            if rule_id in rules or not isinstance(rule["description"], str) or not rule["description"].strip():
                raise CandidateCoverageError("rejection rules need unique IDs and descriptions")
            rules.add(rule_id)
        stages[stage_id] = {**stage, "rules": rules}

    observations = _object(observations, {"schema_version", "contract_sha256", "observations"})
    if observations["schema_version"] != OBSERVATIONS_VERSION:
        raise CandidateCoverageError("unsupported coverage observations version")
    digest = contract_digest(contract)
    if _hash(observations["contract_sha256"]) != digest:
        raise CandidateCoverageError("observations do not match the declared coverage contract")
    if not isinstance(observations["observations"], list):
        raise CandidateCoverageError("coverage observations must be a list")
    root = Path(evidence_root).resolve()
    if not root.is_dir():
        raise CandidateCoverageError("coverage evidence root must be a directory")

    rows: dict[tuple[str, str], dict[str, Any]] = {}
    findings: list[str] = []
    invalid_candidates: set[str] = set()
    for raw in observations["observations"]:
        row = _object(raw, {"candidate_id", "stage_id", "protocol_sha256", "status", "evidence"}, {"rule_id", "upstream_stage_id"})
        candidate, stage_id = _id(row["candidate_id"]), _id(row["stage_id"])
        key = (candidate, stage_id)
        if candidate not in candidates or stage_id not in stages or key in rows:
            raise CandidateCoverageError("coverage observation is undeclared or duplicated")
        if _hash(row["protocol_sha256"]) != stages[stage_id]["protocol_sha256"]:
            raise CandidateCoverageError("coverage observation uses a different protocol")
        status = row["status"]
        if not isinstance(status, str) or status not in STATES:
            raise CandidateCoverageError("unsupported coverage status")
        if ("rule_id" in row) != (status == "scientifically_rejected") or ("upstream_stage_id" in row) != (status == "upstream_excluded"):
            raise CandidateCoverageError("coverage exclusion fields do not match the status")
        if status == "scientifically_rejected" and _id(row["rule_id"]) not in stages[stage_id]["rules"]:
            raise CandidateCoverageError("scientific rejection needs a predeclared stage rule")
        if status == "upstream_excluded" and _id(row["upstream_stage_id"]) not in stages[stage_id]["depends_on"]:
            raise CandidateCoverageError("upstream exclusion must name a direct dependency")
        if not isinstance(row["evidence"], list):
            raise CandidateCoverageError("coverage evidence must be a list")
        if status in {"completed", "scientifically_rejected"} or row["evidence"]:
            try:
                _check_evidence(row["evidence"], root)
            except CandidateCoverageError as exc:
                findings.append(f"{candidate}/{stage_id}: {exc}")
                invalid_candidates.add(candidate)
        rows[key] = row

    counts: Counter[str] = Counter()
    fully_assessed, excluded, unfinished = [], [], []
    for candidate in candidates:
        statuses = []
        for stage_id, stage in stages.items():
            row = rows.get((candidate, stage_id), {"status": "missing"})
            status = row["status"]
            statuses.append(status)
            counts[status] += 1
            dependencies = {parent: rows.get((candidate, parent), {}).get("status", "missing") for parent in stage["depends_on"]}
            if status in {"completed", "scientifically_rejected"} and any(value != "completed" for value in dependencies.values()):
                findings.append(f"{candidate}/{stage_id}: assessment has an unresolved or rejected dependency")
                invalid_candidates.add(candidate)
            if status == "upstream_excluded" and dependencies[row["upstream_stage_id"]] not in {"scientifically_rejected", "upstream_excluded"}:
                findings.append(f"{candidate}/{stage_id}: upstream exclusion has no scientific rejection")
                invalid_candidates.add(candidate)
        if candidate in invalid_candidates:
            unfinished.append(candidate)
        elif all(status == "completed" for status in statuses):
            fully_assessed.append(candidate)
        elif all(status in RESOLVED for status in statuses):
            excluded.append(candidate)
        else:
            unfinished.append(candidate)
    valid = not findings
    complete = valid and not unfinished
    return {
        "ok": complete,
        "valid": valid,
        "complete": complete,
        "contract_sha256": digest,
        "expected_pairs": len(candidates) * len(stages),
        "observed_pairs": len(rows),
        "status_counts": {state: counts[state] for state in sorted(STATES)},
        "fully_assessed_candidate_ids": fully_assessed,
        "excluded_candidate_ids": excluded,
        "unfinished_candidate_ids": unfinished,
        "findings": findings,
    }

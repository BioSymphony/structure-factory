"""Dependency-free public validator for Structure Factory repos."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_CLAIM_LEVELS = {
    "planning",
    "public_demo",
    "public_synthetic_demo",
    "computational_candidate",
    "candidate",
    "blocked",
    "insufficient_evidence",
}

PUBLIC_CAMPAIGN_CLAIM_LEVELS = ALLOWED_CLAIM_LEVELS - {"candidate"}

ALLOWED_PRIVACY = {
    "public_only",
    "public_or_synthetic_only",
    "synthetic_demo",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".runtime",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
}

FORBIDDEN_EXACT_NAME_PARTS = {
    ".env",
    ".env.local",
    "_book",
    "secrets",
    "pod_id",
    "runpod_resource_record",
    "runpod_cleanup_record",
}

FORBIDDEN_NAME_SUBSTRINGS = {
    "secret",
    "token",
    "billing",
}

FORBIDDEN_SUFFIXES = {
    ".ali",
    ".arrow",
    ".bcif",
    ".ckpt",
    ".pdb",
    ".cif",
    ".cs",
    ".db",
    ".dm4",
    ".duckdb",
    ".eer",
    ".fa",
    ".faa",
    ".fasta",
    ".feather",
    ".fastq",
    ".fna",
    ".fq",
    ".gif",
    ".h5",
    ".hdf",
    ".hdf5",
    ".map",
    ".mol2",
    ".mmcif",
    ".mrc",
    ".mrcs",
    ".mdoc",
    ".npy",
    ".npz",
    ".onnx",
    ".parquet",
    ".pem",
    ".pkl",
    ".pickle",
    ".pml",
    ".rawtlt",
    ".rec",
    ".st",
    ".trb",
    ".key",
    ".joblib",
    ".pt",
    ".pth",
    ".safetensors",
    ".sdf",
    ".sqlite",
    ".sqlite3",
    ".tar",
    ".gz",
    ".xz",
    ".zst",
    ".7z",
    ".bz2",
    ".rar",
    ".zip",
    ".mp4",
    ".mov",
}

TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".cff",
    ".css",
    ".csv",
    ".html",
    ".in",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".qmd",
    ".sh",
    ".svg",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}

REQUIRED_HARNESS_FILES = [
    "README.md",
    "AGENTS.md",
    "BIOSAFETY.md",
    "CHANGELOG.md",
    "NON_CLAIMS.md",
    "PUBLIC_RELEASE.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "CITATION.cff",
    "SUPPORT.md",
    "MANIFEST.in",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug-report.yml",
    ".github/ISSUE_TEMPLATE/campaign-request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "docs/agentic-biology-harness.md",
    "docs/agent-recipes.md",
    "docs/assets/README.md",
    "docs/capabilities.md",
    "docs/cli-reference.md",
    "docs/claim-and-evidence.md",
    "docs/workflow-map.md",
    "docs/use-cases.md",
    "docs/faq.md",
    "docs/glossary.md",
    "docs/skill-install.md",
    "docs/standalone-agent-workflow.md",
    "docs/privacy-and-security-model.md",
    "docs/quickstart-tour.md",
    "docs/public-export-shape.md",
    "docs/public-switch-checklist.md",
    "docs/tool-and-skill-radar.md",
    "docs/linear-orchestration.md",
    "docs/compute-backends.md",
    "docs/runpod-stack.md",
    "docs/tooling-and-licensing.md",
    "packs/issue-packs/binder-design-fast-path-v0/pack.yaml",
    "packs/README.md",
    "references/agent-handoff.md",
    "runpod/README.md",
    "schemas/README.md",
    "scripts/install-codex-skill.sh",
    "skills/biosymphony-structure-factory/SKILL.md",
    "skills/README.md",
    ".codex/skills/biosymphony-structure-factory/SKILL.md",
    "templates/github-issue.md",
    "templates/operator-wave-runbook.md",
    "tools/README.md",
    "recipes/README.md",
    "docs/assets/structure-factory-loop.svg",
    "docs/assets/newcomer-paths.svg",
    "docs/assets/workflow-ladder.svg",
    "examples/supercharger/README.md",
]

HARNESS_TEXT_REQUIREMENTS = {
    "README.md": [
        "BioSymphony",
        "Symphony",
        "RunPod",
        "skill",
        "claim ledger",
        "How To Use This",
        "Start Here",
        "Hand A Mission To An Agent",
        "Time Horizons",
        "When To Use This",
        "What Users And Their Agents Can Run",
        "Works With Your Stack",
        "Newcomer Resources",
        "docs/capabilities.md",
        "docs/workflow-map.md",
        "docs/faq.md",
        "docs/glossary.md",
        "bsf scaffold-campaign",
        "bsf doctor",
        "BIOSAFETY.md",
    ],
    "AGENTS.md": [
        "BioSymphony Structure Factory Agent Guide",
        "public_synthetic_demo",
        "computational_candidate",
        "Closeout requires artifacts, hashes, and a claim audit",
    ],
    "BIOSAFETY.md": [
        "Biosafety",
        "does not authorize wet-lab work",
        "Public examples must avoid",
        "NON_CLAIMS.md",
    ],
    "docs/use-cases.md": [
        "Copyable Agent Prompts",
        "Binder-Design Triage",
        "Provider Prep Without Launch",
        "Public-Release Safety Review",
    ],
    "docs/faq.md": [
        "Do I need a GPU?",
        "Do I have to run the CLI commands myself?",
        "Which agents work with this?",
        "Can I use this without Linear or any tracker?",
        "How do I add my own tool, provider, or campaign mode?",
    ],
    "docs/glossary.md": [
        "Glossary",
        "Campaign manifest",
        "Claim ceiling",
        "Evidence mode",
        "pLDDT",
        "iPTM",
        "Stage contract",
        "BioSymphony",
        "CryoCore",
    ],
    "PUBLIC_RELEASE.md": [
        "make release-check",
        "make public-switch-check",
        "make secret-scan",
        "sym:structure-factory",
        "RunPod",
        "computational_candidate",
    ],
    "SECURITY.md": [
        "Private vulnerability reporting",
        "Do not open public issues",
        "make public-switch-check",
    ],
    "docs/agent-recipes.md": [
        "Public-Safe Agent Recipes",
        "docs/use-cases.md",
        "Exact Evidence Values",
        "computational_candidate",
        "bsf scaffold-campaign",
        "claim ceiling",
        "operator gate",
    ],
    "docs/capabilities.md": [
        "Capabilities",
        "Binder-design campaign",
        "GPCR or multimer state atlas",
        "Screening and active learning",
        "Cloud/GPU execution prep",
        "bsf scaffold-campaign",
    ],
    "docs/assets/README.md": [
        "Visual Asset Notes",
        "structure-factory-loop.svg",
        "newcomer-paths.svg",
        "Text equivalent",
    ],
    "docs/skill-install.md": [
        "Install The Structure Factory Skill",
        "scripts/install-codex-skill.sh",
        "make harness-check",
    ],
    "docs/standalone-agent-workflow.md": [
        "Standalone Agent Workflow",
        "Copyable Agent Prompt",
        "bsf scaffold-campaign",
        "templates/github-issue.md",
    ],
    "docs/cli-reference.md": [
        "bsf scaffold-campaign",
        "bsf validate",
        "bsf audit",
        "bsf harness-check",
        "bsf doctor",
    ],
    "docs/claim-and-evidence.md": [
        "Claim And Evidence Guide",
        "computational_candidate",
        "Evidence Modes",
        "Legacy Schema Values",
        "Provider state is not an evidence mode",
    ],
    "docs/privacy-and-security-model.md": [
        "Privacy And Security Model",
        "Public-safe",
        "Never commit",
        "Launch templates",
    ],
    "docs/quickstart-tour.md": [
        "Quickstart Tour",
        "Three ways to start",
        "Use It With An Agent",
        "bsf scaffold-campaign",
        "make public-switch-check",
        "public-safe",
    ],
    "recipes/README.md": [
        "Recipes",
        "PD-L1 binder-design fast path",
        "RunPod no-download smoke",
    ],
    "docs/public-switch-checklist.md": [
        "make public-switch-check",
        "clean root commit",
        "RunPod bridge manifests",
        "Remote Gate",
    ],
    "docs/tool-and-skill-radar.md": [
        "public-safe planning snapshot",
        "Runtime Gated",
        "Review Required",
        "Export Priorities",
    ],
    "tools/README.md": [
        "Tool Cards",
        "Public docs",
        "Runtime use needs current primary-source review",
        "License-gated tools",
    ],
    "docs/agentic-biology-harness.md": [
        "Symphony",
        "Linear",
        "RunPod",
        "Claude-lane",
        "stage contract",
        "candidate jury",
        "claim",
    ],
    "skills/biosymphony-structure-factory/SKILL.md": [
        "sym:structure-factory",
        "RunPod",
        "Symphony",
        "Linear",
        "make harness-check",
    ],
    ".codex/skills/biosymphony-structure-factory/SKILL.md": [
        "sym:structure-factory",
        "RunPod",
        "Symphony",
        "Linear",
        "make harness-check",
    ],
    "templates/operator-wave-runbook.md": [
        "sym:structure-factory",
        "RunPod",
        "Operator authorization",
        "cleanup proof",
        "claim ceiling",
    ],
}

CONTENT_PATTERNS = [
    ("private-workstation-path", re.compile(r"(/" + r"Users/|/" + r"Volumes/|C:\\Users\\)")),
    ("local-user-or-private-root", re.compile(r"\b(github_[0-9]+|SSK_[A-Za-z0-9_]+)\b", re.I)),
    ("assigned-api-key", re.compile(r"\b([A-Z0-9_]*(API_KEY|SECRET|PASSWORD|ACCESS_TOKEN|AUTH_TOKEN|BEARER_TOKEN)[A-Z0-9_]*)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{8,}", re.I)),
    ("openai-style-token", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9\-]{20,}\b")),
    ("literal-runpod-resource-id", re.compile(r'"?(pod_id|networkVolumeId|network_volume_id)"?\s*[:=]\s*"?[a-z0-9]{8,}"?')),
    ("private-tracker-id", re.compile(r"\bVOG-[A-Za-z0-9][A-Za-z0-9-]*\b")),
    ("private-linear-url", re.compile(r"https?://linear\.app/[^\s)>\"]+", re.I)),
    ("private-run-checkpoint", re.compile(r"\bCHECKPOINT-\d{4}-\d{2}-\d{2}\b")),
    ("provider-incident-cost-ledger", re.compile(r"\b(dead[- ]" + r"pods?|pod " + r"fires|burned on dead " + r"pods)\b", re.I)),
    ("generated-candidate-sequence", re.compile(r'"(mpnn_sequence|binder_sequence)"\s*:\s*"[ACDEFGHIKLMNPQRSTVWY]{20,}"')),
]


@dataclass
class Finding:
    severity: str
    check_id: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "check_id": self.check_id,
            "path": self.path,
            "message": self.message,
        }


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(data: Any) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def reject_public_unsafe_input(name: str, value: str) -> None:
    for check_id, pattern in CONTENT_PATTERNS:
        if check_id == "generated-candidate-sequence":
            continue
        match = pattern.search(value)
        if match:
            raise ValueError(f"{name} contains public-safety marker {check_id}: {match.group(0)[:80]}")


def validate_campaign_id(campaign_id: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,79}", campaign_id):
        raise ValueError("campaign_id must be 3-80 chars of lowercase letters, numbers, and hyphens")
    risky_parts = {"secret", "token", "private", "internal"}
    if any(part in campaign_id for part in risky_parts):
        raise ValueError("campaign_id should not include private/security-sensitive words")


def scaffold_lanes(mode: str) -> list[dict[str, Any]]:
    shared = {
        "claim_ceiling": "computational_candidate",
        "runtime_gate": "operator_required_before_gpu_or_license_gated_execution",
    }
    if mode == "binder-design":
        return [
            {
                "id": "target-window-contract",
                "kind": "planning",
                "description": "Public accession, residue window, hotspots, and non-claims.",
                **shared,
            },
            {
                "id": "generation-readiness",
                "kind": "gpu_prep",
                "description": "Binder generation lane setup with runtime-gated models and no committed outputs.",
                **shared,
            },
            {
                "id": "cofold-jury",
                "kind": "model_jury",
                "description": "Cofold and scoring jury contract for generated candidates.",
                **shared,
            },
        ]
    if mode == "model-jury":
        return [
            {
                "id": "evidence-intake",
                "kind": "planning",
                "description": "Public model or structure inputs, quality metrics, and claim ceiling.",
                **shared,
            },
            {
                "id": "jury-contract",
                "kind": "model_jury",
                "description": "Cross-tool scoring, disagreement, failure, and provenance contract.",
                **shared,
            },
        ]
    if mode == "structure-dossier":
        return [
            {
                "id": "accession-contract",
                "kind": "planning",
                "description": "Public accession, validation target, and artifact expectations.",
                **shared,
            },
            {
                "id": "dossier-build",
                "kind": "report_or_jury",
                "description": "Structure evidence dossier with figures, provenance, and non-claims.",
                **shared,
            },
        ]
    if mode == "screening":
        return [
            {
                "id": "screening-contract",
                "kind": "planning",
                "description": "Public receptor/ligand scope, fanout estimate, and evidence ceiling.",
                **shared,
            },
            {
                "id": "shard-plan",
                "kind": "gpu_prep",
                "description": "Provider-neutral shard plan with budget, cleanup, and result schema gates.",
                **shared,
            },
        ]
    raise ValueError(f"unsupported scaffold mode: {mode}")


def scaffold_campaign(
    out_dir: Path,
    *,
    campaign_id: str,
    target_label: str,
    public_accession: str,
    window: str,
    mode: str = "binder-design",
    force: bool = False,
) -> dict[str, Any]:
    validate_campaign_id(campaign_id)
    for name, value in {
        "target_label": target_label,
        "public_accession": public_accession,
        "window": window,
        "mode": mode,
    }.items():
        reject_public_unsafe_input(name, value)

    if out_dir.exists() and any(out_dir.iterdir()) and not force:
        raise ValueError(f"output directory is not empty: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    campaign = {
        "schema_version": 1,
        "campaign_id": campaign_id,
        "title": f"{target_label} public-safe {mode} campaign",
        "mode": mode,
        "claim_level": "planning",
        "system": {
            "privacy": "public_or_synthetic_only",
            "repo_role": "control_plane",
        },
        "target": {
            "label": target_label,
            "public_accession": public_accession,
            "window": window,
            "source_policy": "public accession or synthetic fixture only",
        },
        "lanes": scaffold_lanes(mode),
        "expected_artifacts": [
            "target-window-dossier.json",
            "claim-ledger.md",
            "stage-contract.json",
            "candidate-jury.example.json or dossier-summary.md after evidence exists",
        ],
        "wet_lab_execution": False,
        "therapeutic_claims": False,
        "operator_gate_required_before_execution": True,
    }

    stage_contract = {
        "schema_version": 1,
        "campaign_id": campaign_id,
        "claim_ceiling": "computational_candidate",
        "fail_closed": True,
        "privacy": "public_or_synthetic_only",
        "operator_gate_required": True,
        "progress_ledger": "stage-progress.jsonl",
        "partial_success_policy": "Missing, partial, or unverifiable evidence must downgrade to blocked or insufficient_evidence.",
        "stages": [
            {
                "id": lane["id"],
                "mode": lane["kind"],
                "required_artifacts": [],
                "success_evidence": "declared artifacts, hashes, validation output, and claim ceiling",
            }
            for lane in campaign["lanes"]
        ],
    }

    target_dossier = {
        "schema_version": 1,
        "campaign_id": campaign_id,
        "target_label": target_label,
        "public_accession": public_accession,
        "window": window,
        "privacy": "public_or_synthetic_only",
        "hotspots_or_regions": [],
        "evidence_notes": [
            "Add public-source citations, residue numbering notes, and uncertainty here.",
            "Do not add unpublished sequences, private structures, or generated candidate coordinates.",
        ],
    }

    readme = f"""# {target_label} Structure Factory Campaign

Campaign ID: `{campaign_id}`

This is a public-safe Structure Factory scaffold for `{mode}` work. It is a control-plane starter: manifests, stage contracts, claim boundaries, and expected artifacts only.

## Public Inputs

- target: `{target_label}`
- public accession: `{public_accession}`
- window: `{window}`

## Claim Ceiling

Planning or computational-candidate evidence only. This scaffold does not claim binding, inhibition, selectivity, safety, efficacy, clinical relevance, or therapeutic value.

## Next Local Checks

```bash
bsf validate {out_dir.as_posix()}
bsf audit .
```

## Before Any GPU Or Provider Run

- replace placeholders with reviewed public-accession metadata
- declare expected artifacts and hashes
- confirm tool/license use context
- set budget, runtime cap, and cleanup policy
- keep credentials, provider IDs, private paths, generated structures, and logs outside git
"""

    claim_ledger = f"""# Claim Ledger

Campaign ID: `{campaign_id}`

| Claim | Status | Evidence Mode | Notes |
| --- | --- | --- | --- |
| Target/window selected for planning | draft | public_or_synthetic_only | Back this with public accession notes before execution. |
| Generated candidates bind or modulate target | not claimed | insufficient_evidence | Requires downstream computational evidence and experimental validation. |
| Therapeutic, safety, efficacy, or clinical value | not claimed | insufficient_evidence | Out of scope for this repo. |
"""

    files = {
        "campaign-manifest.json": json.dumps(campaign, indent=2, sort_keys=True) + "\n",
        "stage-contract.json": json.dumps(stage_contract, indent=2, sort_keys=True) + "\n",
        "target-window-dossier.json": json.dumps(target_dossier, indent=2, sort_keys=True) + "\n",
        "README.md": readme,
        "claim-ledger.md": claim_ledger,
    }
    written: list[str] = []
    for name, content in files.items():
        path = out_dir / name
        path.write_text(content, encoding="utf-8")
        written.append(path.as_posix())

    ok, findings = validate_campaign(out_dir)
    return {
        "ok": ok,
        "campaign_dir": out_dir.as_posix(),
        "files": written,
        "findings": [finding.to_dict() for finding in findings],
    }


def iter_public_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        current_path = Path(current)
        for name in names:
            path = current_path / name
            if path.is_file():
                files.append(path)
    return sorted(files)


def audit_tree(root: Path) -> tuple[bool, list[Finding]]:
    findings: list[Finding] = []
    for path in iter_public_files(root):
        rel = path.relative_to(root).as_posix()
        lowered_parts = [part.lower() for part in path.relative_to(root).parts]
        if path.name.lower().endswith(".local.json"):
            findings.append(Finding("error", "local-artifact-file", rel, "local runtime JSON files are not public-release artifacts"))
        for part in lowered_parts:
            if part in FORBIDDEN_EXACT_NAME_PARTS or any(marker in part for marker in FORBIDDEN_NAME_SUBSTRINGS):
                findings.append(Finding("error", "forbidden-name", rel, f"forbidden public filename component: {part}"))
                break
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(Finding("error", "forbidden-generated-artifact", rel, f"generated/heavy artifact suffix is not public by default: {path.suffix}"))
        size = path.stat().st_size
        if size > 25_000_000:
            findings.append(Finding("error", "large-file", rel, f"file is too large for the public control-plane repo: {size} bytes"))
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(Finding("error", "non-text-file", rel, "file is not valid UTF-8 text"))
            continue
        for check_id, pattern in CONTENT_PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append(Finding("error", check_id, rel, f"matched public-safety pattern: {match.group(0)[:80]}"))
        if rel.startswith("runpod/bridge-manifests/"):
            for marker in ["base64 -d", "gunzip", "xz -d", '"approved_at": "20', "US-KS-"]:
                if marker in text:
                    findings.append(Finding("error", "launch-payload-or-approval", rel, f"public bridge manifest contains launch-only marker: {marker}"))
    ok = not any(finding.severity == "error" for finding in findings)
    return ok, findings


def validate_campaign(campaign_dir: Path) -> tuple[bool, list[Finding]]:
    findings: list[Finding] = []
    manifest_path = campaign_dir / "campaign-manifest.json"
    if not manifest_path.exists():
        return False, [Finding("error", "missing-manifest", str(manifest_path), "campaign-manifest.json is required")]
    try:
        manifest = read_json(manifest_path)
    except json.JSONDecodeError as exc:
        return False, [Finding("error", "invalid-json", str(manifest_path), str(exc))]

    rel_manifest = manifest_path.as_posix()
    campaign_id = manifest.get("campaign_id")
    if not isinstance(campaign_id, str) or not campaign_id:
        findings.append(Finding("error", "campaign-id", rel_manifest, "campaign_id must be a non-empty string"))
    claim_level = manifest.get("claim_level")
    if claim_level not in PUBLIC_CAMPAIGN_CLAIM_LEVELS:
        findings.append(Finding("error", "claim-level", rel_manifest, f"claim_level must be one of {sorted(PUBLIC_CAMPAIGN_CLAIM_LEVELS)}"))
    privacy = manifest.get("system", {}).get("privacy")
    if privacy not in ALLOWED_PRIVACY:
        findings.append(Finding("error", "privacy", rel_manifest, f"system.privacy must be one of {sorted(ALLOWED_PRIVACY)}"))
    if manifest.get("wet_lab_execution") is not False:
        findings.append(Finding("error", "wet-lab-boundary", rel_manifest, "wet_lab_execution must be false in public examples"))
    if manifest.get("therapeutic_claims") is not False:
        findings.append(Finding("error", "therapeutic-boundary", rel_manifest, "therapeutic_claims must be false in public examples"))

    target = manifest.get("target", {})
    if not target.get("public_accession"):
        findings.append(Finding("error", "target-accession", rel_manifest, "target.public_accession is required"))
    if not target.get("window"):
        findings.append(Finding("error", "target-window", rel_manifest, "target.window is required"))

    lanes = manifest.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        findings.append(Finding("error", "lanes", rel_manifest, "lanes[] must declare at least one planned lane"))
    else:
        for lane in lanes:
            claim_ceiling = lane.get("claim_ceiling")
            if not claim_ceiling:
                findings.append(Finding("error", "lane-claim-ceiling", rel_manifest, f"lane {lane.get('id', '<missing>')} needs claim_ceiling"))
            elif claim_ceiling not in PUBLIC_CAMPAIGN_CLAIM_LEVELS:
                findings.append(Finding("error", "lane-claim-ceiling", rel_manifest, f"lane {lane.get('id', '<missing>')} claim_ceiling must be one of {sorted(PUBLIC_CAMPAIGN_CLAIM_LEVELS)}"))

    expected = manifest.get("expected_artifacts")
    if not isinstance(expected, list) or not expected:
        findings.append(Finding("error", "expected-artifacts", rel_manifest, "expected_artifacts[] is required"))

    stage_path = campaign_dir / "stage-contract.json"
    if stage_path.exists():
        try:
            stage_contract = read_json(stage_path)
            if stage_contract.get("fail_closed") is not True:
                findings.append(Finding("error", "stage-fail-closed", stage_path.as_posix(), "stage contract must declare fail_closed: true"))
            if not stage_contract.get("stages"):
                findings.append(Finding("error", "stage-list", stage_path.as_posix(), "stage contract must include stages[]"))
        except json.JSONDecodeError as exc:
            findings.append(Finding("error", "invalid-stage-json", stage_path.as_posix(), str(exc)))
    else:
        findings.append(Finding("warning", "missing-stage-contract", stage_path.as_posix(), "stage-contract.json is advised for GPU or long-running campaigns"))

    jury_path = campaign_dir / "candidate-jury.example.json"
    if jury_path.exists():
        try:
            jury = read_json(jury_path)
            candidates = jury.get("candidates")
            if not isinstance(candidates, list):
                findings.append(Finding("error", "jury-candidates", jury_path.as_posix(), "candidate jury must include candidates[]"))
            else:
                for candidate in candidates:
                    candidate_claim = candidate.get("claim_level")
                    if candidate_claim not in PUBLIC_CAMPAIGN_CLAIM_LEVELS:
                        findings.append(Finding("error", "jury-claim-level", jury_path.as_posix(), f"candidate {candidate.get('id')} has invalid claim_level"))
                    if candidate.get("evidence_mode") not in {"synthetic_demo", "public_data", "generated_candidate", "blocked", "insufficient_evidence"}:
                        findings.append(Finding("error", "jury-evidence-mode", jury_path.as_posix(), f"candidate {candidate.get('id')} needs valid evidence_mode"))
        except json.JSONDecodeError as exc:
            findings.append(Finding("error", "invalid-jury-json", jury_path.as_posix(), str(exc)))

    ok = not any(finding.severity == "error" for finding in findings)
    return ok, findings


def harness_check(root: Path) -> tuple[bool, list[Finding]]:
    findings: list[Finding] = []
    for rel in REQUIRED_HARNESS_FILES:
        path = root / rel
        if not path.exists():
            findings.append(Finding("error", "missing-harness-file", rel, "required public harness file is missing"))
        elif not path.is_file():
            findings.append(Finding("error", "harness-path-not-file", rel, "required public harness path is not a file"))

    for rel, needles in HARNESS_TEXT_REQUIREMENTS.items():
        path = root / rel
        if not path.exists() or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                findings.append(Finding("error", "missing-harness-language", rel, f"expected public harness language: {needle}"))

    for rel in [
        "skills/biosymphony-structure-factory/SKILL.md",
        ".codex/skills/biosymphony-structure-factory/SKILL.md",
    ]:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"`([^`]+\.md)`", text):
            target = match.group(1)
            if "://" in target or target.startswith("#"):
                continue
            if not (root / target).exists():
                findings.append(Finding("error", "stale-skill-reference", rel, f"skill references missing markdown file: {target}"))

    codex_skill = root / ".codex/skills/biosymphony-structure-factory/SKILL.md"
    portable_skill = root / "skills/biosymphony-structure-factory/SKILL.md"
    if codex_skill.exists() and portable_skill.exists():
        if codex_skill.read_text(encoding="utf-8") != portable_skill.read_text(encoding="utf-8"):
            findings.append(Finding("error", "skill-copy-drift", portable_skill.relative_to(root).as_posix(), "portable skill must match the Codex skill"))

    pack_path = root / "packs/issue-packs/binder-design-fast-path-v0/pack.yaml"
    if pack_path.exists():
        text = pack_path.read_text(encoding="utf-8")
        for needle in ["routing_label: sym:structure-factory", "claim_ceiling: computational_candidate", "issues:"]:
            if needle not in text:
                findings.append(Finding("error", "issue-pack-contract", pack_path.relative_to(root).as_posix(), f"issue pack missing: {needle}"))

    ok = not any(finding.severity == "error" for finding in findings)
    return ok, findings


def _relative_to(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _read_json_finding(path: Path, root: Path, findings: list[Finding]) -> Any | None:
    try:
        return read_json(path)
    except json.JSONDecodeError as exc:
        findings.append(Finding("error", "invalid-json", _relative_to(root, path), str(exc)))
    except OSError as exc:
        findings.append(Finding("error", "unreadable-file", _relative_to(root, path), str(exc)))
    return None


def _yaml_scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        return None
    value = match.group(1).strip()
    if value in {">", "|"}:
        return None
    return value.strip("\"'")


def _collect_issue_ids(text: str) -> list[str]:
    return sorted(set(re.findall(r"(?m)^\s*-\s+id:\s*([A-Za-z0-9_.-]+)\s*$", text)))


TASK_RECIPES: list[dict[str, Any]] = [
    {
        "task": "Create a public-safe Structure Factory campaign",
        "mode": "planning",
        "commands": [
            "bsf scaffold-campaign .runtime/my-demo --campaign-id my-demo --target-label '<public target>' --public-accession '<PDB:ID>' --window '<region>'",
            "bsf validate .runtime/my-demo",
        ],
        "outputs": [".runtime/my-demo/campaign-manifest.json", ".runtime/my-demo/stage-contract.json"],
        "remote_mutation": False,
    },
    {
        "task": "Render tracker-neutral Symphony or Linear issue drafts",
        "mode": "planning",
        "commands": ["bsf issue-dry-run examples/pd-l1-binder-design-public --out .runtime/pd-l1-issues"],
        "outputs": [".runtime/pd-l1-issues/*.md"],
        "remote_mutation": False,
    },
    {
        "task": "Review the repo capability surface before assigning an agent",
        "mode": "review",
        "commands": ["bsf catalog . --format markdown", "make catalog-md"],
        "outputs": [".runtime/public-capability-catalog.md"],
        "remote_mutation": False,
    },
    {
        "task": "Translate a /goal request into an orchestrated work program",
        "mode": "orchestrator_companion",
        "commands": [
            "bsf catalog . --format markdown",
            "bsf scaffold-campaign .runtime/my-demo --campaign-id my-demo --target-label '<public target>' --public-accession '<PDB:ID>' --window '<region>'",
            "bsf issue-dry-run .runtime/my-demo --out .runtime/my-demo-issues",
        ],
        "outputs": ["campaign contract", "optional issue drafts", "explicit assumptions and hard gates"],
        "remote_mutation": False,
    },
    {
        "task": "Run public-release safety checks without provider access",
        "mode": "release_review",
        "commands": ["make read-only-audit", "make public-switch-check"],
        "outputs": ["local validation logs", "ignored .runtime artifacts"],
        "remote_mutation": False,
    },
    {
        "task": "Prepare cloud or RunPod wave templates without launching",
        "mode": "cloud_prep",
        "commands": ["make runpod-public-template-check", "make launch-bundle"],
        "outputs": [".runtime/structure-factory-no-download-smoke"],
        "remote_mutation": False,
    },
]


def capability_catalog(root: Path) -> dict[str, Any]:
    """Build a machine-readable map of what this repo can help users do."""

    findings: list[Finding] = []
    root = root.resolve()

    campaign_modules: list[dict[str, Any]] = []
    for path in sorted((root / "modules" / "campaigns").glob("*.json")):
        data = _read_json_finding(path, root, findings)
        if not isinstance(data, dict):
            continue
        policies = data.get("policies") if isinstance(data.get("policies"), dict) else {}
        screening_defaults = data.get("screening_defaults") if isinstance(data.get("screening_defaults"), dict) else {}
        wave_plan = data.get("wave_plan") if isinstance(data.get("wave_plan"), dict) else {}
        providers = {
            str(item)
            for item in [
                *(screening_defaults.get("provider_priority") or []),
                *(wave.get("provider") for wave in wave_plan.values() if isinstance(wave, dict)),
            ]
            if item
        }
        if data.get("launch_manifests"):
            providers.add("runpod")
        campaign_modules.append(
            {
                "path": _relative_to(root, path),
                "campaign_id": data.get("campaign_id"),
                "family": data.get("campaign_family"),
                "run_profile": data.get("run_profile"),
                "objective": data.get("scientific_objective"),
                "lane_count": len(data.get("lane_modules") or []),
                "data_module_count": len(data.get("data_modules") or []),
                "stage_contract_count": len(data.get("stage_contracts") or []),
                "launch_manifest_count": len(data.get("launch_manifests") or []),
                "providers": sorted(providers),
                "claim_ceiling": screening_defaults.get("claim_ceiling") or policies.get("claim_ceiling"),
                "operator_gate_signals": {
                    "allow_large_downloads": policies.get("allow_large_downloads"),
                    "allow_raw_cryoem_downloads": policies.get("allow_raw_cryoem_downloads"),
                    "allow_private_data": policies.get("allow_private_data"),
                    "license_gates": data.get("license_gates") or [],
                },
            }
        )

    example_campaigns: list[dict[str, Any]] = []
    examples_dir = root / "examples"
    if examples_dir.is_dir():
        for example_path in sorted(p for p in examples_dir.iterdir() if p.is_dir()):
            campaign_manifest = example_path / "campaign-manifest.json"
            screening_manifest = example_path / "screening-manifest.json"
            readme = example_path / "README.md"
            entry: dict[str, Any] = {
                "path": _relative_to(root, example_path),
                "campaign_id": example_path.name,
                "title": None,
                "mode": None,
                "claim_level": None,
                "privacy": None,
                "target_label": None,
                "public_accession": None,
                "lane_count": 0,
                "expected_artifact_count": 0,
                "kind": "readme_only",
            }
            if campaign_manifest.exists():
                data = _read_json_finding(campaign_manifest, root, findings)
                if isinstance(data, dict):
                    system = data.get("system") if isinstance(data.get("system"), dict) else {}
                    target = data.get("target") if isinstance(data.get("target"), dict) else {}
                    entry.update(
                        {
                            "kind": "campaign_manifest",
                            "campaign_id": data.get("campaign_id") or example_path.name,
                            "title": data.get("title"),
                            "mode": data.get("mode"),
                            "claim_level": data.get("claim_level"),
                            "privacy": system.get("privacy"),
                            "target_label": target.get("label"),
                            "public_accession": target.get("public_accession"),
                            "lane_count": len(data.get("lanes") or []),
                            "expected_artifact_count": len(data.get("expected_artifacts") or []),
                        }
                    )
            elif screening_manifest.exists():
                data = _read_json_finding(screening_manifest, root, findings)
                if isinstance(data, dict):
                    intent = data.get("intent") if isinstance(data.get("intent"), dict) else {}
                    target = data.get("target") if isinstance(data.get("target"), dict) else {}
                    entry.update(
                        {
                            "kind": "screening_manifest",
                            "campaign_id": data.get("campaign_id") or example_path.name,
                            "title": intent.get("natural_language_goal") or target.get("name"),
                            "mode": intent.get("mode") or "screening",
                            "claim_level": intent.get("claim_ceiling"),
                            "target_label": target.get("name") or intent.get("target_hint"),
                        }
                    )
            if entry.get("title") is None and readme.exists():
                try:
                    for line in readme.read_text(encoding="utf-8").splitlines():
                        if line.startswith("# "):
                            entry["title"] = line[2:].strip()
                            break
                except OSError as exc:
                    findings.append(Finding("error", "unreadable-file", _relative_to(root, readme), str(exc)))
            example_campaigns.append(entry)

    stage_contracts: list[dict[str, Any]] = []
    for path in sorted((root / "runpod" / "stage-contracts").glob("*.json")):
        data = _read_json_finding(path, root, findings)
        if not isinstance(data, dict):
            continue
        stage_contracts.append(
            {
                "path": _relative_to(root, path),
                "contract_id": data.get("contract_id"),
                "manifest_id": data.get("manifest_id"),
                "execution_profile": data.get("execution_profile"),
                "stage_count": len(data.get("stages") or []),
                "fail_closed": data.get("fail_closed"),
                "success_claim": data.get("success_claim"),
            }
        )

    provider_profiles: list[dict[str, Any]] = []
    for path in sorted((root / "modules" / "provider-profiles").glob("**/*.json")):
        data = _read_json_finding(path, root, findings)
        if not isinstance(data, dict):
            continue
        provider_profiles.append(
            {
                "path": _relative_to(root, path),
                "provider": data.get("provider"),
                "profile_id": data.get("profile_id"),
                "maps_campaign_profile": data.get("maps_campaign_profile"),
                "operator_gate_required": data.get("operator_gate_required"),
                "execution_ready_requires": data.get("execution_ready_requires") or [],
            }
        )

    issue_packs: list[dict[str, Any]] = []
    for path in sorted((root / "packs" / "issue-packs").glob("*/pack.yaml")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append(Finding("error", "unreadable-file", _relative_to(root, path), str(exc)))
            continue
        issue_packs.append(
            {
                "path": _relative_to(root, path),
                "pack_id": _yaml_scalar(text, "pack_id"),
                "title": _yaml_scalar(text, "title"),
                "routing_label": _yaml_scalar(text, "routing_label"),
                "claim_ceiling": _yaml_scalar(text, "claim_ceiling"),
                "issue_count": len(_collect_issue_ids(text)),
                "issue_ids": _collect_issue_ids(text),
            }
        )

    recipes = [
        _relative_to(root, path)
        for path in sorted((root / "recipes").glob("*.md"))
        if path.name.lower() != "readme.md"
    ]

    checks = [
        {"id": "campaign-modules-present", "ok": bool(campaign_modules), "count": len(campaign_modules)},
        {"id": "examples-present", "ok": bool(example_campaigns), "count": len(example_campaigns)},
        {"id": "stage-contracts-present", "ok": bool(stage_contracts), "count": len(stage_contracts)},
        {"id": "provider-profiles-present", "ok": bool(provider_profiles), "count": len(provider_profiles)},
        {"id": "issue-packs-present", "ok": bool(issue_packs), "count": len(issue_packs)},
        {"id": "recipes-present", "ok": bool(recipes), "count": len(recipes)},
    ]
    ok = not any(finding.severity == "error" for finding in findings) and all(check["ok"] for check in checks)

    return {
        "ok": ok,
        "root": root.as_posix(),
        "counts": {
            "campaign_modules": len(campaign_modules),
            "example_campaigns": len(example_campaigns),
            "stage_contracts": len(stage_contracts),
            "provider_profiles": len(provider_profiles),
            "issue_packs": len(issue_packs),
            "recipes": len(recipes),
            "task_recipes": len(TASK_RECIPES),
        },
        "checks": checks,
        "campaign_modules": campaign_modules,
        "example_campaigns": example_campaigns,
        "issue_packs": issue_packs,
        "stage_contracts": stage_contracts,
        "provider_profiles": provider_profiles,
        "recipes": recipes,
        "task_recipes": TASK_RECIPES,
        "entry_points": [
            "bsf catalog . --format markdown",
            "bsf scaffold-campaign .runtime/my-demo --campaign-id my-demo --target-label '<public target>' --public-accession '<PDB:ID>' --window '<region>'",
            "bsf issue-dry-run examples/pd-l1-binder-design-public --out .runtime/pd-l1-issues",
            "make runpod-public-template-check",
            "make public-switch-check",
        ],
        "findings": [finding.to_dict() for finding in findings],
    }


def _markdown_cell(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, bool):
        text = "yes" if value else "no"
    elif isinstance(value, list):
        text = ", ".join(str(item) for item in value) if value else ""
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    if not rows:
        return ["_None found._"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_markdown_cell(value) for value in row) + " |")
    return lines


def catalog_markdown(catalog: dict[str, Any]) -> str:
    counts = catalog.get("counts") if isinstance(catalog.get("counts"), dict) else {}
    lines = [
        "# Structure Factory Capability Catalog",
        "",
        f"- status: `{'ok' if catalog.get('ok') else 'needs-attention'}`",
        f"- root: `{catalog.get('root', '')}`",
        f"- campaign modules: `{counts.get('campaign_modules', 0)}`",
        f"- public examples: `{counts.get('example_campaigns', 0)}`",
        f"- stage contracts: `{counts.get('stage_contracts', 0)}`",
        f"- provider profiles: `{counts.get('provider_profiles', 0)}`",
        f"- issue packs: `{counts.get('issue_packs', 0)}`",
        f"- recipes: `{counts.get('recipes', 0)}`",
        f"- task recipes: `{counts.get('task_recipes', 0)}`",
        "",
        "## Task Recipes",
        "",
    ]
    lines.extend(
        _markdown_table(
            ["Task", "Mode", "Commands", "Outputs", "Remote Mutation"],
            [
                [
                    item.get("task"),
                    item.get("mode"),
                    item.get("commands") or [],
                    item.get("outputs") or [],
                    item.get("remote_mutation"),
                ]
                for item in catalog.get("task_recipes", [])
                if isinstance(item, dict)
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Campaign Modules",
            "",
        ]
    )
    lines.extend(
        _markdown_table(
            ["Campaign", "Family", "Providers", "Lanes", "Data Modules", "Launch Manifests", "Claim Ceiling", "Path"],
            [
                [
                    item.get("campaign_id"),
                    item.get("family"),
                    item.get("providers") or ["provider-neutral"],
                    item.get("lane_count"),
                    item.get("data_module_count"),
                    item.get("launch_manifest_count"),
                    item.get("claim_ceiling"),
                    item.get("path"),
                ]
                for item in catalog.get("campaign_modules", [])
                if isinstance(item, dict)
            ],
        )
    )
    lines.extend(["", "## Public Examples", ""])
    lines.extend(
        _markdown_table(
            ["Example", "Kind", "Mode", "Claim Level", "Target Or Summary", "Path"],
            [
                [
                    item.get("campaign_id"),
                    item.get("kind"),
                    item.get("mode"),
                    item.get("claim_level"),
                    item.get("target_label") or item.get("title"),
                    item.get("path"),
                ]
                for item in catalog.get("example_campaigns", [])
                if isinstance(item, dict)
            ],
        )
    )
    lines.extend(["", "## Issue Packs", ""])
    lines.extend(
        _markdown_table(
            ["Pack", "Issues", "Claim Ceiling", "Routing Label", "Path"],
            [
                [
                    item.get("pack_id"),
                    item.get("issue_count"),
                    item.get("claim_ceiling"),
                    item.get("routing_label"),
                    item.get("path"),
                ]
                for item in catalog.get("issue_packs", [])
                if isinstance(item, dict)
            ],
        )
    )
    lines.extend(["", "## Stage Contracts", ""])
    lines.extend(
        _markdown_table(
            ["Contract", "Profile", "Stages", "Fail Closed", "Path"],
            [
                [
                    item.get("contract_id"),
                    item.get("execution_profile"),
                    item.get("stage_count"),
                    item.get("fail_closed"),
                    item.get("path"),
                ]
                for item in catalog.get("stage_contracts", [])
                if isinstance(item, dict)
            ],
        )
    )
    lines.extend(["", "## Provider Profiles", ""])
    lines.extend(
        _markdown_table(
            ["Provider", "Profile", "Operator Gate", "Execution Ready Requires", "Path"],
            [
                [
                    item.get("provider"),
                    item.get("profile_id"),
                    item.get("operator_gate_required"),
                    item.get("execution_ready_requires") or [],
                    item.get("path"),
                ]
                for item in catalog.get("provider_profiles", [])
                if isinstance(item, dict)
            ],
        )
    )
    lines.extend(["", "## Starter Commands", ""])
    entry_points = catalog.get("entry_points") if isinstance(catalog.get("entry_points"), list) else []
    if entry_points:
        lines.extend(f"- `{command}`" for command in entry_points)
    else:
        lines.append("_None found._")

    findings = catalog.get("findings") if isinstance(catalog.get("findings"), list) else []
    if findings:
        lines.extend(["", "## Findings", ""])
        lines.extend(
            f"- `{item.get('severity', 'unknown')}` `{item.get('check_id', 'unknown')}` "
            f"`{item.get('path', '')}`: {item.get('message', '')}"
            for item in findings
            if isinstance(item, dict)
        )

    return "\n".join(lines) + "\n"


def repo_relative(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def render_issue(
    campaign: dict[str, Any],
    issue_id: str,
    title: str,
    owned_paths: list[str],
    acceptance: list[str],
    campaign_path: str,
    dependency: str = "none",
) -> str:
    campaign_id = campaign["campaign_id"]
    target = campaign.get("target", {})
    artifacts = "\n".join(f"- `{campaign_path}/{item}`" for item in campaign.get("expected_artifacts", []))
    owned = "\n".join(f"- `{campaign_path}/{path}` - owned by this issue" for path in owned_paths)
    criteria = "\n".join(f"- [ ] {item}" for item in acceptance)
    schema_touched = "\n".join(f"  - {campaign_path}/{path}" for path in owned_paths)
    stage_contract = f"{campaign_path}/stage-contract.json"
    return f"""# {issue_id}: {title}

## Summary

Prepare one public-safe slice of `{campaign_id}` for agent execution, review, or tracker import. This draft is provider-neutral until an operator explicitly authorizes local, cloud, or RunPod execution.

## Inputs

- campaign ID: `{campaign_id}`
- subgroup: `structure-factory`
- routing label: `sym:structure-factory`
- target: `{target.get("label", "unknown")}`
- public accession: `{target.get("public_accession", "unknown")}`
- target window: `{target.get("window", "unknown")}`
- claim ceiling: `computational_candidate`

## Expected Artifacts

{artifacts}

## Stage / Progress Contract

- stage contract: `{stage_contract}`
- artifact granularity: `per-campaign`
- progress ledger: `.runtime/{campaign_id}/{issue_id}/stage-progress.jsonl`
- resume command: `PYTHONPATH=src python3 -m biosymphony_structure_factory.cli validate {campaign_path}`
- partial success policy: blocked, failed, or incomplete lanes must downgrade the final outcome instead of claiming success.

## Provider / Execution Profile

- provider: `provider-neutral`
- execution profile: `other`
- setup posture: `n/a`
- writable volume/env: `n/a`
- operator gate required: `no`

## Tooling / License Posture

- tools: `Structure Factory public CLI`
- posture: `open-default`
- current primary source checked: `no external install required for this dry-run draft`
- intended use context: `public planning`
- image/runtime action: `n/a`
- operator action required: `none for planning; explicit authorization before paid cloud execution`

## Acceptance Criteria

{criteria}

## Validation Commands

```bash
PYTHONPATH=src python3 -m biosymphony_structure_factory.cli validate {campaign_path}
PYTHONPATH=src python3 -m biosymphony_structure_factory.cli audit .
```

## Final Outcome Contract

- worker lane: `codex`
- closeout state: `In Review`
- final comment must include: `<!-- symphony-outcome -->`
- evidence mode: `report_only`
- claim level: `planning`
- artifact packet: `.runtime/{campaign_id}/{issue_id}`
- hash ledger: `n/a`
- cost report: `n/a`
- cleanup proof: `n/a`
- success requires: validation commands pass and any provider execution remains separately authorized.

## Touched Areas

{owned}

## Dependencies

Blocked by: {dependency}

## Risk Notes

- Computational candidate evidence only.
- No wet-lab, binding, therapeutic, safety, or clinical claims.
- GPU execution requires separate operator authorization, budget, cleanup policy, and runtime license/use-context review.

## Complexity

tier: medium

<!-- symphony:schema
schema_version: 1
subgroup: structure-factory
campaign_id: {campaign_id}
routing_label: sym:structure-factory
issue_id: {issue_id}
touched_areas:
{schema_touched}
complexity: medium
claim_ceiling: computational_candidate
-->
	"""


IssueSpec = tuple[str, str, list[str], list[str]]


def issue_plan_for_campaign(campaign: dict[str, Any]) -> list[IssueSpec]:
    mode = campaign.get("mode", "binder-design")
    if mode == "binder-design":
        return [
            (
                "BSF-BINDER-W00",
                "Target Window And Claim Contract",
                ["campaign-manifest.json", "target-window-dossier.json", "claim-ledger.md"],
                ["Target accession and residue window are explicit.", "Claim ceiling is computational candidate.", "No private data is referenced."],
            ),
            (
                "BSF-BINDER-W01",
                "Generation Lane Readiness",
                ["campaign-manifest.json", "stage-contract.json"],
                ["Generation lanes name runtime gates and use-context caveats.", "Operator-gated tools are marked before execution."],
            ),
            (
                "BSF-BINDER-W02",
                "Cofold Jury Contract",
                ["candidate-jury.example.json", "stage-contract.json"],
                ["Candidate jury schema validates.", "Top-candidate ranking is evidence, not a binding claim."],
            ),
            (
                "BSF-BINDER-W03",
                "Report And Closeout",
                ["README.md", "claim-ledger.md"],
                ["Public report states non-claims.", "Failed or partial lanes downgrade instead of claiming success."],
            ),
        ]
    if mode == "model-jury":
        return [
            (
                "BSF-JURY-W00",
                "Evidence Intake And Claim Contract",
                ["campaign-manifest.json", "target-window-dossier.json", "claim-ledger.md"],
                ["Compared models or structures are public or synthetic.", "Claim ceiling and non-claims are explicit."],
            ),
            (
                "BSF-JURY-W01",
                "Method Disagreement And Failure Rows",
                ["stage-contract.json", "candidate-jury.example.json"],
                ["Jury rows preserve method disagreement.", "Failures and blocked rows are represented instead of dropped."],
            ),
            (
                "BSF-JURY-W02",
                "Review Report And Claim Audit",
                ["README.md", "claim-ledger.md"],
                ["Report separates evidence from interpretation.", "Unsupported validation or binding claims are absent."],
            ),
        ]
    if mode == "structure-dossier":
        return [
            (
                "BSF-DOSSIER-W00",
                "Accession And Evidence Contract",
                ["campaign-manifest.json", "target-window-dossier.json", "claim-ledger.md"],
                ["Public accession, entity/window, and evidence mode are explicit.", "Raw-data or reconstruction work is handed off instead of claimed here."],
            ),
            (
                "BSF-DOSSIER-W01",
                "Validation And Figure Plan",
                ["stage-contract.json", "target-window-dossier.json"],
                ["Expected validation artifacts are listed.", "Figures are planned as report artifacts, not evidence by themselves."],
            ),
            (
                "BSF-DOSSIER-W02",
                "Dossier Report And Closeout",
                ["README.md", "claim-ledger.md"],
                ["Dossier states provenance and downgrade conditions.", "Missing or partial evidence closes as blocked or insufficient_evidence."],
            ),
        ]
    if mode == "screening":
        return [
            (
                "BSF-SCREEN-W00",
                "Scope Fanout And Claim Contract",
                ["campaign-manifest.json", "target-window-dossier.json", "claim-ledger.md"],
                ["Receptor/ligand scope is public or synthetic.", "Fanout and cost-bearing work require an operator gate."],
            ),
            (
                "BSF-SCREEN-W01",
                "Shard And Provider Prep Contract",
                ["stage-contract.json", "campaign-manifest.json"],
                ["Shard boundaries and expected ledgers are explicit.", "Provider prep remains non-launching until authorized."],
            ),
            (
                "BSF-SCREEN-W02",
                "Results Schema And Candidate Dossiers",
                ["stage-contract.json", "claim-ledger.md"],
                ["Result tables preserve failures and method disagreement.", "Candidate dossiers stay computational_candidate or lower."],
            ),
            (
                "BSF-SCREEN-W03",
                "Active Learning And Closeout",
                ["README.md", "claim-ledger.md"],
                ["Follow-on tranche criteria are stated.", "Partial, fixture, or dry-run evidence is downgraded."],
            ),
        ]
    raise ValueError(f"unsupported campaign mode for issue dry-run: {mode}")


def issue_dry_run(campaign_dir: Path, out_dir: Path) -> dict[str, Any]:
    ok, findings = validate_campaign(campaign_dir)
    if not ok:
        return {"ok": False, "findings": [finding.to_dict() for finding in findings]}
    campaign = read_json(campaign_dir / "campaign-manifest.json")
    campaign_path = repo_relative(campaign_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    issues = issue_plan_for_campaign(campaign)
    written: list[str] = []
    previous_issue = "none"
    for issue_id, title, owned_paths, acceptance in issues:
        filename = f"{issue_id}-{title.lower().replace(' ', '-')}.md"
        path = out_dir / filename
        path.write_text(
            render_issue(campaign, issue_id, title, owned_paths, acceptance, campaign_path, previous_issue),
            encoding="utf-8",
        )
        written.append(path.as_posix())
        previous_issue = issue_id
    return {"ok": True, "issue_count": len(written), "issues": written}


def cmd_audit(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ok, findings = audit_tree(root)
    write_json({"ok": ok, "root": root.as_posix(), "finding_count": len(findings), "findings": [finding.to_dict() for finding in findings]})
    return 0 if ok else 1


def cmd_validate(args: argparse.Namespace) -> int:
    campaign_dir = Path(args.campaign_dir).resolve()
    ok, findings = validate_campaign(campaign_dir)
    write_json({"ok": ok, "campaign_dir": campaign_dir.as_posix(), "finding_count": len(findings), "findings": [finding.to_dict() for finding in findings]})
    return 0 if ok else 1


def cmd_issue_dry_run(args: argparse.Namespace) -> int:
    result = issue_dry_run(Path(args.campaign_dir).resolve(), Path(args.out).resolve())
    write_json(result)
    return 0 if result.get("ok") else 1


def cmd_harness_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ok, findings = harness_check(root)
    write_json({"ok": ok, "root": root.as_posix(), "finding_count": len(findings), "findings": [finding.to_dict() for finding in findings]})
    return 0 if ok else 1


def cmd_catalog(args: argparse.Namespace) -> int:
    result = capability_catalog(Path(args.root).resolve())
    if args.format == "markdown":
        rendered = catalog_markdown(result)
        if args.out:
            out = Path(args.out).resolve()
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if result.get("ok") else 1

    if args.out:
        out = Path(args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_json(result)
    return 0 if result.get("ok") else 1


def cmd_scaffold_campaign(args: argparse.Namespace) -> int:
    try:
        result = scaffold_campaign(
            Path(args.out_dir).resolve(),
            campaign_id=args.campaign_id,
            target_label=args.target_label,
            public_accession=args.public_accession,
            window=args.window,
            mode=args.mode,
            force=args.force,
        )
    except ValueError as exc:
        write_json({"ok": False, "error": str(exc)})
        return 2
    write_json(result)
    return 0 if result.get("ok") else 1


def cmd_doctor(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    example = (root / args.example).resolve()
    checks: list[dict[str, Any]] = []

    harness_ok, harness_findings = harness_check(root)
    checks.append(
        {
            "id": "harness-check",
            "ok": harness_ok,
            "finding_count": len(harness_findings),
            "findings": [finding.to_dict() for finding in harness_findings],
        }
    )

    audit_ok, audit_findings = audit_tree(root)
    checks.append(
        {
            "id": "public-audit",
            "ok": audit_ok,
            "finding_count": len(audit_findings),
            "findings": [finding.to_dict() for finding in audit_findings],
        }
    )

    validate_ok, validate_findings = validate_campaign(example)
    checks.append(
        {
            "id": "example-validate",
            "ok": validate_ok,
            "campaign_dir": example.as_posix(),
            "finding_count": len(validate_findings),
            "findings": [finding.to_dict() for finding in validate_findings],
        }
    )

    ok = all(check["ok"] for check in checks)
    write_json(
        {
            "ok": ok,
            "root": root.as_posix(),
            "example": example.as_posix(),
            "checks": checks,
            "next_commands": [
                "bsf catalog .",
                "bsf catalog . --format markdown",
                "bsf scaffold-campaign .runtime/my-target-demo --campaign-id my-target-demo --target-label '<public target>' --public-accession '<PDB:ID>' --window '<residue window>'",
                "bsf issue-dry-run examples/pd-l1-binder-design-public --out .runtime/pd-l1-issues",
                "make public-switch-check",
            ],
        }
    )
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bsf", description="Public-safe BioSymphony Structure Factory validator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="scan a repo tree for public-safety blockers")
    audit.add_argument("root", nargs="?", default=".")
    audit.set_defaults(func=cmd_audit)

    validate = subparsers.add_parser("validate", help="validate a public Structure Factory campaign example")
    validate.add_argument("campaign_dir")
    validate.set_defaults(func=cmd_validate)

    dry_run = subparsers.add_parser("issue-dry-run", help="render tracker-neutral Symphony/Linear issue drafts")
    dry_run.add_argument("campaign_dir")
    dry_run.add_argument("--out", required=True)
    dry_run.set_defaults(func=cmd_issue_dry_run)

    harness = subparsers.add_parser("harness-check", help="verify public BioSymphony agentic harness entry points")
    harness.add_argument("root", nargs="?", default=".")
    harness.set_defaults(func=cmd_harness_check)

    catalog = subparsers.add_parser("catalog", help="summarize available campaigns, examples, issue packs, and provider contracts")
    catalog.add_argument("root", nargs="?", default=".")
    catalog.add_argument("--format", choices=["json", "markdown"], default="json", help="output format")
    catalog.add_argument("--out", help="optional path to also write the rendered catalog")
    catalog.set_defaults(func=cmd_catalog)

    scaffold = subparsers.add_parser("scaffold-campaign", help="create a public-safe starter campaign skeleton")
    scaffold.add_argument("out_dir")
    scaffold.add_argument("--campaign-id", required=True, help="lowercase slug, e.g. pd-l1-binder-public")
    scaffold.add_argument("--target-label", required=True, help="human-readable target label")
    scaffold.add_argument("--public-accession", required=True, help="public accession or synthetic fixture label")
    scaffold.add_argument("--window", required=True, help="residue/window/region description")
    scaffold.add_argument(
        "--mode",
        choices=["binder-design", "model-jury", "structure-dossier", "screening"],
        default="binder-design",
    )
    scaffold.add_argument("--force", action="store_true", help="allow writing into a non-empty output directory")
    scaffold.set_defaults(func=cmd_scaffold_campaign)

    doctor = subparsers.add_parser("doctor", help="run local public harness, audit, and example validation checks")
    doctor.add_argument("root", nargs="?", default=".")
    doctor.add_argument("--example", default="examples/pd-l1-binder-design-public", help="repo-relative campaign example to validate")
    doctor.set_defaults(func=cmd_doctor)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

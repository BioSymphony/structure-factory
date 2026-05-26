"""Helpers for writing public-safe bridge-manifest templates."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


PUBLIC_TEMPLATE_STATUS = "non_launchable_public_template"
PUBLIC_TEMPLATE_NOTE = (
    "Public template only. This file documents the expected provider bridge-manifest shape. "
    "It is not execution-ready until a human/operator gate records current license/use context, "
    "budget, placement, a pushed public-safe commit SHA, provider credentials by reference, "
    "and cleanup policy outside public git."
)
PUBLIC_STARTUP_COMMANDS = [
    "set -euo pipefail",
    "echo 'Public non-launchable template. Rebuild a private/operator-gated launch packet from tracked source before execution.'",
    "exit 64",
]


def make_public_bridge_template(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return a non-launchable public template version of a bridge manifest."""
    public = deepcopy(manifest)
    public["remote_launch_allowed"] = False
    public["public_template_status"] = PUBLIC_TEMPLATE_STATUS
    public["public_template_note"] = PUBLIC_TEMPLATE_NOTE

    authorization = public.setdefault("launch_authorization", {})
    authorization["approved_at"] = "PENDING"
    authorization["approved_by"] = "PENDING-OPERATOR-GATE"
    authorization["linear_issue_url"] = "PENDING-TRACKER-ISSUE"
    authorization["source"] = "templates/operator-wave-runbook.md"
    authorization["scope"] = PUBLIC_TEMPLATE_NOTE

    startup = public.setdefault("startup", {})
    startup["commands"] = list(PUBLIC_STARTUP_COMMANDS)
    startup.setdefault("mode", "dockerStartCmd")
    inspection = startup.setdefault("inspection", {})
    inspection["hold_after_success_seconds"] = 0
    inspection["http_artifact_server_port"] = None

    runpod = public.setdefault("runpod", {})
    runpod["imageDigestRequiredForReal"] = True
    if "dataCenterIds" in runpod:
        runpod["dataCenterIds"] = []
    if "networkVolumeId" in runpod and runpod["networkVolumeId"] not in {"", "STRUCTURE_FACTORY_RUNPOD_NETWORK_VOLUME_ID"}:
        runpod["networkVolumeId"] = "STRUCTURE_FACTORY_RUNPOD_NETWORK_VOLUME_ID"

    safety = public.setdefault("safety", {})
    safety["public_template_policy"] = (
        "No secrets, concrete provider resources, private volume assumptions, prior-run artifacts, "
        "accepted-license state, or launchable startup payloads are encoded in this public manifest."
    )

    repo = public.setdefault("repo", {})
    repo.setdefault(
        "commit_or_snapshot_pin_policy",
        "Execution-ready packets must pin an immutable public-safe source ref outside public git.",
    )
    return public

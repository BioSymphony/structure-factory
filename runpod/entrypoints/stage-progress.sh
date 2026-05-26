#!/usr/bin/env bash
set -euo pipefail

sf_progress_path() {
  local run_id="${STRUCTURE_FACTORY_RUN_ID:-structure-factory-run}"
  local volume_root="${STRUCTURE_FACTORY_VOLUME_ROOT:-/workspace/structure-factory}"
  printf '%s/runs/%s/stage-progress.jsonl' "${volume_root}" "${run_id}"
}

sf_stage_event() {
  local stage_id="$1"
  local status="$2"
  local message="${3:-}"
  local progress_path="${STRUCTURE_FACTORY_STAGE_PROGRESS:-$(sf_progress_path)}"
  mkdir -p "$(dirname "${progress_path}")"
  python3 - "$progress_path" "$stage_id" "$status" "$message" <<'PY'
import json
import sys
from datetime import datetime, timezone

path, stage_id, status, message = sys.argv[1:5]
event = {
    "schema_version": 1,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "stage_id": stage_id,
    "status": status,
    "message": message,
}
with open(path, "a", encoding="utf-8") as handle:
    handle.write(json.dumps(event, sort_keys=True) + "\n")
PY
}

sf_stage_start() {
  sf_stage_event "$1" "started" "${2:-}"
}

sf_stage_complete() {
  sf_stage_event "$1" "completed" "${2:-}"
}

sf_stage_fail() {
  sf_stage_event "$1" "failed" "${2:-}"
}

sf_partial_summary() {
  local failed_stage="$1"
  local claim_level="${2:-degraded}"
  local resume_command="${3:-rerun the failed stage command from the stage contract}"
  local artifact_status="${4:-partial}"
  local run_id="${STRUCTURE_FACTORY_RUN_ID:-structure-factory-run}"
  local volume_root="${STRUCTURE_FACTORY_VOLUME_ROOT:-/workspace/structure-factory}"
  local run_root="${volume_root}/runs/${run_id}"
  local progress_path="${STRUCTURE_FACTORY_STAGE_PROGRESS:-$(sf_progress_path)}"
  mkdir -p "${run_root}"
  python3 - "$run_root/partial-summary.json" "$progress_path" "$failed_stage" "$claim_level" "$resume_command" "$artifact_status" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

out, progress_path, failed_stage, claim_level, resume_command, artifact_status = sys.argv[1:7]
events = []
path = Path(progress_path)
if path.exists():
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append({"parse_error": True})
completed = [
    event.get("stage_id")
    for event in events
    if event.get("status") == "completed" and event.get("stage_id")
]
summary = {
    "schema_version": 1,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "completed_stages": completed,
    "failed_stage": failed_stage,
    "resume_command": resume_command,
    "artifact_status": artifact_status,
    "claim_level": claim_level,
    "progress_ledger": str(path),
}
Path(out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
PY
}

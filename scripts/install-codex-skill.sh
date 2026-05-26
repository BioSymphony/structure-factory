#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST_ROOT="${1:-${HOME}/.codex/skills}"
SRC="${ROOT}/skills/biosymphony-structure-factory"
DEST="${DEST_ROOT}/biosymphony-structure-factory"

if [ ! -f "${SRC}/SKILL.md" ]; then
  echo "missing portable skill at ${SRC}/SKILL.md" >&2
  exit 2
fi

mkdir -p "${DEST_ROOT}"
rm -rf "${DEST}"
cp -R "${SRC}" "${DEST}"

echo "Installed BioSymphony Structure Factory skill to ${DEST}"
echo "Run from the repo root: make harness-check"

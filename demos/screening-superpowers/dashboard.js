const RUNTIME_BASE = "../../.runtime/screening-superpowers-fixture/";

const REQUIRED_ARTIFACTS = [
  "screening_manifest.json",
  "validation/input-audit.json",
  "validation/contract-self-check.json",
  "ligand_prep.jsonl",
  "pose_predictions.jsonl",
  "affinity_predictions.jsonl",
  "consensus_ranking.csv",
  "metrics.json",
  "method_summary.json",
  "method_disagreement.jsonl",
  "scaffold_atlas.json",
  "active_learning_tranches.json",
  "rescue_queue.json",
  "evidence_graph.json",
  "selection_rationale.md",
  "failure_report.json",
  "claim_ledger.json",
  "stage-progress.jsonl",
  "executed-commands.jsonl",
  "provenance.md"
];

const OPTIONAL_ARTIFACTS = [
  "receptor_ensemble_manifest.json",
  "validation/screening-manifest-check.json",
  "validation/screening-results-check.json",
  "validation/active-learning-check.json",
  "validation/fanout-estimate.json"
];

const state = {
  files: new Map(),
  source: "runtime",
  selectedArtifact: "",
  search: ""
};

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("loadRuntimeButton").addEventListener("click", () => {
    loadRuntimeArtifacts();
  });
  document.getElementById("artifactFolderInput").addEventListener("change", loadFolderArtifacts);
  document.getElementById("artifactSearch").addEventListener("input", (event) => {
    state.search = event.target.value.trim().toLowerCase();
    renderArtifacts(buildBundle());
  });
  document.getElementById("artifactList").addEventListener("click", (event) => {
    const button = event.target.closest("[data-artifact-path]");
    if (!button) return;
    state.selectedArtifact = button.dataset.artifactPath;
    renderArtifacts(buildBundle());
  });

  loadRuntimeArtifacts();
});

async function loadRuntimeArtifacts() {
  setRunStatus("Loading runtime fixture artifacts", "loading");
  const files = new Map();
  for (const path of [...REQUIRED_ARTIFACTS, ...OPTIONAL_ARTIFACTS]) {
    const artifact = await fetchArtifact(path);
    if (artifact || REQUIRED_ARTIFACTS.includes(path)) {
      files.set(path, artifact || missingArtifact(path));
    }
  }

  const manifestArtifact = files.get("screening_manifest.json");
  const manifest = manifestArtifact && manifestArtifact.status === "present"
    ? parseArtifact(manifestArtifact, {})
    : {};
  const promoteTopN = Number(manifest.outputs && manifest.outputs.promote_top_n) || 0;
  const rankingArtifact = files.get("consensus_ranking.csv");
  const rankingRows = rankingArtifact && rankingArtifact.status === "present"
    ? parseCsv(rankingArtifact.text)
    : [];
  for (const row of rankingRows.slice(0, promoteTopN)) {
    const ligandId = String(row.ligand_id || "").trim();
    if (!ligandId) continue;
    const dossierPath = `candidate_dossiers/${ligandId}.json`;
    const dossier = await fetchArtifact(dossierPath);
    if (dossier) files.set(dossierPath, dossier);
  }

  state.files = files;
  state.source = "runtime";
  state.selectedArtifact = firstPresentArtifact(files);
  render();
}

async function fetchArtifact(path) {
  try {
    const response = await fetch(`${RUNTIME_BASE}${path}`, { cache: "no-store" });
    if (!response.ok) return null;
    const text = await response.text();
    return {
      path,
      kind: artifactKind(path),
      required: REQUIRED_ARTIFACTS.includes(path),
      status: "present",
      size: text.length,
      text
    };
  } catch (_error) {
    return null;
  }
}

async function loadFolderArtifacts(event) {
  const selected = Array.from(event.target.files || []);
  const files = new Map();
  for (const file of selected) {
    const path = normalizeSelectedPath(file);
    if (!path) continue;
    files.set(path, {
      path,
      kind: artifactKind(path),
      required: REQUIRED_ARTIFACTS.includes(path),
      status: "present",
      size: file.size,
      text: await file.text()
    });
  }
  for (const path of REQUIRED_ARTIFACTS) {
    if (!files.has(path)) files.set(path, missingArtifact(path));
  }
  state.files = files;
  state.source = "folder";
  state.selectedArtifact = firstPresentArtifact(files);
  event.target.value = "";
  render();
}

function normalizeSelectedPath(file) {
  let relPath = (file.webkitRelativePath || file.name || "").replace(/\\/g, "/");
  const marker = "screening-superpowers-fixture/";
  const markerIndex = relPath.indexOf(marker);
  if (markerIndex >= 0) return relPath.slice(markerIndex + marker.length);
  const parts = relPath.split("/").filter(Boolean);
  if (parts.length > 1) return parts.slice(1).join("/");
  return relPath;
}

function missingArtifact(path) {
  return {
    path,
    kind: artifactKind(path),
    required: REQUIRED_ARTIFACTS.includes(path),
    status: "missing",
    size: 0,
    text: ""
  };
}

function firstPresentArtifact(files) {
  const preferred = ["metrics.json", "consensus_ranking.csv", "claim_ledger.json"];
  for (const path of preferred) {
    const artifact = files.get(path);
    if (artifact && artifact.status === "present") return path;
  }
  const first = Array.from(files.values()).find((artifact) => artifact.status === "present");
  return first ? first.path : "";
}

function artifactKind(path) {
  if (path.endsWith(".json")) return "json";
  if (path.endsWith(".jsonl")) return "jsonl";
  if (path.endsWith(".csv")) return "csv";
  if (path.endsWith(".md") || path.endsWith(".txt") || path.endsWith(".log")) return "text";
  return "artifact";
}

function buildBundle() {
  const files = state.files;
  const getJson = (path, fallback = {}) => parseArtifact(files.get(path), fallback);
  const getRows = (path) => parseArtifact(files.get(path), []);
  const manifest = getJson("screening_manifest.json");
  const metrics = getJson("metrics.json");
  const claimLedger = getJson("claim_ledger.json");
  const ranking = getRows("consensus_ranking.csv");
  const dossiers = Array.from(files.values())
    .filter((artifact) => artifact.path.startsWith("candidate_dossiers/") && artifact.status === "present")
    .map((artifact) => parseArtifact(artifact, null))
    .filter(Boolean)
    .sort((left, right) => Number(left.rank || 0) - Number(right.rank || 0));
  const artifacts = Array.from(files.values()).sort((left, right) => {
    const leftIndex = [...REQUIRED_ARTIFACTS, ...OPTIONAL_ARTIFACTS].indexOf(left.path);
    const rightIndex = [...REQUIRED_ARTIFACTS, ...OPTIONAL_ARTIFACTS].indexOf(right.path);
    if (leftIndex !== -1 || rightIndex !== -1) return (leftIndex === -1 ? 999 : leftIndex) - (rightIndex === -1 ? 999 : rightIndex);
    return left.path.localeCompare(right.path);
  });
  const missingRequired = REQUIRED_ARTIFACTS.filter((path) => {
    const artifact = files.get(path);
    return !artifact || artifact.status !== "present";
  });

  return {
    artifacts,
    missingRequired,
    manifest,
    metrics,
    claimLedger,
    ranking,
    dossiers,
    methods: getJson("method_summary.json").methods || {},
    methodSummary: getJson("method_summary.json"),
    failures: getJson("failure_report.json").failed_ligands || [],
    tranches: getJson("active_learning_tranches.json").tranches || [],
    rescueItems: getJson("rescue_queue.json").items || [],
    disagreement: getRows("method_disagreement.jsonl"),
    scaffoldAtlas: getJson("scaffold_atlas.json"),
    evidenceGraph: getJson("evidence_graph.json"),
    stageProgress: getRows("stage-progress.jsonl"),
    ligandPrep: getRows("ligand_prep.jsonl"),
    source: state.source
  };
}

function parseArtifact(artifact, fallback) {
  if (!artifact || artifact.status !== "present") return fallback;
  try {
    if (artifact.kind === "json") return JSON.parse(artifact.text);
    if (artifact.kind === "jsonl") return parseJsonl(artifact.text);
    if (artifact.kind === "csv") return parseCsv(artifact.text);
    return artifact.text;
  } catch (_error) {
    return fallback;
  }
}

function parseJsonl(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function parseCsv(text) {
  const lines = text.split(/\r?\n/).filter((line) => line.trim());
  if (!lines.length) return [];
  const headers = parseCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    return headers.reduce((row, header, index) => {
      row[header] = values[index] || "";
      return row;
    }, {});
  });
}

function parseCsvLine(line) {
  const cells = [];
  let value = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    const next = line[index + 1];
    if (char === '"' && quoted && next === '"') {
      value += '"';
      index += 1;
      continue;
    }
    if (char === '"') {
      quoted = !quoted;
      continue;
    }
    if (char === "," && !quoted) {
      cells.push(value);
      value = "";
      continue;
    }
    value += char;
  }
  cells.push(value);
  return cells;
}

function render() {
  const bundle = buildBundle();
  renderStatus(bundle);
  renderSummary(bundle);
  renderRanking(bundle);
  renderMethodLanes(bundle);
  renderDossiers(bundle);
  renderClaims(bundle);
  renderTranches(bundle);
  renderRescue(bundle);
  renderArtifacts(bundle);
}

function renderStatus(bundle) {
  const present = bundle.artifacts.filter((artifact) => artifact.status === "present").length;
  if (!present) {
    setRunStatus("No fixture artifacts loaded", "warn");
    return;
  }
  if (bundle.missingRequired.length) {
    setRunStatus(`${present} artifacts loaded, ${bundle.missingRequired.length} required missing`, "warn");
    return;
  }
  const runId = bundle.manifest.run_id || "screening fixture";
  setRunStatus(`${runId}: ${present} artifacts loaded`, "ok");
}

function setRunStatus(message, level = "") {
  const status = document.getElementById("runStatus");
  status.className = `run-strip ${level}`.trim();
  status.textContent = message;
}

function renderSummary(bundle) {
  const metrics = bundle.metrics || {};
  const manifest = bundle.manifest || {};
  const claimLevel = bundle.claimLedger.overall_claim_level || metrics.claim_level || "unknown";
  const evidenceMode = bundle.claimLedger.evidence_mode || metrics.evidence_mode || "unknown";
  const completedStages = bundle.stageProgress.filter((stage) => stage.status === "completed").length;
  const presentArtifacts = bundle.artifacts.filter((artifact) => artifact.status === "present").length;
  const tiles = [
    ["Run", manifest.run_id || "not loaded", evidenceMode],
    ["Ligands", `${metrics.ligands_prepared ?? "-"} / ${metrics.ligands_total ?? "-"}`, `${metrics.ligands_failed ?? 0} failed control`],
    ["Top candidate", metrics.top_ligand_id || "-", formatScore(metrics.top_consensus_score)],
    ["Dossiers", bundle.dossiers.length || metrics.candidate_dossiers || 0, claimLevel],
    ["Artifacts", presentArtifacts, `${completedStages} stages complete`]
  ];
  document.getElementById("summaryBand").innerHTML = tiles.map(([label, value, detail]) => `
    <div class="metric-tile">
      <span class="label">${escapeHtml(label)}</span>
      <strong class="value ${String(value).length > 14 ? "long" : ""}">${escapeHtml(value)}</strong>
      <span class="detail">${escapeHtml(detail)}</span>
    </div>
  `).join("");
}

function renderRanking(bundle) {
  const host = document.getElementById("rankingTable");
  if (!bundle.ranking.length) {
    host.innerHTML = emptyState("No consensus ranking loaded.");
    return;
  }
  host.innerHTML = `
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Ligand</th>
            <th>Consensus</th>
            <th>Vina proxy</th>
            <th>Boltz proxy</th>
            <th>Disagreement</th>
            <th>Claim</th>
          </tr>
        </thead>
        <tbody>
          ${bundle.ranking.map((row) => {
            const score = Number(row.consensus_score || 0);
            const width = Math.max(0, Math.min(100, Math.round(score * 100)));
            return `
              <tr>
                <td class="mono">${escapeHtml(row.rank)}</td>
                <td class="mono">${escapeHtml(row.ligand_id)}</td>
                <td class="score-bar">
                  <div class="score-track"><span style="width: ${width}%"></span></div>
                  <span class="mono">${formatScore(row.consensus_score)}</span>
                </td>
                <td class="mono">${formatScore(row.best_vina_score_proxy)}</td>
                <td class="mono">${formatScore(row.boltz_affinity_probability_proxy)}</td>
                <td class="mono">${formatScore(row.method_disagreement_proxy)}</td>
                <td>${badge(row.claim_level, row.claim_level)}</td>
              </tr>
            `;
          }).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderMethodLanes(bundle) {
  const methods = Object.entries(bundle.methods || {});
  const calibration = bundle.methodSummary.openbind_style_calibration || {};
  const host = document.getElementById("methodLanes");
  if (!methods.length) {
    host.innerHTML = emptyState("No method summary loaded.");
    return;
  }
  host.innerHTML = `
    <div class="method-list">
      ${methods.map(([name, info]) => `
        <div class="method-item">
          <h3>${escapeHtml(name)}</h3>
          <p>${badge(info.status, info.status)} ${escapeHtml(info.claim_role || "")}</p>
        </div>
      `).join("")}
      <div class="method-item">
        <h3>Calibration baselines</h3>
        <p>${escapeHtml((calibration.simple_baselines_included || []).join(", ") || "not recorded")}</p>
      </div>
    </div>
  `;
}

function renderDossiers(bundle) {
  const host = document.getElementById("dossierGrid");
  if (!bundle.dossiers.length) {
    host.innerHTML = emptyState("No candidate dossiers loaded.");
    return;
  }
  host.innerHTML = bundle.dossiers.map((dossier) => {
    const evidence = dossier.candidate_evidence || {};
    return `
      <article class="dossier-item">
        <h3><span class="mono">#${escapeHtml(dossier.rank)}</span> ${escapeHtml(dossier.ligand_id)}</h3>
        <p>${escapeHtml(dossier.selection_reason || "fixture candidate")}</p>
        <div class="dossier-stats">
          <span>Consensus<strong>${formatScore(evidence.consensus_score)}</strong></span>
          <span>Boltz proxy<strong>${formatScore(evidence.boltz_affinity_probability_proxy)}</strong></span>
          <span>Disagree<strong>${formatScore(evidence.method_disagreement_proxy)}</strong></span>
        </div>
        <p class="mono">${escapeHtml(dossier.caveat || dossier.evidence_mode || "")}</p>
      </article>
    `;
  }).join("");
}

function renderClaims(bundle) {
  const claims = bundle.claimLedger.claims || [];
  const host = document.getElementById("claimLedger");
  if (!claims.length) {
    host.innerHTML = "";
    return;
  }
  host.innerHTML = `
    <div class="claim-list">
      ${claims.map((claim) => `
        <div class="claim-item">
          <h3>${badge(claim.level, claim.level)} ${escapeHtml(claim.claim)}</h3>
          <p>${escapeHtml((claim.evidence || []).join(", "))}</p>
        </div>
      `).join("")}
    </div>
  `;
}

function renderTranches(bundle) {
  const host = document.getElementById("trancheList");
  if (!bundle.tranches.length) {
    host.innerHTML = emptyState("No active-learning tranches loaded.");
    return;
  }
  host.innerHTML = `
    <div class="tranche-list">
      ${bundle.tranches.map((tranche) => `
        <div class="tranche-item">
          <h3>${escapeHtml(tranche.tranche_id)}</h3>
          <p><span class="mono">${escapeHtml((tranche.ligand_ids || []).join(", ") || "none")}</span></p>
          <p>${escapeHtml(tranche.selection_axis || "")}</p>
        </div>
      `).join("")}
    </div>
  `;
}

function renderRescue(bundle) {
  const host = document.getElementById("rescueQueue");
  const rescue = bundle.rescueItems.length
    ? bundle.rescueItems
    : bundle.failures.map((failure) => ({
      ligand_id: failure.ligand_id,
      failure_stage: failure.stage,
      failure_reason: failure.reason,
      claim_level: failure.claim_level
    }));
  if (!rescue.length) {
    host.innerHTML = emptyState("No rescue items loaded.");
    return;
  }
  host.innerHTML = `
    <div class="rescue-list">
      ${rescue.map((item) => `
        <div class="rescue-item">
          <h3>${escapeHtml(item.ligand_id || "unknown")}</h3>
          <p>${badge(item.claim_level || "blocked", item.claim_level || "blocked")} ${escapeHtml(item.failure_stage || "")}</p>
          <p>${escapeHtml(item.failure_reason || item.recommended_action || "")}</p>
        </div>
      `).join("")}
    </div>
  `;
}

function renderArtifacts(bundle) {
  const list = document.getElementById("artifactList");
  const preview = document.getElementById("artifactPreview");
  const query = state.search;
  const filtered = bundle.artifacts.filter((artifact) => !query || artifact.path.toLowerCase().includes(query) || artifact.kind.includes(query));

  if (!state.selectedArtifact || !state.files.has(state.selectedArtifact)) {
    state.selectedArtifact = firstPresentArtifact(state.files);
  }

  list.innerHTML = filtered.map((artifact) => `
    <button class="artifact-row ${artifact.status} ${artifact.path === state.selectedArtifact ? "active" : ""}" type="button" data-artifact-path="${escapeHtml(artifact.path)}">
      <strong>${escapeHtml(artifact.path)}</strong>
      <span>${escapeHtml(artifact.status)} ${escapeHtml(artifact.kind)}</span>
    </button>
  `).join("") || `<div class="empty-state">No artifacts match the filter.</div>`;

  const selected = state.files.get(state.selectedArtifact);
  preview.textContent = artifactPreview(selected);
}

function artifactPreview(artifact) {
  if (!artifact) return "No artifact selected.";
  if (artifact.status !== "present") return `${artifact.path}\n\nRequired artifact is missing from the loaded fixture.`;
  const parsed = parseArtifact(artifact, null);
  if (parsed && typeof parsed === "object") return JSON.stringify(parsed, null, 2);
  return artifact.text || "";
}

function badge(value, label) {
  const normalized = String(value || "unknown").toLowerCase().replace(/[^a-z0-9_-]/g, "_");
  return `<span class="badge ${escapeHtml(normalized)}">${escapeHtml(label || value || "unknown")}</span>`;
}

function emptyState(message) {
  return `<div class="empty-state">${escapeHtml(message)}</div>`;
}

function formatScore(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return "-";
  return number.toFixed(3);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

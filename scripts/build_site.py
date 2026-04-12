from __future__ import annotations

import json
from pathlib import Path

POSTMORTEM_DIR = Path("atlas/data/postmortems")
SITE_DIR = Path("site")
INDEX_HTML = SITE_DIR / "index.html"
DATA_JS = SITE_DIR / "postmortems.js"

HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Postmortem Atlas</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; max-width: 1100px; }
    input, select { padding: 10px; margin-right: 8px; margin-bottom: 12px; }
    .card { border: 1px solid #ddd; border-radius: 10px; padding: 16px; margin: 16px 0; }
    .muted { color: #666; font-size: 14px; }
    .pill { display: inline-block; padding: 4px 8px; margin: 4px 6px 0 0; border-radius: 999px; background: #f2f2f2; font-size: 12px; }
    a { text-decoration: none; }
  </style>
</head>
<body>
  <h1>Postmortem Atlas</h1>
  <p>Structured public outage postmortems, normalized by failure type, detection gap, system layer, and recovery pattern.</p>

  <input id="search" placeholder="Search company, title, failure type, tags..." size="48" />
  <select id="companyFilter"><option value="">All companies</option></select>
  <select id="failureFilter"><option value="">All failure types</option></select>
  <select id="layerFilter"><option value="">All system layers</option></select>
  <select id="detectionFilter"><option value="">All detection methods</option></select>

  <div id="results"></div>

  <script src="./postmortems.js"></script>
  <script>
    const resultsEl = document.getElementById("results");
    const searchEl = document.getElementById("search");
    const companyFilterEl = document.getElementById("companyFilter");
    const failureFilterEl = document.getElementById("failureFilter");
    const layerFilterEl = document.getElementById("layerFilter");
    const detectionFilterEl = document.getElementById("detectionFilter");

    const companies = [...new Set(POSTMORTEMS.map(p => p.company))].sort();
    const failureTypes = [...new Set(POSTMORTEMS.flatMap(p => p.failure_taxonomy))].sort();
    const layers = [...new Set(POSTMORTEMS.flatMap(p => p.system_layers || []))].sort();
    const detectionMethods = [...new Set(POSTMORTEMS.map(p => p.detection_method).filter(Boolean))].sort();

    for (const company of companies) {
      const opt = document.createElement("option");
      opt.value = company;
      opt.textContent = company;
      companyFilterEl.appendChild(opt);
    }

    for (const ft of failureTypes) {
      const opt = document.createElement("option");
      opt.value = ft;
      opt.textContent = ft;
      failureFilterEl.appendChild(opt);
    }

    for (const layer of layers) {
      const opt = document.createElement("option");
      opt.value = layer;
      opt.textContent = layer;
      layerFilterEl.appendChild(opt);
    }

    for (const method of detectionMethods) {
      const opt = document.createElement("option");
      opt.value = method;
      opt.textContent = method;
      detectionFilterEl.appendChild(opt);
    }

    function matches(pm) {
      const q = searchEl.value.trim().toLowerCase();
      const company = companyFilterEl.value;
      const failure = failureFilterEl.value;
      const layer = layerFilterEl.value;
      const detection = detectionFilterEl.value;

      const haystack = [
        pm.company, pm.title, pm.summary, pm.root_cause, pm.atlas_lessons,
        ...(pm.failure_taxonomy || []),
        ...(pm.system_layers || []),
        ...(pm.tags || [])
      ].join(" ").toLowerCase();

      if (q && !haystack.includes(q)) return false;
      if (company && pm.company !== company) return false;
      if (failure && !(pm.failure_taxonomy || []).includes(failure)) return false;
      if (layer && !(pm.system_layers || []).includes(layer)) return false;
      if (detection && pm.detection_method !== detection) return false;
      return true;
    }

    function render() {
      const filtered = POSTMORTEMS.filter(matches);
      resultsEl.innerHTML = filtered.map(pm => `
        <div class="card">
          <h2>${pm.title}</h2>
          <div class="muted">${pm.company} · ${pm.date} · Detection gap: ${pm.detection_gap_minutes} min</div>
          <p>${pm.summary}</p>
          <p><strong>Root cause:</strong> ${pm.root_cause}</p>
          <p><strong>Recovery:</strong> ${(pm.recovery_pattern || []).join(", ")}</p>
          <p><strong>What would have caught it earlier:</strong> ${(pm.what_would_have_caught_it_earlier || []).join("; ")}</p>
          <p><strong>Atlas lesson:</strong> ${pm.atlas_lessons}</p>
          <p><a href="${pm.source_url}" target="_blank" rel="noreferrer">Source postmortem</a></p>
          <div>${(pm.failure_taxonomy || []).map(x => `<span class="pill">${x}</span>`).join("")}</div>
          <div>${(pm.system_layers || []).map(x => `<span class="pill">${x}</span>`).join("")}</div>
          <div>${(pm.tags || []).map(x => `<span class="pill">${x}</span>`).join("")}</div>
        </div>
      `).join("");
    }

    searchEl.addEventListener("input", render);
    companyFilterEl.addEventListener("change", render);
    failureFilterEl.addEventListener("change", render);
    layerFilterEl.addEventListener("change", render);
    detectionFilterEl.addEventListener("change", render);
    render();
  </script>
</body>
</html>
"""

def main() -> int:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    postmortems = []
    for path in sorted(POSTMORTEM_DIR.glob("*.json")):
        postmortems.append(json.loads(path.read_text(encoding="utf-8")))

    DATA_JS.write_text(
        "const POSTMORTEMS = " + json.dumps(postmortems, indent=2) + ";",
        encoding="utf-8",
    )
    INDEX_HTML.write_text(HTML, encoding="utf-8")
    print(f"Built {INDEX_HTML}")
    print(f"Built {DATA_JS}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>NY Metro Ops - LGA Editor</title>
  <style>
    :root {
      --bg: #07090c;
      --panel: #11141a;
      --border: #2b3038;
      --text: #e9edf4;
      --muted: #8c96a8;
      --arrival: #ff4d4d;
      --departure: #2ecc71;
      --accent: #66a3ff;
      --soft: rgba(255,255,255,.06);
      --shadow: 0 18px 45px rgba(0,0,0,.45);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background:
        radial-gradient(circle at top, rgba(102,163,255,.12), transparent 38%),
        linear-gradient(180deg, #0a0d12, #07090c);
      color: var(--text);
      font-family: Inter, Arial, Helvetica, sans-serif;
    }

    .page {
      max-width: 1520px;
      margin: 0 auto;
      padding: 18px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 20px;
      margin-bottom: 14px;
    }

    .brand {
      display: flex;
      align-items: baseline;
      gap: 16px;
      flex-wrap: wrap;
    }

    h1 {
      margin: 0;
      font-size: clamp(28px, 3vw, 44px);
      line-height: 1;
      letter-spacing: .04em;
      font-weight: 900;
      color: #f7f9fb;
    }

    .tagline {
      color: var(--muted);
      text-transform: uppercase;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .22em;
    }

    .updated-box {
      border: 1px solid var(--border);
      background: linear-gradient(180deg, #141923, #0d1117);
      box-shadow: var(--shadow);
      padding: 10px 14px;
      font-size: 12px;
      text-align: right;
      min-width: 250px;
      color: #d9deea;
    }

    .updated-box strong {
      display: block;
      font-size: 15px;
      margin-top: 3px;
      color: #fff;
    }

    .layout {
      display: grid;
      grid-template-columns: 330px minmax(0, 1fr);
      gap: 14px;
      align-items: start;
    }

    .card,
    .diagram-panel {
      background: linear-gradient(180deg, #12161d, #0d1015);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      border-radius: 18px;
      overflow: hidden;
    }

    .card {
      padding: 14px;
      margin-bottom: 12px;
    }

    .airport-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      border-bottom: 1px solid rgba(255,255,255,.09);
      padding-bottom: 10px;
      margin-bottom: 8px;
    }

    .airport-code {
      font-size: 42px;
      font-weight: 900;
      line-height: 1;
      color: #fff;
    }

    .airport-name {
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .1em;
      font-weight: 800;
    }

    .live-badge {
      border: 1px solid rgba(46,204,113,.55);
      background: rgba(46,204,113,.15);
      color: #b8ffd0;
      padding: 6px 9px;
      font-size: 12px;
      font-weight: 900;
      letter-spacing: .08em;
      border-radius: 999px;
      box-shadow: 0 0 0 1px rgba(46,204,113,.08) inset;
    }

    .field {
      display: grid;
      grid-template-columns: 120px 1fr;
      gap: 8px;
      border-bottom: 1px solid rgba(255,255,255,.08);
      padding: 8px 0;
      font-size: 14px;
    }

    .label {
      color: var(--muted);
      text-transform: uppercase;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: .07em;
    }

    .value {
      font-weight: 800;
      color: #f2f6ff;
      word-break: break-word;
    }

    details {
      margin-top: 10px;
      border-top: 1px solid rgba(255,255,255,.08);
      padding-top: 10px;
    }

    summary {
      cursor: pointer;
      list-style: none;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: .1em;
      color: var(--muted);
      font-weight: 900;
    }

    summary::-webkit-details-marker { display: none; }

    .raw-atis {
      margin-top: 10px;
      border: 1px solid rgba(255,255,255,.08);
      padding: 10px;
      font-family: "Courier New", monospace;
      font-size: 11px;
      line-height: 1.45;
      white-space: pre-wrap;
      background: #0a0c11;
      color: #d6dce8;
      max-height: 260px;
      overflow: auto;
    }

    .diagram-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 14px;
      padding: 14px 16px 12px;
      border-bottom: 1px solid rgba(255,255,255,.09);
    }

    .diagram-title {
      font-size: 22px;
      font-weight: 900;
      letter-spacing: .02em;
      color: #fff;
    }

    .diagram-sub {
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 800;
    }

    .airport-location {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 800;
      text-align: right;
    }

    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 12px 14px 0;
      align-items: center;
    }

    .toolbar .group {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
      padding: 8px;
      border: 1px solid rgba(255,255,255,.09);
      border-radius: 12px;
      background: rgba(255,255,255,.03);
    }

    .tool-label {
      font-size: 11px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 800;
      margin-right: 2px;
    }

    .tool-btn {
      appearance: none;
      border: 1px solid rgba(255,255,255,.12);
      background: #11151c;
      color: #dce3f3;
      border-radius: 999px;
      padding: 7px 10px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      transition: transform .08s ease, background .15s ease, border-color .15s ease;
    }

    .tool-btn:hover { transform: translateY(-1px); }
    .tool-btn.active {
      background: var(--accent);
      border-color: rgba(102,163,255,.8);
      color: #fff;
    }

    .tool-btn.arrival.active { background: var(--arrival); border-color: rgba(255,77,77,.8); }
    .tool-btn.departure.active { background: var(--departure); border-color: rgba(46,204,113,.8); }

    .tool-btn.secondary {
      color: #fff;
      background: #0f1319;
    }

    .tool-readout {
      margin-left: auto;
      font-size: 12px;
      color: #c8d0df;
      font-weight: 700;
      letter-spacing: .02em;
    }

    .diagram-wrap {
      padding: 14px;
    }

    .stage {
      position: relative;
      width: min(100%, 1040px);
      margin: 0 auto;
      background: #050608;
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.03);
      user-select: none;
    }

    .stage img {
      display: block;
      width: 100%;
      height: auto;
      background: #050608;
      filter: saturate(.95) contrast(1.02);
      mix-blend-mode: normal;
      opacity: .98;
      user-select: none;
      pointer-events: none;
    }

    .overlay-svg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
    }

    .overlay-hint {
      position: absolute;
      left: 14px;
      bottom: 14px;
      z-index: 8;
      padding: 8px 10px;
      border: 1px solid rgba(255,255,255,.14);
      border-radius: 10px;
      background: rgba(0,0,0,.45);
      color: #e6ebf5;
      font-size: 12px;
      letter-spacing: .02em;
      backdrop-filter: blur(4px);
      max-width: calc(100% - 28px);
    }

    .legend {
      display: flex;
      gap: 18px;
      align-items: center;
      border-top: 1px solid rgba(255,255,255,.08);
      padding: 10px 14px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 900;
      color: #d6dcea;
      flex-wrap: wrap;
    }

    .legend-dot {
      display: inline-block;
      width: 12px;
      height: 12px;
      border-radius: 999px;
      margin-right: 6px;
      vertical-align: -1px;
      box-shadow: 0 0 0 2px rgba(255,255,255,.08);
    }

    .legend-dot.arrival { background: var(--arrival); }
    .legend-dot.departure { background: var(--departure); }

    .statusbar {
      border-top: 1px solid rgba(255,255,255,.08);
      padding: 10px 14px;
      color: var(--muted);
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: .08em;
      font-weight: 800;
      display: flex;
      gap: 14px;
      justify-content: space-between;
      flex-wrap: wrap;
    }

    .statusbar .left, .statusbar .right {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
    }

    .dim {
      color: #c2cbdb;
      font-weight: 800;
    }

    @media (max-width: 1000px) {
      .layout { grid-template-columns: 1fr; }
      .topbar {
        align-items: flex-start;
        flex-direction: column;
      }
      .updated-box { text-align: left; }
      .tool-readout { margin-left: 0; width: 100%; }
    }
  </style>
</head>

<body>
  <div class="page">
    <header class="topbar">
      <div class="brand">
        <h1>NY METRO OPS</h1>
        <div class="tagline">Runway alignment editor</div>
      </div>
      <div class="updated-box">
        UPDATED
        <strong id="updatedAt">—</strong>
      </div>
    </header>

    <main class="layout">
      <aside>
        <section class="card">
          <div class="airport-head">
            <div>
              <div class="airport-code">LGA</div>
              <div class="airport-name">La Guardia</div>
            </div>
            <div class="live-badge">LIVE</div>
          </div>

          <div class="field"><div class="label">Approach</div><div class="value" id="approach">—</div></div>
          <div class="field"><div class="label">Landing</div><div class="value" id="landingRunway">—</div></div>
          <div class="field"><div class="label">Departure</div><div class="value" id="departureRunway">—</div></div>
          <div class="field"><div class="label">Wind</div><div class="value" id="wind">—</div></div>
          <div class="field"><div class="label">ATIS</div><div class="value" id="atisTime">—</div></div>

          <details>
            <summary>View ATIS text</summary>
            <div class="raw-atis" id="rawAtis">—</div>
          </details>
        </section>

        <section class="card">
          <div class="field"><div class="label">Source</div><div class="value">atis.info</div></div>
          <div class="field"><div class="label">Autosave</div><div class="value">localStorage</div></div>
          <div class="field"><div class="label">Status</div><div class="value" id="statusSide">—</div></div>
        </section>
      </aside>

      <section class="diagram-panel">
        <div class="diagram-head">
          <div>
            <div class="diagram-title">LA GUARDIA (LGA)</div>
            <div class="diagram-sub" id="panelSub">Click a runway end, then click the map to place it</div>
          </div>
          <div class="airport-location">New York, New York</div>
        </div>

        <div class="toolbar">
          <div class="group">
            <div class="tool-label">Edit runway end</div>
            <button class="tool-btn active" data-runway="04">04</button>
            <button class="tool-btn" data-runway="22">22</button>
            <button class="tool-btn" data-runway="13">13</button>
            <button class="tool-btn" data-runway="31">31</button>
          </div>

          <div class="group">
            <div class="tool-label">Actions</div>
            <button class="tool-btn secondary" id="resetBtn">Reset defaults</button>
            <button class="tool-btn secondary" id="copyBtn">Copy JSON</button>
            <button class="tool-btn secondary" id="downloadBtn">Download JSON</button>
          </div>

          <div class="tool-readout" id="readout">Selected runway: 04 — click map to place anchor</div>
        </div>

        <div class="diagram-wrap">
          <div class="stage" id="mapStage">
            <img src="/assets/lga_dark_map.png" alt="Dark map reference for LGA">
            <svg class="overlay-svg" id="overlaySvg" viewBox="0 0 100 100" preserveAspectRatio="none"></svg>
            <div class="overlay-hint" id="hint">Select a runway end above, then click anywhere on the map to place its anchor. The point becomes the runway-end reference for both arrival and departure arrows.</div>
          </div>
        </div>

        <div class="legend">
          <div><span class="legend-dot arrival"></span>Arrival / landing arrow</div>
          <div><span class="legend-dot departure"></span>Departure arrow</div>
          <div><span class="legend-dot" style="background:#66a3ff"></span>Selected runway anchor</div>
        </div>

        <div class="statusbar">
          <div class="left">
            <span>Status: <span class="dim" id="status">Waiting for live data...</span></span>
          </div>
          <div class="right">
            <span>Click coords: <span class="dim" id="coordReadout">—</span></span>
          </div>
        </div>
      </section>
    </main>
  </div>

  <script>
    function safe(value, fallback = "—") {
      return value === undefined || value === null || value === "" ? fallback : value;
    }

    const STORAGE_KEY = "lgaRunwayAnchors_v1";

    const defaultAnchors = {
      "04": { x: 31.0, y: 69.5 },
      "22": { x: 52.0, y: 26.8 },
      "13": { x: 40.1, y: 34.0 },
      "31": { x: 73.0, y: 60.9 }
    };

    let selectedRunway = "04";
    let anchors = loadAnchors();

    const activeLayout = {
      arrival: {
        "22": { dx: 10, dy: -10 },
        "04": { dx: -10, dy: 10 },
        "13": { dx: -10, dy: -10 },
        "31": { dx: 10, dy: 10 }
      },
      departure: {
        "22": { dx: -10, dy: 10 },
        "04": { dx: 10, dy: -10 },
        "13": { dx: 10, dy: 10 },
        "31": { dx: -10, dy: -10 }
      }
    };

    function loadAnchors() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return structuredClone(defaultAnchors);
        const parsed = JSON.parse(raw);
        const merged = structuredClone(defaultAnchors);
        for (const key of Object.keys(merged)) {
          if (parsed[key] && typeof parsed[key].x === "number" && typeof parsed[key].y === "number") {
            merged[key] = { x: parsed[key].x, y: parsed[key].y };
          }
        }
        return merged;
      } catch {
        return structuredClone(defaultAnchors);
      }
    }

    function saveAnchors() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(anchors, null, 2));
    }

    function setSelectedRunway(runway) {
      selectedRunway = runway;
      document.querySelectorAll("[data-runway]").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.runway === runway);
      });
      document.getElementById("readout").textContent = `Selected runway: ${runway} — click map to place anchor`;
      document.getElementById("hint").textContent =
        `Selected runway ${runway}. Click the map to place its anchor point. The same anchor will be used for arrival and departure arrows.`;
    }

    function clamp(v) {
      return Math.max(0.5, Math.min(99.5, v));
    }

    function renderOverlay(data) {
      const overlay = document.getElementById("overlaySvg");
      const landing = data?.landing_runway ? String(data.landing_runway).padStart(2, "0") : null;
      const departure = data?.departure_runway ? String(data.departure_runway).padStart(2, "0") : null;

      const parts = [];

      // Defs
      parts.push(`
        <defs>
          <marker id="arrow-red" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 Z" fill="#ff4d4d"></path>
          </marker>
          <marker id="arrow-green" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 Z" fill="#2ecc71"></path>
          </marker>
        </defs>
      `);

      // Draw runway anchors
      for (const runway of ["04", "22", "13", "31"]) {
        const a = anchors[runway];
        const isSelected = runway === selectedRunway;
        const isLanding = runway === landing;
        const isDeparture = runway === departure;

        const r = isSelected ? 1.4 : 0.9;
        const fill = isLanding ? "#ff4d4d" : isDeparture ? "#2ecc71" : "#66a3ff";
        const stroke = isSelected ? "#ffffff" : "rgba(255,255,255,.9)";
        const labelY = clamp(a.y - 1.8);

        parts.push(`
          <circle cx="${a.x}" cy="${a.y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${isSelected ? 0.35 : 0.22}" opacity="0.95"></circle>
          <text x="${a.x + 1.3}" y="${labelY}" fill="#ffffff" font-size="1.9" font-weight="900" stroke="rgba(0,0,0,.55)" stroke-width="0.15" paint-order="stroke">
            ${runway}
          </text>
        `);
      }

      function drawArrow(runway, mode) {
        const a = anchors[runway];
        const v = activeLayout[mode][runway];
        if (!a || !v) return "";

        const x1 = mode === "arrival" ? clamp(a.x + v.dx) : a.x;
        const y1 = mode === "arrival" ? clamp(a.y + v.dy) : a.y;
        const x2 = mode === "departure" ? clamp(a.x + v.dx) : a.x;
        const y2 = mode === "departure" ? clamp(a.y + v.dy) : a.y;

        const stroke = mode === "arrival" ? "#ff4d4d" : "#2ecc71";
        const marker = mode === "arrival" ? "url(#arrow-red)" : "url(#arrow-green)";
        const width = mode === "arrival" ? 1.0 : 0.95;

        return `
          <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${width}" marker-end="${marker}" opacity="0.95"></line>
        `;
      }

      if (landing) parts.push(drawArrow(landing, "arrival"));
      if (departure) parts.push(drawArrow(departure, "departure"));

      overlay.innerHTML = parts.join("");
    }

    function exportJson() {
      return JSON.stringify(anchors, null, 2);
    }

    function download(filename, text) {
      const blob = new Blob([text], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }

    async function copyToClipboard(text) {
      await navigator.clipboard.writeText(text);
    }

    function handleMapClick(event) {
      const stage = document.getElementById("mapStage");
      const rect = stage.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width) * 100;
      const y = ((event.clientY - rect.top) / rect.height) * 100;

      const xx = clamp(x);
      const yy = clamp(y);

      anchors[selectedRunway] = { x: Number(xx.toFixed(1)), y: Number(yy.toFixed(1)) };
      saveAnchors();

      document.getElementById("coordReadout").textContent = `${xx.toFixed(1)}%, ${yy.toFixed(1)}%`;
      document.getElementById("readout").textContent = `Placed runway ${selectedRunway} at x=${xx.toFixed(1)}%, y=${yy.toFixed(1)}%`;
      document.getElementById("hint").textContent =
        `Runway ${selectedRunway} updated. The editor saved the new anchor locally.`;

      renderOverlay(lastData);
    }

    let lastData = null;

    async function refresh() {
      try {
        const response = await fetch("/api/lga", { cache: "no-store" });
        const data = await response.json();
        lastData = data;

        const approach = safe(data.approach_label || data.approach_type);
        const landing = safe(data.landing_runway);
        const departure = safe(data.departure_runway);
        const wind = safe(data.wind);
        const atisTime = safe(data.atis_time);
        const updated = safe(data.updated_at);
        const status = safe(data.status, "Live ATIS loaded");

        document.getElementById("updatedAt").textContent = updated;
        document.getElementById("approach").textContent = approach;
        document.getElementById("landingRunway").textContent = landing;
        document.getElementById("departureRunway").textContent = departure;
        document.getElementById("wind").textContent = wind;
        document.getElementById("atisTime").textContent = atisTime;
        document.getElementById("rawAtis").textContent = safe(data.raw_atis);
        document.getElementById("statusSide").textContent = status;
        document.getElementById("status").textContent = status;
        document.getElementById("panelSub").textContent = `${approach} / land ${landing} / depart ${departure}`;

        renderOverlay(data);
      } catch (error) {
        document.getElementById("status").textContent = `Error: ${error.message}`;
        document.getElementById("statusSide").textContent = "Error";
        console.error(error);
      }
    }

    window.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll("[data-runway]").forEach(btn => {
        btn.addEventListener("click", () => setSelectedRunway(btn.dataset.runway));
      });

      document.getElementById("mapStage").addEventListener("click", handleMapClick);

      document.getElementById("resetBtn").addEventListener("click", () => {
        anchors = structuredClone(defaultAnchors);
        saveAnchors();
        document.getElementById("coordReadout").textContent = "reset to defaults";
        document.getElementById("readout").textContent = `Selected runway: ${selectedRunway} — defaults restored`;
        renderOverlay(lastData);
      });

      document.getElementById("copyBtn").addEventListener("click", async () => {
        try {
          await copyToClipboard(exportJson());
          document.getElementById("readout").textContent = "Anchor JSON copied to clipboard";
        } catch (err) {
          document.getElementById("readout").textContent = "Clipboard copy failed";
          console.error(err);
        }
      });

      document.getElementById("downloadBtn").addEventListener("click", () => {
        download("lga_runway_anchors.json", exportJson());
      });

      setSelectedRunway(selectedRunway);
      refresh();
    });

    setInterval(refresh, 60000);
  </script>
</body>
</html>
"""

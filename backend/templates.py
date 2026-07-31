INDEX_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>NY Metro Ops</title>
  <link href="https://api.mapbox.com/mapbox-gl-js/v3.5.2/mapbox-gl.css" rel="stylesheet" />
  <script src="https://api.mapbox.com/mapbox-gl-js/v3.5.2/mapbox-gl.js"></script>
  <script>
    (function () {
      var theme = 'dark';
      try {
        var stored = localStorage.getItem('nyMetroOpsTheme');
        if (stored === 'light' || stored === 'dark') {
          theme = stored;
        } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
          theme = 'light';
        }
      } catch (err) {
        // localStorage/matchMedia unavailable (e.g. private browsing) - fall back to dark.
      }
      document.documentElement.setAttribute('data-theme', theme);
    })();
  </script>
  <style>
    :root {
      --bg: #07090c;
      --bg-grad-1: #0a0d12;
      --bg-grad-2: #07090c;
      --bg-glow: rgba(102,163,255,.12);
      --panel-grad-1: #12161d;
      --panel-grad-2: #0d1015;
      --updated-grad-1: #141923;
      --updated-grad-2: #0d1117;
      --panel: #11141a;
      --border: #2b3038;
      --text: #e9edf4;
      --text-strong: #ffffff;
      --text-strong-soft: #f2f6ff;
      --text-secondary: #d9deea;
      --muted: #8c96a8;
      --arrival: #ff4d4d;
      --departure: #2ecc71;
      --accent: #66a3ff;
      --soft: rgba(255,255,255,.06);
      --hairline: rgba(255,255,255,.08);
      --hairline-soft: rgba(255,255,255,.06);
      --shadow: 0 18px 45px rgba(0,0,0,.45);
      --live-text: #b8ffd0;
    }
    :root[data-theme="light"] {
      --bg: #eef1f6;
      --bg-grad-1: #f5f7fb;
      --bg-grad-2: #e7ebf2;
      --bg-glow: rgba(102,163,255,.10);
      --panel-grad-1: #ffffff;
      --panel-grad-2: #f3f5f9;
      --updated-grad-1: #ffffff;
      --updated-grad-2: #eef1f6;
      --panel: #ffffff;
      --border: #d7dce4;
      --text: #1b2330;
      --text-strong: #0b0f16;
      --text-strong-soft: #10161f;
      --text-secondary: #333d4d;
      --muted: #5c6576;
      --arrival: #d92c2c;
      --departure: #1f9e56;
      --accent: #2f6fe0;
      --soft: rgba(10,15,30,.045);
      --hairline: rgba(10,15,30,.10);
      --hairline-soft: rgba(10,15,30,.07);
      --shadow: 0 12px 30px rgba(20,30,50,.12);
      --live-text: #0e7a3e;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background:
        radial-gradient(circle at top, var(--bg-glow), transparent 38%),
        linear-gradient(180deg, var(--bg-grad-1), var(--bg-grad-2));
      color: var(--text);
      font-family: Inter, Arial, Helvetica, sans-serif;
      transition: background .2s ease, color .2s ease;
    }
    .page {
      max-width: 1600px;
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
      color: var(--text-strong);
    }
    .tagline {
      color: var(--muted);
      text-transform: uppercase;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: .22em;
    }
    .topbar-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .theme-toggle {
      cursor: pointer;
      border: 1px solid var(--border);
      background: linear-gradient(180deg, var(--updated-grad-1), var(--updated-grad-2));
      color: var(--text-secondary);
      padding: 10px 16px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 900;
      letter-spacing: .12em;
      text-transform: uppercase;
      box-shadow: var(--shadow);
      transition: background .2s ease, color .2s ease, border-color .2s ease;
    }
    .theme-toggle:hover {
      color: var(--text-strong);
      border-color: var(--accent);
    }
    .updated-box {
      border: 1px solid var(--border);
      background: linear-gradient(180deg, var(--updated-grad-1), var(--updated-grad-2));
      box-shadow: var(--shadow);
      padding: 10px 14px;
      font-size: 12px;
      text-align: right;
      min-width: 250px;
      color: var(--text-secondary);
    }
    .updated-box strong {
      display: block;
      font-size: 15px;
      margin-top: 3px;
      color: var(--text-strong);
    }
    .layout {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
      align-items: start;
    }

    .top-cards {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr)) minmax(250px, 1.15fr);
      gap: 12px;
    }
    .card,
    .map-panel {
      background: linear-gradient(180deg, var(--panel-grad-1), var(--panel-grad-2));
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      border-radius: 18px;
      overflow: hidden;
      transition: background .2s ease, border-color .2s ease;
    }
    .card {
      padding: 13px 14px;
      margin: 0;
    }

    .compact-card {
      min-height: 168px;
    }
    .airport-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      border-bottom: 1px solid var(--hairline);
      padding-bottom: 8px;
      margin-bottom: 4px;
    }
    .airport-code {
      font-size: 32px;
      font-weight: 900;
      line-height: 1;
      color: var(--text-strong);
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
      color: var(--live-text);
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
      border-bottom: 1px solid var(--hairline);
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
      color: var(--text-strong-soft);
      word-break: break-word;
    }

    .airport-strip {
      padding-bottom: 10px;
    }

    .compact-metrics {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px 12px;
      padding-top: 4px;
    }

    .compact-metric {
      min-width: 0;
      border-bottom: 1px solid var(--hairline-soft);
      padding: 6px 0 7px;
    }

    .compact-metric.wide {
      grid-column: 1 / -1;
    }

    .strip-label {
      color: var(--muted);
      text-transform: uppercase;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: .08em;
      margin-bottom: 4px;
    }

    .strip-value {
      font-weight: 800;
      color: var(--text-strong-soft);
      font-size: 14px;
      line-height: 1.2;
      overflow-wrap: anywhere;
    }

    .strip-value.runway {
      font-size: 26px;
      line-height: 1;
      letter-spacing: .03em;
    }

    .strip-footer {
      display: flex;
      justify-content: flex-end;
      padding-top: 8px;
    }

    .mini-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 999px;
      padding: 4px 9px;
      font-size: 10px;
      font-weight: 900;
      letter-spacing: .08em;
      color: var(--text-secondary);
      border: 1px solid var(--hairline);
      background: var(--soft);
    }

    .weather-card {
      display: grid;
      grid-template-rows: auto 1fr auto;
    }

    .weather-main {
      display: grid;
      grid-template-columns: 92px 1fr;
      gap: 14px;
      align-items: center;
      padding: 8px 0;
    }

    .wind-compass {
      position: relative;
      width: 84px;
      height: 84px;
      border-radius: 50%;
      border: 1px solid var(--hairline);
      background:
        radial-gradient(circle, var(--bg-glow), transparent 56%),
        var(--soft);
      display: grid;
      place-items: center;
    }

    .wind-compass::before,
    .wind-compass::after {
      content: "";
      position: absolute;
      background: var(--hairline);
    }

    .wind-compass::before {
      width: 1px;
      height: 70%;
    }

    .wind-compass::after {
      width: 70%;
      height: 1px;
    }

    .wind-arrow {
      position: relative;
      width: 54px;
      height: 54px;
      transform: rotate(0deg);
      transition: transform .5s ease;
      z-index: 2;
    }

    .wind-arrow::before {
      content: "";
      position: absolute;
      left: 25px;
      top: 9px;
      width: 4px;
      height: 36px;
      border-radius: 999px;
      background: var(--accent);
      box-shadow: 0 0 12px rgba(102,163,255,.35);
    }

    .wind-arrow::after {
      content: "";
      position: absolute;
      left: 17px;
      top: 5px;
      width: 16px;
      height: 16px;
      border-left: 4px solid var(--accent);
      border-top: 4px solid var(--accent);
      transform: rotate(45deg);
    }

    .mini-wind-arrow {
      position: relative;
      display: inline-block;
      width: 16px;
      height: 16px;
      margin-right: 6px;
      vertical-align: -3px;
      visibility: hidden;
      transition: transform .4s ease;
    }

    .mini-wind-arrow::before {
      content: "";
      position: absolute;
      left: 7px;
      top: 1px;
      width: 2px;
      height: 12px;
      border-radius: 999px;
      background: var(--accent);
    }

    .mini-wind-arrow::after {
      content: "";
      position: absolute;
      left: 4px;
      top: 0;
      width: 6px;
      height: 6px;
      border-left: 2px solid var(--accent);
      border-top: 2px solid var(--accent);
      transform: rotate(45deg);
    }

    .weather-reading {
      display: flex;
      align-items: baseline;
      gap: 8px;
      flex-wrap: wrap;
    }

    .weather-degrees {
      font-size: 34px;
      line-height: 1;
      font-weight: 900;
      color: var(--text-strong);
    }

    .weather-speed {
      font-size: 15px;
      font-weight: 900;
      color: var(--text-secondary);
    }

    .weather-sub {
      color: var(--muted);
      font-size: 11px;
      line-height: 1.35;
      margin-top: 6px;
    }

    .airport-winds {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }

    .airport-wind {
      border-top: 1px solid var(--hairline-soft);
      padding-top: 7px;
      font-size: 11px;
      color: var(--muted);
    }

    .airport-wind strong {
      display: block;
      margin-top: 2px;
      color: var(--text-strong);
      font-size: 12px;
    }

    .note {
      margin-top: 10px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
    }
    .map-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 14px;
      padding: 14px 16px 12px;
      border-bottom: 1px solid var(--hairline);
    }
    .map-title {
      font-size: 22px;
      font-weight: 900;
      letter-spacing: .02em;
      color: var(--text-strong);
    }
    .map-sub {
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 800;
    }
    .map-area {
      position: relative;
      height: 68vh;
      min-height: 580px;
    }
    #map {
      position: absolute;
      inset: 0;
    }
    .legend {
      display: flex;
      gap: 18px;
      align-items: center;
      border-top: 1px solid var(--hairline);
      padding: 10px 14px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 900;
      color: var(--text-secondary);
      flex-wrap: wrap;
    }
    .legend-dot {
      display: inline-block;
      width: 12px;
      height: 12px;
      border-radius: 999px;
      margin-right: 6px;
      vertical-align: -1px;
      box-shadow: 0 0 0 2px var(--hairline);
    }
    .legend-dot.arrival { background: var(--arrival); }
    .legend-dot.departure { background: var(--departure); }
    .legend-dot.airport { background: var(--accent); }
    .statusbar {
      border-top: 1px solid var(--hairline);
      padding: 10px 14px;
      color: var(--muted);
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: .08em;
      font-weight: 800;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .dim { color: var(--text-secondary); font-weight: 800; }
    .airport-marker {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: #66a3ff;
      border: 2px solid #fff;
      box-shadow: 0 0 0 2px rgba(0,0,0,.25), 0 2px 8px rgba(0,0,0,.35);
    }
    .marker-popup h3 {
      margin: 0 0 6px;
      font-size: 14px;
    }
    .marker-popup .row {
      margin: 2px 0;
      font-size: 12px;
      color: #ddd;
      white-space: nowrap;
    }
    @media (max-width: 1200px) {
      .top-cards {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 760px) {
      .top-cards {
        grid-template-columns: 1fr;
      }
      .topbar {
        align-items: flex-start;
        flex-direction: column;
      }
      .updated-box { text-align: left; }
      .map-area { height: 62vh; min-height: 500px; }
    }
  </style>
</head>
<body>
  <div class="page">
    <header class="topbar">
      <div class="brand">
        <h1>NY METRO OPS</h1>
        <div class="tagline">NYC airports live runways</div>
      </div>
      <div class="topbar-right">
        <button class="theme-toggle" id="themeToggle" type="button" aria-label="Toggle color theme">
          <span id="themeToggleLabel">DARK</span>
        </button>
        <div class="updated-box">
          UPDATED
          <strong id="updatedAt">—</strong>
        </div>
      </div>
    </header>

    <main class="layout">
      <section class="top-cards">
        <section class="card airport-strip compact-card">
          <div class="airport-head">
            <div>
              <div class="airport-code">LGA</div>
              <div class="airport-name">La Guardia · ACTIVE</div>
            </div>
            <div class="live-badge">LIVE</div>
          </div>
          <div class="compact-metrics">
            <div class="compact-metric">
              <div class="strip-label">Landing</div>
              <div class="strip-value runway" id="lgaLanding">—</div>
            </div>
            <div class="compact-metric">
              <div class="strip-label">Departure</div>
              <div class="strip-value runway" id="lgaDeparture">—</div>
            </div>
            <div class="compact-metric wide">
              <div class="strip-label">Wind</div>
              <div class="strip-value"><span class="mini-wind-arrow" id="lgaWindArrow"></span><span id="lgaWind">—</span></div>
            </div>
            <div class="compact-metric wide">
              <div class="strip-label">Approach</div>
              <div class="strip-value" id="lgaApproach">—</div>
            </div>
          </div>
          <div class="strip-footer"><span class="mini-badge" id="lgaAtis">ATIS —</span></div>
        </section>

        <section class="card airport-strip compact-card">
          <div class="airport-head">
            <div>
              <div class="airport-code">JFK</div>
              <div class="airport-name">John F. Kennedy · ACTIVE</div>
            </div>
            <div class="live-badge">LIVE</div>
          </div>
          <div class="compact-metrics">
            <div class="compact-metric">
              <div class="strip-label">Landing</div>
              <div class="strip-value runway" id="jfkLanding">—</div>
            </div>
            <div class="compact-metric">
              <div class="strip-label">Departure</div>
              <div class="strip-value runway" id="jfkDeparture">—</div>
            </div>
            <div class="compact-metric wide">
              <div class="strip-label">Wind</div>
              <div class="strip-value"><span class="mini-wind-arrow" id="jfkWindArrow"></span><span id="jfkWind">—</span></div>
            </div>
            <div class="compact-metric wide">
              <div class="strip-label">Approach</div>
              <div class="strip-value" id="jfkApproach">—</div>
            </div>
          </div>
          <div class="strip-footer"><span class="mini-badge" id="jfkAtis">ATIS —</span></div>
        </section>

        <section class="card airport-strip compact-card">
          <div class="airport-head">
            <div>
              <div class="airport-code">EWR</div>
              <div class="airport-name">Newark Liberty · ACTIVE</div>
            </div>
            <div class="live-badge">LIVE</div>
          </div>
          <div class="compact-metrics">
            <div class="compact-metric">
              <div class="strip-label">Landing</div>
              <div class="strip-value runway" id="ewrLanding">—</div>
            </div>
            <div class="compact-metric">
              <div class="strip-label">Departure</div>
              <div class="strip-value runway" id="ewrDeparture">—</div>
            </div>
            <div class="compact-metric wide">
              <div class="strip-label">Wind</div>
              <div class="strip-value"><span class="mini-wind-arrow" id="ewrWindArrow"></span><span id="ewrWind">—</span></div>
            </div>
            <div class="compact-metric wide">
              <div class="strip-label">Approach</div>
              <div class="strip-value" id="ewrApproach">—</div>
            </div>
          </div>
          <div class="strip-footer"><span class="mini-badge" id="ewrAtis">ATIS —</span></div>
        </section>

        <section class="card weather-card compact-card">
          <div class="airport-head">
            <div>
              <div class="airport-code" style="font-size:24px;">METRO WIND</div>
              <div class="airport-name">Mean of current airport winds</div>
            </div>
            <div class="live-badge">LIVE</div>
          </div>

          <div class="weather-main">
            <div class="wind-compass">
              <div class="wind-arrow" id="metroWindArrow"></div>
            </div>
            <div>
              <div class="weather-reading">
                <span class="weather-degrees" id="metroWindDirection">—</span>
                <span class="weather-speed" id="metroWindSpeed">—</span>
              </div>
              <div class="weather-sub">Arrow points from the reported wind direction toward the airport.</div>
            </div>
          </div>

          <div class="airport-winds">
            <div class="airport-wind">LGA<strong id="metroLgaWind">—</strong></div>
            <div class="airport-wind">JFK<strong id="metroJfkWind">—</strong></div>
            <div class="airport-wind">EWR<strong id="metroEwrWind">—</strong></div>
          </div>
        </section>
      </section>

      <section class="map-panel">
        <div class="map-head">
          <div>
            <div class="map-title">NYC AIRPORT VIEW</div>
            <div class="map-sub">Current open runways for LGA, JFK, and EWR</div>
          </div>
          <div class="map-sub" id="mapStyleLabel">Dark style · Mapbox</div>
        </div>

        <div class="map-area">
          <div id="map"></div>
        </div>

        <div class="legend">
          <div><span class="legend-dot airport"></span>Airport</div>
          <div><span class="legend-dot arrival"></span>Arrival / landing runway</div>
          <div><span class="legend-dot departure"></span>Departure runway</div>
        </div>

        <div class="statusbar">
          <div>Source: <span class="dim" id="status">Waiting for live data...</span></div>
          <div>Mapbox: <span class="dim" id="mapboxStatus">loading</span></div>
        </div>
      </section>
    </main>
  </div>

  <script>
    const MAPBOX_TOKEN = "__MAPBOX_TOKEN__";
    mapboxgl.accessToken = MAPBOX_TOKEN;
    const AIRPORTS = {
      LGA: { code: "LGA", name: "La Guardia", lat: 40.7769, lon: -73.8740, color: "#66a3ff" },
      JFK: { code: "JFK", name: "John F. Kennedy", lat: 40.6413, lon: -73.7781, color: "#66a3ff" },
      EWR: { code: "EWR", name: "Newark Liberty", lat: 40.6895, lon: -74.1745, color: "#66a3ff" }
    };

    function safe(value, fallback = "—") {
      return value === undefined || value === null || value === "" ? fallback : value;
    }

    function formatUpdatedAt(value) {
      if (!value) return "—";
      const parsed = new Date(value);
      if (Number.isNaN(parsed.getTime())) return value;
      const datePart = `${String(parsed.getMonth() + 1).padStart(2, "0")}/${String(parsed.getDate()).padStart(2, "0")}/${parsed.getFullYear()}`;
      let hours = parsed.getHours();
      const ampm = hours >= 12 ? "PM" : "AM";
      hours = hours % 12 || 12;
      const minutes = String(parsed.getMinutes()).padStart(2, "0");
      return `${datePart} ${hours}:${minutes}${ampm}`;
    }

    function airportCardIds(code) {
      return {
        approach: `${code.toLowerCase()}Approach`,
        landing: `${code.toLowerCase()}Landing`,
        departure: `${code.toLowerCase()}Departure`,
        wind: `${code.toLowerCase()}Wind`,
        windArrow: `${code.toLowerCase()}WindArrow`,
        atis: `${code.toLowerCase()}Atis`
      };
    }

    function airportPopupHTML(a, status) {
      return `
        <div class="marker-popup">
          <h3>${a.code} · ${a.name}</h3>
          <div class="row">Landing: <b>${safe(status.landing_runway)}</b></div>
          <div class="row">Departure: <b>${safe(status.departure_runway)}</b></div>
          <div class="row">Wind: <b>${safe(status.wind)}</b></div>
          <div class="row">Approach: <b>${safe(status.approach_type || status.approach_label)}</b></div>
        </div>
      `;
    }

    function setCard(code, status) {
      const ids = airportCardIds(code);
      document.getElementById(ids.approach).textContent = safe(status.approach_type || status.approach_label);
      document.getElementById(ids.landing).textContent = safe(status.landing_runway);
      document.getElementById(ids.departure).textContent = safe(status.departure_runway);
      document.getElementById(ids.wind).textContent = safe(status.wind);
      document.getElementById(ids.atis).textContent = `ATIS ${safe(status.atis_time)}`;

      const arrowEl = document.getElementById(ids.windArrow);
      if (arrowEl) {
        const wind = parseWind(status.wind);
        if (wind) {
          arrowEl.style.visibility = 'visible';
          // Aviation wind direction is where the wind comes from; the arrow points downwind.
          arrowEl.style.transform = `rotate(${(wind.direction + 180) % 360}deg)`;
        } else {
          arrowEl.style.visibility = 'hidden';
        }
      }
    }


    const ARRIVAL_EXTENSION_KM = 3.0;
    const DEPARTURE_EXTENSION_KM = 2.0;
    const RUNWAY_ENTRY_KM = 0.8;

    // Threshold coordinates from the OurAirports runway dataset.
    // Each runway points from its threshold toward the reciprocal threshold.
    const RUNWAY_GEOMETRY = {
      LGA: {
        "04": { threshold: [-73.88410187, 40.76919937], opposite: [-73.87069702, 40.78540039] },
        "22": { threshold: [-73.87069702, 40.78540039], opposite: [-73.88410187, 40.76919937] },
        "13": { threshold: [-73.87850189, 40.78229904], opposite: [-73.85710144, 40.77209854] },
        "31": { threshold: [-73.85710144, 40.77209854], opposite: [-73.87850189, 40.78229904] }
      },
      JFK: {
        "04L": { threshold: [-73.785599, 40.622002], opposite: [-73.764702, 40.6488] },
        "22R": { threshold: [-73.764702, 40.6488], opposite: [-73.785599, 40.622002] },
        "04R": { threshold: [-73.77030181884766, 40.62540054321289], opposite: [-73.75489807128906, 40.645198822021484] },
        "22L": { threshold: [-73.75489807128906, 40.645198822021484], opposite: [-73.77030181884766, 40.62540054321289] },
        "13L": { threshold: [-73.790199, 40.657799], opposite: [-73.7593, 40.6437] },
        "31R": { threshold: [-73.7593, 40.6437], opposite: [-73.790199, 40.657799] },
        "13R": { threshold: [-73.816704, 40.648399], opposite: [-73.771599, 40.627899] },
        "31L": { threshold: [-73.771599, 40.627899], opposite: [-73.816704, 40.648399] }
      },
      EWR: {
        "11": { threshold: [-74.180748, 40.702815], opposite: [-74.156502, 40.701203] },
        "29": { threshold: [-74.156502, 40.701203], opposite: [-74.180748, 40.702815] },
        "04L": { threshold: [-74.179456, 40.675392], opposite: [-74.16217, 40.70257] },
        "22R": { threshold: [-74.16217, 40.70257], opposite: [-74.179456, 40.675392] },
        "04R": { threshold: [-74.174253, 40.677588], opposite: [-74.158539, 40.702299] },
        "22L": { threshold: [-74.158539, 40.702299], opposite: [-74.174253, 40.677588] }
      }
    };

    function normalizeRunway(value) {
      const match = String(value || '').toUpperCase().match(/\d{1,2}[LRC]?/);
      if (!match) return null;
      const numberMatch = match[0].match(/^\d{1,2}/);
      const suffixMatch = match[0].match(/[LRC]$/);
      const number = String(parseInt(numberMatch[0], 10)).padStart(2, '0');
      return `${number}${suffixMatch ? suffixMatch[0] : ''}`;
    }

    function splitRunways(value) {
      const matches = String(value || '').toUpperCase().match(/\d{1,2}[LRC]?/g) || [];
      return [...new Set(matches.map(normalizeRunway).filter(Boolean))];
    }

    function bearingBetween(from, to) {
      const lat1 = from[1] * Math.PI / 180;
      const lat2 = to[1] * Math.PI / 180;
      const deltaLon = (to[0] - from[0]) * Math.PI / 180;
      const y = Math.sin(deltaLon) * Math.cos(lat2);
      const x = Math.cos(lat1) * Math.sin(lat2) -
        Math.sin(lat1) * Math.cos(lat2) * Math.cos(deltaLon);
      return (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
    }

    function destinationPoint(lat, lon, bearingDeg, distanceKm) {
      const R = 6371.0;
      const brng = bearingDeg * Math.PI / 180;
      const d = distanceKm / R;
      const lat1 = lat * Math.PI / 180;
      const lon1 = lon * Math.PI / 180;

      const lat2 = Math.asin(
        Math.sin(lat1) * Math.cos(d) +
        Math.cos(lat1) * Math.sin(d) * Math.cos(brng)
      );
      const lon2 = lon1 + Math.atan2(
        Math.sin(brng) * Math.sin(d) * Math.cos(lat1),
        Math.cos(d) - Math.sin(lat1) * Math.sin(lat2)
      );

      return [((lon2 * 180 / Math.PI) + 540) % 360 - 180, lat2 * 180 / Math.PI];
    }

    function runwayGeometry(airportCode, runway) {
      return RUNWAY_GEOMETRY[airportCode]?.[normalizeRunway(runway)] || null;
    }

    function addVector(lineFeatures, headFeatures, tipFeatures, airportCode, runway, kind) {
      const normalized = normalizeRunway(runway);
      const geometry = runwayGeometry(airportCode, normalized);
      if (!geometry) return;

      const heading = bearingBetween(geometry.threshold, geometry.opposite);
      let coordinates;
      let head;
      let tip;

      if (kind === 'arrival') {
        const source = destinationPoint(
          geometry.threshold[1],
          geometry.threshold[0],
          (heading + 180) % 360,
          ARRIVAL_EXTENSION_KM
        );
        const target = destinationPoint(
          geometry.threshold[1],
          geometry.threshold[0],
          heading,
          RUNWAY_ENTRY_KM
        );
        // Arrival vectors run from outside the airport toward the runway.
        coordinates = [source, geometry.threshold, target];
        head = source;
        tip = target;
      } else {
        const target = destinationPoint(
          geometry.opposite[1],
          geometry.opposite[0],
          heading,
          DEPARTURE_EXTENSION_KM
        );
        // Departure vectors run from the runway out of the airport.
        coordinates = [geometry.threshold, geometry.opposite, target];
        head = target;
        tip = target;
      }

      lineFeatures.push({
        type: 'Feature',
        geometry: { type: 'LineString', coordinates },
        properties: {
          airport: airportCode,
          runway: normalized,
          kind,
          bearing: heading
        }
      });

      headFeatures.push({
        type: 'Feature',
        geometry: { type: 'Point', coordinates: head },
        properties: {
          airport: airportCode,
          runway: normalized,
          kind,
          bearing: heading
        }
      });

      const arrowLengthKm = 0.9;
      const arrowHalfWidthKm = 0.38;
      const baseCenter = destinationPoint(
        tip[1],
        tip[0],
        (heading + 180) % 360,
        arrowLengthKm
      );
      const leftBase = destinationPoint(
        baseCenter[1],
        baseCenter[0],
        (heading + 270) % 360,
        arrowHalfWidthKm
      );
      const rightBase = destinationPoint(
        baseCenter[1],
        baseCenter[0],
        (heading + 90) % 360,
        arrowHalfWidthKm
      );

      tipFeatures.push({
        type: 'Feature',
        geometry: {
          type: 'Polygon',
          coordinates: [[tip, leftBase, rightBase, tip]]
        },
        properties: {
          airport: airportCode,
          runway: normalized,
          kind
        }
      });
    }

    function buildRunwayVectors(airports) {
      const lineFeatures = [];
      const headFeatures = [];
      const tipFeatures = [];

      airports.forEach((airportStatus) => {
        splitRunways(airportStatus.landing_runway).forEach((runway) => {
          addVector(lineFeatures, headFeatures, tipFeatures, airportStatus.code, runway, 'arrival');
        });

        splitRunways(airportStatus.departure_runway).forEach((runway) => {
          addVector(lineFeatures, headFeatures, tipFeatures, airportStatus.code, runway, 'departure');
        });
      });

      return {
        lines: { type: 'FeatureCollection', features: lineFeatures },
        heads: { type: 'FeatureCollection', features: headFeatures },
        tips: { type: 'FeatureCollection', features: tipFeatures }
      };
    }

    function ensureRunwayLayers(map) {
      if (map.getSource("runway-lines")) {
        return;
      }

      map.addSource("runway-lines", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      });

      map.addSource("runway-heads", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      });

      map.addSource("runway-tips", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      });

      map.addLayer({
        id: "runway-arrival-lines",
        type: "line",
        source: "runway-lines",
        filter: ["==", ["get", "kind"], "arrival"],
        paint: {
          "line-color": "#ff4d4d",
          "line-width": 4.0,
          "line-opacity": 0.96
        }
      });

      map.addLayer({
        id: "runway-departure-lines",
        type: "line",
        source: "runway-lines",
        filter: ["==", ["get", "kind"], "departure"],
        paint: {
          "line-color": "#2ecc71",
          "line-width": 4.0,
          "line-opacity": 0.96
        }
      });

      map.addLayer({
        id: "runway-arrival-tips",
        type: "fill",
        source: "runway-tips",
        filter: ["==", ["get", "kind"], "arrival"],
        paint: {
          "fill-color": "#ff4d4d",
          "fill-opacity": 1.0,
          "fill-outline-color": "#ff7a7a"
        }
      });

      map.addLayer({
        id: "runway-departure-tips",
        type: "fill",
        source: "runway-tips",
        filter: ["==", ["get", "kind"], "departure"],
        paint: {
          "fill-color": "#2ecc71",
          "fill-opacity": 1.0,
          "fill-outline-color": "#7be3a5"
        }
      });

      map.addLayer({
        id: "runway-arrival-labels",
        type: "symbol",
        source: "runway-heads",
        filter: ["==", ["get", "kind"], "arrival"],
        layout: {
          "text-field": ["get", "runway"],
          "text-size": 14,
          "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
          "text-offset": [0, -1.1],
          "text-anchor": "bottom",
          "text-allow-overlap": true,
          "text-ignore-placement": true
        },
        paint: {
          "text-color": "#ffffff",
          "text-halo-color": "#9d1616",
          "text-halo-width": 5,
          "text-halo-blur": 0.5
        }
      });

      map.addLayer({
        id: "runway-departure-labels",
        type: "symbol",
        source: "runway-heads",
        filter: ["==", ["get", "kind"], "departure"],
        layout: {
          "text-field": ["get", "runway"],
          "text-size": 14,
          "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
          "text-offset": [0, 1.1],
          "text-anchor": "top",
          "text-allow-overlap": true,
          "text-ignore-placement": true
        },
        paint: {
          "text-color": "#ffffff",
          "text-halo-color": "#126f3b",
          "text-halo-width": 5,
          "text-halo-blur": 0.5
        }
      });
    }

    function updateRunwayLayers(map, airports) {
      if (
        !map ||
        !map.getSource("runway-lines") ||
        !map.getSource("runway-heads") ||
        !map.getSource("runway-tips")
      ) {
        return;
      }

      const vectors = buildRunwayVectors(airports);

      map.getSource("runway-lines").setData(vectors.lines);
      map.getSource("runway-heads").setData(vectors.heads);
      map.getSource("runway-tips").setData(vectors.tips);
    }

    function parseWind(value) {
      const match = String(value || "").toUpperCase().match(/(\d{3})\s*(\d{2,3})KT(?:\s*G(\d{2,3})KT)?/);
      if (!match) return null;
      return {
        direction: parseInt(match[1], 10),
        speed: parseInt(match[2], 10),
        gust: match[3] ? parseInt(match[3], 10) : null
      };
    }

    function circularMean(degrees) {
      if (!degrees.length) return null;
      const x = degrees.reduce((sum, d) => sum + Math.cos(d * Math.PI / 180), 0);
      const y = degrees.reduce((sum, d) => sum + Math.sin(d * Math.PI / 180), 0);
      return (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
    }

    function updateMetroWeather(airports) {
      const byCode = Object.fromEntries(airports.map(a => [a.code, a]));
      const parsed = airports.map(a => parseWind(a.wind)).filter(Boolean);
      const meanDirection = circularMean(parsed.map(w => w.direction));
      const meanSpeed = parsed.length
        ? Math.round(parsed.reduce((sum, w) => sum + w.speed, 0) / parsed.length)
        : null;
      const maxGust = parsed
        .map(w => w.gust)
        .filter(v => Number.isFinite(v))
        .reduce((max, v) => Math.max(max, v), 0);

      document.getElementById("metroLgaWind").textContent = safe(byCode.LGA?.wind);
      document.getElementById("metroJfkWind").textContent = safe(byCode.JFK?.wind);
      document.getElementById("metroEwrWind").textContent = safe(byCode.EWR?.wind);

      if (meanDirection === null || meanSpeed === null) {
        document.getElementById("metroWindDirection").textContent = "—";
        document.getElementById("metroWindSpeed").textContent = "—";
        return;
      }

      const roundedDirection = Math.round(meanDirection / 10) * 10 % 360;
      document.getElementById("metroWindDirection").textContent =
        `${String(roundedDirection).padStart(3, "0")}°`;
      document.getElementById("metroWindSpeed").textContent =
        `${String(meanSpeed).padStart(2, "0")} KT${maxGust ? ` · G${maxGust}` : ""}`;

      // Aviation wind direction is where the wind comes from. The arrow points inward/downwind.
      document.getElementById("metroWindArrow").style.transform =
        `rotate(${roundedDirection + 180}deg)`;
    }

    function makeMarkerEl(color) {
      const el = document.createElement('div');
      el.className = 'airport-marker';
      el.style.background = color;
      return el;
    }

    async function loadData() {
      const res = await fetch('/api/nyc', { cache: 'no-store' });
      if (!res.ok) throw new Error(`API ${res.status}`);
      return await res.json();
    }

    const MAP_STYLES = {
      dark: 'mapbox://styles/mapbox/dark-v11',
      light: 'mapbox://styles/mapbox/light-v11',
    };

    function currentTheme() {
      return document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
    }

    function initMap() {
      document.getElementById('mapboxStatus').textContent = 'loaded';

      try {
        const map = new mapboxgl.Map({
          container: 'map',
          style: MAP_STYLES[currentTheme()],
          center: [-73.92, 40.73],
          zoom: 9.85,
          pitch: 0,
          bearing: 0,
          attributionControl: true
        });

        map.addControl(new mapboxgl.NavigationControl({ showCompass: true }), 'top-right');

        map.on('load', () => {
          ensureRunwayLayers(map);
          updateRunwayLayers(map, latestAirports);
        });

        return map;
      } catch (err) {
        console.error(err);
        document.getElementById('status').textContent = `Map error: ${err.message}`;
        document.getElementById('mapboxStatus').textContent = 'error';
        return null;
      }
    }

    let markers = [];
    let latestAirports = [];

    function clearMarkers() {
      markers.forEach(m => m.remove());
      markers = [];
    }

    async function refreshCardsAndMarkers(map) {
      try {
        const data = await loadData();
        const airports = data.airports || [];
        latestAirports = airports;

        document.getElementById('status').textContent = safe(data.status, 'Live ATIS loaded');
        document.getElementById('updatedAt').textContent = formatUpdatedAt(airports.map(a => a.updated_at).find(Boolean));

        updateMetroWeather(airports);

        clearMarkers();
        airports.forEach(a => {
          setCard(a.code, a);
          if (map) {
            const marker = new mapboxgl.Marker({ element: makeMarkerEl(AIRPORTS[a.code]?.color || '#66a3ff') })
              .setLngLat([a.lon, a.lat])
              .setPopup(new mapboxgl.Popup({ offset: 16, closeButton: false }).setHTML(airportPopupHTML(AIRPORTS[a.code], a)))
              .addTo(map);
            marker.getElement().title = `${a.code} · ${a.name}`;
            markers.push(marker);
          }
        });

        if (map) {
          ensureRunwayLayers(map);
          updateRunwayLayers(map, airports);
        }
      } catch (err) {
        document.getElementById('status').textContent = `Error: ${err.message}`;
        console.error(err);
      }
    }

    function syncThemeUI(theme) {
      const label = document.getElementById('themeToggleLabel');
      if (label) label.textContent = theme === 'light' ? 'LIGHT' : 'DARK';
      const mapStyleLabel = document.getElementById('mapStyleLabel');
      if (mapStyleLabel) mapStyleLabel.textContent = theme === 'light' ? 'Light style · Mapbox' : 'Dark style · Mapbox';
    }

    function applyTheme(theme, map) {
      document.documentElement.setAttribute('data-theme', theme);
      try {
        localStorage.setItem('nyMetroOpsTheme', theme);
      } catch (err) {
        // ignore (e.g. private browsing storage restrictions)
      }
      syncThemeUI(theme);

      if (map) {
        // Switching styles wipes any custom sources/layers, so the runway
        // vectors have to be re-added once the new style finishes loading.
        map.once('style.load', () => {
          ensureRunwayLayers(map);
          updateRunwayLayers(map, latestAirports);
        });
        map.setStyle(MAP_STYLES[theme]);
      }
    }

    window.addEventListener('DOMContentLoaded', async () => {
      const map = initMap();
      syncThemeUI(currentTheme());

      const toggleButton = document.getElementById('themeToggle');
      if (toggleButton) {
        toggleButton.addEventListener('click', () => {
          applyTheme(currentTheme() === 'light' ? 'dark' : 'light', map);
        });
      }

      await refreshCardsAndMarkers(map);
      setInterval(() => refreshCardsAndMarkers(map), 60000);
    });
  </script>
</body>
</html>
"""


def render_index(mapbox_token: str = '') -> str:
    return INDEX_TEMPLATE.replace('__MAPBOX_TOKEN__', mapbox_token)

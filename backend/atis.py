from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

import requests

AIRPORT = "KLGA"
ATIS_API_URL = f"https://atis.info/api/{AIRPORT}"
REQUEST_TIMEOUT = 20

APPROACH_RE = re.compile(
    r"\b(?P<approach>(?:ILS(?: OR LOC)?|RNAV(?: [XYZ])?|VISUAL|LOC|LDA|RNP(?: AR)?)(?: [A-Z0-9/.-]+)*)"
    r"\s+R?Y?\s*(?P<landing>\d{1,2}[LRC]?)\s+APCH IN USE",
    re.IGNORECASE,
)
LAND_RE = re.compile(r"\b(?:LAND|LND)\s+R?Y?\s*(?P<landing>\d{1,2}[LRC]?)", re.IGNORECASE)
DEPART_RE = re.compile(r"\bDEPART(?:ING)?\s+R?Y?\s*(?P<depart>\d{1,2}[LRC]?)", re.IGNORECASE)
WIND_RE = re.compile(r"\b(?P<dir>\d{3}|VRB)(?P<speed>\d{2})(?:G(?P<gust>\d{2}))?KT\b", re.IGNORECASE)
TIME_RE = re.compile(r"\b(?P<time>\d{4})Z\b")


def _clean_approach(raw: str) -> str:
    cleaned = raw.upper().strip()
    cleaned = cleaned.replace("R?Y?", "RWY")
    cleaned = cleaned.replace(" RY ", " RWY ")
    cleaned = cleaned.replace(" ILS RWY", " ILS RWY")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def normalize_runway(value: str) -> str:
    value = value.upper().strip()
    # Convert runway 4 to 04, but keep 13, 22, 31, 22L, etc.
    match = re.match(r"^(\d{1,2})([LRC]?)$", value)
    if not match:
        return value
    number, suffix = match.groups()
    if len(number) == 1:
        number = "0" + number
    return number + suffix


def normalize_approach(value: str) -> str:
    value = value.upper().strip()
    # ATIS may say "ILS RY 22" or "ILS RWY 22"; the parser should keep only "ILS".
    value = re.sub(r"\s+R(?:W)?Y$", "", value).strip()
    value = value.replace(" OR LOC", "")
    return value


def parse_atis_text(text: str) -> dict[str, str]:
    result: dict[str, str] = {"raw_atis": text.strip()}

    m = APPROACH_RE.search(text)
    if m:
        approach = normalize_approach(m.group("approach"))
        landing = normalize_runway(m.group("landing"))
        result["approach_type"] = approach
        result["landing_runway"] = landing
        result["approach_label"] = f"{approach} RWY {landing}"

    m = LAND_RE.search(text)
    if m and "landing_runway" not in result:
        result["landing_runway"] = normalize_runway(m.group("landing"))

    m = DEPART_RE.search(text)
    if m:
        result["departure_runway"] = normalize_runway(m.group("depart"))

    m = WIND_RE.search(text)
    if m:
        direction = m.group("dir").upper()
        speed = m.group("speed")
        gust = m.group("gust")
        wind = f"{direction} {speed}KT"
        if gust:
            wind += f" G{gust}KT"
        result["wind"] = wind

    m = TIME_RE.search(text)
    if m:
        result["atis_time"] = m.group("time")

    return result


def fetch_latest_atis() -> dict[str, Any]:
    resp = requests.get(ATIS_API_URL, timeout=REQUEST_TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    data = resp.json()
    records = data if isinstance(data, list) else [data]
    if not records:
        raise ValueError("No ATIS records returned")

    def updated_key(rec: dict[str, Any]) -> datetime:
        raw = rec.get("updatedAt")
        if not raw:
            return datetime.min.replace(tzinfo=timezone.utc)
        try:
            return datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)

    latest = sorted(records, key=updated_key, reverse=True)[0]
    text = str(latest.get("datis", ""))
    parsed = parse_atis_text(text)

    # Preserve useful fields for the UI while keeping the payload compact.
    return {
        "airport": AIRPORT,
        "updated_at": latest.get("updatedAt"),
        "status": "Live ATIS loaded",
        **parsed,
    }


def get_lga_status() -> dict[str, Any]:
    return fetch_latest_atis()

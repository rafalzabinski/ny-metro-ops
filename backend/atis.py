from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

import requests

AIRPORTS = {
    'KLGA': {'code': 'LGA', 'name': 'LaGuardia', 'lat': 40.7769, 'lon': -73.8740},
    'KJFK': {'code': 'JFK', 'name': 'John F. Kennedy', 'lat': 40.6413, 'lon': -73.7781},
    'KEWR': {'code': 'EWR', 'name': 'Newark Liberty', 'lat': 40.6895, 'lon': -74.1745},
}

REQUEST_TIMEOUT = 20

APPROACH_RE = re.compile(
    r'\b(?P<approach>(?:ILS(?: OR LOC)?|RNAV(?: [XYZ])?|VISUAL|LOC|LDA|RNP(?: AR)?)(?: [A-Z0-9/.-]+)*)'
    r'\s+R?Y?\s*(?P<landing>\d{1,2}[LRC]?)\s+APCH IN USE',
    re.IGNORECASE,
)
LAND_RE = re.compile(r'\b(?:LAND|LND)\s+R?Y?\s*(?P<landing>\d{1,2}[LRC]?)', re.IGNORECASE)
DEPART_RE = re.compile(r'\bDEPART(?:ING)?\s+R?Y?\s*(?P<depart>\d{1,2}[LRC]?)', re.IGNORECASE)
WIND_RE = re.compile(r'\b(?P<dir>\d{3}|VRB)(?P<speed>\d{2})(?:G(?P<gust>\d{2}))?KT\b', re.IGNORECASE)
TIME_RE = re.compile(r'\b(?P<time>\d{4})Z\b')
DEPG_RE = re.compile(r'\bDEPG\s+R?Y?\s*(?P<depart>\d{1,2}[LRC]?)', re.IGNORECASE)
APPROACH_ASSIGN_RE = re.compile(
    r'\bAPPROACH IN USE\s+(?P<body>.*?)(?:\.\s|$)',
    re.IGNORECASE,
)


def normalize_runway(value: str) -> str:
    value = value.upper().strip()
    match = re.match(r'^(\d{1,2})([LRC]?)$', value)
    if not match:
        return value
    number, suffix = match.groups()
    if len(number) == 1:
        number = '0' + number
    return number + suffix


def normalize_approach(value: str) -> str:
    value = value.upper().strip()
    value = re.sub(r'\s+R(?:W)?Y$', '', value).strip()
    value = value.replace(' OR LOC', '')
    return value


def _parse_assigned_approach(body: str) -> tuple[str | None, str | None]:
    """
    Parse ATIS phrases like:
      APPROACH IN USE RNAV GPS Z RY 13L, RNAV GPS X RY 22L. DEPG RY 13R
    Returns a cleaned approach description and a runway string if found.
    """
    body = body.strip()
    runway_matches = re.findall(r"RY\s*(\d{1,2}[LRC]?)", body, re.IGNORECASE)
    runway_text = " / ".join(normalize_runway(r) for r in runway_matches) if runway_matches else None

    # Remove runway assignments, then compress spacing/punctuation.
    approach = re.sub(r"RY\s*\d{1,2}[LRC]?", "", body, flags=re.IGNORECASE)
    approach = re.sub(r"\bDEPG\b.*$", "", approach, flags=re.IGNORECASE)
    approach = re.sub(r"\s+", " ", approach).strip(" ,.;")
    if not approach:
        approach = None
    return approach, runway_text


def parse_atis_text(text: str) -> dict[str, str]:
    result: dict[str, str] = {'raw_atis': text.strip()}

    # First, handle the generic "ILS RWY XX APCH IN USE" pattern used by some airports.
    m = APPROACH_RE.search(text)
    if m:
        approach = normalize_approach(m.group("approach"))
        landing = normalize_runway(m.group("landing"))
        result["approach_type"] = approach
        result["landing_runway"] = landing
        result["approach_label"] = f"{approach} RWY {landing}"

    # JFK often uses "APPROACH IN USE ..." with multiple runway assignments in one sentence.
    m = APPROACH_ASSIGN_RE.search(text)
    if m:
        approach, runway_text = _parse_assigned_approach(m.group("body"))
        if approach and "approach_type" not in result:
            result["approach_type"] = approach
            result["approach_label"] = approach
        if runway_text and "landing_runway" not in result:
            result["landing_runway"] = runway_text

    m = LAND_RE.search(text)
    if m and "landing_runway" not in result:
        result["landing_runway"] = normalize_runway(m.group("landing"))

    m = DEPG_RE.search(text)
    if m and "departure_runway" not in result:
        result["departure_runway"] = normalize_runway(m.group("depart"))

    m = DEPART_RE.search(text)
    if m and "departure_runway" not in result:
        result["departure_runway"] = normalize_runway(m.group("depart"))

    m = WIND_RE.search(text)
    if m:
        direction = m.group('dir').upper()
        speed = m.group('speed')
        gust = m.group('gust')
        wind = f'{direction} {speed}KT'
        if gust:
            wind += f' G{gust}KT'
        result['wind'] = wind

    m = TIME_RE.search(text)
    if m:
        result['atis_time'] = m.group('time')

    return result


def _updated_key(rec: dict[str, Any]) -> datetime:
    raw = rec.get('updatedAt')
    if not raw:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromisoformat(str(raw).replace('Z', '+00:00'))
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


def fetch_latest_atis(airport_icao: str) -> dict[str, Any]:
    url = f'https://atis.info/api/{airport_icao}'
    resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers={'User-Agent': 'Mozilla/5.0'})
    resp.raise_for_status()
    data = resp.json()
    records = data if isinstance(data, list) else [data]
    if not records:
        raise ValueError('No ATIS records returned')

    latest = sorted(records, key=_updated_key, reverse=True)[0]
    text = str(latest.get('datis', ''))
    parsed = parse_atis_text(text)
    airport = AIRPORTS.get(airport_icao, {'code': airport_icao[1:], 'name': airport_icao})

    return {
        'icao': airport_icao,
        'code': airport['code'],
        'name': airport['name'],
        'lat': airport.get('lat'),
        'lon': airport.get('lon'),
        'updated_at': latest.get('updatedAt'),
        'status': 'Live ATIS loaded',
        **parsed,
    }


def get_nyc_airports_status() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for airport_icao in ['KLGA', 'KJFK', 'KEWR']:
        try:
            results.append(fetch_latest_atis(airport_icao))
        except Exception as exc:
            airport = AIRPORTS[airport_icao]
            results.append(
                {
                    'icao': airport_icao,
                    'code': airport['code'],
                    'name': airport['name'],
                    'lat': airport['lat'],
                    'lon': airport['lon'],
                    'updated_at': None,
                    'status': f'Failed to load ATIS: {exc}',
                    'raw_atis': None,
                    'approach_label': '—',
                    'landing_runway': '—',
                    'departure_runway': '—',
                    'wind': '—',
                    'atis_time': '—',
                }
            )
    return results


def get_lga_status() -> dict[str, Any]:
    return fetch_latest_atis('KLGA')

"""Client for the QGEO SLM (Site Log Manager) public REST API at slm.qgeo.kz.

This instance runs the IGS Site Log Manager
(https://github.com/International-GNSS-Service/SLM). Its public,
unauthenticated station list is served from:

    GET {SLM_BASE_URL}/api/public/stations/

Pagination follows the `datatables`-style scheme used by that project:
`length`/`start` query params, and a `next` field in the response carrying
the full URL of the next page (or null on the last page). No login is
required for this endpoint; SLM_USER/SLM_PASS are sent as HTTP Basic auth
only in case a future deployment locks it down.

Environment variables (put in .env):
- SLM_BASE_URL (e.g. https://slm.qgeo.kz)
- SLM_USER (optional)
- SLM_PASS (optional)
"""
from pathlib import Path
import os
import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')

SLM_BASE_URL = os.getenv('SLM_BASE_URL', 'https://slm.qgeo.kz').rstrip('/')
SLM_USER = os.getenv('SLM_USER')
SLM_PASS = os.getenv('SLM_PASS')

STATIONS_URL = f"{SLM_BASE_URL}/api/public/stations/"

# station records per page; the SLM instance currently hosts under 100
# stations total, so this comfortably fits everything in one request
PAGE_SIZE = 500


def _auth():
    if SLM_USER and SLM_PASS:
        return (SLM_USER, SLM_PASS)
    return None


def get_stations(timeout=30):
    """Fetch all stations from the SLM public API, following pagination.

    Returns a list of station dicts using SLM's own field names, e.g.:
    {'name': 'EIND00KAZ', 'llh': [lat, lon, height], 'city': 'Inderbor',
     'antenna_type': 'LEIAR25.R4', 'antenna_serial_number': '...',
     'receiver_type': 'LEICA GR30', 'serial_number': '...',
     'agencies': [{'name': ..., 'shortname': ..., 'country': ...}], ...}
    """
    stations = []
    url = STATIONS_URL
    params = {'length': PAGE_SIZE}
    while url:
        resp = requests.get(url, params=params, auth=_auth(), timeout=timeout)
        resp.raise_for_status()
        payload = resp.json()
        stations.extend(payload.get('data', []))
        url = payload.get('next')
        # `next` already carries its own query string
        params = None
    return stations


def build_station_map(stations, code_length=4):
    """Return dict mapping short station codes (e.g. 'EIND') -> fields.

    Keys match the columns used in `data/templates/station_table_template.csv`
    so callers can merge this straight into a candidate record.
    """
    mapping = {}
    for s in stations:
        name = (s.get('name') or '').strip().upper()
        if not name:
            continue
        code = name[:code_length]

        lat, lon, height = (list(s.get('llh') or ()) + [None, None, None])[:3]
        # antenna_marker_une is (Up, North, East) eccentricity of the antenna
        # reference point above the survey marker, i.e. the antenna height
        antenna_height = (list(s.get('antenna_marker_une') or ()) + [None])[0]

        agencies = s.get('agencies') or []
        operator = ''
        if agencies:
            operator = agencies[0].get('name', '')
            if agencies[0].get('country'):
                operator = f"{operator} ({agencies[0]['country']})"

        entry = {
            'IGS_ID': name,
            'SiteName': s.get('city') or '',
            'Latitude_deg': lat,
            'Longitude_deg': lon,
            'Ellipsoidal_height_m': height,
            'Antenna_model': s.get('antenna_type') or '',
            'Antenna_serial': s.get('antenna_serial_number') or '',
            'Antenna_height_m': antenna_height,
            'Receiver_model': s.get('receiver_type') or '',
            'Receiver_serial': s.get('serial_number') or '',
            'DOMES_number': s.get('domes_number') or '',
            'Operator_institution': operator,
        }
        mapping[code] = {k: v for k, v in entry.items() if v not in (None, '')}
    return mapping

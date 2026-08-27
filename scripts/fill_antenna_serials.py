#!/usr/bin/env python3
"""Fill antenna serial numbers in candidates.json and candidates_summary.csv using SLM API.

Usage: python3 scripts/fill_antenna_serials.py

Requires: requests, python-dotenv, pandas
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
JSON_PATH = ROOT / 'data' / 'web' / 'candidates.json'
CSV_PATH = ROOT / 'data' / 'processed' / 'candidates_summary' / 'candidates_summary.csv'


def load_candidates(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_candidates(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_serial_map():
    from slm_api import get_stations, build_station_map
    stations = get_stations()
    mapping = build_station_map(stations)
    return {code: info['Antenna_serial'] for code, info in mapping.items() if info.get('Antenna_serial')}


def update_candidates_with_serials(candidates, serial_map):
    changed = 0
    for rec in candidates:
        code = (rec.get('StationCode') or rec.get('Site') or '').strip().upper()
        if not code:
            continue
        short = code[:4]
        serial = serial_map.get(short)
        if serial and rec.get('Antenna_serial') != serial:
            rec['Antenna_serial'] = serial
            changed += 1
    return changed


def update_csv(csv_path, serial_map):
    import pandas as pd
    if not csv_path.exists():
        print('CSV not found, skipping CSV update:', csv_path)
        return 0
    df = pd.read_csv(csv_path, dtype=str).fillna('')
    if 'Antenna_serial' not in df.columns:
        df['Antenna_serial'] = ''
    updated = 0
    for idx, row in df.iterrows():
        site = str(row.get('Site', '')).strip().upper()
        if not site:
            continue
        short = site[:4]
        serial = serial_map.get(short)
        if serial and df.at[idx, 'Antenna_serial'] != serial:
            df.at[idx, 'Antenna_serial'] = serial
            updated += 1
    df.to_csv(csv_path, index=False)
    return updated


def main():
    candidates = load_candidates(JSON_PATH)
    serial_map = build_serial_map()

    dbg = ROOT / 'data' / 'processed' / 'slm_antenna_serials.json'
    with open(dbg, 'w', encoding='utf-8') as f:
        json.dump(serial_map, f, ensure_ascii=False, indent=2)
    print(f'Built serial map entries: {len(serial_map)}; wrote debug {dbg}')

    changed = update_candidates_with_serials(candidates, serial_map)
    save_candidates(JSON_PATH, candidates)
    print(f'Updated {changed} records in {JSON_PATH}')

    csv_updated = update_csv(CSV_PATH, serial_map)
    print(f'Updated {csv_updated} cells in CSV {CSV_PATH}')


if __name__ == '__main__':
    main()

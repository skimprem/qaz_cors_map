#!/usr/bin/env python3
"""Generate 9-char IGS IDs and fill SiteName from the SLM API, update JSON/CSV tables.

Usage: python3 scripts/generate_igs_ids.py
"""
import json
from pathlib import Path
import sys

try:
    import pandas as pd
except Exception as e:
    print("Missing dependency: pandas. Install with `pip install pandas`", file=sys.stderr)
    raise


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
JSON_PATH = ROOT / "data" / "web" / "candidates.json"
CSV_PATH = ROOT / "data" / "processed" / "candidates_summary" / "candidates_summary.csv"


def read_candidates(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_candidates(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    from slm_api import get_stations, build_station_map

    candidates = read_candidates(JSON_PATH)

    stations = get_stations()
    mapping = build_station_map(stations)

    # write mapping for inspection
    debug_out = ROOT / "data" / "processed" / "mapping_city.json"
    with open(debug_out, 'w', encoding='utf-8') as dfout:
        json.dump(mapping, dfout, ensure_ascii=False, indent=2)
    print(f"Wrote station->city mapping for inspection: {debug_out} (entries: {len(mapping)})")

    # report which candidate codes have no mapping
    candidate_codes = [(rec.get('StationCode') or rec.get('Site') or '').strip().upper() for rec in candidates]
    missing = [c for c in candidate_codes if c and c not in mapping]
    print(f"Mapping coverage: {len(candidate_codes)-len(missing)}/{len(candidate_codes)} found; {len(missing)} missing")
    if missing:
        print("Missing candidates:", ','.join(missing))

    # update candidates data
    changed = 0
    for rec in candidates:
        code = rec.get("StationCode") or rec.get("Site")
        if not code:
            continue
        code = code.strip().upper()
        info = mapping.get(code, {})
        # prefer the real IGS ID (site name) reported by SLM, fall back to the
        # locally-assumed convention for stations not yet found in the API
        igs_id = info.get("IGS_ID") or f"{code}00KAZ"
        if rec.get("IGS_ID", "") != igs_id:
            rec["IGS_ID"] = igs_id
            changed += 1
        if (not rec.get("SiteName")) and info.get("SiteName"):
            rec["SiteName"] = info["SiteName"]
            changed += 1

    write_candidates(JSON_PATH, candidates)
    print(f"Updated {len(candidates)} records in {JSON_PATH} (changed fields: {changed})")

    # update CSV if exists
    if CSV_PATH.exists():
        df = pd.read_csv(CSV_PATH)
        if 'IGS_ID' not in df.columns:
            df['IGS_ID'] = ""
        if 'SiteName' not in df.columns:
            df['SiteName'] = ""
        updated = 0
        for idx, row in df.iterrows():
            site = str(row.get('Site', '')).strip().upper()
            if not site:
                continue
            info = mapping.get(site, {})
            igs = info.get("IGS_ID") or f"{site}00KAZ"
            if df.at[idx, 'IGS_ID'] != igs:
                df.at[idx, 'IGS_ID'] = igs
                updated += 1
            if (not str(df.at[idx, 'SiteName']).strip()) and info.get("SiteName"):
                df.at[idx, 'SiteName'] = info["SiteName"]
                updated += 1
        df.to_csv(CSV_PATH, index=False)
        print(f"Updated CSV {CSV_PATH} (updated cells: {updated})")
    else:
        print(f"CSV not found: {CSV_PATH}; skipping CSV update")


if __name__ == '__main__':
    main()

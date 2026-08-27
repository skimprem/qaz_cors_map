#!/usr/bin/env python3
"""
Generate web assets: JSON summary and station thumbnails.

Usage:
  # activate venv first
  python3 scripts/generate_web_assets.py

This script:
 - reads `data/processed/candidates_summary/candidates_summary.csv`
 - writes `data/web/candidates.json`
 - converts `data/stations/<ID>.pdf` first page to `data/web/station_images/<ID>.png` using `pdftoppm` if available

Requirements:
 - pandas
 - poppler-utils (`pdftoppm`) recommended for PDF->PNG conversion
"""
from pathlib import Path
import json
import subprocess
import sys
import shutil

try:
    import pandas as pd
except Exception:
    print('Please install pandas in your environment: pip install pandas')
    raise


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
CSV_IN = ROOT / 'data' / 'processed' / 'candidates_summary' / 'candidates_summary.csv'
WEB_DIR = ROOT / 'data' / 'web'
IMG_DIR = WEB_DIR / 'station_images'
STATIONS_PDF = ROOT / 'data' / 'stations'


def ensure_dirs():
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)


def write_json():
    if not CSV_IN.exists():
        print('Input CSV not found:', CSV_IN)
        return False
    df = pd.read_csv(CSV_IN, dtype=str).fillna('')

    # read template headers to ensure JSON includes all desired fields
    template_path = ROOT / 'data' / 'templates' / 'station_table_template.csv'
    template_fields = []
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as tf:
            header = tf.readline().strip()
            template_fields = [c.strip() for c in header.split(',') if c.strip()]

    # fetch station metadata directly from the SLM public API
    from slm_api import get_stations, build_station_map
    stations = get_stations()
    excel_map = build_station_map(stations)
    print(f'Loaded {len(excel_map)} stations from SLM API')

    records = []
    for _, row in df.iterrows():
        rec = {k: '' for k in template_fields} if template_fields else {}
        # copy existing columns
        for k, v in row.items():
            rec[k] = v
        # map common names from candidates_summary to template fields
        if 'Site' in row and 'StationCode' in rec:
            rec['StationCode'] = row['Site']
        if 'First_obs' in row and 'Obs_start_date' in rec:
            rec['Obs_start_date'] = row['First_obs']
        if 'Last_obs' in row and 'Obs_last_date' in rec:
            rec['Obs_last_date'] = row['Last_obs']
        if 'Span_yr' in row and 'Obs_span_yr' in rec:
            rec['Obs_span_yr'] = row['Span_yr']
        if 'Available' in row and 'Data_availability_count' in rec:
            rec['Data_availability_count'] = row['Available']
        if 'Processed' in row and 'Processed_count' in rec:
            rec['Processed_count'] = row['Processed']
        if 'Not_estimated' in row and 'Not_estimated_count' in rec:
            rec['Not_estimated_count'] = row['Not_estimated']
        if 'No_solution' in row and 'No_solution_count' in rec:
            rec['No_solution_count'] = row['No_solution']

        # AnnexA plot path if station PDF exists under data/stations
        site = row.get('Site', '').upper()
        pdf_path = ROOT / 'data' / 'stations' / f'{site}.pdf'
        if pdf_path.exists():
            if 'AnnexA_plot_path' in rec:
                rec['AnnexA_plot_path'] = str(pdf_path.relative_to(ROOT))
            else:
                rec['AnnexA_plot_path'] = str(pdf_path.relative_to(ROOT))
        # supplement from excel_map if available and template expects these fields
        if site and site in excel_map:
            for k, v in excel_map[site].items():
                if not rec.get(k):
                    rec[k] = v

        records.append(rec)
    # try to merge Annex A velocities extracted earlier
    annex_path = ROOT / 'data' / 'processed' / 'annexA_velocities.json'
    annex_map = {}
    if annex_path.exists():
        try:
            with open(annex_path, 'r', encoding='utf-8') as af:
                annex = json.load(af)
            for e in annex:
                # station_pdf like 'data/stations/EIND.pdf'
                sp = e.get('station_pdf','')
                stem = Path(sp).stem.upper()
                vals = e.get('values', {})
                annex_map[stem] = vals
        except Exception as e:
            print('Failed to load annex velocities:', e)

    # merge annex velocities into records
    for rec in records:
        code = (rec.get('StationCode') or rec.get('Site') or '').upper()
        if not code:
            continue
        vals = annex_map.get(code)
        if not vals:
            continue
        # for each velocity key, pick first found numeric value
        for k, v in vals.items():
            # k expected like 'V_N_mm_per_yr' or similar; map to fields used in UI
            if k.upper().startswith('V_N'):
                rec['Velocity_N_mm_per_yr'] = v.get('value') or ''
                if v.get('uncertainty'):
                    # set both naming conventions for compatibility
                    rec['Velocity_N_uncertainty_mm_per_yr'] = v.get('uncertainty')
                    rec['Velocity_uncertainty_N_mm_per_yr'] = v.get('uncertainty')
            elif k.upper().startswith('V_E'):
                rec['Velocity_E_mm_per_yr'] = v.get('value') or ''
                if v.get('uncertainty'):
                    rec['Velocity_E_uncertainty_mm_per_yr'] = v.get('uncertainty')
                    rec['Velocity_uncertainty_E_mm_per_yr'] = v.get('uncertainty')
            elif k.upper().startswith('V_U') or k.upper().startswith('V_UP'):
                rec['Velocity_U_mm_per_yr'] = v.get('value') or ''
                if v.get('uncertainty'):
                    rec['Velocity_U_uncertainty_mm_per_yr'] = v.get('uncertainty')
                    rec['Velocity_uncertainty_U_mm_per_yr'] = v.get('uncertainty')
            else:
                # unknown key: copy as-is
                rec[k] = v.get('value') or ''
                if v.get('uncertainty'):
                    rec[k + '_uncertainty'] = v.get('uncertainty')

    # deduplicate records by StationCode (or Site) keeping non-empty fields
    deduped = {}
    for rec in records:
        code = (rec.get('StationCode') or rec.get('Site') or '').upper()
        if not code:
            # fallback to source_file or unique id
            code = rec.get('source_file', '') + '|' + rec.get('Site', '')
        if code not in deduped:
            deduped[code] = dict(rec)
        else:
            exist = deduped[code]
            for k, v in rec.items():
                if (exist.get(k) in (None, '') ) and v not in (None, ''):
                    exist[k] = v
            deduped[code] = exist

    out_records = list(deduped.values())
    out = WEB_DIR / 'candidates.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(out_records, f, ensure_ascii=False, indent=2)
    print('Wrote', out)
    return True


def pdftoppm_available():
    return shutil.which('pdftoppm') is not None


def make_thumbnail(pdf_path: Path, out_path: Path):
    # Use pdftoppm to render first page as PNG
    if not pdftoppm_available():
        print('pdftoppm not found; skipping thumbnails. Install poppler-utils.')
        return False

    cmd = ['pdftoppm', '-f', '1', '-singlefile', '-png', str(pdf_path), str(out_path.with_suffix(''))]
    try:
        subprocess.run(cmd, check=True)
        print('Created thumbnail', out_path)
        return True
    except subprocess.CalledProcessError:
        print('pdftoppm failed for', pdf_path)
        return False


def generate_thumbnails():
    pdfs = sorted(STATIONS_PDF.glob('*.pdf'))
    if not pdfs:
        print('No station PDFs found in', STATIONS_PDF)
        return
    for p in pdfs:
        id = p.stem.upper()
        out_png = IMG_DIR / f'{id}.png'
        if out_png.exists():
            continue
        make_thumbnail(p, out_png)


def main():
    ensure_dirs()
    ok = write_json()
    if ok:
        generate_thumbnails()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Assemble comparative table for 19 candidate stations.

Reads CSV tables produced by `scripts/parse_reports.py` under `data/processed/`,
extracts per-site metrics and writes `data/processed/candidates_summary.csv` and `.xlsx`.
"""
from pathlib import Path
import re
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / 'data' / 'processed'
OUT = PROCESSED / 'candidates_summary'

CANDIDATES = [
    'EIND','LORA','RBEY','RAKT','PZHT','DYRG','NARS','DBOZ','CKSH',
    'PUZK','TNIS','MKRJ','MSAT','MAKD','SEKB','SSHB','FCKP','BUSH','ZNUR'
]


def is_site_code(s: str):
    if not isinstance(s, str):
        return False
    return bool(re.fullmatch(r'[A-Z0-9]{4}', s.strip()))


def extract_rows_from_csv(csv_path: Path):
    rows = []
    try:
        df = pd.read_csv(csv_path, header=None, dtype=str, keep_default_na=False)
    except Exception:
        return rows

    for _, r in df.iterrows():
        first = r.iloc[0].strip() if isinstance(r.iloc[0], str) else ''
        if is_site_code(first):
            # get up to 8 columns if present
            vals = [r.iloc[i].strip() if i < len(r) else '' for i in range(8)]
            rows.append(vals)
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    all_csvs = list(PROCESSED.rglob('*.csv'))
    extracted = []
    for c in all_csvs:
        rows = extract_rows_from_csv(c)
        for vals in rows:
            extracted.append({
                'Site': vals[0],
                'First_obs': vals[1],
                'Last_obs': vals[2],
                'Span_yr': vals[3],
                'Available': vals[4],
                'Processed': vals[5],
                'Not_estimated': vals[6],
                'No_solution': vals[7],
                'source_file': str(c.relative_to(ROOT))
            })

    df = pd.DataFrame(extracted)
    if df.empty:
        print('No site rows found in processed CSVs')
        return

    # keep only candidates
    df_candidates = df[df['Site'].isin(CANDIDATES)].copy()

    # Convert numeric columns
    for col in ['Span_yr','Available','Processed','Not_estimated','No_solution']:
        df_candidates[col] = pd.to_numeric(df_candidates[col], errors='coerce')

    # Reorder rows by candidate order
    df_candidates['Site'] = pd.Categorical(df_candidates['Site'], categories=CANDIDATES, ordered=True)
    df_candidates = df_candidates.sort_values('Site')

    out_csv = OUT / 'candidates_summary.csv'
    out_xlsx = OUT / 'candidates_summary.xlsx'
    df_candidates.to_csv(out_csv, index=False)
    try:
        df_candidates.to_excel(out_xlsx, index=False)
    except Exception:
        pass

    print(f'Wrote summary for {len(df_candidates)} candidate stations to {out_csv}')


if __name__ == '__main__':
    main()

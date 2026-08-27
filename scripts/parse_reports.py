#!/usr/bin/env python3
"""
Parse Rui's PDF reports into CSV and JSON files.

Usage:
  python scripts/parse_reports.py

Outputs to: data/processed/

Requires: pdfplumber, pandas
"""
import os
from pathlib import Path
import json
import pandas as pd
import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / 'data' / 'report'
OUT_DIR = ROOT / 'data' / 'processed'


def ensure_out():
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_tables_from_pdf(pdf_path: Path):
    tables = []
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            # try extract tables
            try:
                page_tables = page.extract_tables()
            except Exception:
                page_tables = []

            for t_idx, raw_table in enumerate(page_tables, start=1):
                # normalize rows
                df = pd.DataFrame(raw_table)
                tables.append({'page': i, 'table_index': t_idx, 'df': df})

            # also save page text for manual parsing
            try:
                text = page.extract_text() or ''
            except Exception:
                text = ''
            texts.append({'page': i, 'text': text})

    return tables, texts


def save_tables(tables, out_prefix: Path):
    saved = []
    for t in tables:
        page = t['page']
        idx = t['table_index']
        df: pd.DataFrame = t['df']
        # try to set first row as header if it looks like header
        out_csv = out_prefix / f'table_page{page:03d}_idx{idx:02d}.csv'
        try:
            df.to_csv(out_csv, index=False, header=False)
        except Exception:
            df.to_csv(out_csv, index=False)
        saved.append(str(out_csv))
    return saved


def save_texts(texts, out_prefix: Path):
    out_txt = out_prefix / 'pages_text.txt'
    with open(out_txt, 'w', encoding='utf-8') as f:
        for p in texts:
            f.write(f"--- PAGE {p['page']} ---\n")
            f.write(p['text'] + '\n\n')
    return str(out_txt)


def process_report(pdf_file: Path):
    print(f'Processing: {pdf_file}')
    tables, texts = extract_tables_from_pdf(pdf_file)
    out_prefix = OUT_DIR / pdf_file.stem
    out_prefix.mkdir(parents=True, exist_ok=True)

    saved_tables = save_tables(tables, out_prefix)
    saved_text = save_texts(texts, out_prefix)

    manifest = {
        'pdf': str(pdf_file),
        'tables_csv': saved_tables,
        'pages_text': saved_text,
        'num_tables': len(saved_tables),
        'num_pages': len(texts)
    }

    with open(out_prefix / 'manifest.json', 'w', encoding='utf-8') as mf:
        json.dump(manifest, mf, ensure_ascii=False, indent=2)

    print(f'Wrote {len(saved_tables)} tables and text for {pdf_file.name}')


def main():
    ensure_out()
    pdfs = sorted(REPORT_DIR.glob('*.pdf'))
    if not pdfs:
        print('No PDF reports found in', REPORT_DIR)
        return

    for pdf in pdfs:
        process_report(pdf)


if __name__ == '__main__':
    main()

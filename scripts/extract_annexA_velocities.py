#!/usr/bin/env python3
"""Extract station velocity numbers from Annex A PDFs in data/stations.

Workflow:
- try to extract selectable text using pdfplumber
- search for velocity patterns (V_N, V_E, V_UP, "velocity", numbers with mm/yr)
- if no text, and if `pdftoppm` + `pytesseract` available, rasterize first page and OCR it
- save JSON with found values to `data/processed/annexA_velocities.json`

Run locally in the project's venv:
  source .venv/bin/activate
  pip install pandas pdfplumber pytesseract pillow
  # system: install tesseract-ocr and poppler-utils (pdftoppm)
  python3 scripts/extract_annexA_velocities.py
"""
from pathlib import Path
import re
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STATIONS_DIR = ROOT / 'data' / 'stations'
OUT_PATH = ROOT / 'data' / 'processed' / 'annexA_velocities.json'


def extract_text_pdf(path):
    try:
        import pdfplumber
    except Exception:
        return ''
    try:
        with pdfplumber.open(path) as pdf:
            pages = []
            for p in pdf.pages:
                t = p.extract_text()
                if t:
                    pages.append(t)
            return "\n".join(pages)
    except Exception:
        return ''


def ocr_pdf(path):
    # requires pdftoppm (poppler) and pytesseract + pillow
    png_path = None
    try:
        cmd = ['pdftoppm', '-f', '1', '-l', '1', '-png', str(path), str(path) + '_page']
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # pdftoppm will write file like <path>_page-1.png
        cand = Path(str(path) + '_page-1.png')
        if not cand.exists():
            # try alternative suffix
            cand = Path(str(path) + '_page.png')
        if not cand.exists():
            return ''
        png_path = cand
        from PIL import Image
        import pytesseract
        txt = pytesseract.image_to_string(Image.open(png_path))
        # cleanup produced image
        try:
            png_path.unlink()
        except Exception:
            pass
        return txt
    except FileNotFoundError:
        return ''
    except Exception:
        return ''


def extract_trends_with_positions(path):
    """Use pdfplumber word positions to find 'trend = X +/- Y mm/yr' occurrences and their vertical position."""
    try:
        import pdfplumber
    except Exception:
        return []
    res = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                words = page.extract_words()
                n = len(words)
                i = 0
                while i < n:
                    w = words[i]['text']
                    if 'trend' in w.lower():
                        # collect following words up to a unit indicator or a short window
                        seq = [words[i]]
                        j = i+1
                        while j < n and len(seq) < 12:
                            seq.append(words[j])
                            if re.search(r'mm\W*/?\W*yr|mm', words[j]['text'], flags=re.I):
                                break
                            j += 1
                        text = ' '.join(wd['text'] for wd in seq)
                        # search number and uncertainty
                        m = re.search(r'([+-]?\d+\.?\d*)\s*(?:±|\+/-|\+_)?\s*([0-9]+\.?[0-9]*)?', text)
                        if m:
                            val = m.group(1)
                            unc = m.group(2)
                            # compute median top position of words in seq
                            tops = [float(wd.get('top', 0)) for wd in seq]
                            top_med = sorted(tops)[len(tops)//2] if tops else 0
                            res.append({'top': top_med, 'value': val, 'uncertainty': unc, 'match': text})
                        i = j
                    else:
                        i += 1
    except Exception:
        return []
    return res


def find_velocities(text):
    if not text or not text.strip():
        return {}
    res = {}
    # 1) Prefer explicit 'trend = ...' occurrences with component nearby
    # examples: "North trend = -0.12 mm/yr" or "trend (East) = 0.05 mm/yr" or "trend = -0.12 mm/yr (N)"
    # accept ±, +/- and the observed '+_' style used in these GMT plots
    trend_pat = re.compile(r'(?:trend)\s*(?:\(|:)?\s*(?:\(?\s*(North|East|Up|N|E|U)\s*\)?)?\s*[:=]\s*([+-]?\d+\.?\d*)\s*(?:±|\+/-|\+_)?\s*([0-9]+\.?[0-9]*)?\s*(mm\s*/?\s*yr|mm/yr|mm yr|mmyr)?', flags=re.I)
    for m in trend_pat.finditer(text):
        label = m.group(1)
        val = m.group(2)
        unc = m.group(3)
        if label:
            lab = label.upper()
            if lab.startswith('N'):
                res['V_N_mm_per_yr'] = {'value': val, 'uncertainty': unc, 'match': m.group(0)}
            elif lab.startswith('E'):
                res['V_E_mm_per_yr'] = {'value': val, 'uncertainty': unc, 'match': m.group(0)}
            elif lab.startswith('U'):
                res['V_U_mm_per_yr'] = {'value': val, 'uncertainty': unc, 'match': m.group(0)}
        else:
            # no component label in same match — attempt to infer from nearby text window
            span = text[max(0, m.start()-80):m.end()+80]
            if re.search(r'North|Latitude|Lat|N', span, re.I) and 'V_N_mm_per_yr' not in res:
                res['V_N_mm_per_yr'] = {'value': val, 'uncertainty': unc, 'match': m.group(0)}
            elif re.search(r'East|Longitude|Lon|E', span, re.I) and 'V_E_mm_per_yr' not in res:
                res['V_E_mm_per_yr'] = {'value': val, 'uncertainty': unc, 'match': m.group(0)}
            elif re.search(r'Up|Height|Ellip|U', span, re.I) and 'V_U_mm_per_yr' not in res:
                res['V_U_mm_per_yr'] = {'value': val, 'uncertainty': unc, 'match': m.group(0)}

    # 2) fallback: generic patterns (V_N, North, numbers with ±)
    if not res:
        patterns = [
            r'V[_\s-]*(N|E|U|Up|North|East|Up)[:=\s]*([+-]?\d+\.?\d*)\s*(?:±|\+/-|\+_)?\s*([0-9]+\.?[0-9]*)?\s*(mm\s*/?\s*yr|mm/yr|mm yr|mmyr)?',
            r'(North|East|Up)[\s:]*(?:velocity|trend)?\s*[:=\s]*([+-]?\d+\.?\d*)\s*(?:±|\+/-|\+_)?\s*([0-9]+\.?[0-9]*)?\s*(mm/yr|mm/yr)?',
            r'([+-]?\d+\.?\d*)\s*(?:±|\+/-|\+_)\s*([0-9]+\.?[0-9]*)\s*(mm\s*/?\s*yr|mm/yr)',
        ]
        for pat in patterns:
            for m in re.finditer(pat, text, flags=re.I):
                groups = [g for g in m.groups() if g]
                label = None
                val = None
                unc = None
                for g in groups:
                    if re.match(r'^[+-]?\d', str(g)) and val is None:
                        val = g
                    elif isinstance(g, str) and re.search(r'^(N|E|U|North|East|Up)$', g, re.I) and label is None:
                        label = g
                    elif re.match(r'^[0-9]+\.?[0-9]*$', str(g)) and unc is None:
                        unc = g
                key = None
                if label:
                    k = label.upper()
                    if k.startswith('N'):
                        key = 'V_N_mm_per_yr'
                    elif k.startswith('E'):
                        key = 'V_E_mm_per_yr'
                    elif k.startswith('U') or k.startswith('UP'):
                        key = 'V_U_mm_per_yr'
                else:
                    # assign by availability order
                    if 'V_N_mm_per_yr' not in res:
                        key = 'V_N_mm_per_yr'
                    elif 'V_E_mm_per_yr' not in res:
                        key = 'V_E_mm_per_yr'
                    else:
                        key = 'V_U_mm_per_yr'
                if key and key not in res:
                    res[key] = {'value': val, 'uncertainty': unc, 'match': m.group(0)}

    # 3) If still missing components, collect generic numeric matches in text order
    needed = [k for k in ('V_N_mm_per_yr', 'V_E_mm_per_yr', 'V_U_mm_per_yr') if k not in res]
    if needed:
        num_pat = re.compile(r'([+-]?\d+\.?\d*)\s*(?:±|\+/-)?\s*([0-9]+\.?[0-9]*)?\s*(mm\s*/?\s*yr|mm/yr|mm yr|mmyr)', flags=re.I)
        matches = []
        for m in num_pat.finditer(text):
            matches.append((m.start(), m.group(1), m.group(2)))
        matches.sort(key=lambda x: x[0])
        # assign left-to-right to missing components in order N, E, U
        for (pos, val, unc), key in zip(matches, needed):
            if key not in res:
                res[key] = {'value': val, 'uncertainty': unc, 'match': val}

    return res


def process_file(path):
    # First try position-aware extraction (best for 3-panel GMT plots)
    tr = []
    try:
        tr = extract_trends_with_positions(path)
    except Exception:
        tr = []
    if tr and len(tr) >= 1:
        # sort by top coordinate (smaller top == visually higher on page)
        tr_sorted = sorted(tr, key=lambda x: x['top'])
        vals = {}
        # assign in visual order: top->Latitude (N), mid->Longitude (E), bottom->Vertical (U)
        mapping = ['V_N_mm_per_yr', 'V_E_mm_per_yr', 'V_U_mm_per_yr']
        for idx, item in enumerate(tr_sorted[:3]):
            key = mapping[idx]
            vals[key] = {'value': item.get('value'), 'uncertainty': item.get('uncertainty'), 'match': item.get('match')}
        snippet = '\n'.join(i['match'] for i in tr_sorted)
        return {'station_pdf': str(path.relative_to(ROOT)), 'method': 'positioned', 'values': vals, 'snippet': snippet}

    # fallback to text/OCR based extraction
    txt = extract_text_pdf(path)
    method = 'pdfplumber'
    if not txt.strip():
        txt = ocr_pdf(path)
        method = 'ocr' if txt.strip() else 'none'
    vals = find_velocities(txt)
    snippet = (txt or '').strip()[:500]
    return {'station_pdf': str(path.relative_to(ROOT)), 'method': method, 'values': vals, 'snippet': snippet}


def main():
    STATIONS_DIR.mkdir(parents=True, exist_ok=True)
    out = []
    for p in sorted(STATIONS_DIR.glob('*.pdf')):
        try:
            rec = process_file(p)
            out.append(rec)
            print(p.name, '->', rec['method'], 'found keys:', list(rec['values'].keys()))
        except Exception as e:
            print('ERR processing', p, e)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open('w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print('\nWrote', OUT_PATH)


if __name__ == '__main__':
    main()

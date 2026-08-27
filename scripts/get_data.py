import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Загружаем переменные из .env файла
load_dotenv(ROOT / '.env')

blocks = [
    [
        'LSAY',
        'LKZT',
        'LZHK',
        'EIND',
        'LKRT',
        'LCHP',
        'LORA',
        'LAKS'
    ],
    [
        'RBEY',
        'RKYZ',
        'RTSH',
        'RAKT',
        'RJNO',
        'RBLS'
    ],
    [
        'DAKT',
        'DEMB',
        'DKOM',
        'DYRG',
        'PTRG',
        'PZHT'
    ],
    [
        'DBOZ',
        'NARS',
        'NQZL',
        'NZHS',
        'NKZR'
    ],
    [
        'PKOS',
        'PUZK',
        'TNIS',
        'CKSH',
        'TPET'
    ],
    [
        'HMYA',
        'MAKD',
        'MKRJ',
        'MSAT',
        'XKZE',
        'HULB'
    ],
    [
        'CBST',
        'CERM',
        'SEKB',
        'SBYA',
        'SJLZ',
        'SPAV',
        'SSHB'
    ],
    [
        'FKRA',
        'FAJG',
        'BUSH',
        'FCKP',
        'FAKS',
        'FOSK',
        'FKTK',
        'FZAY'
    ],
    [
        'ZNUR',
    ]
]

# load station metadata directly from the SLM public API
from slm_api import get_stations

stations_list = get_stations()


def _flatten_station(s):
    lat, lon, height = (list(s.get('llh') or ()) + [None, None, None])[:3]
    return {
        'station_name': s.get('name'),
        'city': s.get('city'),
        'latitude': lat,
        'longitude': lon,
        'height_m': height,
        'antenna_type': s.get('antenna_type'),
        'antenna_serial_number': s.get('antenna_serial_number'),
        'receiver_type': s.get('receiver_type'),
        'receiver_serial_number': s.get('serial_number'),
        'domes_number': s.get('domes_number'),
    }


excel = pd.DataFrame([_flatten_station(s) for s in stations_list])
print('Loaded station metadata from SLM API, rows:', len(excel))

# Получаем параметры подключения из .env
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')

engine = create_engine(URL.create(
    'postgresql+psycopg2',
    username=user,
    password=password,
    host=host,
    port=port,
    database=database,
))

query = """
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');
"""

tables_df = pd.read_sql(query, engine)

query = "SELECT * FROM public.monitor_station;"

stations = pd.read_sql(query, engine)

query = "SELECT * FROM public.monitor_rinexfile;"
rinex = pd.read_sql(query, engine)

if rinex.empty:
    raise RuntimeError('No RINEX files found in public.monitor_rinexfile; nothing to plot.')

x_limits = (rinex['date'].min(), rinex['date'].max())

BLOCKS_DIR = ROOT / 'data' / 'blocks'
BLOCKS_DIR.mkdir(parents=True, exist_ok=True)

code_col = 'station_name'

for block_number, block in enumerate(blocks):

    excel_idx = excel[excel[code_col].astype(str).str.upper().isin([f'{x}00KAZ' for x in block])].index
    excel.loc[excel_idx, 'block'] = block_number + 1

    fig, ax = plt.subplots(nrows=len(block), figsize=(50, 10))
    
    # Если одна строка, ax будет скалярным, преобразуем в массив
    if len(block) == 1:
        ax = [ax]

    for station_idx, station in enumerate(block):

        station_ids = stations[stations['code'] == station]['id']
        
        if len(station_ids) != 1:
            print(f"Station: {station} - Not found or multiple entries found.")
            continue
       
        station_id = station_ids.iloc[0]
        print(f"Station: {station}, ID: {station_id}")
        rinex_files = rinex[rinex['station_id'] == station_id].sort_values('date')
        
        if len(rinex_files) == 0:
            print(f"Station: {station} - No RINEX files found.")
            continue

        # Создаем градиент цветов от красного (низкие значения) к зеленому (высокие)
        norm = Normalize(vmin=rinex_files['completeness'].min(), vmax=rinex_files['completeness'].max())
        colors = cm.RdYlGn(norm(rinex_files['completeness']))

        ax[station_idx].bar(rinex_files['date'], rinex_files['completeness'], width=1.0, color=colors)
        ax[station_idx].set_title(station)
        ax[station_idx].set_xlim(x_limits)
        ax[station_idx].set_ylabel("Completeness (%)")
        ax[station_idx].tick_params(axis='x', rotation=45)

    ax[-1].set_xlabel("Date")
    fig.suptitle(f"RINEX File Completeness for Block: {block_number+1}")
    fig.tight_layout()
    pic_path = BLOCKS_DIR / f"block_{block_number+1}.png"
    fig.savefig(pic_path)
    plt.close(fig)
    excel.loc[excel_idx, 'pic'] = str(pic_path.relative_to(ROOT))

# write JSON with blocks instead of Excel
out_path = ROOT / 'data' / 'stations' / 'cors_stations_complete_20260224_145419_with_blocks.json'
excel.to_json(out_path, orient='records', force_ascii=False)
print('Wrote', out_path)

engine.dispose()
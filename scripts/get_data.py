import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

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

excel = pd.read_excel('data/stations/cors_stations_complete_20260224_145419.xlsx')

print(excel.columns)

# Получаем параметры подключения из .env
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

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

x_limits = (rinex['date'].min(), rinex['date'].max())
for block_number, block in enumerate(blocks):

    excel_idx = excel[excel['station_name'].isin([f'{x}00KAZ' for x in block])].index

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


    fig.suptitle(f"RINEX File Completeness for Block: {block_number+1}")
    plt.xlabel("Date")
    plt.ylabel("Completeness (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    pic_path = f"block_{block_number+1}.png"
    plt.savefig(pic_path)
    excel.loc[excel_idx, 'pic'] = pic_path

excel.to_excel('data/stations/cors_stations_complete_20260224_145419_with_blocks.xlsx', index=False)
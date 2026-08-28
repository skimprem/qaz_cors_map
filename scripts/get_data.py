import sys
from pathlib import Path

import pandas as pd
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

load_dotenv(ROOT / '.env')

BLOCKS = [
    ['LSAY', 'LKZT', 'LZHK', 'EIND', 'LKRT', 'LCHP', 'LORA', 'LAKS'],
    ['RBEY', 'RKYZ', 'RTSH', 'RAKT', 'RJNO', 'RBLS'],
    ['DAKT', 'DEMB', 'DKOM', 'DYRG', 'PTRG', 'PZHT'],
    ['DBOZ', 'NARS', 'NQZL', 'NZHS', 'NKZR'],
    ['PKOS', 'PUZK', 'TNIS', 'CKSH', 'TPET'],
    ['HMYA', 'MAKD', 'MKRJ', 'MSAT', 'XKZE', 'HULB'],
    ['CBST', 'CERM', 'SEKB', 'SBYA', 'SJLZ', 'SPAV', 'SSHB'],
    ['FKRA', 'FAJG', 'BUSH', 'FCKP', 'FAKS', 'FOSK', 'FKTK', 'FZAY'],
    ['ZNUR'],
]

OUT_PATH = ROOT / 'data' / 'stations' / 'cors_stations_complete_20260224_145419_with_blocks.json'


def load_station_metadata():
    """Load station metadata directly from the SLM public API."""
    from slm_api import get_stations

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

    df = pd.DataFrame([_flatten_station(s) for s in get_stations()])
    print('Loaded station metadata from SLM API, rows:', len(df))
    return df


def assign_blocks(df):
    """Tag each station row with its block number by name matching. No DB needed."""
    for block_number, block in enumerate(BLOCKS):
        idx = df[df['station_name'].astype(str).str.upper().isin([f'{x}00KAZ' for x in block])].index
        df.loc[idx, 'block'] = block_number + 1
    return df


def generate_block_completeness_plots(df):
    """Plot per-station RINEX completeness bar charts per block and set df['pic'].

    Not called by default: these bar charts have been superseded by the
    Annex A trend plots and are no longer part of the published map/table.
    Requires a working Postgres connection (DB_* vars in .env) with QGEO's
    `monitor_station` / `monitor_rinexfile` tables (data availability
    tracking, unrelated to SLM's site-log metadata). Kept here in case the
    plots are ever needed again.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    import matplotlib.cm as cm

    engine = create_engine(URL.create(
        'postgresql+psycopg2',
        username=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
    ))
    try:
        stations = pd.read_sql("SELECT * FROM public.monitor_station;", engine)
        rinex = pd.read_sql("SELECT * FROM public.monitor_rinexfile;", engine)

        if rinex.empty:
            raise RuntimeError('No RINEX files found in public.monitor_rinexfile; nothing to plot.')

        x_limits = (rinex['date'].min(), rinex['date'].max())

        blocks_dir = ROOT / 'data' / 'blocks'
        blocks_dir.mkdir(parents=True, exist_ok=True)

        for block_number, block in enumerate(BLOCKS):
            idx = df[df['station_name'].astype(str).str.upper().isin([f'{x}00KAZ' for x in block])].index

            fig, ax = plt.subplots(nrows=len(block), figsize=(50, 10))
            if len(block) == 1:
                ax = [ax]

            for station_idx, station in enumerate(block):
                station_ids = stations[stations['code'] == station]['id']
                if len(station_ids) != 1:
                    print(f"Station: {station} - Not found or multiple entries found.")
                    continue

                station_id = station_ids.iloc[0]
                rinex_files = rinex[rinex['station_id'] == station_id].sort_values('date')
                if len(rinex_files) == 0:
                    print(f"Station: {station} - No RINEX files found.")
                    continue

                norm = Normalize(vmin=rinex_files['completeness'].min(), vmax=rinex_files['completeness'].max())
                colors = cm.RdYlGn(norm(rinex_files['completeness']))

                ax[station_idx].bar(rinex_files['date'], rinex_files['completeness'], width=1.0, color=colors)
                ax[station_idx].set_title(station)
                ax[station_idx].set_xlim(x_limits)
                ax[station_idx].set_ylabel("Completeness (%)")
                ax[station_idx].tick_params(axis='x', rotation=45)

            ax[-1].set_xlabel("Date")
            fig.suptitle(f"RINEX File Completeness for Block: {block_number + 1}")
            fig.tight_layout()
            pic_path = blocks_dir / f"block_{block_number + 1}.png"
            fig.savefig(pic_path)
            plt.close(fig)
            df.loc[idx, 'pic'] = str(pic_path.relative_to(ROOT))
    finally:
        engine.dispose()

    return df


def main():
    df = load_station_metadata()
    assign_blocks(df)
    df.to_json(OUT_PATH, orient='records', force_ascii=False)
    print('Wrote', OUT_PATH)


if __name__ == '__main__':
    main()

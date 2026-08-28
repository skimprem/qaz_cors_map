import json
from pathlib import Path

import pandas as pd
import geopandas as gpd
import requests
import zipfile
import folium

ROOT = Path(__file__).resolve().parents[1]

url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
zip_path = ROOT / "countries.zip"
extract_path = ROOT / "data" / "ne_countries"
shapefile_path = extract_path / "ne_110m_admin_0_countries.shp"

if not shapefile_path.exists():
    extract_path.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(zip_path, "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    zip_path.unlink()

world = gpd.read_file(shapefile_path)
kazakhstan = world[world['ADMIN'] == 'Kazakhstan']

source_path = ROOT / 'data' / 'stations' / 'cors_stations_complete_20260224_145419_with_blocks.json'
with open(source_path, 'r', encoding='utf-8') as f:
    df = pd.DataFrame(json.load(f))

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
    crs='EPSG:4326'
)

# link each candidate station's marker straight to its row in stations.html;
# stations.html only lists the 19 IGS candidates, so other network stations
# get no link here
candidates_path = ROOT / 'data' / 'web' / 'candidates.json'
candidate_codes = set()
if candidates_path.exists():
    with open(candidates_path, 'r', encoding='utf-8') as f:
        candidate_codes = {rec.get('StationCode', '').upper() for rec in json.load(f)}

station_codes = gdf['station_name'].astype(str).str[:4].str.upper()
gdf['Stations table'] = station_codes.apply(
    lambda code: f'<a href="stations.html?site={code}" target="_blank">Open in table &raquo;</a>'
    if code in candidate_codes else ''
)

index_map = kazakhstan.explore(
    color='none',
    tiles='CartoDB positron',
    zoom_start=5,
    tooltip=False,
    style_kwds={
    "color": "black",     # Set border (edge) color to black
    "weight": 2,          # Increase border thickness
    "fillOpacity": 0.6    # Transparency of the fill
    }
)

# Добавляем прямоугольники для каждого блока ПЕРЕД маркерами
margin = 0.5  # отступ в градусах
for block_id in gdf['block'].unique():
    if pd.isna(block_id):
        continue
    
    block_data = gdf[gdf['block'] == block_id]

    min_lat = block_data['latitude'].min() - margin
    max_lat = block_data['latitude'].max() + margin
    min_lon = block_data['longitude'].min() - margin
    max_lon = block_data['longitude'].max() + margin

    # Создаем прямоугольник
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
    popup_html = f'<b>Block {int(block_id)}</b>'

    folium.Rectangle(
        bounds=bounds,
        color='blue',
        fill=True,
        fillColor='blue',
        fillOpacity=0.1,
        weight=2,
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(index_map)

gdf.explore(
    m=index_map,
    column='block',
    cmap='Set1',
    marker_kwds={'radius': 5},
    tooltip=['station_name', 'block'],
    popup=True,
    legend=False
)

# gold ring around candidate stations so they stand out from the rest of the network
for _, row in gdf[station_codes.isin(candidate_codes)].iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=10,
        color='#FFD700',
        weight=3,
        fill=False,
        opacity=0.9,
    ).add_to(index_map)

# top-right so it doesn't overlap Leaflet's default zoom control (top-left)
header_html = """
<header style="position:absolute;top:10px;right:10px;z-index:4000;background:rgba(255,255,255,0.9);padding:6px;border-radius:4px;">
    <a href="stations.html">Stations table</a>
</header>
"""
index_map.get_root().html.add_child(folium.Element(header_html))

index_map.save(ROOT / 'index.html')

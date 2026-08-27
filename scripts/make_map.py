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
    pic_file = block_data['pic'].iloc[0] if 'pic' in block_data.columns and pd.notna(block_data['pic'].iloc[0]) else None
    
    min_lat = block_data['latitude'].min() - margin
    max_lat = block_data['latitude'].max() + margin
    min_lon = block_data['longitude'].min() - margin
    max_lon = block_data['longitude'].max() + margin
    
    # Создаем прямоугольник
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
    
    # HTML для попапа прямоугольника
    popup_html = f'<b>Block {int(block_id)}</b><br>'
    if pic_file:
        popup_html += f'<a href="{pic_file}" target="_blank">View Block Image</a>'
    
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

index_map.save(ROOT / 'index.html')

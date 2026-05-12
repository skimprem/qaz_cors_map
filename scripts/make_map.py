import os
import pandas as pd
import geopandas as gpd
import requests
import zipfile
import folium

url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
zip_path = "countries.zip"
extract_path = "data/ne_countries"

if not os.path.exists(extract_path):
    os.makedirs(extract_path, exist_ok=True)
    r = requests.get(url)
    with open(zip_path, "wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

world = gpd.read_file(f"{extract_path}/ne_110m_admin_0_countries.shp")
kazakhstan = world[world['ADMIN'] == 'Kazakhstan']

source_path = os.path.join(
    os.path.expanduser('~'),
    'gitrepo',
    'qaz_cors_map',
    'data',
    'stations',
    'cors_stations_complete_20260224_145419_with_blocks.xlsx'
)

df = pd.read_excel(source_path)

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

gdf.explore(
    m=index_map,
    column='block',
    cmap='Set1',
    marker_kwds={'radius': 5},
    tooltip=['station_name', 'block'],
    popup=True,
    legend=False
)

# Добавляем прямоугольники для каждого блока
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
    popup_html = f'<b>Block {block_id}</b><br>'
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

index_map.save('index.html')

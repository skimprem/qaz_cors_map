import os
import pandas as pd
import geopandas as gpd
import requests
import zipfile

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
    'src',
    'cors_stations_complete_20260224_145419.xlsx'
)

df = pd.read_excel(source_path, sheet_name='cors_stations_complete_20260224')

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
    crs='EPSG:4326'
)

index_map = kazakhstan.explore(
    color='grey',
    linewidth=8,
    tiles='CartoDB positron',
    zoom_start=5,
    tooltip=False
)

gdf.explore(
    m=index_map,
    color='red',
    marker_kwds={'radius': 5},
    tooltip=['station_name'],
    popup=True
)

index_map.save('index.html')

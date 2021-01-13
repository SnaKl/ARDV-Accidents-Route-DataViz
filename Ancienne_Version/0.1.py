import geojson
import geopandas as gpd
import pandas as pd
import folium
import csv



map = folium.Map(location=[46.4252134, 2.5], zoom_start=6)

sf = lambda x :{'fillColor':'#2196f3', 'fillOpacity':0.8, 'color':'#0000ee', 'weight':1, 'opacity':1}

folium.GeoJson(
    data="./geojson/departements.geojson",
    name="departements",
    style_function= sf,
    tooltip = folium.GeoJsonTooltip(fields=('nom', 'code'),
                                    aliases=('Commune', 'Code postal')),
).add_to(map)

map.save(outfile='map.html')
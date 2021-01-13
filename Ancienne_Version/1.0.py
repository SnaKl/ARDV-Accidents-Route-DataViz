import geojson
import geopandas as gpd
import pandas as pd
import folium
import plotly.express as px
import csv
import json

departement = gpd.read_file('./geojson/departements.geojson')

df = pd.read_csv('./csv/caracteristiques-2019.csv', sep=';')

name_department = pd.DataFrame(departement).loc[:, 'code':'nom']
nb_accident_dep = df.dep.astype(str).str.zfill(2).value_counts().rename_axis('code').reset_index(name='counts')

accident_dep = pd.merge(nb_accident_dep, name_department, on='code');


fig = px.choropleth_mapbox(accident_dep, geojson=departement, 
                           featureidkey='properties.code', locations='code', 
                           # custom_data=name_department,
                           # hover_data=name_department
                           color='counts', color_continuous_scale="Viridis",
                           range_color=(min(accident_dep.counts), max(accident_dep.counts)),
                           mapbox_style="carto-positron",
                           zoom=6, center = {"lat": 46.4252134, "lon": 2.5},
                           opacity=0.5,
                           labels={'nom':'test','code':'departement', 'counts': 'nombre d\'accident'}
                          )
# fig.update_traces(textposition='inside', textinfo='percent+label',\
#                  hovertemplate = "Country:%{label}: <br>Population: %{value} </br>(life expentancy, iso num) : %{customdata}"
# )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)  # Turn off reloader if inside Jupyter
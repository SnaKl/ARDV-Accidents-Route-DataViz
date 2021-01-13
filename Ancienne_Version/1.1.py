import geojson
import geopandas as gpd
import pandas as pd
import folium
import plotly.express as px
import csv
import json

departement = gpd.read_file('./geojson/departements.geojson')
x, y = departement.geometry[0].exterior.coords.xy

characteristics = pd.read_csv('./csv/accident/caracteristiques-2019.csv', sep=';')

name_department = pd.DataFrame(departement).loc[:, 'code':'nom']
nb_accident_dep = characteristics.dep.astype(str).str.zfill(2).value_counts().rename_axis('code').reset_index(name='counts')

accident_dep = pd.merge(nb_accident_dep, name_department, on='code');


defaultFig = px.choropleth_mapbox(accident_dep, geojson=departement, 
                           featureidkey='properties.code', locations='code', 
                           hover_name =accident_dep.nom,
                           color='counts', color_continuous_scale="Viridis",
                           range_color=(min(accident_dep.counts), max(accident_dep.counts)),
                           mapbox_style="carto-positron",
                           zoom=7, center = {"lat": 49.453533722068, "lon": 3.608257387098},
                           opacity=0.5,
                           labels={'code':'departement', 'counts': 'nombre d\'accident'}
                          )

defaultFig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# defaultFig.show()





import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=defaultFig, id='map')
])

@app.callback(
    Output("map", "figure"), 
    [Input("map", "clickData")])

def display_click_data(clickData):
    if(clickData == None): return (defaultFig)
    location = clickData['points'][0]['location']
    print(clickData)
    return (defaultFig)

# def madeFig(location):
#     departement = gpd.read_file('./geojson/departements.geojson')
#     characteristics = pd.read_csv('./csv/caracteristiques-2019.csv', sep=';')
#     name_department = pd.DataFrame(departement).loc[:, 'code':'nom']
#     nb_accident_dep = characteristics.dep.astype(str).str.zfill(2).value_counts().rename_axis('code').reset_index(name='counts')

#     accident_dep = pd.merge(nb_accident_dep, name_department, on='code');
#     returnFig = px.choropleth_mapbox(accident_dep, geojson=departement, 
#                            featureidkey='properties.code', locations='code', 
#                            # custom_data=name_department,
#                            # hover_data=name_department
#                            color='counts', color_continuous_scale="Viridis",
#                            range_color=(min(accident_dep.counts), max(accident_dep.counts)),
#                            mapbox_style="carto-positron",
#                            zoom=6, center = {"lat": 46.4252134, "lon": 2.5},
#                            opacity=0.5,
#                            labels={'nom':'test','code':'departement', 'counts': 'nombre d\'accident'}
#                           )
#     return(returnFig)

app.run_server(debug=True)  # Turn off reloader if inside Jupyter
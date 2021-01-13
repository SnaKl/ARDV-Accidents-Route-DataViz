import ClassMap
import math

classMap = ClassMap.ClassMap()
# print(classMap.GetAllCoords(classMap.geojson["departments"]))
# print(classMap.GetBounds(classMap.geojson['departments']))
# print(classMap.GetCenterCoords(classMap.GetAntipodes(classMap.geojson['departments'])))
# x, y = departement.geometry[0].exterior.coords.xy

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()
app.layout = html.Div([
   dcc.Graph(figure=classMap.defaultMap, id='map')
])

@app.callback(
   Output("map", "figure"), 
   [Input("map", "clickData")])

def display_click_data(clickData):
   if(clickData == None): return (classMap.defaultMap)
   # récupère le type de l'item cliquer (department/commune /department_point/commune_point)
   type = clickData['points'][0]['customdata'][0]
   # si clique sur un point 
   if(type.endswith('_point')): return classMap.defaultMap
   location = clickData['points'][0]['location']
   return madeFig(location, type)

def madeFig(location, type):
   if(type == 'commune'): 
      caracteristics = classMap.csv['characteristics']
      caracteristics['type'] = ['commune_point' for string in range(len(caracteristics.index))]
      datas = caracteristics.loc[caracteristics.com.astype(str).str.startswith(str(location))]
      miny = min(datas.lat) 
      minx = min(datas.long) 
      maxy = max(datas.lat)
      maxx = max(datas.long)
      zoom = -math.sqrt((maxx - minx) * (maxy - miny))*2+11
      return classMap.MakePlotMap(datas, zoom)
   else:
      test = madeFigDepartment(location)
      test.update_geos(fitbounds="locations")
      return test

def madeFigDepartment(location):
   accident_com_location = classMap.accident_com.loc[classMap.accident_com.insee_com.astype(str).str.startswith(str(location))]
   communes_location = classMap.geojson['communes'].loc[classMap.geojson['communes'].insee_com.astype(str).str.startswith(str(location))]    

   return classMap.MakeMap(accident_com_location, communes_location, 
                     "properties.insee_com", "insee_com", 
                     "nom_comm", ["postal_code","nb_accident"], "nb_accident",
                     classMap.GetZoom(communes_location), classMap.GetCenterCoords(classMap.GetAntipodes(communes_location)), 1,
                     {'insee_com':'Code INSEE', 'postal_code':'Code postal', 'nb_accident': 'Nombre d\'accidents'})


app.run_server(debug=True)  # Turn off reloader if inside Jupyter
import ClassMap

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
   location = clickData['points'][0]['location']
   type = clickData['points'][0]['customdata'][0]
   test = madeFig(location, type)
   return (test)

def madeFig(location, type):
   if(type == 'commune'): 
      return classMap.defaultMap
   else:
      return madeFigDepartment(location)

def madeFigDepartment(location):
   accident_com_location = classMap.accident_com.loc[classMap.accident_com.insee_com.astype(str).str.startswith(str(location))]
   communes_location = classMap.geojson['communes'].loc[classMap.geojson['communes'].insee_com.astype(str).str.startswith(str(location))]    

   return classMap.MakeMap(accident_com_location, communes_location, 
                     "properties.insee_com", "insee_com", 
                     "nom_comm", ["postal_code","nb_accident"], "nb_accident",
                     classMap.GetZoom(communes_location), classMap.GetCenterCoords(classMap.GetAntipodes(communes_location)), 1,
                     {'insee_com':'Code INSEE', 'postal_code':'Code postal', 'nb_accident': 'Nombre d\'accidents'})


app.run_server(debug=True)  # Turn off reloader if inside Jupyter
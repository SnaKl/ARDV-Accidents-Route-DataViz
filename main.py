import ClassMap
import math
import plotly.express as px
classMap = ClassMap.ClassMap()

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash.dash import no_update

# mulit drop down choice
multiOptionDict = {'Color': ['Department', 'Commune'], 'Point':0}

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
   dcc.Graph(id='histoMainGraph'),  
   html.Div([
      # dropdown choix des valuers
      html.Div([
         html.Label('Valeurs à observer', htmlFor='histoValuesParamDropdown'),
         dcc.Dropdown(id="histoValuesParamDropdown",
                     options = [{'label':label[0], 'value':label[1]} for label in classMap.observableValuesLabels.items()],
                     value='jour',
                     style={'width':250, 'textAlign':'left'}), 
      ], style={'textAlign': 'center'}),

      # dropdown choix comparaison
      html.Div([
         html.Label('Comparateur', htmlFor='histoColorParamDropdown'),
         dcc.Dropdown(id='histoColorParamDropdown',
                     options=[
                        {'label': 'None', 'value': ''},
                        {'label': 'Sexe', 'value': 'sexe'},
                        {'label': 'Gravité de blessure', 'value':'grav'},     
                     ],
                     value='',
                     style={'width':250, 'textAlign':'left'}), 
      ], style={'display': 'block', 'marginLeft': 10, 'textAlign': 'center'}),
      # radio button paramètre d'affichage
      html.Div([
         html.Label('Paramètre d\'affichage', htmlFor='histoHistnormParamRadioBtn'),
         dcc.RadioItems(id='histoHistnormParamRadioBtn',
            options=[
               {'label': 'Nombre', 'value': ''},
               {'label': 'Probability', 'value': 'probability'},
               {'label': 'Percent', 'value': 'percent'},
            ],
            value='percent',
            style={'textAlign': 'left', 'margin':'auto'}
         ),
      ], style={'display':'flex', 'flexDirection': 'column', 'marginLeft': 10, 'textAlign': 'center'}),
      # radio button paramètre d'affiche multiple
      html.Div([
         html.Label('Paramètre comparateur', htmlFor='histoBarmodeParamRadioBtn'),
         dcc.RadioItems(id='histoBarmodeParamRadioBtn',
            options=[
               {'label': 'Stack', 'value': 'stack'},
               {'label': 'Group', 'value': 'group'},
               {'label': 'Overlay', 'value': 'overlay'},
            ],
            value='stack',
            style={'textAlign': 'left', 'margin':'auto'}
         ),     
      ], style={'display':'flex', 'flexDirection': 'column', 'marginLeft': 10, 'textAlign': 'center'}),
   ], style={'display': 'flex', 'justifyContent':'center' }),   

   html.H1 ('Application', style={'textAlign': 'center'}), 
   html.Div([
      html.Label("Multi dynamic Dropdown", style={'marginRight': 5}),
      # dropdown choix d'affichage global map
      dcc.Dropdown(id="multiVisualChoice",
                  options=[{'label':name, 'value':name} for name in multiOptionDict.keys()],
                  style={'width':250, 'textAlign':'left'},
                  multi=True), 
      # permet de lancer le choix
      html.Button('Visualiser', id='visualButton', n_clicks=0, style={'marginLeft': 5}),
      ], style={'display': 'flex', 'justifyContent':'center', 'alignItems':'center'}),   
   # map
   dcc.Graph(figure=classMap.defaultMap, id='map'),
   
   html.Div([
         # dropdown du focus
         dcc.Dropdown(id='InfoDropdown',
                     options =[{ 'label':classMap.departmentsMapInfo['mergeText'][i], 
                                 'value':classMap.departmentsMapInfo['mergeText'][i]} 
                                 for i in range(classMap.departmentsMapInfo['size'])], 
                     style={'width':250, 'textAlign':'left'},), 
         # dropwn choix
         dcc.Dropdown(id='WTDdown',options=[{'label':'Zoom', 'value':'Zoom'}, {'label':'Focus', 'value':'Focus'}], style={'width':250, 'textAlign':'left', 'marginLeft':2},multi=True), 
         html.Button('Go', id='WTDrequest', n_clicks=0, style={'marginLeft':6}),
         ], style={'display': 'flex', 'justifyContent':'center', 'alignItems':'center'}),
   html.Div([
        dcc.Graph(id='MapFocusPie', style={'flex': '1 1 0', 'width': 0}),
        dcc.Graph(id='MapFocusLine', style={'flex': '1 1 0', 'width': 0}),
        dcc.Graph(id='MapFocusPieChoc', style={'flex': '1 1 0', 'width': 0}),
        ], style={'display': 'flex',}),
], style={'width': '90%', 'margin':'auto'})

# permet de changer l'histogramme à l'uppuie des radio button
@app.callback(
   Output('histoMainGraph', 'figure'),
   [Input('histoValuesParamDropdown', 'value'),
    Input('histoColorParamDropdown', 'value'),
    Input('histoHistnormParamRadioBtn', 'value'),
    Input('histoBarmodeParamRadioBtn', 'value')],
)
def UpdateHistoMainFigure(valuesParam, colorParam, histnormParam, barmodeParam):
   bargapParam = 0
   # si valuers et comparaison sont pareil
   if valuesParam == colorParam:
      # empèche la mise a jour
      raise PreventUpdate    
   
   # si pas de choix (none)
   if not histnormParam:
      histnormParam = ''
   
   # valuers choisie par l'utilisateur 
   loc = [valuesParam]
   if colorParam:
      loc += [colorParam]

   # récupère que les valuers choisie dans allMerged
   dataframe = classMap.allMerged.loc[:, loc]
   # si pas de colorParem
   if not colorParam:
      fig = px.histogram(dataframe, x=valuesParam,  histnorm=histnormParam)
   else:
      fig = px.histogram(dataframe, x=valuesParam, color=colorParam,  histnorm=histnormParam, barmode = barmodeParam)

   # affichage des pourcentage
   if histnormParam == 'percent':
      fig.update_yaxes(ticksuffix="%")

   # si groupe espace les valeurs
   if barmodeParam == 'group' and colorParam:
      bargapParam = .2

   fig.update_layout(title_text="Histogramme des accidents",
                     xaxis_title=valuesParam,
                     yaxis_title="Pourcentage d'accident",
                     legend_title=colorParam,
                     bargap=bargapParam
                     )

   return fig




############################## multi dropdown #################################
# s'occupe de généré les options en fonctions des options déja séléctionné
@app.callback(
   Output('multiVisualChoice', 'options'),
   Input('multiVisualChoice', 'value'),
   # empeche l'appele au chargement de la map
   prevent_initial_call=True
)
def UpdateMultiOptions(values):
   # si aucune valuer ne fait rien
   if not values:
      return [{'label':name, 'value':name} for name in multiOptionDict.keys()]
   # si permière valeur ne correspond pas à Color ou point efface les choix
   # et retourne les choix classique
   if values[0] not in ['Color', 'Point']:
      return [{'label':name, 'value':name} for name in multiOptionDict.keys()]
   # si valeurs choisie point ou 2 change les options pour seulement elles même 
   if(len(values)>=2 or values[0] == 'Point'):
      return [{'label':value, 'value':value} for value in values]
   # crée les otpions liés au premier choix
   opts = multiOptionDict[values[0]]
   options = [{'label':value, 'value':value} for value in opts]
   options.append({'label':values[0], 'value':values[0]})
   return options


############################# click on multi dropdown submit and map #################################
# quand clique sur visualButton prend en compte les valuers choisie dans
# multiVisualChoice display la map en fonction change aussi les options de
# InfoDropdown et WTDdown pour adapter à la nouvelle map. InfoDropdown 
# correspond à tous les item possible (derpatement/commune: numéro nom) 
# WTDdown correspond au différentes options possible comme point (montre 
# tous les coordonnées des accident dans la zone séléctionné), 
# color (montre le nombre d'accident par zone departements->communes)

# implémentation futur:
# - au clique sur un objet de la map (département/communes/point) change
# les diagramme graphique s'adpterons pour afficher les informations
# correspondant à l'élement cliqué.
# - crée une sorte d'historique pour revenir à la vision précedante sur la map
@app.callback(
   Output('map', 'figure'), 
   Output('MapFocusPie', 'figure'), 
   Output('MapFocusLine', 'figure'), 
   Output('MapFocusPieChoc', 'figure'), 
   Output('InfoDropdown', 'value'),
   Output('InfoDropdown', 'options'),
   Output('WTDdown', 'options'),
   Input('visualButton', 'n_clicks'),
   Input('multiVisualChoice', 'value'),
   Input('map', 'clickData'),
   Input('WTDdown', 'value'),
   Input('WTDrequest', 'n_clicks'),
   State('InfoDropdown', 'value'),
   prevent_initial_call=True
)
def visualMultiFunction(visualButton, multiVisualChoice, map, WTDdownValue, WTDButton, InfoDropdownValue,):
   # récupère le context
   ctx = dash.callback_context
   # si aucun context ne fait rien
   if not ctx.triggered:
      raise PreventUpdate
   # récupère l'id de l'élement cliqué
   button_id = ctx.triggered[0]['prop_id'].split('.')[0]

   # si clique sur WTDdown dropdown 
   if(button_id == 'WTDdown'):
      # si aucune valuers renvoie les valuers par defaut
      if not WTDdownValue:
         return no_update, no_update, no_update, no_update, no_update, no_update, [{'label':'Zoom', 'value':'Zoom'}, {'label':'Focus', 'value':'Focus'}]
      # si la première valuer n'est pas zoom ou focus, return valuers par défault
      if WTDdownValue[0] not in ['Zoom', 'Focus']:
         return no_update, no_update, no_update, no_update, no_update, no_update, [{'label':'Zoom', 'value':'Zoom'}, {'label':'Focus', 'value':'Focus'}]
      # si premiere valuers focus supprime les autre options
      if WTDdownValue[0] == 'Focus':
         return no_update, no_update, no_update, no_update, no_update, no_update, [{'label':'Focus', 'value':'Focus'}]
      # si 2 valeurs ne peut plus en choisir d'autre
      if len(WTDdownValue)>=2:
         return no_update, no_update, no_update, no_update, no_update, no_update, [{'label':value, 'value':value} for value in WTDdownValue]
      # return zoom et autre possibilité
      return no_update, no_update, no_update, no_update, no_update, no_update, [{'label':'Zoom', 'value':'Zoom'}, {'label':'Color', 'value':'Color'}, {'label':'Point', 'value':'Point'}]

   # si l'evenèment correspond au click sur le visualButton        
   if(button_id == 'visualButton'):
      # si il n'y a pas de value ne fait rien
      if not multiVisualChoice:
         raise PreventUpdate
      # si choix point retourne map point
      if multiVisualChoice[0] == 'Point':
         caracteristics = classMap.csv['characteristics']
         caracteristics['type'] = ['commune_point' for string in range(len(caracteristics.index))]
         miny = min(caracteristics.lat) 
         minx = min(caracteristics.long) 
         maxy = max(caracteristics.lat)
         maxx = max(caracteristics.long)
         zoom = -math.sqrt((maxx - minx) * (maxy - miny))*2+11
         return classMap.MakePlotMap(caracteristics, zoom), no_update, no_update, no_update, [], [], []
      # si color est multiVisualChoice inférieur à 2 ne fait rien 
      if len(multiVisualChoice) < 2:
         raise PreventUpdate
      # si choix Department affiche color department
      if(multiVisualChoice[1] == 'Department'):
         optionsInfoDropdown = [{ 'label':classMap.departmentsMapInfo['mergeText'][i], 
                                 'value':classMap.departmentsMapInfo['mergeText'][i]} 
                                 for i in range(classMap.departmentsMapInfo['size'])]
         optionsWTDdown = [{'label':'Zoom', 'value':'Zoom'}, {'label':'Focus', 'value':'Focus'}]
         return classMap.departmentsMap, no_update, no_update, no_update, [], optionsInfoDropdown, optionsWTDdown
      # si choix Commune affiche color commune
      if(multiVisualChoice[1] == 'Commune'):
         optionsInfoDropdown = [{ 'label':classMap.communesMapInfo['mergeText'][i], 
                                 'value':classMap.communesMapInfo['mergeText'][i]} 
                                 for i in range(classMap.communesMapInfo['size'])]
         optionsWTDdown = [{'label':'Zoom', 'value':'Zoom'}, {'label':'Focus', 'value':'Focus'}]
         return classMap.communesMap, no_update, no_update, no_update, [], optionsInfoDropdown, optionsWTDdown

      raise PreventUpdate

   # si clique sur la map
   if(button_id == 'map'):
      print(map)
      # récupère type de n'éléement cliqué
      type = map['points'][0]['customdata'][0]
      # si clique sur un point ne fait rien
      if(type.endswith('_point')): 
         return no_update, no_update, no_update, no_update, map['points'][0]['hovertext'], no_update, no_update
      # séléctionne automatiquement l'élement cliquer
      return no_update, no_update, no_update, no_update, "{} {}".format(map['points'][0]['location'], map['points'][0]['hovertext']), no_update, no_update


   if(button_id == 'WTDrequest'):
      # si aucune valeur 
      if not WTDdownValue or not InfoDropdownValue:
         raise PreventUpdate

      # récupère le code INSEE et le nom
      try:
         location, name = InfoDropdownValue.split(' ')
      except:
         location = InfoDropdownValue
         name = None
      
      # Si choisie focus adapte les graphiques
      if(WTDdownValue[0] == 'Focus'):
         try:
            querry = InfoDropdownValue.split()[0]
            if not querry.endswith('A') and not querry.endswith('B'):
               querry = str(int(querry))

            if len(querry) < 4:
               dataQuery = classMap.allMerged[classMap.allMerged.dep == querry]
            else:
               dataQuery = classMap.allMerged[classMap.allMerged.com == querry]
         except:
            dataQuery = classMap.allMerged[classMap.allMerged.Num_Acc == InfoDropdownValue]

         
         mapFocusPie = px.pie(values=dataQuery.grav.value_counts().values, names=dataQuery.grav.value_counts().index)
         
         mapFocusLine = px.line(dataQuery.mois.value_counts().sort_index(), y="mois")
         mapFocusLine.update_layout(title='Average High and Low Temperatures in New York',
                                    xaxis_title='Month',
                                    yaxis_title='Nombre d\'accident')

                                    
         MapFocusPieChoc = px.pie(values=dataQuery.choc.value_counts(), names=dataQuery.choc.value_counts().index)

         # raise PreventUpdate
         return no_update, mapFocusPie, mapFocusLine, MapFocusPieChoc, no_update, no_update, no_update














         
      elif len(WTDdownValue) < 2:
         raise PreventUpdate
      # Si Zoom point affiche la map point
      elif (WTDdownValue[1] == 'Point'):
         caracteristics = classMap.csv['characteristics']
         if len(str(location)) < 4: 
            caracteristics['type'] = ['department_point' for string in range(len(caracteristics.index))]
         else:
            caracteristics['type'] = ['commune_point' for string in range(len(caracteristics.index))]
         datas = caracteristics.loc[caracteristics.com.astype(str).str.startswith(str(location))]
         optionsInfoDropdown = [{ 'label':datas['Num_Acc'][ind], 
                                 'value':datas['Num_Acc'][ind]} 
                                    for ind in datas.index]
         if datas.empty:
            raise PreventUpdate
         miny = min(datas.lat) 
         minx = min(datas.long) 
         maxy = max(datas.lat)
         maxx = max(datas.long)
         zoom = -math.sqrt((maxx - minx) * (maxy - miny))*2+11
         return classMap.MakePlotMap(datas, zoom), no_update, no_update, no_update, [], optionsInfoDropdown, [{ 'label':'Focus', 'value':'Focus'}]
      
      # sinon color
      else:
         # si len < 4 c'est un departement
         if len(str(location)) < 4:
            accident_com_location = classMap.accident_com.loc[classMap.accident_com.insee_com.astype(str).str.startswith(str(location))]
            communes_location = classMap.geojson['communes'].loc[classMap.geojson['communes'].insee_com.astype(str).str.startswith(str(location))]   
            optionValues = communes_location.loc[:, ['insee_com', 'nom_comm']]
            optionsInfoDropdown = [{ 'label':f"{optionValues['insee_com'][ind]} {optionValues['nom_comm'][ind]}", 
                                    'value':f"{optionValues['insee_com'][ind]} {optionValues['nom_comm'][ind]}"} 
                                    for ind in optionValues.index]
            makeMap = classMap.MakeMap(accident_com_location, communes_location, 
                     "properties.insee_com", "insee_com", 
                     "nom_comm", ["postal_code","nb_accident"], "nb_accident",
                     classMap.GetZoom(communes_location), classMap.GetCenterCoords(classMap.GetAntipodes(communes_location)), 1,
                     {'insee_com':'Code INSEE', 'postal_code':'Code postal', 'nb_accident': 'Nombre d\'accidents'})

            return makeMap, no_update, no_update, no_update, [], optionsInfoDropdown, no_update
         # c'est une commune
         else:
            caracteristics = classMap.csv['characteristics']
            caracteristics['type'] = ['commune_point' for string in range(len(caracteristics.index))]
            datas = caracteristics.loc[caracteristics.com.astype(str).str.startswith(str(location))]
            optionsInfoDropdown = [{ 'label':datas['Num_Acc'][ind], 
                                    'value':datas['Num_Acc'][ind]} 
                                    for ind in datas.index]
            miny = min(datas.lat) 
            minx = min(datas.long) 
            maxy = max(datas.lat)
            maxx = max(datas.long)
            zoom = -math.sqrt((maxx - minx) * (maxy - miny))*2+11
            return classMap.MakePlotMap(datas, zoom), no_update, no_update, no_update, [], optionsInfoDropdown, [{ 'label':'Focus', 'value':'Focus'}]

   raise PreventUpdate

if __name__ == '__main__':
   app.run_server(debug=True)  # Turn off reloader if inside Jupyter
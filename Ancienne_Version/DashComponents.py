# -*- coding: utf-8 -*-
import ClassMap
import math
classMap = ClassMap.ClassMap()

import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
fig = px.scatter(df, x='gdp per capita', y='life expectancy',
                 size='population', color='continent', hover_name='country',
                 log_x=True)

dfTips = px.data.tips()
figHisto = px.histogram(dfTips, x='total_bill')

# figBox = px.box(dfTips, x='day', y='total_bill', color='smoker')
# figBox.update_traces(quartilemethod='exclusive') # or 'inclusive', or 'linear' by default

# figPie = px.pie(dfTips, values='tip', names='day')

# dfCanada = px.data.gapminder().query('country=='Canada'')
# figLine = px.line(dfCanada, x='year', y='lifeExp', title='Life expectancy in Canada')

# figBar = px.bar(dfCanada, x='year', y='pop')

# figBubble = px.scatter(px.data.gapminder().query('year==2007'), x='gdpPercap', y='lifeExp',
# 	                    size='pop', color='continent',
#                         hover_name='country', log_x=True)


# 'Num_Acc', 'jour', 'mois', 'an', 'hrmn', 'lum', 'dep', 'com', 'agg', 'int', 'atm', 'col', 'adr', 'lat', 'long'

multiOptionDict = {'Color': ['Department', 'Commune'], 'Point':None}

df = px.data.tips()

app.layout = html.Div([
    html.H1 ('Application', style={'textAlign': 'center'}), 

    dcc.Graph(id='histoMainGraph'),  
    html.Div([
        dcc.RadioItems(
            options=[
                {'label': 'jour', 'value': 'jour'},
                {'label': 'mois', 'value': 'mois'},
                {'label': 'hrmn', 'value': 'hrmn'},
                {'label': 'rounded', 'value': 'rounded'},
                {'label': 'Lumière', 'value':'lum'},
                {'label': 'Condition Atmo', 'value':'atm'},
                {'label': 'Type de collision', 'value':'col'},

                {'label': 'Catégorie de route', 'value':'catr'},
                {'label': 'Régime de circulation', 'value':'circ'},
                {'label': 'Nombre total de voies de circulation', 'value':'nbv'},
                {'label': 'existence d’une voie réservée', 'value':'vosp'},
                {'label': 'déclivité de la route', 'value':'prof'},
                {'label': 'Tracé en plan', 'value':'plan'},
                {'label': 'Etat de la surface', 'value':'surf'},
                {'label': 'Vitesse maximale autorisée', 'value':'vma'},

                {'label': 'Gravité de blessure', 'value':'grav'},           
                {'label': 'Sexe de l\'usager', 'value':'sexe'}, 
                {'label': 'Année de naissance de l\'usager', 'value':'an_nais'}, 
                {'label': 'Motif du déplacement', 'value':'trajet'}, 
            ],
            value='jour',
            labelStyle={'display': 'inline-block'},
            id='histoValuesParamRadioBtn'
        ),

        dcc.RadioItems(
            options=[
                {'label': 'None', 'value': ''},
                {'label': 'Sexe', 'value': 'sexe'},
            ],
            value='',
            labelStyle={'display': 'inline-block'},
            id='histoColorParamRadioBtn'
        ),

        dcc.RadioItems(
            options=[
                {'label': 'None', 'value': ''},
                {'label': 'Probability', 'value': 'probability'},
                {'label': 'Percent', 'value': 'percent'},
            ],
            value='',
            labelStyle={'display': 'inline-block'},
            id='histohistnormParamRadioBtn'
        ),
    ], style={'columnCount': 3}),
    
    html.Div([
        html.Label('Multi dynamic Dropdown', style={'marginRight': 5}),
        dcc.Dropdown(id='multiVisualChoice',
                options=[{'label':name, 'value':name} for name in multiOptionDict.keys()],
                style={'width':250, 'textAlign':'left'},
                multi=True,
                # persistence=True
                # value=['color']
                ), 
        html.Button('Visualiser', id='visualButton', n_clicks=0, style={'marginLeft': 5}),
        ], style={'display': 'flex', 'justifyContent':'center', 'alignItems':'center'}),   
    dcc.Graph(id='map', figure=fig),     
    html.Div([
        dcc.Dropdown(id='',options=[{'label':'name', 'value':'name'}], style={'width':250, 'textAlign':'left'},), 
        dcc.Dropdown(id='',options=[{'label':'name', 'value':'name'}], style={'width':250, 'textAlign':'left', 'marginLeft':2},), 
        html.Button(id='', n_clicks=0, children='Submit', style={'marginLeft':6}),
        ], style={'display': 'flex', 'justifyContent':'center', 'alignItems':'center'}),
        
    # html.Div([
    #     dcc.Graph(figure=figHisto),
    #     dcc.Graph(figure=figBox),
    #     dcc.Graph(figure=figPie),
    #     dcc.Graph(figure=figLine),
    #     dcc.Graph(figure=figBar),
    #     dcc.Graph(figure=figBubble),
    #     ], style={'columnCount': 3}),

])

@app.callback(
    Output('histoMainGraph', 'figure'),
    [Input('histoValuesParamRadioBtn', 'value'),
     Input('histoColorParamRadioBtn', 'value'),
     Input('histohistnormParamRadioBtn', 'value')],
)
def UpdateHistoMainFigure(ValuesParam, ColorParam, histnormParam):
    if not histnormParam:
        histnormParam = ''
                
    if not ColorParam:
        return px.histogram(classMap.allMerged.loc[:,[ValuesParam]].sort_values(by=[ValuesParam]), x=ValuesParam,  histnorm=histnormParam)
        
    # if values in ['jour','mois', 'hrmn', 'rounded', 'lum', 'atm', 'col']:
    # if values in ['catr', 'circ', 'nbv', 'vosp', 'prof', 'plan', 'surf', 'vma']:
    # if values in ['grav', 'sexe', 'an_nais', 'trajet']:
    
    return px.histogram(classMap.allMerged.loc[:,[ValuesParam, ColorParam]].sort_values(by=[ValuesParam]), x=ValuesParam, color=ColorParam,  histnorm=histnormParam)






@app.callback(
    Output('multiVisualChoice', 'options'),
    Input('multiVisualChoice', 'value'),
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







@app.callback(
    Output('map', 'figure'), 
    Input('visualButton', 'n_clicks'),
    Input('multiVisualChoice', 'value'),
    Input('map', 'clickData')
)
def visualMultiFunction(visualButton, multiVisualChoice, map):
    # récupère le context
    ctx = dash.callback_context
    # si aucun context ne fait rien
    if not ctx.triggered:
        raise PreventUpdate
    # récupère l'id de l'élement cliqué
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # print(button_id)
    # ctx_msg = json.dumps({
    #     'states': ctx.states,
    #     'triggered': ctx.triggered,
    #     'inputs': ctx.inputs
    # }, indent=2)
    # print(ctx_msg,'\n')
    # print(ctx.triggered[0])
    
    # si l'evenèment correspond au click sur le visualButton        
    if(ctx.triggered[0]['prop_id'].split('.')[0] == 'visualButton'):
        values = ctx.inputs['multiVisualChoice.value']
        # si il n'y a pas de value ne fait rien
        if not values:
            raise PreventUpdate
        # si choix point retourne map point
        if values[0] == 'Point':
            return figHisto
        # si color est values inférieur à 2 ne fait rien 
        if len(values) < 2:
            raise PreventUpdate
        # si choix Department affiche color department
        if(values[1] == 'Department'):
            return figHisto
        # affiche color commune
        return figHisto

    # si clique sur la map
    if(ctx.triggered[0]['prop_id'].split('.')[0] == 'map'):
        # affiche les informations de la map
        print(ctx.inputs)
        return figHisto

    raise PreventUpdate
    






if __name__ == '__main__':
    app.run_server(debug=True)
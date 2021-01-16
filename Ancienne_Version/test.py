import pandas as pd
import plotly.express as px
from functools import reduce
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

caracteristiques = pd.read_csv('./csv/accident/caracteristiques-2019.csv', sep=';', decimal=',')
lieux = pd.read_csv('./csv/accident/lieux-2019.csv', sep=';', decimal=',')
usagers = pd.read_csv('./csv/accident/usagers-2019.csv', sep=';', decimal=',')
vehicules = pd.read_csv('./csv/accident/vehicules-2019.csv', sep=';', decimal=',')


data_frames = [caracteristiques, lieux, usagers, vehicules]

df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Num_Acc'], how='outer'), data_frames)


dictLabels= {
    'mois' : {1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Août", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"},
    'lum' : {1:"Plein jour", 2:"Crépuscule ou aube", 3:"Nuit sans éclairage public", 4:"Nuit avec éclairage public non allumé", 5:"Nuit avec éclairage public allumé"},
    'atm' : {-1:"Non renseigné", 1:"Normale", 2:"Pluie légère", 3:"Pluie forte", 4:"Neige - grêle", 5:"Brouillard - fumée", 6:"Vent fort - tempête", 7:"Temps éblouissant", 8:"Temps couvert", 9:"Autre"},
    'col' : {-1 : "Non renseigné", 1:"Deux véhicules - frontale", 2:"Deux véhicules - par l’arrière", 3:"Deux véhicules – par le coté", 4:"Trois véhicules et plus – en chaîne", 5:"Trois véhicules et plus - collisions multiples", 6:"Autre collision", 7:"Sans collision"},
    'catr': {1:"Autoroute", 2:"Route nationale", 3:"Route Départementale", 4:"Voie Communales", 5:"Hors réseau public", 6:"Parc de stationnement ouvert à la circulation publique", 7:"Routes de métropole urbaine", 9:"autre"},
    'circ' : {-1:"Non renseign", 1:"A sens unique", 2:"Bidirectionnelle", 3:"A chaussées séparées", 4:"Avec voies d’affectation variable"},
    'vosp' : {-1:"Non renseigné", 0:"Sans objet ", 1:"Piste cyclable ", 2:"Bande cyclable ", 3:"Voie réservée"},
    'prof' : {-1:"Non renseigné", 1:"Plat ", 2:"Pente", 3:"Sommet de côte", 4:"Bas de côte"},
    'plan' : {-1:"Non renseigné ", 1:"Partie rectiligne ", 2:"En courbe à gauche ", 3:"En courbe à droite", 4:"En « S »"},
    'surf' : {-1:"Non renseigné", 1:"Normale", 2:"Mouillée", 3:"Flaques", 4:"Inondée", 5:"Enneigée", 6:"Boue ", 7:"Verglacée", 8:"Corps gras – huile", 9:"Autre"},
    'grav' : {1:"Indemne", 2:"Tué", 3:"Blessé hospitalisé", 4:"Blessé léger"},
    'sexe' : {1:"Masculin", 2:"Féminin"},
    'trajet' : {-1:"Non renseigné", 0:"Non renseigné", 1:"Domicile – travail",  2:"Domicile – école ", 3:"Courses – achats ", 4:"Utilisation professionnelle ", 5:"Promenade – loisirs ", 9:"Autre"},
}

for label in dictLabels:
    item, data = [], []
    for key, value in dictLabels[label].items():
        item += [key]
        data += [value]
    df_merged.loc[:, label] = df_merged[label].replace(item, data)

# print(df_merged)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
fig = px.scatter(df, x='gdp per capita', y='life expectancy',
                 size='population', color='continent', hover_name='country',
                 log_x=True)

dfTips = px.data.tips()
# print(dfTips)

figBox = px.box(dfTips, x='day', y='total_bill', color='smoker')
figBox.update_traces(quartilemethod='exclusive') # or 'inclusive', or 'linear' by default

figPie = px.pie(df_merged, values='lum', names='mois')

dfCanada = px.data.gapminder().query('country==\'Canada\'')

figLine = px.line(dfCanada, x='year', y='lifeExp', title='Life expectancy in Canada')

figBubble = px.scatter(px.data.gapminder().query('year==2007'), x='gdpPercap', y='lifeExp',
	                    size='pop', color='continent',
                        hover_name='country', log_x=True)

app.layout = html.Div([
    html.Div([
        dcc.Graph(figure=figBox),
        dcc.Graph(figure=figPie),
        dcc.Graph(figure=figLine),
        dcc.Graph(figure=figBubble),
        ], style={'columnCount': 3}),
])

# @app.callback(
#     Output('histoMainGraph', 'figure'),
#     [Input('histoValuesParamRadioBtn', 'value'),
#      Input('histoColorParamRadioBtn', 'value'),
#      Input('histoHistnormParamRadioBtn', 'value'),
#      Input('histoBarmodeParamRadioBtn', 'value')],
# )
# def UpdateHistoMainFigure():
#     return fig

if __name__ == '__main__':
   app.run_server(debug=True)
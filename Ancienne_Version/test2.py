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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1 ('Application', style={'textAlign': 'center'}), 

    dcc.Graph(id='histoMainGraph'),  
    html.Div([
        dcc.RadioItems(
            options=[
                {'label': 'jour', 'value': 'jour'},
                {'label': 'mois', 'value': 'mois'},
                # {'label': 'hrmn', 'value': 'hrmn'},
                {'label': 'rounded', 'value': 'rounded'},
                {'label': 'Luminosité', 'value':'lum'},
                {'label': 'Condition Atmosphérique', 'value':'atm'},
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
            # labelStyle={'display': 'inline-block'},
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
                {'label': 'Nombre', 'value': ''},
                {'label': 'Probability', 'value': 'probability'},
                {'label': 'Percent', 'value': 'percent'},
            ],
            value='percent',
            labelStyle={'display': 'inline-block'},
            id='histoHistnormParamRadioBtn'
        ),

        dcc.RadioItems(
            options=[
                {'label': 'Stack', 'value': 'stack'},
                {'label': 'Group', 'value': 'group'},
                {'label': 'Overlay', 'value': 'overlay'},
            ],
            value='stack',
            labelStyle={'display': 'inline-block'},
            id='histoBarmodeParamRadioBtn'
        ),       
    ], style={'columnCount': 3}),
    
])

@app.callback(
    Output('histoMainGraph', 'figure'),
    [Input('histoValuesParamRadioBtn', 'value'),
     Input('histoColorParamRadioBtn', 'value'),
     Input('histoHistnormParamRadioBtn', 'value'),
     Input('histoBarmodeParamRadioBtn', 'value')],
)
def UpdateHistoMainFigure(valuesParam, colorParam, histnormParam, barmodeParam):
    bargapParam = 0
    if valuesParam == 'sexe' and colorParam == 'sexe':
        raise PreventUpdate    

    if not histnormParam:
        histnormParam = ''
    
    loc = [valuesParam]
    if colorParam:
        loc += [colorParam]

    

    # .where(df_merged[valuesParam] > 0) permet de supprimer les valuers non renseigné
    # try:
    #     dataframe = df_merged.loc[:, loc].sort_values(by=[valuesParam]).where(df_merged[valuesParam] >= 0)
    # except:
    #     dataframe = df_merged.loc[:, loc].sort_values(by=[valuesParam])
    # dataframe = df_merged.loc[:, loc].sort_values(by=[valuesParam])
    dataframe = df_merged.loc[:, loc]
    if not colorParam:
        fig = px.histogram(dataframe, x=valuesParam,  histnorm=histnormParam)
    else:
        fig = px.histogram(dataframe, x=valuesParam, color=colorParam,  histnorm=histnormParam, barmode = barmodeParam, )


    
    if histnormParam == 'percent':
        fig.update_yaxes(ticksuffix="%")
    # facet_col="sexe", 

    if barmodeParam == 'group' and colorParam:
        bargapParam = .1

    fig.update_layout(barmode=barmodeParam)
    fig.update_layout(title_text="Histogramme des accidents",
                      xaxis_title=valuesParam,
                      yaxis_title="Pourcentage d'accident",
                      legend_title=colorParam,
                      bargap=bargapParam
                      )
    
    # if ticktextLabel:
    #     fig.update_xaxes(
    #         tickvals=sorted(pd.unique(df_merged[valuesParam].where(df_merged[valuesParam] > 0)).tolist()),
    #         ticktext=ticktextLabel, 
    #         )



    return fig

if __name__ == '__main__':
   app.run_server(debug=True)
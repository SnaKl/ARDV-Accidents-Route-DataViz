# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.graph_objects as go


# from functools import reduce
# caracteristiques = pd.read_csv('./csv/accident/caracteristiques-2019.csv', sep=';', decimal=',')
# lieux = pd.read_csv('./csv/accident/lieux-2019.csv', sep=';', decimal=',')
# usagers = pd.read_csv('./csv/accident/usagers-2019.csv', sep=';', decimal=',')
# vehicules = pd.read_csv('./csv/accident/vehicules-2019.csv', sep=';', decimal=',')

# data_frames = [caracteristiques, lieux, usagers, vehicules]

# df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Num_Acc'], how='outer'), data_frames)


# labels= {
#    'mois' : {1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Août", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"},
#    'lum' : {1:"Plein jour", 2:"Crépuscule ou aube", 3:"Nuit sans éclairage public", 4:"Nuit avec éclairage public non allumé", 5:"Nuit avec éclairage public allumé"},
#    'atm' : {1:"Non renseign", 1:"Normale", 2:"Pluie légère", 3:"Pluie forte", 4:"Neige - grêle", 5:"Brouillard - fumée", 6:"Vent fort - tempête", 7:"Temps éblouissant", 8:"Temps couvert", 9:"Autre"},
#    'col' : {-1 : "Non renseigné", 1:"Deux véhicules - frontale", 2:"Deux véhicules - par l’arrière", 3:"Deux véhicules – par le coté", 4:"Trois véhicules et plus – en chaîne", 5:"Trois véhicules et plus - collisions multiples", 6:"Autre collision", 7:"Sans collision"},
#    'catr': {1:"Autoroute", 2:"Route nationale", 3:"Route Départementale", 4:"Voie Communales", 5:"Hors réseau public", 6:"Parc de stationnement ouvert à la circulation publique", 7:"Routes de métropole urbaine", 9:"autre"},
#    'circ' : {-1:"Non renseign", 1:"A sens unique", 2:"Bidirectionnelle", 3:"A chaussées séparées", 4:"Avec voies d’affectation variable"},
#    'vosp' : {-1:"Non renseigné", 0:"Sans objet ", 1:"Piste cyclable ", 2:"Bande cyclable ", 3:"Voie réservée"},
#    'prof' : {-1:"Non renseigné", 1:"Plat ", 2:"Pente", 3:"Sommet de côte", 4:"Bas de côte"},
#    'plan' : {-1:"Non renseigné ", 1:"Partie rectiligne ", 2:"En courbe à gauche ", 3:"En courbe à droite", 4:"En « S »"},
#    'surf' : {-1:"Non renseigné", 1:"Normale", 2:"Mouillée", 3:"Flaques", 4:"Inondée", 5:"Enneigée", 6:"Boue ", 7:"Verglacée", 8:"Corps gras – huile", 9:"Autre"},
#    'grav' : {1:"Indemne", 2:"Tué", 3:"Blessé hospitalisé", 4:"Blessé léger"},
#    'sexe' : {1:"Masculin", 2:"Féminin"},
#    'trajet' : {-1:"Non renseigné", 0:"Non renseigné", 1:"Domicile – travail",  2:"Domicile – école ", 3:"Courses – achats ", 4:"Utilisation professionnelle ", 5:"Promenade – loisirs ", 9:"Autre"},
# }

# for label in labels:
#    item, data = [], []
#    for key, value in labels[label].items():
#       item += [key]
#       data += [value]
#    df_merged.loc[:, label] = df_merged[label].replace(item, data)

import ClassMap
classMap = ClassMap.ClassMap()

print(classMap.allMerged)


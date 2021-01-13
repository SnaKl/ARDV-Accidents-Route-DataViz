import geojson
import geopandas as gpd
import pandas as pd
import plotly.express as px
import csv
from shapely.geometry import Polygon
import statistics
import math
from functools import reduce

class ClassMap:
   __raw_departements = gpd.read_file('./geojson/departements.geojson')
   __raw_communes = gpd.read_file('./geojson/communes.geojson')
   geojson = {
      'departments' : __raw_departements, 
      'communes' : __raw_communes,
      }
   # donné brut
   __raw_caracteristiques = pd.read_csv('./csv/accident/caracteristiques-2019.csv', sep=';', decimal=',')
   __raw_lieux = pd.read_csv('./csv/accident/lieux-2019.csv', sep=';', decimal=',')
   __raw_usagers = pd.read_csv('./csv/accident/usagers-2019.csv', sep=';', decimal=',')
   __raw_vehicules = pd.read_csv('./csv/accident/vehicules-2019.csv', sep=';', decimal=',')
   csv = {
      'characteristics' : __raw_caracteristiques,
      'places' : __raw_lieux,
      'users' : __raw_usagers,
      'vehicle' : __raw_vehicules
      }

   #  labels dctionary
   dictLabels= {
      # 'mois' : {1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin", 7:"Juillet", 8:"Août", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"},
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

   def __init__(self):
      # arondis à l'heure près. ex: 02:54 -> 2 
      self.csv['characteristics'] = self.roundedHourCaracte()
      # merged toutes les informations brut grâce au Num_Acc
      self.allMerged = reduce(lambda  left,right: pd.merge(left,right,on=['Num_Acc'], 
                                            how='outer'), [self.__raw_caracteristiques, self.__raw_lieux, self.__raw_usagers, self.__raw_vehicules])
      # remplace toute les valuers par collone dans le dictLabels
      self.replaceLabelsMerged()
      # token necessaire pour la map
      px.set_mapbox_access_token("pk.eyJ1Ijoic25ha2wiLCJhIjoiY2tpeXhqYmQzMWl0NTJ6bno4dzV4amJnayJ9.-qT1chzjLoOM6N1RDv_Zag")
      # récupère les informations des départements et rename 
      self.departmentsInfo = self.__raw_departements.loc[:,~self.__raw_departements.columns.isin(['id', 'geometry'])].rename(columns={'nom_dep0':'nom_dep_maj', 'region0':'region'})
      # nombre d'accident par departement
      self.accident_dep = self.GetAccidentDep()  
      # info par communes
      self.communesInfo = self.__raw_communes.loc[:,~self.__raw_communes.columns.isin(['geometry'])] 
      # nombre d'accident par commune 
      self.accident_com = self.GetAccidentCom()
      # crée la map par défault qui est la map département (toute)
      self.defaultMap = self.departmentsMap = self.MakeMap(self.accident_dep, self.geojson['departments'], 
                                    "properties.insee_dep", "insee_dep", 
                                    "nom_dep", ["insee_dep","nb_accident"], "nb_accident",
                                    1.2, [16.8669662, 7.0432566], 1,
                                    {'insee_dep':'Département', 'nb_accident': 'Nombre d\'accidents'})
      # information sur la map départemnt
      self.departmentsMapInfo = {'hoverText':self.departmentsMap['data'][0]['hovertext'], 
                                 'locations':self.departmentsMap['data'][0]['locations'],
                                 'size': len(self.departmentsMap['data'][0]['hovertext']),
                                 'mergeText':sorted([ f"{self.departmentsMap['data'][0]['locations'][i]} {self.departmentsMap['data'][0]['hovertext'][i]}" 
                                                      for i in range(len(self.departmentsMap['data'][0]['hovertext']))])}
      # crée la map la map commune (toute)
      self.communesMap = self.MakeMap(self.accident_com, self.geojson['communes'], 
                                    "properties.insee_com", "insee_com", 
                                    "nom_comm", ["postal_code","nb_accident"], "nb_accident",
                                    1.2, [16.8669662, 7.0432566], 1,
                                    {'insee_com':'Code INSEE', 'postal_code':'Code postal', 'nb_accident': 'Nombre d\'accidents'})
      # information sur la map commune
      self.communesMapInfo = {'hoverText':self.communesMap['data'][0]['hovertext'], 
                                 'locations':self.communesMap['data'][0]['locations'],
                                 'size': len(self.communesMap['data'][0]['hovertext']),
                                 'mergeText':sorted([ f"{self.communesMap['data'][0]['locations'][i]} {self.communesMap['data'][0]['hovertext'][i]}" 
                                                      for i in range(len(self.communesMap['data'][0]['hovertext']))])}
   
   # arondis à l'heure près. ex: 02:54 -> 2 
   def roundedHourCaracte(self):
      temp = self.csv['characteristics']
      # créer la colonne rounded
      temp['rounded']=""
      # pour chaque heure
      for roudendHour in range(24):
         # pour chaque row
         for ind in temp.index:
            # récupère l'heure (split(':') hh:mm) 
            h = temp['hrmn'][ind].split(':')[0]
            if int(h) == roudendHour:
               temp.loc[[ind] ,'rounded'] = roudendHour
      return temp

   # remplace toutes les valuers des colonnes en fonction de dictLabel
   def replaceLabelsMerged(self):
      for label in self.dictLabels:
         item, data = [], []
         for key, value in self.dictLabels[label].items():
            item += [key]
            data += [value]
         self.allMerged.loc[:, label] = self.allMerged[label].replace(item, data)

   # récupère le nombre d'accident par dépatement
   def GetAccidentDep(self):
      nb_accident_dep = self.__raw_caracteristiques.dep.astype(str).str.zfill(2).value_counts().rename_axis('insee_dep').reset_index(name='nb_accident')
      merge = pd.merge(nb_accident_dep, self.departmentsInfo, on='insee_dep')
      merge['type'] = ['department' for string in range(len(merge.index))]
      return merge
   # récupère le nombre d'accident par commune
   def GetAccidentCom(self):
      accident_communes = self.__raw_caracteristiques.com.value_counts().rename_axis('insee_com').reset_index(name='nb_accident')
      merge = pd.merge(accident_communes, self.communesInfo, on='insee_com')
      merge['type'] = ['commune' for string in range(len(merge.index))]
      # merge = pd.merge(accident_communes, name_communes, how='left', left_on='com', right_on='insee_com')
      return merge

   # récupère toute les coordonées possible des polygones
   def GetAllCoords(self, geoData):
      coords = []
      for geometry in geoData['geometry']:
         if(type(geometry) != Polygon):
            for multiPolygon in geometry:
               coords.append(multiPolygon.exterior.coords.xy)
         else:
            coords.append(geometry.exterior.coords.xy)
      return coords

   # récupère les bornes
   def GetBounds(self, geoData):
      return geoData['geometry'].bounds
   
   # définis automatiquement le zoom de la map fonction de l'aire total de la géométrie à visualiser
   def GetZoom(self, geoData):
      areaSum = sum(geoData['geometry'].area)
      test = -math.sqrt(areaSum)*2.1+9
      return test
   
   # récupère min/max X/Y
   def GetAntipodes(self, geoData):
      bounds = self.GetBounds(geoData)
      minX = statistics.mean(bounds['minx'])
      maxX = statistics.mean(bounds['maxx'])
      minY = statistics.mean(bounds['miny'])
      maxY = statistics.mean(bounds['maxy'])
      return {'minx':minX, 'maxx':maxX, 'miny':minY, 'maxy':maxY}

   # récupère le centre en fonction des antipodes
   def GetCenterCoords(self, antipodes):
      lat = antipodes['minx'] + (antipodes['maxx'] - antipodes['minx'])/2
      lon = antipodes['miny'] + (antipodes['maxy'] - antipodes['miny'])/2
      return [lon, lat]
   
   # récupère l'aire
   def GetArea(self, geoData):
      return geoData['geometry'].area
   
   # return la map color en fonction des paramètres données 
   def MakeMap(self, datas, geoDatas, featureDdKey, location, hoverName, hoverData, dataColor, zoomChoice, coords, opacityChoice, label):
      return px.choropleth_mapbox(datas, geojson=geoDatas, 
                                 featureidkey=featureDdKey, locations=location,
                                 custom_data=['type'],
                                 hover_name =datas[hoverName],
                                 hover_data=[datas[string] for string in hoverData if 1],
                                 color=dataColor, color_continuous_scale="Viridis",
                                 range_color=(min(datas[dataColor]), max(datas[dataColor])),
                                 mapbox_style="carto-positron",
                                 zoom=zoomChoice, center = {"lat": coords[0], "lon": coords[1]},
                                 opacity=opacityChoice,
                                 labels=label,
                              )

   # return la map de points en fonction des paramètres données 
   def MakePlotMap(self, datas, zoomChoice):
      return px.scatter_mapbox(datas,
                              lat=datas.lat,
                              lon=datas.long,
                              custom_data=['type'],
                              hover_name=datas['Num_Acc'],
                              hover_data={'lat':False, 'long':False},
                              zoom=zoomChoice)
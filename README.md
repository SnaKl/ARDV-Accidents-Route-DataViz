# Projet Python

## Présentation

Dans le cadre du cours de Python à ESIEE Paris, troisième année Informatique et Applications, réalisation d'un dashbord codé en python sous Visual Studio Code.<br>
<br>
Présence d'un histogramme et d'une représentation géolocalisée à partir d'un jeu de données téléchargé sur [datagouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2019/#_). Ces fichiers CSV représentent les bases de données annuelles des accidents corporels de la circulation routière (années de 2005 à 2019).<br>
<br>
**Quelles caractéristiques relèvent les facteurs d'accidents de la route en France ?**
<br>
Dans ce cadre, nous avons exploité les données et donnons à l'utilisateur la possibilité de comparer différentes informations entre elles pour mettre en avant les réponses à notre problématique.

> Si le texte est affiché de cette façon c'est qu'une amélioration est envisagée, ou est en cours de développement.

## Rapport d'analyse 

Grâce à la base de données très complète, nous avons pu proposer des facteurs de comparaison très variés (date, luminosité, condition atmosphérique, type de collision... (cf partie facteurs) grâce auxquels nous sommes en mesure d'établir certaines conclusions :
<br>
* Les points de chocs les plus meurtriers sont incontestablements les chocs avant, avec un pourcentage de ??????????. A l'inverse, un choc se produisant au côté gauche de la voiture est le moins critique, avec un taux de ??? %.
* Les mois les plus meurtriers sont Juin et Juillet, il révèlent le plus haut pourcentage de décès de la route (???% pour Juin et ???? pour Juillet). En adéquation avec la période des départs en vacances, nous pouvons facilement en déduire que les accidents se produisent plus fréquemment et à une allure plus meurtrière dans ce contexte. En revanche, il est à noter que le mois d'Août affiche une baisse considérable du taux de décès, et montre alors que les vacanciers sont majoritairement tranquilles et ne prennent certainement pas leur voitures. Le pic d'accident meurtrier reprend de plus belle en septembre, lors du retour de vacances.
* Nous démontrons qu'en prenant compte de tous les types de blessures confondus (indemne, meurtrier, blesser léger etc...), la ville est la zone la plus dangereuse avec un taux de ????% d'accidents.
* La vitesse la plus meurtrière est inconstétablement 80-90 km/h, où ????% de victimes sont décédés contre ???% pour les autres kilométrages allant jusqu'à 150 km/h. La vitesse de 50 km/h en seconde place démontre bien notre précédente constatation et le danger de la ville face aux automobilistes.
* Les femmes ont en moyenne moins d'accidents que les hommes tout au long de leur vie. Cependant, alors que la courbe des accidents d'hommes passés 55 ans se verra baisser, celle des femmes monte à ce moment-là.
<br>
Nous permettons à l'utilisateur de comparer des données très larges, répondant à des questionnements au delà de la problématique générale. Ainsi, nous avons pu relever que les jours les "plus meurtriers" était le 20 et 26, BLABLABLA ...........

## User Guide

### L'installation du programme
#### Pré-requis

Avoir installé le module python sur Visual Studio Code<br>
Avoir installé un gestionnaire de paquet pour python (ici pip)

#### Installer projet via git
Dans Visual Studio Code, clôner le répertoire git : https://github.com/SnaKl/ProjectPython, branche *master*

#### Installer geopandas
`pip install geopandas`

#### Installer plotly

`pip install plotly`<br>
Si une version antérieure est déjà installée : `pip install plotly --upgrade`

#### Installer dash
`pip install dash`

#### Lancement du dashboard
Il ne reste plus qu'à lancer le programme (run)<br>
<br>
Il est à noter que le lancement du dashboard est **très lent**, dû à toutes les données chargées, une bonne dizaine de minutes est à prévoir (temps variable en fonction de l'appareil sur lequel est lancé le programme). Le fait de charger tous le dashboard dès son lancement permet ainsi à l'utilisateur d'effectuer des traitements et comparaisons de données dans un temps quasi instantanné par la suite.

### Les fonctionnalités du Dashboard

Le dashboard se compose de trois grandes parties :

#### Histogramme général des accidents de la route

   Cet histogramme permet de manipuler toutes les données des CSV et de les comparer en fonction de facteurs sélectionnés. Il est indépendant des autres parties du dashboard et représente toutes les données confondues (tous les lieux de France).<br>
   <br>Des options situées **sous l'histogramme** permettent de modifier les paramètres d'affichage des données (empilés, groupés, recouverts) et la façon dont elles sont comparées (en nombre, probabilité ou pourcentage). <br>
   <br>Un filtre du facteur sélectionné se trouve **à droite** de l'histogramme, il permet de retirer les éléments souhaités.
   <br>
   
#### Carte des accidents et ses diagrammes
   C'est une carte intéractive centrée sur la France mais avec laquelle on peut accéder aux autres pays du monde afin de respecter les données d'accidents des DOM TOM.
   <br>
   <br>Un filtre situé **au dessus** de la map permet de choisir si on souhaite afficher la carte selon les départements ou les communes. On peut aussi choisir d'afficher les résultats en focus ou par zoom. Ce dernier paramètre permet d'afficher la zone sélectionnée plus précisémment et ainsi afficher jusqu'aux petits points représentant les accidents. 
   > Un filtre par région est en cours de développement.
   Une graduation présente sur **la droite de la carte** indique le nombre d'accident par département en fonction de la couleur.<br>
   <br>
   **Au survol** des départements, on nous indique le nombre d'accidents comptabilisé dans cette zone.<br>
   <br>
   Sous la carte, on retrouve trois diagrammes dépendants de la sélection sur cette dernière :
   * Un diagramme circulaire représentant le nombre d'accident par type de choc (indemne, blessé léger, tué etc...)
   * Une courbe du nombre d'accident par mois dans la zone
   * Un diagramme circulaire du pourcentage du nombre d'accident par point de choc (arrière, avant, côtés etc...)

#### Les facteurs proposés


#### Ses fonctionnalités

## Developper Guide

### Le dossier CSV
La base de données complète représente 11 fichiers CSV, répartis en deux dossiers :<br>

  * **accident**
    * *caractéristiques-2019.csv* : circonstances générales de l'accident
    * *lieux-2019.csv* : lieu principal de l'accident
    * *usagers-2019.csv* : les usagers impliqués dans l'accident (conducteur, passagers, passants etc...)
    * *vehicules-2019.csv* : les véhicules impliqués dans l'accident
    <br>
Le document PDF *description-des-bases-de-donnees-onisr-annees-2005-a-2019.pdf* donne une description complète des différentes tabs des CSV, un atout majeur pour avoir une vue d'ensemble sur les différents facteurs pouvant être rajoutés dans le dashboard.<br>
    
 * Le document CSV *correspondance-code-insee-code-postal*, provenant de [datagouv.fr](https://www.data.gouv.fr/fr/datasets/correspondance-code-insee-code-postal/) assure la correspondance entre les codes postaux et les documents GeoJSON.
 
### Les documents geojson


 
 ### Le dossier geojson

Le format GeoJSON permet de décrire des données de type de point et d'y ajouter des attributs d'information qui ne sont pas spatiales.
Ainsi, les fichiers geojson *communes.geojson*, *departements.geojson* et *regions.geojson* ont pour but


> ligne de code

##Titre <a name="facteurs"></a>

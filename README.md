# Projet Python

## Présentation

Dans le cadre du cours de Python à ESIEE Paris, troisième année Informatique et Applications, réalisation d'un dashbord codé en python sous Visual Studio Code.<br>
<br>
Présence d'un histogramme et d'une représentation géolocalisée à partir d'un jeu de données téléchargé sur [datagouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2019/#_). Ces fichiers CSV représentent les bases de données **annuelle 2019** des accidents corporels de la circulation routière.<br>
<br>
***Quelles caractéristiques relèvent les facteurs d'accidents de la route en France ?***
<br>
Dans ce cadre, nous avons exploité les données et donnons à l'utilisateur la possibilité de comparer différentes informations entre elles pour mettre en avant les réponses à notre problématique.

> Si le texte est affiché de cette façon c'est qu'une amélioration est envisagée, ou est en cours de développement.

## Rapport d'analyse 

Grâce à la base de données très complète, nous avons pu proposer des facteurs de comparaison très variés (date, luminosité, condition atmosphérique, type de collision... (cf partie facteurs) grâce auxquels nous sommes en mesure d'établir certaines conclusions :
<br>
* Les points de chocs les plus meurtriers sont incontestablements les chocs avant, avec un pourcentage de 35,7 %. A l'inverse, un choc se produisant à l'arrière droit de la voiture est le moins critique, avec un taux de 1,88 %.
* Les mois les plus meurtriers sont Juin et Juillet, il révèlent le plus haut pourcentage de décès de la route (9,6% pour Juin et 9,8% pour Juillet). En adéquation avec la période des départs en vacances, nous pouvons facilement en déduire que les accidents se produisent plus fréquemment et à une allure plus meurtrière dans ce contexte. En revanche, il est à noter que le mois d'Août affiche une baisse considérable du taux de décès, et montre alors que les vacanciers sont majoritairement tranquilles et ne prennent certainement pas leur voitures. Le pic d'accident meurtrier reprend de plus belle en septembre, lors du retour de vacances.
* Nous démontrons qu'en prenant compte de tous les types de blessures confondus (indemne, meurtrier, blesser léger etc...), la ville est la zone la plus dangereuse avec un taux de 51,5 % d'accidents.
* La vitesse la plus meurtrière est inconstétablement 80-90 km/h, où 44,4% de victimes sont décédés contre 4,7% en moyenne pour les autres kilométrages allant jusqu'à 150 km/h. La vitesse de 50 km/h en seconde place démontre bien notre précédente constatation et le danger de la ville face aux automobilistes.
* Les femmes ont en moyenne moins d'accidents que les hommes tout au long de leur vie. Cependant, passé 56 ans, la probabilité pour une femme d'avoir un accident est plus forte que celle d'un homme.
<br>
Nous permettons à l'utilisateur de comparer des données très larges, répondant à des questionnements au delà de la problématique générale. Ainsi, nous avons pu relever que les jours les "plus meurtriers" était le 20 et 26; que le taux de mortalité est plus élevé de jour que de nuit; la pluie légère provoque plus d'accidents que les autres conditions atmosphériques (neige, pluies fortes, etc...); il y a plus d'accidents dans les trajets de type loisirs / promenades que lors de trajet professionnel ou autre.

## User Guide

### L'installation du programme
#### Pré-requis

Avoir installé le module python sur Visual Studio Code<br>
Avoir installé l'utilitaire python Anaconda3
Avoir installé un gestionnaire de paquet pour python (ici nous utilisons **Conda**)

#### Installer projet via git
Dans Visual Studio Code, clôner le répertoire git : https://github.com/SnaKl/ProjectPython, branche *master*

#### Installer geopandas
`conda install geopandas`

#### Installer plotly

`conda install plotly`<br>
Si une version antérieure est déjà installée : `conda install plotly --upgrade`

#### Installer dash
`conda install dash`

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
   
##### Les facteurs de comparaison proposés
   * Jour
   * Mois  
   * Heures
   * Luminosité
   * Condition Atmosphérique
   * Type de collision
   * Catégorie de route
   * Régime de circulation
   * Nombre total de voies de circulation
   * Existence d’une voie réservée
   * Déclivité de la route
   * Tracé en plan
   * Etat de la surface
   * Vitesse maximale autorisée
   * Gravité de blessure
   * Sexe de l'usager
   * Année de naissance de l'usager
   * Motif du déplacement
   * Point de choc initial
   * Système de sécurité
   
   > Le programme a été codé de manière très évolutif, il est ainsi facile de rajouter un facteur (il doit être présent parmis la liste du document *description-des-bases-de-donnees-onisr-annees-2005-a-2019.pdf*)
   
#### Carte des accidents et ses diagrammes
   C'est une carte intéractive centrée sur la France mais avec laquelle on peut accéder aux autres pays du monde afin de respecter les données d'accidents des DOM TOM.
   <br>
   <br>Un filtre situé **au dessus** de la map permet de choisir si on souhaite afficher la carte selon les départements ou les communes. On peut aussi choisir d'afficher les résultats en focus ou par zoom. Ce dernier paramètre permet d'afficher la zone sélectionnée plus précisémment et ainsi afficher jusqu'aux petits points représentant les accidents. 
   > L'ajout d'un filtre par région est en cours de développement.
   > Un historique de recherche permettant de revenir rapidement sur la dernière zone ciblée sans repasser par les filtres est en projet.
   
   Une graduation présente sur **la droite de la carte** indique le nombre d'accident par département en fonction de la couleur.<br>
   <br>
   > Une autre graduation colorant les zones en fonction du taux d'accident mortel est en cours de projet.
   
   **Au survol** des départements, on nous indique le nombre d'accidents comptabilisé dans cette zone.<br>
   <br>
   
##### Diagrammes par régions
Sous la carte, on retrouve trois diagrammes pouvant être mis à jour en fonction de la zone cliquée sur la carte :
   * Un diagramme circulaire représentant le nombre d'accident par type de choc (indemne, blessé léger, tué etc...)
   * Une courbe du nombre d'accident par mois dans la zone
   * Un diagramme circulaire du pourcentage du nombre d'accident par point de choc (arrière, avant, côtés etc...)
   <br>
   Ces diagrammes possèdent eux aussi leurs propres filtres, permettant ainsi de sélectionner une zone et un mode d'affichage sans forcément passer par la carte.
   > Projet de comparaison entre deux régions / communes / départements en cours
   <br>
   <br>
   > Une troisième partie constituée d'un autre histogramme similaire à la première partie est en projet. Il aurait la même fonctionnalité mais spécifique à la zone choisie sur la carte.


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
Les documents *communes.geojson* et *departements.geojson* sont utilisés pour instancier les données de la map. Ils sont reliés aux données des autres CSV via le numéro de département que l'on retrouve sur le document *correspondance-code-insee-code-postal*.  
> Le fichier *regions.geojson* sera prochainement utilisé pour l'ajout de la fonctionnalité de filtre par régions.

### Le fichier process_module.py

Fichier contenant le code de la classe ClassMap générant tous le dashboard. Cela cause une lenteur au démarrage du programme mais permet ainsi de minimiser les processus une fois le dashboard lancé. L'utilisateur peut alors utiliser les fonctionnalités quasi-instantanément.<br>
Cette classe rend le code très évolutif, en effet il est facile de rajouter des map ou des diagrammes qui seront générés automatiquement par la classe avec les bons paramètres.
> De plus, un des projet futur pour le dashboard est l'ajout des données 2020 ainsi qu'un déploiement des résultats au niveau mondial, la classe permettra une telle évolution.


### Le fichier main.py

Fichier appelant la méthode class et assurant la gestion de l'affichage du dashboard.
Il contient les conditions permettant de :
* afficher les données souhaitées lors d'un clic sur un radio bouton, une zone de la carte, un filtre etc...
* permettre la sélection multiples de filtres et assurer l'affichage pertinant des choix suivants
* détecte le type de zone que l'utilisateur sélectionne sur la map

### Les erreurs de données
Les fichiers CSV téléchargés possèdent quelques erreurs comprenant notamment :
- des accidents répertoriés en plein océan
- des usagers pouvant atteindre un âge de 115 ans
- un kilométrage variant jusqu'à 800 km/h

# Projet Python

## Présentation

Dans le cadre du cours de Python à ESIEE Paris, troisième année Informatique et Applications, réalisation d'un dashbord codé en python sous Visual Studio Code.<br>
<br>
Présence d'un histogramme et d'une représentation géolocalisée à partir d'un jeu de données téléchargé sur [datagouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2019/#_). Ces fichiers CSV représentent les bases de données annuelles des accidents corporels de la circulation routière (Années de 2005 à 2019).<br>
<br>
Dans ce cadre, nous exploiterons les données dans le but de répondre à cette problématique : **???????????????????????????????????**

## Rapport d'analyse 

## User Guide

### Pré-requis

Avoir installé le module python sur Visual Studio Code<br>
Avoir installé un gestionnaire de paquet pour python (ici pip)

### Installer projet via git
Dans Visual Studio Code, clôner le répertoire git : https://github.com/SnaKl/ProjectPython, branche *master*

### Installer geopandas
`pip install geopandas`

### Installer plotly

`pip install plotly`<br>
Si une version antérieure est déjà installée : `pip install plotly --upgrade`

### Installer dash
`pip install dash`

### Précision
Il est à noter que le lancement du dashboard est **très lent**, dû à toutes les données chargées. Une bonne dizaine de minutes est à prévoir. 

## Developper Guide

### Le dossier CSV
La base de données complète représente 11 fichiers CSV, répartis en deux dossiers :<br>

  * **accident**
    * *caractéristiques-2019.csv* : circonstances générales de l'accident
    * *lieux-2019.csv* : lieu principal de l'accident
    * *usagers-2019.csv* : les usagers impliqués dans l'accident (conducteur, passagers, passants etc...)
    * *vehicules-2019.csv* : les véhicules impliqués dans l'accident
    
  * **insee**
    * *arrondissement2020.csv*
    * *canton2020.csv*
    * *communes2020.csv*
    * *departement2020.csv*
    * *mvtcommune2020.csv*
    * *pays2020.csv*
    * *region2020.csv*
    
Le document CSV *correspondance-code-insee-code-postal* assure 

> ligne de code


# Optimisation d’une tournée en Californie

Le scénario part de Los Angeles, visite dix autres villes et revient au point de départ. Le programme compare la méthode du plus proche voisin à une tournée améliorée par 2-opt.

## Données

Le fichier locations.csv contient onze noms et coordonnées extraits du [fichier 2014_us_cities.csv de Plotly](https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv). La provenance primaire et une licence propre à ce fichier ne sont pas précisées dans le CSV.

## Exécution

Depuis le dossier du projet, lancer `python fetch_data.py` pour extraire les coordonnées du CSV source. Lancer ensuite `python route.py` avec Python 3. Après récupération des données, le calcul fonctionne hors ligne. Ouvrir `tours.svg` dans un navigateur et survoler les points pour lire les noms.

Le programme vérifie que chaque ville est visitée une seule fois, que les deux tournées reviennent au départ et que 2-opt ne dégrade pas la distance. Les distances sont à vol d’oiseau. Le scénario ne représente pas des livraisons observées.


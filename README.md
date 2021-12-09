# ecoco2_test
Eco CO2 technical test

## Test instructions
- Récupérer les données de taux de CO2 en France pour les années 2017 et 2018 à partir de l'API décrite ici https://api-recrutement.ecoco2.com/docs/#tag/v1
- Stocker dans une table django.
- Filtrer les données pour produire une deuxième table avec une fréquence horaire.
- À partir de la table horaire, interpoler les résultats pour (re)obtenir la même fréquence initiale de 30 minutes.
- Afficher les 20 derniers points dans un tableau avec la différence entre la vraie donnée et la donnée interpolée.
- Pour chaque donnée (réelle et interpolée), rajouter une ligne au tableau avec la moyenne pour les jours ouvrés, et les weekends.
- Bonus: Ajouter un graphe de la différence entre les deux données.

## Implementation choices
- **Django + Postgresql** database: I debated using a database dedicated to time series or JSON data such as TimescaleDB or MongoDB,
    but considering the limited amount of data handled for the test I will store the hourly and 30min data sets in JSONField format
    on a default Postgres database.
- **Pandas** for data handling, filtering and interpolation: it is possible and maybe worth it to perform the data processing at the 
    database level for larger datasets, but the ease of implementation provided by Pandas is hard to match in this use case.
- **Docker** containers for database and Django services.

## Usage
From the project root directory:
1. Build and start Docker services
```
docker-compose up
```
2. Run initial migration and populate database
```
virtualenv .venv
source .venv/bin/activate
python manage.py migrate
python manage.py populate_db
```
3. Navigate to table and chart pages
http://localhost:8000/table
http://localhost:8000/chart

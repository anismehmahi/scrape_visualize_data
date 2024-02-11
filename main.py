import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta

# Chemin vers le répertoire contenant les fichiers CSV
csv_directory = "./meteoData/"

# Informations d'authentification MongoDB
mongo_username = 'mohamedaminebentayeb'
mongo_password = 'amine09'
mongo_host = 'localhost'
mongo_port = 27017
mongo_database = 'meteo_data'
mongo_collection = 'summary'

# Colonnes à inclure dans l'analyse
included_variables = ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms', 'msl_pressure:hPa']

# Connexion à la base de données MongoDB avec les informations d'authentification
client = MongoClient(f'mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_database}')
db = client[mongo_database]
collection = db[mongo_collection]

# Fonction pour résumer les données et les enregistrer dans MongoDB
def summarize_and_store():
    # Lire tous les fichiers CSV dans le répertoire
    all_files = os.listdir(csv_directory)
    csv_files = [file for file in all_files if file.endswith(".csv")]

    # Créer un DataFrame vide pour stocker toutes les données
    all_data = pd.DataFrame()

    # Lire chaque fichier CSV et concaténer les données en incluant uniquement les variables spécifiées
    for csv_file in csv_files:
        file_path = os.path.join(csv_directory, csv_file)
        df = pd.read_csv(file_path, usecols=included_variables, delimiter=';')
        all_data = pd.concat([all_data, df], ignore_index=True)

        # Afficher les colonnes du fichier
        print(f"Colonnes du fichier {csv_file} : {df.columns.tolist()}")

    # Résumer les données en incluant plusieurs statistiques descriptives
    summary_data = all_data.describe().transpose()

    # Convertir le résultat en dictionnaire pour l'insertion dans MongoDB
    summary_dict = summary_data.to_dict()

    # Ajouter une clé pour la date du résumé
    summary_dict['summary_date'] = datetime.utcnow()

    # Insérer les données résumées dans MongoDB
    collection.insert_one(summary_dict)

    # Supprimer les fichiers résumés
    for csv_file in csv_files:
        file_path = os.path.join(csv_directory, csv_file)
        os.remove(file_path)

    print("Données résumées enregistrées dans MongoDB et fichiers résumés supprimés.")

# Appeler la fonction pour résumer et stocker les données
summarize_and_store()

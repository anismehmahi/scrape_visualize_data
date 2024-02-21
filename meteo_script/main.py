import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timedelta
import json

# Chemin vers le répertoire contenant les fichiers JSON
json_directory = "./meteoData/"

# Informations d'authentification MongoDB
# mongo_username = 'mohamedaminebentayeb'
# mongo_password = 'amine09'
mongo_host = 'localhost'
mongo_port = 27017
mongo_database = 'meteo_data'
mongo_collection = 'summary'

# Colonnes à inclure dans l'analyse
included_variables = ['t_2m:C', 'precip_1h:mm', 'wind_speed_10m:ms', 'msl_pressure:hPa']

# Connexion à la base de données MongoDB avec les informations d'authentification
client = MongoClient(f"mongodb://localhost:27017/")
db = client[mongo_database]
collection = db[mongo_collection]
def process_weather_data(data):
    data = data.get("data", []) 
    # Créer des DataFrames pour chaque variable
    df_t_2m = pd.DataFrame(columns=["validdate", "t_2m:C"])
    df_precip_1h = pd.DataFrame(columns=["validdate", "precip_1h:mm"])
    df_wind_speed_10m = pd.DataFrame(columns=["validdate", "wind_speed_10m:ms"])
    df_msl_pressure = pd.DataFrame(columns=["validdate", "msl_pressure:hPa"])

    

    # Iterate through each parameter in the data
    for parameter_data in data:
        parameter = parameter_data['parameter']
        coordinates = parameter_data['coordinates'][0]
        dates = coordinates['dates']

        for date_data in dates:
            date_str = date_data['date']
            value = date_data['value']

            # Ajouter les valeurs dans le DataFrame approprié en fonction du paramètre
            if parameter == 't_2m:C':
                df_t_2m = df_t_2m.append({"validdate": date_str, "t_2m:C": value}, ignore_index=True)
            elif parameter == 'precip_1h:mm':
                df_precip_1h = df_precip_1h.append({"validdate": date_str, "precip_1h:mm": value}, ignore_index=True)
            elif parameter == 'wind_speed_10m:ms':
                df_wind_speed_10m = df_wind_speed_10m.append({"validdate": date_str, "wind_speed_10m:ms": value}, ignore_index=True)
            elif parameter == 'msl_pressure:hPa':
                df_msl_pressure = df_msl_pressure.append({"validdate": date_str, "msl_pressure:hPa": value}, ignore_index=True)

    # Fusionner les DataFrames en fonction de la colonne "validdate"
    merged_df = df_t_2m.merge(df_msl_pressure, on="validdate").merge(df_precip_1h, on="validdate").merge(df_wind_speed_10m, on="validdate")
    #commpare between df_t_2m and df_msl_pressure validdate
    merged_df["msl_pressure:hPa"]=merged_df["msl_pressure:hPa"].astype(float)
   
    return merged_df
# Fonction pour résumer les données et les enregistrer dans MongoDB
def summarize_and_store():
    # Lire tous les fichiers JSON dans le répertoire
    all_files = os.listdir(json_directory)
    json_files = [file for file in all_files if file.endswith(".json")]

    # Créer un dictionnaire vide pour stocker toutes les données
    all_data = []

    # Lire chaque fichier JSON et ajouter les données au dictionnaire
    for json_file in json_files:
        file_path = os.path.join(json_directory, json_file)
        with open(file_path, 'r') as f:
            data = json.load(f)
            collection_data=process_weather_data(data)
            #describe collection_data
            description=collection_data.describe().transpose()
            print(description)
            #convertir le résultat en dictionnaire pour l'insertion dans MongoDB
            description_dict=description.to_dict()
            #ajouter une clé pour la date du résumé
            description_dict['summary_date']=datetime.utcnow()
            #insérer les données résumées dans MongoDB
            collection.insert_one(description_dict)
            
        # Afficher les clés du fichier
        print(f"Clés du fichier {json_file} : {list(data.keys())}")

    # Supprimer les fichiers résumés
    for json_file in json_files:
        file_path = os.path.join(json_directory, json_file)
        os.remove(file_path)

    print("Données résumées enregistrées dans MongoDB et fichiers résumés supprimés.")

# Appeler la fonction pour résumer et stocker les données
summarize_and_store()
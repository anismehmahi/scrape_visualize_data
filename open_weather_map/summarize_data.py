import os
import json
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['open_weather_data']
collection = db['open_weather_summary']

# Parcourir les fichiers JSON dans le répertoire
directory = './downloaded_data'
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)
            summary_data = {
                'ville': data['name'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'description': data['weather'][0]['description'],
                'pression': data['main']['pressure'],
                'humidite': data['main']['humidity']
            }
            # Insérer le résumé dans la base de données MongoDB
            collection.insert_one(summary_data)
        # Supprimer le fichier une fois traité
        os.remove(filepath)

# Déconnexion de la base de données MongoDB
client.close()

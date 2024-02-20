import os
import json
import pymongo
from datetime import datetime, timedelta
import requests

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["earthquake_db"]
collection = db["summaries"]
processed_files_collection = db["processed_files"]

# Répertoire des données
data_dir = "./downloaded_data/"

# Parcourir les fichiers du répertoire
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(data_dir, filename)
        if processed_files_collection.count_documents({"filename": filename}) == 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
                earthquake_list = data.get("features", [])
                for earthquake in earthquake_list:
                    summary = {
                        "id": earthquake.get("id"),
                        "adresse": earthquake["properties"].get("place"),
                        "mag":earthquake["properties"].get("mag"),
                        #"timestamp":earthquake["properties"].get("time")
                                            }
                    
                    detail_url = earthquake["properties"].get("detail")
                    if detail_url:
                        try:
                            response = requests.get(detail_url)
                            if response.status_code == 200:
                                detail_data = response.json()
                                products_origin = detail_data['properties']['products']['origin'][0]['properties']
                                
                                summary.update({
                                
                                    "depth": products_origin.get("depth"),
                                    "latitude": products_origin.get("latitude"),
                                    "longitude": products_origin.get("longitude"),
                                    "num_phases_used": products_origin.get("num-phases-used"),
                                    "num_stations_used": products_origin.get("num-stations-used"),
                                    "origin_source": products_origin.get("origin-source"),
                                    "timestamp": products_origin.get("eventtime")
                                })
                        except requests.RequestException as e:
                            print(f"Failed to retrieve details for earthquake {summary['id']}: {e}")
                    
                    # Utiliser update_one avec upsert=True pour insérer ou mettre à jour
                    collection.update_one({"id": summary['id']}, {"$set": summary}, upsert=True)
            # Après traitement, marquer le fichier comme traité
            processed_files_collection.insert_one({"filename": filename})

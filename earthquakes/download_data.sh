#!/bin/bash

# Répertoire de stockage
DIR="./downloaded_data"

# Vérifier si le répertoire existe, sinon le créer
if [ ! -d "$DIR" ]; then
  mkdir -p "$DIR"
fi

# Nom du fichier avec date et heure
FILENAME="earthquake_data_$(date +'%Y-%m-%d_%H-%M').json"

# URL de l'API pour les données des dernières 60 minutes
URL="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

# Téléchargement des données
curl -s "$URL" > "$DIR/$FILENAME"


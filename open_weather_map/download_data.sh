#!/bin/bash

# Répertoire de stockage
DIR="./downloaded_data"

# Vérifier si le répertoire existe, sinon le créer
if [ ! -d "$DIR" ]; then
  mkdir -p "$DIR"
fi

# Clé API OpenWeatherMap
API_KEY="f3a737596b79879689106917005ad24e"

# Ville à interroger
VILLE="Paris"

# Appel à l'API OpenWeatherMap pour les données météorologiques actuelles de la ville spécifiée
curl -s "http://api.openweathermap.org/data/2.5/weather?q=$VILLE&appid=$API_KEY&units=metric" > "$DIR/$VILLE-$(date +'%Y-%m-%d_%H-%M-%S').json"

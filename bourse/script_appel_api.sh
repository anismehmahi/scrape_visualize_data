#!/bin/bash

# Créer un dossier s'il n'existe pas
dossier="./data"
if [ ! -d "$dossier" ]; then
    mkdir -p "$dossier"
fi

API_KEY="9M1N8QJKC7TYZNIS"
SYMBOLS=("AAPL" "GOOGL" "MSFT")
ENDPOINT="TIME_SERIES_INTRADAY"
INTERVAL="5min"

# Parcourir chaque symbole boursier
for SYMBOL in "${SYMBOLS[@]}"; do
    # Effectuer la requête API et enregistrer la réponse dans un fichier
    curl -s "https://www.alphavantage.co/query?function=${ENDPOINT}&symbol=${SYMBOL}&interval=${INTERVAL}&apikey=${API_KEY}" > "${SYMBOL}_data_$(date +\%Y-\%m-\%d_\%H-\%M-\%S).json"
    
    # Vérifier si la requête a réussi
    if [ $? -eq 0 ]; then
        echo "La requête pour ${SYMBOL} a réussi."
    else
        echo "La requête pour ${SYMBOL} a échoué."
    fi
done

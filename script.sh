#!/bin/bash

api_url='https://api.meteomatics.com'
username='universitpariscit_bentayeb_mohamedamine'
password='q2RZ6k6ssX'

# Calculer le temps de fin comme le temps actuel en UTC
end_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Calculer le temps de début comme 3 jours avant le temps de fin
start_time=$(date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%SZ")

# Mettre en forme les temps dans le format requis pour l'URL de l'API
api_url="${api_url}/${start_time}--${end_time}:PT1H/t_2m:C,precip_1h:mm,wind_speed_10m:ms,msl_pressure:hPa/52.520551,13.461804/csv"
echo "${api_url}"

# Créer un nom de fichier basé sur la date et l'heure de téléchargement
output_filename="./meteoData/meteomatics_data_$(date -u +"%Y%m%d_%H%M%S").csv"

# Effectuer la demande avec curl en utilisant l'authentification de base et en stockant les résultats dans le fichier
curl --user "${username}:${password}" "${api_url}" > "${output_filename}"

# Vérifier si la demande a réussi (code d'état 200)
if [ $? -eq 0 ]; then
    echo "Les données ont été téléchargées avec succès dans ${output_filename}"
else
    echo "Erreur: Impossible de récupérer les données. Code d'état: ${status_code}"
fi

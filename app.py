import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px

def afficher_graphiques(data):
    for variable, values in data.items():
        fig = px.box(x=[variable], y=list(values.values()), labels={variable: variable})
        fig.show()

# Connexion à la base de données MongoDB
mongo_username = 'mohamedaminebentayeb'
mongo_password = 'amine09'
mongo_host = 'localhost'
mongo_port = 27017
mongo_database = 'meteo_data'
mongo_collection = 'summary'

client = MongoClient(f'mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_database}')
db = client[mongo_database]
collection = db[mongo_collection]

# Récupérer la liste des dates disponibles dans la collection
dates_list = [entry['summary_date'] for entry in collection.find({}, {'summary_date': 1})]

# Sélectionner une date à afficher
selected_date = st.selectbox('Sélectionner une date', dates_list)

# Récupérer les données associées à la date sélectionnée
selected_data = collection.find_one({'summary_date': selected_date})

# Afficher les statistiques
st.write(f"Statistiques pour la date : {selected_date}")


# Remplacer les noms de variables par des noms significatifs dans la variable data
data = {
    "Température (°C)": {
        "min": selected_data["min"]["t_2m:C"],
        "max": selected_data["max"]["t_2m:C"],
        "std": selected_data["std"]["t_2m:C"],
        "mean": selected_data["mean"]["t_2m:C"],
    },
    "Précipitations (mm)": {
        "min": selected_data["min"]["precip_1h:mm"],
        "max": selected_data["max"]["precip_1h:mm"],
        "std": selected_data["std"]["precip_1h:mm"],
        "mean": selected_data["mean"]["precip_1h:mm"],
    },
    "Vitesse du vent (m/s)": {
        "min": selected_data["min"]["wind_speed_10m:ms"],
        "max": selected_data["max"]["wind_speed_10m:ms"],
        "std": selected_data["std"]["wind_speed_10m:ms"],
        "mean": selected_data["mean"]["wind_speed_10m:ms"],
    },
    "Pression au niveau de la mer (hPa)": {
        "min": selected_data["min"]["msl_pressure:hPa"],
        "max": selected_data["max"]["msl_pressure:hPa"],
        "std": selected_data["std"]["msl_pressure:hPa"],
        "mean": selected_data["mean"]["msl_pressure:hPa"],
    },
}


def afficher_graphiques(data):
    for variable, values in data.items():
        # Créer un box plot avec Plotly Express
        fig = px.box(y=list(values.values()), labels={variable: variable})
        
        # Ajouter des titres et libellés
        fig.update_layout(
            title=f"Statistiques pour {variable}",
            xaxis_title=variable,
            yaxis_title="Valeurs",
        )

        # Afficher le graphique
        st.plotly_chart(fig)

afficher_graphiques(data)

import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
mongo_database = 'meteo_data'

# Function to fetch Meteo data
def fetch_meteo_data(selected_date):
    db = client[mongo_database]
    collection = db['summary']
    return collection.find_one({'summary_date': selected_date})

# Function to fetch Earthquake data
def fetch_earthquake_data():
    # Assuming earthquake data is stored in a similar manner but in a different collection/database
    db = client['earthquake_data']  # Update with your actual database name
    collection = db['earthquakes']  # Update with your actual collection name
    return pd.DataFrame(list(collection.find()))  # Convert the MongoDB cursor to a DataFrame

# Function to display Meteo statistics and charts
def display_meteo_tab():
    collection = client[mongo_database]['summary']
    dates_list = [entry['summary_date'] for entry in collection.find({}, {'summary_date': 1})]
    selected_date = st.selectbox('Select a date', dates_list)
    selected_data = fetch_meteo_data(selected_date)

    st.write(f"Statistics for the date: {selected_date}")
    data = {
        "Temperature (°C)": {
            "min": selected_data["min"]["t_2m:C"],
            "max": selected_data["max"]["t_2m:C"],
            "std": selected_data["std"]["t_2m:C"],
            "mean": selected_data["mean"]["t_2m:C"],
        },
        "Precipitations (mm)": {
            "min": selected_data["min"]["precip_1h:mm"],
            "max": selected_data["max"]["precip_1h:mm"],
            "std": selected_data["std"]["precip_1h:mm"],
            "mean": selected_data["mean"]["precip_1h:mm"],
        },
        # Add other variables as needed
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

    for variable, values in data.items():
        fig = px.box(y=list(values.values()), labels={"value": variable})
        fig.update_layout(title=f"Statistics for {variable}", yaxis_title="Values")
        st.plotly_chart(fig)

# Function to display Earthquake data and charts
def display_earthquake_tab():
    earthquake_data = fetch_earthquake_data()
    if not earthquake_data.empty:
        st.write("Earthquake Data Overview")
        # Display earthquake data or charts here
        # Example: st.write(earthquake_data.head())
    else:
        st.write("No earthquake data available.")

# Main app structure
def main():
    st.sidebar.title("Data Selection")
    app_mode = st.sidebar.selectbox("Choose the data you want to view:", ["Meteo", "Earthquakes"])

    if app_mode == "Meteo":
        display_meteo_tab()
    elif app_mode == "Earthquakes":
        display_earthquake_tab()
if __name__ == "__main__":
    main()

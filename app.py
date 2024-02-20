import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import colorsys

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
mongo_database = 'meteo_data'
def lighten_color(color, amount):
  """
  Lightens a given color by a specified amount (0-1).
  """
  try:
    h, l, s = colorsys.rgb_to_hls(*color)
    l = (l + amount) % 1
    return colorsys.hls_to_rgb(h, l, s)
  except (TypeError, ValueError):
    # Handle potential errors with color input
    return color
# Function to fetch Meteo data
def fetch_meteo_data(selected_date):
    db = client[mongo_database]
    collection = db['summary']
    return collection.find_one({'summary_date': selected_date})

# Function to fetch Earthquake data
def fetch_earthquake_data():
    # Assuming earthquake data is stored in a similar manner but in a different collection/database
    db = client['earthquake_db']  # Update with your actual database name
    collection = db['summaries']  # Update with your actual collection name
    return pd.DataFrame(list(collection.find()))  # Convert the MongoDB cursor to a DataFrame

# Function to display Meteo statistics and charts
def display_meteo_tab():
    collection = client[mongo_database]['summary']
    dates_list = [entry['summary_date'] for entry in collection.find({}, {'summary_date': 1})]
    selected_date = st.sidebar.selectbox('Select a date', dates_list,index=0)
    selected_data = fetch_meteo_data(selected_date)
    # Utiliser une boîte de sélection pour choisir le type de visualisation
    visualization_type = st.sidebar.selectbox("Choose Visualization Type", ["Histogram","Table", "Boxplot"] )


 # Format the date string for better readability
    if isinstance(selected_date, str):
                formatted_date = datetime.strptime(selected_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
    else:
                formatted_date = selected_date.strftime("%Y-%m-%d %H:%M:%S")
    st.title(f"Statistics for the date: {formatted_date}")
  # Extracting additional information (25%, 50%, 75%) for each variable
    data = {
    "Temperature (°C)": {
        "min": selected_data["min"]["t_2m:C"],
        "max": selected_data["max"]["t_2m:C"],
        "std": selected_data["std"]["t_2m:C"],
        "mean": selected_data["mean"]["t_2m:C"],
        "25%": selected_data["25%"]["t_2m:C"],
        "50%": selected_data["50%"]["t_2m:C"],
        "75%": selected_data["75%"]["t_2m:C"],
    },
    "Precipitations (mm)": {
        "min": selected_data["min"]["precip_1h:mm"],
        "max": selected_data["max"]["precip_1h:mm"],
        "std": selected_data["std"]["precip_1h:mm"],
        "mean": selected_data["mean"]["precip_1h:mm"],
        "25%": selected_data["25%"]["precip_1h:mm"],
        "50%": selected_data["50%"]["precip_1h:mm"],
        "75%": selected_data["75%"]["precip_1h:mm"],
    },
    "Vitesse du vent (m/s)": {
        "min": selected_data["min"]["wind_speed_10m:ms"],
        "max": selected_data["max"]["wind_speed_10m:ms"],
        "std": selected_data["std"]["wind_speed_10m:ms"],
        "mean": selected_data["mean"]["wind_speed_10m:ms"],
        "25%": selected_data["25%"]["wind_speed_10m:ms"],
        "50%": selected_data["50%"]["wind_speed_10m:ms"],
        "75%": selected_data["75%"]["wind_speed_10m:ms"],
    },
    "Pression au niveau de la mer (hPa)": {
        "min": selected_data["min"]["msl_pressure:hPa"],
        "max": selected_data["max"]["msl_pressure:hPa"],
        "std": selected_data["std"]["msl_pressure:hPa"],
        "mean": selected_data["mean"]["msl_pressure:hPa"],
        "25%": selected_data["25%"]["msl_pressure:hPa"],
        "50%": selected_data["50%"]["msl_pressure:hPa"],
        "75%": selected_data["75%"]["msl_pressure:hPa"],
    },
}

    if visualization_type == "Boxplot":
        for variable, values in data.items():
            fig = px.box(y=list(values.values()), labels={"value": variable})
            fig.update_layout(title=f"Statistics for {variable}", yaxis_title="Values")
            st.plotly_chart(fig)

    elif visualization_type == "Histogram":
        bar_names = ['min', '25%', 'mean', '75%', 'max']
       

        for variable, values in data.items():
            if values:
                data_values = [values[stat] for stat in bar_names]

                # Create a figure with the specified colors
                fig = go.Figure(layout_template='plotly_white')  # Optional: Set a white background
                for stat, value in zip(bar_names, data_values):
                    
                    stat_label = f'{stat} (Zero)' if value == 0 else stat
                    color = "Blue" if value != 0 else "Red"
                    fig.add_trace(go.Bar(x=[stat_label], y=[value], name=f'{stat}', marker_color=color))

                # Add spacing and layout
                fig.update_layout(
                    title=f"Distribution of {variable}",
                    xaxis_title="Statistics",
                    yaxis_title="Values",
                    barmode='group',
                    bargap=0.2
                )
                st.plotly_chart(fig)
            else:
                st.warning(f"No data available for {variable}")



    elif visualization_type == "Table":
        for variable, values in data.items():
            # Créer un tableau HTML pour chaque variable
            html_table = """
            <table>
                <tr>
                    <th>Variable</th>
                    <th>Minimum</th>
                    <th>25%</th>
                    <th>Moyenne</th>
                    <th>75%</th>
                    <th>Maximum</th>
                    <th>Ecart-type</th>
                </tr>
            """
            html_table += f"""
            <tr>
                <td>{variable}</td>
                <td>{values["min"]}</td>
                <td>{values["25%"]}</td>
                <td>{values["mean"]}</td>
                <td>{values["75%"]}</td>
                <td>{values["max"]}</td>
                <td>{values["std"]}</td>
            </tr>
            """
            html_table += "</table>"
            st.header(variable)

            # Afficher le tableau HTML
            st.write(html_table, unsafe_allow_html=True)


# Helper function to convert timestamp to a Python datetime object
def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

# Function to fetch filtered Earthquake data
def fetch_filtered_earthquake_data(region=None, start_date=None, end_date=None):
    db = client['earthquake_db']  # Update with your actual database name
    collection = db['summaries']  # Update with your actual collection name
    query = {}
    
    if region:
        query["adresse"] = {"$regex": region, "$options": "i"}  # Case-insensitive match
    
    if start_date and end_date:
        query["timestamp"] = {"$gte": start_date.isoformat(), "$lte": end_date.isoformat()}
    
    earthquakes = list(collection.find(query))
    for eq in earthquakes:
        # print(eq)
        eq["timestamp"] = parse_timestamp(eq["timestamp"])
    
    return pd.DataFrame(earthquakes)


def get_unique_regions():
    db = client['earthquake_db']  # Update with your actual database name
    collection = db['summaries']  # Update with your actual collection name
    # Get unique 'adresse' entries and extract the region part
    addresses = collection.distinct('adresse')
    regions = set(address.split(', ')[-1] for address in addresses if ', ' in address)  # Extract region after the comma
    return list(regions)

# Enhanced function to display Earthquake data on an interactive map
def display_earthquake_tab():
    st.title("Earthquake Data Visualization")
     # Get unique regions for the sidebar selection
    unique_regions = get_unique_regions()
    unique_regions.insert(0, 'All regions')  # Add 'All regions' as the first option
    selected_region = st.sidebar.selectbox("Select a region", unique_regions, index=0)  # Default to 'All regions'

    region =selected_region
    start_date = st.sidebar.date_input("Start date", value=None)
    end_date = st.sidebar.date_input("End date", value=None)

    # If 'All regions' is not selected, filter by the selected region
    if selected_region != 'All regions':
        earthquake_data = fetch_filtered_earthquake_data(selected_region, start_date, end_date)
    else:
        earthquake_data = fetch_filtered_earthquake_data(None, start_date, end_date)

    if not earthquake_data.empty:
        if ((start_date==None) and (end_date==None)):
            st.write(f"Displaying earthquakes for : {region}") 
        elif ((start_date!=None) and (end_date==None)):
            st.write(f"Displaying earthquakes for region: {region} from {start_date}") 
        elif ((start_date==None) and (end_date!=None)):
            passt.write(f"Displaying earthquakes for region: {region} until {end_date}")
        else:
            st.write(f"Displaying earthquakes for region: {region} from {start_date} to {end_date}")

        

        # Ensure latitude and longitude are numeric for plotting
        earthquake_data["latitude"] = pd.to_numeric(earthquake_data["latitude"])
        earthquake_data["longitude"] = pd.to_numeric(earthquake_data["longitude"])
        earthquake_data["depth"] = pd.to_numeric(earthquake_data["depth"])
        earthquake_data["mag"] = pd.to_numeric(earthquake_data["mag"])
        

        fig = px.scatter_mapbox(earthquake_data, lat="latitude", lon="longitude",
                         hover_name="adresse", hover_data=["mag", "depth"],
                         color="mag", size="mag",
                         color_continuous_scale=["green", "yellow", "red"],
                         size_max=15,  height=600)  # Adjusted zoom level for a broader view

        # Update layout to use OpenStreetMap and remove margins
        fig.update_layout(
            mapbox_style="open-street-map",
            width=1100,
            margin={"r":0,"t":0,"l":0,"b":0},
            mapbox=dict(
                center=dict(lat=0, lon=0),  # Center on the Equator and Prime Meridian
                zoom=1.5  # Adjust zoom level as needed
            )
        )

        # Display the map in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("No earthquake data available for the selected filters.")



# Main app structure
def main():
    st.set_page_config(page_title="Real Time Dashboard", page_icon=':star', layout='wide')


    st.sidebar.title("Data Selection")
    # Ajouter 2 tabs de ilyes et mazigh
    app_mode = st.sidebar.selectbox("Choose the data you want to view:", [ "Meteo","Earthquakes", ])


    # ici aussi
    if app_mode == "Meteo":
        display_meteo_tab()
    elif app_mode == "Earthquakes":
        display_earthquake_tab()
if __name__ == "__main__":

    main()






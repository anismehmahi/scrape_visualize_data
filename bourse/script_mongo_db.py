import os
import json
from pymongo import MongoClient
from datetime import datetime, timedelta

# Connection to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['donnees_bourse']
collection = db['resume_donnees_bourse']

# Directory where JSON files are stored
data_directory = "./data_projet"

# Get a list of JSON files in the directory
json_files = [f for f in os.listdir(data_directory) if f.endswith('.json')]

# Define the interval for summarization (1 hour in this example)
summarization_interval = timedelta(hours=24)

# Current date and time
now = datetime.now()

stock_names = {
    "AAPL": "Apple",
    "GOOGL": "Google",
    "MSFT": "Microsoft",
    # Add more symbols and names as needed
}

# Iterate over each JSON file
for json_file in json_files:
    file_path = os.path.join(data_directory, json_file)
    
    # Check the last modification time of the file
    last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    
    # Check if the file has been modified within the specified interval
    if now - last_modified_time <= summarization_interval:
        # Load JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract relevant information and store each timestamp in MongoDB
        time_series = data.get('Time Series (60min)', {})
        symbol = data['Meta Data']['2. Symbol']
        stock_name = f"{symbol} ({stock_names.get(symbol, symbol)})"
        
        for timestamp, entry in time_series.items():
            entry['stock_name'] = stock_name
            entry['timestamp'] = timestamp
            entry['timestamp_stored'] = now
            collection.insert_one(entry)
        
        # Remove the file after storing timestamps
        os.remove(file_path)
        print(f"Timestamps from file {json_file} stored and file removed.")

# Disconnect from MongoDB
client.close()
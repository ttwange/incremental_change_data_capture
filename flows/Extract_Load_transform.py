import os
import requests
import pandas as pd
import json

def get_asset_data(url: str) -> pd.DataFrame:
    """Get asset data from CoinCap API and save it as a CSV file."""
    # Send a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_data = response.json()
        data = json_data["data"]
        
        # Create a DataFrame
        df = pd.DataFrame(data)
        
        # Define the path to save the CSV file
        asset_data_folder = 'asset_data'
        csv_file_path = os.path.join(asset_data_folder, 'asset-data.csv')
        
        # Ensure the 'asset_data' folder exists
        if not os.path.exists(asset_data_folder):
            os.makedirs(asset_data_folder)
        
        # Save the DataFrame as a CSV file in the 'asset_data' folder
        df.to_csv(csv_file_path, index=False)
        
        return df
    else:
        # Handle the case when the request fails
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

# Define the URL to fetch data from
url = "http://api.coincap.io/v2/assets"

# Call the function and print the DataFrame
print(get_asset_data(url))

def transform_asset(df: int) -> pd.DataFrame:
    """Transform raw asset data into cleaned format for further analysis."""
    # Clean the data: Replace None values with appropriate defaults (e.g., 0)
    df.fillna(0, inplace=True)

    # Convert numeric columns to appropriate data types
    numeric_columns = ["supply", "maxSupply", "marketCapUsd", "volumeUsd24Hr", "priceUsd", "changePercent24Hr", "vwap24Hr"]
    df[numeric_columns] = df[numeric_columns].astype(float)

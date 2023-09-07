import os
import json
import requests
import pandas as pd
from prefect import task, flow
from sqlalchemy import create_engine

@task()
def get_asset_data(url: str, csv_file_path: str) -> str:
    """Get asset data from CoinCap API and save it as a CSV file."""
    
    response = requests.get(url)
    
    if response.status_code == 200:
        
        json_data = response.json()
        data = json_data["data"]

        df = pd.DataFrame(data)
        
        # Ensure the 'asset_data' folder exists
        if not os.path.exists(os.path.dirname(csv_file_path)):
            os.makedirs(os.path.dirname(csv_file_path))
        
        # Save the DataFrame as a CSV file in the specified path
        df.to_csv(csv_file_path, index=False)
        
        # Return the CSV file path
        return csv_file_path
    else:
        # Handle the case when the request fails
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None
    
@task()
def transform_asset(csv_file_path: str) -> pd.DataFrame:
    """Transform raw asset data into cleaned format for further analysis."""
    # Load data from the csv file into a dataframe
    df = pd.read_csv(csv_file_path)
    
    # Clean the data: Replace None values with appropriate defaults (e.g., 0)
    df.fillna(0, inplace=True)

    # Convert numeric columns to appropriate data types
    numeric_columns = ["supply", "maxSupply", "marketCapUsd", "volumeUsd24Hr", "priceUsd", "changePercent24Hr", "vwap24Hr"]

    df[numeric_columns] = df[numeric_columns].astype(float)

    df = df.drop('explorer', axis=1)

    print(df.dtypes)
    return df
    
@task
def load_postgres(df):
    """Loads data into PostgreSQL database using SQLAlchemy ORM"""
    # Define the PostgreSQL database connection URL
    db_url = 'postgresql://docker:docker@localhost:5431/exampledb'
       
    # Create an SQLAlchemy engine to connect to the database
    engine = create_engine(db_url)
    pd.io.sql.get_schema(df, name='asset', con=engine)
    # Use the to_sql method to insert the DataFrame into the 'asset' table
    df.to_sql(name='asset', con=engine, if_exists='append', index=False)  # Set index=False to avoid saving DataFrame index
    
    # Print a message to indicate that the data upload is complete
    print("Data upload complete")


@flow()
def Extract_Load_transform() -> None:
    # Define the URL to fetch data from
    url = "http://api.coincap.io/v2/assets"
    
    # Define the path to save 
    csv_file_path = "./asset_data/asset-data.csv"
    
    df = get_asset_data(url, csv_file_path)
    df_csv = transform_asset(df)
    load_postgres(df_csv)

if __name__ == "__main__":
    Extract_Load_transform()

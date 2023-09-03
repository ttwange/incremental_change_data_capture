import json
import requests
import pandas as pd

url = "http://api.coincap.io/v2/assets"


def get_asset_data(url: str) -> pd.DataFrame:
  """Get asset data from CoinCap API."""
  payload = {}
  headers = {}
  response = requests.request("GET",url, headers=headers, data=payload)
  json_data = json.loads(response.text.encode('utf8'))
  asset_data = json_data["data"]

  df = pd.DataFrame(asset_data)
  df.to_csv('asset-data.csv',index=False)
  #return df
  print(df)



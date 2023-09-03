import requests
import json


url = "http://api.coincap.io/v2/assets"
payload = {}
headers = {}

response = requests.request("GET",url, headers=headers, data=payload)
json_data = json.loads(response.text.encode('utf8'))

asset_data = json_data["data"]

import pandas as pd
df = pd.DataFrame(asset_data)
df.to_csv('asset-data.csv',index=False)

print(df)
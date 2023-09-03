import requests
import json
import pandas as pd
from python_whatsapp_bot import Whatsapp

response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")

json_response = response.json()
string_response = json.dumps(json_response, indent=2)

df = pd.DataFrame.from_dict(json_response, orient="index")
df["str-date-time"] = df.apply(lambda row: f"{row.date} {row.hour.split('-')[0]}", axis=1)
df["date-time"] = pd.to_datetime(df["str-date-time"], format='%d-%m-%Y %H')
df = df.drop(columns=['str-date-time', 'date', 'hour'])

print(df)

# wa_bot = Whatsapp('636718231', string_response)

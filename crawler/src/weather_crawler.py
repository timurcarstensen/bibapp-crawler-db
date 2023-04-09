# standard library imports
import os

# third party imports
import pandas as pd
from datetime import date, datetime
import mysql.connector

response = pd.read_json(
    "https://api.weatherapi.com/v1/current.json?key=63c572bf2bda4bf4946152445210710&q=Mannheim&aqi=no"
)

df = pd.DataFrame(response)
df.drop(df.columns[[0]], axis=1, inplace=True)
drop_cols = [
    "name",
    "region",
    "country",
    "lat",
    "lon",
    "tz_id",
    "localtime_epoch",
    "localtime",
    "last_updated_epoch",
    "precip_mm",
    "precip_in",
    "vis_km",
    "vis_miles",
    "wind_mph",
    "temp_f",
    "feelslike_f",
    "gust_mph",
]
df.drop(drop_cols, axis=0, inplace=True)


date = datetime.now().replace(second=0, microsecond=0)
timestamp = str(date).replace(":", "-")
dict = df.to_dict()
last_updated = dict["current"]["last_updated"]
temp_c = dict["current"]["temp_c"]
is_day = dict["current"]["is_day"]
weather_condition = dict["current"]["condition"]["text"]
wind_kph = dict["current"]["wind_kph"]
wind_degree = dict["current"]["wind_degree"]
wind_dir = dict["current"]["wind_dir"]
pressure_mb = dict["current"]["pressure_mb"]
pressure_in = dict["current"]["pressure_in"]
humidity = dict["current"]["humidity"]
cloud = dict["current"]["cloud"]
feelslike_c = dict["current"]["feelslike_c"]
uv = dict["current"]["uv"]
gust_kph = dict["current"]["gust_kph"]


cnx = mysql.connector.connect(
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_ROOT_PASSWORD"),
    host="dm-1-db",
    port=os.getenv("MYSQL_PORT"),
    database=os.getenv("MYSQL_DATABASE"),
)

cursor = cnx.cursor()

features = (
    "(last_updated, "
    "temp_c, "
    "is_day, "
    "weather_condition, "
    "wind_kph, "
    "wind_degree, "
    "pressure_mb, "
    "pressure_in, "
    "humidity, "
    "cloud, "
    "feelslike_c, "
    "uv, "
    "gust_kph)"
)
# noinspection SqlNoDataSourceInspection
query = f"INSERT INTO weather_data {features} VALUES (%s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


data = (
    timestamp,
    last_updated,
    temp_c,
    is_day,
    weather_condition,
    wind_kph,
    wind_degree,
    wind_dir,
    pressure_mb,
    pressure_in,
    humidity,
    cloud,
    feelslike_c,
    uv,
    gust_kph,
)
cursor.execute(query, data)
cnx.commit()


cursor.close()
cnx.close()

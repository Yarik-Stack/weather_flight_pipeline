import os
import pandas as pd
from dotenv import load_dotenv

#-------------------------------- LOADING VARIABLES FROM .env FILE -------------

def load_env_vars():
    load_dotenv()
    return {
        'DB_NAME': os.getenv('db_schema'),
        'DB_HOST': os.getenv('db_host'),
        'DB_USER': os.getenv('db_user'),
        'DB_PASSWORD': os.getenv('db_password'),
        'DB_PORT': os.getenv('db_port'),
        'WEATHER_API_KEY': os.getenv('weather_api_key'),
        'AERODATABOX_API_KEY': os.getenv('aerodatabox_api_key')
    }

#----------------------------- MERGING TABLES ----------------------------------
def table_concat(cities_df, weather_df, airport_df):
    merged_df = pd.merge(cities_df, airport_df, on='city_id', how='left')
    merged_df = pd.concat([merged_df, weather_df], axis=1)
    return merged_df
#-------------------------------------------------------------------------------


#------------------------- DIVIDING ONE TABLE INTO TWO -------------------------
def table_division(merged_df):
    cities_names_df = merged_df[['city_id', 'city', 'longitude', 'latitude', 'temperature', 'weather', 'description', 'airport_name', 'icao_code', 'iata_code', 'date']].drop_duplicates()
    city_info_df = merged_df[['city_id', 'country', 'population', 'date']]
    return cities_names_df, city_info_df
#-------------------------------------------------------------------------------


#----------------------- APPENDING TO SQL DATABASE -----------------------------
def db_appending(engine, cities_names_df, city_info_df):
    with engine.begin() as conn:
        cities_names_df.to_sql('cities', con=conn, if_exists='append', index=False)
        city_info_df.to_sql('city_info', con=conn, if_exists='append', index=False)

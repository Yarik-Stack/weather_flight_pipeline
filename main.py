
#----------------------------- LIBRARIES IMPORT --------------------------------
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from datetime import datetime
from lat_lon_parser import parse 
from sqlalchemy import create_engine
from sqlalchemy import text
from pytz import timezone
from datetime import datetime, timedelta

#------------------------------ FUNCTIONS IMPORT -------------------------------

from db_connection import database_connection
from cities_parser import get_cities, get_city_info, data_collection
from weather import get_weather, weather_apply
from flights import get_flight_info, get_arrival_flights
from utils import load_env_vars, table_concat, table_division, db_appending

#----------------------------- FUNCTION INITIATION -----------------------------
def app_init():
    env = load_env_vars()
    db = database_connection()
    cities = get_cities()
    cities_df = data_collection(cities) #------------ get_city_info is inside --
#-------------------------- API's ----------------------------------------------
    weather_df = weather_apply(cities_df, env['WEATHER_API_KEY'])
    airport_df = get_flight_info(cities_df)
    flights_df = get_arrival_flights(airport_df)
#---------------------- TABLES MERGING -----------------------------------------
    merged_df = table_concat(cities_df, weather_df, airport_df)
    cities_names_df, city_info_df = table_division(merged_df)
    db_appending(db['engine'], cities_names_df, city_info_df)
    if not flights_df.empty:
        flights_df.to_sql('flights', con=db['engine'], if_exists='append', index=False)
        print(f"Saved {len(flights_df)} flight records to 'flights' table.")
    else:
        print('No flight data to save.')

#---------------------------- FUNCTION INITIALIZATION --------------------------

if __name__ == "__main__":
    load_dotenv()
    app_init()


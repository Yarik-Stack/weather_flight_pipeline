import requests
import os
from datetime import datetime, timedelta
import pandas as pd
from pytz import timezone

#---------------------------- AIRPORT DATA FUNCTION ----------------------------
def get_flight_info(cities_df):

    icao_codes = []
    iata_codes = []
    city_ids = []
    airport_name = []

    for index, row in cities_df.iterrows():
        latitude = row['latitude']
        longitude = row['longitude']

#---------- API CALL ----------
        url = 'https://aerodatabox.p.rapidapi.com/airports/search/location'
        querystring = {'lat':latitude,'lon':longitude,'radiusKm':'50','limit':'10','withFlightInfoOnly':'true'}
        headers = {
            'X-RapidAPI-Host': 'aerodatabox.p.rapidapi.com',
            'X-RapidAPI-Key': os.getenv('aerodatabox_api_key')
        }
        response = requests.request('GET', url, headers=headers, params=querystring)
        if response.status_code == 200:
            airport_json = response.json()
            for item in airport_json.get('items', []):
                icao_codes.append(item['icao'])
                iata_codes.append(item['iata'])
                airport_name.append(item['name'])
                city_ids.append(row['city_id'])
        else:
            print(f"Error for city {row['city']}: {response.status_code}, {response.text}")

    airport_df = pd.DataFrame({'icao_code': icao_codes,'iata_code': iata_codes, 'airport_name': airport_name, 'city_id': city_ids})
    return airport_df

def get_arrival_flights(airport_df):
    berlin_timezone = timezone('Europe/Berlin')
    today = datetime.now(berlin_timezone).date()
    tomorrow = today + timedelta(days=1)

    time_ranges = [["00:00", "11:59"], ["12:00", "23:59"]]
    flight_items = []

    api_key = os.getenv("aerodatabox_api_key")

    for _, row in airport_df.iterrows():
        icao = row['icao_code']
        for start_time, end_time in time_ranges:
            url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao}/{tomorrow}T{start_time}/{tomorrow}T{end_time}"
            querystring = {
                "withLeg": "true",
                "direction": "Arrival",
                "withCancelled": "false",
                "withCodeshared": "true",
                "withCargo": "false",
                "withPrivate": "false"
            }
            headers = {
                'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
                'x-rapidapi-key': api_key
            }

            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                flights_json = response.json()
                retrieval_time = datetime.now(berlin_timezone).strftime("%Y-%m-%d %H:%M:%S")

                for item in flights_json.get("arrivals", []):
                    flight_item = {
                        "arrival_airport_icao": icao,
                        "departure_airport_icao": item["departure"]["airport"].get("icao", None),
                        "scheduled_arrival_time": item["arrival"]["scheduledTime"].get("local", None),
                        "flight_number": item.get("number", None),
                        "timestamp_flight": retrieval_time
                    }
                    flight_items.append(flight_item)
            else:
                print(f"Error fetching data for ICAO {icao}: {response.status_code} - {response.text}")

    df = pd.DataFrame(flight_items)

    if not df.empty:
        df["scheduled_arrival_time"] = df["scheduled_arrival_time"].str[:-6]  # remove timezone info
        df["scheduled_arrival_time"] = pd.to_datetime(df["scheduled_arrival_time"])
        df["timestamp_flight"] = pd.to_datetime(df["timestamp_flight"])
        df = df.drop_duplicates()
    print(df)
    return df
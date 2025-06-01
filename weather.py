import requests
import pandas as pd

#-------------------------- WEATHER COLLECTING FUNCTION ------------------------
def get_weather(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    responce = requests.get(url)
    if responce.status_code ==200:
        weather = responce.json()
        return {
            'temperature': weather['list'][0]['main']['temp'],
            'weather': weather['list'][0]['weather'][0]['main'],
            'description': weather['list'][0]['weather'][0]['description']
        }
    else:
        return {
            'temperature': None, 'weather': None, 'description': None
        }
    
#---------- Applying data to every city ----------
def weather_apply(cities_df, api_key):
    weather_data = []
    for _, row in cities_df.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        weather = get_weather(lat, lon, api_key)
        weather_data.append(weather)
    weather_df = pd.DataFrame(weather_data)
    return weather_df
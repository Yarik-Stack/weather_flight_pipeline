import pandas as pd
from bs4 import BeautifulSoup
import requests
from lat_lon_parser import parse 
from datetime import datetime, timedelta

#--------------------------- WIKIPEDIA PARSING FUNCTION ------------------------

#------------------------- Cities and their Wikipedia URLs ---------------------
def get_cities():
    return {
    'Berlin': 'https://en.wikipedia.org/wiki/Berlin',
    'Hamburg': 'https://en.wikipedia.org/wiki/Hamburg',
    'Munich': 'https://en.wikipedia.org/wiki/Munich',
    'Dresden': 'https://en.wikipedia.org/wiki/Dresden'
    }

def get_city_info(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    country = None
    city_info = soup.find('table', class_='infobox')
    if city_info:
        for row in city_info.find_all('tr'):
            header = row.find('th')
            if header and 'Country' in header.text:
                td = row.find('td')
                if td:
                    country = td.text.strip()
                break

    try:
        population = soup.find(string="Population").find_next("td").get_text()
        population = population.replace(",", "").strip()
    except AttributeError:
        population = None

    try:
        latitude = parse(soup.find('span', class_='latitude').text.strip())
        longitude = parse(soup.find('span', class_='longitude').text.strip()) 
    except Exception as e:
        print("Coordinates parsing error", e)
        latitude = None
        longitude = None

    return {
        'country': country,
        'latitude': latitude,
        'longitude': longitude,
        'population': population,
    }

#----------------------------- City data collection ----------------------------
def data_collection(cities):
    data = []
    for index, (city, url) in enumerate(cities.items()):
        info = get_city_info(url)
        info['city'] = city
        info['city_id'] = index
        # print(info) 
        data.append(info)

    cities_df = pd.DataFrame(data)
    cities_df['population'] = pd.to_numeric(cities_df['population'], errors='coerce')
    cities_df['date'] = datetime.today().date()
    # print(cities_df)
    return cities_df
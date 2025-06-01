from cities_parser import get_cities, data_collection
from weather import weather_apply
from utils import load_env_vars


def test_weather():
    env = load_env_vars()
    cities = get_cities()
    cities_df = data_collection(cities)
    weather_df = weather_apply(cities_df, env["WEATHER_API_KEY"])
    print(weather_df.head())

if __name__ == "__main__":

    test_weather()

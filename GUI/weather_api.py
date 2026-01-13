import requests

API_KEY = "8d5e56909da60b64202440e959885ab7"
CITY = "Ho Chi Minh"

URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

def get_current_weather():
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(URL_CURRENT, params=params)
    return response.json()

def get_hourly_forecast():
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(URL_FORECAST, params=params)
    return response.json()

from weather_api import get_current_weather

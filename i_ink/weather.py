import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OWM_API_KEY = os.getenv("OWM_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"


def fetch_hourly_forecast(lat, lon):
    if not OWM_API_KEY:
        raise RuntimeError("OpenWeatherMap API key not set in .env")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OWM_API_KEY
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def extract_short_term_forecast(data, hours=3):
    results = []
    for hour in data.get("hourly", [])[:hours]:
        timestamp = datetime.utcfromtimestamp(hour["dt"])
        temp = round(hour["temp"])
        clouds = hour.get("clouds", 0)
        pop = int(hour.get("pop", 0) * 100)  # convert to %
        results.append((timestamp, temp, clouds, pop))
    return results


def format_forecast_entry(entry):
    timestamp, temp, clouds, pop = entry
    return f"{timestamp}: {temp}°C, Clouds: {clouds}%, Rain Probability: {pop}%"


def get_short_term_forecast(lat, lon, hours=3):
    data = fetch_hourly_forecast(lat, lon)
    short_term_forecast = extract_short_term_forecast(data, hours)
    return [format_forecast_entry(entry) for entry in short_term_forecast]

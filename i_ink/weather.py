import requests
import zoneinfo 
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://192.168.1.129:8080/data"


def fetch_forecast():
    print(f"Fetching weather... ({BASE_URL})")
    response = requests.get(BASE_URL, timeout=10)
    print("Fetched.")
    response.raise_for_status()
    return response.json()

"""
def extract_short_term_forecast(data, hours=6):
    results = []
    for hour in data.get("hourly", [])[:hours]:
        hour_ts = datetime.fromtimestamp(hour["dt"], timezone.utc)

        temp_c = round(hour["temp"] - 273.15)
        feels_like_c = round(hour["feels_like"] - 273.15)
        time_str = hour_ts.astimezone(zoneinfo.ZoneInfo("Europe/Warsaw")).strftime("%H:%M")
        results.append({"time": time_str,
                        "temperature": temp_c,
                        "feels_like": feels_like_c})
    return results
"""
    

def format_forecast_entry(entry):
    # forecast_time, temp, clouds, pop = entry
    return f"{entry['time']}:\nTemp {entry['temperature']}°C, Feels Like: {entry['feels_like']}"


def get_hours_forecast(complete_forecast: dict, hours=6) -> list[dict]:
    # data = fetch_forecast()
    # print(f"get_short_term_forecast.data = {data}")
    # sunset_time_unix, sunrise_time_unix = data["result"]["current"]["sunset"], data["result"]["current"]["sunrise"]
    # sunset_str = 
    # all_hours_sorted_ = sorted(complete_forecast["hourly"], key=lambda d: d["dt"])
    # hourly_forecast = extract_short_term_forecast(data["result"], hours=hours)
    for k in complete_forecast:
        print(f"  {k}")
    return sorted(complete_forecast["hourly"], key=lambda d: d["dt"])[1:hours+1]
    # return [format_forecast_entry(entry) for entry in short_term_forecast]

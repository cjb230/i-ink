import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://192.168.1.129:8080/data"


def fetch_forecast():
    print(f"Fetching weather from ({BASE_URL})...", end="")
    response = requests.get(BASE_URL, timeout=10)
    print(" fetched.")
    response.raise_for_status()
    return response.json()


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

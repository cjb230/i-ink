from datetime import datetime, timedelta, timezone
import zoneinfo


def printable_hour(unix_time: int) -> str:
    local_time = datetime.fromtimestamp(unix_time)
    return "24" if local_time.hour == 0 else str(local_time.hour)


def k_to_c_str(kelvin_temp: float) -> str:
    return str(round(kelvin_temp - 273.15)) + '°C'


def unix_ts_to_str(unix_time: int, format_mask: str = "%H:%M:%S") -> str:
    """
    Assumes unix time is in UTC.
    """
    dt_utc = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    return dt_utc.astimezone(zoneinfo.ZoneInfo("Europe/Warsaw")).strftime(format_mask).lstrip("0")


def uvi_to_str(uvi: float) -> str:
    return_str: str = ""
    if uvi < 2:
        return_str = "Low"
    elif uvi < 5:
        return_str = 'Moderate'
    elif uvi < 7:
        return_str = "High"
    elif return_str < 10:
        return_str = "Very high"
    else:
        return_str = "Extreme"
    return return_str


def hour_report(minute_conditions: list) -> dict:
    # it's probably sorted already, but let's be sure
    sorted_minutes = sorted(minute_conditions, key=lambda x: x["dt"])

    # forget the past
    now = int(datetime.now(timezone.utc).timestamp())
    future_minutes = [minute for minute in sorted_minutes if minute["dt"] > now]

    total_rain_mm = int(sum(minute["precipitation"] for minute in future_minutes)/60)
    if future_minutes[0]["precipitation"] > 0:  # raining now
        rain_stop = next((minute["dt"] for minute in future_minutes if minute["precipitation"] == 0), None)
        if rain_stop:
            rain_str = f"Rain stops: {unix_ts_to_str(rain_stop, '%H:%M')}"
        else:
            rain_str = f"{total_rain_mm} mm rain this hour"
    else:  # not raining now
        rain_start = next((minute["dt"] for minute in future_minutes if minute["precipitation"] > 0), None)
        if rain_start:
            rain_str = f"Rain starts: {unix_ts_to_str(rain_start, '%H:%M')}"
        else:
            rain_str = "No rain this hour"
    return rain_str


def alert_to_str(alert: dict) -> str:
    return_str = alert["event"]
    return return_str


def transform_weather(weather_data) -> dict:
    results = {}
    results["update_str"] = weather_data["timestamp"]

    results["hourly"] = weather_data["result"]["hourly"][1:5]
    for hour in results["hourly"]:
        hour["hour_str"] = printable_hour(unix_time=hour["dt"])
        del hour["dt"]

    results["daily"] = weather_data["result"]["hourly"][1:5]

    dt_utc = datetime.fromisoformat(weather_data["timestamp"])
    time_str = dt_utc.astimezone(zoneinfo.ZoneInfo("Europe/Warsaw")).strftime("%H:%M:%S")
    results["update_str"] = time_str
    results["current"] = weather_data["result"]["current"]

    
    temp_str = f"Temp: {k_to_c_str(results["current"]["temp"])}"
    feels_like_str = f"Feels like: {k_to_c_str(results["current"]["feels_like"])}"
    sunrise_str = f"Sunrise: {unix_ts_to_str(results["current"]["sunrise"])}"
    sunset_str = f"Sunset: {unix_ts_to_str(results["current"]["sunset"])}"
    uvi_str = f"UV Index: {uvi_to_str(results["current"]["uvi"])}"
    rain_str = hour_report(weather_data["result"]["minutely"])
    if "alerts" in weather_data["result"]:
        results["current"]["alert_str"] = alert_to_str(weather_data["result"]["alerts"][0])
    results["current"]["sunrise_str"] = sunrise_str
    results["current"]["sunset_str"] = sunset_str

    text_lines = [temp_str]
    if abs(results["current"]["temp"]-results["current"]["feels_like"]) > 4:
        text_lines.append(feels_like_str)
    if results["current"]["uvi"] > 2:
        text_lines.append(uvi_str)
    else:
        text_lines.append("")

    text_lines.append(rain_str)
    results["current"]["text_lines"] = text_lines
    return results


def transform_trains(trains_data, max_display=3, earliest_minutes_ahead=1) -> dict:
    now = datetime.now().time()
    results = {"warsaw": [],  "podkowa_lesna": []}

    timestamp_str = trains_data["timestamp"]
    del trains_data["timestamp"]

    for train_direction, train_list in trains_data.items():
        for train_time, train_no in train_list:
            if train_time > now:
                delta = datetime.combine(datetime.today(), train_time) - datetime.combine(datetime.today(), now)
                if delta >= timedelta(minutes=earliest_minutes_ahead):
                    results[train_direction].append((train_time, train_no))
                if len(results) == max_display:
                    break

    dt_utc = datetime.fromisoformat(timestamp_str)
    results["update_str"] = dt_utc.astimezone(zoneinfo.ZoneInfo("Europe/Warsaw")).strftime("%H:%M:%S")

    return results
